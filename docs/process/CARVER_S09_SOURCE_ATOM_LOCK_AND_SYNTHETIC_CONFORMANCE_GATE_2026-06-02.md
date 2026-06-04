# Carver S09 Source Atom Lock And Synthetic Conformance Gate

Date: 2026-06-02

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_S09_SOURCE_ATOM_LOCK_NOT_DATA_NOT_BACKTEST
```

## Purpose

Lock the Strategy 9 source atoms needed to instantiate a source-clean multiple trend following forecast block, and define the synthetic-only conformance checks required before any real-data S09 gate.

This gate follows:

```text
docs/process/CARVER_S09_CHAPTER_OPENING_DECISION_2026-06-02.md
docs/process/CARVER_NEXT_CANDIDATE_AFTER_S26_S27_PARK_OPUS_HOSTILE_AUDIT_RAW_2026-06-02.md
```

## Lane Declaration

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` lane is opened.

## Source Atom Sheet

| Atom | Locked process value | Source anchor |
| --- | --- | --- |
| Strategy | Strategy nine: Multiple trend following rules | Carver pp. 201-231 |
| Input frequency | Daily completed prices | S09 chapter framing, pp. 201-203 |
| EWMAC speed set | `2, 4, 8, 16, 32, 64` | pp. 202-203 |
| EWMAC shorthand | `EWMACn = EWMAC(n, 4n)` | p. 203 |
| Per-speed scalars | `12.1, 8.53, 5.95, 4.10, 2.79, 1.91` for EWMAC `2,4,8,16,32,64` | Table 29, p. 204 |
| Individual forecast cap | `+/-20` after scalar | p. 203 |
| Forecast combination input | Combine individual capped forecasts, not raw forecasts | pp. 208-209 |
| Weights | Equal weights across the locked eligible surviving trend rules | pp. 215-220 |
| Cost/speed eligibility threshold | Book source verified as maximum `0.15` SR cost units | p. 216 |
| Turnover reference | EWMAC turnovers from Table 35 | pp. 217-218 |
| FDM rows | Table 36 rows for eligible suffix sets | p. 221 |
| Combined cap | Apply FDM, then cap combined forecast again at `+/-20` | pp. 221-222 |
| Position sizing/buffering | Inherited from prior trend machinery, not opened by this gate | p. 203 and S08 trading plan |

## Machine-Locked Synthetic Values

The synthetic code surface may use only these speed sets and FDM rows:

| Eligible EWMAC speeds | Equal weight | FDM |
| --- | ---: | ---: |
| `2, 4, 8, 16, 32, 64` | `1/6` | `1.26` |
| `4, 8, 16, 32, 64` | `1/5` | `1.19` |
| `8, 16, 32, 64` | `1/4` | `1.13` |
| `16, 32, 64` | `1/3` | `1.08` |
| `32, 64` | `1/2` | `1.03` |
| `64` | `1` | `1.00` |

Any other speed subset remains fail-closed until separately source-locked.

## Synthetic EWMA Convention

For synthetic conformance only:

```text
alpha = 2 / (span + 1)
initial EWMA = first completed synthetic close
minimum observations = slowest admitted span + 1
```

This convention tests deterministic arithmetic. It does not settle future real-data warm-up, production initialisation, cost eligibility, buffer, or position semantics.

## Synthetic Conformance Surface

Synthetic checks must use deterministic in-memory completed daily bars only:

- monotonic uptrend path to verify positive EWMAC sign at all six speeds;
- monotonic downtrend path to verify negative EWMAC sign at all six speeds;
- flat path to verify zero raw and final forecast;
- constructed extreme paths to verify individual and combined `+/-20` caps;
- all six Table 36 FDM rows;
- fail-closed checks for non-source-native lanes, unordered/non-suffix speed sets, future bars, mixed contracts, incomplete bars, unresolved source atoms, and timestamp-misaligned daily price risk.

## Boundaries

This gate does not open:

- provider access;
- Databento or NinjaTrader usage;
- Appendix C CSV parsing;
- market-row parsing;
- diagnostics;
- backtests;
- returns, PnL, Sharpe, drawdown, turnover, or costs;
- position sizing;
- buffering;
- carry;
- CFD adapter work;
- old QuantLab pipeline use;
- TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion, or GitHub publication.

## Exit Criteria

This gate passes only when:

- the source atom sheet above is preserved;
- synthetic tests prove EWMAC arithmetic, scalar application, individual caps, equal weights, FDM, and combined cap for all locked S09 speed rows;
- fail-closed governance checks pass;
- a local hostile audit records that no real data, strategy diagnostics, or backtest authorization was smuggled in.

The next gate after this one should be a data-readiness/backtest-readiness gate, not an implicit real-data run.

