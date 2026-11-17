# Verification report

Environment: Windows, Python 3.12.7, Flask 3.0.3, openpyxl 3.1.5, pytest 7.4.4, Node.js 22.23.2.

## Automated checks

The full local A+B project passed 30 tests on November 16, 2026. Packages were extracted into a new directory; paths were disjoint, the file manifest was complete and SHA-256 values matched. Separating tests by ownership did not remove assertions.

Coverage: CRUD, persistence across application instances, favorites, method validation, genuine XLSX, import into a separate empty database, labels/favorites/fields preserved, duplicates, same-name records with different data, multilingual text and leading zeros, formula-like text export, formula rejection, bad files/headers, atomic rejection, size/row limits, write protection, environment database paths and HTTPS Origin behavior.

Results: evidence/pytest.txt. Both app.js and excel.js passed node --check. The Ubuntu installer passed Bash syntax checking; it has not run on the server.

## Browser acceptance

- Five fictional contacts and two favorites displayed correctly.
- Favorites showed two records and the correct heading.
- Alex Lin displayed two phones, two emails, a social account and an address with leading zeros preserved.
- The editor showed all six methods and labels; saving displayed Contact saved.
- Main, Favorites and editor screenshots are under evidence/.
- After extracting excel.js, template download and empty-template import succeeded: Imported 0; skipped 0 duplicates. All five contacts remained.

## Verification limits

The complete A+B source is now available on main following hajiyao's November 17 upload ([0f11165](https://github.com/abet64287-crypto/addressBook/commit/0f1116596844622d09149fe9e157e3df8afcd0cc)). The test and browser results above remain the November 16 local records; this status update does not claim a new test run. Phone-device acceptance, load testing, public deployment and CSDN submission have not been performed. The complete video is not recorded. Repeat acceptance on the current complete checkout before release and on any actual HTTPS deployment. Initial preview restrictions were resolved using localhost without changing system firewall or proxy settings.
