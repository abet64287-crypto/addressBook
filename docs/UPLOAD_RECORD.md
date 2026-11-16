# A 部分上传记录

仓库：<https://github.com/abet64287-crypto/addressBook>  
分支：`main`  
提交账户：`abet64287-crypto`  
记录日期：2026-11-16。

## 分批内容

| 批次 | 内容 | 提交链接 |
| --- | --- | --- |
| 1 | 项目范围、运行说明和 A/B 分工 | [0e91c595](https://github.com/abet64287-crypto/addressBook/commit/0e91c595000df090739439523810f13af87bc184) |
| 2 | 联系人模型、校验、SQLite、多种联系方式、收藏和 API | [151093d8](https://github.com/abet64287-crypto/addressBook/commit/151093d84c6bce3687ad6e59f8653f876ac08cf6) |
| 3 | 英文联系人界面、搜索、分组、收藏列表和响应式样式 | [dcbf3b66](https://github.com/abet64287-crypto/addressBook/commit/dcbf3b6658df4836a7f1d31ad1f36d68f2d3e396) |
| 4 | 测试、部署配置、代码规范、截图、认领清单和本上传记录 | 本文件所在提交；见 [main 提交历史](https://github.com/abet64287-crypto/addressBook/commits/main/) |

前面三批已分别成功推送；本文件随第四批提交。四批均有实际文件变更，不使用空提交。作者、时间及完整哈希由 GitHub 的提交历史保留。

## 当前范围与验收

- 仅上传 A 部分。B 的五个文件没有代替队友提交：`addressbook/excel.py`、`addressbook/excel_routes.py`、`addressbook/static/excel.js`、`tests/test_excel.py`、`docs/EXCEL_FORMAT.md`。
- A 单独存在时缺少 Excel 依赖，不能启动或部署。队友须提交 B，再经 PR 评审合并。
- 30 项测试通过及浏览器下载 / 导入结果来自完整本地 A+B 集成版本；不宣称 A 单独通过全套运行测试。
- 源码包含运行说明、代码规范、测试、设计、演示脚本和运行截图；没有上传数据库、虚拟环境、缓存、口令或服务器密钥。
- 至少三次仓库提交的数量要求已有记录；两人各自编码贡献、完整视频、PSP、Release、PR、个人博客和最终提交仍需按实际完成。

## 如何保留和使用证据

1. 打开 main 提交历史，截图保留作者、四条提交说明和时间。
2. 点击每条提交链接，检查文件变更；个人博客填写本人的提交数，并与队友的提交分开统计。
3. 后续不压缩或重写这些提交；队友通过新分支 / PR 增加自己的变更。
4. 合并 B 后在服务器重新执行测试、录屏、发布版本并保存对应 Git SHA。

本地另保存 `team-handoff/github-upload-receipt.json`，包含每批完整提交 SHA、链接及远程校验结果；该文件在第四批推送后生成，避免本文件对自身提交哈希产生循环引用。
