# RiskEvidence Development Final Report

The optional RiskEvidence Quarantine extension is implemented at source commit `c2128a9603d2a14d4927bfe72e5e1caf1306c829`.

The implementation preserves the legacy public executor and direct Quarantine path, adds a typed pure evaluator and a non-committing risk-aware AACO path, binds optional threshold policy to the deterministic protocol digest, preserves the legacy absent-extension golden digest, and stores structured risk provenance in audit records.

Ubuntu 24.04 passed formatting, clippy with warnings denied, and all 60 workspace tests. OpenBSD 7.9 at the current address read from `security/open_bsd_connection.json` passed all 60 workspace tests. OpenBSD's packaged toolchain lacked cargo-fmt and cargo-clippy, which is explicitly recorded as not evaluated rather than passed.

Release B-RE1 results (30 samples, 100,000 inner iterations, 20,000 warmups) had median evaluator latency of 1.868 ns disabled, 18.389 ns insufficient, and 18.822 ns Quarantine on the recorded Ubuntu/WSL2 host. B-RE2 contains all 64 requested threshold combinations over a fixed 16-record synthetic corpus. These numbers are implementation-local and do not establish production detection accuracy.

Primary artifacts:

- `spec/poa-risk-evidence.md`
- `crates/poa-core/src/risk.rs`
- `crates/poa-core/tests/risk_evidence.rs`
- `docs/work_reports/103_risk_evidence/evidence/risk_evidence/`

See the nested `reports/`, `manifests/`, `raw/`, `processed/`, `matrices/`, and `snapshots/` directories for complete reproducibility and claim boundaries.
