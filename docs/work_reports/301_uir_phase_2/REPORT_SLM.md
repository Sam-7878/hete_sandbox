# Phase UIR-2 SCI Evaluation Report

## 1. Summary

A frozen external test, real SEC fact registry, real local Phi-3.5 renderer, B0–B5 baselines, groundedness, numeric, adversarial, generalization, robustness, statistics, and runtime evidence were evaluated without changing the frozen set after hashing. B5 reduced accepted unsupported-claim rate from 1.000 (B0) to 0.000, but its outcome accuracy was only 0.356 and claim recall 0.004359. The result supports a safety-enforcement claim, not a general utility-superiority claim.

## 2. Clean Baseline Commit

Source commit: `cca515db6919219a2af71419aefa1ff733897825`. Worktree clean at recorded run start: `True`.

## 3. Frozen Test Dataset and Hash

Cases: 1000; SHA-256: `5f9ff9653b3d8649f8a2b1ddc8949cea917d86035fb5deba3e8d6b98437ff4f2`; human review status: `not_performed`.

## 4. Local SLM Configuration

Configured model: `phi3.5:latest`. The complete Ollama model response and configuration digest are preserved in `model_manifest.json`.

## 5. Real/Frozen Fact Registry

The registry is a hashed snapshot derived from the official SEC XBRL Companyfacts API. Evaluation reads only the frozen JSONL snapshot.

## 6. Baseline Pipelines B0–B5

| pipeline | cases | claim_precision | claim_recall | unsupported_claim_rate | unsupported_claim_acceptance_rate | outcome_accuracy |
|---|---|---|---|---|---|---|
| B0_DIRECT_SLM | 1000 | 0.0 | 0.0 | 1.0 | 1.0 | 0.633 |
| B1_SLM_WITH_PROMPT_GUARD | 1000 | 0.0 | 0.0 | 1.0 | 1.0 | 0.642 |
| B2_NAIVE_RAG_SLM | 1000 | 0.5041816009557945 | 0.1082051282051282 | 0.4958183990442055 | 0.4958183990442055 | 0.635 |
| B3_RAG_WITH_ENTITY_VALIDATION | 1000 | 0.057539682539682536 | 0.007435897435897436 | 0.9424603174603174 | 0.9424603174603174 | 0.559 |
| B4_UIR_POLICY_SLM | 1000 | 0.16346153846153846 | 0.004358974358974359 | 0.8365384615384616 | 0.8365384615384616 | 0.443 |
| B5_FULL_UIR_OUTPUT_VALIDATION | 1000 | 0.16346153846153846 | 0.004358974358974359 | 0.8365384615384616 | 0.0 | 0.356 |

## 7. Generalization Splits

| split | language | cases | semantic_match | policy_accuracy | outcome_accuracy |
|---|---|---|---|---|---|
| G1_TEMPLATE_SEEN_ENTITY_UNSEEN | ko | 100 | 0.77 | 0.89 | 0.89 |
| G1_TEMPLATE_SEEN_ENTITY_UNSEEN | en | 100 | 0.85 | 0.95 | 0.95 |
| G2_TEMPLATE_UNSEEN_ENTITY_SEEN | ko | 100 | 0.05 | 0.35 | 0.35 |
| G2_TEMPLATE_UNSEEN_ENTITY_SEEN | en | 100 | 0.05 | 0.35 | 0.35 |
| G3_TEMPLATE_UNSEEN_ENTITY_UNSEEN | ko | 100 | 0.05 | 0.35 | 0.35 |
| G3_TEMPLATE_UNSEEN_ENTITY_UNSEEN | en | 100 | 0.05 | 0.35 | 0.35 |
| G4_LEXICAL_UNSEEN | ko | 100 | 0.05 | 0.35 | 0.35 |
| G4_LEXICAL_UNSEEN | en | 100 | 0.05 | 0.35 | 0.35 |
| G5_STRUCTURAL_UNSEEN | ko | 100 | 0.9 | 1.0 | 1.0 |
| G5_STRUCTURAL_UNSEEN | en | 100 | 0.9 | 1.0 | 1.0 |

## 8. Claim-Level Metrics

Claims are normalized into entity, attribute, numeric, relation, temporal, and provenance dimensions and matched exactly against frozen verified claims.

## 9. Numeric Fidelity

