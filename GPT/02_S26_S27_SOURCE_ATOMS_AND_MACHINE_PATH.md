# S26/S27 Source Atoms And Machine Path

Status:

```text
SOURCE_ATOM_AND_MACHINE_PATH_SUMMARY_FOR_MECHANICAL_VERIFICATION_AUDIT
```

## Locked Source Atoms Claimed By Current Implementation

S26:

- Equilibrium is EWMA span 5 over hourly price.
- Raw forecast is `equilibrium - price`.
- Risk-adjusted forecast divides by sigma price.
- Forecast scalar is `9.3` for S26.
- Forecast cap is +/-20.
- No FDM.
- No buffering.
- Hourly data required.

S27:

- Uses S26 fast mean reversion as base.
- Uses EWMAC(16,64) trend proxy.
- Mean-reversion forecast must not oppose trend forecast.
- Uses V/Q/M-style volatility attenuation.
- Volatility multiplier is EWMA(10) of the attenuation term.
- Forecast scalar is around `20` for S27 after trend overlay and volatility multiplier.
- Forecast cap remains +/-20.

## Scalar Blocker Disposition

The stale concern that S27 might inherit the S26 scalar `9.3` was locally resolved on 2026-06-01 by direct source check:

```text
S26 scalar: 9.3
S27 scalar: around 20 / implemented as 20.0
S27 cap: +/-20
BACKTEST_RESULT_SCALAR_STATUS: NOT_FAILED_BY_SCALAR_ATOM
```

Artifact:

```text
docs/process/CARVER_S27_SCALAR_BLOCKER_DISPOSITION_2026-06-01.md
SHA256: 848F2CDAE1BC5529B410F1DB5949C47E96BC2565B93A1ADE06FB1A7099E48033
```

Related code/source-lock patch:

- `src/carver/spine/s26_s27.py` now labels the source lock as S27 scalar/cap status, not inherited S26 scalar.
- `tests/test_s26_s27_fast_mean_reversion_synthetic.py` was updated accordingly.

Verification after patch:

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic -v
42 passed

python -m unittest discover -s tests -v
198 passed, 1 skipped
```

## Current Machine Path

Current source-native ZN machine path:

```text
Databento dated contract OHLCV rows
-> local dated-contract continuous lineage
-> daily runtime rows: sigma, EWMAC16 trend proxy, V/Q/M multiplier
-> hourly S26/S27 forecast rows
-> M1-style ladder/base-position rows
-> desired rounded position rows
-> close-to-close hourly PnL rows
-> ETF public per-side commission estimate
-> mechanical verification replay and recomputation
```

This is source-native futures Development/Reconciliation work. It is not a full Carver limit-order execution simulator and does not include spread, slippage, settlement substitution, prop-firm flattening, margin, carry, portfolio integration, OOS, Lockbox, Forward, deployment, trading, or promotion.

## Position And Cost Constants Used In Current ZN Path

```text
capital_usd = 100000
target_risk = 0.20
instrument_weight = 1.0
idm = 1.0
fx_rate = 1.0
zn_multiplier = 1000.0
forecast_to_position_divisor = 10.0
rounding_policy = NEAREST
cost_model = ETF public per-side commission only
ETF_ZN_FEE_PER_SIDE_USD = 1.51
```

## Scripts Of Interest

| Script | SHA256 |
|---|---:|
| `tools/audit/carver_s27_zn_mechanical_verifier.py` | `E426668D744D1010DF3003F8AAE48353171F02DBAD65005A9CF277D4738E1A4F` |
| `tools/audit/carver_s27_zn_parity_verifier.py` | `EF217262CA9ACC0629FC75BEF826A5073D601D039223FA3A6ECAB2E2FC742C39` |
| `tools/databento/carver_s27_zn_2024_validation_backtest.py` | `39A26DCE9D291FC2D3280DDB851E020EDF213B06C0CE0961F4ED753D5A2FE52D` |
| `tools/databento/carver_s27_candidate_comparison_2022_2023.py` | `ADA1E91423DDAAF0594DA98CCBA5CAF2E74C8B0EB3054304C0F774633328EC79` |

## Main Hostile Question

The mechanical verifier now recomputes forecast, position, PnL, fees, roll/runtime alignment, and no-promotion boundaries from existing local artifacts. The audit should decide whether this is independent enough or still shares a blocking assumption with the original backtest path.
