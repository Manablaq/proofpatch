# ProofPatch Current Bradbury Final Evidence

This is the canonical final-evidence record for the current ProofPatch replacement deployment on GenLayer Bradbury Testnet.

`docs/BRADBURY_FINAL_EVIDENCE.md` is historical and superseded.

## Source checkpoint

```text
Repository: Manablaq/proofpatch
Commit: 61ffd044c5e9e6e25092e8ddd8886f301ad19d24
Branch: fix/finalized-attestation-reads
Network: Bradbury Testnet
```

## Canonical contracts

```text
Owner:
0x1f87Ae197af539253978d435aD45cCf28Fb95024

Governor:
0x20a14189cb68d1878eaA9253b14983ace1684aA6

Protected Target:
0x7e22B7c72B196e0db60785344570Fb558bD3b33A
```

## Exact upgrade bindings

```text
Proposal ID:
1

Parent version:
1.0.0

Parent code hash:
7607cce754d8f7905eed629b0e8af0f3ce51bd405b3b4ba9db19e5d831209f19

Candidate version:
2.0.0

Candidate code hash:
013f8ae10b9f38aaad7689168b94335a514a9c30882f4a03daa3eb546cda83ea

Policy fingerprint:
18c5d7e9852799896fb7fe3ee11ce8abc1104122adbb4afcee22e163fb424e50

Evidence-set hash:
bb4f2a6092e32f9ec67c2508f243a09036bfd1ad1d4b505f26766df65250cb5d
```

## Evidence publications

```text
CI commit:
c0016a45f627a568cdbabf0db0b6cd2729faad53

Audit commit:
be1fa7a60b6ec9256600fc0dbd9f86bb62600450

Audit verdict:
PASS

Independent review:
true
```

## Final transaction chain

```text
Review:
0x0a6b3c9275dc12fb9f98f7ceb52cc165db74444b4c27de10dcdd235ca338e34b

Finality-generated target upgrade:
0xd196ac64c42e48e944f6ca85b79ab0a74fcc6100235e8b6e3015a604a57e5e59

Finality-generated confirm_install:
0xdd8118477147a0d8a9b65442b87d31ec0f8916e116e8ca89804901828a1462a5
```

All three reached:

```text
FINALIZED
AGREE
FINISHED_WITH_RETURN
```

No manual target upgrade, manual confirm_install, appeal, duplicate review, or manual finalization was used.

## Final canonical state

```text
Proposal status:
VERIFIED

Last review code:
INSTALL_VERIFIED

Active proposal:
0

Current version:
2.0.0

Current code hash:
013f8ae10b9f38aaad7689168b94335a514a9c30882f4a03daa3eb546cda83ea

Installed proposal:
1

Installed candidate hash:
013f8ae10b9f38aaad7689168b94335a514a9c30882f4a03daa3eb546cda83ea

Release label:
ProtectedTarget/v2-safe

Product:
ProofPatch Protected Target

Protected value:
proofpatch-bradbury-baseline-v1
```

The target owner and ProofPatch Governor binding remained unchanged.

## Replay prohibition

Proposal #1 is complete and VERIFIED.

Do not repeat:

- create_proposal
- review_proposal
- appeal
- proofpatch_upgrade
- confirm_install
- manual finalization
- reconcile_install
- mark_execution_timeout
- cancel / expire / repair

```text
NO_MORE_UPGRADE_WRITES_REQUIRED=YES
```
