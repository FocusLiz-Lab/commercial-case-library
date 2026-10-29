# commercial-case-library

共享商业案例原子库，供 `dkskill`、`lhskill`、`openskill` 等 SkillHub 复用。

## 数据文本检查

发布数据使用中性称呼，不保留受限品牌名称及其拼音、缩写、推广域名和联系方式。兼容字符、全角写法及不可见字符也纳入检查。

提交前运行 `python tools/sanitize_case_text.py --check`，校验全部季度记录及清单大小。需要清理时运行 `python tools/sanitize_case_text.py --write`，再执行只读检查。处理保留记录数量和稳定 ID，原文摘录中的受限名称会被替换，不能将处理后的摘录当作逐字原文引用。GitHub Actions 会对新提交自动执行检查。

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

## 独立更新命令

安装最新整套 skills 后，在 Agent 中直接输入：

```text
$commercial-case-library-update
```

自动检查并更新本工具箱的整套 skill 和原子资料。仅检查时输入 `$commercial-case-library-update 检查更新`。旧安装可先使用已有更新路由，或执行以下命令获取新入口，再刷新宿主技能列表：

```text
npx -y skills add FocusLiz-Lab/commercial-case-library -g --all
```
