# 腾讯云 Ubuntu 共存部署（远程尚未执行）

按 2026-11-16 服务器输出：2 核 / 2 GB，可用内存约 1.4 GiB，磁盘剩余 32 GB；计算器占用 127.0.0.1:8000，Caddy 占用 80/443，两者 active；8001 空闲。

| 配置 | 通讯录 |
| --- | --- |
| 程序 / 虚拟环境 | `/opt/address-book` / `/opt/address-book/.venv` |
| 独立账号 / 服务 | `addressbook` / `address-book.service` |
| 独立数据文件 | `/var/lib/addressbook/contacts.sqlite3` |
| 内部监听 | `127.0.0.1:8001` |
| 建议公网域名 | `contacts.calculator-demo.site`（待配置 DNS 和证书） |

前后端由一个 Flask 应用提供，Waitress 运行，复用现有 Caddy。不要开放 8001 公网端口，不另装 Nginx。项目没有登录功能，公开演示用虚构联系人；真实通讯录应先增加访问控制。

## GitHub 拉取（当前首选）

两人分别上传并合并 main 后，按 [GITHUB_HANDOFF.md](GITHUB_HANDOFF.md) 第四步从公开仓库 clone，然后运行安装器。无需本机 SCP；下面保留 ZIP 上传作为备用路线。

## 1. 本机上传最新源码包（备用）

在 Windows PowerShell 执行，把 `你的SSH用户名` 换成平时登录服务器的账号。IP 来自计算器仓库记录，若已变更，请用当前公网 IP。

```powershell
scp E:\ExPrograming\address-book-source.zip 你的SSH用户名@43.129.177.221:~/address-book-source.zip
```

使用现有 SSH 密钥或交互密码上传，不用在聊天中提供密码。

## 2. Ubuntu 首次安装

在服务器 Bash 执行。安装器遇到已有 `/opt/address-book`、服务文件或占用的 8001 时会停止；如中途失败，不要删除目录重试，先检查并修复报错。

```bash
sudo apt-get update
sudo apt-get install -y unzip
ADDRESSBOOK_STAGE=$(mktemp -d /tmp/address-book-install.XXXXXX)
unzip ~/address-book-source.zip -d "$ADDRESSBOOK_STAGE"
sudo bash "$ADDRESSBOOK_STAGE/address-book/deploy/ubuntu/install.sh"
```

安装器创建独立虚拟环境、账号、数据目录和 systemd 服务，不编辑 Caddy 或计算器。成功时返回 `{"status":"ok"}`。检查：

```bash
systemctl is-active address-book calculator-api caddy
curl -fsS http://127.0.0.1:8001/api/health
curl -fsS http://127.0.0.1:8000/api/health
```

失败时用 `sudo journalctl -u address-book -n 50 --no-pager` 查看日志。服务代码只读，只有数据目录和独立临时目录可写。

## 3. 域名解析

在 `calculator-demo.site` 的 DNS 管理中新增主机记录 **contacts**，类型 **A**，值为服务器当前公网 IPv4（根据原项目为 `43.129.177.221`）。保留原有 api 记录。

```bash
getent ahostsv4 contacts.calculator-demo.site
```

结果应指向当前服务器。若采用其他域名，下一步 Caddyfile 中的主机名也要相应修改。

## 4. 新增 Caddy 站点

先备份现有配置，记住输出的备份路径：

```bash
ADDRESSBOOK_CADDY_BACKUP="/etc/caddy/Caddyfile.before-address-book.$(date +%Y%m%d%H%M%S)"
sudo cp -a /etc/caddy/Caddyfile "$ADDRESSBOOK_CADDY_BACKUP"
printf '%s\n' "$ADDRESSBOOK_CADDY_BACKUP"
sudo nano /etc/caddy/Caddyfile
```

在文件末尾、现有所有站点块外新增以下内容，同名站点只保留一份。不要覆盖整个文件，也不修改原有计算器站点。

```caddyfile
contacts.calculator-demo.site {
    encode gzip
    reverse_proxy 127.0.0.1:8001
}
```

先检查：

```bash
sudo caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
```

只有检查成功，才平滑加载：

```bash
sudo systemctl reload caddy
```

Caddy 为站点自动申请 HTTPS 证书，需要 DNS 正确且公网 80/443 可达，沿用已有放行配置。

服务的 Waitress 参数 `--url-scheme=https` 代表只接受该 HTTPS 站点的本机转发，保证 Flask 的 Origin 校验正确识别外部协议。没有关闭跨站写入保护。

## 5. 公网验收

```bash
curl -fsS https://contacts.calculator-demo.site/api/health
curl -fsS https://43-129-177-221.sslip.io/api/health
systemctl is-active address-book calculator-api caddy
```

两次健康请求都应成功。第二个地址是计算器仓库记录的原入口。然后在浏览器验证：新增虚构联系人、编辑、收藏、刷新、Excel 模板下载、导出、导入和错误文件反馈；检查计算器仍能计算并查看历史。健康检查不能代替实际读写验证。

需要虚构演示数据时，显式执行（不会清空数据）：

```bash
cd /opt/address-book
sudo -u addressbook env ADDRESSBOOK_DATABASE=/var/lib/addressbook/contacts.sqlite3 /opt/address-book/.venv/bin/python seed_demo.py
```

验收成功后，把公网地址放入博客并录制完整视频。当前建议域名不是已经上线的证据。

## 6. 回退

若新站点配置有误，在本次配置操作后立即恢复刚才的备份；若期间有其他配置变更，先人工合并，避免覆盖。仍在同一 Bash 会话时可以使用这个变量，否则使用上面记录的实际备份路径。

```bash
sudo cp -a "$ADDRESSBOOK_CADDY_BACKUP" /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
```

检查成功再执行 `sudo systemctl reload caddy`。可用 `sudo systemctl disable --now address-book` 停用通讯录。不要停计算器、不要删除数据库。

备份通讯录可短暂停止 address-book 服务后复制 `/var/lib/addressbook/contacts.sqlite3`，再启动，或采用 SQLite 在线备份 API。它和计算器数据库互相独立。

## 验证状态

本地 29 项测试通过，包括环境变量数据路径和 HTTPS 来源检查；安装脚本已进行 Bash 语法检查。Linux 安装、systemd、域名解析、证书和公网读写仍需在服务器实际执行并验证。本地测试不能证明已完成云部署。

参考：[Waitress 参数](https://docs.pylonsproject.org/projects/waitress/en/stable/runner.html)、[Caddy 配置验证与加载](https://caddyserver.com/docs/command-line)、[Caddy 自动 HTTPS](https://caddyserver.com/docs/automatic-https)。
