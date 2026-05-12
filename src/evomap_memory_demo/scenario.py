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
    triggers: tuple[str, ...]


@dataclass(frozen=True)
class SourceThread:
    thread_id: str
    role: str
    evidence: str


@dataclass(frozen=True)
class Scenario:
    persona: str
    prompt: str
    projects: tuple[str, ...]
    infra_aliases: dict[str, str]
    source_threads: tuple[SourceThread, ...]
    distractor_threads: tuple[SourceThread, ...]
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
    source_threads=(
        SourceThread(
            "thread-a",
            "background",
            (
                "User explains that an existing asset-publishing skill works "
                "for one concrete website workflow, but becomes brittle when "
                "the same learning assets must be reused by apps and video."
            ),
        ),
        SourceThread(
            "thread-b",
            "correction",
            (
                "User corrects an agent that tried to store permanent full "
                "asset URLs in the database; the safer rule is to store "
                "object_key and resolve URLs by region."
            ),
        ),
        SourceThread(
            "thread-c",
            "validation",
            (
                "A text-only validation records that asset_manifest plus "
                "AssetUrlResolver is the reusable plan for web, apps, and "
                "video jobs."
            ),
        ),
    ),
    distractor_threads=(
        SourceThread(
            "thread-noise-1",
            "distractor",
            (
                "User discusses UI color choices and title typography for a "
                "Japanese-learning landing page. This should not affect asset "
                "storage or URL-resolution decisions."
            ),
        ),
        SourceThread(
            "thread-noise-2",
            "distractor",
            (
                "User discusses background music and opening animation timing "
                "for short videos. This is useful context for video editing, "
                "but not the Gene needed for shared asset reuse."
            ),
        ),
    ),
    memory_assets=(
        MemoryAsset(
            "Gene",
            "shared-asset-pipeline-invariant",
            (
                "Store object_key and metadata in DB, never fixed full URLs. "
                "Generate region-specific URLs through AssetUrlResolver. Treat "
                "asset_manifest as the shared source for web, apps, and video."
            ),
            (
                "N5",
                "单词",
                "音频",
                "插图",
                "素材",
                "网站",
                "app",
                "视频",
                "国内",
                "海外",
                "OSS",
                "复用",
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
            (
                "日语",
                "N5",
                "单词",
                "素材",
                "网站",
                "app",
                "视频",
                "国内",
                "海外",
                "复用",
                "learning",
                "website",
                "apps",
                "video",
                "oss-cn-assets",
                "server-global-edge",
                "asset_manifest",
                "AssetUrlResolver",
                "object_key",
            ),
        ),
    ),
)
