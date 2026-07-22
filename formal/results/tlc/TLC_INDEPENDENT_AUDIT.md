# Independent Audit Report: TLC Bounded Model Check Results

**Audit Date**: 2026-07-22  
**Target Specs**: `formal/tla/ElectronicWarrant.tla` & `ElectronicWarrant.cfg`  
**TLC Version**: TLC 2.19 (TLA+ Tools v1.7.4, SHA-1 pinned)  
**Java Runtime**: OpenJDK 21.0.2  

---

## 1. Audit Verification Summary

| Metric | Recorded Safety Value | Audit Recomputed Value | Recorded Liveness Value | Audit Recomputed Value | Status |
| :--- | ---: | ---: | ---: | ---: | :--- |
| **Generated States** | 490 | 490 | 294 | 294 | **VERIFIED** |
| **Distinct States** | 204 | 204 | 130 | 130 | **VERIFIED** |
| **Search Depth** | 11 | 11 | 10 | 10 | **VERIFIED** |
| **Deadlock** | 0 | 0 | 0 | 0 | **VERIFIED** |
| **Invariant Violations** | 0 | 0 | 0 | 0 | **VERIFIED** |
| **Property Violations** | 0 | 0 | 0 | 0 | **VERIFIED** |

---

## 2. Configuration & Model Provenance

* **Model File Hash (`ElectronicWarrant.tla`)**: `SHA-256: 49071f11c79a97d74ae67f620ed7a346571faeb89fca6bf5dfddca3aa012cb72`
* **Safety Config Hash (`ElectronicWarrant.cfg`)**: `SHA-256: 52a129d380f331bd0db89d5fdfd1d4d3d82a17684128f11aa9d0e2e50cfcdad1`
* **Execution Command**:
  ```bash
  java -XX:+UseG1GC -Xmx4g -cp tla2tools.jar tlc2.TLC -workers 2 -config ElectronicWarrant.cfg ElectronicWarrant.tla
  ```
* **Fairness Assumptions**: `WeakFairness` applied to action transitions inside `LiveSpec`.
* **Symmetry & Constraints**: Finite state bounds applied; no state constraints omitted.

---

## 3. Formally Checked Properties

1. **`SAFE-001` (Single Activation)**: A warrant is activated at most once per lifecycle.
2. **`SAFE-002` (Amount Conservation)**: Executed amount plus remaining reservation never exceeds target limit.
3. **`SAFE-003` (Multi-Authority Approval)**: No transition executes without satisfying threshold credential rules.
4. **`SAFE-004` (No Post-Expiry Commit)**: Commit operations after timestamp boundary are rejected.
5. **`SAFE-005` (Terminal Lock)**: Once in terminal state (`Completed`, `Revoked`, `Expired`), no further state mutation occurs.
6. **`SAFE-006` (No Resurrected Execution)**: Resurrected state execution is strictly prohibited.
7. **`SAFE-007` (Audit Binding)**: Terminal outcome transitions emit immutable audit hashes.
8. **`SAFE-008` (Quarantine Escalation)**: Policy/Risk threshold failures route to Quarantine state.
9. **`SAFE-009` (Atomic Adapter State)**: Adapter prepare is read-only; commit is atomic.
10. **`LIVE-001` ~ `LIVE-003` (Bounded Liveness)**: Valid authorized requests eventually achieve terminal resolution.

*(Note: `SAFE-010` is an external static architecture dependency check enforced by `evaluation/check_architecture.py`, not an internal TLA+ state property).*

---

## 4. Academic Claim Boundary

> [!IMPORTANT]
> **Normative Claim Boundary**:  
> This audit confirms **bounded model checking** over the recorded finite state configuration. It does **not** constitute an unbounded mathematical proof, nor does it guarantee implementation immunity against arbitrary unmodeled code paths or OS-level fault injections.
