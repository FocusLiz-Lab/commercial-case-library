---
name: commercial-case-library
description: Shared commercial case atom library for multiple SkillHub packages. Use when a user asks to download, check, update, or search the shared business case library, or when another skill such as dkskill, lhskill, or openskill needs real business examples, commercial cases, benchmark projects, monetization examples, offer/pricing examples, 生财有术案例, or case-study evidence.
---

# commercial-case-library

This skill is the shared commercial case dependency for other skills. It prevents `dkskill`, `lhskill`, `openskill`, and future creator/business skills from downloading duplicate commercial-case atoms.

## Shared Location

Use this global location by default:

```text
~/.agents/shared/commercial-case-library/知识库/商业案例库/
```

Override with `COMMERCIAL_CASE_LIBRARY_HOME` only when the user explicitly needs a custom location.

## When Another Skill Needs Cases

If another skill detects the user needs business cases, benchmark examples, project teardowns, monetization examples, offer examples, pricing examples, or 生财有术案例:

1. Run `python scripts/check_cases.py`.
2. If available, use the returned path and continue the original task.
3. If missing, run python scripts/download_cases.py automatically.
4. Continue the original task after download succeeds.

Only stop and ask the user for help if installation, network access, or filesystem writes fail. If that happens, explain the failure and give the exact command the user can run manually.

## Commands

Check local status:

```powershell
python scripts/check_cases.py
```

Download or update the shared library:

```powershell
python scripts/download_cases.py
```

Search local cases:

```powershell
python scripts/search_cases.py "AI 工具 订阅" --limit 8
```

## Data Contract

The case library contains JSONL atom files:

```text
atoms.jsonl
atoms_2017Q1.jsonl
atoms_2017Q2.jsonl
...
```

For GitHub distribution, the full merged `atoms.jsonl` may be omitted to avoid large single-file downloads. Treat `commercial_cases_manifest.json` plus `atoms_*.jsonl` as the canonical shared library.

Each record follows the dbskill-style atom schema, commonly including:

- `id`
- `knowledge`
- `original`
- `date`
- `topics`
- `type`
- `title`
- `metrics`
- `commercial_use`
- `source`

Use `knowledge`, `title`, `topics`, `metrics`, and `commercial_use` for summaries. Avoid quoting long `original` passages.

## Boundary

- This skill is a shared local data dependency, not a strategy framework.
- Do not duplicate the commercial case library inside dependent skills.
- Do not answer with fabricated cases when the local library is missing.
- Do not expose private local paths unless needed for debugging.

