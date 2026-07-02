from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from common import case_dir


REPO = "FocusLiz-Lab/commercial-case-library"
REMOTE_DIR = "知识库/商业案例库"


def fetch_json(url: str):
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as response:
        target.write_bytes(response.read())


def main() -> int:
    encoded_dir = urllib.parse.quote(REMOTE_DIR)
    api_url = f"https://api.github.com/repos/{REPO}/contents/{encoded_dir}?ref=main"
    items = fetch_json(api_url)
    files = [item for item in items if item.get("type") == "file"]
    if not files:
        print(f"未在 GitHub 仓库中找到 {REMOTE_DIR}。", file=sys.stderr)
        return 1

    target_dir = case_dir()
    count = 0
    for item in files:
        name = item["name"]
        if not (name.endswith(".jsonl") or name.endswith(".json") or name.endswith(".md")):
            continue
        target = target_dir / name
        print(f"下载 {name} -> {target}")
        download(item["download_url"], target)
        count += 1

    print(json.dumps({"downloaded": count, "target_dir": str(target_dir)}, ensure_ascii=False, indent=2))
    return 0 if count else 1


if __name__ == "__main__":
    raise SystemExit(main())
