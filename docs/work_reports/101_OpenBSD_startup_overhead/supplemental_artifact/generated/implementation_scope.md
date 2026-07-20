# Implementation Scope

This complement adds OpenBSD startup timing instrumentation, a native empty-unveil deny-all probe, strict raw validation/statistics, and supplemental packaging. It does not add domain functionality.

Measured stages: load, schema validation, inheritance, canonicalization, digest, resource preparation, listener bind, unveil rules, unveil lock, pledge, business-loop readiness, and total startup.

`Instant` provides monotonic timing. Each stage is rounded upward to integer microseconds; unmeasured values use `null`, never zero. The independently measured total may differ slightly from the rounded stage sum.
