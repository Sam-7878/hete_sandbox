# Limitations

- Ubuntu no-op measurements do not demonstrate OS enforcement and must not be cited as OpenBSD security evidence.
- OpenBSD native/cross-host raw records do not contain measured duration; generated 0 µs values mean unmeasured, not zero-cost.
- OpenBSD startup overhead P50/P95/max was not measured.
- The example is a simplified payment transition, not Open Banking compliance.
- Canonicalization is deterministic for the typed integer-only policy model, not arbitrary JSON numeric values.
- Privilege expansion records an approval ID and reason but does not verify an external approver signature or identity.
- Network CIDR enforcement is application-level and does not replace firewall policy. Hostnames are disabled in the evaluated policy.
- Audit output is append-only at the application level; it is not tamper-evident durable storage or system-wide exactly-once semantics.
- Quarantine counters are in-memory and reset on restart.
- The newline-delimited TCP example is not production hardened.
- Linux backend is an explicit unsupported skeleton and provides no security evidence.
- One OpenBSD 7.9 VM and one Ubuntu 24.04 WSL2 client were evaluated; this does not establish portability or comparative superiority.
