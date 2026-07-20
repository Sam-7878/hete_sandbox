# Final Claim–Evidence Matrix

| Claim | Source | Test / raw evidence | Status |
|---|---|---|---|
| OpenBSD startup overhead measured | `openbsd_startup_probe.rs` | START-001; 30 raw runs | Verified |
| Timing fields valid and total consistent | `openbsd_startup_evidence.py` | START-003/004 automated tests | Verified |
| Policy digest stable across startup runs | canonical policy/digest | START-002; 1 digest across 30 runs | Verified |
| Invalid policy keeps listener/business loop closed | verifier startup | START-005 | Verified on OpenBSD |
| Missing resource keeps listener/business loop closed | resource preparation | START-006 | Verified on OpenBSD |
| Empty unveil is deny-all, not unrestricted | `unveil_plan`, `sandbox_probe` | SBOX-EMPTY-001; ENOENT/ENOENT/EPERM | Verified on OpenBSD |
| AACO/cross-host baseline remains traceable | P0/P1 raw | 13 OpenBSD records | Verified baseline evidence |
| Supplemental package reproduces generated reports | generation/package scripts | raw validation + SHA-256 manifest | Verified |
