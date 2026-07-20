# Paper-Ready Results

## OpenBSD startup measurement

| Environment | Runs | Success | P50 (µs) | P95 (µs) | Max (µs) | Policy digests |
|---|---:|---:|---:|---:|---:|---:|
| OpenBSD 7.9 Hyper-V, release, warm-unspecified | 30 | 30 | 48947 | 50771 | 50775 | 1 |

Permitted sentence:

> The one-time startup cost of loading, validating, resolving, canonicalizing, and applying the evaluated POA process policy was descriptively measured over 30 successful OpenBSD 7.9 release runs (P50 48947 µs, P95 50771 µs, maximum 50775 µs).

## Enforcement and fail-closed observations

| Case | Observation | Result |
|---|---|---|
| Empty unveil policy | `/etc/passwd` ENOENT(2), formerly known path ENOENT(2), post-lock addition EPERM(1) | deny-all verified |
| Malformed policy | exit 1, listener closed, business loop false | fail-closed |
| Missing resource | exit 1, listener closed, business loop false | fail-closed |
| Baseline OpenBSD evidence | 13 records, all passed | policy-bound evidence |

All startup runs used source commit `ed9b6c2be2349bf328ca3f67a16e1b5dc392fb62` and policy digest `sha256:3f3fbd07bb40da498804282a09ddbb2354050bd3a14bd9c5c845dd16bfd8404a`. Ubuntu baseline contains 8 records and is not combined with OpenBSD performance values.
