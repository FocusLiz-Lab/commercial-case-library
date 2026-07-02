# commercial-case-library

共享商业案例原子库，供 `dkskill`、`lhskill`、`openskill` 等 SkillHub 复用。

默认共享下载位置：

```text
~/.agents/shared/commercial-case-library/知识库/商业案例库/
```

安装后可用：

```text
$commercial-case-library
```

安装目录结构为 `skills/commercial-case-library/`，安装器会把 `SKILL.md`、`scripts/` 和内置季度案例数据一起复制。首次需要共享库时会自动把内置数据复制到：

```text
~/.agents/shared/commercial-case-library/知识库/商业案例库/
```

常用脚本需在已安装的 `commercial-case-library` skill 目录内运行：

```powershell
python scripts/check_cases.py
python scripts/download_cases.py
python scripts/search_cases.py "AI 工具 订阅" --limit 8
```

数据采用季度 JSONL 拆分文件，清单见：

```text
知识库/商业案例库/commercial_cases_manifest.json
```
