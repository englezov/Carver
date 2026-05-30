# Carver Databento API Access Remediation Result

Date: 2026-05-30

Status:

```text
PROCESS_LOCAL_CARVER_DATABENTO_API_ACCESS_REMEDIATION_RESULT_AUTHENTICATION_BLOCKED_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Diagnose why freshly created valid-shaped Databento API keys return HTTP 401 on metadata-only endpoints, without requesting historical market data.

This remediation follows:

```text
docs/process/CARVER_DATABENTO_16_SYMBOL_DAILY_OHLCV_QUARANTINE_INTAKE_EXECUTION_FAIL_CLOSED_2026-05-30.md
```

## Allowed Boundary

Performed:

```text
official Databento Python client installation
metadata-only Databento API calls
secret-safe environment checks
redacted support-evidence documentation
process decision documentation
```

Not performed:

```text
market data download
historical data request
market-row parsing
diagnostics
backtests
forecasts
positions
costs
carry
trend
OOS
Lockbox
Forward
CFD adapters
old QuantLab active-pipeline use
tuning
deployment
trading
promotion
Git staging/commit/push/PR
remote repository operations
```
## Official Client Check

Installed official client:

```text
databento==0.78.0
```

Secret-safe environment state:

```text
DATABENTO_API_KEY_PRESENT: YES
DATABENTO_API_KEY_VALUE_PRINTED_OR_RECORDED: NO
```

Official client metadata checks:

```text
db.Historical(...).metadata.list_schemas(dataset="GLBX.MDP3")
RESULT: 401 auth_authentication_failed

db.Historical(...).metadata.list_datasets()
RESULT: 401 auth_authentication_failed
```

HTTP Basic-auth metadata checks already recorded:

```text
GET /v0/metadata.list_schemas?dataset=GLBX.MDP3
RESULT: 401 auth_authentication_failed

GET /v0/metadata.list_unit_prices?dataset=GLBX.MDP3
RESULT: 401 auth_authentication_failed
```

Auth-shape variants already tested:

```text
Basic key-as-username blank-password: 401 auth_authentication_failed
Basic blank-username key-as-password: 400 auth_invalid_username_in_basic_auth
Bearer key: 401 Not authenticated
X-API-Key: 401 Not authenticated
Basic key-as-username user-id-as-password: 401 auth_authentication_failed
Basic user-id-as-username key-as-password: 401 auth_authentication_failed
```

Interpretation:

```text
OFFICIAL_CLIENT_CONFIRMS_AUTHENTICATION_BLOCK
LOCAL_HTTP_AUTH_CODE_NOT_ROOT_CAUSE
LOCKED_16_SYMBOL_REQUEST_NOT_ROOT_CAUSE
NO_MARKET_DATA_REQUESTED
```

## Support Packet

Use this exact support text with Databento, without including any secret key value:

```text
Fresh Databento account with credits visible in portal.
Fresh API key created from Databento API keys page.
API key is 32 characters total and starts with db-.
Using Databento Python client 0.78.0:
  client = databento.Historical(API_KEY)
  client.metadata.list_schemas(dataset="GLBX.MDP3")
returns:
  401 auth_authentication_failed Authentication failed.

Using HTTP Basic Auth with the API key as username and blank password:
  GET https://hist.databento.com/v0/metadata.list_schemas?dataset=GLBX.MDP3
also returns:
  401 auth_authentication_failed

No historical data request was made. No market data was requested.
Please confirm whether the account/API key is active for Historical API metadata endpoints and whether any account activation, plan, permission, billing, or portal state is still pending.
```

## Decision

Decision:

```text
KEEP_DATABENTO_AS_PREFERRED_PROGRAMMATIC_PROVIDER_BUT_BLOCK_EXECUTION_PENDING_ACCOUNT_AUTH_FIX
```

Reason:

Databento remains the preferred architecture for the 16-symbol and eventual 102-row source-native futures daily intake path because it supports programmatic historical access, CME Group futures coverage, raw output preservation, symbology/reference metadata, and scalable batch requests.

However, all Databento execution gates remain blocked until metadata authentication succeeds with the official client or documented HTTP Basic Auth.

Manual portal downloads are not selected as the primary path because they do not scale to the 16-symbol pilot and eventual 102-row portfolio universe.

Backup provider decision:

```text
OPEN_BACKUP_PROVIDER_DECISION_GATE_IF_DATABENTO_SUPPORT_CANNOT_FIX_AUTH_PROMPTLY
```

Preferred backup candidates:

```text
Norgate Data futures package for broad daily historical research
CME DataMine for official CME source authority / settlement datasets
Barchart OnDemand for commercial API daily futures history if pricing/access is acceptable
```

## Closed Boundaries

Still closed:

```text
Databento historical data request
market data download
market-row parsing
diagnostics
backtests
forecasts
positions
costs
carry
trend
volatility/risk calculations
OOS
Lockbox
Forward
CFD adapters
old QuantLab active-pipeline use
tuning
deployment
trading
promotion
Git staging
commit
push
PR update/opening
remote repository operations
```
