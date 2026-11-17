# Implementation design

## Architecture and data

Browser HTML/CSS/JavaScript calls the Flask JSON API. Shared domain validation handles both forms and imported data. SQLite stores stable contact IDs and JSON records containing name, company, group, notes, favorite and methods. Each method has type, label and value. Queries use bound parameters, and connections close after each operation.

JSON supports variable method lists in this small application. More complex queries or larger workloads could use a separate method table. SQLite is intended for a single-instance, small-scale deployment.

## Features

Favorites are saved transactionally and displayed through stars, counts and a dedicated view. Refreshes read the saved state. The editor adds/removes phone, email, social and address rows with independent labels. Values have length limits, email receives basic format validation, and phone numbers remain text.

Excel uses genuine XLSX with one contact per row and indexed value/label columns. Every row is validated before saving the entire batch in one transaction. Exact duplicates are skipped; different records are inserted without overwriting existing contacts. User values are exported as text rather than formulas.

## Module boundaries

A's factory registers B's excel_api Blueprint. The HTML loads deferred classic scripts app.js and then excel.js. B reuses A's api, refresh and toast functions, validator and storage layer. Both members' runtime files are available on main as of November 17, 2026; B's Excel upload is recorded in UPLOAD_RECORD.md.

| Method | Path | Purpose |
| --- | --- | --- |
| GET | /api/contacts | List contacts |
| POST | /api/contacts | Create contact |
| PUT | /api/contacts/<id> | Replace editable data |
| DELETE | /api/contacts/<id> | Delete contact |
| PATCH | /api/contacts/<id>/favorite | Set favorite state |
| GET | /api/health | Health check |
| GET | /api/export | Export all contacts |
| GET | /api/template | Download compatible template |
| POST | /api/import | Import multipart field file |

## Request handling and hosting

Writes require X-Requested-With: AddressBook. Any supplied Origin must match the application origin. CORS is not enabled. User text is HTML-escaped; the page uses a same-origin content security policy.

There is no login or per-user isolation. Public demonstrations should use fictional data; real contact data requires access control. The prepared Waitress service listens only on localhost behind Caddy's HTTPS site and uses the external HTTPS scheme so Origin checks remain correct. Server deployment is still pending.
