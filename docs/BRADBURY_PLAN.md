# Bradbury Verification Plan and Record

This document now distinguishes the canonical safe-upgrade path that is already complete from adversarial/recovery paths that must not be replayed against proposal #1.

## Canonical deployment

The canonical live contracts are:

- Governor:
  `0xc0100eFD567CD9dCcC8b9D17E381774fC4113ade`
- Protected target:
  `0xe7165dEA0F712E3161ADa773c41755d79F1e696B`
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

Registration:

- Parent:
  `0xac7f7997622ea75a0330dd9027349a6cadd3e9cc36ad787939c85e651d9f8153`
- Finality-generated registration child:
  `0x1599b7bfdcb569f84e423ae8cb051d6884a6a295b42d59e623bd8b0d9484e92d`

Review:

- Outer EVM transaction:
  `0x4ff466bf5ea4c29123b92ccd98fb28777f0124b700a3b2dee7479f9b197de97e`
- Review parent:
  `0xdaf2daf536913570bb7b2b9a81b6a05f85cc5e8fde38e95519bfae1a38891345`

Generated install path:

- Upgrade child:
  `0x12296f35e3e570d4c828022a769dc32c9c4d18ca5bb2c1a736a5f01ffdbcdb33`
- Confirmation child:
  `0x9715daa0308bffc9a7b439f99ddcf9337eae186b16564c93570f7174cf17b475`

The review and upgrade evidence must be interpreted with both consensus/finality status and execution result. `Accepted` alone is never treated as proof of successful code installation.

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

See `BRADBURY_FINAL_EVIDENCE.md`.
