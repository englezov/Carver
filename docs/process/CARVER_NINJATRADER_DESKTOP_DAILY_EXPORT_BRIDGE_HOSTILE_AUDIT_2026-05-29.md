# Carver NinjaTrader Desktop Daily Export Bridge Hostile Audit

Date: 2026-05-29

Status:

```text
PROCESS_SAFE_AFTER_PATCHES_NOT_EXECUTION_AUTHORIZATION
```

## Scope

Hostile audit of the NinjaTrader Desktop daily export bridge implementation:

```text
tools/nt8/CarverDailyBarExporter.cs
src/carver/spine/ninjatrader_desktop_export.py
tests/test_ninjatrader_desktop_daily_export_synthetic.py
docs/process/CARVER_NINJATRADER_DESKTOP_DAILY_EXPORT_BRIDGE_GATE_2026-05-29.md
src/carver/spine/__init__.py
```

## First Audit Blockers

The first hostile audit found three blockers:

1. The parser was generic enough that a caller could provide a matching non-ZN spec and matching non-ZN rows.
2. The default quarantine root was process-cwd relative instead of Carver-absolute.
3. The NinjaScript artifact could fail to write when a chart contained an in-progress daily bar after `LastCompletedTradeDateUtc`, because it returned before finalizing the export.

Non-blocking findings:

- File name was not locked to `ZN_06-26_Daily_Last_257.csv`.
- The C# writer used direct `File.WriteAllLines` instead of temp-file-then-move.

## Patches Applied

Parser hard locks:

```text
contract == ZN
contract_month == 06-26
display_symbol == ZN 06-26
bar_type == Last
timeframe == 1 Day
expected_rows == 257
```

Quarantine hardening:

```text
C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\desktop_daily_exports
```

is now the default absolute quarantine root.

Filename lock:

```text
ZN_06-26_Daily_Last_257.csv
```

is required by the Carver-side file parser.

NinjaScript runtime patch:

- When the script sees a bar after `LastCompletedTradeDateUtc`, it attempts the final write before returning.
- The final write goes to a `.tmp` file first, then moves into the locked output filename.

## Re-Audit Result

Second hostile audit found:

```text
Blockers: None.
```

Confirmed:

- Parser is hard-locked to `ZN`, `06-26`, `ZN 06-26`, `Last`, `1 Day`, exactly `257` rows.
- Default quarantine root is Carver-absolute.
- Filename is locked.
- C# writes before returning on newer-than-last-completed bars.
- C# writes through a temp file before moving into the locked output file.
- No order/account/report/API/browser-token path appears in the scoped files.
- Docs still forbid NinjaTrader execution, data export, trading, diagnostics, backtests, OOS/Lockbox/Forward, CFD, old QuantLab, tuning, deployment, promotion, and remote push.

## Verification

Local verification after patches:

```text
python -m unittest tests.test_ninjatrader_desktop_daily_export_synthetic -v
6 passed

python -m unittest discover -s tests -v
74 passed

python -m compileall -q src tests
passed

git diff --check
passed, with only expected CRLF warning on src/carver/spine/__init__.py
```

## Verdict

```text
PROCESS_SAFE_AFTER_PATCHES_NOT_EXECUTION_AUTHORIZATION
```

The bridge is safe as a process/implementation gate artifact.

It still authorizes no NinjaTrader Desktop import, no script run, no data export, no real ZN parse, no diagnostics, no backtest, no returns, no PnL, no Sharpe, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.
