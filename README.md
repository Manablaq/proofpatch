# ProofPatch

**No code upgrade without consensus.**

[![ProofPatch verify](https://github.com/Manablaq/proofpatch/actions/workflows/verify.yml/badge.svg)](https://github.com/Manablaq/proofpatch/actions/workflows/verify.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Production](https://img.shields.io/badge/Production-proofpatch.vercel.app-0b7a68)](https://proofpatch.vercel.app)

ProofPatch is a GenLayer-native semantic upgrade firewall for Intelligent Contracts. A protected target designates ProofPatch as its sole GenVM upgrader, so an exact candidate can replace live code only after immutable evidence binding, independent validator semantic review, GenLayer finality, exact-byte installation, and post-install verification.

## Live deployment

- **Application:** https://proofpatch.vercel.app
- **Dashboard:** https://proofpatch.vercel.app/app
- **Network:** Bradbury Testnet
- **Governor:** `0x20a14189cb68d1878eaA9253b14983ace1684aA6`
- **Protected target:** `0x7e22B7c72B196e0db60785344570Fb558bD3b33A`
- **Registered owner:** `0x1f87Ae197af539253978d435aD45cCf28Fb95024`
- **Installed version:** `2.0.0`
- **Canonical proposal:** `#1`
- **Final proposal state:** `VERIFIED`
- **Last review/install code:** `INSTALL_VERIFIED`
- **Active proposal:** `0`
- **Release:** `ProtectedTarget/v2-safe`

Proposal #1 is canonical reviewer evidence and is permanently historical/read-only. Its registration, review, generated upgrade, confirmation, and final verification are complete and must not be replayed.

## What ProofPatch proves

ProofPatch combines deterministic bindings with validator semantic review:

1. Register a protected target and immutable upgrade policy.
2. Freeze exact candidate bytes and SHA-256 before review.
3. Bind source, CI, and independent audit evidence to immutable publisher/version identities.
4. Enforce freshness, expiry, stable evidence IDs, and independent corroboration.
5. Have leader and validators independently repeat evidence verification and semantic policy evaluation.
6. Require exact agreement on every authorization-driving field and semantic safety boolean.
7. Emit the upgrade consequence only on GenLayer finality.
8. Re-check authorization and exact candidate bytes immediately before installation.
9. Persist installed proposal/hash metadata and verify the completed installation.
10. Provide repair, retry, expiry, reconciliation, and timeout paths so consequential state cannot remain locked indefinitely.

There is no fuzzy confidence threshold or tolerance that can authorize code installation.

## Reviewer-facing evidence

Start here:

- [`docs/SUBMISSION.md`](docs/SUBMISSION.md) — compact reviewer handoff and submission checklist
- [`docs/BRADBURY_CURRENT_FINAL_EVIDENCE.md`](docs/BRADBURY_CURRENT_FINAL_EVIDENCE.md) — current canonical addresses, hashes, transactions, and final state
- [`docs/REVIEWER_COVERAGE_AUDIT.md`](docs/REVIEWER_COVERAGE_AUDIT.md) — deterministic vs Bradbury proof boundary
- [`docs/REVIEWER_GATES.md`](docs/REVIEWER_GATES.md) — reviewer-readiness hard gates
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — trust chain and consensus boundary
- [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) — security assumptions and adversarial model
- [`docs/BRADBURY_PLAN.md`](docs/BRADBURY_PLAN.md) — canonical Bradbury verification record
- [`docs/BRADBURY_TARGET_V1_RECOVERY.md`](docs/BRADBURY_TARGET_V1_RECOVERY.md) — preserved failed-deployment diagnosis and resolution
- [`docs/TYPECHECK_GATE.md`](docs/TYPECHECK_GATE.md) — strict GenVM typecheck evidence policy

## Repository layout

```text
.github/workflows/
  verify.yml                       contract + frontend CI

contracts/
  proofpatch_governor.py           immutable semantic upgrade governor
  protected_target_v1.py          canonical protected target base
  protected_target_v2_safe.py     installed compatible candidate
  protected_target_v2_unsafe.py   adversarial fixture; never deploy canonically

abi/
  proofpatch_governor.json
  protected_target_v1.json
  protected_target_v2_safe.json

tests/
  direct/                          deterministic Direct Mode regression suite
  integration/                     explicit Bradbury integration boundary

scripts/
  preflight.py                     lint + typecheck + schema + Direct Mode
  hash_source.py                   exact SHA-256 helper
  build_evidence.py                canonical evidence envelopes
  verify_deployed_source.py        finalized RPC byte-for-byte parity

artifacts/
  local-preflight.json
  strict-typecheck/

docs/
  ...

frontend/
  app/                             Next.js App Router routes
  components/                      product UI
  lib/                             GenLayer reads/writes, wallet, tx tracking
  package.json
```

## Verification

### Contracts and Direct Mode

Requires Python 3.12+ and Git.

```bash
cd ~/Downloads/proofpatch

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

python scripts/preflight.py
```

A passing preflight performs the GenVM lint/type/schema gates and the complete Direct Mode suite, then writes reviewer-facing verification artifacts only after every gate succeeds.

Run only the deterministic suite with:

```bash
source .venv/bin/activate
pytest tests/direct -v
```

### Frontend

The production frontend uses Next.js 16, React 19, GenLayerJS, TanStack Query, next-themes, Sonner, and Lucide.

```bash
cd ~/Downloads/proofpatch/frontend

npm ci
npm run typecheck
npm run build
npm run dev -- -p 4173
```

`npm run typecheck` generates Next.js route/type declarations before running TypeScript, so clean checkouts do not rely on a committed generated `next-env.d.ts`.

## Frontend safety model

The application uses live Bradbury reads and does not present demo proposal data as canonical chain state.

- Proposal #1 is permanently historical/read-only.
- Owner and non-owner wallet states are separated.
- Immutable candidate/evidence preflight runs before proposal submission.
- Editing proposal fields invalidates prior preflight results.
- A finalized active-slot re-check runs immediately before proposal creation.
- A returned transaction hash is persisted immediately and tracked instead of blindly resubmitted.
- Consensus, finality/lifecycle, and GenVM execution are displayed separately.
- `proofpatch_upgrade`, `confirm_install`, and manual finalization are not exposed as operator actions.
- Reconciliation requires finalized target metadata for the exact proposal ID and candidate hash.
- Execution timeout requires the deadline to have passed and is blocked when the exact installation is already visible.
- Evidence repair cannot change frozen candidate bytes/hash.

## Canonical bindings

```text
Parent code hash
7607cce754d8f7905eed629b0e8af0f3ce51bd405b3b4ba9db19e5d831209f19

Installed candidate hash
013f8ae10b9f38aaad7689168b94335a514a9c30882f4a03daa3eb546cda83ea

Policy fingerprint
18c5d7e9852799896fb7fe3ee11ce8abc1104122adbb4afcee22e163fb424e50

Evidence-set hash
bb4f2a6092e32f9ec67c2508f243a09036bfd1ad1d4b505f26766df65250cb5d
```

## Submission safety

Before submission:

- keep `main` clean and synchronized with `origin/main`;
- require contract preflight and frontend typecheck/build to pass;
- use the stable production URL `https://proofpatch.vercel.app`;
- use the canonical Bradbury addresses and evidence record;
- never replay Proposal #1 or its generated child transactions merely to produce new screenshots or logs.

See [`docs/SUBMISSION.md`](docs/SUBMISSION.md) for the final reviewer handoff.
