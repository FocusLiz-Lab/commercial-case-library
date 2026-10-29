"""Validate or sanitize restricted references in distributed case text."""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "skills" / "commercial-case-library" / "知识库" / "商业案例库"
RESTRICTED = re.compile(
    r"\u751f\u8d22(?:\u6709\u672f)?|\u751f\u8ca1(?:\u6709\u8853)?"
    r"|\x73hengcai[a-z0-9]*|\x73cys[a-z0-9]*", re.IGNORECASE
)
IGNORED = re.compile(r"[\s\u200b-\u200f\u202a-\u202e\u2060-\u206f\ufeff]+")


def comparable(text: str) -> str:
    return IGNORED.sub("", unicodedata.normalize("NFKC", text))


def visible_text(text: str) -> tuple[str, list[int]]:
    """Map normalized matches back to the original without rewriting other text."""
    chars, offsets = [], []
    for index, char in enumerate(text):
        for normalized in unicodedata.normalize("NFKC", char):
            if not normalized.isspace() and unicodedata.category(normalized) != "Cf":
                chars.append(normalized)
                offsets.append(index)
    return "".join(chars), offsets


def sanitize(text: str) -> str:
    if not RESTRICTED.search(comparable(text)):
        return text
    # Remove promotional identifiers rather than inventing working replacements.
    text = re.sub(r"[（(]ID[：:]\s*\x73hengcai[a-z0-9]+[^）)]*[）)]", "", text, flags=re.I)
    text = re.sub(r"V[：:]\s*\x73hengcai[a-z0-9]+", "（联系方式已省略）", text, flags=re.I)
    text = re.sub(r"[：:]https___\x73cys\b", "", text, flags=re.I)
    text = re.sub(r"(?:https?://)?(?:www\.)?(?:\x73cys|\x73hengcaiyoushu)\.com(?:/[^\s，。；）)]*)?",
                  "相关案例页面", text, flags=re.I)
    text = re.sub(r"(提取码[：:]\s*)\x73cys\b", r"\1[已省略]", text, flags=re.I)
    text = re.sub(r"(优惠码[：:]\s*)\x73cys[a-z0-9]*", r"\1[已省略]", text, flags=re.I)
    text = re.sub(r"\x73hengcaiyoushu\b", "example", text, flags=re.I)
    normalized, offsets = visible_text(text)
    for match in reversed(list(RESTRICTED.finditer(normalized))):
        start, end = offsets[match.start()], offsets[match.end() - 1] + 1
        text = text[:start] + "商业社区" + text[end:]
    return text


def transform(value):
    if isinstance(value, str):
        return sanitize(value)
    if isinstance(value, list):
        return [transform(item) for item in value]
    if isinstance(value, dict):
        return {sanitize(key): transform(item) for key, item in value.items()}
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Sanitize files and refresh manifest sizes")
    mode.add_argument("--check", action="store_true", help="Read-only validation (default)")
    args = parser.parse_args()
    files = sorted(DATA.glob("atoms*.jsonl"))
    if not files:
        raise ValueError("No case shards found")
    changed_files, changed_records, total, problems = 0, 0, 0, []
    for path in files:
        raw = path.read_bytes()
        lines = raw.decode("utf-8-sig").splitlines(keepends=True)
        output, changed = [], False
        for index, line in enumerate(lines, 1):
            if not line.strip():
                output.append(line)
                continue
            record = json.loads(line)
            total += 1
            cleaned = transform(record)
            if cleaned != record:
                problems.append(f"{path.name}:{index}")
                changed_records += 1
                if args.write:
                    if cleaned.get("id") != record.get("id"):
                        raise ValueError(f"Stable ID would change: {path.name}:{index}")
                    newline = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
                    line = json.dumps(cleaned, ensure_ascii=False, separators=(",", ":")) + newline
                    changed = True
            output.append(line)
        if changed:
            path.write_bytes("".join(output).encode("utf-8"))
            changed_files += 1
    # Scan all tracked text too, including samples and escaped JSON strings.
    # Repository metadata and local caches are intentionally excluded.
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", "__pycache__"} for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix not in {".md", ".py", ".json", ".yml", ".yaml", ".txt"}:
            continue
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig")
        if path.suffix == ".json":
            text = json.dumps(json.loads(text), ensure_ascii=False)
        if RESTRICTED.search(comparable(text)):
            problems.append(str(path.relative_to(ROOT)))
            if args.write and path.suffix != ".json":
                path.write_bytes(sanitize(raw.decode("utf-8-sig")).encode("utf-8"))
    manifest_path = DATA / "commercial_cases_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    if set(entry["file"] for entry in manifest["files"]) != {p.name for p in files}:
        raise ValueError("Manifest shard list differs from actual files")
    if manifest["file_count"] != len(files):
        raise ValueError("Manifest shard count differs from actual files")
    for entry in manifest["files"]:
        actual = (DATA / entry["file"]).stat().st_size
        if entry["bytes"] != actual:
            if args.write:
                entry["bytes"] = actual
            else:
                problems.append(f"Manifest size mismatch: {entry['file']}")
    if args.write:
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": total, "shards": len(files), "affected_records": changed_records,
                      "written_shards": changed_files, "findings": problems}, ensure_ascii=False, indent=2))
    return 0 if args.write or not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
