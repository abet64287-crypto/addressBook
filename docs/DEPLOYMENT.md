# Ubuntu deployment alongside the calculator

Prepared only: remote installation, DNS, certificates and public acceptance have not been executed.

The server output on November 16, 2026 showed two cores, 2 GB RAM, about 1.4 GiB available memory and 32 GB free disk. The calculator uses localhost:8000; Caddy uses 80/443. Both were active and 8001 was free.

| Item | Address Book |
| --- | --- |
| Source / environment | /opt/address-book / /opt/address-book/.venv |
| Account / systemd service | addressbook / address-book.service |
| Database | /var/lib/addressbook/contacts.sqlite3 |
| Listener | 127.0.0.1:8001 |
| Suggested hostname | contacts.calculator-demo.site, pending DNS/certificate setup |

Waitress serves the combined application behind existing Caddy. Keep 8001 private. There is no login system; public demonstrations should use fictional data.

## 1. Install the complete GitHub source

B's Excel modules are already on main as of November 17, 2026 ([0f11165](https://github.com/abet64287-crypto/addressBook/commit/0f1116596844622d09149fe9e157e3df8afcd0cc)). Verify the complete checkout before deploying. Use the existing TAT passwordless terminal:

```bash
sudo apt-get update
sudo apt-get install -y git
git clone --branch main --single-branch https://github.com/abet64287-crypto/addressBook.git "$HOME/addressBook-deploy"
cd "$HOME/addressBook-deploy"
git log -1 --oneline
sudo bash deploy/ubuntu/install.sh
```

If the checkout, application directory, service file or port 8001 already exists, inspect it instead of deleting it and repeating initial installation. The installer checks for B's runtime modules, creates a separate account/environment/database/service, and leaves Caddy and the calculator unchanged. A Git-based installation records the SHA in /opt/address-book/REVISION.

```bash
systemctl is-active address-book calculator-api caddy
curl -fsS http://127.0.0.1:8001/api/health
curl -fsS http://127.0.0.1:8000/api/health
```

Expected Address Book response: {"status":"ok"}. On failure, inspect `sudo journalctl -u address-book -n 50 --no-pager`. The service has read-only source and writable data/private temporary storage.

## 2. DNS

Add an A record named contacts under calculator-demo.site, pointing to the current server public IPv4. The calculator documentation records 43.129.177.221; use the actual current address if changed. Preserve existing records.

```bash
getent ahostsv4 contacts.calculator-demo.site
```

The result should match the server. Use the same hostname in Caddy.

## 3. Additional Caddy site

Back up the current file and retain the printed path:

```bash
ADDRESSBOOK_CADDY_BACKUP="/etc/caddy/Caddyfile.before-address-book.$(date +%Y%m%d%H%M%S)"
sudo cp -a /etc/caddy/Caddyfile "$ADDRESSBOOK_CADDY_BACKUP"
printf '%s\n' "$ADDRESSBOOK_CADDY_BACKUP"
sudo nano /etc/caddy/Caddyfile
```

Append this block outside all existing sites. Do not replace the full file or edit calculator sites. Keep one block for the new hostname.

```caddyfile
contacts.calculator-demo.site {
    encode gzip
    reverse_proxy 127.0.0.1:8001
}
```

Validate:

```bash
sudo caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
```

Only after success:

```bash
sudo systemctl reload caddy
```

Caddy obtains HTTPS certificates when DNS is correct and public 80/443 are reachable. Waitress uses --url-scheme=https for this HTTPS-only proxy route, preserving correct Origin checks without disabling write protection.

## 4. Public acceptance

```bash
curl -fsS https://contacts.calculator-demo.site/api/health
curl -fsS https://43-129-177-221.sslip.io/api/health
systemctl is-active address-book calculator-api caddy
```

The second URL is the calculator's recorded public entry point. Verify actual browser creation/editing, favorites, refresh, template download, export, import and invalid-file feedback. Check the calculator still calculates and displays history. Health checks do not replace actual read/write acceptance.

Optional fictional seed data:

```bash
cd /opt/address-book
sudo -u addressbook env ADDRESSBOOK_DATABASE=/var/lib/addressbook/contacts.sqlite3 /opt/address-book/.venv/bin/python seed_demo.py
```

After success, place the working URL in each blog and record the complete video. The proposed hostname is not proof of deployment.

## 5. Rollback and backup

For an immediate rollback, restore the backup from this change. If other configuration changed afterward, merge it manually first. In the same Bash session:

```bash
sudo cp -a "$ADDRESSBOOK_CADDY_BACKUP" /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
```

Reload only after successful validation. Stop only the new service with `sudo systemctl disable --now address-book`; preserve the calculator and both databases.

Use SQLite online backup, or stop only the address book while copying its database and then restart it. Keep backups outside source directories.

## References and verification

The complete local version passed 30 tests; installer syntax was checked. Linux installation, systemd, certificates and public behavior require actual server verification.

[Waitress options](https://docs.pylonsproject.org/projects/waitress/en/stable/runner.html), [Caddy validation/reload](https://caddyserver.com/docs/command-line), [automatic HTTPS](https://caddyserver.com/docs/automatic-https).
