# Excel Module — Member B

Status: On November 17, 2026, hajiyao uploaded the Excel modules, browser interaction script, tests, and this guide to main in [0aff42a](https://github.com/abet64287-crypto/addressBook/commit/0aff42af796f91cc6eb13a95b1a64d50eda55eb3).

Owner: Member B. Module files: `addressbook/excel.py`, `addressbook/excel_routes.py`, `addressbook/static/excel.js`, and `tests/test_excel.py`.

## Workbook Format

Use a genuine `.xlsx` workbook with exactly one worksheet and one contact per row. The base columns are `Name`, `Company`, `Group`, `Favorite`, and `Notes`; the `Name` header is required.

Each contact method uses separate indexed columns, such as `Phone1` / `Phone1Label` and `Phone2` / `Phone2Label`. The same convention applies to `Email`, `Social`, and `Address`, with indexes from 1 to 30. `Favorite` is exported as `Yes` or `No`; imports also accept `true` / `false`, `1` / `0`, and the supported legacy Chinese boolean values.

Exports expand columns according to the actual contact information and write all user-provided values as text. Legacy Chinese headers remain compatible with imports; new templates and exports use English headers.

## Validation and Import Rules

- Each import supports at most 1,000 data rows and 245 columns, with a 10 MB request limit and a 40 MB uncompressed workbook limit.
- Validate all records before calling `store.import_contacts` to save them in one transaction. Invalid rows reject the entire batch; row validation errors include English messages and row numbers.
- Skip exact duplicate records, ignoring contact method order. Add contacts with the same name but different information as separate records without overwriting existing contacts.
- Reject formula and error cells. Keep phone numbers formatted as text when editing workbooks so that spreadsheet software does not remove leading zeros before import.

## Integration with Member A

- A's `create_app` registers B's `excel_api` Blueprint. A applies the shared same-origin write protection.
- B accesses the storage layer using `current_app.config['DATABASE']` and reuses A's `validate_contact` when parsing records.
- A's HTML loads `app.js` followed by `excel.js`. B's script reuses the `api`, `refresh`, and `toast` functions provided by A. Both files are classic scripts loaded with `defer`.
- `/api/template` and `/api/export` use GET. `/api/import` uses multipart POST with a file field named `file`; the response reports `imported`, `skipped`, and `total` counts.

## Acceptance Checks

The current main branch includes both A and B. Before release, run `python -m pytest -q tests/test_excel.py` on the latest checkout. Also demonstrate template download, export of multiple contact methods, reimport into an isolated empty test database, duplicate imports, and rejection of invalid workbooks.

Provide actual screenshots or video evidence of these workflows in addition to automated test results.
