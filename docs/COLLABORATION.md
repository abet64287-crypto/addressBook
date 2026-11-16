# Collaboration plan

Repository: [addressBook](https://github.com/abet64287-crypto/addressBook). Member A is the repository owner, provisionally abet64287-crypto. Member B's name and GitHub username remain to be completed.

## Responsibilities

A owns contacts, favorites, persistence, UI, shared fixtures and contact/deployment tests. B owns excel.py, excel_routes.py, static/excel.js, tests/test_excel.py and docs/EXCEL_FORMAT.md. Packages do not overlap. The application registers B's Blueprint and loads both scripts; A alone is incomplete.

A maintains the storage transaction used by imports. Both members verify data contracts, validation, duplicate behavior and results together. Notify the other member before changing an interface.

## Git workflow

1. Use the selected team repository. It is not a fork; confirm the course's specified-fork requirement.
2. Four initial A batches are uploaded to main. See UPLOAD_RECORD.md for immutable links and later updates.
3. B adds the assigned files on feature/excel-transfer, then opens a PR to main. A reviews and verifies the complete project before merging.
4. Preserve actual identities, timestamps and meaningful history. Record each member's contributions separately.
5. Run complete tests and the manual demo, publish a Release and retain its source SHA.
6. Each member publishes an individual blog containing both PSP tables, responsibilities, problems and contribution ratios totaling 100%.

## Actual records to complete

| Date | Participants | Problem or decision | Resolution | Commit/evidence |
| --- | --- | --- | --- | --- |
| [Actual date] | [Names] | [Actual event] | [Outcome] | [Link] |

| Member | Actual work and evidence | Contribution |
| --- | --- | --- |
| A | [Complete] | [Value]% |
| B | [Complete] | [Value]% |
| Total | | 100% |

Commit counts do not directly determine contribution ratios. See [task claims](TASK_CLAIMS.md) and [handoff](GITHUB_HANDOFF.md).
