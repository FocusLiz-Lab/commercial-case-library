from __future__ import annotations

import json
from pathlib import Path

from common import case_dir, candidate_case_dirs, usable_case_dir


def file_count(path: Path) -> int:
    return len([p for p in path.glob("*") if p.is_file()])


def main() -> int:
    found = usable_case_dir()
    payload = {
        "available": found is not None,
        "shared_dir": str(case_dir()),
        "active_dir": str(found) if found else None,
        "checked": [str(path) for path in candidate_case_dirs()],
        "file_count": file_count(found) if found else 0,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if found else 1


if __name__ == "__main__":
    raise SystemExit(main())
