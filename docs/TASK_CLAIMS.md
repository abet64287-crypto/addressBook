# Two-member task claims

Repository: [addressBook](https://github.com/abet64287-crypto/addressBook). Deadline: November 17, 2026, 23:59 UTC+8.

The owner selected Part A; the teammate is assigned Part B. Record actual work, verification and review within these boundaries.

| Area | A: repository owner | B: teammate |
| --- | --- | --- |
| Features | CRUD, methods, favorites, search, groups and UI | Excel template, export, import and validation |
| Python | domain.py, store.py, __init__.py | excel.py, excel_routes.py |
| Browser | index.html, app.js, style.css | excel.js |
| Tests | Contact/deployment tests and shared fixtures | Excel tests |
| Documents | General design, operation and integration | Excel format and transfer evidence |
| Branch | feature/contacts-ui for later changes | feature/excel-transfer |

## A: Contact management, favorites and UI

Claimant: repository owner, provisionally abet64287-crypto.

- [ ] Understand and verify the contact model and storage.
- [ ] Verify/improve create, edit, delete and dynamic method rows.
- [ ] Verify favorites, filtering and persistence after restart.
- [ ] Check search, groups, empty states, English feedback and narrow-screen behavior.
- [ ] Preserve the navy/light-gray interface without slogans or branding.
- [ ] Submit actual improvements/fixes with relevant verification.
- [ ] Review B and participate in Excel round-trip acceptance.

Acceptance: retain two phones, two emails, a social account and an address with separate labels. Favorites persist; editing, deletion, search and groups work. Provide actual commits, screenshots, personal PSP time and problems encountered.

## B: Excel transfer and validation

Claimant: teammate; the Excel files were uploaded by hajiyao on November 17, 2026 in [0f11165](https://github.com/abet64287-crypto/addressBook/commit/0f1116596844622d09149fe9e157e3df8afcd0cc). Complete the student's name and confirm the account mapping in the blog.

- [ ] Understand indexed columns and the shared validator.
- [ ] Verify genuine XLSX, English headers and one contact per row.
- [ ] Round-trip all fields into an isolated empty database.
- [ ] Check leading zeros, prefixes, multilingual values and special characters.
- [ ] Check invalid files/headers/emails/formulas and row/size limits.
- [ ] Confirm atomic rejection, duplicate skipping and same-name/different-data insertion.
- [ ] Submit actual improvements/fixes, tests and format documentation.
- [ ] Provide transfer evidence, review A and record personal PSP time and problems.

Acceptance: compatible workbooks open correctly; values, labels and favorites survive transfer; counts are accurate; errors leave no partial batch. Verify actual browser transfer as well as tests.

## Shared interfaces and delivery

Contacts contain name/company/group/notes/favorite/methods. Methods contain type/label/value, using phone/email/social/address. IDs are not import-update keys. A registers B's Blueprint and supplies api/refresh/toast; B passes validated records to transactional storage.

A and B are uploaded to main. B's five files were added directly by hajiyao in [0f11165](https://github.com/abet64287-crypto/addressBook/commit/0f1116596844622d09149fe9e157e3df8afcd0cc); no PR accompanied the upload. Review and verify the complete checkout before deployment. The required PR remains outstanding and should document actual follow-up work. Both members record their own work, review each other, complete a full video and publish separate blogs. Contribution percentages must total 100% and reflect actual work.

See [handoff](GITHUB_HANDOFF.md) and [upload records](UPLOAD_RECORD.md). The chosen new repository's compatibility with the course's specified-fork requirement remains to be confirmed.
