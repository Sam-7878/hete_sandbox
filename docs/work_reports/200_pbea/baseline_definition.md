# Comparative baseline definition

All three modes use source commit `1bcfa8b`, the same `adversarial_probe` binary, release profile, OpenBSD 7.9 VM, policy/request fixtures, actor, operation, iteration schedule, hardware allocation, and loopback topology. A closed `VerifierMode` selects only the control boundary; there are no separately weakened toy programs.

| Mode | Included controls | Deliberately absent controls |
|---|---|---|
| Access-only (B0) | successful identity/access precondition, strict Rust request decoding, direct business mutation | candidate/invariant guard, four-outcome transition semantics, digest binding, quarantine, application endpoint policy, pledge/unveil |
| Transition-only (B1) | B0 admission plus AACO candidate/invariant/reconcile, Commit/Reject/Quarantine/Abort, digest binding | runtime filesystem/process restriction and application endpoint enforcement |
| Full-PBEA (P) | B1 plus strict production policy validation, required-resource preparation, application endpoint allowlist, native OpenBSD unveil/pledge, fail-closed startup | none of the evaluated PBEA controls |

B0 outcome label `success` is a comparative harness label, not a claim that B0 implements PBEA four-outcome semantics. B1 parses and validates policy but does not claim native runtime enforcement. P rejects production `noop`, non-OpenBSD runtime selection, missing resources, and an unlocked unveil table.
