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


## 手动更新整套 Skill 与原子资料

在 Agent 中输入 `$commercial-case-library 更新 skill 和原子库`，也可在任意子 skill 后输入“检查更新 / 更新 skill”。

直接运行已安装 skill 的 `python "{skillDir}/tools/update_skill.py"`；加 `--check` 仅检查。无需 Git 或 GitHub 登录，更新来自本仓库 main 的固定提交；覆盖前自动备份，失败回滚。已有安装需先重新安装一次以获得此入口：

```text
npx -y skills add FocusLiz-Lab/commercial-case-library -g --all
```

原子更新直接读取 main 中最新资料，不依赖旧 Release。备份目录及提交号由脚本返回。自定义安装位置可用 `--skills-dir` 指向各 skill 文件夹的共同父目录。
