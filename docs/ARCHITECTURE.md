# ProofPatch Architecture

## Purpose

ProofPatch is a GenLayer-native semantic upgrade firewall. A protected Intelligent Contract designates the ProofPatch governor as its sole GenVM upgrader. Code replacement is therefore impossible through an owner key alone: an exact candidate must pass evidence verification, independent validator semantic review, Optimistic Democracy, finality, installation, and post-install confirmation.

## Trust chain

```text
Protected target
  -> immutable Upgrade Constitution
  -> exact frozen candidate bytes
  -> approved immutable source publisher
  -> CI evidence from registered CI publisher
  -> independent audit evidence from a distinct publisher
  -> freshness + expiry + stable evidence IDs
  -> leader independently fetches and analyzes
  -> validators independently fetch and analyze again
  -> exact agreement on all authorization-driving fields
  -> parent tx finalizes (native GenLayer appeal window remains available)
  -> target re-checks authorization and exact candidate bytes/hash
  -> GenVM code slot replacement
  -> finalized install confirmation
  -> governor verifies target's persisted install attestation
  -> VERIFIED
```

## Contracts

### `ProofPatchGovernor`

The governor is intentionally immutable in v1. It does not add any address to its own `root.upgraders` list and exposes no self-upgrade method.

Responsibilities:

- register a target's immutable policy;
- require exact immutable GitHub commit URLs under approved repository prefixes;
- require independent audit publisher ownership distinct from source publisher ownership;
- freeze exact candidate bytes before review;
- globally order proposals while isolating each target's active proposal;
- block evidence-ID replay within `(target, issuer, kind)`;
- independently fetch parent source, candidate source, CI evidence, and audit evidence;
- enforce exact SHA-256 bindings before semantic review;
- enforce evidence freshness and expiry;
- classify repairable evidence failures separately from transient review failures;
- run custom `run_nondet_unsafe` leader/validator review;
- compare the full authorization-driving semantic vector exactly;
- emit an upgrade message only with `on="finalized"`;
- confirm the installed exact candidate and advance current source/version/hash.

### `ProtectedTarget v1`

The example protected contract demonstrates the required integration pattern:

- owner is **not** an upgrader;
- ProofPatch governor is the sole upgrader;
- owner can request a finalized one-time policy registration;
- `proofpatch_upgrade` can only be called by the governor;
- it queries live authorization before reading candidate code;
- it hashes returned bytes again before installation;
- it persists proposal/hash attestation before code replacement;
- it emits finalized confirmation after replacement.

### `ProtectedTarget v2 safe`

Keeps the exact v1 persistent storage field order and the ProofPatch interface, while adding only a read feature.

### `ProtectedTarget v2 unsafe`

Never deploy this candidate. It is an adversarial review fixture containing an owner upgrade bypass and unrestricted state mutation.

## Consensus boundary

Only irreducibly semantic analysis lives inside nondeterminism. Storage writes and messages occur after `run_nondet_unsafe` returns.

The validator does **not** validate schema only. It independently executes the same complete evidence-fetch + binding + semantic-review function and compares:

- target;
- proposal ID;
- parent SHA-256;
- candidate SHA-256;
- policy fingerprint;
- evidence-set fingerprint;
- review kind/error class;
- decision;
- every semantic safety boolean.

Reasoning prose is intentionally not an authorization input. There is no fuzzy confidence threshold and no numeric tolerance controlling installation.

## Semantic vector

A candidate is approved only when every independently reproduced boolean is exactly `true`:

1. `storage_layout_compatible`
2. `user_rights_preserved`
3. `no_privilege_escalation`
4. `upgrade_authority_preserved`
5. `consensus_binding_preserved`
6. `evidence_trust_preserved`
7. `finality_safety_preserved`
8. `liveness_preserved`
9. `no_hidden_value_transfer`
10. `constitution_satisfied`

Any `false` deterministically derives `REJECT`.

## Evidence state repair

Immutable candidate bytes/hash never change during repair. When evidence itself is bad, the proposal moves to `EVIDENCE_REPAIR_REQUIRED`. The owner may supply new immutable evidence URLs and new stable evidence IDs, but may not alter target, parent, candidate bytes, candidate hash, or policy fingerprint.

Transient network/LLM failure moves to `REVIEW_RETRY_REQUIRED`; no authorization is granted and the same evidence can be reviewed again.

## Installation liveness

An approved proposal has an execution deadline. Target authorization checks the deadline immediately before installation. If the finalized child message never completes, the owner can reconcile a completed install or mark the execution timed out after the deadline. A late child message then fails authorization.

## Bootstrap trust

ProofPatch can cryptographically chain all later upgrades from the registered parent hash, but the first registration still needs proof that the submitted repository source is the exact deployed contract source. `scripts/verify_deployed_source.py` calls `gen_getContractCode` at `status=finalized`, base64-decodes the deployed source, and requires byte-for-byte equality with the local file.

That parity check is a mandatory deployment/submission gate, not optional documentation.
