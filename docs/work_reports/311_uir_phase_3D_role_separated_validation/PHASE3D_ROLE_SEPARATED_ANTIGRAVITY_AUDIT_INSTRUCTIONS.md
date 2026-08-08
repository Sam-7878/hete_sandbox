# Phase UIR-3D Role-Separated Audit Instructions
## Codex + AntiGravity Gemini 3.5 Flash + Gemini 3.6 Flash + Gemini 3.1 Pro

### Target Paper
**A Universal Intermediate Representation for Policy-Constrained Multilingual Small Language Model Agents**

---

## 0. Goal

The local Phase 3D SLM campaign is already complete. The remaining publication blockers are the actual multi-model audit, model-review provenance, and valid agreement statistics.

Roles are separated as follows:

- **Codex**: packet preparation/validation, ingestion, agreement/statistics, publication gate, final report
- **AI-R1 / AntiGravity Gemini 3.5 Flash**: actual independent model audit
- **AI-R2 / AntiGravity Gemini 3.6 Flash**: actual independent model audit
- **AI-R3 / AntiGravity Gemini 3.1 Pro**: actual independent model audit

Codex must never generate reviewer judgments.

---

## 1. Shared Inputs

Repository root:

```text
hete_sandbox/
```

Audit packets:

```text
evaluation/uir_phase3d/audit_packets/audit_input_AI-R1.jsonl
evaluation/uir_phase3d/audit_packets/audit_input_AI-R2.jsonl
evaluation/uir_phase3d/audit_packets/audit_input_AI-R3.jsonl
```

Prompt-template SHA-256:

```text
1660e3f70d9c11b0b415a7adb3c4bcc01dd1b8c9576af19c8881335336198310
```

Shared frozen cases:

```text
1,200
```

Frozen-v2 SHA-256:

```text
9bb8a5d423b53bae14b2c699cba6b1338f0115345f94c6b4a9f93af2400d4a3c
```

Parser SHA-256:

```text
bee778f3e3767fdcd64d0926f27c680143d217ea1d6febcabd08aac96de321d7
```

---

## 2. Execution Order

```text
STEP 1  Codex prepares and validates the three audit packets
STEP 2  User runs AntiGravity Gemini 3.5 Flash as AI-R1
STEP 3  User runs AntiGravity Gemini 3.6 Flash as AI-R2
STEP 4  User runs AntiGravity Gemini 3.1 Pro as AI-R3
STEP 5  User returns the three captured JSONL files to Codex
STEP 6  Codex validates provenance/schema/coverage
STEP 7  Codex runs ingest_actual_ai_reviews.py
STEP 8  Codex computes agreement/adjudication/statistics
STEP 9  Codex runs publication_gate_phase3d.py
STEP 10 Codex regenerates REPORT_PHASE3D_PUBLICATION_FINAL.md
STEP 11 Confirm READY_FOR_MANUSCRIPT_DRAFT or repository-equivalent status
```

---

# ROLE A — CODEX: PRE-AUDIT PREPARATION

## A1. Repository integrity

Run:

```bash
cd /mnt/d/_Work/goat_bank/hete_sandbox
source ../.venv/bin/activate
git status
```

Record commit and clean/dirty status.

## A2. Validate packets

Check all three packet files:

```text
AI-R1 = 1,200 cases
AI-R2 = 1,200 cases
AI-R3 = 1,200 cases
```

Verify:

- identical case-ID sets
- no duplicate case IDs
- fixed prompt-template hash
- same frozen-v2 identity
- no other-reviewer judgments
- no parser outputs
- no B0-B6 scores
- no agreement statistics

## A3. Handoff to user

Codex reports only:

```text
AI-R1 packet ready
AI-R2 packet ready
AI-R3 packet ready
1,200 cases each
prompt-template hash verified
frozen-v2 integrity verified
```

---

# ROLE B — AI-R1: ANTIGRAVITY Jemini 3.5 Flash

## B1. Start a fresh isolated session

In AntiGravity:

```text
New session
Engine: Gemini 3.5 Flash
```

Do not reuse a session containing HETE results, parser outputs, or other reviewer outputs.

## B2. Input

Use only:

```text
evaluation/uir_phase3d/audit_packets/audit_input_AI-R1.jsonl
```

## B3. Reviewer instruction

Use the following instruction in the Gemini 3.5 Flash session:

