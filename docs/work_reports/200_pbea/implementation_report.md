# PBEA comparative security implementation report

## Outcome

The work order is **Completed** for the specified bounded comparative evaluation. The implementation source was frozen at commit `1bcfa8b`; the final native experiment produced 810/810 consistency-valid records on OpenBSD 7.9. Reporting-tool robustness fixes and result documents were added after the experiment without changing the probe or raw records.

## Implemented changes

- Added the closed `VerifierMode::{AccessOnly, TransitionOnly, FullPbea}` comparison boundary without changing `poa-core`.
- Retained historical `poa-*` crate names for compatibility while using PBEA terminology in all new research artifacts.
- Added strict policy/schema loading, mode-policy checks, state hashing, controlled adversarial scenarios S0–S8, isolated pledge-termination observation, and one-record-per-run JSON output.
- Moved the existing S7 injected error to reconciliation, after candidate creation and before state installation.
- Added controlled helper and loopback sink behavior; no external target or production data is touched.
- Added Ubuntu/POSIX OpenBSD matrix runners, strict evidence validator, Wilson 95% computation, metric aggregation, deterministic Markdown/LaTeX generation, and tests.
- Added a production OpenBSD evaluation policy and a dedicated evaluation request schema whose amount range permits the domain invariant test at value zero.

## Verification performed

| Check | Result |
|---|---|
| Ubuntu 24.04 `cargo test --workspace` | passed |
| Ubuntu `cargo clippy -p poa-verifier-example --all-targets -- -D warnings` | passed |
| Ubuntu `cargo fmt --all` / formatting check | passed |
| Architecture checks ARCH-001–ARCH-025 including frozen `poa-core` hash | passed |
| Python EVD-001–EVD-008 | 8 passed |
| B0/B1 S0–S8 pilot | 18/18 valid |
| OpenBSD Full-PBEA S0–S8 pilot | 9/9 valid |
| OpenBSD 7.9 `cargo test --workspace` from frozen source | passed |
| Final matrix | 810 records (270/mode), valid |

The mode tests cover the closed parser, capability boundaries, production/noop rejection, and the B1 runtime-claim boundary (MODE-001–005 intent). ADV-S0-001 through ADV-S8-001 are exercised both by pilots and by 30 final records per mode. S5 has alternating malformed-policy and missing-resource cases (ADV-S5-001/002). EVD tests cover schema shape, hashes, effect consistency, duplicates, mode/scenario combinations, Wilson golden values, deterministic LaTeX, and provenance.

## Completion classification

- **Completed:** mode architecture; S0–S8; 30 repetitions; 810 raw records; consistency validation; MESR/BRSR/SIVR/CER/FCR/OCA; Wilson intervals; latency distribution; LaTeX; claim/evidence and limitation documents; OpenBSD native enforcement evidence.
- **Partial:** none.
- **Not Completed:** none within the work-order scope.

Out-of-scope claims remain explicitly unverified rather than being treated as incomplete implementation work.
