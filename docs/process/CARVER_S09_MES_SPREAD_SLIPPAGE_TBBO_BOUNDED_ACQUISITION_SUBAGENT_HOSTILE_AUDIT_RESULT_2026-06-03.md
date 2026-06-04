# S09 MES Spread Slippage TBBO Bounded Acquisition Hostile Audit Result

Date: 2026-06-03

Status:

```text
PASS_TBBO_BOUNDED_RAW_ACQUISITION_NO_SPREAD_LOCK
```

Tooling note:

```text
PARENT_THREAD_SPAWNED_HOSTILE_AUDIT_SUBAGENT
```

The operator requested a spawned hostile-audit subagent. The parent thread
spawned a fresh hostile-audit subagent for this bounded TBBO acquisition audit.
Any subagent-local tool exposure limitation is not a failure of the
parent-thread spawn requirement. The work performed here was read/audit plus
writing this audit result file only.

Authorized scope verified:

- operator_authorization: tbbo bounded acquisition only
- lane_class: SOURCE_NATIVE_FUTURES
- provider: DATABENTO_HISTORICAL
- dataset: GLBX.MDP3
- schema: tbbo
- stype_in: raw_symbol
- raw_symbols: MESM9, MESU9, MESZ9, MESH0, MESM0
- window: 2019-05-05 through 2020-04-05
- request_start: 2019-05-05
- request_end_exclusive: 2020-04-06
- row_id: APPENDIX_C_174_006

Raw TBBO file verification:

| Symbol | Size bytes | SHA256 | Result |
| --- | ---: | --- | --- |
| MESM9 | 42428016 | C65BEEC9897B9FB0842F602EF7EE71D03C051E9C7A71AAC8E16E8BCDD7B1D991 | receipt ledger matches file |
| MESU9 | 125879478 | 45742C6AE8CC76841F9006FC2D3F2613E351D2DF9633E5F137F39DC17138FFD3 | receipt ledger matches file |
| MESZ9 | 104488616 | 9704BC134FB17BB70E8D357B735FDB465FAA33BAF9A86DE91C34F518E27A1B6F | receipt ledger matches file |
| MESH0 | 237153572 | D91C87DC2222634FE169DA0364E4D5C862B15FA3721D329E6C0AD7753A1D9998 | receipt ledger matches file |
| MESM0 | 187024247 | 879C061CBC1F6F2A510B265BFABD02AF51B440225744C0ABB028838426AB12F8 | receipt ledger matches file |

The five raw DBN files exist, and the receipt ledger hashes and sizes match the
current files. Total verified raw DBN size is 696973929 bytes.

Provider-quality warning verification:

- 2020-02-27 degraded
- 2020-02-28 degraded

These warnings are recorded in the TBBO acquisition status and provenance and
must be explicitly handled by any later spread/slippage extraction. This audit
does not authorize or perform that extraction.

Fail-closed checks:

- no MBP-1 data file was found in the S09 machinery evidence tree
- `mbp_1_download` remains `NO`
- `spread_slippage_policy_lock` remains `NO`
- no spread/slippage value or policy was selected or locked
- active historical MES cost ledger remains header-only with 1 line
- `historical_mes_cost_values` remains `FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED`
- S09 strategy input evidence completion remains fail-closed with `remaining_evidence_count: 6`

Hash-manifest checks:

- TBBO bounded acquisition hash manifest: 11 entries, 0 missing or mismatched
- historical cost-source hash manifest: 56 entries, 0 missing or mismatched

Negative-scope verification:

No cost computation, risk-adjusted cost computation, speed-eligibility
computation, forecast computation, diagnostics, backtests, TEST, VALIDATION,
Lockbox, Forward, CFD adapter work, QuantLab/old adapter reuse, Git staging,
commit, push, PR, deployment, trading, promotion, or remote publication was
performed by this audit.

Verdict:

The bounded raw TBBO acquisition is internally consistent and remains within
the operator-authorized route. It is raw source-native evidence for later
spread/slippage extraction only. It is not a cost lock, not a spread/slippage
policy, and not authorization to proceed to computation or backtesting.
