from __future__ import annotations

from dataclasses import asdict, dataclass

from .scenario import SCENARIO, Scenario


WITHOUT_EVOMAP_RESPONSE = """我需要先确认一些信息：
1. 日语工作坊的 17000 多个单词表结构是什么？照片和音频分别存在哪里？
2. 场景分类是已有字段，还是需要重新让模型给单词打标签？
3. 跟读视频合集的生成脚本读取数据库、CSV、JSON，还是直接从网站接口拉取？
4. 视频生成出的例句图片和音频要回写到网站哪张表？
5. 网站展示时，应该直接引用视频产物路径，还是复制一份素材？

在确认这些之前，我只能给一个通用方案。可能的方向有三种：
- 网站和视频各自维护一套单词/素材数据，但以后会不同步。
- 视频脚本直接扫网站素材目录，但很难把例句图片和音频回写到网站。
- 建一套 manifest，但需要先确认网站和视频之间的主从关系。

请你先提供网站数据结构、视频脚本入口、现有素材路径和回写方式。"""


WITH_EVOMAP_RESPONSE = """这是一个日语工作坊网站和跟读视频互相反哺的任务，我先复用了 workshop-shadowing-feedback-loop Gene，以及它的正向 Capsule 证据。

我按这些已知约定落最小实现：
1. 以日语工作坊的 `word_id` 为主键，不复制一套视频专用单词表。
2. 从 17000 多个单词里筛选一个最小场景包，例如 `scene=restaurant`，生成 `scene_word_set`。
3. 跟读视频只读取 `scene_word_set` 和已有单词照片/音频，生成 `video_collection_manifest`。
4. 视频阶段生成的例句、例句图片、旁白音频，写入 `word_learning_assets`，仍然挂回原始 `word_id`。
5. 网站展示读取 `word_learning_assets`，把“场景、跟读视频、例句图片、音频”补回单词详情页。

最小垂直切片：
- 从网站词库里选 8 个餐厅场景单词。
- 生成一份 `scene_word_set_restaurant.json`。
- 为其中 3 个词生成例句、例句图片和跟读音频。
- 生成一个 30 秒跟读视频合集 manifest。
- 把新产生的场景标签、例句图片 object_key、音频 object_key 回写到网站展示 manifest。

我只需要你确认两件真实运行前必须确认的事：
- 是否允许我新增或修改网站的学习素材 manifest / migration？
- 是否允许我执行真实的视频渲染和素材上传？"""


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
                "SIMULATED_SOURCE_THREADS",
                "=" * 78,
            ]
        )
        lines.extend(
            f"- {thread.thread_id} [{thread.role}]: {thread.evidence}"
            for thread in self.scenario.source_threads
        )
        lines.extend(
            [
                "",
                "DISTRACTOR_THREADS",
                "=" * 78,
            ]
        )
        lines.extend(
            f"- {thread.thread_id} [{thread.role}]: {thread.evidence}"
            for thread in self.scenario.distractor_threads
        )
        lines.extend(
            [
                "",
                "EVOLVER_DISTILLATION",
                "=" * 78,
                "The simulated source threads produce these reusable assets:",
            ]
        )
        lines.extend(
            f"- {asset.kind} {asset.asset_id}: {asset.summary}"
            for asset in self.scenario.memory_assets
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
                "NEW_THREAD_WITH_EVOMAP_RECALL",
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
        source_threads = "\n".join(
            f"- **{thread.thread_id} / {thread.role}**: {thread.evidence}"
            for thread in self.scenario.source_threads
        )
        distractor_threads = "\n".join(
            f"- **{thread.thread_id} / {thread.role}**: {thread.evidence}"
            for thread in self.scenario.distractor_threads
        )
        recall_hits = "\n".join(
            f"- **{asset.kind} `{asset.asset_id}`**: {asset.summary}"
            for asset in self.scenario.memory_assets
        )
        return f"""# EvoMap Agent Memory Demo

## What This Demo Reproduces

This is a text-only reproduction of cross-thread experience reuse. It does not
upload files, run database migrations, or call real infrastructure.

## Simulated Source Threads

{source_threads}

## Distractor Threads

{distractor_threads}

## Simulated Evolver Distillation

{recall_hits}

## Prompt

```text
{self.scenario.prompt}
```

## Without EvoMap

```text
{self.without_evomap}
```

## New Thread With EvoMap Recall

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
