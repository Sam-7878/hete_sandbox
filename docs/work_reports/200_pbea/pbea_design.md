# PBEA Comparative Harness Design

Date: 2026-08-02

## Shared execution path

`ComparativeHarness` owns the selected `VerifierMode`, one validated effective policy, and one domain/trust state. Every scenario first constructs the same `TransitionRequest`, validates the actor identity, and verifies the operation allowlist. Only after access authorization succeeds does the mode select enabled mechanisms.

`VerifierMode` is a closed enum serialized as `access-only`, `transition-only`, or `full-pbea`. Its capability profile is explicit and testable. Full-PBEA runtime activation is fail-closed and never falls back to transition-only or access-only.

## State behavior

B0 invokes the direct business handler after common admission. It does not deliberately manufacture partial effects: an injected failure after candidate preparation occurs before state installation and therefore naturally leaves state unchanged. B1/P call the existing verifier transition route. P additionally applies OpenBSD runtime constraints once all fixture resources, policy, request, provenance, and output data needed before locking are prepared.

## Scenario decisions

| Scenario | B0 | B1 | P |
|---|---|---|---|
| S0 benign | success | commit | commit |
| S1 invalid state | success/effect | reject/no state change | reject/no state change |
| S2 external read | success/effect | commit/effect | reject/denied |
| S3 child exec | success/effect | commit/effect | terminated/no marker |
| S4 disallowed egress | success/effect | commit/effect | reject/no sink data |
| S5 invalid policy | startup succeeds | malformed rejected; missing runtime resource not required | both subcases fail closed |
| S6 repeated violation | rejects without quarantine | quarantine at threshold | quarantine at threshold |
| S7 post-candidate failure | abort/no installed state | abort/no installed state | abort/no installed state |
| S8 wrong digest | success/digest ignored | reject | reject |

The B0 labels `success`, `reject`, and `abort` are comparative normalization labels, not a claim that B0 natively implements the four PBEA outcomes.

## Runtime probes

The evaluation policy unveils only controlled fixture directories needed by the probe and omits process-execution promises. The external secret is synthetic and outside the unveil set. Network traffic is loopback-only. Full-PBEA S4 is blocked by the application endpoint allowlist, not attributed to `pledge`.

## Evidence validation

`validate_records.py` rejects unknown fields, invalid enums, unauthenticated/unauthorized rows, duplicate IDs, missing iterations, mode-inappropriate digests, state hash mismatches, negative duration, inconsistent exit/signal fields, and scenario-specific effect inconsistencies. It also requires exactly 30 unique iterations for every mode/scenario in final mode.

## Metrics

`compute_security_metrics.py` calculates MESR, BRSR, SIVR, CER, FCR, and OCA by mode. Wilson intervals use z=1.959963984540054 and the standard score interval. Latency summaries use count, min, P50, P95, max, arithmetic mean, and population standard deviation. Tables and paper sentences consume only validated generated metrics.
