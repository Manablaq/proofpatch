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
Governor          0xc0100eFD567CD9dCcC8b9D17E381774fC4113ade
Protected target  0xe7165dEA0F712E3161ADa773c41755d79F1e696B
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
0f30dea3a111d4d6ba13b68bb667338618c963ea5258049303a2492be73fc1ab

Evidence-set hash
c252fd77fb2209cf65a5d47fbb3079218c6d1d196461c6f72573b3fcdd046ec5
```

## Canonical transaction chain

```text
Target deployment
0x2ab59d543d453a487e9a863bcde18d8bb501171a9827d52f476a11e789fa6dc1

Registration parent
0xac7f7997622ea75a0330dd9027349a6cadd3e9cc36ad787939c85e651d9f8153

Registration child
0x1599b7bfdcb569f84e423ae8cb051d6884a6a295b42d59e623bd8b0d9484e92d

Review outer transaction
0x4ff466bf5ea4c29123b92ccd98fb28777f0124b700a3b2dee7479f9b197de97e

Review parent
0xdaf2daf536913570bb7b2b9a81b6a05f85cc5e8fde38e95519bfae1a38891345

Finality-generated upgrade child
0x12296f35e3e570d4c828022a769dc32c9c4d18ca5bb2c1a736a5f01ffdbcdb33

Install confirmation child
0x9715daa0308bffc9a7b439f99ddcf9337eae186b16564c93570f7174cf17b475
```

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

- `docs/BRADBURY_FINAL_EVIDENCE.md` — canonical chain evidence
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
