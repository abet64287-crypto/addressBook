# Address Book

> Current repository status (November 17, 2026): The complete A+B source is uploaded to main, and the application is deployed at [contacts.calculator-demo.site](https://contacts.calculator-demo.site/). Member B's five Excel files were added by hajiyao in [0aff42a](https://github.com/abet64287-crypto/addressBook/commit/0aff42af796f91cc6eb13a95b1a64d50eda55eb3). The local test suite passed all 30 tests on November 17. The public homepage and health endpoint were also checked successfully; full production acceptance is separate from these availability checks.

A pair-programming address book using Flask, SQLite, openpyxl and an English HTML/CSS/JavaScript interface. Features include contact CRUD, favorites, multiple labeled contact methods, search, groups and Excel import/export.

- Repository: [addressBook](https://github.com/abet64287-crypto/addressBook)
- Live Application: [contacts.calculator-demo.site](https://contacts.calculator-demo.site/)
- Assignment: [Extreme Programming](https://bbs.csdn.net/topics/620593436)
- Deadline: **November 17, 2026, 23:59 (UTC+8 / Beijing time)**
- Ownership: A owns contacts and UI; B owns Excel transfer and validation.

## Run locally

The complete A+B source is available on main. Python 3.12 is recommended.

```powershell
git clone https://github.com/abet64287-crypto/addressBook.git
cd addressBook
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe seed_demo.py
.\.venv\Scripts\python.exe run.py
```

Open [the application](http://127.0.0.1:5000). Seeding is optional: it adds fictional contacts and skips exact duplicates without clearing existing records. With dependencies installed, `python run.py` is sufficient. Set `PORT` to change the development port.

SQLite data persists at `instance/contacts.sqlite3`, which is excluded from Git. Set `ADDRESSBOOK_DATABASE` for a different path. Stop the service before making a file-copy backup, or use SQLite's online backup API.

## Features and Excel contract

Contacts support phone, email, social and address entries with independent labels: up to 30 entries per type and 120 total. Favorites persist across refreshes and restarts. Search covers names, companies, groups and method values.

Use a single XLSX worksheet, one contact per row. Base columns: `Name` (required), `Company`, `Group`, `Favorite`, `Notes`. Repeated entries use `Phone1`, `Phone1Label`, `Phone2`, `Phone2Label`, and equivalent Email/Social/Address columns, numbered 1-30. Exports expand columns as needed.

- Favorite accepts Yes/No, true/false and 1/0; blank means No.
- Preserve phone numbers and account identifiers as text to retain leading zeros. Exports use text cells.
- Validate all records before one transactional save. Invalid input rejects the entire batch with a specific error.
- Skip exact duplicates, ignoring method order. Same-name contacts with different data are added, not overwritten. Edit existing records through the interface.
- Limits: 1,000 data rows, 245 columns, a 10 MB request and 40 MB uncompressed content. Larger collections require separate batches.
- Reject formula/error cells. Export user-provided values as text.
- Older Chinese templates remain compatible; the interface and new workbook headers are English.

## Verification

```text
python -m pytest -q
node --check addressbook/static/app.js
node --check addressbook/static/excel.js
```

Tests use temporary databases and cover CRUD, persistence, favorites, validation, Excel round trips, duplicates, leading zeros, formulas, atomic rejection, limits and deployment configuration. The suite was rerun locally on November 17, 2026, against [6cc1cb1](https://github.com/abet64287-crypto/addressBook/commit/6cc1cb11b7ca8878b59be489fecdb675eb28780f), with the result `30 passed in 1.37s`. The subsequent [871ebb9](https://github.com/abet64287-crypto/addressBook/commit/871ebb92c77d82f2eaced6fedf87662402bff207) only translated the Excel format guide; application code was unchanged. This local result does not replace acceptance testing of the deployed service.

## Responsibilities and documents

| Area | Files | Owner |
| --- | --- | --- |
| Contacts, favorites, persistence and API | domain.py, store.py, __init__.py | A |
| Main interface | templates/index.html, static/app.js, static/style.css | A |
| Excel parser, endpoints and browser interaction | excel.py, excel_routes.py, static/excel.js | B |
| Contact/deployment tests and shared fixtures | tests/test_contacts.py, tests/test_deployment.py, tests/conftest.py | A |
| Excel tests and format guide | tests/test_excel.py, docs/EXCEL_FORMAT.md | B |

- [Task claims](docs/TASK_CLAIMS.md) and [collaboration](docs/COLLABORATION.md)
- [Design](docs/DESIGN.md) and [coding standards](docs/CODING_STANDARDS.md)
- [Test report](docs/TEST_REPORT.md) and [delivery status](docs/DELIVERY_STATUS.md)
- [Blog draft](docs/BLOG_DRAFT.md) and [blog/PSP template](docs/BLOG_TEMPLATE.md)
- [Demo script](docs/DEMO_SCRIPT.md) and [submission checklist](docs/SUBMISSION_CHECKLIST.md)
- [GitHub handoff](docs/GITHUB_HANDOFF.md), [upload records](docs/UPLOAD_RECORD.md) and [Ubuntu deployment](docs/DEPLOYMENT.md)

## Cloud deployment and outstanding work

The application is deployed and publicly accessible over HTTPS:

- Application: [https://contacts.calculator-demo.site/](https://contacts.calculator-demo.site/)
- Health check: [https://contacts.calculator-demo.site/api/health](https://contacts.calculator-demo.site/api/health)

On November 17, 2026, both URLs returned HTTP 200, and the health endpoint returned `{"status":"ok"}`. These checks verify availability, not every application workflow.

See [deployment instructions](docs/DEPLOYMENT.md) for an Ubuntu example using Waitress behind Caddy, a separate systemd service on localhost port 8001, and data under `/var/lib/addressbook`. Its hostname, paths, and service settings are examples; use the actual server configuration when maintaining the deployed application.

The selected repository was newly created, not forked; confirm the assignment's specified-fork requirement. The Excel upload, local automated retest, and public deployment are complete. Full acceptance of the deployed workflows, the required PR, Release, complete video, individual PSP records, personal blogs and final submissions remain outstanding. Each member should record actual participation and review the other's work.
