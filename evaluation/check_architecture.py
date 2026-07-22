#!/usr/bin/env python3
"""Verify HETE core/domain/adapter boundaries (ARCH-001 through ARCH-015)."""
from __future__ import annotations

import argparse
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

    print(json.dumps({"status": "passed", "tests": passed, "graph": graph}, sort_keys=True))


if __name__ == "__main__":
    main()
