# S27_V2 Desired-Position Executable External Audit Synthesis

Date: 2026-06-09

Status:

```text
EXTERNAL_HOSTILE_AUDIT_PASS_NO_P0_P1_P2
```

## Source

Operator pasted GPT/alternate external hostile-audit result for the desired-position executable handoff packet prepared in:

```text
docs/process/CARVER_S27_ZN_V2_DESIRED_POSITION_EXECUTABLE_EXTERNAL_AUDIT_HANDOFF_2026-06-09.md
```

The external audit reported:

```text
Verdict: PASS
P0 findings: None
P1 findings: None
P2 findings: None
```

The audit stated that the next gate may proceed only as the next separately authorized non-result gate. It explicitly did not authorize order/fill/cost/PnL/result/backtest/source-faithful evidence work.

## Key Confirmations

The external audit confirmed:

- `DesiredPositionExecutableBundle.validate()` binds to the active forecast executable bundle and does not accept caller-supplied forecast or desired-position rows as authority.
- Standalone desired-position row validation remains non-authoritative.
- The remediation manifest, cost parameter file, Appendix C/static spec file, and provider definition file are byte/hash locked rather than merely path locked.
- Attachment hashes matched the pinned constants:
  - remediation manifest `0b8ae370b8b6ee3a31976448cabc30fe6ae658eeef5123171bb67bf67805febc`;
  - cost parameter `e6b7c69a712fd7a5effbabbd4c809f24c1a6dfabbfb1ce317b387c923ac7f098`;
  - Appendix C/static spec `908d9c147babf839ff4475f4286bf9e7828921f274f2d1a4a7a4cb5c2b7ead1d`;
  - ZNM6 provider definition `cb1908e05cd41037a681a1a9aede56eb93001ad7c4576b048b15c87b0ec00742`.
- Desired-position arithmetic is enforced for:
  - capital/account value `500000.0 USD`;
  - annual target risk `0.20`;
  - instrument weight `1.0`;
  - IDM `1.0`;
  - USD/USD FX `1.0`;
  - forecast-to-position divisor `10.0`, locally bound pending source-formula audit;
  - ZN point value `1000.0 USD` from Appendix C/static authority;
  - nearest whole-contract `ROUND_HALF_AWAY_FROM_ZERO`;
  - first-row flat-zero initial/current position.
- `Carver.pdf` Appendix C was available to the auditor through the library for the narrow ZN point-value check and confirmed the packet's authority separation.
- Databento provider definition `contract_multiplier = 2147483647` is explicitly rejected as ZN point-value authority.
- Appendix C/static evidence remains point-value authority; provider definition evidence remains selected-contract identity/effective-date evidence only.
- Self-consistent forged rows, hashes, policy rewrites, forecast bundles, provider multiplier forgeries, and downstream flags are rejected by active rebuild/equality checks and focused tests.
- The implementation emits desired-position metadata only and has no order/fill/cost/PnL/result/backtest/source-faithful evidence surface.

## P3 Notes

The external audit recorded two non-blocking P3 notes:

1. The auditor did not rerun the full pytest suite from the flattened packet, but did run `py_compile` on the attached Python files. The packet's local audit record already reports `28 passed` for desired-position tests and `79 passed` for the focused combined suite.
2. The private `_validate_structural_formula()` helper remains non-authoritative. This is acceptable because the authoritative accept path remains `DesiredPositionExecutableBundle.validate()`.

## Boundary

This record is not a backtest, not PnL, not result interpretation, not promotion evidence, and not a source-faithful evidence claim.

No order/fill/cost/PnL/result/backtest-readiness gate may proceed without separate operator authorization.

