# POA Process-Trust Running Example

## 검증 상태

- Ubuntu 24.04.4 LTS: Rust 35 tests, application evidence, architecture check, raw-to-report pipeline 완료
- OpenBSD 7.9: Rust 35 tests, native sandbox probe, Ubuntu→OpenBSD cross-host E2E 완료
- 검증 source commit: `d6210e48312f14b2ed19104a02c66e481bdb6a01`

Ubuntu의 no-op backend 결과는 OpenBSD OS security evidence로 사용하지 않는다.

## Ubuntu 24.04 재현

Windows에서 배포판 이름 `Ubuntu`인 24.04 인스턴스를 사용한다. `Ubuntu-20.04`는 사용하지 않는다.

```sh
cd /mnt/d/_Work/goat_bank/hete_sandbox
sh evaluation/runners/run_ubuntu_evidence.sh
```

이 runner는 workspace tests, application raw JSONL, 20회 startup 측정, architecture 검사, report, environment manifest를 생성한다.

## OpenBSD native sandbox evidence

OpenBSD 7.9에서 실행한다.

```sh
cd /path/to/hete_sandbox
sh evaluation/runners/run_openbsd_native.sh "$PWD" \
  "$PWD/docs/work_reports/100_p0_p1/openbsd-native"
```

Allowed path, denied path, prohibited exec, post-lock unveil의 stdout/stderr/exit code와 환경 정보를 저장한다. `prohibited-exec`의 exit 134와 `Abort trap`은 pledge 위반의 기대 결과다.

## Ubuntu–OpenBSD E2E

SSH 연결 정보는 `security/open_bsd_connection.json`을 사용한다. 이 환경에서 SSH는 port 22이며 `verifier_port: 50051`은 SSH port가 아니다. Example verifier는 TCP 7878에서 수신한다.

```sh
cd /mnt/d/_Work/goat_bank/hete_sandbox
SSH_KEY=/home/sam/.ssh/hete_openbsd_ed25519 \
KNOWN_HOSTS=/home/sam/.ssh/hete_openbsd_known_hosts \
RUN_TAG=manual-$(date -u +%Y%m%dT%H%M%SZ) \
sh evaluation/runners/run_cross_host_e2e.sh \
  sam@192.168.1.102 22 /remote/path/hete_sandbox 192.168.1.102
```

Pinned known-hosts, strict host-key checking, batch authentication을 적용한다. Runner는 Commit, Reject, Quarantine, Abort, wrong-digest, malformed spec, missing unveil resource를 실행한다. OS denial과 prohibited exec는 native runner가 담당한다.

## Fail-closed 판정

- 정상 server log에는 sandbox 적용 뒤 `BUSINESS_LOOP_ENTERED policy_digest=...`가 있어야 한다.
- Malformed spec과 missing resource는 non-zero exit, `listener_status=closed`, BUSINESS_LOOP marker 없음이어야 한다.
- `protocol/fixtures/invalid/kernel-resource-missing.json`은 schema-valid이지만 required unveil path가 존재하지 않는 runtime failure fixture다.

## 증거 재생성

```sh
python3 evaluation/collect_cross_host_evidence.py \
  docs/work_reports/100_p0_p1/cross-host \
  docs/work_reports/100_p0_p1/raw/openbsd-cross-host.jsonl \
  --source-commit "$(git rev-parse HEAD)" \
  --policy-digest-file protocol/examples/hete.verifier.payment.effective.sha256

python3 evaluation/collect_openbsd_evidence.py \
  docs/work_reports/100_p0_p1/openbsd-native \
  docs/work_reports/100_p0_p1/raw/openbsd-native.jsonl \
  --source-commit "$(git rev-parse HEAD)" \
  --policy-digest-file protocol/examples/hete.verifier.payment.effective.sha256
```
