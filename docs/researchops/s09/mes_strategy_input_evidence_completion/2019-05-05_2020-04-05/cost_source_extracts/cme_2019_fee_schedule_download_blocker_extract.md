# CME 2019 Fee Schedule Download Blocker Extract

Date captured: 2026-06-03

Authorized gate:

```text
source-native historical MES cost source acquisition/extraction
```

Attempted source URL from official historical-fees page:

```text
https://www.cmegroup.com/company/clearing-fees/historical-fees/files/cme-fee-schedules-2019.zip
```

Attempt method:

```text
Invoke-WebRequest from the clean Carver workspace
```

Operator authorization:

```text
official_cme_2019_fee_schedule_archive_permitted_route
```

Observed blocker:

```text
CME returned an anti-scraping / automated-access block page instead of the ZIP archive. The response instructed automated users to contact CME Group's Global Command Center for appropriate access.
```

Extraction result:

```text
FAIL_CLOSED_OFFICIAL_CME_2019_FEE_SCHEDULE_ARCHIVE_NOT_RETRIEVED_AUTOMATED_ACCESS_BLOCKED
```

Required next action:

Use a permitted non-automated CME access route or operator-provided official CME 2019 fee schedule archive before extracting historical MES exchange/clearing/regulatory fee values.

Boundary:

No unofficial mirror, current-fee default, broker assumption, spread/slippage assumption, old workspace state, or retired-window artifact was promoted into this machinery-development slice.
