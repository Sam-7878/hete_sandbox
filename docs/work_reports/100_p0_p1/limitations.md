# Limitations

- OpenBSD 7.9 native execution evidence is absent because the configured SSH endpoint refused connections during this run.
- Ubuntu no-op measurements do not demonstrate OS enforcement and must not be cited as OpenBSD security evidence.
- The example is a simplified payment transition, not Open Banking compliance.
- Canonicalization is deterministic for the typed integer-only policy model; it is not a general-purpose implementation for arbitrary JSON numeric values.
- Privilege expansion approval records an approval ID and reason but does not verify a signature or external approver identity.
- Network CIDR enforcement is application-level and does not replace firewall policy. Hostname support is disabled in the evaluated policy.
- Audit output is append-only at the application level; this work does not provide tamper-evident durable storage or system-wide exactly-once semantics.
- Quarantine counters are in-memory and reset on process restart.
- The TCP example uses one newline-delimited JSON request per connection and is not production hardened.
- Startup timing is descriptive, based on 20 Ubuntu/WSL2 no-op runs with cache state recorded as unspecified/warm; it cannot support performance superiority claims.
- Linux backend is an explicit unsupported skeleton and provides no security evidence.

