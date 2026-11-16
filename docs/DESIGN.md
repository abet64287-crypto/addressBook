# 实现设计

## 架构

浏览器 HTML/CSS/JavaScript → Flask JSON API → 领域校验 → SQLite；Excel 模块与表单共用 `validate_contact`，保证两条输入路径有相同规则。

联系人为 `{id, name, company, group, notes, favorite, methods}`；`methods` 是 `{type, label, value}` 列表。SQLite 保存稳定 ID 和 JSON 联系人内容，SQL 使用绑定参数，连接在每次操作后关闭。对本次小型应用，JSON 结构方便保留不同类型和数量的联系方式；复杂分析或大规模查询可迁移至独立联系方式表。

## 收藏

`PATCH /api/contacts/<id>/favorite` 仅接受布尔状态；SQLite 单事务更新当前联系人收藏字段。前端显示星标、数量及收藏视图。刷新从数据库重新读取，收藏不依赖浏览器内存。

## 联系方式

列表允许电话、邮箱、社交账号、地址四类，每项有独立标签；编辑表单动态添加和移除。文本字段校验长度，邮箱校验基本格式，电话号码不转数字以保留区号和前导零。详情页按类型和标签展示。

## Excel

使用 openpyxl 生成真实 XLSX。一行一个联系人，固定基础列与按序号扩展的联系方式列。每条值和标签各占一列；导出标记为文本，避免表格软件解释用户输入为公式。导入检查文件、表头、行号、字段及公式，构建完整合法记录列表后才开启写入事务。完全相同记录跳过，其他新增，不执行覆盖更新。兼容格式见 README。

## 接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/contacts` | 所有联系人 |
| POST | `/api/contacts` | 新建 |
| PUT | `/api/contacts/<id>` | 更新完整联系人 |
| DELETE | `/api/contacts/<id>` | 删除 |
| PATCH | `/api/contacts/<id>/favorite` | 更新收藏 |
| GET | `/api/export` | 全量导出 |
| GET | `/api/template` | 空白兼容模板 |
| POST | `/api/import` | multipart `file` 字段导入 |

写请求要求 `X-Requested-With: AddressBook`，如果包含 Origin 则必须与当前服务相同；不启用跨站资源共享。前端渲染用户文本进行 HTML 转义，页面采用同源 CSP。**本版本无账号隔离与身份认证**，因此默认仅绑定回环地址；多人公网部署前须增加认证或使用网关访问控制。SQLite 适合单实例、小规模部署。
