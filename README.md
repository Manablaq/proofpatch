# ProofPatch

**No code upgrade without consensus.**

ProofPatch is a GenLayer-native semantic upgrade firewall for Intelligent Contracts. A protected target makes ProofPatch its sole GenVM upgrader. An exact candidate can replace live code only after immutable source/evidence binding, independent semantic validator review, GenLayer finality, exact-byte installation, and post-install verification.

## Status

This repository is **Milestone 1: local core + adversarial Direct Mode suite + frontend prototype**.

It is deliberately **not** labeled deployment-ready yet. The next gate is an authoritative local GenVM lint/typecheck/schema + Direct Mode run on your machine. Cross-contract upgrade/finality behavior then moves to Bradbury integration verification rather than being faked in Direct Mode.

## Why this is GenLayer-native

A deterministic contract can compare hashes. It cannot safely decide whether arbitrary replacement source code semantically preserves human-written security invariants, avoids alternate privilege paths, retains evidence trust rules, and keeps consequential consensus correctly bound. ProofPatch puts that semantic judgment behind independent GenLayer validator consensus and uses the result to control GenVM's native code-upgrade capability.

## Repository

```text
contracts/
  proofpatch_governor.py         immutable semantic upgrade governor
  protected_target_v1.py        reference protected target
  protected_target_v2_safe.py   compatible safe candidate
  protected_target_v2_unsafe.py adversarial candidate; never deploy

tests/direct/
  test_proofpatch_governor.py
  test_protected_target_source_guards.py

tests/integration/
  README.md                      explicit Bradbury proof boundary

scripts/
  preflight.py                   lint + strict typecheck + schema + tests
  hash_source.py                 exact SHA-256
  build_evidence.py              canonical CI/audit envelopes
  verify_deployed_source.py      finalized RPC byte-for-byte parity

docs/
  ARCHITECTURE.md
  THREAT_MODEL.md
  REVIEWER_GATES.md
  BRADBURY_PLAN.md

frontend/
  index.html / styles.css / app.js
```

## First local run — macOS

Requires Python 3.12+ and Git.

```bash
cd ~/Downloads/proofpatch

python3 --version
git --version

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

python scripts/preflight.py
```

`preflight.py` is intentionally fail-fast. It runs, for each production contract:

- `genvm-lint check`
- `genvm-lint typecheck --strict`
- `genvm-lint schema`
- the complete `tests/direct` suite

and only writes `artifacts/local-preflight.json` if every step succeeds.

## Run only the Direct Mode suite

```bash
source .venv/bin/activate
pytest tests/direct -v
```

## Preview the frontend

No Node dependencies are needed for this first UI prototype:

```bash
cd frontend
python3 -m http.server 4173
```

Open `http://localhost:4173`.

The current frontend intentionally uses local demonstration data until real Bradbury governor/target addresses exist. We will bind it to live read/write calls only after the contract interface and deployment addresses survive the local and Bradbury gates.

## Source/deployment parity

Never resubmit an old Explorer deployment after correcting repository code.

```bash
python scripts/verify_deployed_source.py \
  --rpc YOUR_GENLAYER_RPC \
  --address 0xYOUR_DEPLOYED_CONTRACT \
  --source contracts/proofpatch_governor.py \
  --status finalized
```

Exit code `0` is required. It compares decoded deployed bytes, not merely a claimed hash.

## Security model summary

- ProofPatch is the target's sole upgrader.
- Policy is immutable in v1.
- Candidate bytes/hash are frozen before review.
- Mutable branch URLs are rejected.
- Source/CI/audit publishers are policy-bound.
- Independent audit publisher GitHub ownership must differ from source publisher ownership.
- Evidence IDs cannot be replayed within a target/issuer/kind.
- Evidence has explicit publication, expiry, and maximum-age rules.
- Evidence/hash failures are repairable; transient provider failures are retryable.
- Leader and validators independently repeat the complete evidence + semantic review.
- Authorization-driving result fields match exactly.
- No fuzzy confidence/tolerance controls upgrade execution.
- Upgrade message is emitted only on finality.
- Target re-checks exact authorization and candidate bytes immediately before replacing code.
- Installation is confirmed and reconciled against target-persisted metadata.
- Final submission requires byte-for-byte repository/deployment/Explorer parity.

Read `docs/REVIEWER_GATES.md` before any deployment or submission.

## Toolchain snapshot

The initial development requirements deliberately reference immutable Git commits for the GenLayer testing suite and GenVM linter. After the first successful Mac install, keep the resulting environment unchanged for the milestone and record its outputs in the repository.
