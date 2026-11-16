# Address Book

> 当前 GitHub 交付范围为成员 A（联系人、收藏、界面和部署配置），按功能分批提交。成员 B 的 Excel 模块由队友后续提交；A 单独存在时不能启动或部署。完整本地项目已通过 30 项测试，仓库集成后需再次验收。上传记录见 `docs/UPLOAD_RECORD.md`（随最后一批材料提交）。

双人极限编程作业的本地实现：联系人管理、收藏、多种联系方式、Excel 导入导出。界面使用英文、响应式，无前端构建依赖。数据持久化到 SQLite。

团队仓库：<https://github.com/abet64287-crypto/addressBook>。你已选择 A（联系人管理、收藏与界面），队友负责 B（Excel 导入导出与校验），详见 [双人任务认领单](docs/TASK_CLAIMS.md)。

任务：<https://bbs.csdn.net/topics/620593436>；截止 **2026-11-17 23:59（北京时间）**。

## 快速运行（Windows PowerShell）

在本目录打开终端，建议使用 Python 3.12：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe seed_demo.py
.\.venv\Scripts\python.exe run.py
```

打开 <http://127.0.0.1:5000>。`seed_demo.py` 可选，只新增虚构演示联系人，不清空数据；相同演示记录会跳过。`PORT` 环境变量可修改端口。

已有依赖时也可直接 `python seed_demo.py`、`python run.py`。数据库自动建立于 `instance/contacts.sqlite3`，关闭后仍保留。备份请停服务后复制整个 `instance` 目录。该目录不上传 Git。

## 操作与功能

- 新建、编辑、删除联系人；按姓名、公司、分组或联系方式搜索，按分组筛选。
- 星标收藏、取消收藏、单独查看收藏；刷新和重启后保留。
- 一位联系人最多 120 条联系方式，每种最多 30 条，支持电话、邮箱、社交账号、地址及独立标签。
- 下载 Excel 模板、导入 `.xlsx`、导出所有联系人；界面显示导入新增/跳过数量和错误原因。
- 收藏状态、分组、备注和每条联系方式标签均可往返保存。

## Excel 格式

只接受一个工作表；一位联系人一行。基础列：`Name`（必需）、`Company`、`Group`、`Favorite`、`Notes`。
多值列：`Phone1`、`Phone1Label`、`Phone2`、`Phone2Label`，以此类推；`Email`、`Social`、`Address`同理。编号范围 1–30。推荐先下载模板；导出会按实际数据自动扩展列数。

- Favorite 填写“Yes/No”，空白视为否；也接受 true/false、1/0。
- 电话及账号应在 Excel 中设置为文本，避免前导零被表格软件提前删除；导出自动使用文本单元格。
- 整份文件校验通过后一次事务写入；有错误时整份不写入，反馈行号或表头问题。
- **全部字段相同（忽略联系方式排列顺序）才算重复**，跳过重复，不覆盖已有数据。同名但不同信息会新增。修改已有联系人请使用界面编辑。
- 每次最多 1000 数据行、245 列、10 MB 压缩文件和 40 MB 解压内容；超过 1000 位联系人时需分批导入。
- 不接受公式单元格；导出用户输入按文本处理。只导入文本值，不执行表格公式。

## 验证

```powershell
python -m pytest -q
node --check addressbook/static/app.js
```

测试使用临时数据库，不会修改正常使用的数据。覆盖 CRUD、持久化、收藏、多条信息、Excel 完整往返、重复策略、前导零、公式、错误导入的原子性、大小与行数限制等。

## 模块与后续双人协作

| 模块 | 文件 | 建议负责 |
| --- | --- | --- |
| 模型、校验、收藏和持久化 | `domain.py`、`store.py` | 成员 A |
| Excel 格式、读写及导入校验 | `excel.py` | 成员 B |
| HTTP 与联调 | `__init__.py` | 两人共同确认接口 |
| 界面交互和样式 | `templates/`、`static/` | 两人按功能分工 |
| 测试、评审、证据与博客 | `tests/`、`docs/` | 两人共同参与并分别记录 |

这是待实际认领的模块划分，不是对已经发生的双人贡献的声明。不要通过改 Git 作者或重复上传伪造参与。按用户指定的团队仓库协作，两人各自在真实账号、分支上完成认领、改进、测试与交叉评审，再合并；参见 [协作说明](docs/COLLABORATION.md)。

## 提交材料

- [题目逐项对照与当前状态](docs/DELIVERY_STATUS.md)
- [实现设计](docs/DESIGN.md)
- [代码规范](docs/CODING_STANDARDS.md)
- [博客模板和两张 PSP 表](docs/BLOG_TEMPLATE.md)
- [演示脚本与截图清单](docs/DEMO_SCRIPT.md)
- [发布与提交清单](docs/SUBMISSION_CHECKLIST.md)
- [可选部署说明](docs/DEPLOYMENT.md)

当前按 A/B 模块分批上传；成员 A 按功能提交，成员 B 等待队友提交。尚未发布 Release、发起团队集成 PR 或提交 CSDN 作业。用户选择的新建仓库非 Fork，原题该条款仍待确认。两人的贡献、PSP 实际时间、截图和视频须按实际情况补充。博客需要各自发布。

## Ubuntu 云部署

为现有 Caddy + 计算器（8000）准备了 [部署步骤](docs/DEPLOYMENT.md)、`deploy/ubuntu/install.sh` 和独立 systemd 服务（8001）。支持 `ADDRESSBOOK_DATABASE` 指定数据路径，新增 `/api/health`；远程尚未执行。

## 两人分包上传 GitHub

你上传 A（联系人与界面），队友上传 B（Excel），两包合并 main 后服务器直接从公开仓库 git clone。具体步骤见 [分包上传与部署](docs/GITHUB_HANDOFF.md)。测试已按职责拆为 tests/test_contacts.py、tests/test_excel.py、tests/test_deployment.py，共用 tests/conftest.py。
