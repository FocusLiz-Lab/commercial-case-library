from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import usable_case_dir

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def iter_records(path: Path):
    files = [path / "atoms.jsonl"] if (path / "atoms.jsonl").exists() else sorted(path.glob("atoms_*.jsonl"))
    for file in files:
        with file.open("r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue


def score_record(record: dict, terms: list[str]) -> int:
    haystack = " ".join(
        str(record.get(key, ""))
        for key in ("title", "heading", "knowledge", "commercial_use", "topics", "project_types", "platforms")
    ).lower()
    return sum(haystack.count(term.lower()) for term in terms)


def compact(record: dict, score: int) -> dict:
    return {
        "score": score,
        "id": record.get("id"),
        "date": record.get("date"),
        "title": record.get("title") or record.get("heading"),
        "topics": record.get("topics", []),
        "metrics": record.get("metrics", []),
        "knowledge": record.get("knowledge"),
        "commercial_use": record.get("commercial_use"),
    }


def date_key(item: dict) -> str:
    date = str(item.get("date") or "")
    return date[:10]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    path = usable_case_dir()
    if not path:
        print(json.dumps({"available": False, "results": []}, ensure_ascii=False, indent=2))
        return 1

    terms = [term for term in args.query.replace("，", " ").replace(",", " ").split() if term]
    results = []
    for record in iter_records(path):
        score = score_record(record, terms)
        if score > 0:
            results.append(compact(record, score))

    results.sort(key=lambda item: (date_key(item), item["score"]), reverse=True)
    print(json.dumps({"available": True, "case_dir": str(path), "results": results[: args.limit]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
