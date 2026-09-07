# Reviewer Readiness Gates

A release is **not submission-ready** unless every applicable gate below passes.

| Gate | Required proof |
|---|---|
| Evidence provenance | Exact approved source/CI/audit publisher identities and immutable repository prefixes are policy-bound. |
| Immutability/versioning | Every source/evidence URL must use the canonical approved raw-GitHub prefix, an exact lowercase 40-hex commit, and parser-stable ASCII path segments. Dot segments, percent encoding, backslashes, repeated separators, queries/fragments, and mutable branches are rejected before fetch. |
| Freshness | Evidence publication/expiry values satisfy the registered maximum age. |
| Independent corroboration | Audit publisher owner differs from source publisher owner; audit verdict and independence flag are bound. |
| Stable evidence identity | Evidence IDs are non-reusable within target/issuer/kind. |
| Correctable failures | Hash/4xx/envelope failures become `EVIDENCE_REPAIR_REQUIRED`; transient fetch/LLM failures become `REVIEW_RETRY_REQUIRED`. |
| Consensus → consequence | Target, proposal, parent hash, candidate hash, policy fingerprint, evidence-set hash, semantic vector and final decision are exact-match fields. |
| No fuzzy payout/authorization | No tolerance or confidence range can authorize installation. |
| Independent validator substance | Validator repeats the evidence fetch and semantic policy application; shape-only checks cannot pass. |
| Bypass resistance | Target owner is not an upgrader; candidate review explicitly checks alternate privilege/upgrade paths. |
| Storage compatibility | Safe fixture preserves exact storage field order; CI must run compatibility/interface regressions. |
| Finality | Upgrade child message is emitted only `on="finalized"`. |
| Appeal visibility | UI surfaces accepted/appealable/finalized states separately; no claim that accepted equals final. |
| Liveness | Proposal expiry, review retry/repair, execution deadline, timeout and reconciliation paths exist. |
| Cross-case isolation | Proposal/evidence keys bind their target and exact evidence set. |
| Post-review response | Repair creates a fresh review using new evidence IDs without changing candidate bytes/hash. |
| Post-install verification | Target persists installed proposal/hash; governor checks both before `VERIFIED`. |
| Repository/deployment parity | Finalized `gen_getContractCode` bytes equal submitted source exactly. |
| Explorer parity | The Explorer link used in submission must point to that exact corrected deployment, never an earlier one. |
| Adversarial regression | Unsafe privilege, evidence, semantic disagreement, replay, stale, timeout and source-mismatch scenarios are tested. |
| Execution result | Finality and successful GenVM execution are both checked on Bradbury receipts. |

## Stop rule

If any gate fails, do not submit and do not describe the project as reviewer-ready.
