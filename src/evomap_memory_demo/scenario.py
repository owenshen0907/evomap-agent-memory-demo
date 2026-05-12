from __future__ import annotations

from dataclasses import dataclass


USER_PROMPT = (
    "我要给 N5 单词卡生成一批音频和插图，上传到 OSS，并让网站、两个 app、"
    "视频剪辑流水线都能复用。国内用户走国内 OSS/CDN，海外用户走海外加速。"
    "你帮我设计并落地最小实现。"
)


@dataclass(frozen=True)
class MemoryAsset:
    kind: str
    asset_id: str
    summary: str


@dataclass(frozen=True)
class Scenario:
    persona: str
    prompt: str
    projects: tuple[str, ...]
    infra_aliases: dict[str, str]
    memory_assets: tuple[MemoryAsset, ...]


SCENARIO = Scenario(
    persona=(
        "Independent developer maintaining a Japanese-learning website, two "
        "mobile app lines, a short-video pipeline, and domestic/global infra."
    ),
    prompt=USER_PROMPT,
    projects=(
        "jp-workshop-web",
        "speak-practice-app",
        "grammar-helper-app",
        "short-video-pipeline",
    ),
    infra_aliases={
        "db": "db-primary",
        "storage": "oss-cn-assets",
        "domestic_app_server": "server-cn-app",
        "global_edge": "server-global-edge",
    },
    memory_assets=(
        MemoryAsset(
            "Gene",
            "shared-asset-pipeline-invariant",
            (
                "Store object_key and metadata in DB, never fixed full URLs. "
                "Generate region-specific URLs through AssetUrlResolver. Treat "
                "asset_manifest as the shared source for web, apps, and video."
            ),
        ),
        MemoryAsset(
            "Capsule",
            "shared-asset-pipeline-positive-jp-learning-stack",
            (
                "Positive evidence that the shared-asset Gene works for a "
                "Japanese-learning stack with db-primary, oss-cn-assets, "
                "server-cn-app, server-global-edge, and four shared data "
                "consumers."
            ),
        ),
    ),
)
