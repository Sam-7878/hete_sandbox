# UIR Phase 3 Report

## 1. Phase-2 diagnostic

Frozen Test v1 (`5f9ff9653b3d8649f8a2b1ddc8949cea917d86035fb5deba3e8d6b98437ff4f2`)는 변경하지 않았다. v1 재분석은 retrospective diagnostic이며 unseen external test로 주장하지 않는다.

Phase-2 기록 대비 semantic match는 0.372에서 0.643, outcome accuracy는 0.594에서 0.872로 변했다.

## 2. Semantic failure taxonomy

자동 taxonomy와 case-level CSV를 구현했다. 주요 오류는 intent/action/target/attribute/period/condition/policy/code-switch/morphology/syntax/security-reject로 분리된다.

## 3. Frontend changes

typed normalization, domain-instance-free SemanticLexicon, KO particle-safe entity boundary, EN alias/syntax 처리, nested condition AST, `NeedsClarification`을 추가했다.

## 4. Regression safety results

기존 fail-closed 경로를 유지했다. v1 retrospective에서 adversarial bypass=0, invalid entity FAR count=0, reject 시 renderer invocation=0였다. 실제 frozen-v2 수치는 사람 검토 전에는 산출하지 않는다.

## 5. Output contract strategy comparison

`FILTER_AND_RENDER`는 model prose를 폐기하고 verified fact와 exact match된 claim만 결정적으로 렌더링한다. 비교표는 `output_strategy_comparison.csv`에 있으며 golden contract fixture 범위이다.

## 6. Numeric fidelity

`N1_VERIFIED_NUMERIC_SLOT_BINDING`은 numeric value를 문자열로 보존하고 provenance 및 source SHA-256 digest를 결합한다. `numeric_diagnostic.csv`는 golden diagnostic이다.

## 7. Frozen-v2 design

1,200건, KO/EN 각 600건 후보를 생성했다. parser hash `bee778f3e3767fdcd64d0926f27c680143d217ea1d6febcabd08aac96de321d7`가 기록되었다. 현재 상태는 `candidate_pending_human_review`이며 frozen benchmark가 아니다.

## 8. Human review agreement

상태: `pending`; reviewer count: `0`; agreement: `None`; adjudicated: `False`.

## 9. Leakage analysis

dev template ID와 후보 template ID 분리, exact/normalized/5-gram/entity/lexicon overlap 자동 검사를 구현했다. 상세는 `LEAKAGE_REPORT.md` 참조.

## 10. Generalization

최종 수치는 **WITHHELD_PENDING_HUMAN_REVIEW**이다. 후보를 unseen frozen-v2로 부르지 않는다.

## 11. Groundedness

claim exact metric을 primary로 유지하고 field-level metric을 보조로 검증했다. 100개 golden fixture를 사용한다.

## 12. Safety–utility trade-off

전략별 diagnostic Pareto 표를 생성했다. 이는 golden fixture 결과이고 최종 SCI 결과가 아니다.

## 13. Statistics

safety, utility, latency 파일을 분리했다. 실측 v2 표본이 없는 검정은 `NA`로 유지했다.

## 14. Runtime

Rust 단위 시험과 Python artifact validation을 Ubuntu 24.04 및 프로젝트 `.venv`에서 수행한다.

## 15. Failure analysis

v1 실패 taxonomy와 pipeline funnel로 parser, retrieval, generation, validation 손실을 분리한다.

## 16. Limitations

실제 독립 reviewer 2인 검토와 adjudication, 그 후의 모델 캠페인은 아직 수행되지 않았다. diagnostic fixture 수치는 실제 LLM 성능으로 해석할 수 없다.

## 17. Publication-readiness verdict

**BLOCKED — HUMAN REVIEW REQUIRED.** `review_gate.py`가 완료되기 전 publication-ready report 생성은 ARCH-UIR-GEN-006에 의해 실패한다.
