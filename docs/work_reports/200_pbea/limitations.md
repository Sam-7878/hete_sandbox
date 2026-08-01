# Limitations

- One OpenBSD 7.9 VM and one hardware allocation were evaluated; external validity across kernels, hypervisors, and hardware is not established.
- Thirty repetitions quantify sampling uncertainty for these deterministic fixtures but do not represent a population of real attacks.
- Authentication and access control are trusted preconditions, not re-evaluated attack surfaces.
- S2–S4 use controlled file, helper, and loopback targets. They are mechanism tests, not malware benchmarks.
- Quarantine state is in-memory and process-lifetime scoped; distributed persistence and recovery are not claimed.
- S4 demonstrates the HETE application allowlist before connect. OpenBSD pledge allows `inet` and is not credited for endpoint filtering.
- Full-PBEA mixed latency includes per-probe startup and the S3 child lifecycle. It is unsuitable as steady-state service latency.
- The experiment does not establish universal immunity, complete mediation for arbitrary software, zero-day resistance, or protection against a compromised kernel/administrator.
