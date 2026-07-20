#!/usr/bin/env python3
"""ARCH-001 boundary check using Cargo metadata plus source policy checks."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

DOMAIN_PACKAGES={"poa-verifier-example", "open-banking", "drone", "voting"}
FORBIDDEN_CORE=("PaymentOperation", "DroneOperation", "BankingOperation")
FORBIDDEN_MAPPER=("amount", "currency", "payment", "drone", "banking")

def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[1]); args=parser.parse_args()
    raw=subprocess.check_output(["cargo","metadata","--format-version","1","--no-deps"], cwd=args.workspace, text=True)
    metadata=json.loads(raw); packages={p["name"]:p for p in metadata["packages"]}
    core=packages.get("poa-core")
    if core is None: raise SystemExit("ARCH-001 FAIL: poa-core missing")
    dependencies={d["name"] for d in core["dependencies"]}
    bad=dependencies & DOMAIN_PACKAGES
    if bad: raise SystemExit(f"ARCH-002 FAIL: poa-core domain dependencies: {sorted(bad)}")
    core_text="\n".join(p.read_text(encoding="utf-8") for p in (args.workspace/"crates/poa-core/src").glob("*.rs"))
    if any(token in core_text for token in FORBIDDEN_CORE): raise SystemExit("ARCH-003 FAIL: domain operation imported into core")
    mapper=(args.workspace/"crates/poa-sandbox/src/mapper.rs").read_text(encoding="utf-8").lower()
    if any(token in mapper for token in FORBIDDEN_MAPPER): raise SystemExit("ARCH-004 FAIL: business rule in sandbox mapper")
    graph={p["name"]:sorted(d["name"] for d in p["dependencies"]) for p in metadata["packages"]}
    print(json.dumps({"test_id":"ARCH-001","status":"passed","graph":graph}, sort_keys=True))

if __name__ == "__main__": main()

