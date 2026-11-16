# Two-member GitHub handoff and deployment

Repository: [addressBook](https://github.com/abet64287-crypto/addressBook). A owns contacts/UI; B owns Excel. The two disjoint packages form one complete application after integration.

| Package | Owner | Content |
| --- | --- | --- |
| address-book-A.zip | Repository owner | Contacts, storage, favorites/API, main UI, shared helpers, contact/deployment tests and general documents |
| address-book-B.zip | Teammate | Excel parser, Blueprint, browser transfer, tests and format guide |

Archive paths are relative to the repository root. Upload extracted contents, not ZIPs or another enclosing directory. The root should directly contain README.md, run.py, requirements.txt, addressbook/, tests/ and deploy/. The local file-ownership.json records owners and SHA-256 hashes; environments, databases, caches and Git metadata are excluded.

## A upload status

Four functional A commits are on main, followed by an English-documentation update. See [upload records](UPLOAD_RECORD.md). A alone cannot run or deploy. Each member should understand, verify, improve and review their assigned work and keep actual participation records. Later A changes can use a feature branch.

## B upload and PR

1. The owner invites the teammate as a collaborator and the teammate accepts, or B forks the team repository and opens a cross-repository PR.
2. B extracts their package and creates feature/excel-transfer from the latest main under their own account.
3. On that branch use Add file > Upload files, preserving paths. Adding files within existing folders must not delete A's files.
4. Confirm the diff contains B's five files only:

```text
addressbook/excel.py
addressbook/excel_routes.py
addressbook/static/excel.js
tests/test_excel.py
docs/EXCEL_FORMAT.md
```

5. Open a PR to the team repository's main. A reviews and verifies the full application before merging. Preserve meaningful commit history.

## Integration and release

```text
python -m pip install -r requirements-dev.txt
python -m pytest -q
node --check addressbook/static/app.js
node --check addressbook/static/excel.js
```

Repeat manual acceptance, record the actual date/version/results/problems, and keep meaningful changes in separate commits. Initial A history meets the repository count minimum; B must still contribute code. Commit count does not directly define contribution ratios.

Publish a Release after acceptance; retain PR and SHA links. Record the full video and finish both PSP records and personal blogs.

## Server pulls from GitHub

After B is merged, use the existing TAT passwordless terminal. Public HTTPS clone does not require local-PC SSH setup.

```bash
sudo apt-get update
sudo apt-get install -y git
git clone --branch main --single-branch https://github.com/abet64287-crypto/addressBook.git "$HOME/addressBook-deploy"
cd "$HOME/addressBook-deploy"
git log -1 --oneline
sudo bash deploy/ubuntu/install.sh
```

If the checkout or installation exists, inspect it instead of deleting it and repeating the initial installer. It checks B's runtime modules and records the source SHA at /opt/address-book/REVISION.

```bash
systemctl is-active address-book calculator-api caddy
curl -fsS http://127.0.0.1:8001/api/health
curl -fsS http://127.0.0.1:8000/api/health
```

Then follow [deployment](DEPLOYMENT.md) for DNS, the added Caddy site and public read/write acceptance. Preserve calculator configuration.

B has not been uploaded on the teammate's behalf. No team PR, collaborator invitation or server deployment has been performed. Confirm the assignment's specified-fork requirement for the new team repository.
