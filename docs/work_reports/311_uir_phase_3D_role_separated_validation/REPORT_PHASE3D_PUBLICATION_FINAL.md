# UIR Phase 3D Publication Evidence Report

## 1. Evidence correction rationale

Phase 3C R1/R2/R3 artifacts remain reclassified as `Phase3C-script-audit`: they were deterministic validator outputs and are not admitted as direct model judgments. The role-separated audit below uses only the captured Gemini outputs.

## 2. Actual role-separated AI-model audit provenance

Validation status: **PASS**. Shared cases: 1200. Unique model sessions: 144.

| Reviewer | Engine | Model selector | Rows | Verified raw batches | Review SHA-256 |
|---|---|---|---:|---:|---|
| AI-R1 | AntiGravity Gemini 3.5 Flash | `gemini-3.5-flash` | 1200 | 48 | `357efb32f012a946d5d1b40dcfe804f3fabdf692361a822192840965af21af90` |
| AI-R2 | AntiGravity Gemini 3.6 Flash | `gemini-3.6-flash-high` | 1200 | 48 | `2d1126b47fee45f49ece3f6376c9aeead45725f6c17a67f8ea1f999dae273b6e` |
| AI-R3 | AntiGravity Gemini 3.1 Pro | `gemini-3.1-pro` | 1200 | 48 | `d1758cfe2f784576c30586166a4fd9d4a81fd1d4fe6387612776d220cd67fcc6` |

All 3,600 final rows were checked against 144 captured model batches, including session IDs, exact model selectors, underlying response-stream hashes, schema-validated `structured_output` judgments, prompt hash, and frozen case coverage. Script-generated judgments were not admitted.

Packet metadata warnings retained for reproducibility:

- AI-R1: packet engine=['AntiGravity Sonnet 4.6'], actual role=AntiGravity Gemini 3.5 Flash; the original packets are retained for hash reproducibility
- AI-R3: packet engine=['AntiGravity Opus 4.6'], actual role=AntiGravity Gemini 3.1 Pro; the original packets are retained for hash reproducibility

The original packet files were not retrospectively edited because their SHA-256 values are recorded in every review provenance. Actual engine identity is established by each CLI capture's model selector and the matching review wrapper.

## 3. Cross-model agreement

| Field | N | Three-way raw | Fleiss kappa | R1-R2 raw | R1-R3 raw | R2-R3 raw |
|---|---:|---:|---:|---:|---:|---:|
| source_text_valid | 1200 | 1.000000 | NA | 1.000000 | 1.000000 | 1.000000 |
| language_valid | 1200 | 1.000000 | NA | 1.000000 | 1.000000 | 1.000000 |
| intent_valid | 1200 | 0.979167 | 0.792806 | 0.979167 | 1.000000 | 0.979167 |
| target_valid | 1200 | 0.999167 | -0.000278 | 0.999167 | 1.000000 | 0.999167 |
| conditions_valid | 1200 | 0.415000 | 0.199507 | 0.487500 | 0.812500 | 0.530000 |
| policy_valid | 1200 | 1.000000 | NA | 1.000000 | 1.000000 | 1.000000 |
| outcome_valid | 1200 | 1.000000 | NA | 1.000000 | 1.000000 | 1.000000 |
| claims_valid | 1200 | 0.915833 | 0.169340 | 0.978333 | 0.916667 | 0.936667 |

Kappa is reported as `NA` with `zero_marginal_variance` where a statistic is undefined; it is never forced to 1.0. 15 defined kappa values were independently recomputed with scikit-learn 1.8.0 and statsmodels 0.14.6; maximum absolute delta was 3.2751579226442118e-15 (status: PASS).

## 4. Benchmark uncertainty and disagreement analysis

Field-level disagreement records: 829. Unresolved records: 0.

- `R1 == R2 != R3`: 162 field-level records
- `R1 == R3 != R2`: 504 field-level records
- `R2 == R3 != R1`: 163 field-level records

Case-level rationales and majority status are retained in `results/uir_phase3d/actual_ai_adjudication.csv`.

## 5. Frozen-v2 integrity

Dataset SHA-256: `9bb8a5d423b53bae14b2c699cba6b1338f0115345f94c6b4a9f93af2400d4a3c`. Parser SHA-256: `bee778f3e3767fdcd64d0926f27c680143d217ea1d6febcabd08aac96de321d7`. Prompt-template SHA-256: `1660e3f70d9c11b0b415a7adb3c4bcc01dd1b8c9576af19c8881335336198310`.

## 6. B0-B6 baselines

Campaign records: 9800; campaign ID: `phase3d-publication-final`. Seven pipelines B0-B6 are included.

## 7. UIR semantic generalization

Overall semantic match 0.875000, structural match 0.875000, and cross-lingual equivalence 1.000000.

## 8. Policy enforcement

Frozen policy semantics were unchanged. Detailed policy accuracy, FAR, FRR, and invalid-entity rejection results remain in `policy_summary.csv` and the final statistical artifacts.

## 9. Adversarial safety

B6 attack success, policy bypass, entity-lock violation, and unsupported-claim acceptance are recorded in `safety_summary.csv` and `stat_safety_final.csv`.

## 10. B5 versus B6 safety-utility trade-off

B6 states: `{"FULL_VERIFIED_ANSWER": 1050, "NO_VERIFIED_ANSWER": 150, "PARTIAL_VERIFIED_ANSWER": 200}`. Unsupported acceptance: 0.000000. Useful-answer rate: 1.000000.

## 11. Real SEC factual and numeric fidelity

Compact immutable fact IDs prevent the model from reproducing numeric values, units, provenance URIs, and hashes. B6 end-to-end numeric preservation is 0.950000, unit accuracy 0.950000, and provenance coverage/correctness 1.000000/1.000000. Valid JSON is 1.000000, truncation 0.000000, and missing provenance 0.000000. The ten numeric misses are partial selections that omit the numeric fact; no incorrect numeric claim is accepted.

## 12. Runtime

Stage-level P50/P95/P99 data are in `latency_summary.csv`. Configured generation budget: 384; measured valid-output P99: 87.0; 1.25x rule pass: True.

## 13. Statistical significance

Safety and utility use paired McNemar tests with bootstrapped risk-difference confidence intervals; latency uses Wilcoxon and paired bootstrap; Holm correction is applied.

## 14. Failure analysis

All final campaign failures remain in `failures.jsonl`; no low-performing case was removed. Policy-prevented B6 paths are `NO_VERIFIED_ANSWER`, while real-fact partial selections are `PARTIAL_VERIFIED_ANSWER`.

## 15. Reproducibility

Generation commit `738278b`, post-processing commit `e6ad3460bb7d1e0566ccebaecb15be8430153714`, workers `8`, and dataset/parser/model/config hashes are recorded in `run_manifest_phase3d.json`. Actual reviewer output hashes are listed above and in `actual_ai_audit_summary.json`.

## 16. Limitations

The benchmark was independently audited by three AI model engines under isolated contexts. This measures cross-model annotation consistency and is not human ground-truth validation. The AntiGravity CLI did not expose a runtime temperature setting, so provenance records `not_exposed_by_antigravity_cli` rather than claiming an unverifiable temperature. R1/R3 packet engine labels retained legacy names; this metadata mismatch is disclosed above and the packet hashes are frozen.

## 17. Publication readiness

Status: **READY_FOR_MANUSCRIPT_DRAFT**. Blocking checks: `none`.
