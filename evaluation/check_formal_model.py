#!/usr/bin/env python3
"""Static traceability check for the bounded TLA+ model."""
from pathlib import Path
import json

model = (Path(__file__).resolve().parents[1] / "formal/tla/ElectronicWarrant.tla").read_text(encoding="utf-8")
properties = ["UnauthorizedExecution", "NoReplay", "AmountBound", "Conservation", "NoPostExpiryExecution", "RevocationSafety", "DomainBinding", "Atomicity", "AuditCompleteness", "DomainNeutralCore"]
missing = [name for name in properties if f"{name} ==" not in model]
if missing:
    raise SystemExit(f"FORMAL FAIL: missing {missing}")
print(json.dumps({"status":"passed", "mapped_safety_properties": properties, "note":"Static traceability only; run TLC with ElectronicWarrant.cfg for bounded exploration."}, sort_keys=True))
