# Coding standards

## General conventions

- Use UTF-8 and descriptive names; Python indentation is four spaces.
- Keep changes focused and follow the surrounding JavaScript/CSS style.
- Separate domain validation, persistence, routing and interface responsibilities.
- Keep interface labels, errors and new Excel headers in English. Contact values may use other languages.
- Maintain the simple navy/light-gray interface without slogans or added branding.
- Explain errors and actionable recovery; remove temporary debugging output.
- Do not commit contact databases, credentials, environments, caches or temporary files. Use fictional demo data.

## Data rules

Preserve phone numbers and identifiers as text. Reuse the shared validator for forms and imports. Document duplicate policy and atomic failure behavior. Generate genuine XLSX, export user values as text and preserve labels, multiple methods and favorites. Use bound SQL parameters and close connections.

## Verification and review

| Item | Command or convention |
| --- | --- |
| Runtime | Python 3.12; native HTML/CSS/JavaScript |
| Install | python -m pip install -r requirements-dev.txt |
| Local run | python run.py |
| Complete-project tests | python -m pytest -q |
| JavaScript checks | node --check addressbook/static/app.js; node --check addressbook/static/excel.js |
| Manual acceptance | DEMO_SCRIPT.md |

Run applicable checks before merging. Focus on persistence, multiple methods, Excel round trips and errors. Describe actual changes in commit messages, use each member's own identity and review the other member's work. Record actual outcomes and limitations. Follow additional source-repository rules if applicable.
