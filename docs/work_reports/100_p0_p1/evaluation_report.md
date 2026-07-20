# Evaluation Report

## Ubuntu 24.04 development evaluation

수치는 `raw/ubuntu-e2e.jsonl`에서 `evaluation/generate_report.py`로 생성했다.

- Rust tests: 33 passed, 0 failed
- Application E2E: 6 passed, 0 failed, 2 not evaluated
- Observed application outcomes: Commit 1, Reject 2, Quarantine 1, Abort 1
- Fail-closed malformed specification: 1 passed, listener not opened
- Policy digest stability: 8 records, 1 digest
- OpenBSD kernel enforcement evidence: 0 records

상세 outcome confusion table은 `generated/evaluation_report_ubuntu.md`, LaTeX fragment는 `generated/evaluation_table_ubuntu.tex`가 authoritative generated artifact이다.

## Startup overhead

Ubuntu no-op development backend에서 20회 측정했다. 이 값은 OpenBSD enforcement cost가 아니며 성능 우월성 주장에 사용할 수 없다. P50/P95/max는 `generated/startup_overhead_ubuntu.md`에서 raw timing으로 자동 생성된다.

## OpenBSD evaluation

미실행. 설정된 SSH endpoint가 connection refused를 반환했고, 현재 Codex 실행 계정에는 Hyper-V VM 상태 조회 권한이 없었다. 이 실패를 pass 또는 예상 결과로 변환하지 않았다.

