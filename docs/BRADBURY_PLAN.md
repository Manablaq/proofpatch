# Bradbury Verification Plan and Record

This document now distinguishes the canonical safe-upgrade path that is already complete from adversarial/recovery paths that must not be replayed against proposal #1.

## Canonical deployment

The canonical live contracts are:

- Governor:
  `0x20a14189cb68d1878eaA9253b14983ace1684aA6`
- Protected target:
  `0x7e22B7c72B196e0db60785344570Fb558bD3b33A`
- Registered owner:
  `0x1f87Ae197af539253978d435aD45cCf28Fb95024`

Source/deployment parity and finality checks for the canonical deployment are preserved in the project evidence archive.

## Canonical safe-upgrade proof — complete

The completed path is:

1. Target registration finalized.
2. Policy fingerprint and parent version/hash were bound.
3. Exact immutable safe-v2 candidate bytes were proposed.
4. CI and independently-owned audit evidence were bound.
5. Proposal #1 was reviewed through GenLayer validator consensus.
6. The review parent finalized.
7. Exactly one generated child upgrade transaction executed.
8. The protected target installed the exact frozen candidate.
9. The install confirmation completed.
10. Governor state reached `VERIFIED`.
11. Current version/hash moved to the exact safe-v2 values.
12. Active proposal returned to `0`.
13. Protected value, owner/governor relationship, product identity, and release invariants remained intact.

Final proposal facts:

```text
proposal_id       1
parent_version    1.0.0
candidate_version 2.0.0
status            VERIFIED
last_review_code  INSTALL_VERIFIED
active_proposal   0
release           ProtectedTarget/v2-safe
```

This path is canonical evidence and must not be repeated merely for UI testing.

## Transaction evidence

Deployments:

- Governor:
  `0x68ae65eee7a25430c70007fd9f587b3be97364aee82f57f3c63a1763e6e02bfe`
- Protected target:
  `0x604f8d63e246f6e190d753e3b23a19c9340909f7d06418f50407e1432c2a11aa`

Registration:

- Parent:
  `0xa0b19fe09cb2faed06d02c48b4b47e661f2c73f1585538cf1ec5f094e1fc09ae`

Proposal:

- Creation:
  `0x1c32f5beb67fad804eea8c79f061c11ca16d402d119ea133e1a59e34541e801c`

Review:

- Review parent:
  `0x0a6b3c9275dc12fb9f98f7ceb52cc165db74444b4c27de10dcdd235ca338e34b`

Generated install path:

- Upgrade child:
  `0xd196ac64c42e48e944f6ca85b79ab0a74fcc6100235e8b6e3015a604a57e5e59`
- Confirmation child:
  `0xdd8118477147a0d8a9b65442b87d31ec0f8916e116e8ca89804901828a1462a5`

The review, generated upgrade, and confirmation are all finalized successful transactions. `Accepted` alone is never treated as proof of successful code installation.

## Recovery semantics

The governor contains deadline-bound recovery for unresolved queued installs.

For a future proposal:

- `reconcile_install` is appropriate only when finalized target metadata already reports the exact proposal ID and candidate hash;
- `mark_execution_timeout` is appropriate only after the execution deadline when the exact installation is not present;
- a late generated child cannot be treated as authorized after timeout.

Proposal #1 does not need either recovery action because its installation already completed and was verified. Do not call reconciliation or timeout on proposal #1.

## Adversarial testing boundary

`protected_target_v2_unsafe.py` is an adversarial fixture and must not be deployed to the canonical target.

Unsafe privilege/evidence/semantic disagreement, replay, stale evidence, timeout, and source-mismatch behavior belongs in deterministic regression tests or in a separate disposable Bradbury target if a future reviewer explicitly requires another live destructive proof.

The canonical verified target must not be disturbed just to manufacture additional test transactions.

## Submission archive

Preserve:

- repository commit SHA;
- governor and target addresses;
- exact source/candidate SHA-256 values;
- policy fingerprint;
- evidence-set hash;
- immutable evidence URLs and IDs;
- finalized source-parity output;
- review parent receipt;
- generated upgrade child receipt;
- install confirmation receipt;
- consensus/finality and execution-result fields;
- Explorer links for the matching canonical deployments;
- final `VERIFIED` proposal summary;
- final audit log hash.

See `BRADBURY_CURRENT_FINAL_EVIDENCE.md` for the current canonical record. `BRADBURY_FINAL_EVIDENCE.md` is retained only as superseded historical provenance.
