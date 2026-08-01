# Comparative overhead report

The measurements below are wall-clock durations of complete scenario probes on the same OpenBSD 7.9 VM. They are a **mixed-scenario evaluation cost**, not a production request benchmark.

| Mode | n | Min µs | P50 µs | P95 µs | Max µs | Mean µs | Population σ µs |
|---|---:|---:|---:|---:|---:|---:|---:|
| B0 | 270 | 9,436 | 10,195 | 24,207 | 97,958 | 11,992.12 | 7,231.59 |
| B1 | 270 | 9,304 | 10,415 | 15,596 | 24,569 | 11,068.26 | 2,016.05 |
| P | 270 | 9,536 | 10,549 | 187,731 | 402,531 | 32,904.17 | 67,488.68 |

Full-PBEA's median is 3.47% above B0's median. Its mean and P95 are dominated by S3, where an isolated process is spawned, sandboxed, deliberately terminated by pledge, and reaped so a signal can be recorded. No throughput, steady-state service latency, or cross-machine performance claim is made from these values.
