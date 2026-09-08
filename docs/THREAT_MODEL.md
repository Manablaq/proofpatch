# ProofPatch Threat Model

## Assets

- the protected target's executable source code;
- persistent target storage and user rights;
- the immutable upgrade constitution;
- approved publisher boundaries;
- candidate/source/evidence bindings;
- finality-safe upgrade authorization;
- integrator trust in `VERIFIED` releases.

## Adversaries

- compromised or malicious target owner;
- malicious proposal author;
- malicious leader;
- validator disagreement or provider variance;
- compromised evidence endpoint;
- stale/mutable evidence;
- coordinated but non-independent sources;
- prompt injection embedded in source/comments/evidence;
- delayed/replayed cross-contract messages;
- evidence replay across proposals;
- old deployment submitted after repository correction;
- malicious candidate that preserves obvious APIs while adding an alternate bypass.

## Defenses

### Admin bypass

The protected target adds only ProofPatch to `root.upgraders`. Owner is intentionally excluded. The review checks preservation of that design and CI must assert ProofPatch interface compatibility.

### Mutable, stale, or parser-aliased evidence

All accepted source/evidence URLs must use a single canonical raw-GitHub representation: an approved canonical repository prefix, an exact lowercase 40-hex Git commit, and parser-stable ASCII path segments. Dot segments (`.` / `..`), percent-encoded aliases, backslashes, repeated separators, queries/fragments, control/space aliases, and mutable branch paths are rejected before the URL reaches GenVM's HTTP parser. Evidence envelopes carry publication and expiry times and must be within the policy's maximum age.

### Hash without provenance

A SHA-256 is never treated as authority. Each policy binds exact source, CI, and audit publisher identities/repository prefixes. Audit ownership must differ from source publisher ownership.

### Evidence reuse

CI and audit evidence IDs are stable identifiers and cannot be reused for the same target/issuer/kind, even after cancellation or repair.

### Cross-case contamination

Each proposal binds target, parent, candidate, policy fingerprint, and evidence-set fingerprint. Active proposal state is per target. Evidence replay keys include target and issuer.

### Shape-only validator

The validator independently repeats the full source/evidence retrieval and semantic analysis. Exact result-vector comparison is required.

### Tolerance changes consequences

No confidence/tolerance value controls approval. Approval is deterministic from an exact boolean vector.

### Prompt injection

The semantic prompt explicitly labels source, candidate, comments, strings, and constitution text as untrusted data. Embedded instructions cannot redefine the review role. The review specifically searches alternate paths and semantic bypasses.

### Time-of-check/time-of-use candidate substitution

Candidate bytes are stored when the proposal is created. Review verifies the immutable source URL hashes to those exact bytes. Target later retrieves those same stored bytes from the governor, hashes them again, and installs only if the exact authorization remains live.

### Accepted-before-finalized side effects

Upgrade messages use `on="finalized"`. ProofPatch also refuses to promote provisional cross-contract state on the return path: `confirm_install` and `reconcile_install` read the target with `StorageType.LATEST_FINAL`. Timeout recovery first checks finalized target state and may use `LATEST_NON_FINAL` only to detect an installation that is still pending finality. A non-final-only candidate can never produce `VERIFIED`, update the current policy hash/version, or release the active proposal slot.

### Lost or delayed child message

Authorization expires. Late installs fail. An exact finalized install whose confirmation child was delayed/lost can be reconciled. If the exact candidate exists only in non-final state, timeout fails closed and keeps the active proposal locked until finality resolves.

### Source/deployment mismatch

Submission is blocked unless `scripts/verify_deployed_source.py` reports byte-for-byte parity against finalized deployed code.

## Explicit v1 assumptions

- GitHub/raw.githubusercontent.com HTTPS namespace control is the publisher authentication mechanism in v1. An approved repository is an approved publisher. A later version may add cryptographic detached signatures, but signatures are not falsely claimed today.
- Independent corroboration means the audit raw-GitHub owner must differ from the source publisher owner. Organizational independence beyond namespace ownership remains an integrator governance choice and is documented, not hidden.
- Semantic code analysis is consensus-governed judgment, not a formal proof. Adversarial regressions and native appeals remain important.
- The first parent deployment must pass the external finalized-source parity check. Later parent hashes are chained from previously verified installations.
