# S09 MES Cost-Screen Suspicion Hostile Audit Result

Supersession:

```text
SUPERSEDED_BY_CORRECTED_S09_MES_RISK_COST_UNIT_BRIDGE_ANNUALIZED_USD_RISK
```

This audit correctly found the no-surviving-speed conclusion unsafe, but its
multiplier-only repair was an intermediate hypothesis. The current correction
uses annualized USD risk: daily point risk * 16 * MES 5 USD/point multiplier.
See
`docs/process/CARVER_S09_MES_RISK_COST_UNIT_BRIDGE_CORRECTION_RESULT_2026-06-03.md`.

Date: 2026-06-03

Status:

```text
FAIL_CURRENT_NO_SURVIVING_SPEED_CONCLUSION_UNSAFE_UNIT_MISMATCH_FOUND
```

Subagent constraint note:

The separate subagent tool was not exposed in this session. I performed the hostile audit directly under the requested constraints and wrote only this file.

Scope honored:

- Re-read `README.md`, `docs/mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md`, `docs/process/CLEAN_WORKSPACE_MIGRATION_RECORD_2026-05-28.md`, and `docs/process/LANE_CLASSIFICATION_AND_ADAPTER_QUARANTINE_RULES_2026-05-28.md`.
- No forecasts, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, provider API/network downloads, Git, remote operations, deployment, trading, or promotion were run.
- This audit inspected only current local code and locked local artifacts.

Concrete finding:

The current no-surviving-speed result is mathematically correct for the implemented formula, but the implemented formula appears to divide USD round-turn costs by an unmultiplied price-point risk denominator. That is a unit mismatch.

The daily risk ledger column is named `daily_price_risk_currency`, and the risk-adjusted cost code divides USD costs by that value. However, the daily risk value is currently computed as:

```text
current_price * annual_percentage_risk / 16
```

For MES, that is an index-points daily risk value, not USD per contract, unless it is multiplied by the MES contract multiplier. The locked MES multiplier is `5.0`, and spread/slippage was already converted from points to USD using that same multiplier. Therefore the numerator is USD, while the denominator is currently points.

Evidence inspected:

