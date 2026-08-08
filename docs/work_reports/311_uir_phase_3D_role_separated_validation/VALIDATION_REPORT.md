# Phase 3D Role-Separated Audit Validation Report

## Outcome

Validation completed successfully. The publication gate status is `READY_FOR_MANUSCRIPT_DRAFT`; all nine gate checks pass.

Codex did not generate, fill, or edit reviewer judgments. Validation used the user-supplied AntiGravity outputs only.

## Input state

- Ubuntu: 24.04.4 LTS
- Python environment: `/mnt/d/_Work/goat_bank/.venv`
- Pre-validation repository commit: `01c433b2b9b1e93c8428899c55cca8081560eb65`
- Pre-validation worktree: clean
- Shared frozen cases: 1,200
- Prompt-template SHA-256: `1660e3f70d9c11b0b415a7adb3c4bcc01dd1b8c9576af19c8881335336198310`
- Frozen-v2 SHA-256: `9bb8a5d423b53bae14b2c699cba6b1338f0115345f94c6b4a9f93af2400d4a3c`
- Parser SHA-256: `bee778f3e3767fdcd64d0926f27c680143d217ea1d6febcabd08aac96de321d7`

## Provenance and integrity validation

| Reviewer | Engine | Rows | Raw batches | Unique sessions | Review SHA-256 |
|---|---|---:|---:|---:|---|
| AI-R1 | AntiGravity Gemini 3.5 Flash | 1,200 | 48 | 48 | `357efb32f012a946d5d1b40dcfe804f3fabdf692361a822192840965af21af90` |
| AI-R2 | AntiGravity Gemini 3.6 Flash | 1,200 | 48 | 48 | `2d1126b47fee45f49ece3f6376c9aeead45725f6c17a67f8ea1f999dae273b6e` |
| AI-R3 | AntiGravity Gemini 3.1 Pro | 1,200 | 48 | 48 | `d1758cfe2f784576c30586166a4fd9d4a81fd1d4fe6387612776d220cd67fcc6` |

The validator confirmed:

- exactly 1,200 unique, known case IDs per reviewer;
- identical three-reviewer case-ID sets;
- 144 distinct model session IDs with no cross-reviewer reuse;
- exact reviewer, engine, and model-selector identity;
- required provenance and `actual_model_generation` annotation method;
- `not_exposed_by_antigravity_cli` temperature disclosure;
- valid eight-field judgments and complete reconstruction objects;
- final JSONL judgments exactly match the captured schema-validated `structured_output` objects;
- all 144 underlying response-stream SHA-256 values recompute correctly and remain preserved separately;
- no script-generated judgment was admitted.

Result: `PASS`, failures: 0.

## Disclosed packet metadata warning

The immutable R1 and R3 packet rows retain legacy engine labels (`AntiGravity Sonnet 4.6` and `AntiGravity Opus 4.6`). The actual captures and final wrappers identify `gemini-3.5-flash` and `gemini-3.1-pro` respectively. The original packets were not edited retrospectively because their hashes are recorded in review provenance. This mismatch is disclosed in the final report and must remain a limitation in the manuscript.

## Agreement results

| Field | Three-way raw | Fleiss kappa |
|---|---:|---:|
| source_text_valid | 1.000000 | NA |
| language_valid | 1.000000 | NA |
| intent_valid | 0.979167 | 0.792806 |
| target_valid | 0.999167 | -0.000278 |
| conditions_valid | 0.415000 | 0.199507 |
| policy_valid | 1.000000 | NA |
| outcome_valid | 1.000000 | NA |
| claims_valid | 0.915833 | 0.169340 |

There are 829 field-level disagreement records and no unresolved three-label cases:

- `R1 == R2 != R3`: 162
- `R1 == R3 != R2`: 504
- `R2 == R3 != R1`: 163
- all three disagree: 0

Undefined kappas use `NA / zero_marginal_variance`; they are not forced to 1.0. Fifteen defined Cohen/Fleiss kappa values were independently recomputed with scikit-learn 1.8.0 and statsmodels 0.14.6. Maximum absolute difference from ingestion output was `3.2751579226442118e-15`, below the `1e-12` tolerance.

The low `conditions_valid` agreement is material benchmark uncertainty and must not be summarized as uniformly high cross-model agreement.

## Publication gate

All required checks are true:

- `actual_multi_model_audit_complete`
- `model_review_provenance_recorded`
- `agreement_statistics_valid`
- `frozen_v2_integrity_verified`
- `SEC_truncation_fixed`
- `real_fact_campaign_complete`
- `B6_filtering_verified`
- `B0_B6_final_campaign_complete`
- `final_statistics_complete`

Final status: `READY_FOR_MANUSCRIPT_DRAFT`.

## Verification commands

```bash
source ../.venv/bin/activate
python evaluation/uir_phase3d/validate_role_separated_audits.py
python evaluation/uir_phase3d/ingest_actual_ai_reviews.py \
  --air1 results/uir_phase3d/actual_ai_work/actual_ai_review_R1.jsonl \
  --air2 docs/work_reports/309_uir_phase_3D_role_separated_R2/actual_ai_review_R2.jsonl \
  --air3 docs/work_reports/310_uir_phase_3D_role_separated_R3/actual_ai_review_R3.jsonl
python evaluation/uir_phase3d/validate_agreement_statistics.py
python evaluation/uir_phase3d/publication_gate_phase3d.py
python evaluation/uir_phase3d/generate_phase3d_report.py
pytest -q evaluation/uir_phase3d
```

Test result: `8 passed`.
