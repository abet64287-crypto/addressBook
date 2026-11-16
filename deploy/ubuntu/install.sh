#!/usr/bin/env bash
# Initial installation only. Does not edit Caddy or the calculator service.
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
    printf '%s\n' 'Run this installer with sudo.' >&2
    exit 1
fi
SOURCE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
APP_DIR=/opt/address-book
UNIT_FILE=/etc/systemd/system/address-book.service
if [[ -e "$APP_DIR" || -e "$UNIT_FILE" ]]; then
    printf '%s\n' 'Address Book already exists. Initial installer stopped without changing it.' >&2
    exit 1
fi
if ss -H -lnt 'sport = :8001' | grep -q .; then
    printf '%s\n' 'Port 8001 is already in use. Installation stopped.' >&2
    exit 1
fi
test -f "$SOURCE_DIR/requirements.txt"
test -f "$SOURCE_DIR/run.py"
test -f "$SOURCE_DIR/addressbook/excel.py"
test -f "$SOURCE_DIR/addressbook/excel_routes.py"
test -f "$SOURCE_DIR/addressbook/static/excel.js"
apt-get update
apt-get install -y python3 python3-venv curl
if ! id addressbook >/dev/null 2>&1; then
    useradd --system --user-group --home-dir /var/lib/addressbook --shell /usr/sbin/nologin addressbook
fi
install -d -o addressbook -g addressbook -m 0750 /var/lib/addressbook
install -d -o root -g root -m 0755 "$APP_DIR"
tar -C "$SOURCE_DIR" --exclude=.git --exclude=.venv --exclude=instance --exclude=__pycache__ --exclude=.pytest_cache -cf - . | tar -C "$APP_DIR" -xf -
if git -C "$SOURCE_DIR" rev-parse HEAD >/dev/null 2>&1; then
    git -C "$SOURCE_DIR" rev-parse HEAD > "$APP_DIR/REVISION"
fi
chown -R root:root "$APP_DIR"
chmod -R u=rwX,go=rX "$APP_DIR"
python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/python" -m pip install -r "$APP_DIR/requirements.txt"
install -o root -g root -m 0644 "$APP_DIR/deploy/ubuntu/address-book.service" "$UNIT_FILE"
systemctl daemon-reload
systemctl enable --now address-book.service
curl --retry 8 --retry-connrefused --retry-delay 1 -fsS http://127.0.0.1:8001/api/health
printf '\n%s\n' 'Local service is ready. Configure DNS and add the Caddy site next.'
