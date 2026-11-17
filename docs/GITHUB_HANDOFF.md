# Two-member GitHub handoff and deployment

Repository: [addressBook](https://github.com/abet64287-crypto/addressBook). A owns contacts/UI; B owns Excel. Both members' files are now on main; the Excel upload was completed on November 17, 2026 in [0aff42a](https://github.com/abet64287-crypto/addressBook/commit/0aff42af796f91cc6eb13a95b1a64d50eda55eb3).

| Package | Owner | Content |
| --- | --- | --- |
| address-book-A.zip | Repository owner | Contacts, storage, favorites/API, main UI, shared helpers, contact/deployment tests and general documents |
| address-book-B.zip | Teammate | Excel parser, Blueprint, browser transfer, tests and format guide |

Archive paths are relative to the repository root. Upload extracted contents, not ZIPs or another enclosing directory. The root should directly contain README.md, run.py, requirements.txt, addressbook/, tests/ and deploy/. The repository is the reviewable source deliverable; local ZIP packages and ownership manifests are optional handoff artifacts and are not included here. Environments, databases, caches and credentials are excluded.

## A upload status

Four functional A commits are on main, followed by an English-documentation update. See [upload records](UPLOAD_RECORD.md). B's five Excel files are now also on main. Each member should understand, verify, improve and review their assigned work and keep actual participation records. Later A changes can use a feature branch.

## B upload status and remaining PR

B uploaded all five assigned files directly to main under the hajiyao account on November 17, 2026 in [0aff42a](https://github.com/abet64287-crypto/addressBook/commit/0aff42af796f91cc6eb13a95b1a64d50eda55eb3). The upload added these files without replacing A's files:

```text
addressbook/excel.py
addressbook/excel_routes.py
addressbook/static/excel.js
tests/test_excel.py
docs/EXCEL_FORMAT.md
```

The direct upload did not create a PR. Review the uploaded changes and verify the full application. The assignment still requires a PR: create a feature branch for actual follow-up work, open a PR to the required target, and retain review evidence. Preserve the existing upload history.

## Integration and release

```text
python -m pip install -r requirements-dev.txt
python -m pytest -q
node --check addressbook/static/app.js
node --check addressbook/static/excel.js
```

Repeat manual acceptance, record the actual date/version/results/problems, and keep meaningful changes in separate commits. Both accounts now have code uploads on main, and the repository meets the minimum commit count. Refresh each member's final count after further changes. Commit count does not directly define contribution ratios.

Publish a Release after acceptance; retain PR and SHA links. Record the full video and finish both PSP records and personal blogs.

## Server pulls from GitHub

The complete A+B source is available on main. After current-checkout acceptance, use the existing TAT passwordless terminal. Public HTTPS clone does not require local-PC SSH setup.

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

B's upload was made by hajiyao directly to main. No team PR or server deployment has been recorded. Confirm the assignment's specified-fork requirement for the new team repository.
