# WP0 Baseline

- Source commit: `039e0aaee3be0bc5fe9d8ac1acd2b871005d8538`
- Repository state before implementation: clean
- Execution environment: Ubuntu 24.04.4 LTS on WSL2 (`Ubuntu` distribution)
- Rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`
- Python: project virtual environment Python 3.12.13
- Existing architecture: `poa-core`, `poa-protocol`, `poa-sandbox`, and `poa-verifier-example`

The work-order suggestion to create a branch and one commit per WP was not applied automatically because branch and commit history are user-owned repository operations. WP boundaries are instead preserved in the work reports and file layout.

The first concurrent WSL baseline test attempt encountered transient WSL service error `0x8007274c`; it was retained as an environment incident and followed by serialized Ubuntu 24.04 checks. Final verified results are recorded in `IMPLEMENTATION_REPORT.md`.