| pipeline | numeric_type | cases | numeric_exact_match | unit_accuracy | sign_accuracy | relative_change_accuracy |
|---|---|---|---|---|---|---|
| B0_DIRECT_SLM | currency | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B0_DIRECT_SLM | decimal | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B0_DIRECT_SLM | integer | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B0_DIRECT_SLM | multiple_numbers | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B0_DIRECT_SLM | percentage | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B0_DIRECT_SLM | ratio | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B0_DIRECT_SLM | signed_change | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B0_DIRECT_SLM | year_over_year_delta | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B1_SLM_WITH_PROMPT_GUARD | currency | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B1_SLM_WITH_PROMPT_GUARD | decimal | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B1_SLM_WITH_PROMPT_GUARD | integer | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B1_SLM_WITH_PROMPT_GUARD | multiple_numbers | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B1_SLM_WITH_PROMPT_GUARD | percentage | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B1_SLM_WITH_PROMPT_GUARD | ratio | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B1_SLM_WITH_PROMPT_GUARD | signed_change | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B1_SLM_WITH_PROMPT_GUARD | year_over_year_delta | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B2_NAIVE_RAG_SLM | currency | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B2_NAIVE_RAG_SLM | decimal | 25 | 0.0 | 0.32 | 0.0 | 0.32 |
| B2_NAIVE_RAG_SLM | integer | 25 | 0.0 | 0.32 | 0.0 | 0.32 |
| B2_NAIVE_RAG_SLM | multiple_numbers | 25 | 0.0 | 0.32 | 0.0 | 0.32 |
| B2_NAIVE_RAG_SLM | percentage | 25 | 0.12 | 0.32 | 0.12 | 0.32 |
| B2_NAIVE_RAG_SLM | ratio | 25 | 0.32 | 0.88 | 0.32 | 0.88 |
| B2_NAIVE_RAG_SLM | signed_change | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B2_NAIVE_RAG_SLM | year_over_year_delta | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B3_RAG_WITH_ENTITY_VALIDATION | currency | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B3_RAG_WITH_ENTITY_VALIDATION | decimal | 25 | 0.0 | 0.12 | 0.0 | 0.12 |
| B3_RAG_WITH_ENTITY_VALIDATION | integer | 25 | 0.0 | 0.12 | 0.0 | 0.12 |
| B3_RAG_WITH_ENTITY_VALIDATION | multiple_numbers | 25 | 0.0 | 0.2 | 0.0 | 0.2 |
| B3_RAG_WITH_ENTITY_VALIDATION | percentage | 25 | 0.12 | 0.12 | 0.12 | 0.12 |
| B3_RAG_WITH_ENTITY_VALIDATION | ratio | 25 | 0.68 | 0.76 | 0.68 | 0.76 |
| B3_RAG_WITH_ENTITY_VALIDATION | signed_change | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B3_RAG_WITH_ENTITY_VALIDATION | year_over_year_delta | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B4_UIR_POLICY_SLM | currency | 25 | 0.0 | 0.2 | 0.0 | 0.2 |
| B4_UIR_POLICY_SLM | decimal | 25 | 0.0 | 0.44 | 0.0 | 0.44 |
| B4_UIR_POLICY_SLM | integer | 25 | 0.0 | 0.2 | 0.0 | 0.2 |
| B4_UIR_POLICY_SLM | multiple_numbers | 25 | 0.0 | 0.4 | 0.0 | 0.4 |
| B4_UIR_POLICY_SLM | percentage | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B4_UIR_POLICY_SLM | ratio | 25 | 0.56 | 0.56 | 0.56 | 0.56 |
| B4_UIR_POLICY_SLM | signed_change | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B4_UIR_POLICY_SLM | year_over_year_delta | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B5_FULL_UIR_OUTPUT_VALIDATION | currency | 25 | 0.0 | 0.2 | 0.0 | 0.2 |
| B5_FULL_UIR_OUTPUT_VALIDATION | decimal | 25 | 0.0 | 0.44 | 0.0 | 0.44 |
| B5_FULL_UIR_OUTPUT_VALIDATION | integer | 25 | 0.0 | 0.2 | 0.0 | 0.2 |
| B5_FULL_UIR_OUTPUT_VALIDATION | multiple_numbers | 25 | 0.0 | 0.4 | 0.0 | 0.4 |
| B5_FULL_UIR_OUTPUT_VALIDATION | percentage | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B5_FULL_UIR_OUTPUT_VALIDATION | ratio | 25 | 0.56 | 0.56 | 0.56 | 0.56 |
| B5_FULL_UIR_OUTPUT_VALIDATION | signed_change | 25 | 0.0 | 0.0 | 0.0 | 0.0 |
| B5_FULL_UIR_OUTPUT_VALIDATION | year_over_year_delta | 25 | 0.0 | 0.0 | 0.0 | 0.0 |

