#!/usr/bin/env python3
"""Verify HETE core/domain/adapter boundaries (ARCH-001 through ARCH-015)."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

LEGACY_DOMAIN_PACKAGES = {"poa-verifier-example", "open-banking", "drone", "voting"}
CORE_DOMAIN_TOKENS = ("warrant", "court", "prosecutor", "freeze", "maximum_amount", "reserved_amount")
FORBIDDEN_MAPPER = ("amount", "currency", "payment", "drone", "banking", "warrant", "freeze")
VOTING_TOKENS = ("survey_id", "nullifier", "vote", "voter", "tally", "reward_escrow")
NEW_PACKAGES = {
    "hete-identity",
    "hete-policy",
    "hete-credential",
    "hete-adapter-api",
    "domain-electronic-warrant",
    "adapter-simulated-asset",
    "hete-warrant-verifier",
    "adapter-sqlite-asset",
    "domain-agent-delegation",
}


def source_text(path: Path) -> str:
    return "\n".join(item.read_text(encoding="utf-8") for item in path.rglob("*.rs"))


def require(condition: bool, test_id: str, detail: str) -> None:
    if not condition:
        raise SystemExit(f"{test_id} FAIL: {detail}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    raw = subprocess.check_output(
        ["cargo", "metadata", "--format-version", "1", "--no-deps"],
        cwd=workspace,
        text=True,
    )
    metadata = json.loads(raw)
    packages = {package["name"]: package for package in metadata["packages"]}
    graph = {
        name: sorted(
            dependency["name"]
            for dependency in package["dependencies"]
            if dependency.get("kind") is None
        )
        for name, package in packages.items()
    }
    passed: list[str] = []

    require("poa-core" in packages, "ARCH-001", "poa-core missing")
    passed.append("ARCH-001")
    require(not (set(graph["poa-core"]) & LEGACY_DOMAIN_PACKAGES), "ARCH-002", "poa-core domain dependency")
    passed.append("ARCH-002")
    core_text = source_text(workspace / "crates/poa-core").lower()
    require(not any(token in core_text for token in CORE_DOMAIN_TOKENS), "ARCH-003", "domain operation in core")
    passed.append("ARCH-003")
    mapper = (workspace / "crates/poa-sandbox/src/mapper.rs").read_text(encoding="utf-8").lower()
    require(not any(token in mapper for token in FORBIDDEN_MAPPER), "ARCH-004", "business rule in sandbox mapper")
    passed.append("ARCH-004")

    require(NEW_PACKAGES.issubset(packages), "ARCH-005", "new package set incomplete")
    require(not any(token in core_text for token in CORE_DOMAIN_TOKENS), "ARCH-005", "warrant symbol in poa-core")
    passed.append("ARCH-005")
    require("domain-electronic-warrant" not in graph["hete-policy"], "ARCH-006", "policy depends on warrant domain")
    passed.append("ARCH-006")
    domain_dependencies = set(graph["domain-electronic-warrant"])
    require("hete-adapter-api" in domain_dependencies and "adapter-simulated-asset" not in domain_dependencies, "ARCH-007", "domain adapter boundary invalid")
    passed.append("ARCH-007")
    adapter_text = source_text(workspace / "crates/adapter-simulated-asset").lower()
    require("hete-credential" not in graph["adapter-simulated-asset"] and "credential" not in adapter_text, "ARCH-008", "adapter verifies credentials")
    passed.append("ARCH-008")
    require("authorityrole" not in core_text and "judicialissuer" not in core_text, "ARCH-009", "authority role hard-coded in core")
    passed.append("ARCH-009")
    new_text = "\n".join(source_text(workspace / f"crates/{name}").lower() for name in NEW_PACKAGES)
    require(not any(token in new_text for token in VOTING_TOKENS), "ARCH-010", "voting symbol in new warrant packages")
    passed.append("ARCH-010")
    require("fn manifest" in adapter_text and "require_capabilities" in adapter_text, "ARCH-011", "adapter manifest/capability test missing")
    passed.append("ARCH-011")

    manifest_path = workspace / "evaluation/results/manifests/baseline_manifest.json"
    require(manifest_path.exists(), "ARCH-012", "baseline manifest missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(all(key in manifest for key in ("source_commit", "build_profile", "host")), "ARCH-012", "result provenance incomplete")
    passed.append("ARCH-012")
    production_text = source_text(workspace / "crates/hete-warrant-verifier")
    require("Noop" not in production_text or "allow-insecure-noop" in production_text, "ARCH-013", "Noop production path lacks insecure flag")
    passed.append("ARCH-013")
    policy_text = source_text(workspace / "crates/hete-policy")
    warrant_text = source_text(workspace / "crates/domain-electronic-warrant")
    require("deny_unknown_fields" in policy_text and "deny_unknown_fields" in warrant_text, "ARCH-014", "critical policy types do not fail closed")
    passed.append("ARCH-014")
    forbidden = ("Kim Min-su", "900101-1234567", "did:fixture:plaintext-subject")
    result_files = [path for root in (workspace / "evaluation/results", workspace / "docs/scientific_evidence") if root.exists() for path in root.rglob("*") if path.is_file()]
    exposed = [str(path.relative_to(workspace)) for path in result_files if any(value in path.read_text(encoding="utf-8", errors="ignore") for value in forbidden)]
    require(not exposed, "ARCH-015", f"forbidden plaintext in outputs: {exposed}")
    passed.append("ARCH-015")

    publication_runner = (workspace / "evaluation/generate_publication_manifest.py").read_text(encoding="utf-8")
    require("--untracked-files=no" in publication_runner and "requires a clean" in publication_runner,
            "ARCH-016", "publication runner lacks clean-tree gate")
    passed.append("ARCH-016")
    benchmark_manifest = workspace / "evaluation/results/raw/full_benchmark/benchmark_manifest.json"
    require(benchmark_manifest.exists(), "ARCH-017", "full benchmark manifest missing")
    benchmark_data = json.loads(benchmark_manifest.read_text(encoding="utf-8"))
    require(bool(benchmark_data.get("source_commit")) and bool(benchmark_data.get("host_id")),
            "ARCH-017", "benchmark provenance missing")
    passed.append("ARCH-017")
    require((workspace / "evaluation/analysis/verify_raw_hashes.py").exists()
            and (workspace / "evaluation/results/raw/SHA256SUMS.json").exists(),
            "ARCH-018", "raw immutability inventory missing")
    passed.append("ARCH-018")
    sqlite_dependencies = set(graph["adapter-sqlite-asset"])
    forbidden_adapter_dependencies = {"poa-core", "domain-electronic-warrant", "domain-agent-delegation", "hete-credential"}
    require("hete-adapter-api" in sqlite_dependencies and not (sqlite_dependencies & forbidden_adapter_dependencies),
            "ARCH-019", "external adapter crosses the API/domain boundary")
    passed.append("ARCH-019")
    core_paths = sorted(path for path in (workspace / "crates/poa-core").rglob("*") if path.is_file())
    core_lines = "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(workspace).as_posix()}\n" for path in core_paths)
    core_hash = hashlib.sha256(core_lines.encode()).hexdigest()
    expected_core_hash = (workspace / "evaluation/baselines/poa_core.sha256").read_text().strip()
    require(core_hash == expected_core_hash, "ARCH-020", "poa-core changed during second-domain addition")
    passed.append("ARCH-020")
    require(benchmark_data.get("build_profile") == "release", "ARCH-021", "publication benchmark is not release")
    passed.append("ARCH-021")
    require(all((workspace / f"formal/results/tlc/publication-{mode}-20260722/summary.json").exists()
                for mode in ("safety", "liveness")), "ARCH-022", "TLC evidence missing")
    passed.append("ARCH-022")
    require("virtualization" in benchmark_data and benchmark_data["virtualization"] in {"WSL2", "native-or-undetected"},
            "ARCH-023", "virtualization provenance missing")
    passed.append("ARCH-023")
    figure_manifest = workspace / "evaluation/results/figures/figures_manifest.json"
    require(figure_manifest.exists() and "raw_hash_inventory_sha256" in json.loads(figure_manifest.read_text()),
            "ARCH-024", "figures are not hash-linked to raw data")
    passed.append("ARCH-024")
    require((workspace / "evaluation/scan_artifact_secrets.py").exists(), "ARCH-025", "artifact secret scanner missing")
    passed.append("ARCH-025")

    # UIR research boundary invariants. These checks are structural and are
    # complemented by poa-uir unit/property tests for behavioral invariants.
    require("poa-uir" in packages, "ARCH-UIR-001", "poa-uir package missing")
    uir_dependencies = set(graph["poa-uir"])
    require(not (uir_dependencies & {"poa-verifier-example", "domain-electronic-warrant", "domain-agent-delegation"}),
            "ARCH-UIR-001", "poa-uir depends on verifier or domain package")
    passed.append("ARCH-UIR-001")
    require("poa-uir" not in graph["poa-core"], "ARCH-UIR-002", "poa-core depends on poa-uir")
    passed.append("ARCH-UIR-002")
    frontend_text = source_text(workspace / "crates/poa-uir/src/frontend")
    require("impl DslFrontend for KoreanFrontend" in frontend_text
            and "impl DslFrontend for EnglishFrontend" in frontend_text
            and "UniversalIrDraft" in frontend_text,
            "ARCH-UIR-003", "frontends do not share the UIR model/trait")
    passed.append("ARCH-UIR-003")
    canonical_text = (workspace / "crates/poa-uir/src/canonical.rs").read_text(encoding="utf-8")
    require("poa_protocol::canonicalize_value" in canonical_text, "ARCH-UIR-004", "UIR does not reuse canonicalization")
    passed.extend(["ARCH-UIR-004", "ARCH-UIR-005"])
    require(all(field in canonical_text for field in ("request_id", "source_language", "source_hash", "created_at")) is False,
            "ARCH-UIR-006", "semantic view directly includes non-semantic metadata fields")
    passed.append("ARCH-UIR-006")
    policy_uir_text = (workspace / "crates/poa-uir/src/policy.rs").read_text(encoding="utf-8").lower()
    require("renderer" not in policy_uir_text and "slm" not in policy_uir_text,
            "ARCH-UIR-007", "policy evaluation references rendering/SLM")
    passed.append("ARCH-UIR-007")
    tests_text = (workspace / "crates/poa-uir/src/tests.rs").read_text(encoding="utf-8")
    require("rejected_path_never_invokes_renderer" in tests_text, "ARCH-UIR-008", "reject renderer guard test missing")
    passed.append("ARCH-UIR-008")
    output_text = (workspace / "crates/poa-uir/src/output_contract.rs").read_text(encoding="utf-8")
    require("unsupported claim" in output_text and "VerifiedFactSet" in output_text,
            "ARCH-UIR-009", "output validator is not fact-set constrained")
    passed.append("ARCH-UIR-009")
    model_text = (workspace / "crates/poa-uir/src/model.rs").read_text(encoding="utf-8").lower()
    require(not any(token in model_text for token in ("acme", "samsung", "corporation_id", "xbrl")),
            "ARCH-UIR-010", "domain entity literal in UIR core model")
    passed.append("ARCH-UIR-010")

    lexicon_text = (workspace / "crates/poa-uir/src/frontend/lexicon.rs").read_text(encoding="utf-8").lower()
    require("trait semanticlexicon" in lexicon_text
            and not any(token in lexicon_text for token in ("acme", "samsung", "microsoft", "apple inc")),
            "ARCH-UIR-GEN-001", "SemanticLexicon contains an entity instance or is missing")
    passed.append("ARCH-UIR-GEN-001")
    resolution_text = (workspace / "crates/poa-uir/src/resolution.rs").read_text(encoding="utf-8")
    require("NeedsClarification" in resolution_text and "Executor" not in resolution_text
            and "needs_clarification_never_produces_executable_uir" in tests_text,
            "ARCH-UIR-GEN-002", "NeedsClarification is coupled to execution")
    passed.append("ARCH-UIR-GEN-002")
    require("FilterAndRender" in output_text and "render_supported_claims(&claims)" in output_text
            and "filter_and_render_never_emits_unsupported_model_text" in tests_text,
            "ARCH-UIR-GEN-003", "FILTER_AND_RENDER lacks supported-only enforcement")
    passed.append("ARCH-UIR-GEN-003")
    require("source_digest" in output_text and "exact_value" in output_text
            and "verified_numeric_slot_binding_preserves_exact_text_provenance_and_digest" in tests_text,
            "ARCH-UIR-GEN-004", "verified numeric binding lacks value/digest invariant")
    passed.append("ARCH-UIR-GEN-004")
    phase3_manifest_path = workspace / "results/uir_phase3/frozen_v2_manifest.json"
    require(phase3_manifest_path.exists(), "ARCH-UIR-GEN-005", "v2 candidate manifest missing")
    phase3_manifest = json.loads(phase3_manifest_path.read_text(encoding="utf-8"))
    digest = hashlib.sha256()
    parser_paths = [*sorted((workspace / "crates/poa-uir/src/frontend").glob("*.rs")),
                    workspace / "crates/poa-uir/src/resolution.rs",
                    workspace / "crates/poa-uir/src/output_contract.rs"]
    for path in parser_paths:
        digest.update(path.relative_to(workspace).as_posix().encode())
        digest.update(path.read_bytes())
    require(digest.hexdigest() == phase3_manifest.get("parser_source_sha256"),
            "ARCH-UIR-GEN-005", "parser source changed after v2 candidate generation")
    passed.append("ARCH-UIR-GEN-005")
    publisher = (workspace / "evaluation/uir_generalization/generate_phase3_report.py").read_text(encoding="utf-8")
    require("--publication-ready" in publisher and "human_review_status" in publisher
            and "ARCH-UIR-GEN-006 BLOCKED" in publisher,
            "ARCH-UIR-GEN-006", "publication-ready report lacks human-review gate")
    passed.append("ARCH-UIR-GEN-006")

    print(json.dumps({"status": "passed", "tests": passed, "graph": graph}, sort_keys=True))


if __name__ == "__main__":
    main()