```text
You are AI-R1, an independent benchmark auditor.

Engine identity:
Google AntiGravity — Gemini 3.5 Flash

You are evaluating a frozen multilingual UIR benchmark.

For every case:

1. Read the source text independently.
2. Do NOT trust the candidate annotation by default.
3. Before comparing with the candidate, reconstruct:
   - intent
   - target
   - conditions
   - policy decision
   - expected outcome
   - required claims
4. Compare your independent reconstruction with the candidate annotation.
5. Judge these fields independently:
   - source_text_valid
   - language_valid
   - intent_valid
   - target_valid
   - conditions_valid
   - policy_valid
   - outcome_valid
   - claims_valid
6. Allowed values are only: 1, 0, or NA.
7. Return structured judgment plus a concise rationale.
8. Do not output hidden chain-of-thought.
9. Do not reference other reviewers or system performance.
10. Do not optimize your judgments to agree with an expected publication result.

Your output is an independent model judgment.
```

## B4. Output

Save/capture as:

```text
actual_ai_review_R1.jsonl
```

Each row must ultimately identify:

```text
reviewer_id = AI-R1
engine = AntiGravity Gemini 3.5 Flash
annotation_method = actual_model_generation
```

The capture wrapper—not the model—must calculate `raw_response_sha256`.

## B5. Completion criteria

- 1,200 unique case IDs
- no missing cases
- actual Gemini 3.5 Flash model generation
- provenance recorded
- no R2/R3 visibility

Then terminate the session.

---

# ROLE C — AI-R2: ANTIGRAVITY GEMINI 3.6 FLASH

## C1. Start a different fresh session

```text
New session
Engine: Gemini 3.6 Flash
```

Do not show the Jemini 3.5 Flash output.

## C2. Input

Use only:

```text
evaluation/uir_phase3d/audit_packets/audit_input_AI-R2.jsonl
```

## C3. Reviewer instruction

```text
You are AI-R2, an independent benchmark auditor.

Engine identity:
Google AntiGravity — Gemini 3.6 Flash

For every benchmark case:

1. Interpret the source text independently.
2. Ignore the candidate annotation during your initial semantic reconstruction.
3. Reconstruct:
   - intent
   - target
   - conditions
   - policy decision
   - expected outcome
   - required claims
4. Compare your reconstruction with the candidate annotation.
5. Judge:
   - source_text_valid
   - language_valid
   - intent_valid
   - target_valid
   - conditions_valid
   - policy_valid
   - outcome_valid
   - claims_valid
6. Use only 1, 0, or NA.
7. Return structured output and a short rationale.
8. Do not expose hidden chain-of-thought.
9. Do not use Jemini 3.5 Flash/Gemini 3.1 Pro judgments, parser outputs, benchmark scores, or publication targets.
10. Do not attempt to maximize agreement.

Your task is independent semantic validation, not confirmation.
```

## C4. Output

```text
actual_ai_review_R2.jsonl
```

Required identity:

```text
reviewer_id = AI-R2
engine = AntiGravity Gemini 3.6 Flash
annotation_method = actual_model_generation
```

## C5. Completion criteria

- 1,200 unique cases
- no missing cases
- provenance complete
- no R1/R3 contamination

Then terminate the session.

---

# ROLE D — AI-R3: ANTIGRAVITY Gemini 3.1 Pro

## D1. Start a third fresh session

```text
New session
Engine: Gemini 3.1 Pro
```

Do not expose R1 or R2 outputs or their agreement.

## D2. Input

Use only:

```text
evaluation/uir_phase3d/audit_packets/audit_input_AI-R3.jsonl
```

## D3. Reviewer instruction

```text
You are AI-R3, the third independent benchmark auditor.

Engine identity:
Google AntiGravity — Gemini 3.1 Pro

Perform a reconstruction-first audit.

For every case:

1. Initially ignore the candidate annotation.
2. Reconstruct from source text:
   - language interpretation
   - intent
   - target
   - conditions
   - policy decision
   - expected outcome
   - required claims
3. Only then compare your reconstruction with the candidate annotation.
4. Judge:
   - source_text_valid
   - language_valid
   - intent_valid
   - target_valid
   - conditions_valid
   - policy_valid
   - outcome_valid
   - claims_valid
5. Use only 1, 0, or NA.
6. Return structured output and a concise rationale.
7. Do not output hidden chain-of-thought.
8. Do not act as a tie-breaker using other reviewers; you do not have access to them.
9. Do not use parser/system performance as evidence.

Your output must represent your own independent model judgment.
```

## D4. Output

```text
actual_ai_review_R3.jsonl
```

Required identity:

```text
reviewer_id = AI-R3
engine = AntiGravity Gemini 3.1 Pro
annotation_method = actual_model_generation
```

## D5. Completion criteria

- 1,200 unique cases
- actual Gemini 3.1 Pro generation
- provenance complete
- no R1/R2 visibility

Then terminate the session.

---

