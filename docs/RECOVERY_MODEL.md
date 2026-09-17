# ProofPatch v2 recovery model

Every upgrade carries a capsule before installation. The capsule is either the exact current certified parent or a separately identified recovery candidate. The governor stores its bytes and hash; the target retrieves and hashes the bytes again immediately before replacing code.

Recovery authorization is bound to the incident, affected release, and capsule hash. If the target no longer holds the affected release, the authorization is stale. If recovery code or target metadata differs, the operation fails closed. The target persists the recovery attestation before code replacement and emits finalized confirmation. The governor only records `RECOVERED` after a finalized readback proves the exact release/hash/mode.

The contract does not invent a rollback target after an incident. The capsule is part of the pre-install consensus input and appears in the proposal summary, evidence-set hash, release record, and lineage hash. `EXACT_PARENT` restores the parent release identity; `RECOVERY_CANDIDATE` creates a new recovered release record with the affected release as its parent. Recovery confirmation has a separate execution deadline, and finalized target state can be reconciled or retried without granting a new recovery choice.
