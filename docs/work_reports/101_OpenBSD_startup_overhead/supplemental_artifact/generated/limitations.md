# Limitations

- Startup overhead was measured only on one OpenBSD 7.9 Hyper-V VM and is not generalized to other hardware or deployment environments.
- The 30-run cohort used `warm_unspecified`; filesystem and CPU cache state was not forcibly flushed or controlled.
- This is descriptive one-time startup cost, not an OS comparison, production workload benchmark, or performance-superiority result.
- The example does not provide production Open Banking or DID compliance.
- Audit files are application append-only, not tamper-evident durable storage or system-wide exactly-once semantics.
- Quarantine counters remain in memory and reset on process restart.
- Network CIDR enforcement is application-level and does not replace firewall policy.
- The newline-delimited TCP example is not production hardened.
- No complete malware or supply-chain attack experiment was performed.
- The Linux backend remains unsupported and provides no security evidence.