# ROLE E — USER HANDOFF TO CODEX

After completing all three AntiGravity sessions, provide Codex with:

```text
actual_ai_review_R1.jsonl
actual_ai_review_R2.jsonl
actual_ai_review_R3.jsonl
```

Do not manually merge or edit judgments unless required to repair transport-format corruption. Any such repair must be logged.

---

# ROLE F — CODEX: PRE-INGESTION VALIDATION

Codex checks:

## Coverage

```text
R1 = 1,200
R2 = 1,200
R3 = 1,200
```

## Identity

```text
AI-R1 / AntiGravity Gemini 3.5 Flash
AI-R2 / AntiGravity Gemini 3.6 Flash
AI-R3 / AntiGravity Gemini 3.1 Pro
```

## Provenance per row

Must include:

```text
session_run_id
timestamp
generation_interface
raw_response_sha256
temperature = not_exposed_by_antigravity_cli
annotation_method = actual_model_generation
```

## Integrity

- no duplicate case ID
- no unknown case ID
- no missing case ID
- valid judgment schema
- prompt-template hash matches
- no script-generated annotation substituted for model output

If validation fails, Codex must stop and report the exact failed rows. It must not auto-fill judgments.

---

# ROLE G — CODEX: INGESTION

Run:

```bash
source ../.venv/bin/activate

python evaluation/uir_phase3d/ingest_actual_ai_reviews.py   --air1 /path/to/actual_ai_review_R1.jsonl   --air2 /path/to/actual_ai_review_R2.jsonl   --air3 /path/to/actual_ai_review_R3.jsonl
```

The ingestion should generate:

- pairwise raw agreement
- Cohen's kappa where defined
- three-way raw agreement
- Fleiss' kappa where defined
- disagreement records
- majority/unresolved adjudication evidence

---

# ROLE H — CODEX: AGREEMENT / ADJUDICATION CHECK

For single-class marginals:

```text
kappa = NA
reason = zero_marginal_variance
```

Never force kappa to 1.0.

Report disagreement patterns:

```text
R1 == R2 != R3
R1 == R3 != R2
R2 == R3 != R1
all three disagree
```

Unresolved cases must remain visible.

---

# ROLE I — CODEX: PUBLICATION GATE

Run:

```bash
python evaluation/uir_phase3d/publication_gate_phase3d.py
```

Required final checks:

```text
actual_multi_model_audit_complete
model_review_provenance_recorded
agreement_statistics_valid
frozen_v2_integrity_verified
SEC_truncation_fixed
real_fact_campaign_complete
B6_filtering_verified
B0_B6_final_campaign_complete
final_statistics_complete
```

Expected final state:

```text
READY_FOR_MANUSCRIPT_DRAFT
```

or repository-equivalent publication-ready status.

---

# ROLE J — CODEX: FINAL REPORT

Run:

```bash
python evaluation/uir_phase3d/generate_phase3d_report.py
```

Output:

```text
REPORT_PHASE3D_PUBLICATION_FINAL.md
```

The report must include:

1. actual three-engine audit provenance
2. reviewer coverage
3. pairwise agreement
4. Fleiss' kappa where defined
5. disagreement analysis
6. frozen-v2 integrity
7. UIR semantic generalization
8. policy enforcement
9. B0-B6 comparison
10. adversarial safety
11. B5 vs B6 safety–utility result
12. SEC numeric preservation
13. provenance preservation
14. runtime
15. statistical significance
16. limitations
17. final publication readiness

---

# 3-Model Independence Rules

Never provide any AntiGravity reviewer with:

- another reviewer's output
- current agreement score
- parser predictions
- B0-B6 results
- semantic-match score
- policy score
- desired publication outcome

Never allow Codex to:

- create reviewer judgments
- fill missing judgments
- edit disagreement cases to improve agreement
- forge engine metadata
- label script validation as actual model generation

---

# Paper Terminology After Successful Gate

If the three actual model audits are successfully ingested, the manuscript may say:

> The frozen benchmark was independently audited by three model engines—Gemini 3.5 Flash, Gemini 3.6 Flash, and Gemini 3.1 Pro—under isolated review contexts. Agreement statistics were computed only after all model outputs had been captured and provenance-validated.

It must also state:

> The benchmark was validated by AI models rather than human annotators; cross-model agreement measures annotation consistency across model engines and does not constitute human ground-truth validation.

---

# Stop Rule

Once the gate reports:

```text
READY_FOR_MANUSCRIPT_DRAFT
```

stop architecture development and benchmark tuning.

Proceed directly to:

```text
SCI manuscript preview (.md)
→ user review
→ section-by-section LaTeX drafting
```
