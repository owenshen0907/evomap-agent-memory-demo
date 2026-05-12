import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evomap_memory_demo.simulator import build_demo


class SimulatorTest(unittest.TestCase):
    def test_demo_contains_both_paths(self) -> None:
        demo = build_demo()

        self.assertIn("请你先提供服务器清单", demo.without_evomap)
        self.assertIn("asset_manifest", demo.with_evomap)
        self.assertIn("AssetUrlResolver", demo.with_evomap)

    def test_memory_assets_are_present(self) -> None:
        demo = build_demo()
        asset_ids = {asset.asset_id for asset in demo.scenario.memory_assets}

        self.assertIn("shared-asset-pipeline-invariant", asset_ids)
        self.assertIn("shared-asset-pipeline-positive-jp-learning-stack", asset_ids)


if __name__ == "__main__":
    unittest.main()
