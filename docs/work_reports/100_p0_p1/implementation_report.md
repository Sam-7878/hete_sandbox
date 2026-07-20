# POA Process Trust P0/P1 Implementation Report

작성 시각: 2026-07-20 (Asia/Seoul)

## 요약

Domain-neutral POA core, strict protocol validator/resolver, OpenBSD process sandbox, AACO verifier example, evaluation pipeline을 구현했다. 동일한 source commit `d6210e48312f14b2ed19104a02c66e481bdb6a01`을 기준으로 Ubuntu 24.04.4와 OpenBSD 7.9에서 Rust test 35개가 각각 모두 통과했다.

Ubuntu client에서 OpenBSD verifier로 실제 TCP 요청을 보내 Commit, Reject, Quarantine, Abort, wrong-digest Reject를 확인했다. OpenBSD native probe에서 allowed path 성공, policy 외 path의 ENOENT, prohibited exec의 SIGABRT, lock 이후 unveil 변경의 EPERM을 확인했다. Malformed policy와 존재하지 않는 required unveil resource는 모두 exit 1로 listener 이전에 종료됐다.

## 완료 항목

- Draft 2020-12 JSON Schema와 `additionalProperties:false`
- 구조화 validation code/path, semantic version, pledge/unveil/path/size/backend/network 검증
- missing parent, multi-level, depth, cycle chain, monotonic inheritance와 승인된 expansion audit
- deterministic canonical JSON, SHA-256 golden digest, snapshot test
- domain-neutral AACO descriptor/kernel과 Commit/Reject/Quarantine/Abort
- non-commit domain-state 비전파와 quarantine trust-state 격리
- audit record의 policy digest 및 payload hash binding
- OpenBSD `unveil`, null lock, `pledge`와 listener 이전 resource preparation
- explicit unsafe no-op development backend와 unsupported Linux skeleton
- request schema, byte/depth/range/unknown-field 제한
- inbound/outbound IP/CIDR/port/protocol allowlist와 DNS-disabled hostname rejection
- Cargo metadata 기반 dependency boundary 검사
- Ubuntu raw JSONL, 20회 startup 측정, Markdown/LaTeX 생성
- OpenBSD native 및 Ubuntu→OpenBSD cross-host raw JSONL과 combined report
- Ubuntu/OpenBSD 환경 manifest와 실행 로그 보존

## 검증 결과

- Ubuntu 24.04.4: Rust 35/35, application evidence 6 passed + OpenBSD 전용 2 not evaluated
- OpenBSD 7.9: Rust 35/35
- OpenBSD combined evidence: 13/13 passed, startup failure 2건, denial/termination record 5건, policy digest 1개
- Cross-host outcomes: Commit 1, Reject 2, Quarantine 1, Abort 1
- OpenBSD kernel probes: allowed 1, filesystem denial 1, SIGABRT 1, post-lock EPERM 1

상세 값은 `generated/evaluation_report_ubuntu.md`, `generated/evaluation_report_openbsd_combined.md`, 각 raw JSONL을 authoritative artifact로 사용한다.

## 남은 범위

- OpenBSD startup overhead 20회 측정은 수행하지 않았다. Ubuntu no-op 측정값을 OpenBSD 비용으로 해석하지 않는다.
- 본 구현은 연구용 running example이며 production Open Banking compliance, 외부 승인자 서명 검증, tamper-evident audit storage를 제공하지 않는다.

## 코드 구조

- `crates/poa-core`: descriptor, outcome, AACO hook/kernel, audit type
- `crates/poa-protocol`: model, schema loader, validator, inheritance, canonicalization, digest
- `crates/poa-sandbox`: backend trait, OpenBSD/no-op/Linux implementations, mapper
- `crates/poa-verifier-example`: request boundary, transition, TCP verifier, native probe
- `protocol`: schema, policies, request schema, invalid fixtures, canonical golden
- `evaluation`: runners, evidence validator/report generator, environment and architecture tooling

## 재현 기준

```sh
cd /mnt/d/_Work/goat_bank/hete_sandbox
cargo test --workspace --all-targets
sh evaluation/runners/run_ubuntu_evidence.sh
```

검증 source commit: `d6210e48312f14b2ed19104a02c66e481bdb6a01`
