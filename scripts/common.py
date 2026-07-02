from __future__ import annotations

import os
from pathlib import Path


def shared_root() -> Path:
    override = os.environ.get("COMMERCIAL_CASE_LIBRARY_HOME")
    if override:
        return Path(override).expanduser().resolve()
    return Path.home() / ".agents" / "shared" / "commercial-case-library"


def case_dir() -> Path:
    return shared_root() / "知识库" / "商业案例库"


def bundled_case_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "知识库" / "商业案例库"


def candidate_case_dirs() -> list[Path]:
    return [case_dir(), bundled_case_dir()]


def usable_case_dir() -> Path | None:
    for path in candidate_case_dirs():
        if (path / "commercial_cases_manifest.json").exists() or any(path.glob("atoms_*.jsonl")):
            return path
    return None
