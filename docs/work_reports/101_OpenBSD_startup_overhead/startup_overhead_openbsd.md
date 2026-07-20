# OpenBSD 7.9 Startup Overhead

> Generated exclusively from validated OpenBSD native raw JSONL.

- Runs: 30 successful, 0 failed
- Build profile: `release`
- Cache condition: `warm_unspecified`
- Source commit: `ed9b6c2be2349bf328ca3f67a16e1b5dc392fb62`
- Distinct policy digests: 1 (`sha256:3f3fbd07bb40da498804282a09ddbb2354050bd3a14bd9c5c845dd16bfd8404a`)

| Stage | Min (µs) | P50 (µs) | P95 (µs) | Max (µs) | Mean (µs) | Stddev (µs) |
|---|---:|---:|---:|---:|---:|---:|
| t_load_us | 32 | 38 | 49 | 105 | 41.60 | 12.63 |
| t_schema_us | 46652 | 48730 | 50525 | 50565 | 48674.57 | 1236.72 |
| t_inheritance_us | 50 | 65 | 94 | 103 | 67.63 | 12.79 |
| t_canonicalize_us | 29 | 39 | 56 | 69 | 40.70 | 8.79 |
| t_digest_us | 5 | 5 | 7 | 14 | 5.80 | 1.62 |
| t_resource_prepare_us | 20 | 25 | 32 | 45 | 25.90 | 4.60 |
| t_listener_bind_us | 18 | 20 | 32 | 33 | 21.23 | 3.59 |
| t_unveil_apply_us | 19 | 21 | 29 | 33 | 21.80 | 2.95 |
| t_unveil_lock_us | 1 | 1 | 1 | 2 | 1.03 | 0.18 |
| t_pledge_apply_us | 5 | 6 | 10 | 10 | 6.17 | 1.24 |
| t_business_loop_ready_us | 2 | 3 | 3 | 4 | 2.67 | 0.54 |
| t_total_startup_us | 46861 | 48947 | 50771 | 50775 | 48914.43 | 1238.33 |

Stage timers use Rust's monotonic `Instant`. `t_total_startup_us` is measured independently; the small absolute difference from the stage sum is instrumentation/control-flow and per-stage rounding residual. Measured sub-microsecond stages are rounded upward to 1 µs; cache state was not forcibly flushed.
