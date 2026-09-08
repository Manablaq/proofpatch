# ProofPatch Submission Handoff

This is the reviewer-facing entry point for the completed ProofPatch release.

## Project

**ProofPatch — No code upgrade without consensus.**

ProofPatch is a GenLayer-native semantic upgrade firewall for Intelligent Contracts. It freezes exact candidate bytes, binds immutable publisher-backed evidence, runs independent validator semantic review, binds the exact consensus result to the upgrade consequence, waits for finality, then verifies the exact installed candidate.

## Public links

- Production application: https://proofpatch.vercel.app
- Production dashboard: https://proofpatch.vercel.app/app
- Repository: https://github.com/Manablaq/proofpatch
- Default branch: `main`

## Canonical Bradbury deployment

```text
Network           Bradbury Testnet
Governor          0x20a14189cb68d1878eaA9253b14983ace1684aA6
Protected target  0x7e22B7c72B196e0db60785344570Fb558bD3b33A
Registered owner  0x1f87Ae197af539253978d435aD45cCf28Fb95024

Proposal           1
Installed version  2.0.0
Status              VERIFIED
Last review code    INSTALL_VERIFIED
Active proposal     0
Release             ProtectedTarget/v2-safe
```

## Exact consequential bindings

```text
Parent code hash
7607cce754d8f7905eed629b0e8af0f3ce51bd405b3b4ba9db19e5d831209f19

Candidate code hash
013f8ae10b9f38aaad7689168b94335a514a9c30882f4a03daa3eb546cda83ea

Policy fingerprint
18c5d7e9852799896fb7fe3ee11ce8abc1104122adbb4afcee22e163fb424e50

Evidence-set hash
bb4f2a6092e32f9ec67c2508f243a09036bfd1ad1d4b505f26766df65250cb5d
```

## Canonical transaction chain

```text
Governor deployment
0x68ae65eee7a25430c70007fd9f587b3be97364aee82f57f3c63a1763e6e02bfe

Target deployment
0x604f8d63e246f6e190d753e3b23a19c9340909f7d06418f50407e1432c2a11aa

Registration parent
0xa0b19fe09cb2faed06d02c48b4b47e661f2c73f1585538cf1ec5f094e1fc09ae

Proposal creation
0x1c32f5beb67fad804eea8c79f061c11ca16d402d119ea133e1a59e34541e801c

Review parent
0x0a6b3c9275dc12fb9f98f7ceb52cc165db74444b4c27de10dcdd235ca338e34b

Finality-generated upgrade child
0xd196ac64c42e48e944f6ca85b79ab0a74fcc6100235e8b6e3015a604a57e5e59

Install confirmation child
0xdd8118477147a0d8a9b65442b87d31ec0f8916e116e8ca89804901828a1462a5
```

The review, generated upgrade, and install confirmation each reached `FINALIZED`, `AGREE`, and `FINISHED_WITH_RETURN`.

## Reviewer hard gates

ProofPatch explicitly covers:

1. **Evidence trust/provenance** — source, CI, and audit publisher identities/repository prefixes are policy-bound.
2. **Immutable/versioned/fresh/corroborated evidence** — immutable commit URLs, freshness/expiry, stable evidence IDs, and independent audit corroboration are enforced.
3. **Correctable evidence failures** — repairable failures persist as `EVIDENCE_REPAIR_REQUIRED`; transient failures use `REVIEW_RETRY_REQUIRED`.
4. **Liveness/recovery** — proposal expiry, retry/repair, execution deadline, reconciliation, and timeout prevent indefinite lock.
5. **Exact consensus-to-consequence binding** — every authorization-driving binding and semantic boolean must match exactly; no tolerance/confidence range can authorize installation.

## Verification

Run the complete contract gate:

```bash
python scripts/preflight.py
```

Run the production frontend gates:

```bash
cd frontend
npm ci
npm run typecheck
npm run build
```

GitHub Actions runs both contract and frontend verification on pushes and pull requests.

## Evidence index

- `docs/BRADBURY_CURRENT_FINAL_EVIDENCE.md` — current canonical chain evidence
- `docs/BRADBURY_FINAL_EVIDENCE.md` — superseded historical chain evidence
- `docs/REVIEWER_COVERAGE_AUDIT.md` — proof coverage boundary
- `docs/REVIEWER_GATES.md` — hard-gate checklist
- `docs/ARCHITECTURE.md` — design and trust chain
- `docs/THREAT_MODEL.md` — security model
- `docs/BRADBURY_PLAN.md` — live verification record
- `docs/BRADBURY_TARGET_V1_RECOVERY.md` — failed first target attempt and resolution
- `docs/TYPECHECK_GATE.md` — strict typecheck evidence behavior

## Canonical replay prohibition

Proposal #1 is complete and must remain historical/read-only.

Do not repeat its review, upgrade, confirmation, reconciliation, timeout, expiry, cancellation, repair, registration, or deployment merely to create new evidence. Track existing transaction hashes through consensus, finality, and execution instead.
