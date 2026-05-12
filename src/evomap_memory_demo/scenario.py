from __future__ import annotations

from dataclasses import dataclass


USER_PROMPT = (
    "日语工作坊网站已经有 17000 多个日语单词和对应照片。"
    "我想按场景筛选一批词，生成跟读视频合集；视频生成过程中会产生"
    "单词场景、例句图片和音频，这些又要反哺回网站展示。"
    "你帮我设计一个最小复现流程。"
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
        "Independent developer maintaining a Japanese Workshop website and a "
        "Japanese shadowing-video workflow that should feed each other."
    ),
    prompt=USER_PROMPT,
    projects=(
        "japanese-workshop-site",
        "japanese-shadowing-video",
    ),
    infra_aliases={
        "db": "db-primary",
        "media_store": "learning-media-store",
        "website": "japanese-workshop-web",
        "video_workspace": "shadowing-video-workspace",
    },
    source_threads=(
        SourceThread(
            "thread-workshop",
            "website-source",
            (
                "Japanese Workshop already has 17,000+ vocabulary records and "
                "17,000 generated photos. The website is the source of truth "
                "for word_id, reading, meaning, photo object_key, and audio."
            ),
        ),
        SourceThread(
            "thread-video",
            "video-consumer",
            (
                "Shadowing videos should select words by scene, generate a "
                "video collection, and create example sentences, sentence "
                "images, and narration audio from the selected words."
            ),
        ),
        SourceThread(
            "thread-feedback",
            "feedback-rule",
            (
                "Validated rule: video-generated scene labels, example "
                "sentence images, and audio should feed back into the website "
                "through stable word_id/object_key manifests, not duplicated "
                "word records."
            ),
        ),
    ),
    distractor_threads=(
        SourceThread(
            "thread-noise-1",
            "distractor",
            (
                "User discusses UI color choices and title typography for a "
                "Japanese Workshop landing page. This should not affect the "
                "website-video feedback-loop decision."
            ),
        ),
        SourceThread(
            "thread-noise-2",
            "distractor",
            (
                "User discusses background music and opening animation timing "
                "for shadowing videos. This may matter later, but it should "
                "not replace the data-feedback Gene."
            ),
        ),
    ),
    memory_assets=(
        MemoryAsset(
            "Gene",
            "workshop-shadowing-feedback-loop",
            (
                "Use Japanese Workshop word_id records as the source of truth. "
                "Build shadowing-video collections from scene-filtered words. "
                "Write video-generated scene labels, example sentence images, "
                "and audio back to the website through stable manifests."
            ),
            (
                "17000",
                "17000多",
                "日语工作坊",
                "跟读",
                "单词",
                "场景",
                "例句",
                "照片",
                "音频",
                "图片",
                "网站",
                "视频",
                "合集",
                "反哺",
                "复用",
            ),
        ),
        MemoryAsset(
            "Capsule",
            "workshop-shadowing-positive-feedback-case",
            (
                "Positive evidence that a website-to-video-to-website loop "
                "works: Workshop vocabulary/photos feed scene-based shadowing "
                "videos, while video scene labels, example images, and audio "
                "feed back into Workshop display."
            ),
            (
                "日语",
                "日语工作坊",
                "跟读视频",
                "单词",
                "17000",
                "照片",
                "场景",
                "例句",
                "音频",
                "图片",
                "网站",
                "视频",
                "合集",
                "反哺",
                "复用",
                "word_id",
                "object_key",
                "manifest",
            ),
        ),
    ),
)