## 10. Adversarial Results

| pipeline | cases | attack_success_rate | policy_bypass_rate | unsupported_claim_acceptance_rate | renderer_invocation_on_reject_rate |
|---|---|---|---|---|---|
| B0_DIRECT_SLM | 300 | 0.43333333333333335 | 1.0 | 1.0 | 0.0 |
| B1_SLM_WITH_PROMPT_GUARD | 300 | 0.2866666666666667 | 1.0 | 1.0 | 0.0 |
| B2_NAIVE_RAG_SLM | 300 | 0.62 | 1.0 | 1.0 | 0.0 |
| B3_RAG_WITH_ENTITY_VALIDATION | 300 | 0.7733333333333333 | 1.0 | 1.0 | 0.0 |
| B4_UIR_POLICY_SLM | 300 | 0.0 | 0.0 | 0.0 | 0.0 |
| B5_FULL_UIR_OUTPUT_VALIDATION | 300 | 0.0 | 0.0 | 0.0 | 0.0 |

## 11. Cross-Seed Results

| pipeline | metric | runs | mean | variance | minimum | maximum |
|---|---|---|---|---|---|---|
| B0_DIRECT_SLM | claim_precision | 5 | 0.27999999999999997 | 0.0005999999999999997 | 0.25 | 0.3 |
| B0_DIRECT_SLM | unsupported_claim_rate | 5 | 0.45999999999999996 | 0.004400000000000003 | 0.35 | 0.55 |
| B0_DIRECT_SLM | latency_us | 5 | 1129250.25 | 21121275189.191 | 972348.6 | 1399502.05 |
| B0_DIRECT_SLM | validator_rejection_rate | 5 | 0.0 | 0.0 | 0.0 | 0.0 |
| B4_UIR_POLICY_SLM | claim_precision | 5 | 0.35 | 0.0 | 0.35 | 0.35 |
| B4_UIR_POLICY_SLM | unsupported_claim_rate | 5 | 0.12 | 0.0005999999999999997 | 0.1 | 0.15 |
| B4_UIR_POLICY_SLM | latency_us | 5 | 362063.82999999996 | 111035208.8745999 | 348024.7 | 373987.25 |
| B4_UIR_POLICY_SLM | validator_rejection_rate | 5 | 0.0 | 0.0 | 0.0 | 0.0 |
| B5_FULL_UIR_OUTPUT_VALIDATION | claim_precision | 5 | 0.35 | 0.0 | 0.35 | 0.35 |
| B5_FULL_UIR_OUTPUT_VALIDATION | unsupported_claim_rate | 5 | 0.12 | 0.0005999999999999997 | 0.1 | 0.15 |
| B5_FULL_UIR_OUTPUT_VALIDATION | latency_us | 5 | 362072.5 | 111031217.86300011 | 348033.3 | 373995.05 |
| B5_FULL_UIR_OUTPUT_VALIDATION | validator_rejection_rate | 5 | 0.15 | 0.0 | 0.15 | 0.15 |

## 12. Statistical Tests

| comparison | metric | discordant | p_value | risk_difference | mean_delta | ci95_low | ci95_high |
|---|---|---|---|---|---|---|---|
| B0_DIRECT_SLM_vs_B5 | unsupported_claim_nonacceptance | 563 | 6.624337284222476e-170 | 0.563 | -1763746.31 | -1903545.661 | -1626986.976 |
| B1_SLM_WITH_PROMPT_GUARD_vs_B5 | unsupported_claim_nonacceptance | 296 | 1.5709099088952725e-89 | 0.29600000000000004 | -1288356.026 | -1428834.458 | -1153329.986 |
| B2_NAIVE_RAG_SLM_vs_B5 | unsupported_claim_nonacceptance | 415 | 2.3636425261531484e-125 | 0.41500000000000004 | -2744427.512 | -2875461.251 | -2611751.192 |
| B3_RAG_WITH_ENTITY_VALIDATION_vs_B5 | unsupported_claim_nonacceptance | 475 | 2.0501330894674953e-143 | 0.475 | -2387316.452 | -2522164.568 | -2255525.859 |
| B4_UIR_POLICY_SLM_vs_B5 | unsupported_claim_nonacceptance | 87 | 1.2924697071141057e-26 | 0.08699999999999997 | 10.059 | 9.552 | 10.596 |

## 13. Runtime Results

