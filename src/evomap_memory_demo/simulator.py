from __future__ import annotations

from dataclasses import asdict, dataclass

from .scenario import SCENARIO, Scenario


WITHOUT_EVOMAP_RESPONSE = """我需要先确认一些信息：
1. 你的国内和海外服务器分别是什么角色？海外是 CDN、反向代理还是同步存储？
2. OSS 桶名、endpoint、CDN 域名是什么？是否已有签名 URL 规则？
3. 网站、两个 app、视频流水线分别读哪个数据库和接口？
4. 素材 URL 应该直接存数据库，还是每次运行时拼接？
5. 视频流水线是读数据库、CSV、JSON manifest，还是直接扫 OSS？

在确认这些之前，我只能给一个通用方案。可能的方向有三种：
- 每个项目各自上传和维护 URL，但会有重复数据。
- 把 OSS URL 直接存到词条表，但未来 CDN/海外域名变更会比较麻烦。
- 建一个 asset 表，但需要先确认所有项目的读取方式。

请你先提供服务器清单、数据库 schema、OSS 配置和现有项目结构。"""


WITH_EVOMAP_RESPONSE = """这是一个 substantive 任务，我先复用了已有的日语学习栈拓扑和共享素材 Gene。

我按这些已知约定落最小实现：
1. 新增 `asset_manifest`，作为网站、两个 app、视频流水线的共同事实源。
2. 上传音频/插图到 `oss-cn-assets`，数据库只保存 `object_key`、`sha256`、`asset_type`、`word_id`、`locale`、`status`。
3. 不把完整 URL 写入数据库；新增 `AssetUrlResolver(region, object_key)`。
4. `region=cn` 时返回国内 OSS/CDN URL；`region=global` 时返回 `server-global-edge` 加速 URL。
5. 网站和 app 通过 API 读 manifest；视频流水线读取 manifest snapshot，避免每个项目各写一套路径规则。

最小垂直切片：
- 先选 3 个 N5 单词生成 audio + image。
- 上传到 OSS 并校验 sha256。
- 写入 `asset_manifest`。
- 在 API 返回 `asset_urls.cn` 和 `asset_urls.global`。
- 视频导出一份 `asset_manifest_n5_sample.json` 做验证。

我只需要你确认两件真实运行前必须确认的事：
- 是否允许我写数据库 migration？
- 是否允许我用当前环境里的 OSS 凭证执行真实上传？"""


@dataclass(frozen=True)
class DemoResult:
    scenario: Scenario
    without_evomap: str
    with_evomap: str

    def to_dict(self) -> dict:
        return {
            "scenario": asdict(self.scenario),
            "without_evomap": self.without_evomap,
            "with_evomap": self.with_evomap,
        }

    def to_text(self) -> str:
        lines = [
            "SCENARIO",
            "=" * 78,
            f"Persona: {self.scenario.persona}",
            "Projects: " + ", ".join(self.scenario.projects),
            "Infra aliases:",
        ]
        lines.extend(
            f"- {name}: {alias}"
            for name, alias in self.scenario.infra_aliases.items()
        )
        lines.extend(
            [
                "",
                "WITHOUT_EVOMAP",
                "=" * 78,
                "User prompt:",
                self.scenario.prompt,
                "",
                "Likely agent response:",
                self.without_evomap,
                "",
                "WITH_EVOMAP",
                "=" * 78,
                "User prompt:",
                self.scenario.prompt,
                "",
                "Recall hits:",
            ]
        )
        lines.extend(
            f"- {asset.kind} {asset.asset_id}: {asset.summary}"
            for asset in self.scenario.memory_assets
        )
        lines.extend(["", "Agent response after recall:", self.with_evomap])
        return "\n".join(lines)

    def to_markdown(self) -> str:
        recall_hits = "\n".join(
            f"- **{asset.kind} `{asset.asset_id}`**: {asset.summary}"
            for asset in self.scenario.memory_assets
        )
        return f"""# EvoMap Agent Memory Demo

## Prompt

```text
{self.scenario.prompt}
```

## Without EvoMap

```text
{self.without_evomap}
```

## Recall Hits

{recall_hits}

## With EvoMap

```text
{self.with_evomap}
```
"""


def build_demo() -> DemoResult:
    return DemoResult(
        scenario=SCENARIO,
        without_evomap=WITHOUT_EVOMAP_RESPONSE,
        with_evomap=WITH_EVOMAP_RESPONSE,
    )
