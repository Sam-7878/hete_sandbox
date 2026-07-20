# Legacy HETE Reference Review

참조 대상은 `goat_bank/hete`이며 읽기 전용으로 검토했다. 새 구현과 산출물은 모두 `goat_bank/hete_sandbox`에만 유지한다.

## 반영한 항목

### Empty-unveil Null Lock

기존 OpenBSD sandbox는 unveil path가 비어 있을 때 다음 순서를 사용한다.

```text
unveil("/", "")
unveil(NULL, NULL)
```

OpenBSD에서 `unveil(NULL, NULL)`만 호출하면 사전에 unveil된 path가 없는 경우 filesystem 제한이 생기지 않는다. Sandbox mapper에 explicit root-mask plan을 추가하고 `empty_unveil_policy_masks_root_before_lock` test로 고정했다.

## 의도적으로 그대로 가져오지 않은 항목

- 기존 non-OpenBSD stub은 경고 후 계속 실행하지만, 새 구현은 production no-op을 명세 validation과 backend 양쪽에서 거부한다.
- 기존 구현은 pledge 목록이 비면 `stdio`를 자동 추가한다. 새 작업지시서는 mapper가 policy에 없는 promise를 임의 추가하지 못하게 하므로 이를 채택하지 않았다. 빈 pledge가 OpenBSD에서 적용 불가능하면 startup이 fail-closed 된다.
- 기존 compatibility 함수는 명세가 없을 때 default sandbox로 진행한다. 새 구현은 missing/invalid specification에서 listener 이전에 종료한다.
- 기존 domain protocol과 banking/drone operation은 generic core로 복사하지 않았다.

## 향후 OpenBSD 재검증에 참고할 항목

- `hete/tests/run_openbsd_native_tests.py`는 pinned host key와 `RejectPolicy`를 사용하는 strict SSH 구조다.
- `hete/tests/bootstrap_openbsd_ssh.py`는 host fingerprint 확인과 key login 검증 절차를 제공한다.
- sandbox VM 연결이 복구되면 새 runner도 동일한 pinned-host-key 원칙으로 실행해야 한다.

