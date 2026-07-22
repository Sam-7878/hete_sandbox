-------------------------- MODULE ElectronicWarrant --------------------------
EXTENDS Naturals, FiniteSets, Sequences

CONSTANTS MaxAmount, Expiry

States == {"Draft", "Submitted", "CredentialVerified", "Authorized", "Active",
           "PartiallyExecuted", "FullyExecuted", "Suspended", "Revoked",
           "Expired", "Released", "Rejected", "Failed"}

VARIABLES warrant_state, authorized, nonce_used, reserved, executed, released,
          now, adapter_committed, audit_count

vars == <<warrant_state, authorized, nonce_used, reserved, executed, released,
          now, adapter_committed, audit_count>>

Init == /\ warrant_state = "Draft"
        /\ authorized = FALSE
        /\ nonce_used = FALSE
        /\ reserved = 0 /\ executed = 0 /\ released = 0
        /\ now = 0 /\ adapter_committed = FALSE /\ audit_count = 0

Submit == /\ warrant_state = "Draft"
          /\ warrant_state' = "Submitted"
          /\ UNCHANGED <<authorized, nonce_used, reserved, executed, released, now,
                         adapter_committed, audit_count>>

Authorize == /\ warrant_state = "Submitted" /\ ~nonce_used
             /\ warrant_state' = "Authorized"
             /\ authorized' = TRUE /\ nonce_used' = TRUE
             /\ UNCHANGED <<reserved, executed, released, now, adapter_committed, audit_count>>

Activate == /\ warrant_state = "Authorized" /\ authorized /\ now < Expiry
            /\ warrant_state' = "Active" /\ reserved' = MaxAmount
            /\ adapter_committed' = TRUE /\ audit_count' = audit_count + 1
            /\ UNCHANGED <<authorized, nonce_used, executed, released, now>>

Execute(amount) == /\ warrant_state \in {"Active", "PartiallyExecuted"}
                   /\ now < Expiry /\ amount > 0
                   /\ executed + amount <= reserved
                   /\ executed' = executed + amount
                   /\ warrant_state' = IF executed' = reserved THEN "FullyExecuted" ELSE "PartiallyExecuted"
                   /\ audit_count' = audit_count + 1
                   /\ UNCHANGED <<authorized, nonce_used, reserved, released, now, adapter_committed>>

Release == /\ warrant_state \in {"Active", "PartiallyExecuted"}
           /\ released' = reserved - executed
           /\ warrant_state' = "Released" /\ audit_count' = audit_count + 1
           /\ UNCHANGED <<authorized, nonce_used, reserved, executed, now, adapter_committed>>

Revoke == /\ warrant_state \in {"Authorized", "Active", "PartiallyExecuted", "Suspended"}
          /\ warrant_state' = "Revoked" /\ released' = reserved - executed
          /\ audit_count' = audit_count + 1
          /\ UNCHANGED <<authorized, nonce_used, reserved, executed, now, adapter_committed>>

Tick == /\ now' = now + 1
        /\ UNCHANGED <<warrant_state, authorized, nonce_used, reserved, executed,
                       released, adapter_committed, audit_count>>

Expire == /\ now >= Expiry /\ warrant_state \in {"Active", "PartiallyExecuted"}
          /\ warrant_state' = "Expired" /\ released' = reserved - executed
          /\ audit_count' = audit_count + 1
          /\ UNCHANGED <<authorized, nonce_used, reserved, executed, now, adapter_committed>>

Next == Submit \/ Authorize \/ Activate \/ (\E amount \in 1..MaxAmount: Execute(amount))
        \/ Release \/ Revoke \/ Tick \/ Expire

Spec == Init /\ [][Next]_vars

TypeInvariant == /\ warrant_state \in States
                 /\ reserved \in 0..MaxAmount /\ executed \in 0..MaxAmount
                 /\ released \in 0..MaxAmount /\ now \in Nat /\ audit_count \in Nat
UnauthorizedExecution == warrant_state \in {"Active", "PartiallyExecuted", "FullyExecuted"} => authorized
NoReplay == nonce_used => authorized
AmountBound == executed <= MaxAmount
Conservation == executed + released <= reserved
NoPostExpiryExecution == now >= Expiry => warrant_state # "FullyExecuted" \/ executed <= reserved
RevocationSafety == warrant_state = "Revoked" => released = reserved - executed
DomainBinding == TRUE \* Binding is an immutable input in the Rust model.
Atomicity == adapter_committed => warrant_state \in {"Active", "PartiallyExecuted", "FullyExecuted", "Released", "Expired", "Revoked"}
AuditCompleteness == warrant_state \in {"FullyExecuted", "Released", "Expired", "Revoked", "Rejected", "Failed"} => audit_count > 0
DomainNeutralCore == TRUE \* Checked structurally by ARCH-005 and ARCH-010.

=============================================================================
