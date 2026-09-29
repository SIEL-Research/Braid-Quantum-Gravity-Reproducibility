#!/usr/bin/env python3
"""Extract theorem-like environments from a LaTeX manuscript."""

import argparse
import json
from pathlib import Path
import re


PATTERN = re.compile(
    r"\\begin\{(theorem|proposition|lemma|corollary)\}"
    r"(?:\[([^]]+)\])?(.*?)\\end\{\1\}",
    re.DOTALL,
)


def inventory(tex_path: Path, id_prefix: str) -> dict:
    source = tex_path.read_text(encoding="utf-8")
    lines = source.splitlines()
    counters: dict[str, int] = {}
    records = []
    for match in PATTERN.finditer(source):
        kind, title, body = match.groups()
        counters[kind] = counters.get(kind, 0) + 1
        prefix = {
            "theorem": "THE",
            "proposition": "PRO",
            "lemma": "LEM",
            "corollary": "COR",
        }[kind]
        line = source.count("\n", 0, match.start()) + 1
        records.append(
            {
                "id": f"{id_prefix}-{prefix}-{counters[kind]:02d}",
                "kind": kind,
                "title": title or "",
                "line": line,
                "statement": " ".join(body.split()),
            }
        )
    return {
        "schema": "siel.bqg.theorem-inventory.v1",
        "manuscript": tex_path.name,
        "counts": {
            "theorem": counters.get("theorem", 0),
            "proposition": counters.get("proposition", 0),
            "lemma": counters.get("lemma", 0),
            "corollary": counters.get("corollary", 0),
            "total": len(records),
        },
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("tex", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--id-prefix", default="V099")
    args = parser.parse_args()
    result = inventory(args.tex, args.id_prefix)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
