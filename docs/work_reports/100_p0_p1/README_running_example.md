# POA Process-Trust Running Example

## 현재 검증 상태

- Ubuntu 24.04.4 LTS: 전체 Rust 테스트, application E2E 6건, architecture check, raw-to-report pipeline 검증 완료
- OpenBSD 7.9: native runner와 probe 구현 완료, 그러나 2026-07-20 현재 설정된 SSH endpoint가 connection refused를 반환하여 실행 증거 미수집
- Ubuntu의 no-op backend 결과는 OS security evidence로 사용하지 않는다.

## Ubuntu 24.04 재현

Windows 명령 프롬프트에서 `Ubuntu` 배포판을 사용한다.

```sh
cd /mnt/d/_Work/goat_bank/hete_sandbox
sh evaluation/runners/run_ubuntu_evidence.sh
```

이 명령은 다음을 실행한다.

1. `cargo test --workspace --all-targets`
2. application E2E raw JSONL 생성
3. 20회 startup descriptive measurement
4. Cargo metadata 기반 architecture boundary 검사
5. raw validation 및 Markdown/LaTeX report 생성
6. Ubuntu environment manifest 생성

## OpenBSD 7.9 사전 조건

- OpenBSD VM과 SSH endpoint가 실행 중이어야 한다.
- Rust/Cargo가 설치되어 있어야 한다.
- repository가 OpenBSD의 `REMOTE_WORKSPACE`에 있어야 한다.
- 실행 계정이 `/var/hete/audit`을 생성하고 쓸 수 있어야 한다.
- verifier port 7878이 Ubuntu client에서 도달 가능해야 한다.
- SSH host key는 `security/open_bsd_connection.json`이 가리키는 pinned known-hosts 파일로 검증한다.

## OpenBSD native sandbox evidence

OpenBSD 안에서 다음을 실행한다.

```sh
cd /path/to/hete_sandbox
sh evaluation/runners/run_openbsd_native.sh "$PWD" \
  "$PWD/docs/work_reports/100_p0_p1/openbsd-native"
```

runner는 allowed path, denied path, prohibited exec, post-lock unveil probe의 stdout, stderr, exit code와 환경 정보를 저장한다. `prohibited-exec`는 pledge 위반에 의한 kernel termination이 정상 기대 결과이므로, shell 종료 상태와 OpenBSD log를 함께 판정해야 한다.

## Ubuntu–OpenBSD application E2E

Ubuntu에서 SSH 설정과 remote workspace를 준비한 뒤 실행한다.

```sh
sh evaluation/runners/run_cross_host_e2e.sh \
  USER@OPENBSD_HOST SSH_PORT /remote/path/hete_sandbox OPENBSD_HOST
```

각 scenario는 verifier를 새로 시작하므로 violation counter가 scenario 사이에 섞이지 않는다. 실행 항목은 Commit, Reject, Quarantine, Abort, wrong-policy-digest Reject이다. OS denial과 prohibited exec는 별도의 native runner가 담당한다.

## Fail-closed 확인

`protocol/fixtures/invalid/`의 fixture는 listener bind 전에 validation이 실패해야 한다. Production policy에서 no-op backend를 선택하거나 OpenBSD sandbox 적용이 실패하면 `BUSINESS_LOOP_ENTERED` marker가 출력되어서는 안 된다.

