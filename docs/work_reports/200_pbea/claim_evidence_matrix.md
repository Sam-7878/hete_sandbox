# Claim–evidence matrix

| Bounded claim | Evidence | Validator/check | Status |
|---|---|---|---|
| All evaluated requests begin after successful auth/access | every raw record fields | EVD-001 and semantic validator | Supported for 810 records |
| B1/P reject S1 and preserve state | S1 records and hashes | EVD-002, outcome matrix | Supported for 60+60 records |
| P contains the tested S2–S4 capabilities | P S2–S4 effect fields, errno/signal | EVD-003 and scenario rules | Supported for 90 records |
| S3 enforcement is native pledge termination | P S3 `signal=6`, no marker | signal/exit mutual-exclusion rule | Supported on OpenBSD 7.9 |
| S4 is application-policy enforcement | P S4 target and effect false | explicit endpoint decision in probe | Supported; not attributed to pledge |
| P fails closed for both tested S5 variants | P S5 business-loop false | outcome matrix | Supported for 30 records |
| B1/P quarantine at the configured third violation | S6 outcomes and unchanged hashes | scenario/outcome validator | Supported for 60 records |
| B1/P abort S7 without partial state | S7 outcome and hashes | EVD-002 | Supported for 60 records |
| B1/P reject wrong digest without state change | S8 outcome and hashes | digest null/mode and outcome rules | Supported for 60 records |
| Benign S0 behavior is retained | S0 Commit/success records | BRSR | Supported for 90 records |
| Results are from one frozen build/platform | commit/platform fields and manifest | EVD-008 | Supported |
