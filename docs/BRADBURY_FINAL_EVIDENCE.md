# ProofPatch Historical Bradbury Final Evidence — Superseded

This file preserves the completed historical ProofPatch safe-upgrade path for provenance. It is superseded and MUST NOT be used as the current submission deployment or current canonical evidence.

## Historical network and contracts

```text
Network           Bradbury Testnet
Governor          0xc0100eFD567CD9dCcC8b9D17E381774fC4113ade
Protected target  0xe7165dEA0F712E3161ADa773c41755d79F1e696B
Registered owner  0x1f87Ae197af539253978d435aD45cCf28Fb95024
```

## Frozen and installed bindings

```text
Parent version       1.0.0
Parent code hash      7607cce754d8f7905eed629b0e8af0f3ce51bd405b3b4ba9db19e5d831209f19

Candidate version    2.0.0
Candidate code hash  013f8ae10b9f38aaad7689168b94335a514a9c30882f4a03daa3eb546cda83ea

Policy fingerprint   0f30dea3a111d4d6ba13b68bb667338618c963ea5258049303a2492be73fc1ab
Evidence-set hash    c252fd77fb2209cf65a5d47fbb3079218c6d1d196461c6f72573b3fcdd046ec5
```

## Final proposal state

```text
Proposal ID          1
Status               VERIFIED
Last review code     INSTALL_VERIFIED
Active proposal      0
Release label        ProtectedTarget/v2-safe
```

Historical proposal summary:

```json
{
  "proposal_id": 1,
  "target": "0xe7165dEA0F712E3161ADa773c41755d79F1e696B",
  "parent_version": "1.0.0",
  "parent_code_hash": "7607cce754d8f7905eed629b0e8af0f3ce51bd405b3b4ba9db19e5d831209f19",
  "candidate_version": "2.0.0",
  "candidate_code_hash": "013f8ae10b9f38aaad7689168b94335a514a9c30882f4a03daa3eb546cda83ea",
  "policy_fingerprint": "0f30dea3a111d4d6ba13b68bb667338618c963ea5258049303a2492be73fc1ab",
  "evidence_set_hash": "c252fd77fb2209cf65a5d47fbb3079218c6d1d196461c6f72573b3fcdd046ec5",
  "status": "VERIFIED",
  "last_review_code": "INSTALL_VERIFIED",
  "created_at": 1788694965,
  "expires_at": 1788867765,
  "reviewed_at": 1788703412,
  "execution_deadline": 1788789812
}
```

## Historical transactions

Target deployment:

```text
0x2ab59d543d453a487e9a863bcde18d8bb501171a9827d52f476a11e789fa6dc1
```

Registration:

```text
Parent
0xac7f7997622ea75a0330dd9027349a6cadd3e9cc36ad787939c85e651d9f8153

Finality-generated registration child
0x1599b7bfdcb569f84e423ae8cb051d6884a6a295b42d59e623bd8b0d9484e92d
```

Review:

```text
Outer EVM
0x4ff466bf5ea4c29123b92ccd98fb28777f0124b700a3b2dee7479f9b197de97e

Review parent
0xdaf2daf536913570bb7b2b9a81b6a05f85cc5e8fde38e95519bfae1a38891345
```

Generated upgrade/install:

```text
Upgrade child
0x12296f35e3e570d4c828022a769dc32c9c4d18ca5bb2c1a736a5f01ffdbcdb33

Confirmation child
0x9715daa0308bffc9a7b439f99ddcf9337eae186b16564c93570f7174cf17b475
```

The review parent and generated upgrade path reached finality and successful execution on this historical deployment. That historical result does not identify the corrected submission deployment.

## Final audit

```text
Final audit v2 script SHA-256
b85135d68f7e265762c71afb17947a61100713c0e9f041704889aa392bc24298

Final audit v2 log SHA-256
1270ae8e13fc8877613bde4c674ffbb7e1b1628db8d8e085fb93dbb6b5baa176
```

## Production frontend

```text
Production URL   https://proofpatch.vercel.app
Dashboard URL    https://proofpatch.vercel.app/app
Status           LIVE
```

This section records the production/frontend state associated with the historical deployment. The corrected submission path must be wired only after the replacement governor/target deployment is finalized and independently verified.

Production promotion has completed. Temporary Preview URLs are not submission URLs.

## Replay prohibition

The following historical actions are complete and must not be repeated:

- deploy the historical target;
- register the historical target;
- review Proposal #1;
- manually call the generated upgrade path;
- manually confirm installation;
- reconcile Proposal #1;
- mark Proposal #1 execution timeout;
- expire/cancel/repair Proposal #1;
- manually finalize any completed historical transaction.

A returned transaction hash must be tracked through consensus, finality, and execution rather than blindly resubmitted.
