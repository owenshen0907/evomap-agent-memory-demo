#!/usr/bin/env python3
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evomap_memory_demo.validation import validate_recall  # noqa: E402


def main() -> int:
    result = validate_recall()
    print(result.to_text())
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
