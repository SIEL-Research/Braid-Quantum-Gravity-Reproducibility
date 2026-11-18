import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUPPLEMENT = ROOT / "reproduction" / "v1.2"


class CurrentReproductionTest(unittest.TestCase):
    def test_statement_index_covers_current_inventory(self):
        items = json.loads((SUPPLEMENT / "statement_map.json").read_text())["entries"]
        identifiers = [item["id"] for item in items]
        inherited_theorems = {f"V110-THE-{n:02}" for n in range(1, 48) if n != 27}
        inherited_other = {f"V110-PRO-{n:02}" for n in range(1, 5)} | {"V110-COR-01", "V110-COR-02"}
        expected = inherited_theorems | inherited_other | {
            "V110-THE-27a", "V110-THE-27b", "V120-THE-01", "V120-THE-02", "V120-LEM-01",
        }
        self.assertCountEqual(identifiers, expected)
        index = (SUPPLEMENT / "THEOREM_EVIDENCE_INDEX_v1.2.md").read_text()
        rows = re.findall(r"(?m)^\| (V1(?:10|20)-[A-Z]+-\w+) \|", index)
        self.assertCountEqual(rows, identifiers)
        opens = {"V110-THE-16", "V110-THE-27b", "V110-THE-44"}
        self.assertEqual({item["id"] for item in items if item["evidence_kind"] == "open"}, opens)
        for item in items:
            if item["id"] in opens:
                self.assertIsNone(item["legacy_id"], item["id"])
                self.assertEqual(item["proof_route"], "OPEN_INTERFACES.md")

    def test_local_routes_resolve(self):
        docs = [ROOT / "README.md", *SUPPLEMENT.glob("*.md")]
        for doc in docs:
            for url in re.findall(r"\[[^\]]+\]\(([^)]+)\)", doc.read_text()):
                if url.startswith(("https://", "http://", "#")):
                    continue
                path, _, fragment = url.partition("#")
                target = doc.parent / path
                self.assertTrue(target.exists(), (doc, url))
                if target.suffix == ".md" and fragment:
                    headings = re.findall(r"(?m)^#+ (.+)$", target.read_text())
                    slugs = {re.sub(r"[^\w -]", "", h.lower()).replace(" ", "-") for h in headings}
                    self.assertIn(fragment, slugs, (doc, url))

    def test_expected_exact_results(self):
        for name in ("pointing", "hda_example"):
            source = SUPPLEMENT / f"verify_{name}.py"
            result = json.loads(subprocess.check_output([sys.executable, str(source)]))
            expected = json.loads((SUPPLEMENT / f"expected_{name}.json").read_text())
            self.assertEqual(result, expected)
