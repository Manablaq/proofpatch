# ProofPatch Reviewer Coverage Audit

This audit separates deterministic test coverage, canonical Bradbury evidence, and future/disposable adversarial paths. It intentionally does not fake IC-to-IC finality in unit tests and does not replay a completed canonical live upgrade merely to create extra transactions.

## Reviewer hard gates

| Gate | ProofPatch control |
|---|---|
| Evidence provenance | Source, CI, and audit publishers/repository prefixes are policy-bound. |
| Immutable/versioned evidence | Canonical raw-GitHub URLs require an exact lowercase 40-hex commit and parser-stable ASCII path segments; mutable branches and URL-normalization aliases are rejected before fetch. |
| Freshness/corroboration | Publication/expiry/max-age rules and independent audit corroboration are enforced. |
| Correctable evidence failure | Repairable failures enter `EVIDENCE_REPAIR_REQUIRED`; transient review failures enter `REVIEW_RETRY_REQUIRED`. |
| Liveness/recovery | Proposal expiry, repair/retry, execution deadline, reconciliation, and timeout paths prevent indefinite lock. |
| Exact consensus-to-consequence | Consequential target/proposal/hash/policy/evidence/semantic fields are exact-match inputs; there is no tolerance-based authorization. |

## Deterministic Direct Mode coverage

The Direct Mode suite covers deterministic policy/consensus logic that does not require an actual finalized IC-to-IC message:

- immutable, publisher-bound source/CI/audit authority policy;
- independent audit publisher;
- rejection of mutable branch URLs;
- rejection of dot-segment, percent-encoding, backslash, repeated-separator, uppercase-commit, and other URL-canonicalization aliases;
- owner-only proposal creation;
- exact frozen candidate bytes and SHA-256 binding;
- evidence-ID replay prevention;
- repairable candidate/source/hash and HTTP 4xx failures;
- retryable HTTP 5xx and malformed LLM failures;
- strict evidence timestamp and identity types;
- semantic rejection and target release;
- validator independent re-execution;
- exact full-result validator agreement;
- proposal expiry and active-target release;
- retry state recovery through fresh review;
- evidence repair with new immutable URLs and fresh evidence IDs while candidate bytes/hash remain unchanged;
- stale evidence cannot authorize;
- evidence identity is target-scoped;
- mutation of consequential consensus bindings causes disagreement;
- all-true approval requires exact consequential agreement;
- target constructor/address boundary regression;
- adversarial privilege, evidence, replay, stale, timeout, and source-mismatch cases.

## Canonical Bradbury proof — complete safe path

The canonical live safe-v2 path is complete.

- Governor:
  `0xc0100eFD567CD9dCcC8b9D17E381774fC4113ade`
- Protected target:
  `0xe7165dEA0F712E3161ADa773c41755d79F1e696B`
- Proposal:
  `1`
- Final status:
  `VERIFIED`
- Last review/install code:
  `INSTALL_VERIFIED`
- Active proposal:
  `0`
- Current version:
  `2.0.0`
- Current candidate hash:
  `013f8ae10b9f38aaad7689168b94335a514a9c30882f4a03daa3eb546cda83ea`

The completed live path demonstrates:

1. finalized target registration;
2. immutable policy/source binding;
3. exact safe candidate proposal;
4. real GenLayer semantic validator review;
5. review finality;
6. generated child upgrade execution;
7. target-side exact authorization/candidate re-check;
8. exact code installation;
9. finalized install confirmation;
10. governor transition to `VERIFIED`;
11. final active-slot release;
12. preserved target invariants.

Canonical transaction IDs are recorded in `BRADBURY_FINAL_EVIDENCE.md`.

## Frontend reviewer boundary

The Next.js frontend uses live Bradbury finalized reads and deliberately distinguishes:

- submitted transaction;
- consensus running;
- accepted/finality pending;
- finalized;
- GenVM execution result;
- canonical proposal/target reconciliation.

Safety controls include:

- owner recognition and wrong-wallet read-only behavior;
- no manual `proofpatch_upgrade` button;
- no manual `confirm_install` button;
- no manual finalization button;
- Proposal #1 permanent write lock;
- immutable candidate/evidence preflight;
- duplicate pending-transaction guard;
- persisted transaction hash tracking;
- state-aware review/repair/cancel/expire controls;
- exact-target-gated reconciliation;
- deadline + target-state-gated execution timeout.

## Paths intentionally not replayed on the canonical target

The unsafe candidate negative path and a deliberately failed queued-child timeout path are not replayed against Proposal #1.

Reason:

- Proposal #1 already completed successfully.
- Repeating review/upgrade/confirmation would be invalid and reviewer-hostile.
- Creating a destructive timeout condition on the verified target would manufacture failure rather than verify the completed canonical safe path.
- Equivalent adversarial/liveness semantics are covered deterministically.
- If a reviewer explicitly requires another live destructive path, it should use a separate disposable target and fresh proposal/evidence identities.

## Stop rule

Do not describe `Accepted` as `Finalized`.

Do not describe `Finalized` as execution success unless the execution result also proves success.

Do not repeat a successful canonical write merely because UI state, indexing, or consensus finality takes time.

Do not call Proposal #1 review, upgrade, confirmation, reconciliation, timeout, expiry, repair, or cancellation actions again.
