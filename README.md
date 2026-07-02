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

常用脚本：

```powershell
python scripts/check_cases.py
python scripts/download_cases.py
python scripts/search_cases.py "AI 工具 订阅" --limit 8
```

数据采用季度 JSONL 拆分文件，清单见：

```text
知识库/商业案例库/commercial_cases_manifest.json
```
