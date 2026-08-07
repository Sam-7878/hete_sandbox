#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import statistics as py_stats
from collections import defaultdict
from pathlib import Path

from paired_statistics import mcnemar_exact, paired_bootstrap_delta, percentile


def read_jsonl(path: Path) -> list[dict]: return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    fields = fields or (list(rows[0]) if rows else [])
    with path.open("w", encoding="utf-8", newline="") as handle: writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore"); writer.writeheader(); writer.writerows(rows)
def ratio(numerator: int, denominator: int) -> float: return numerator / denominator if denominator else 0.0


def summary(group: list[dict]) -> dict:
    generated = sum(row["metrics"]["generated_claims"] for row in group); supported = sum(row["metrics"]["supported_claims"] for row in group); required = sum(row["metrics"]["required_claims"] for row in group); recalled = sum(row["metrics"]["recalled_claims"] for row in group); accepted = sum(row["metrics"]["accepted_claims"] for row in group); accepted_unsupported = sum(row["metrics"]["accepted_unsupported_claims"] for row in group)
    return {"cases": len(group), "claim_precision": ratio(supported, generated), "claim_recall": ratio(recalled, required), "unsupported_claim_rate": ratio(generated - supported, generated), "unsupported_claim_acceptance_rate": ratio(accepted_unsupported, accepted), "numeric_exact_match": py_stats.fmean(row["metrics"].get("numeric_exact_match", 0.0) for row in group) if group else 0.0, "entity_accuracy": py_stats.fmean(row["metrics"].get("entity_accuracy", 0.0) for row in group) if group else 0.0, "relation_accuracy": py_stats.fmean(row["metrics"].get("relation_accuracy", 0.0) for row in group) if group else 0.0, "temporal_accuracy": py_stats.fmean(row["metrics"].get("temporal_accuracy", 0.0) for row in group) if group else 0.0, "provenance_accuracy": py_stats.fmean(row["metrics"].get("provenance_accuracy", 0.0) for row in group) if group else 0.0, "outcome_accuracy": ratio(sum(row["correct_outcome"] for row in group), len(group)), "invalid_entity_far": ratio(sum(row["category"] == "invalid_entity" and row["actual_outcome"] == "COMMIT" for row in group), sum(row["category"] == "invalid_entity" for row in group)), "attack_success_rate": ratio(sum(row["attack_success"] for row in group), sum(bool(row.get("attack_type")) for row in group)), "policy_bypass_rate": ratio(sum(row["policy_bypass"] for row in group), sum(not case_policy_valid(row) for row in group)), "entity_lock_violation_rate": ratio(sum(row["entity_lock_violation"] for row in group), len(group)), "renderer_invocation_on_reject_rate": ratio(sum(row["renderer_invocation_on_reject_path"] for row in group), sum(row["expected_outcome"] == "REJECT" for row in group))}


def case_policy_valid(row: dict) -> bool: return bool(row.get("policy_valid", True))


