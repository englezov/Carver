# S27_V2 Desired-Position Executable Remediation-Pack Implementation Record

Date: 2026-06-09

Status:

```text
LOCAL_IMPLEMENTATION_COMPLETE_LOCAL_HOSTILE_REAUDIT_PASS
```

## Authorization

Operator authorized `S27_V2` non-result desired-position executable ledger implementation after external PASS on the position policy decision and evidence binding packet.

Authorized scope:

- construct deterministic local-only desired-position ledger rows for the audited `ZNM6` remediation pack;
- bind the desired-position row to the active forecast executable bundle;
- apply externally passed position policies:
  - capital/account value `500000 USD`;
  - annual risk target `20%`;
  - instrument weight `1.0`;
  - IDM `1.0`;
  - USD/USD FX `1.0`;
  - ZN point value `1000 USD` per full point from Appendix C/static authority;
  - forecast-to-position divisor `10.0`, locally bound pending external/source-formula audit;
  - base/optimal position formula;
  - `ROUND_HALF_AWAY_FROM_ZERO`;
  - first-row flat-zero initial/current position context;
  - hard rejection of Databento definition `contract_multiplier = 2147483647` as point-value authority;
- focused local verification tests;
- local hostile audits and narrow follow-up patches for in-scope findings.

Non-authorized scope:

- no provider/API access;
- no downloads or new data;
- no OOS/Lockbox/Forward;
- no backtests or result-scored runs;
- no order/fill/cost/PnL/result emission;
- no result interpretation or PnL evaluation;
- no tuning;
- no adapter work, deployment, trading, promotion;
- no Git actions;
- no source-faithful evidence claim.

## Files Added

```text
src/carver/spine/s27_v2_replay/desired_position_executable.py
tests/test_s27_v2_desired_position_executable.py
```

## Implementation Summary

The new desired-position surface follows the established S27_V2 executable pattern:

- standalone `DesiredPositionExecutableLedgerRow.validate()` fails closed and is not authoritative;
- `DesiredPositionExecutableBundle.validate()` is the only accepting validation path;
- bundle validation rebuilds the active forecast executable bundle from the audited remediation pack;
- bundle validation rebuilds the active desired-position row from the active forecast bundle and locked policies;
- self-consistent forged rows, hashes, policy constants, forecast bundles, and downstream flags are rejected;
- order/fill/cost/PnL/result/source-faithful-evidence flags are rejected;
- no public package-root export was added.

## Desired-Position Policy Binding

Locked policy constants:

```text
capital_account_value = 500000.0
capital_currency = USD
annual_target_risk = 0.20
instrument_weight = 1.0
instrument_diversification_multiplier = 1.0
fx_rate = 1.0
fx_rate_pair = USD/USD
forecast_to_position_divisor = 10.0
contract_point_value = 1000.0
contract_point_value_currency = USD
rounding_policy = ROUND_HALF_AWAY_FROM_ZERO
initial_current_position_contracts = 0
```

Position formula:

```text
base_unrounded_contracts =
    capital_account_value
    * annual_target_risk
    * instrument_weight
    * instrument_diversification_multiplier
    / (
        current_price
        * contract_point_value
        * fx_rate
        * annual_percentage_risk
    )

desired_unrounded_contracts =
    base_unrounded_contracts
    * capped_forecast
    / forecast_to_position_divisor

desired_rounded_contracts =
    ROUND_HALF_AWAY_FROM_ZERO(desired_unrounded_contracts)
```

## Source-Evidence Boundary

Appendix C/static evidence is used for ZN point-value authority:

```text
contract_point_value = 1000 USD per full point
```

Provider definition evidence is used only for selected-contract identity and effective-date binding:

```text
raw_symbol = ZNM6
instrument_id = 42000661
currency = USD
exchange = XCBT
group = ZN
asset = ZN
security_type = FUT
activation = 2025-09-19 21:30:00+00:00
expiration = 2026-06-18 17:01:00+00:00
```

The implementation hard-rejects use of the Databento definition field:

```text
contract_multiplier = 2147483647
```

as point-value authority.

After local hostile-audit P2 hardening, the implementation also:

- byte-locks the audited remediation manifest;
- byte-locks the audited `cost_parameter.csv`;
- byte-locks the Appendix C/static spec source file;
- byte-locks the provider definition source file;
- selects the unique latest-prior active `ZNM6` provider definition row at or before the selected decision timestamp;
- asserts `instrument_id = 42000661`;
- asserts `exchange = XCBT`;
- asserts exact activation `2025-09-19 21:30:00+00:00`;
- asserts exact expiration `2026-06-18 17:01:00+00:00`.

## Deterministic Output Metadata

The authorized local builder produced:

```text
bundle_hash = e2e2e7f312dca29a403d30fd4e08e95a66cca58265735215ca65da449267e685
row_hash = 990bd47a3dcc7ab7bebe54112369650062dc33049a107c551fd15784f837f382
raw_symbol = ZNM6
selected_decision_timestamp_utc = 2026-04-13T03:00:00Z
base_unrounded_contracts = 14.318967539315619
capped_forecast_value = 0.0
desired_unrounded_contracts = 0.0
desired_rounded_contracts = 0
provider_definition_znm6_row_hash = 30c82b556e1ab4960a314431fc70d1afe4e1b0bd22a82e66f36c18db5c35e6bc
```

This is desired-position ledger metadata only. It is not a backtest, not PnL, not a result interpretation, not promotion evidence, and not a source-faithful evidence claim.

## Focused Verification

Verification passed:

```text
python -m pytest tests\test_s27_v2_desired_position_executable.py -q
28 passed in 110.98s

python -m py_compile src\carver\spine\s27_v2_replay\desired_position_executable.py tests\test_s27_v2_desired_position_executable.py
PASS

python -m pytest tests\test_s27_v2_forecast_executable.py tests\test_s27_v2_position_evidence_gate.py tests\test_s27_v2_desired_position_executable.py -q
79 passed in 289.50s
```

The first combined focused run timed out at 244 seconds before reporting. It was rerun with a longer timeout and passed.

## Test Coverage

Focused tests cover:

- normal desired-position build;
- formula arithmetic;
- half-away-from-zero rounding examples;
- out-of-scope pack rejection;
- audited remediation manifest/source byte-hash pinning through active build;
- unique latest-prior provider definition row binding;
- exact `ZNM6` provider identity/effective-date binding;
- standalone row validation fail-closed;
- forged forecast bundle rejection;
- self-consistent policy/numeric row forgery rejection;
- hard rejection of provider `contract_multiplier = 2147483647` as point-value authority;
- downstream order/fill/cost/PnL/result/source-faithful-evidence flag rejection;
- desired-position emission flag must remain explicitly true for this authorized non-result surface.

## Next Step

Local hostile re-audit passed after the P2 hardening patch. Record:

```text
docs/process/CARVER_S27_ZN_V2_DESIRED_POSITION_EXECUTABLE_REMEDIATION_PACK_LOCAL_AUDIT_RESULT_2026-06-09.md
```

Prepare an external GPT/alternate hostile-audit handoff packet before moving to any later order/fill/cost/PnL/backtest-readiness gate.

## Non-Authorization

This record authorizes no provider/API access, downloads, new data, OOS/Lockbox/Forward, backtests, result-scored runs, order/fill/cost/PnL/result emission, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim.
