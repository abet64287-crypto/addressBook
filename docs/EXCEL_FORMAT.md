# Excel module — Member B

状态：2026 年 11 月 17 日，hajiyao 已通过 [0aff42a](https://github.com/abet64287-crypto/addressBook/commit/0aff42af796f91cc6eb13a95b1a64d50eda55eb3) 将 Excel 模块、交互脚本、测试及本说明上传到 main。

认领：队友。模块文件：`addressbook/excel.py`、`addressbook/excel_routes.py`、`addressbook/static/excel.js`、`tests/test_excel.py`。

## 格式

真正的 `.xlsx`，一个工作表，一位联系人一行。基础列：Name、Company、Group、Favorite、Notes；Name 必需。每条联系方式使用独立编号列，例如 Phone1 / Phone1Label、Phone2 / Phone2Label；Email、Social、Address 同理，编号 1–30。Favorite 为 Yes/No，导入也接受 true/false、1/0 和旧版中文布尔值。

导出自动按现有信息扩展列，所有用户值作为文本写入。旧版中文表头仍可导入；新模板和导出统一为英文。

## 规则

- 一次最多 1000 数据行、245 列、10 MB 请求、40 MB 解压内容。
- 校验所有记录后再调用 `store.import_contacts` 开启事务保存；错误行使整份拒绝，提供英文错误及行号。
- 完全相同记录（忽略联系方式顺序）跳过，同名不同内容新增，不覆盖已有联系人。
- 不接受公式或错误单元格。表格软件编辑电话号码时须保持文本格式，以免前导零提前丢失。

## 与 A 的接口

- A 的 `create_app` 注册 B 的 `excel_api` Blueprint；同源写保护由 A 统一执行。
- B 通过 `current_app.config['DATABASE']` 访问 A 的存储层；B 的解析使用 A 的 `validate_contact`。
- A 的 HTML 顺序加载 `app.js` 和 `excel.js`。B 的脚本复用 `api`、`refresh`、`toast`，A 提供这些公共函数；二者都是 defer 经典脚本。
- `/api/template`、`/api/export` 为 GET；`/api/import` 为 multipart POST，文件字段名为 `file`，结果为 imported/skipped/total。

## 验收

当前 main 已包含 A、B 两部分。发布前在最新检出版本运行 `python -m pytest -q tests/test_excel.py`，并实际演示模板下载、导出多条联系方式、向测试空数据库重新导入、重复导入、错误文件拒绝。截图或视频不能只用自动化结果代替。
