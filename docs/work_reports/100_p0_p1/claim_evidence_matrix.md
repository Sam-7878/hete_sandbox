# Claim–Evidence Matrix

| Claim | Source | Test / evidence | Status |
|---|---|---|---|
| Invalid specification prevents startup before listener | `poa-protocol/validator.rs`, verifier `main.rs` | SPEC-002/003/004/005/006/007/008, E2E-007 raw | Verified on Ubuntu control flow |
| Inheritance is deterministic and rejects weakening/cycles | `inheritance.rs` | INH-001/003/004/006/007/009, approved expansion test | Verified |
| Transition binds to deterministic policy digest | `canonical.rs`, `digest.rs`, `audit.rs` | DIG-001..006, golden snapshot, OUT-001, 8 raw records/1 digest | Verified |
| AACO reports four distinct outcomes | `poa-core/kernel.rs`, verifier library | OUT-001..005 and E2E-001..004 | Verified on Ubuntu |
| Non-commit does not propagate domain state | verifier outcome tests | OUT-002/004/005 | Verified |
| Generic core does not depend on example/domain crates | Cargo workspace graph | ARCH-001 generated dependency graph | Verified |
| Production no-op is rejected | validator/no-op backend | SPEC-008, production-noop backend test | Verified |
| OpenBSD mapper applies unveil lock and pledge fail-closed | `poa-sandbox/openbsd.rs` | native runner/probe exists | Implemented, native evidence missing |
| Empty unveil policy does not leave filesystem unrestricted | `poa-sandbox/mapper.rs` | `empty_unveil_policy_masks_root_before_lock` | Mapper plan verified; native evidence missing |
| Denied filesystem access is enforced by OpenBSD kernel | `sandbox_probe denied-path` | E2E-005/SBOX-005 | Unverified |
| Prohibited exec terminates process under pledge | `sandbox_probe prohibited-exec` | E2E-006/SBOX-006 | Unverified |
| Application network policy restricts address/port/protocol | verifier allowlist | P1 network unit test, malformed CIDR test | Verified in application logic |
| Startup overhead is characterized descriptively | startup measurement example | 20 raw Ubuntu records and generated summary | Verified for Ubuntu no-op only |
