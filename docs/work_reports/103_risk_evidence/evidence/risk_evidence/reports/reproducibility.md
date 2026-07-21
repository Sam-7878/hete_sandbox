# Reproducibility

## Source

Use commit `c2128a9603d2a14d4927bfe72e5e1caf1306c829`. Run from the `hete_sandbox` root on Ubuntu 24.04.

```sh
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
cargo test -p poa-core risk
cargo test -p poa-protocol risk
```

## Benchmark

```sh
GIT_COMMIT=c2128a9603d2a14d4927bfe72e5e1caf1306c829 \
RUST_VERSION=rustc-1.96.0-ac68faa20 \
cargo build --release -p poa-verifier-example --example risk_evidence_benchmark

target/release/examples/risk_evidence_benchmark overhead > evaluator_overhead.jsonl
target/release/examples/risk_evidence_benchmark sensitivity > sensitivity_results.jsonl

python3 evaluation/process_risk_evidence.py \
  --overhead evaluator_overhead.jsonl \
  --sensitivity sensitivity_results.jsonl \
  --output processed
```

B-RE1 uses 20,000 warmup calls per path, 30 samples per path, and 100,000 inner calls per sample in a release build. B-RE2 enumerates 4횞4횞4=64 AllThresholds configurations over the 16-record fixed corpus compiled into the runner.

## Snapshots

```sh
python3 evaluation/generate_risk_snapshots.py \
  --legacy-canonical protocol/examples/hete.verifier.payment.effective.canonical.json \
  --output snapshots \
  --git-commit c2128a9603d2a14d4927bfe72e5e1caf1306c829
```

## OpenBSD

Read `security/open_bsd_connection.json` immediately before every connection because the IP may change. Verify the server ED25519 fingerprint against `host_key_sha256`, synchronize the source without deleting the remote workspace, and run the same test commands supported by the installed OpenBSD toolchain. On the recorded OpenBSD 7.9 environment, cargo-fmt and cargo-clippy were unavailable; workspace and focused tests passed.
