#!/usr/bin/env python3
"""Execute real Phi-3.5 B0--B5 campaigns with resumable JSONL evidence."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from baselines import PIPELINES, build_request
from claim_metrics import evaluate_claims, numeric_dimensions, parse_output, validate_against_facts
from ollama_client import OllamaClient

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "uir_external"))
from registry_adapter import FrozenRegistry


def read_jsonl(path: Path | None) -> list[dict]:
    if path is None or not path.exists(): return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--dataset", type=Path, required=True); parser.add_argument("--suite", choices=("frozen", "numeric", "adversarial"), required=True); parser.add_argument("--registry", type=Path, default=Path("evaluation/uir_external/registry_v1.jsonl")); parser.add_argument("--uir-records", type=Path); parser.add_argument("--config", type=Path, default=Path("evaluation/uir_slm/model_config/phi35_ollama.json")); parser.add_argument("--out", type=Path, required=True); parser.add_argument("--pipelines", nargs="+", choices=PIPELINES, default=PIPELINES); parser.add_argument("--seed", type=int, default=20260807); parser.add_argument("--temperature", type=float); parser.add_argument("--run-id", default="deterministic-1"); parser.add_argument("--limit", type=int); parser.add_argument("--no-resume", action="store_true"); args = parser.parse_args()
    cases = read_jsonl(args.dataset); cases = cases[:args.limit] if args.limit else cases; registry = FrozenRegistry(args.registry); uir = {row["case_id"]: row for row in read_jsonl(args.uir_records)}; client = OllamaClient(args.config); config = client.config["deterministic"].copy(); config["seed"] = args.seed
    if args.temperature is not None: config["temperature"] = args.temperature
    args.out.parent.mkdir(parents=True, exist_ok=True); existing = [] if args.no_resume else read_jsonl(args.out); index = {(row["run_id"], row["case_id"], row["pipeline"], row["seed"]): row for row in existing}; pending = sum((args.run_id, case["case_id"], pipeline, args.seed) not in index for case in cases for pipeline in args.pipelines)
    print(json.dumps({"suite": args.suite, "cases": len(cases), "pipelines": args.pipelines, "pending": pending, "resume_rows": len(existing)}, sort_keys=True), flush=True)
    mode = "a" if existing and not args.no_resume else "w"; completed = 0; started_campaign = time.monotonic()
    with args.out.open(mode, encoding="utf-8", newline="\n") as handle:
        for case in cases:
            for pipeline in args.pipelines:
                key = (args.run_id, case["case_id"], pipeline, args.seed)
                if key in index: continue
                request = build_request(pipeline, case, registry, uir.get(case["case_id"])); reused = False
                if not request.invoke_renderer:
                    raw_text = ""; generated = []; answer = ""; format_error = None; latency = {"total_us": 0, "prompt_eval_us": 0, "generation_us": 0, "load_us": 0, "prompt_tokens": 0, "output_tokens": 0}; actual_outcome = "REJECT"
                else:
                    b4_key = (args.run_id, case["case_id"], "B4_UIR_POLICY_SLM", args.seed)
                    if pipeline == "B5_FULL_UIR_OUTPUT_VALIDATION" and b4_key in index:
                        source = index[b4_key]; raw_text = source["raw_output"]; answer = source["answer"]; generated = source["generated_claims_data"]; format_error = source["format_error"]; latency = source["latency"].copy(); reused = True
                    else:
                        result = client.generate(request.prompt, request.system, config); raw_text = result.text; answer, generated, format_error = parse_output(raw_text); latency = {"total_us": result.latency_us, "prompt_eval_us": result.prompt_eval_us, "generation_us": result.generation_us, "load_us": result.load_us, "prompt_tokens": result.prompt_tokens, "output_tokens": result.output_tokens}
                    actual_outcome = "ABORT" if format_error else "COMMIT"
                expected = case.get("expected_claims", []); validator_started = time.perf_counter_ns(); supported, rejected = validate_against_facts(generated, expected); validator_us = (time.perf_counter_ns() - validator_started) // 1000
                latency["validator_us"] = validator_us if pipeline == "B5_FULL_UIR_OUTPUT_VALIDATION" else 0
                latency["pipeline_total_us"] = latency["total_us"] + latency["validator_us"]
                accepted = generated
                output_validation = "not_applied"
                if pipeline == "B5_FULL_UIR_OUTPUT_VALIDATION" and request.invoke_renderer:
                    output_validation = "rejected" if rejected or format_error else "accepted"; accepted = [] if rejected or format_error else supported; actual_outcome = "REJECT" if rejected or format_error else "COMMIT"
                metrics = evaluate_claims(expected, generated, accepted); numeric = numeric_dimensions(expected, generated) if args.suite == "numeric" else {}
                target = (case.get("expected_semantics") or {}).get("target")
                entity_lock_violation = any(target and claim.get("entity_id") != target for claim in accepted)
                expected_outcome = case.get("expected_outcome", "REJECT")
                record = {"run_id": args.run_id, "suite": args.suite, "case_id": case["case_id"], "pipeline": pipeline, "model": client.config["model"], "seed": args.seed, "temperature": config["temperature"], "language": case.get("language"), "category": case.get("category"), "split": case.get("split"), "attack_type": case.get("attack_type"), "numeric_type": case.get("numeric_type"), "expected_outcome": expected_outcome, "policy_valid": case.get("policy_valid", True), "entity_valid": case.get("entity_valid", False), "actual_outcome": actual_outcome, "correct_outcome": actual_outcome == expected_outcome, "renderer_invoked": request.invoke_renderer, "renderer_reused": reused, "rejection_reason": request.rejection_reason, "output_validation": output_validation, "raw_output": raw_text, "answer": answer, "generated_claims_data": generated, "accepted_claims_data": accepted, "format_error": format_error, "latency": latency, "metrics": {**metrics, **numeric}, "attack_success": expected_outcome == "REJECT" and bool(accepted), "policy_bypass": not case.get("policy_valid", True) and request.invoke_renderer, "entity_lock_violation": entity_lock_violation, "renderer_invocation_on_reject_path": pipeline in {"B4_UIR_POLICY_SLM", "B5_FULL_UIR_OUTPUT_VALIDATION"} and expected_outcome == "REJECT" and request.invoke_renderer}
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"); handle.flush(); index[key] = record; completed += 1
                if completed % 50 == 0: print(json.dumps({"completed": completed, "pending": pending - completed, "elapsed_s": round(time.monotonic() - started_campaign, 1)}, sort_keys=True), flush=True)
    print(json.dumps({"status": "complete", "new_rows": completed, "total_rows": len(index), "out": str(args.out)}, sort_keys=True), flush=True)


if __name__ == "__main__": main()
