# RiskEvidence Pre-implementation Analysis

Date: 2026-07-21  
Scope: `hete_sandbox` optional RiskEvidence-based Quarantine extension

## Repository findings

The current kernel is intentionally small and domain-blind. `poa-core` owns the generic transition descriptor, AACO hook trait, four terminal outcomes, and the audit record. `poa-protocol` owns the strict JSON model, schema validation, inheritance, canonicalization, and SHA-256 policy digest. `poa-verifier-example` is the composition boundary that converts a protocol policy into executable verifier behavior. `poa-sandbox` contains platform confinement only.

The existing public `AacoHooks` API uses stage-specific errors: authorization and validation return `RejectReason`, while mutation and reconciliation return `AbortReason`. `execute_transition` therefore cannot represent a Risk failure at every stage. Changing those signatures would break existing consumers. The current example's direct Quarantine is an application-level repeated-policy-violation counter, not typed RiskEvidence.

`AuditRecord` identifies the transition, effective policy digest, actor, operation, outcome, timestamp, and optional payload hash. It does not retain structured failure evidence or the evaluator decision. The protocol schema is fail-closed (`additionalProperties: false`), and `ProtocolSpec` uses `deny_unknown_fields`. The canonicalizer serializes the effective policy, removes only approval metadata, and sorts object keys plus known set-like arrays. Consequently, an absent optional field can preserve the existing golden digest, while a present RiskEvidence policy can be digest-bound without changing the digest algorithm.

## Boundary and dependency decision

RiskEvidence belongs in `poa-core`: it is a domain-neutral outcome-routing input and must be usable by any verifier. Protocol configuration belongs in `poa-protocol`, which must remain independent of `poa-core`. The application boundary will explicitly convert the validated protocol structure to the core `QuarantinePolicy`; this avoids a reverse or cyclic crate dependency.

The existing `AacoHooks` and `execute_transition` interfaces will remain intact. A separate optional risk-aware hook and executor will classify `Policy`, `Risk`, and `Internal` failures through one common function. This preserves existing source behavior and direct Quarantine semantics while supporting Risk at authorize, validate, mutate-candidate, reconcile, and commit boundaries.

## State-integrity finding

The legacy hook passes an owned candidate into `reconcile`, so an implementation may commit inside reconciliation. A risk-aware executor cannot guarantee non-commit if it reuses that contract. Its optional hook must therefore separate candidate reconciliation from commit: authorization, validation, mutation, reconciliation, then commit. Candidate data remains local until the final step. A failure at or before reconciliation drops the candidate and leaves committed state unchanged. A commit-stage internal failure maps to Abort; a commit-stage Risk failure is supported but implementers must make commit atomic because the core cannot roll back external side effects.

## Protocol inheritance finding

Existing inheritance performs field-specific restrictive merging and otherwise takes the child specification. The optional RiskEvidence policy needs an explicit rule. To avoid silently disabling a parent control, an omitted child field inherits the parent value. A child may tighten an enabled parent without approval; disabling it or weakening thresholds requires the existing explicit privilege-expansion approval. This rule applies only when the extension is present and does not alter legacy specifications.

## Old implementation assessment

The reference HETE implementation supplies the useful high-level idea—occurrence and confidence thresholds route Risk to Reject or Quarantine—but its free-form category and missing severity, source, timestamp, and correlation provenance do not meet this repository's fail-closed type and audit requirements. No source will be copied. The new representation uses bounded basis points, closed category/source enums, validated correlation IDs, explicit threshold mode, and a pure evaluator.

## Risks and controls

- Numeric ambiguity: basis points are integer-only in `0..=10_000`; floating point is excluded.
- Unknown semantic labels: category and source are closed enums in v1; unknown values fail deserialization.
- Clock nondeterminism: `observed_at_ms` is audit provenance only and never enters evaluation.
- Policy identity drift: threshold fields are in the effective policy and therefore its digest; runtime evidence is never part of that digest.
- State leakage: only a successfully reconciled candidate reaches commit.
- Audit overcollection: structured RiskEvidence is retained, but domain payload and candidate state are not.
- Disabled extension: Risk fails closed to Reject and still emits a minimal structured assessment.

## Planned touch points

- `crates/poa-core/src/risk.rs`: strong types, policy, evaluator, classification metadata.
- `crates/poa-core/src/kernel.rs`: additive risk-aware hook and executor.
- `crates/poa-core/src/outcome.rs`: additive typed risk outcome reasons.
- `crates/poa-core/src/audit.rs`: optional structured risk audit extension.
- `crates/poa-protocol/src/model.rs`, validator, inheritance, and schema: optional policy configuration.
- `crates/poa-verifier-example`: conversion/composition helper and benchmark harness.
- `spec/poa-risk-evidence.md`: normative extension contract.
- Tests and SCI evidence under this work-report directory.

No production source was changed before this analysis was recorded.
