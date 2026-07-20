# POA Process-Trust Supplemental Artifact

This package supports traceability and regeneration of the evaluated POA specification, AACO outcomes, OpenBSD process enforcement, and startup measurements.

Evaluated source commit: `ed9b6c2be2349bf328ca3f67a16e1b5dc392fb62`.
Historical P0/P1 baseline raw retains its original evidence commit(s): `d6210e48312f14b2ed19104a02c66e481bdb6a01`. Each raw record is authoritative for its own provenance.

## Prerequisites and topology

- Ubuntu 24.04 with Python 3.12 and Rust/Cargo for validation/report generation.
- OpenBSD 7.9 with Rust/Cargo for native release measurement.
- Ubuntu client and OpenBSD verifier on a reachable private test network.
- SSH port (for example 22) is distinct from verifier TCP port 7878.

## Expected observations

- 30 valid startup runs: exit 0 and one stable policy digest.
- Empty-unveil: exit 0 with ENOENT/ENOENT/EPERM, representing deny-all semantics.
- Invalid policy and missing resource: exit 1, listener closed, no business-loop marker.
- Prohibited exec baseline: exit 134 / SIGABRT is the expected pledge termination.

## Authoritative data

Files under `raw/` are authoritative. Markdown and LaTeX under `generated/` are derived outputs. `FILE_SHA256SUMS.json` binds every packaged file.

## Reproduction

Run `scripts/run_openbsd_complementary.sh` on OpenBSD, copy its output to Ubuntu, then run `openbsd_startup_evidence.py`, `collect_complementary_evidence.py`, and `generate_complementary_reports.py`. Use placeholder host/path values appropriate for the test environment; no credentials are included.

## Known limitations

One OpenBSD VM, warm-unspecified cache state, no OS comparison, no production workload, in-memory quarantine, application-level network allowlist, and no complete malware or supply-chain experiment.