- `src/carver/spine/s09_mes_readiness.py:517-541` computes daily risk via `s09_daily_price_risk` and labels the result `daily_price_risk_currency`; line 540 records `LOCKED_CURRENT_PRICE_TIMES_LOCKED_ANNUAL_PERCENTAGE_RISK_OVER_16`.
- `src/carver/spine/s09_mes_readiness.py:828-843` computes `risk_adjusted_cost_per_trade_sr = total_cost_per_trade_currency / daily_price_risk_currency`.
- `src/carver/spine/s09_mes_readiness.py:846-877` applies `turnover * risk_adjusted_cost_per_trade_sr <= 0.15`.
- `tools/databento/carver_s09_mes_dual_speed_eligibility_values.py:130-159` implements the same speed burden calculation for the dual scenarios.
- `tools/databento/carver_s09_mes_strategy_input_evidence_completion.py:4061-4071` computes daily risk as `current_price * annual_percentage_risk / 16`.
- `tools/databento/carver_s09_mes_strategy_input_evidence_completion.py:4622-4629` validates that formula exactly, without multiplier.
- `tools/databento/carver_s09_mes_dual_cost_scenario_policy.py:33` locks `MES_MULTIPLIER = 5.0`.
- `tools/databento/carver_s09_mes_dual_cost_scenario_policy.py:126-160` uses `MES_MULTIPLIER` for notional but still divides costs by the unmultiplied daily-risk ledger value.
- `tools/databento/carver_s09_mes_spread_slippage_tbbo_source_native_extraction.py:168-188` converts median spread points to USD with `locked_round_turn_usd = rounded_spread_points * MES_MULTIPLIER`.
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_DAILY_PRICE_RISK_ledger.csv` locks `2020-03-02,3072.5,0.29778305426118784,57.18365213859373`.
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_DUAL_RISK_ADJUSTED_COST_ledger.csv` locks `2.93 / 57.18365213859373 = 0.051238` and `2.49 / 57.18365213859373 = 0.043544`.
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/speed/20260603_S09_MES_DUAL_SPEED_ELIGIBILITY_ledger.csv` locks no surviving speed under those ratios.
- `docs/process/CARVER_P05_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_2026-05-29.md:237-248` supports the 0.15 SR threshold and Strategy Nine turnover table, including `EWMAC64 = 5.2`, and notes no cheap-enough variation means the instrument cannot be traded.

Arithmetic table:

```text
locked point risk = 57.18365213859373
MES multiplier = 5.0
currency risk if multiplier applied = 285.91826069296865
threshold = 0.15 SR
```

| Scenario | Cost USD | Span | Turnover | Current ratio using 57.183652 | Current burden | Current pass | Multiplied ratio using 285.918261 | Multiplied burden | Multiplied pass |
|---|---:|---:|---:|---:|---:|---|---:|---:|---|
| Conservative | 2.93 | 2 | 98.5 | 0.051238 | 5.046984 | NO | 0.010248 | 1.009397 | NO |
| Conservative | 2.93 | 4 | 50.2 | 0.051238 | 2.572169 | NO | 0.010248 | 0.514434 | NO |
| Conservative | 2.93 | 8 | 25.4 | 0.051238 | 1.301456 | NO | 0.010248 | 0.260291 | NO |
| Conservative | 2.93 | 16 | 13.2 | 0.051238 | 0.676347 | NO | 0.010248 | 0.135269 | YES |
| Conservative | 2.93 | 32 | 7.6 | 0.051238 | 0.389412 | NO | 0.010248 | 0.077882 | YES |
| Conservative | 2.93 | 64 | 5.2 | 0.051238 | 0.266440 | NO | 0.010248 | 0.053288 | YES |
| ETF all-in | 2.49 | 2 | 98.5 | 0.043544 | 4.289075 | NO | 0.008709 | 0.857815 | NO |
| ETF all-in | 2.49 | 4 | 50.2 | 0.043544 | 2.185904 | NO | 0.008709 | 0.437181 | NO |
| ETF all-in | 2.49 | 8 | 25.4 | 0.043544 | 1.106015 | NO | 0.008709 | 0.221203 | NO |
| ETF all-in | 2.49 | 16 | 13.2 | 0.043544 | 0.574780 | NO | 0.008709 | 0.114956 | YES |
| ETF all-in | 2.49 | 32 | 7.6 | 0.043544 | 0.330934 | NO | 0.008709 | 0.066187 | YES |
| ETF all-in | 2.49 | 64 | 5.2 | 0.043544 | 0.226428 | NO | 0.008709 | 0.045286 | YES |

Audit answers:

1. Formula implementation: internally consistent, but currently uses `total_cost_usd / daily_price_risk_currency` where the denominator is generated from price points, not USD per contract.
2. Locked inputs: current cost and speed artifacts are hash-bound local locks, but the risk-adjusted-cost and speed locks inherit the denominator unit mismatch.
3. Denominator: `57.183652` should not be treated as USD unless source governance explicitly says MES multiplier is excluded. Current evidence points the other way because costs and spread/slippage are USD and the MES multiplier is locked at `5.0`.
4. Turnover: current evidence supports the Strategy Nine turnover table as source average turnover estimates in annual SR cost-screen units.
5. Spread/slippage double count: no direct double count found. TBBO spread was converted from points to USD once as a round-turn cost. The issue is denominator mismatch, not spread double-counting.
6. Threshold: `0.15 SR` is source-supported in the process evidence and matches the turnover screen form, but the risk-adjusted cost term must be in the same SR/currency unit before use.
7. Alternative plausible interpretations: with the MES multiplier applied to daily price risk, no-surviving-speed is false. Both locked cost scenarios would pass spans `16,32,64`, while faster spans `2,4,8` remain too expensive.

Recommended governance action:

Fail closed on the current `speed_eligibility_values` result as unsafe for readiness decisions. Do not treat S09 MES as cost-blocked. Open a narrow operator-authorized correction gate for `daily_price_risk_currency_unit_repair` or equivalent:

- preserve the existing unmultiplied point-risk ledger as `daily_price_risk_points` or mark it superseded for cost screening;
- lock MES multiplier source evidence into the risk/cost unit bridge;
- compute `daily_price_risk_currency = daily_price_risk_points * MES_MULTIPLIER`;
- recompute dual risk-adjusted costs and speed eligibility from existing locked local artifacts only;
- keep forecasts, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, Git, remote operations, deployment, trading, and promotion forbidden until the corrected cost-screen artifacts pass hostile audit.
