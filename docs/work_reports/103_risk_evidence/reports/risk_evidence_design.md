# RiskEvidence Extension Design

Date: 2026-07-21  
Status: implementation baseline

## Design goal

RiskEvidence is an optional Quarantine policy extension. It does not become a required POA element and it does not introduce domain concepts into the kernel. Existing specifications, `AacoHooks`, `execute_transition`, four outcome labels, and direct Quarantine remain valid.

## Core model

`BasisPoints(u16)` accepts exactly `0..=10_000`. `RiskCategory` and `EvidenceSource` are closed, snake-case enums. The initial category vocabulary is replay attack, geofence violation, authentication failure, policy escalation, fraud signal, and anomaly signal. Sources are replay window, geofence engine, authentication verifier, policy validator, pattern detector, and external oracle.

`CorrelationId` is a non-empty, trimmed, control-character-free UTF-8 string of at most 128 bytes. `RiskEvidence` contains category, severity basis points, confidence basis points, occurrences (`>= 1`), source, observation timestamp in Unix milliseconds, and correlation ID. JSON decoding rejects unknown fields and invalid values.

`QuarantinePolicy` contains `enabled`, minimum occurrences, minimum severity, minimum confidence, and `EvidenceAggregation::{AllThresholds, AnyThreshold}`. Construction and deserialization validate every bound. No floating-point operations or clocks occur in evaluation.

## Pure evaluation

The evaluator compares the three policy thresholds in a fixed order: occurrences, severity, confidence. It returns:

- `ExtensionDisabled` when disabled;
- `Insufficient { failed_thresholds }` when the selected mode is not satisfied;
- `Quarantine { score_bps, matched_thresholds }` when satisfied.

For `AllThresholds`, all three comparisons must pass. For `AnyThreshold`, one or more must pass. `score_bps` is the conservative minimum of severity and confidence; occurrences is a discrete gate and is reported separately in the match list. `observed_at_ms`, category, source, and correlation ID do not affect the decision.

## Failure routing

The common classifier implements this table:

| Failure class | Extension/decision | Terminal outcome |
|---|---|---|
| Policy | any | Reject |
| Internal | any | Abort |
| Risk | absent or disabled | Reject |
| Risk | insufficient | Reject |
| Risk | sufficient | Quarantine |

Every Risk classification returns a `RiskAssessment` containing the evidence, decision, and stable reason code. This lets callers bind outcome and evidence without changing the shape of the legacy `TransitionOutcome` variants.

## Additive kernel API

The risk-aware hook is additive and exposes `authorize`, `validate`, `mutate_candidate`, `reconcile(&Candidate)`, `commit(Candidate)`, and `state`. Each stage returns the same `TransitionFailure` type. The executor preserves AACO ordering and calls commit only after successful reconciliation. It returns `TransitionResult { outcome, risk_assessment }`.

The legacy hook/executor remains unchanged. Existing direct `TransitionOutcome::Quarantine(RepeatedPolicyViolation)` remains a valid application decision and has no fabricated RiskEvidence.

## Audit contract

`AuditRecord` gains an optional `risk_evidence` object. It contains the full typed evidence, evaluator decision, and stable reason code. The existing `policy_digest` remains the policy identity. The audit extension contains no request payload or candidate/domain state. Old records deserialize with the optional field absent; unknown fields still fail closed.

## Protocol contract and digest

Top-level `risk_evidence` is optional. When present, all five fields are required and unknown fields are rejected:

```json
{
  "enabled": true,
  "minimum_occurrences": 3,
  "minimum_severity_bps": 8000,
  "minimum_confidence_bps": 8000,
  "aggregation": "all_thresholds"
}
```

The protocol crate uses an equivalent validated configuration type rather than depending on `poa-core`. The application performs an explicit fallible conversion. An absent field is omitted from serialization, preserving the existing canonical bytes and golden digest. A present policy is serialized into the canonical effective policy and therefore changes the digest. Runtime evidence is not part of policy serialization.

On inheritance, omission inherits the parent. Tightening means enabling a disabled policy, raising one or more minimums, or changing `any_threshold` to `all_thresholds`; it is allowed. Disabling an enabled parent, lowering a minimum, or changing `all_thresholds` to `any_thresholds` is privilege expansion and requires the repository's existing explicit approval metadata.

## Validation and verification

Unit and deterministic generated-case tests cover value bounds, closed enum round trips, All/Any boundary tables, disabled routing, every kernel stage, state non-commit, audit round trips and minimization, and evaluator determinism/monotonicity. Existing suites protect Commit, Reject, Abort, direct Quarantine, inheritance, schema strictness, golden digest, and platform behavior.

Release benchmarks will measure disabled, insufficient, and Quarantine evaluator paths using warmup plus at least 30 independent samples. A fixed labeled synthetic corpus and complete threshold grid will report quarantine/false-quarantine/missed-containment counts and precision/recall/F1. These measurements characterize only this implementation and corpus; they do not establish real-world detection performance or whole-system constant-time behavior.
