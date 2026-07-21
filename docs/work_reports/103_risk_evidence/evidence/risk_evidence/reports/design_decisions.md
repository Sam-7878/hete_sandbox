# Design Decisions

## Clean redesign

The legacy HETE code was used only to identify the occurrence/confidence routing concept and its limitations. It was not copied because its string categories, missing severity/source/time/correlation provenance, and application-local shape conflict with the sandbox's type and crate boundaries.

## Strong closed vocabulary

Severity was added separately from confidence: impact magnitude and belief in the evidence are different inputs. Source and correlation ID make provenance and cross-record tracing explicit. V1 uses closed enums instead of `Other(String)` so unknown semantics fail closed; vocabulary growth requires a reviewed protocol/code revision.

## Deterministic evaluator

Basis points avoid floating-point ambiguity. `observed_at_ms` is retained for audit but excluded from the evaluator because wall-clock comparison would introduce clock/trust dependencies and a time-window aggregation design not present in this scope. An explainable `EvidenceDecision` replaces a Boolean so failed/matched thresholds are testable and auditable.

## Compatibility and linkage

The public legacy outcome shape was not changed. `TransitionResult` links the outcome to optional `RiskAssessment`. Threshold Quarantine has evidence; existing direct Quarantine remains evidence-free and retains `RepeatedPolicyViolation`.

## Crate boundary

Core owns domain-neutral evidence and evaluation. Protocol owns an equivalent wire policy and remains independent of core. The example application performs a fallible explicit conversion. This prevents cyclic dependency and avoids putting banking, drone, voting, or AI-agent types into core.

## Digest and inheritance

Configured thresholds change execution routing, so all five protocol fields are digest-bound. Runtime observations are excluded. An absent optional field is omitted, retaining the legacy canonical bytes. Child omission inherits; disabling or lowering protection is an audited privilege expansion.

## AnyThreshold

AnyThreshold is exposed for explicit policies and tests but can Quarantine on a single signal, increasing false quarantines. AllThresholds is the conservative documented baseline. Neither is silently selected when the extension is absent.