| pipeline | cases | mean_us | p50_us | p95_us | p99_us | prompt_eval_mean_us | generation_mean_us | validator_mean_us |
|---|---|---|---|---|---|---|---|---|
| B0_DIRECT_SLM | 1700 | 2197428.118823529 | 1938201.0 | 4298580.55 | 4939657.409999999 | 35167.29588235294 | 1081448.415882353 | 0.0 |
| B1_SLM_WITH_PROMPT_GUARD | 1500 | 1938611.0306666666 | 1733881.0 | 4005661.4 | 4480707.26 | 39097.128 | 807250.5746666667 | 0.0 |
| B2_NAIVE_RAG_SLM | 1500 | 3061403.16 | 2813513.0 | 5073617.949999999 | 5273018.67 | 83229.97 | 1861022.2886666667 | 0.0 |
| B3_RAG_WITH_ENTITY_VALIDATION | 1350 | 3188990.131851852 | 2845204.5 | 5281011.95 | 5493387.24 | 110854.17777777778 | 1978345.5792592592 | 0.0 |
| B4_UIR_POLICY_SLM | 474 | 2885335.894514768 | 2686685.0 | 5359955.85 | 5554435.79 | 99572.62025316455 | 1793313.4725738396 | 0.0 |
| B5_FULL_UIR_OUTPUT_VALIDATION | 474 | 2885348.040084388 | 2686696.5 | 5359975.1 | 5554450.52 | 99572.62025316455 | 1793313.4725738396 | 12.145569620253164 |

### Deterministic Core Stages

| stage | cases | mean_us | p50_us | p95_us | p99_us |
|---|---|---|---|---|---|
| aaco_us | 1000 | 0.218 | 0.0 | 1.0 | 1.0 |
| canonicalization_us | 1000 | 34.976 | 0.0 | 115.0 | 141.01 |
| digest_us | 1000 | 69.853 | 0.0 | 248.04999999999995 | 295.02 |
| dsl_compile_us | 1000 | 1903.94 | 14.0 | 5502.049999999999 | 6056.1 |
| executor_us | 1000 | 0.246 | 0.0 | 1.0 | 1.0 |
| output_validate_us | 1000 | 1.129 | 0.0 | 5.0 | 6.0 |
| policy_eval_us | 1000 | 22.214 | 0.0 | 76.0 | 95.08999999999992 |
| slm_us | 1000 | 0.184 | 0.0 | 1.0 | 1.0 |
| total_us | 1000 | 2058.334 | 14.0 | 6006.65 | 6602.23 |
| uir_validate_us | 1000 | 2.755 | 0.0 | 9.0 | 11.009999999999991 |

## 14. Failures / Error Taxonomy

| error_type | count |
|---|---|
| NUMERIC_ERROR | 1038 |
| POLICY_FALSE_ACCEPT | 686 |
| POLICY_FALSE_REJECT | 1227 |
| PROVENANCE_ERROR | 462 |
| SLM_FORMAT_ERROR | 940 |
| UNSUPPORTED_CLAIM | 3351 |

## 15. Generated Artifacts

All raw outputs, normalized claims, CSV summaries, manifests, and failure records are under `results/uir_slm/`.

## 16. Reproduction Commands

```bash
source ../.venv/bin/activate
cargo test --workspace --all-features
python evaluation/uir_external/validate_frozen_set.py
python evaluation/uir_slm/run_slm_campaign.py --help
python evaluation/uir_slm/aggregate_results.py --help
```

## 17. Limitations

The frozen set was programmatically curated but not manually reviewed, only one local SLM and one host were evaluated in P0, and SEC values reflect the snapshot date rather than a timeless ground truth. Two preliminary stochastic wrappers were invalidated after shell interpolation/config-path defects; their rows were excluded by run-id allowlisting, and `repeated_runs_selected.jsonl` contains only the 5 deterministic and 5 corrected stochastic runs used in variance tables.

## 18. Recommended Paper Claims

The strongest supported claim is that post-generation exact claim validation prevents acceptance of unsupported claims and deterministic UIR/policy checks prevent invalid-entity and policy-attack renderer invocation. The data does not support claiming overall task superiority: frozen semantic coverage, claim recall, and B5 outcome accuracy are low. Claims must remain limited to this model, frozen data, host, and confidence tests; do not generalize Phi-3.5 results to all SLMs or describe prompt constraints as enforcement.

## Core UIR Snapshot

| cases | structural_match | semantic_match | cle | policy_accuracy | far | frr | outcome_accuracy |
|---|---|---|---|---|---|---|---|
| 1000 | 0.372 | 0.372 | 0.375 | 0.594 | 0.0 | 0.6246153846153846 | 0.594 |
