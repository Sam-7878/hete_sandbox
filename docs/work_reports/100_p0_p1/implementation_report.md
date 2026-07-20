# POA Process Trust P0/P1 Implementation Report

작성 시각: 2026-07-20 (Asia/Seoul)

## 요약

빈 repository 골격에서 domain-neutral POA core, strict protocol validator/resolver, OpenBSD backend, AACO verifier example, evaluation pipeline을 구현했다. Ubuntu 24.04에서는 33개 Rust test가 모두 통과했고 application E2E raw record 8건 중 6건이 pass, OpenBSD 전용 2건은 `not_evaluated`로 기록됐다. OpenBSD native evidence는 host connection refusal 때문에 아직 완료되지 않았다.

## 완료

- Draft 2020-12 JSON Schema와 `additionalProperties:false`
- structured validation code/path, semantic version, promise/permission/path/size/backend/network 검증
- missing parent, multi-level, depth, cycle chain, monotonic merge 및 승인된 expansion audit
- deterministic canonical JSON, SHA-256 golden digest 및 snapshot test
- domain-neutral AACO descriptor/kernel과 Commit/Reject/Quarantine/Abort
- non-commit domain-state non-propagation 및 trust-state-only quarantine
- audit record의 policy digest 및 payload hash binding
- backend interface, explicit unsafe no-op development backend, Linux unsupported skeleton
- OpenBSD `unveil`, `unveil(NULL,NULL)`, `pledge` mapper와 fail-closed startup state
- request JSON Schema, maximum bytes, nesting depth, unknown-field/range enforcement
- inbound/outbound IP/CIDR/port/protocol allowlist와 DNS-disabled hostname rejection
- Cargo metadata 기반 dependency graph boundary check
- Ubuntu raw JSONL validation → Markdown/LaTeX generation
- 20회 Ubuntu no-op startup descriptive measurement
- OpenBSD native negative probe와 cross-host runner 구현

## 부분 완료

- OpenBSD code path는 target-specific Rust로 구현됐으나 OpenBSD 7.9에서 compile/run하지 못했다.
- simplified cross-host example은 runner까지 구현됐으나 실제 Ubuntu–OpenBSD 네트워크 실행은 미검증이다.
- environment manifest는 Ubuntu만 생성됐다. OpenBSD runner는 manifest command를 포함하지만 raw artifact가 없다.
- OpenBSD denial/termination evidence schema 통합은 native raw가 생긴 뒤 최종 report에 합쳐야 한다.

## 미완료

- SBOX-004/005/006/008 OpenBSD native 판정 및 kernel termination signal 확인
- E2E-005/E2E-006 OpenBSD raw JSONL
- OpenBSD verifier listener를 통한 E2E-001..008 전체 재현
- OpenBSD startup overhead 20회 측정
- OpenBSD environment manifest와 combined final evaluation table

## 코드 구조

- `crates/poa-core`: descriptor, outcome, AACO hook/kernel, audit type
- `crates/poa-protocol`: model, schema loader, strict validator, inheritance, canonicalization, digest
- `crates/poa-sandbox`: backend trait, OpenBSD/no-op/Linux implementations, mapper
- `crates/poa-verifier-example`: request boundary, state transition, TCP verifier, native probe
- `protocol`: schema, base/child policy, request schema, invalid fixtures, canonical golden
- `evaluation`: runners, evidence validator/report generator, environment and architecture tooling

## 검증 명령

```sh
cd /mnt/d/_Work/goat_bank/hete_sandbox
$HOME/.cargo/bin/cargo test --workspace --all-targets
sh evaluation/runners/run_ubuntu_evidence.sh
```

검증된 source commit: `8408d5ced85f3d5f80f7b735f68197172b6434a8`
