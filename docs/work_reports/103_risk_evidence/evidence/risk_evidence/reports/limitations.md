# Limitations

- The evaluator processes one already-aggregated evidence record. Time-window aggregation is not implemented.
- Evidence authenticity, signatures, attestation, and anti-tamper storage are not verified by this extension.
- `ExternalOracle` names provenance only; it does not establish oracle trustworthiness.
- No banking, drone, voting, or AI-agent detector is implemented here. Applications must create typed evidence at their own boundary.
- The 16 labels are synthetic and deliberately small. They do not represent production attacks, prevalence, costs, or domain distributions.
- Thresholds are not automatically calibrated or optimized, and the reported best synthetic F1 is not a production recommendation.
- Distributed deduplication, correlation consistency, and concurrent occurrence aggregation are outside scope.
- Pre-commit non-propagation is guaranteed by the optional hook contract. A commit implementation must itself be atomic; core cannot roll back external side effects after publication.
- Closed category/source enums trade runtime extensibility for fail-closed semantics. New meanings require a versioned code/schema change.
- Ubuntu nanosecond figures are a local microbenchmark and may be affected by compiler, CPU, WSL2 scheduling, and frequency behavior.
- OpenBSD cargo-fmt and cargo-clippy results are unverified because those components were not installed; tests did run successfully.
