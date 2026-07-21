# RiskEvidence Implementation Report

Source commit: `c2128a9603d2a14d4927bfe72e5e1caf1306c829`

## Result

HETE Sandbox now implements RiskEvidence as an additive, optional, domain-independent Quarantine policy extension. The legacy AACO trait and executor remain unchanged. A new risk-aware hook routes Policy, Risk, and Internal failures through one classifier at authorization, validation, candidate mutation, reconciliation, and commit.

The core model supplies bounded `BasisPoints`, validated `CorrelationId`, closed category/source enums, structured evidence, validated Quarantine policy, explicit All/Any threshold modes, explainable decisions, failure classification, and outcome-linked assessment metadata. Candidate reconciliation is separated from commit in the optional path; all pre-commit failures drop the candidate.

Protocol integration adds a strict optional `risk_evidence` object. It is included in canonical policy bytes and digest when present. Its absence preserves the existing golden digest. Omitted child policy inherits the parent; weakening uses the existing approved privilege-expansion mechanism.

Audit records carry an optional structured assessment with evidence, reason code, decision, matches/failures, and the existing policy digest. Payload/candidate/domain state are not added.

## Verification

- Ubuntu 24.04: fmt passed, clippy with `-D warnings` passed, all 60 workspace tests passed.
- OpenBSD 7.9: all 60 workspace tests passed; the packaged Rust toolchain did not include cargo-fmt or cargo-clippy.
- The legacy Commit, Reject, Abort, repeated direct Quarantine, schema, inheritance, OpenBSD backend, and golden digest tests remained green.
- New core tests cover RE-MOD, RE-EVAL, RE-DIS, RE-KER, RE-STATE, RE-AUD, and RE-PROP cases.

## Benchmark summary

On the recorded Ubuntu/WSL2 environment, median per-evaluation release times were 1.868 ns disabled, 18.389 ns insufficient, and 18.822 ns Quarantine. These are microbenchmark results from 30 independent samples with 100,000 inner evaluations and 20,000 warmups; they are not end-to-end transition latency.

The 64-configuration synthetic sensitivity grid shows threshold-dependent precision/recall. The highest supplied-corpus F1 was 0.9333 at multiple configurations, including occurrences=1, severity=7000, confidence=8000. This does not establish an optimal production threshold or real-world detection accuracy.
