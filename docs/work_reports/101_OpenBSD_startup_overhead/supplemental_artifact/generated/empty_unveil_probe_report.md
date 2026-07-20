# Empty-Unveil Native Probe

> Generated from `raw/empty-unveil-openbsd.jsonl` and the preserved native logs.

- Selected semantics: **deny-all**
- Status: **passed**
- Exit code: 0
- Observation: `EMPTY_UNVEIL_DENY_ALL external_errno=Some(2) formerly_known_errno=Some(2) post_lock_errno=Some(1)`
- Listener opened: false (standalone native sandbox probe)
- Business loop entered: false (standalone native sandbox probe)

The implementation maps an empty `unveil_paths` list to `unveil("/", "")` before `unveil(NULL, NULL)`. Both `/etc/passwd` and a formerly known audit path remained inaccessible, and a post-lock path addition returned EPERM(1).
