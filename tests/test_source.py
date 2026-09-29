import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bqg_v1 import verify_source_class


class CanonicalSourceTest(unittest.TestCase):
    def test_exact_source_class(self):
        actual = verify_source_class(ROOT / "data/canonical_source_class_v1.json")
        expected = json.loads(
            (ROOT / "expected/source_verification_v1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
