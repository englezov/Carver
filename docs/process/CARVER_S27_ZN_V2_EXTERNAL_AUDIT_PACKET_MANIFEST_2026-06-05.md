# Carver S27 ZN V2 External Audit Packet Manifest

Date: 2026-06-05

Status:

```text
PROCESS_ONLY_S27_ZN_V2_EXTERNAL_AUDIT_PACKET_MANIFEST_NOT_HANDOFF_NOT_RUNNER_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

Define the focused file packet for a future external hostile audit of the S27
ZN v2 source-faithful machinery after local source-lock, implementation-slice,
replay-step, multi-row, and local data-contract gates.

This manifest does not copy files to any handoff folder. It does not write the
large-audit prompt to a file. Large hostile-audit prompts must be provided in
the agent response, not in a repository file.

This record authorizes no provider/API access, no data download, no file
parsing, no diagnostic, no backtest, no OOS, no Lockbox, no Forward, no tuning,
no alpha claim, no promotion, no Git staging, no commit, no push, no PR, no
deployment, and no trading.

## Book Attachment

The operator should attach the local book separately:

```text
Carver.pdf
```

Local presence observed:

```text
C:\Users\apops\Desktop\Carver\Carver.pdf
```

The book is intentionally not copied or committed by this manifest.

## GPT Extended Pro Packet

Maximum file limit:

```text
20_FILES
```

Recommended focused packet, excluding `Carver.pdf` because the operator
attaches the book separately:

| # | File | SHA256 |
|---|---|---|
| 1 | `docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md` | `72A3357F320F9D92C742F58CA9B5EC0D1B865DAD488D7ADDFFBCB5CD23DAB51F` |
| 2 | `docs/process/CARVER_S27_ZN_SOURCE_LOCK_REAUDIT_RESULT_2026-06-05.md` | `36B19F379037FA465D11662D26BDDAF20ECF2DA51C77B4F45248F43DF04B133A` |
| 3 | `docs/process/CARVER_S27_ZN_V2_LOCAL_DATA_CONTRACT_GATE_2026-06-05.md` | `A46EA99A47BE8E5D0863CC658166F16126B6FA009F1B3C1368C286C15605EF57` |
| 4 | `docs/process/CARVER_S27_ZN_V2_SOURCE_LOCK_IMPLEMENTATION_EXERCISE_2026-06-05.md` | `FF9FDF1484A56CEBAA771AFBFB12ED491F07D9D9D16752A568D86AB9E023043A` |
| 5 | `docs/process/CARVER_S27_ZN_V2_LOCAL_HOSTILE_AUDIT_RESULT_2026-06-05.md` | `13542DF162CDB80ECEC80C670A5687B8DA9C0C5F45B0440E2E6E4EDDA8E38276` |
| 6 | `src/carver/spine/s27_v2.py` | `567FC91106CBDE05A876708497C5A1C9290828A29A6A3B93AC0CD4386BEF751F` |
| 7 | `tests/test_s27_v2_source_lock_synthetic.py` | `E46D12D2DE03B9B1E5CEFDB3A4ACB1C9BE66BC2BBB430C63632905AA3E267225` |

GPT audit focus:

- Source faithfulness to attached `Carver.pdf`.
- S26/S27 scalar treatment.
- EWMA5 equilibrium and EWMAC(16,64) trend veto.
- V/Q/M construction and causality.
- Sigma-price bridge and strict-prior daily/hourly alignment.
- Adjacent limit-order execution, market-order cases, one-hour lag, session,
  overnight, and roll handling.
- Commission and spread cost boundaries.
- Ledger/provenance completeness.
- Fail-closed behavior and test coverage.
- Absence of old diagnostic runner, CFD adapter, provider/API, data download,
  file parser, backtest runner, or OOS/Lockbox/Forward path.

## Opus Packet

Maximum file limit:

```text
5_FILES_PLUS_BOOK
```

Recommended packet, excluding `Carver.pdf` because the operator attaches the
book separately:

| # | File | SHA256 |
|---|---|---|
| 1 | `docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md` | `72A3357F320F9D92C742F58CA9B5EC0D1B865DAD488D7ADDFFBCB5CD23DAB51F` |
| 2 | `docs/process/CARVER_S27_ZN_V2_LOCAL_DATA_CONTRACT_GATE_2026-06-05.md` | `A46EA99A47BE8E5D0863CC658166F16126B6FA009F1B3C1368C286C15605EF57` |
| 3 | `docs/process/CARVER_S27_ZN_V2_LOCAL_HOSTILE_AUDIT_RESULT_2026-06-05.md` | `13542DF162CDB80ECEC80C670A5687B8DA9C0C5F45B0440E2E6E4EDDA8E38276` |
| 4 | `src/carver/spine/s27_v2.py` | `567FC91106CBDE05A876708497C5A1C9290828A29A6A3B93AC0CD4386BEF751F` |
| 5 | `tests/test_s27_v2_source_lock_synthetic.py` | `E46D12D2DE03B9B1E5CEFDB3A4ACB1C9BE66BC2BBB430C63632905AA3E267225` |

If Opus needs the external source-lock re-audit details, replace the local
data-contract gate with:

```text
docs/process/CARVER_S27_ZN_SOURCE_LOCK_REAUDIT_RESULT_2026-06-05.md
```

## Handoff Folder Rule

For GPT Extended Pro through the app, the handoff folder is:

```text
C:\Users\apops\Desktop\GPT
```

Before any actual handoff, the folder must be cleaned and repopulated under
separate operator authorization. This manifest performs no folder cleanup and
no file copy.

## Gate Decision

Current gate:

```text
S27_V2_EXTERNAL_AUDIT_PACKET_MANIFEST_CREATED_PROCESS_ONLY_NOT_HANDOFF
```

Next required action:

```text
OPERATOR_ASSISTED_EXTERNAL_AUDIT_HANDOFF_IF_DESIRED
```

Still not authorized:

```text
NO_PROVIDER_API
NO_DATA_DOWNLOAD
NO_FILE_PARSING
NO_DIAGNOSTIC
NO_BACKTEST
NO_OOS
NO_LOCKBOX
NO_FORWARD
NO_TUNING
NO_ALPHA_CLAIM
NO_PROMOTION
NO_GIT_STAGE_COMMIT_PUSH_PR
NO_HANDOFF_FOLDER_CLEAN_OR_COPY
```
