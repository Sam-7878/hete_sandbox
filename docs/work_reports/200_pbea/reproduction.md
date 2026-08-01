# Reproduction guide

## Frozen experiment

Checkout source commit `1bcfa8b` on OpenBSD 7.9, build the two release binaries, and use the POSIX runner:

```sh
cargo test --workspace
cargo build --release -p poa-verifier-example --bin adversarial_probe --bin controlled_helper
sh evaluation/comparative/run_matrix_openbsd.sh \
  target/release/adversarial_probe target/release/controlled_helper \
  protocol/schema/poa-protocol-v1.schema.json \
  protocol/examples/hete.verifier.pbea-eval.json \
  protocol/schemas/pbea-eval-transition-request.json \
  /tmp/pbea-results/raw /tmp/pbea-eval 1bcfa8b
```

The runner must execute on OpenBSD for Full-PBEA evidence. It creates only controlled `/tmp/pbea-eval` fixtures and loopback listeners.

## Validation and regeneration

After transferring the three JSONL files to Ubuntu 24.04:

```sh
python3 evaluation/comparative/validate_records.py \
  docs/work_reports/200_pbea/raw/access-only.jsonl \
  docs/work_reports/200_pbea/raw/transition-only.jsonl \
  docs/work_reports/200_pbea/raw/full-pbea.jsonl
python3 evaluation/comparative/compute_security_metrics.py \
  docs/work_reports/200_pbea/raw/*.jsonl \
  --output docs/work_reports/200_pbea/generated/metrics.json
python3 evaluation/comparative/generate_tables.py \
  docs/work_reports/200_pbea/generated/metrics.json \
  docs/work_reports/200_pbea/generated
python3 evaluation/comparative/generate_report.py \
  docs/work_reports/200_pbea/generated/metrics.json \
  docs/work_reports/200_pbea/comparative_evaluation_report.md
```

The validator must pass before any generated number is used. Shell glob order does not affect aggregation, but explicit paths are preferable for audit logs.
