# Unverified Claims

다음 주장은 이번 결과로 검증되지 않았다.

- OpenBSD 7.9에서 allowed path read/write가 성공한다.
- `unveil`이 policy 밖의 filesystem path를 실제로 차단한다.
- `pledge`가 prohibited exec/syscall에서 process를 kernel termination한다.
- unveil lock 이후 policy modification이 실제로 거부된다.
- sandbox 적용 실패가 OpenBSD native binary의 business loop 진입을 막는다.
- Ubuntu client와 OpenBSD verifier 사이 E2E-001..008이 실제 네트워크에서 모두 재현된다.
- OpenBSD startup overhead의 P50/P95/max 값.
- malware, supply-chain attack, 모든 내부자 공격에 대한 완전한 방어.
- production readiness, zero defect, 100% security.
- full Open Banking, DID 또는 system-wide exactly-once compliance.
- 다른 OS 또는 Linux 대비 성능/보안 우월성.

Native 재검증은 OpenBSD VM과 SSH endpoint가 복구된 뒤 `README_running_example.md`의 runner를 실행하고, raw log/exit code/signal/environment manifest를 보존한 후에만 이 목록에서 제거한다.

