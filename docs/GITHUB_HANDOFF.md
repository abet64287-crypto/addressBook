# 两人上传同一个仓库，再由服务器从 GitHub 部署

仓库：<https://github.com/abet64287-crypto/addressBook>。首次检查时仓库为空；成员 A 按功能分批上传，记录见 [UPLOAD_RECORD.md](UPLOAD_RECORD.md)。你负责 A，队友负责 B；两包互不覆盖，合并后才是可运行项目，不是两个独立应用。

## 包内容

| 包 | 负责人 | 内容 |
| --- | --- | --- |
| `address-book-A.zip` | 你 | 联系人模型、数据库、收藏和联系人 API、主界面、公共前端函数、联系人及部署测试、运行配置和部署文件、项目文档 |
| `address-book-B.zip` | 队友 | Excel 读写、Excel Blueprint 接口、前端导入交互、Excel 测试、格式说明 |

包里的路径就是仓库根目录路径。不要把 ZIP 本身作为源码上传，不要多套 A、B、address-book 等目录。仓库根目录应直接看到 README.md、run.py、requirements.txt、addressbook/、tests/ 和 deploy/。

两包的文件清单与 SHA-256 在交付目录 `file-ownership.json` 中。服务器数据库、虚拟环境、缓存和 Git 元数据不包含在包内。

## 第一步：你上传 A

1. 解压 `address-book-A.zip` 到本机新文件夹。
2. 打开空的 GitHub 仓库，使用 **uploading an existing file** 入口。
3. 拖入解压目录内的文件和文件夹（包括 .gitignore、.gitattributes），不是外层文件夹。
4. 阅读、检查自己负责的代码，以自己的账号提交到 main。提交说明可用 `feat: add contact management, favorites and UI`。
5. A 上传后暂缺 Excel 模块，不能启动 / 部署，这是分批集成的中间状态。

每位成员按认领范围理解、验证、改进和交叉评审，并根据实际参与填写分工及贡献记录。

## 第二步：队友上传 B 并发起 PR

1. 你在仓库 Settings → Collaborators 邀请队友，队友接受邀请；如果不加入协作者，可由队友 Fork 后发 PR。
2. 队友解压 `address-book-B.zip`，在自己的 GitHub 账号下基于 main 创建 `feature/excel-transfer` 分支。
3. 打开该分支，用 Add file → Upload files 上传 B 包的内部内容，保留原路径。
4. 文件夹合并是新增内部文件，不替换 A 的整个文件夹。提交前确认差异只包含 B 的五个文件，没有删除 A 文件。
5. 队友创建 PR，方向为 `feature/excel-transfer` → `main`。你评审 Excel 代码并在完整代码上验收后合并。
6. 如走 Fork，PR 的目标是本团队仓库的 main。

B 五个文件：

```text
addressbook/excel.py
addressbook/excel_routes.py
addressbook/static/excel.js
tests/test_excel.py
docs/EXCEL_FORMAT.md
```

## 第三步：集成验收与版本发布

完整仓库中执行：

```text
python -m pip install -r requirements-dev.txt
python -m pytest -q
node --check addressbook/static/app.js
node --check addressbook/static/excel.js
```

再录制全部功能的操作视频。把实际验收日期、版本、结果与本人问题补到文档，形成有意义的第三次提交；原题要求至少三次提交，不依赖空提交或只修改作者。你和队友用各自账号形成真实提交，保存 PR、提交次数和截图。

通过后发布 Release（例如 v1.0.0），两人各自写 PSP 和个人博客。贡献比例按实际工作共同确定，不按包大小或提交次数直接推断。

## 第四步：Ubuntu 从 GitHub 拉取

等 A、B 均在 main，进入现有 TAT 免密终端即可。仓库是公开仓库，HTTPS clone 不需要你本机配置 SSH。

```bash
sudo apt-get update
sudo apt-get install -y git
git clone --branch main --single-branch https://github.com/abet64287-crypto/addressBook.git "$HOME/addressBook-deploy"
cd "$HOME/addressBook-deploy"
git log -1 --oneline
sudo bash deploy/ubuntu/install.sh
```

若 `addressBook-deploy` 已存在，先确认其来源及工作状态，不要删除后重试，也不要重复执行初装。若已经安装到 `/opt/address-book`，请先检查当前服务和数据，使用适合现状的更新流程。

安装器会确认 B 的三个运行模块存在，并在 `/opt/address-book/REVISION` 保存拉取的 Git 提交，便于核验实际部署版本。

检查本地服务：

```bash
systemctl is-active address-book calculator-api caddy
curl -fsS http://127.0.0.1:8001/api/health
curl -fsS http://127.0.0.1:8000/api/health
```

然后按 [DEPLOYMENT.md](DEPLOYMENT.md) 第 3–5 节配置 DNS 和新增 Caddy 站点，验证公网浏览器读写；不要覆盖计算器的 Caddy 配置。

## 当前状态

已完成本地模块拆分、交付包及合并验证；本次仅分批提交 A 部分。未代队友提交 B，未创建 PR、邀请协作者或操作云服务器。原题的指定 Fork 条款仍待确认；按用户选择使用该新建团队仓库。
