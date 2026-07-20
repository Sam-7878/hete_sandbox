# Evaluation Report

## Ubuntu 24.04.4 development evaluation

- Rust tests: 35 passed, 0 failed
- Application evidence: 6 passed, 0 failed, OpenBSD 전용 2 not evaluated
- Outcomes: Commit 1, Reject 2, Quarantine 1, Abort 1
- Malformed specification: startup failure 1, listener not opened
- Policy digest: 8 records에서 1개
- Startup: 20회 no-op descriptive measurement

Ubuntu 수치의 authoritative artifact는 `raw/ubuntu-e2e.jsonl`, `raw/ubuntu-startup.jsonl`, `generated/evaluation_report_ubuntu.md`, `generated/startup_overhead_ubuntu.md`이다.

## OpenBSD 7.9 native 및 cross-host evaluation

Vaccine real-time monitoring 해제 후 pinned host key와 SSH port 22를 사용해 재시도했다. `verifier_port` 50051은 SSH port가 아니며, 실제 verifier example은 TCP 7878을 사용한다.

- OpenBSD native Rust tests: 35 passed, 0 failed
- Combined raw records: 13 passed, 0 failed, 0 not evaluated
- Cross-host application: E2E-001/002/003/004/008 passed
- Native kernel: SBOX-004/005/006/008 및 E2E-005/006 passed
- Fail-closed startup: E2E-007 malformed spec, SBOX-003 missing resource passed
- Startup failures: 2, 두 경우 모두 exit 1 및 listener closed
- OpenBSD denial/termination records: 5
- Policy digest: 13 records에서 1개

`prohibited-exec`의 exit 134와 `Abort trap (core dumped)`는 pledge 위반에 대한 기대 kernel termination이다. Denied path는 ENOENT(2), post-lock unveil은 EPERM(1)이 관측됐다.

OpenBSD raw에는 wall-clock duration을 계측하지 않아 생성 report의 duration은 0이다. 이는 성능 수치가 아니라 미계측 표시다.

Authoritative artifact는 `raw/openbsd-cross-host.jsonl`, `raw/openbsd-native.jsonl`, `generated/evaluation_report_openbsd_combined.md`이다.
