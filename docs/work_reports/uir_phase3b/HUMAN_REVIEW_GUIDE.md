# Phase 3B Human Review Guide

## Review inputs

- `evaluation/uir_phase3b/review/review_R1.csv`
- `evaluation/uir_phase3b/review/review_R2.csv`
- `evaluation/uir_phase3b/review/adjudication.csv`

R1 and R2 must work independently and must not inspect the other reviewer's sheet before both reviews are complete. Reviewer IDs are anonymous; no personal data should be added.

Each of the eight `*_valid` fields accepts only:

- `1`: valid/correct
- `0`: invalid/incorrect
- `NA`: not applicable

Notes are optional during independent review. Judgments are intentionally blank in the committed templates.

## Coverage

Full dual review of all 1,200 cases is preferred. The enforced minimum is 400 dual-reviewed cases, at least 30 from every category, with each language representing at least 45% of the reviewed sample.

## Adjudication

Every disagreement requires an `adjudication.csv` row. A field that both reviewers mark `0` also requires adjudication because the ground truth must be corrected rather than silently retained or the case deleted.

Required columns include both reviewer values, final validity, reason, serialized original value, and serialized adjudicated value. Corrections are applied field-by-field; no case deletion is supported.

## Freeze and final campaign

After reviews and adjudication are complete:

1. Commit the completed review evidence so the worktree is clean.
2. Run `python evaluation/uir_phase3b/review_and_freeze.py --freeze` in Ubuntu 24.04 with `.venv` activated.
3. Verify `results/uir_phase3b/FROZEN_TEST_V2_MANIFEST.json` and commit/hash identity.
4. Run `python evaluation/uir_phase3b/run_publication_campaign.py` from the same clean commit.

The final runner refuses to invoke Ollama unless human review, adjudication, frozen dataset hash, parser hash, real SEC subset, and clean-commit gates all pass.
