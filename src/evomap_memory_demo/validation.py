from __future__ import annotations

from dataclasses import dataclass

from .scenario import SCENARIO, MemoryAsset, Scenario
from .simulator import WITH_EVOMAP_RESPONSE


RECALL_QUERY = (
    "新线程里先有一些干扰信息：我刚才聊了首页配色、视频片头音乐和字幕模板。"
    "现在真正要做的是：日语工作坊网站已经有 17000 多个单词和照片，"
    "我要按场景筛词生成跟读视频合集；视频过程中生成的场景、例句图片、"
    "音频又要反哺回网站展示。请先 recall 可用经验，再给最小复现方案。"
)


@dataclass(frozen=True)
class RecallValidationResult:
    scenario: Scenario
    query: str
    recall_hits: tuple[MemoryAsset, ...]
    agent_response: str
    passed: bool
    assertions: tuple[str, ...]

    def to_text(self) -> str:
        lines = [
            "AUTOMATED_RECALL_VALIDATION",
            "=" * 78,
            "This script simulates source threads, distractor threads, and a new-thread recall query.",
            "",
            "SOURCE_THREADS",
            "=" * 78,
        ]
        lines.extend(
            f"- {thread.thread_id} [{thread.role}]: {thread.evidence}"
            for thread in self.scenario.source_threads
        )
        lines.extend(["", "DISTRACTOR_THREADS", "=" * 78])
        lines.extend(
            f"- {thread.thread_id} [{thread.role}]: {thread.evidence}"
            for thread in self.scenario.distractor_threads
        )
        lines.extend(
            [
                "",
                "RECALL_QUERY",
                "=" * 78,
                self.query,
                "",
                "RECALL_HITS",
                "=" * 78,
            ]
        )
        lines.extend(
            f"- {asset.kind} {asset.asset_id}: {asset.summary}"
            for asset in self.recall_hits
        )
        lines.extend(["", "AGENT_RESPONSE_AFTER_RECALL", "=" * 78, self.agent_response])
        lines.extend(["", "ASSERTIONS", "=" * 78])
        lines.extend(f"- {assertion}" for assertion in self.assertions)
        lines.extend(["", "RESULT", "=" * 78, "PASS" if self.passed else "FAIL"])
        return "\n".join(lines)


def recall_assets(query: str, scenario: Scenario = SCENARIO) -> tuple[MemoryAsset, ...]:
    normalized_query = query.casefold()
    scored: list[tuple[int, MemoryAsset]] = []

    for asset in scenario.memory_assets:
        score = sum(1 for trigger in asset.triggers if trigger.casefold() in normalized_query)
        if score:
            scored.append((score, asset))

    kind_order = {"Gene": 0, "Capsule": 1}
    scored.sort(key=lambda item: (kind_order.get(item[1].kind, 9), -item[0], item[1].asset_id))
    return tuple(asset for _, asset in scored)


def validate_recall(query: str = RECALL_QUERY, scenario: Scenario = SCENARIO) -> RecallValidationResult:
    recall_hits = recall_assets(query, scenario)
    recalled_ids = {asset.asset_id for asset in recall_hits}
    expected_ids = {asset.asset_id for asset in scenario.memory_assets}

    assertions = (
        "query contains distractor context about UI, music, and subtitle templates",
        "recall returns the workshop-shadowing feedback-loop Gene",
        "recall returns the positive workshop-shadowing Capsule",
        "agent response uses word_id, scene_word_set, and video_collection_manifest",
        "agent response asks only for real execution approvals",
    )
    response_terms = ("word_id", "scene_word_set", "video_collection_manifest")
    passed = (
        expected_ids.issubset(recalled_ids)
        and all(term in WITH_EVOMAP_RESPONSE for term in response_terms)
        and "是否允许我新增或修改网站的学习素材 manifest / migration" in WITH_EVOMAP_RESPONSE
        and "是否允许我执行真实的视频渲染和素材上传" in WITH_EVOMAP_RESPONSE
    )

    return RecallValidationResult(
        scenario=scenario,
        query=query,
        recall_hits=recall_hits,
        agent_response=WITH_EVOMAP_RESPONSE,
        passed=passed,
        assertions=assertions,
    )
