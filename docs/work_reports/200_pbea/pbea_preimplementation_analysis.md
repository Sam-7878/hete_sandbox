# PBEA Comparative Evaluation Pre-implementation Analysis

Date: 2026-08-02

## Repository baseline

The repository already contains the mechanisms evaluated as Policy-Bound Execution Architecture (PBEA): AACO transition execution, isolated candidates, invariant checks, Commit/Reject/Quarantine/Abort, strict protocol validation, deterministic effective-policy digests, application endpoint authorization, fail-closed startup, and OpenBSD `pledge`/`unveil`. The historical `poa-*` crate prefix is retained for artifact provenance; new evaluation-facing names use PBEA.

`poa-core` is protected by an architecture baseline hash and must not be changed. The appropriate additive boundary is `poa-verifier-example`, with experiment orchestration and statistics under `evaluation/comparative`. Existing OpenBSD probes demonstrate native denial behavior but do not provide the required same-request-path B0/B1/P comparison.

## Compatibility findings

The existing `Verifier` implements transition-only application semantics. Runtime OpenBSD enforcement is applied separately during startup. Comparative modes therefore need one wrapper that performs the same authentication/access admission before selecting one of three mechanism profiles:

- B0 Access-only: direct business handler after access admission; no candidate reconciliation, digest enforcement, endpoint policy, or OS runtime restriction.
- B1 Transition-only: existing verifier transition path and digest binding; no runtime backend or endpoint restriction.
- P Full-PBEA: the B1 transition path plus application endpoint policy and native OpenBSD runtime enforcement.

No mode may silently substitute another mode. Full-PBEA in production requires `os_backend=openbsd`; a no-op backend is an error.

## Scenario implementation findings

S0, S1, S6, S7, and S8 can reuse or minimally extend the existing verifier path. S7 requires moving the existing injected storage failure from candidate creation to reconciliation, after candidate creation but before state installation. This preserves its prior external outcome and strengthens alignment with the documented fault point.

S2–S4 require controlled resources only. The fixture root will contain an allowed input, a non-sensitive synthetic secret outside the unveiled paths, a compiled marker helper, marker/log directories, and a loopback sink. No host credential, host-sensitive file, malware, or external network target is used.

S3 Full-PBEA must survive long enough to emit evidence even though the constrained execution is expected to terminate. The parent probe therefore launches an isolated child copy; the child applies the same effective runtime policy and attempts the helper execution. The parent records the signal and marker state. Each matrix row remains independently process-isolated.

S5 alternates malformed-policy and missing-runtime-resource subcases. Access-only ignores runtime policy and starts. Transition-only rejects malformed policy but does not require the missing runtime resource. Full-PBEA rejects both, which makes the FCR denominator and subcase behavior explicit rather than hiding non-applicable controls.

## Evidence and statistical findings

The authoritative raw format is one JSON object per mode/scenario/iteration. All rows begin with authenticated=true and authorized=true. B0 has a null policy digest by definition; B1 and P require the same non-empty effective-policy digest. State-change booleans must equal hash inequality. Effect-success consistency is scenario-specific and checked automatically.

The final balanced matrix is 3 modes × 9 scenarios × 30 repetitions = 810 records with seed 20260802. Metrics are computed only from validated raw records. Each rate reports numerator, denominator, percentage, and Wilson 95% confidence interval. Undefined denominators remain null rather than being coerced to zero.

## Scope boundary

The experiment can support bounded claims about the enumerated controlled effects. It cannot establish universal malware prevention, insider-threat elimination, production attack probability, supply-chain immunity, or superiority to all ZTA/UCON implementations.

No production source was changed before this analysis was recorded.
