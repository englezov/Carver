# S27 ZN V2 GPT Replay Scaffold Patched External Audit Synthesis

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_GPT_REPLAY_SCAFFOLD_PATCHED_EXTERNAL_AUDIT_SYNTHESIS_NOT_PATCH_OR_REPLAY_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

Record the operator-supplied GPT Extended Pro / GPT-5.5 hostile external audit result for the patched S27 V2 replay scaffold packet.

This is a process-only synthesis. It authorizes no code patch, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Audited Packet

Handoff record:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_PATCHED_EXTERNAL_AUDIT_HANDOFF_2026-06-06.md
```

Packet target:

```text
C:\Users\apops\Desktop\GPT
```

Packet contained `Carver.pdf`, the source-lock/design/planning records, local hostile-audit and patch records, current-state record, and a zip of the patched scaffold package.

## External Verdict

GPT verdict:

```text
PASS_WITH_REQUIRED_EDITS
```

Local synthesis:

```text
S27_V2_REPLAY_SCAFFOLD_NOT_READY_FOR_PARSER_FILE_REPLAY_IMPLEMENTATION
S27_V2_REPLAY_SCAFFOLD_READY_FOR_NARROW_SCHEMA_HARDENING_PATCH_GATE_ONLY
```

GPT found no P0 and found no immediate forbidden execution surface. The runner still fails closed. The blocking issues are P1 schema/provenance gaps that must be patched before any parser/file replay implementation relies on the scaffold.

## P0 Synthesis

No P0 reported.

GPT found no provider/API/download path, no parser/file replay execution path, no diagnostic/backtest/OOS/Lockbox/Forward surface, no subprocess/CLI/Git/deployment/trading surface, and no code path that computes or presents PnL/performance.

## P1 Required Edits

The next patch gate must address these P1 categories:

1. **Order-kind-specific cost rules**
   - Limit fills must be commission-only.
   - Market fills must include positive normal spread.
   - Preserve price-space spread multiplier proof.
   - Add cost calculation binding so commission, spread, and total cost are not mutually arbitrary.

2. **Limit/market order source-faithfulness**
   - Limit orders must be adjacent single-lot orders.
   - Order rows must bind `current_position_before_order`.
   - Limit side/target consistency must fail closed.
   - Market quantity/side must match current-to-target position delta.

3. **Order/fill enum validation**
   - `OrderSide` must be explicitly validated in order and fill rows.

4. **Desired-position rounding**
   - `rounding_policy` must be exactly `NEAREST`.

5. **Forecast ledger value auditability**
   - Forecast rows must expose actual values or bound canonical value payloads for EWMA5 equilibrium, raw forecast, sigma bridge, annual percentage sigma, sigma price, risk-adjusted forecast, EWMAC/trend sign, veto decision, V/Q/M, scalar, cap, and desired unrounded position.
   - Minimum scalar guard: carry `scalar_value` and require `20.0` with the existing book-approximate scalar label.

6. **Transition/session/lag facts**
   - Add exact transition kind validation.
   - Bind one-hour lag proof, session transition row, raw-symbol/session/date continuity proof, roll-boundary fact where applicable, and overnight recompute policy where applicable.

7. **PnL schema hardening**
   - Require close-only price source.
   - Add multiplier value hash.
   - Add currency/FX policy/value/source fields where applicable.
   - Preserve fail-closed currency value/source pairing.

8. **Trust-root/evidence-manifest cross-check**
   - `TrustedReplayBundleScaffold.validate()` must require equality between `ReplayTrustRoot.active_evidence_manifest_hash` and `EvidenceManifest.active_evidence_manifest_hash`.

9. **Source-row value schemas**
   - Before parser implementation, add explicit daily, hourly decision/fill, session, roll, and cost-parameter row schemas or bound value payloads with completed timestamps, trading dates, raw symbols, closes, sigma values, readiness/status, row locators, and row hashes.

10. **Date validation**
    - ISO date validation for `ReplayIdentity.completed_trading_date`, `SourceUniverseProof.requested_start`, and `SourceUniverseProof.requested_end`.
    - Start/end ordering validation where applicable.

11. **Process-record drift**
    - Update stale "Next Gate" text in the scaffolding record so the cost-schema re-audit is not shown as pending after it passed.

## P2 Synthesis

GPT also flagged lower-severity issues:

- compatibility verdict/reason fields should become exact labels or enums;
- `TrustedReplayBundleScaffold` naming may overstate trust until child ledgers are included;
- import/compile assurance is absent by design under current authorizations and should be separately authorized before parser work, without becoming replay/backtest execution.

## Gate Decision

The patched scaffold must not proceed to parser/file replay implementation.

Next allowed progress requires separate operator authorization for a narrow schema-hardening patch addressing the P1 list above.

Recommended authorization text:

```text
Operator authorizes S27_V2 replay scaffold GPT P1 schema-hardening patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```
