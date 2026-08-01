# PBEA threat model

## Scope boundary

The evaluated threat begins only after the actor has authenticated successfully, the access-control decision is allow, and the request arrived through an accepted service/channel. Every raw record therefore has `actor_authenticated=true` and `access_authorized=true`. The experiment asks what happens when an already admitted request attempts a harmful state transition or capability use.

PBEA means **Policy-Bound Execution Architecture**. Historical crate and protocol identifiers beginning with `poa-` are retained for compatibility; they do not narrow the paper's PBEA scope.

## In-scope adversary actions

- Submit a syntactically valid transition that violates a domain invariant.
- Read a controlled file outside the declared filesystem capability.
- execute a controlled marker helper after runtime promises are applied.
- Connect to a controlled loopback sink not present in the application allowlist.
- Supply malformed runtime policy or require a resource that does not exist.
- Repeat a policy-digest violation using a valid actor.
- Trigger an internal fault after candidate creation and before commit.
- Bind a request to the wrong deterministic policy digest.

All targets are synthetic fixtures under `/tmp/pbea-eval` or loopback. No third-party host, production secret, malware, or destructive payload is used.

## Security objectives

The bounded objectives are: prevent the tested malicious effect, preserve state on non-commit outcomes, refuse invalid Full-PBEA startup before the business loop, preserve benign behavior, and retain a claim-to-record trail. Authentication compromise, kernel compromise, physical attack, undisclosed vulnerabilities, general malware immunity, and universal insider/supply-chain protection are out of scope.
