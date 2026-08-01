# Scenario manifest

The authoritative machine-readable manifest is `evaluation/comparative/scenarios.yaml`. Each mode/scenario cell has 30 iterations, giving 810 records.

| ID | Controlled action | B0 expected | B1 expected | P expected | Principal evidence |
|---|---|---|---|---|---|
| S0 | benign transition | success | Commit | Commit | changed state hash |
| S1 | amount=0 invariant violation | success, invalid state admitted | Reject | Reject | unchanged hash for B1/P |
| S2 | read `/tmp/pbea-eval/outside/secret.txt` | success | success | Reject | P `errno=2`, effect false |
| S3 | execute marker helper | success | success | terminated | P signal 6, marker absent |
| S4 | connect to controlled `127.0.0.1:8989` sink | success | success | Reject | P application-policy pre-connect block |
| S5 | odd: malformed JSON; even: missing unveil resource | success | odd fail/even success | startup failure | business loop false on failure |
| S6 | three valid-actor wrong-digest requests | success | Quarantine | Quarantine | threshold reached, state unchanged |
| S7 | fault after candidate and before commit | natural direct success | Abort | Abort | unchanged hash for B1/P |
| S8 | wrong policy digest | success | Reject | Reject | state unchanged for B1/P |

S4 is attributed to the application network policy, not to pledge. S3 runs Full-PBEA in an isolated child so the parent can record the OS termination signal without fabricating a result.