def classify(row: dict) -> str | None:
    if row["format_error"]: return "SLM_FORMAT_ERROR"
    if row["metrics"]["accepted_unsupported_claims"]: return "OUTPUT_CONTRACT_ESCAPE" if row["pipeline"] == "B5_FULL_UIR_OUTPUT_VALIDATION" else "UNSUPPORTED_CLAIM"
    if row["entity_lock_violation"]: return "PARSE_TARGET_ERROR"
    if row["policy_bypass"]: return "POLICY_FALSE_ACCEPT"
    if row["expected_outcome"] == "COMMIT" and row["actual_outcome"] == "REJECT": return "POLICY_FALSE_REJECT"
    if row["metrics"].get("numeric_exact_match", 1.0) < 1.0: return "NUMERIC_ERROR"
    if row["metrics"].get("provenance_accuracy", 1.0) < 1.0: return "PROVENANCE_ERROR"
    return None


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--raw", type=Path, nargs="+", required=True); parser.add_argument("--uir-records", type=Path, required=True); parser.add_argument("--frozen", type=Path, default=Path("evaluation/uir_external/frozen_test_v1.jsonl")); parser.add_argument("--out", type=Path, default=Path("results/uir_slm")); args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True); records = [row for path in args.raw for row in read_jsonl(path)]; primary = [row for row in records if row["suite"] == "frozen" and row["run_id"] == "deterministic-1"]
    outputs_path = args.out / "outputs_raw.jsonl"; outputs_path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for row in records), encoding="utf-8")
    claims = []
    for row in records:
        accepted_keys = {json.dumps(item, sort_keys=True) for item in row["accepted_claims_data"]}
        for index, claim in enumerate(row["generated_claims_data"]): claims.append({"run_id": row["run_id"], "suite": row["suite"], "case_id": row["case_id"], "pipeline": row["pipeline"], "seed": row["seed"], "claim_index": index, "claim": claim, "accepted": json.dumps(claim, sort_keys=True) in accepted_keys})
    (args.out / "claims_raw.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for row in claims), encoding="utf-8")
    baseline = []
    for pipeline in sorted({row["pipeline"] for row in primary}): baseline.append({"pipeline": pipeline, **summary([row for row in primary if row["pipeline"] == pipeline])})
    write_csv(args.out / "baseline_comparison.csv", baseline); write_csv(args.out / "groundedness_summary.csv", baseline)
    write_csv(args.out / "metric_summary.csv", [row for row in baseline if row["pipeline"] == "B5_FULL_UIR_OUTPUT_VALIDATION"])
    write_csv(args.out / "model_summary.csv", [{"model": primary[0]["model"] if primary else "", "cases": len(primary), "pipelines": len({row["pipeline"] for row in primary}), "seeds": len({row["seed"] for row in records})}])
    numeric_rows = [row for row in records if row["suite"] == "numeric" and row["run_id"] == "deterministic-1"]; numeric_summary = []
    for pipeline in sorted({row["pipeline"] for row in numeric_rows}):
        for kind in sorted({row["numeric_type"] for row in numeric_rows}):
            group = [row for row in numeric_rows if row["pipeline"] == pipeline and row["numeric_type"] == kind]
            if group: numeric_summary.append({"pipeline": pipeline, "numeric_type": kind, "cases": len(group), **{field: py_stats.fmean(row["metrics"].get(field, 0.0) for row in group) for field in ("numeric_exact_match", "unit_accuracy", "sign_accuracy", "relative_change_accuracy")}})
    write_csv(args.out / "numeric_summary.csv", numeric_summary)
    attack_rows = [row for row in records if row["suite"] == "adversarial" and row["run_id"] == "deterministic-1"]; adversarial = []
    for pipeline in sorted({row["pipeline"] for row in attack_rows}): adversarial.append({"pipeline": pipeline, **summary([row for row in attack_rows if row["pipeline"] == pipeline])})
    write_csv(args.out / "adversarial_summary.csv", adversarial)
    frozen = {row["case_id"]: row for row in read_jsonl(args.frozen)}; uir = read_jsonl(args.uir_records); generalization = []
    for split in sorted({row["split"] for row in frozen.values()}):
        for language in ("ko", "en"):
            group = [row for row in uir if frozen[row["case_id"]]["split"] == split and frozen[row["case_id"]]["language"] == language]; generalization.append({"split": split, "language": language, "cases": len(group), "semantic_match": ratio(sum(row["semantic_match"] for row in group), len(group)), "policy_accuracy": ratio(sum(row["expected_policy_decision"] == row["actual_policy_decision"] for row in group), len(group)), "outcome_accuracy": ratio(sum(row["correct"] for row in group), len(group))})
    write_csv(args.out / "generalization_split_summary.csv", generalization)
    latency_rows = []
    for pipeline in sorted({row["pipeline"] for row in records}):
        group = [row for row in records if row["pipeline"] == pipeline and row["renderer_invoked"]]; values = [row["latency"]["pipeline_total_us"] for row in group]
        latency_rows.append({"pipeline": pipeline, "cases": len(group), "mean_us": py_stats.fmean(values) if values else 0.0, "p50_us": percentile(values, .5), "p95_us": percentile(values, .95), "prompt_eval_mean_us": py_stats.fmean(row["latency"]["prompt_eval_us"] for row in group) if group else 0.0, "generation_mean_us": py_stats.fmean(row["latency"]["generation_us"] for row in group) if group else 0.0, "validator_mean_us": py_stats.fmean(row["latency"]["validator_us"] for row in group) if group else 0.0})
    write_csv(args.out / "latency_summary.csv", latency_rows)
    by_pipeline = {pipeline: {row["case_id"]: row for row in primary if row["pipeline"] == pipeline} for pipeline in {row["pipeline"] for row in primary}}; proposed = by_pipeline.get("B5_FULL_UIR_OUTPUT_VALIDATION", {}); tests = []
    for pipeline, cases in sorted(by_pipeline.items()):
        if pipeline == "B5_FULL_UIR_OUTPUT_VALIDATION": continue
        common = sorted(set(cases) & set(proposed)); left = [not bool(cases[key]["metrics"]["accepted_unsupported_claims"]) for key in common]; right = [not bool(proposed[key]["metrics"]["accepted_unsupported_claims"]) for key in common]; test = mcnemar_exact(left, right); latency = paired_bootstrap_delta([cases[key]["latency"]["pipeline_total_us"] for key in common], [proposed[key]["latency"]["pipeline_total_us"] for key in common]); tests.append({"comparison": f"{pipeline}_vs_B5", "metric": "unsupported_claim_nonacceptance", **test, **latency, "risk_difference": ratio(sum(right), len(right)) - ratio(sum(left), len(left))})
    write_csv(args.out / "statistical_tests.csv", tests)
    failures = []
    for row in records:
        taxonomy = classify(row)
        if taxonomy: failures.append({"error_type": taxonomy, **row})
    (args.out / "failures.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for row in failures), encoding="utf-8")
    print(json.dumps({"records": len(records), "primary": len(primary), "claims": len(claims), "failures": len(failures)}, sort_keys=True))


if __name__ == "__main__": main()
