import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evomap_memory_demo.simulator import build_demo
from evomap_memory_demo.validation import validate_recall


class SimulatorTest(unittest.TestCase):
    def test_demo_contains_both_paths(self) -> None:
        demo = build_demo()

        rendered = demo.to_text()

        self.assertIn("SIMULATED_SOURCE_THREADS", rendered)
        self.assertIn("DISTRACTOR_THREADS", rendered)
        self.assertIn("EVOLVER_DISTILLATION", rendered)
        self.assertIn("NEW_THREAD_WITH_EVOMAP_RECALL", rendered)
        self.assertIn("请你先提供服务器清单", demo.without_evomap)
        self.assertIn("asset_manifest", demo.with_evomap)
        self.assertIn("AssetUrlResolver", demo.with_evomap)

    def test_memory_assets_are_present(self) -> None:
        demo = build_demo()
        asset_ids = {asset.asset_id for asset in demo.scenario.memory_assets}

        self.assertIn("shared-asset-pipeline-invariant", asset_ids)
        self.assertIn("shared-asset-pipeline-positive-jp-learning-stack", asset_ids)

    def test_source_threads_are_present(self) -> None:
        demo = build_demo()
        roles = {thread.role for thread in demo.scenario.source_threads}

        self.assertEqual({"background", "correction", "validation"}, roles)

    def test_distractor_threads_are_present(self) -> None:
        demo = build_demo()
        roles = {thread.role for thread in demo.scenario.distractor_threads}

        self.assertEqual({"distractor"}, roles)

    def test_recall_validation_passes_with_distractors(self) -> None:
        result = validate_recall()
        recalled_ids = {asset.asset_id for asset in result.recall_hits}

        self.assertTrue(result.passed)
        self.assertIn("shared-asset-pipeline-invariant", recalled_ids)
        self.assertIn("shared-asset-pipeline-positive-jp-learning-stack", recalled_ids)
        self.assertIn("DISTRACTOR_THREADS", result.to_text())


if __name__ == "__main__":
    unittest.main()
