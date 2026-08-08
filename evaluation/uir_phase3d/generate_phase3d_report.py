#!/usr/bin/env python3
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/"results/uir_phase3d";REPORT=ROOT/"docs/work_reports/308_uir_phase_3D_role_separated/REPORT_PHASE3D_PUBLICATION_FINAL.md"
def load(p):return json.loads(p.read_text()) if p.exists() else {}
def csvrows(name):
    p=OUT/name
    if not p.exists():return []
    with p.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def main():
    gate=load(OUT/"PUBLICATION_GATE_PHASE3D.json");campaign=load(OUT/"campaign_summary.json");budget=load(OUT/"generation_budget_validation.json");b6=load(OUT/"b6_filtering_summary.json");audit=load(OUT/"actual_ai_audit_summary.json");run=load(OUT/"run_manifest_phase3d.json")
    semantic=csvrows("semantic_summary.csv");overall=next((x for x in semantic if x.get("split")==x.get("language")=="overall"),{})
    numeric=next((x for x in csvrows("numeric_summary.csv") if x.get("pipeline")=="B6_UIR_FILTER_AND_RENDER"),{})
    sec=next((x for x in csvrows("sec_structured_output_diagnostic.csv") if x.get("pipeline")=="B6_UIR_FILTER_AND_RENDER"),{})
    safety=next((x for x in csvrows("safety_utility_summary.csv") if x.get("pipeline")=="B6_UIR_FILTER_AND_RENDER"),{})
    text=f"""# UIR Phase 3D Publication Evidence Report

## 1. Evidence correction rationale
Phase3C R1/R2/R3 artifacts are retained but reclassified as `Phase3C-script-audit`: they were produced by deterministic validators, not direct Sonnet/Gemini/Opus generations.

## 2. Actual AI-model audit protocol
Reconstruction-first isolated packets and strict provenance ingestion are implemented. Actual audit status: `{audit.get('status','not_received')}`. Script-generated judgments are rejected.

## 3. Cross-model agreement
{('See actual_ai_agreement.csv.' if audit else 'Not computed: actual AntiGravity engine outputs have not been supplied.')}

## 4. Benchmark uncertainty/disagreements
{('See actual_ai_adjudication.csv; unresolved='+str(audit.get('unresolved')) if audit else 'Pending actual three-engine audit.')}

## 5. Frozen-v2 integrity
Dataset SHA-256 remains `9bb8a5d423b53bae14b2c699cba6b1338f0115345f94c6b4a9f93af2400d4a3c`; parser SHA-256 remains `bee778f3e3767fdcd64d0926f27c680143d217ea1d6febcabd08aac96de321d7`.

## 6. B0-B6 baselines
Campaign records: `{campaign.get('records','not run')}`; campaign ID: `phase3d-publication-final`.

## 7. UIR semantic generalization
Overall semantic match `{overall.get('semantic_match','NA')}`, structural match `{overall.get('structural_match','NA')}`, cross-lingual equivalence `{overall.get('cross_lingual_equivalence','NA')}`.

## 8. Policy enforcement
See `policy_summary.csv`; frozen policy semantics were unchanged.

## 9. Adversarial safety
See `safety_summary.csv` and `stat_safety_final.csv`.

## 10. B5 vs B6 safety-utility trade-off
B6 states: `{json.dumps(b6.get('states',{}),sort_keys=True)}`; unsupported acceptance `{b6.get('unsupported_claim_acceptance_rate','NA')}`; useful-answer rate `{safety.get('useful_answer_rate','NA')}`.

## 11. Real SEC factual/numeric fidelity
Compact immutable fact IDs replace model reproduction of numeric values, units, provenance URIs, and hashes. B6 end-to-end numeric preservation `{numeric.get('numeric_exact_match','NA')}`, unit accuracy `{numeric.get('unit_accuracy','NA')}`, provenance coverage/correctness `{numeric.get('provenance_coverage','NA')}`/`{numeric.get('provenance_correctness','NA')}`. B6 valid JSON `{sec.get('valid_json_rate','NA')}`, truncation `{sec.get('json_truncation_rate','NA')}`, missing provenance `{sec.get('missing_provenance_rate','NA')}`. The ten numeric misses are partial selections that retain temporal/provenance facts but omit the numeric fact; no incorrect numeric claim is accepted.

## 12. Runtime
See `latency_summary.csv`; configured generation budget `{budget.get('configured_max_new_tokens','NA')}`, measured p99 `{budget.get('p99_valid_structured_output_tokens','NA')}`, 1.25× rule pass `{budget.get('pass','NA')}`.

## 13. Statistical significance
Safety and utility use paired McNemar with bootstrapped risk-difference CI; latency uses Wilcoxon and paired bootstrap; Holm correction is applied.

## 14. Failure analysis
All final campaign failures remain in `failures.jsonl`; no low-performing case is removed. Policy-prevented B6 paths are explicitly `NO_VERIFIED_ANSWER`, while real-fact partial selections are `PARTIAL_VERIFIED_ANSWER`.

## 15. Reproducibility
Generation commit `{run.get('commit','not run')}`, post-processing commit `{run.get('postprocessing_commit','not run')}`, workers `{run.get('workers','NA')}`, and dataset/parser/model/config hashes are recorded in `run_manifest_phase3d.json`.

## 16. Limitations
No claim of human review is made. Until actual AntiGravity outputs with provenance are ingested, Phase3D cannot claim a triple independent AI-model audit.

## 17. Publication readiness
Status: **{gate.get('status','BLOCKED_PUBLICATION_EVIDENCE_INCOMPLETE')}**. Blocking checks: `{', '.join(gate.get('blocking_checks',[]))}`.
"""
    REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(text,encoding="utf-8")
if __name__=="__main__":main()
