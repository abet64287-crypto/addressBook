# Public Deployment Check

Check date: November 17, 2026 (UTC+8).

## Public URLs

- Application: [Address Book](https://contacts.calculator-demo.site/)
- Health endpoint: [Service health](https://contacts.calculator-demo.site/api/health)
- Source snapshot used for the release: [`31bc5eb`](https://github.com/abet64287-crypto/addressBook/commit/31bc5eb73cf6a28a463604d1c97b9e18dc74053b)

## Observed results

| Check | Result |
| --- | --- |
| Public HTTPS homepage | HTTP 200 |
| Browser rendering | The English contact interface rendered, including the contact list, details, favorites navigation, search/group controls, and Excel transfer controls |
| Public health endpoint | HTTP 200 with `{"status":"ok"}` |

The public deployment uses a separate database from the local screenshot session. Its deployed source commit was not independently established by these HTTP checks.

## Local automated verification

A fresh local checkout of [`6cc1cb1`](https://github.com/abet64287-crypto/addressBook/commit/6cc1cb11b7ca8878b59be489fecdb675eb28780f) was tested on November 17, 2026:

```text
30 passed in 1.37s
```

The local environment used Windows, Python 3.13.11, Flask 3.0.3, openpyxl 3.1.5, and pytest 7.4.4. Subsequent commits `871ebb9` and `31bc5eb` changed documentation only. Application code in the release source snapshot is identical to that locally tested version.

## Remaining acceptance

The HTTP checks establish public availability, and the browser observation establishes page rendering. A full acceptance pass of the deployed CRUD, persistence, favorites, search/groups, and Excel workflows remains separate. Record those results after testing the public service with appropriate demonstration data.

See [README](../README.md) for installation, the Excel contract, and public access links, and [deployment instructions](DEPLOYMENT.md) for configuration examples.
