# Claim–Evidence Matrix

| Claim | Source | Test / evidence | Status |
|---|---|---|---|
| Invalid specification prevents startup before listener | `poa-protocol/validator.rs`, verifier `main.rs` | SPEC-002..008, E2E-007, exit 1 + listener closed | Verified on Ubuntu and OpenBSD |
| Missing required unveil resource prevents listener startup | `poa-sandbox/openbsd.rs`, verifier `main.rs` | SBOX-003, exit 1 + listener closed | Verified on OpenBSD |
| Inheritance is deterministic and rejects weakening/cycles | `inheritance.rs` | INH-001/003/004/006/007/009, approved expansion test | Verified |
| Transition binds to deterministic policy digest | `canonical.rs`, `digest.rs`, `audit.rs` | DIG-001..006, golden snapshot, combined 13 records/1 digest | Verified |
| AACO reports four distinct outcomes | `poa-core/kernel.rs`, verifier | OUT-001..005, cross-host E2E-001..004 | Verified on Ubuntu and OpenBSD network path |
| Non-commit does not propagate domain state | verifier outcome tests and audit | OUT-002/004/005, E2E-002/003/004 | Verified |
| Generic core does not depend on example/domain crates | Cargo workspace graph | ARCH-001 dependency graph | Verified |
| Production no-op is rejected | validator/no-op backend | SPEC-008, backend test | Verified |
| OpenBSD applies unveil lock and pledge after listener setup | `poa-sandbox/openbsd.rs` | native tests, BUSINESS_LOOP marker, SBOX-006/008 | Verified on OpenBSD |
| Empty unveil policy does not leave filesystem unrestricted | `mapper.rs`, OpenBSD backend | `empty_unveil_policy_masks_root_before_lock` | Mapper/native build verified; empty-policy runtime probe not separately measured |
| Allowed path remains usable | `sandbox_probe allowed-path` | SBOX-004 | Verified on OpenBSD |
| Policy-external filesystem path is denied | `sandbox_probe denied-path` | SBOX-005, E2E-005, ENOENT(2) | Verified on OpenBSD |
| Prohibited exec terminates under pledge | `sandbox_probe prohibited-exec` | SBOX-006, E2E-006, SIGABRT(6) | Verified on OpenBSD |
| Policy modification after lock is denied | `sandbox_probe post-lock-unveil` | SBOX-008, EPERM(1) | Verified on OpenBSD |
| Network policy restricts address/port/protocol | verifier allowlist | unit test, malformed CIDR test | Verified in application logic |
| Startup overhead is characterized descriptively | startup example | 20 Ubuntu raw records | Verified for Ubuntu no-op only |
