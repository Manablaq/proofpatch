# ProofPatch

**No code upgrade without consensus.**

ProofPatch is a GenLayer-native semantic upgrade firewall for Intelligent Contracts. A protected target makes ProofPatch its sole GenVM upgrader. An exact candidate can replace live code only after immutable source/evidence binding, independent semantic validator review, GenLayer finality, exact-byte installation, and post-install verification.

## Current status

The canonical Bradbury safe-upgrade path is complete and preserved as reviewer evidence.

- Network: Bradbury Testnet
- Governor: `0xc0100eFD567CD9dCcC8b9D17E381774fC4113ade`
- Protected target: `0xe7165dEA0F712E3161ADa773c41755d79F1e696B`
- Registered owner: `0x1f87Ae197af539253978d435aD45cCf28Fb95024`
- Parent version: `1.0.0`
- Installed version: `2.0.0`
- Proposal: `#1`
- Proposal status: `VERIFIED`
- Last review/install code: `INSTALL_VERIFIED`
- Active proposal: `0`
- Release label: `ProtectedTarget/v2-safe`

The live proposal #1 path must **not** be replayed. Its review, generated upgrade, confirmation, and final verification already completed successfully.

Frontend work is on branch `frontend/live-bradbury-v1`. It is connected to live finalized Bradbury reads, implements owner-aware proposal creation, evidence repair, review/cancel/expiry controls, queued-install recovery, persistent transaction tracking, and separate consensus/finality/execution presentation. Production promotion remains intentionally pending until the final browser/reviewer audit is complete.

## Why this is GenLayer-native

A deterministic contract can compare hashes. It cannot safely decide whether arbitrary replacement source code semantically preserves human-written security invariants, avoids alternate privilege paths, retains evidence trust rules, and keeps consequential consensus correctly bound. ProofPatch puts that semantic judgment behind independent GenLayer validator consensus and uses the exact result to control GenVM's native code-upgrade capability.

## Repository

```text
contracts/
  proofpatch_governor.py
  protected_target_v1.py
  protected_target_v2_safe.py
  protected_target_v2_unsafe.py

tests/
  direct/
  integration/

scripts/
  preflight.py
  hash_source.py
  build_evidence.py
  verify_deployed_source.py

docs/
  ARCHITECTURE.md
  THREAT_MODEL.md
  REVIEWER_GATES.md
  REVIEWER_COVERAGE_AUDIT.md
  BRADBURY_PLAN.md
  BRADBURY_FINAL_EVIDENCE.md

frontend/
  app/
  components/
  lib/
  package.json
```

## Local contract verification

Requires Python 3.12+ and Git.

```bash
cd ~/Downloads/proofpatch

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

python scripts/preflight.py
```

`preflight.py` is intentionally fail-fast. It runs the configured GenVM lint/type/schema gates and the complete deterministic Direct Mode suite, and only records a successful artifact if every step succeeds.

To run only the Direct Mode suite:

```bash
source .venv/bin/activate
pytest tests/direct -v
```

## Frontend

The current frontend is a Next.js 16 / React 19 application using GenLayerJS, TanStack Query, next-themes, Sonner, and Lucide.

```bash
cd ~/Downloads/proofpatch/frontend

npm install
npm run typecheck
npm run build
npm run dev -- -p 4173
```

Open:

```text
http://localhost:4173/
http://localhost:4173/app
```

The app uses live Bradbury reads. It does **not** present demo proposal state as canonical chain state.

Safety rules in the UI:

- Proposal #1 is permanently historical/read-only.
- A transaction hash is persisted as soon as a write is submitted.
- A pending transaction is tracked rather than blindly resubmitted.
- `Accepted`, `Finalized`, and execution success are displayed as distinct facts.
- `proofpatch_upgrade`, `confirm_install`, and manual finalization are not exposed as operator buttons.
- Reconciliation is only offered when finalized target metadata reports the exact queued proposal ID and candidate hash.
- Execution timeout is only offered after the deadline and only when the exact installation is not already visible.
- Evidence repair cannot change frozen candidate bytes/hash.

## Canonical Bradbury evidence

See `docs/BRADBURY_FINAL_EVIDENCE.md` for the preserved canonical addresses, hashes, proposal state, transaction IDs, and replay prohibition.

Key bindings:

- Parent hash:
  `7607cce754d8f7905eed629b0e8af0f3ce51bd405b3b4ba9db19e5d831209f19`
- Installed candidate hash:
  `013f8ae10b9f38aaad7689168b94335a514a9c30882f4a03daa3eb546cda83ea`
- Policy fingerprint:
  `0f30dea3a111d4d6ba13b68bb667338618c963ea5258049303a2492be73fc1ab`
- Evidence-set hash:
  `c252fd77fb2209cf65a5d47fbb3079218c6d1d196461c6f72573b3fcdd046ec5`

## Security model summary

- ProofPatch is the target's sole upgrader.
- Policy is immutable in v1.
- Candidate bytes/hash are frozen before review.
- Mutable branch URLs are rejected.
- Source/CI/audit publishers are policy-bound.
- Independent audit publisher ownership must differ from source publisher ownership.
- Evidence IDs cannot be replayed within their target/issuer/kind scope.
- Evidence has explicit publication, expiry, and maximum-age rules.
- Evidence/hash failures are repairable; transient provider failures are retryable.
- Leader and validators independently repeat the complete evidence + semantic review.
- Authorization-driving result fields match exactly.
- No fuzzy confidence/tolerance controls upgrade execution.
- Upgrade consequence is finality-bound.
- Target re-checks exact authorization and candidate bytes immediately before replacement.
- Installation is confirmed and reconciled against target-persisted metadata.
- Every locked/active path has expiry or recovery logic.
- Repository/deployment/source parity is a submission gate.

Read `docs/REVIEWER_GATES.md`, `docs/REVIEWER_COVERAGE_AUDIT.md`, and `docs/BRADBURY_FINAL_EVIDENCE.md` before submission.
