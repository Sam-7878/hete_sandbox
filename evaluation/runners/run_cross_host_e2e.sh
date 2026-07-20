#!/bin/sh
set -eu
if [ "$#" -ne 4 ]; then
  echo "usage: $0 SSH_TARGET SSH_PORT REMOTE_WORKSPACE VERIFIER_HOST" >&2
  exit 64
fi
ssh_target=$1
ssh_port=$2
remote_workspace=$3
verifier_host=$4
workspace=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
out="$workspace/docs/work_reports/100_p0_p1/cross-host"
mkdir -p "$out"

run_scenario() {
  scenario=$1
  ssh -p "$ssh_port" "$ssh_target" "cd '$remote_workspace' && mkdir -p /var/hete/audit && exec target/release/poa-verifier-example serve protocol/schema/poa-protocol-v1.schema.json protocol/base/hete.base.verifier.json protocol/examples/hete.verifier.payment.json /var/hete/audit/transitions.jsonl 0.0.0.0:7878" >"$out/$scenario.server.stdout.log" 2>"$out/$scenario.server.stderr.log" &
  server_transport_pid=$!
  sleep 3
  if ! python3 "$workspace/evaluation/runners/send_e2e_request.py" "$verifier_host" "$scenario" --digest-file "$workspace/protocol/examples/hete.verifier.payment.effective.sha256" >"$out/$scenario.client.json" 2>"$out/$scenario.client.stderr.log"; then
    kill "$server_transport_pid" 2>/dev/null || true
    wait "$server_transport_pid" 2>/dev/null || true
    return 1
  fi
  kill "$server_transport_pid" 2>/dev/null || true
  wait "$server_transport_pid" 2>/dev/null || true
}

ssh -p "$ssh_port" "$ssh_target" "cd '$remote_workspace' && \$HOME/.cargo/bin/cargo build --release --bin poa-verifier-example --bin sandbox_probe" >"$out/build.stdout.log" 2>"$out/build.stderr.log"
for scenario in commit reject quarantine abort wrong-digest; do run_scenario "$scenario"; done
echo "Cross-host application scenarios completed; run run_openbsd_native.sh for E2E-005/E2E-006 kernel evidence."

