# UIR Phase 3B Status Report

## Outcome

Publication freeze automation is implemented, but final publication evidence is correctly blocked.

## Completed

- Parser implementation remains frozen; Phase-3B changed evaluation instrumentation only.
- Candidate v2.0 preserves 1,200 cases and records pre-review pairing/policy-text corrections in an audit log.
- Independent R1/R2 sheets use only `1`, `0`, or `NA`; no judgments are prefilled.
- Field-level raw agreement and Cohen's kappa, adjudication, correction audit, dataset hashing, and freeze gates are implemented.
- Real SEC subset: 200 cases, KO/EN 100 each, hash `b66fb6fc48033b4194b57513e1b4162216516ce74cdc874953579960102b989e`.
- B0--B6 runner, B6 FILTER_AND_RENDER, final metrics/statistics, clean-run provenance, and publication report gate are implemented.

## Blocking checks

- human_review_completed
- adjudication_completed
- frozen_v2
- dataset_sha256_set
- parser_sha256_fixed
- clean_commit
- final_slm_campaign_complete
- all_primary_metrics_complete
- statistics_complete

## Required human action

Two independent reviewers must complete the review sheets without seeing each other's judgments. Disagreements and agreed-invalid ground truth fields must then be adjudicated and committed. Only after that may `review_and_freeze.py --freeze` and `run_publication_campaign.py` run.

## Integrity statement

No reviewer values, agreement scores, frozen-v2 metrics, or final SLM results were fabricated. `REPORT_PUBLICATION_READY.md` is not generated while any gate is incomplete.
