# Carver Databento Appendix C Coverage Probe Provenance

Date: 2026-05-30

Status:

```text
DATABENTO_APPENDIX_C_METADATA_SYMBOLOGY_COVERAGE_PROBE_ONLY_NOT_DATA_INTAKE
```

Scope: Databento metadata and symbology only for the audited 102-row Appendix C universe. No OHLCV data request, market-row parsing, diagnostics, backtests, forecasts, positions, costs, carry, trend, risk, OOS, Lockbox, Forward, CFD adapter work, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git, or remote repository operations.

Probe window: `2026-05-27` through `2026-05-29`. The probe used Databento continuous symbology identifiers (`<candidate>.c.0`) solely as metadata coverage evidence. Continuous symbols are not authorized as source data or strategy input by this probe.

Datasets inventoried/probed:

```text
GLBX.MDP3, XEUR.EOBI, XCBF.PITCH, IFUS.IMPACT, IFEU.IMPACT, IFLL.IMPACT, NDEX.IMPACT, XEEE.EOBI
```

Coverage summary:

```text
{
  "DATABENTO_EXACT_METADATA_MATCH": 48,
  "DATABENTO_UNAVAILABLE_OR_UNRESOLVED_NO_METADATA_MATCH": 16,
  "DATABENTO_ALIAS_REQUIRED_METADATA_MATCH": 17,
  "DATABENTO_OTHER_DATASET_EXACT_METADATA_MATCH": 5,
  "DATABENTO_UNAVAILABLE_NO_RELEVANT_DATASET_IDENTIFIED_FROM_PUBLISHER_LIST": 16
}
```

NinjaTrader blocked or variant-mismatch rows with a Databento metadata candidate: `33`.

Alias caveat: `DATABENTO_ALIAS_REQUIRED_METADATA_MATCH` means a local candidate alias resolved in Databento symbology. It is not a production mapping lock and requires a separate source/provider mapping gate before any data intake.
