# Deterministic Policy Merge Rules

## Resolution

- parent lookup key는 `protocol_id`이다.
- parent부터 child 방향으로 최대 depth 8까지 계산한다.
- missing parent와 cycle은 전체 chain을 포함한 구조화 오류로 종료한다.
- effective policy에서는 `extends`와 승인 metadata를 제거한다.

## Operations

- `name`을 key로 merge한다.
- child가 parent의 required context를 제거하면 거부한다.
- allowed actor 추가와 새 operation 추가는 privilege expansion이다.
- 명시적 승인 없는 production expansion은 거부한다.

## Pledge와 unveil

- 기본 pledge 결과는 parent/child promise 교집합이다.
- child-only promise는 승인 없는 경우 거부한다.
- 동일 unveil path는 parent permission의 부분집합만 허용한다.
- 새 unveil path 및 permission 확대는 승인 없는 경우 거부한다.
- duplicate path 또는 permission conflict는 validation/enforcement 전에 거부한다.

## Data와 network

- input schema 변경은 ambiguous conflict로 거부한다.
- message size 및 nesting depth는 더 작은 값을 사용한다.
- inbound/outbound endpoint 또는 DNS 권한 추가는 privilege expansion이다.
- endpoint set은 protocol/address/port tuple로 비교한다.

## Approval metadata

`privilege_expansion.approved=true`이고 non-empty approval ID와 reason이 있어야 expansion이 허용된다. 허용된 expanded field는 `expansion_audit`에 남고, 승인 metadata 자체는 effective policy digest에서 제외된다.

## Canonical form

- object key는 lexical order로 정렬한다.
- set 성격 array와 operations는 정의된 deterministic order로 정렬한다.
- whitespace를 제거한다.
- 현재 정책 model의 numeric field는 integer만 허용한다.
- canonical bytes에 SHA-256을 적용하고 `sha256:<hex>`로 표기한다.

Golden digest: `sha256:3f3fbd07bb40da498804282a09ddbb2354050bd3a14bd9c5c845dd16bfd8404a`

