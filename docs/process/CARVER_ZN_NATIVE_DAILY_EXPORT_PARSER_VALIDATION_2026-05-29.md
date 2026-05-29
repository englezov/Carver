# Carver ZN Native Daily Export Parser Validation

Date: 2026-05-29

Status:

```text
CARVER_ZN_NATIVE_DAILY_EXPORTS_PARSER_VALIDATED_NOT_STITCHED_NOT_DIAGNOSTIC
```

## Scope

Parser-only validation and merge-policy forensics for the four ZN daily `Last` files exported by the NinjaTrader manifest helper.

Input files stayed under the Git-ignored quarantine:

```text
C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\native_daily_exports\ZN
```

No market data rows are committed in Git.

This record does commit data-derived parser metadata: row counts, first/last dates, first/last OHLC summaries, and file hashes. It does not commit full market rows, continuous series rows, returns, signals, diagnostics, or performance outputs.

## Manifest Binding

Validation used the manifest-bound parser in:

```text
src/carver/spine/data_acquisition.py
```

Allowed files:

```text
ZN/ZN 09-25.Last.txt
ZN/ZN 12-25.Last.txt
ZN/ZN 03-26.Last.txt
ZN/ZN 06-26.Last.txt
```

Parser requirements:

- source-native futures only;
- declared manifest request only;
- `Day` interval;
- `Last` data type;
- exact filename;
- exact quarantine path;
- completed date-aligned daily bars;
- finite positive OHLC;
- finite non-negative volume;
- strict increasing dates;
- no duplicate dates;
- no rows outside the locked request window.

## File Hashes

```text
ZN 09-25.Last.txt 2C5CFE112AD5AB717F310A78F50C9AC5D82E8B6C41234E51ED97089DB53AB619
ZN 12-25.Last.txt 0B48F7CAEF747ED1131B3EFE5F6DEE9B05E34D384F99A18BCA117B1560DFB430
ZN 03-26.Last.txt BAE21942C8FE7E3C5C7CFEDDAFDB670D93248875611EFB71B48FCD30467A3F5C
ZN 06-26.Last.txt A91A6FAF6CD6284D422A19B1EEB5D264839844FB0E36A8D46C36BA65EC14DFB9
```

## Parser-Only Summary

Manifest: `CARVER_PARTS_1_3_DAILY_SEED_S09_ZN_CONTINUOUS_READINESS`

| File | Rows | First date | Last date | First OHLC | Last OHLC |
|---|---:|---|---|---|---|
| ZN/ZN 09-25.Last.txt | 82 | 2025-05-29 | 2025-09-19 | 110.234/110.734/109.812/110.688 | 112.891/112.891/112.75/112.828 |
| ZN/ZN 12-25.Last.txt | 147 | 2025-05-29 | 2025-12-19 | 110.266/110.766/109.844/110.719 | 112.844/112.875/112.609/112.703 |
| ZN/ZN 03-26.Last.txt | 210 | 2025-05-29 | 2026-03-20 | 110.219/110.719/109.797/110.672 | 111.297/111.297/110.672/110.797 |
| ZN/ZN 06-26.Last.txt | 259 | 2025-05-29 | 2026-05-28 | 110.141/110.641/109.719/110.594 | 109.875/110.234/109.547/110.047 |

Minimum continuous-readiness target:

```text
257 rows
```

## Merge-Policy Forensics

The four files all begin on the requested start date:

```text
2025-05-29
```

However, their first OHLC values are not identical:

```text
largest identical first-date cluster: 4
largest identical first-OHLC cluster: 1
potential provider merge policy by exact first-OHLC test: FALSE
```

Interpretation:

- The files passed parser-only validation as manifest-declared source-native ZN daily `Last` files.
- The identical first date alone does not prove provider merge contamination because the helper requested the same start date for every contract.
- The first OHLC values differ by contract, so this validation pass did not find exact first-bar cloning across contracts.
- This record does not authorize using the files as a continuous series. Roll rule, merge policy, and back-adjustment remain separately blocked.

## Verification

```text
subagent hostile audit:
PROCESS_SAFE_PARSER_VALIDATION_AND_FORENSICS_NOT_STITCHED_NOT_DIAGNOSTIC

python -m unittest tests.test_data_acquisition_synthetic -v
11 passed

python -m compileall -q src tests
passed

python -m unittest discover -s tests -v
85 passed

git ls-files -- data/**
no tracked data files
```

## Non-Authorization

This validation authorizes no continuous stitching, no roll/back-adjustment construction, no strategy computation, no S09 forecast, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.
