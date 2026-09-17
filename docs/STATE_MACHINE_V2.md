# ProofPatch v2 state machine

## Target modes

```text
BOOTSTRAP → ACTIVE
ACTIVE → PROVISIONAL → ACTIVE
PROVISIONAL → INCIDENT_OPEN → INCIDENT_CONFIRMED → RECOVERED
                                  │
                                  └→ RECOVERY_RETRY_REQUIRED → INCIDENT_CONFIRMED
```

`PROVISIONAL` blocks protected application writes. `ACTIVE` and `RECOVERED` allow them. Recovery cannot bypass incident consensus.

## Upgrade proposal

```text
PROPOSED
  ├─ evidence invalid → EVIDENCE_REPAIR_REQUIRED → PROPOSED
  ├─ transient failure → REVIEW_RETRY_REQUIRED → PROPOSED
  ├─ semantic reject → REJECTED
  ├─ expiry → EXPIRED
  ├─ owner cancellation → CANCELLED
  └─ exact approval → UPGRADE_QUEUED → INSTALLED_PROVISIONAL
                                      └→ CERTIFICATION_QUEUED → CERTIFIED
```

Installation is never certification. Finalized target attestations are required for installation reconciliation and activation.

## Assurance and incident states

Assurance uses `ASSURANCE_PENDING`, `ASSURANCE_REPAIR_REQUIRED`, and `ASSURANCE_RETRY_REQUIRED`. A failed or expired assurance path opens an append-only incident docket. A fresh incident with valid evidence can challenge that exact provisional release. Incident review ends in `INCIDENT_CONFIRMED`, `INCIDENT_DISMISSED`, repair, or retry. The review transaction itself remains subject to GenLayer's native appeal lifecycle; only its finalized outcome can trigger the precommitted recovery capsule. Recovery has its own deadline, reconciliation path, and retry state.

## Idempotency and deadlines

Proposal, release, evidence, incident, installation, activation, and recovery identities are hash-bound. Duplicate confirmations are harmless only when their identities match. Proposal execution and assurance deadlines are checked before every consequence; non-final target state never proves completion.
