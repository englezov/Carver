# Carver Tradovate API Credential Requirements Investigation

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_TRADOVATE_API_CREDENTIAL_REQUIREMENTS_INVESTIGATION_NOT_DATA_NOT_CREDENTIAL_EXTRACTION
```

## Purpose

Answer the operator question:

```text
We do not have an API token. Is that something we set ourselves?
```

This is a process-only credential-requirements investigation for the locked Carver S09 ZN direct-daily API probe gate. It inspects official NinjaTrader/Tradovate documentation only.

## Scope Boundary

Allowed:

- Official NinjaTrader/Tradovate API documentation and help-center pages.
- Process-only interpretation of credential requirements.
- No local browser storage inspection.
- No credential extraction.
- No API authentication request.
- No market-data request.

Forbidden:

- Browser cookie, localStorage, sessionStorage, IndexedDB, profile, or DevTools token inspection.
- Username/password collection in chat.
- API key, API secret, token, account, or browser session extraction.
- `md/getChart`, `md/cancelChart`, order, account, report, trading, deployment, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, old QuantLab import, tuning, promotion, or remote push by inference.

## Official Sources Inspected

- Tradovate Help Center: "How Do I Get Access to the Tradovate API?"
  <https://tradovate.zendesk.com/hc/en-us/articles/4403105829523-How-Do-I-Get-Access-to-the-Tradovate-API>
- Tradovate Help Center: "Should I Use OAuth, an API Key, or an API Key with a Dedicated Password?"
  <https://tradovate.zendesk.com/hc/en-us/articles/4403105862035-Should-I-Use-OAuth-an-API-Key-or-an-API-Key-with-a-Dedicated-Password>
- Tradovate Partner API: "API Keys"
  <https://partner.tradovate.com/overview/quick-setup/api-keys>
- Tradovate Partner API: "5-Minute Quickstart"
  <https://partner.tradovate.com/overview/quick-setup/5-minute-quickstart>
- Tradovate Partner API: "Auth Overview"
  <https://partner.tradovate.com/overview/quick-setup/auth-overview>
- NinjaTrader Partner Developer Platform: "Welcome to Tradovate Partner API"
  <https://partner.ninjatrader.com/nt-prop/overview/welcome/introduction-to-tradovate-partner-api>
- NinjaTrader Developer Community: "Trader APIs"
  <https://developer.ninjatrader.com/products/api>
- Tradovate Partner API: "Market Data"
  <https://partner.tradovate.com/overview/core-concepts/web-sockets/market-data/market-data>
- Tradovate Partner API: "Market Data Request Reference"
  <https://partner.tradovate.com/overview/core-concepts/web-sockets/market-data/market-data-request-reference>
- Tradovate API reference:
  <https://api.tradovate.com/>

## Findings

### 1. The API token is not self-invented

The operator does not locally choose an arbitrary token value. Official documentation describes account/API-access setup and an API-key-based authentication flow.

The retail Tradovate help-center page says API key generation requires a live Tradovate account above USD 1,000, completion of the CME Information License Agreement, and subscription to the API Access Add-on before generating an API key in Application Settings.

The Partner API docs describe API keys as containing credential fields such as:

```text
name
password
appId
appVersion
sec
cid
```

The quickstart then uses those fields in an `/auth/accesstokenrequest` call.

### 2. The official auth flow can return a market-data token

The Tradovate API reference documents `auth/accesstokenrequest` as an access-token request using user credentials plus API key fields. The documented response shape includes an `accessToken`, and the broader API examples show an `mdAccessToken` in the auth response.

For the Carver S09 ZN direct-daily probe, the only token needed by the already-audited one-shot client is the market-data token:

```text
CARVER_TRADOVATE_MD_ACCESS_TOKEN
```

The existing Carver client intentionally does not implement `/auth/accesstokenrequest`, because that would broaden the current gate from one read-only market-data WebSocket probe into a separate authentication implementation.

### 3. API-key permissions and market-data entitlements matter

The help-center flow includes selecting permissions for the generated API key. The Partner API docs distinguish production/staging credentials and market-data WebSocket access. The NinjaTrader/Tradovate docs describe market-data access through WebSocket chart/quote/DOM/histogram requests, but access still depends on the account/key/entitlement state returned by authentication and the data permissions on the account.

Therefore the current free-trial browser login being able to display charts does not, by itself, prove that a separate API key and market-data token are available to local code.

### 4. Official docs support the current endpoint quarantine

Official market-data docs describe:

```text
md/getChart
md/cancelChart
```

and chart request fields matching the Carver gate shape:

```text
symbol
chartDescription.underlyingType
chartDescription.elementSize
chartDescription.elementSizeUnit
timeRange.asMuchAsElements
```

They also state that successful chart requests return subscription IDs and that chart subscriptions must be cancelled with `md/cancelChart`.

This matches the current Carver client boundary: authorize, request exactly one locked ZN chart, cancel the chart subscription, and save the raw response only under the Git-ignored quarantine.

## Interpretation For Carver

The cleanest current posture is:

```text
KEEP_CURRENT_CLIENT_AS_MD_TOKEN_ONLY
```

Reason:

- It avoids inspecting browser storage.
- It avoids collecting username/password/API secret in this chat.
- It avoids implementing an un-audited auth flow under a data-probe gate.
- It keeps the real-data action surface limited to the already-audited market-data WebSocket boundary.

## Operator Paths From Here

### Path A: Manual market-data token supply

The operator obtains a valid `mdAccessToken` through official means outside Codex, then writes only this local ignored field:

```text
runtime/tradovate_api_probe.env
CARVER_TRADOVATE_MD_ACCESS_TOKEN=<redacted>
```

Carver then runs the existing one-shot ZN direct-daily probe. This path requires no new code if the token is valid.

### Path B: Separate auth-token implementation gate

The operator authorizes a new narrow implementation gate for `/auth/accesstokenrequest`.

Minimum required constraints:

- Read credentials only from Git-ignored local env/file.
- Admit only the official fields required for auth.
- Do not print, commit, or echo any credential or token.
- Persist no token except in Git-ignored local runtime state.
- Extract only `mdAccessToken` for the S09 ZN market-data probe.
- Do not call account, order, report, trading, profile, or user endpoints.
- Do not run `md/getChart` in the auth gate.
- Require hostile audit before using the result.

### Path C: No API access; defer to manual export later

If the trial/live account cannot generate an API key or market-data token, record the API blockage and later open a separate manual direct-daily export gate. That would still forbid browser storage extraction and would not use minute-derived fallback unless direct daily is separately recorded as unavailable.

## Recommendation

Do not use Chrome remote debugging to steal or inspect a session token.

Do not broaden the existing S09 ZN API probe gate to username/password/API-secret auth by implication.

Use either Path A if the operator can obtain an official `mdAccessToken`, or Path B if the operator wants Carver to implement the official REST auth exchange as its own narrow, audited credential gate.

## Non-Authorization

This investigation authorizes no browser storage inspection, no credential extraction, no authentication request, no market-data request, no data export, no parsing, no diagnostics, no backtest, no returns, no PnL, no Sharpe, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push.
