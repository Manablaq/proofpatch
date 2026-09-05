# Integration test boundary

ProofPatch deliberately does **not** fake IC→IC finality in Direct Mode.

The Bradbury integration suite will be added after the first local GenVM lint/Direct Mode pass and will prove, with real transaction receipts:

1. `ProtectedTarget.register_with_proofpatch()` emits a finalized registration to the governor.
2. An all-true, independently agreed semantic review queues exactly one finalized upgrade message.
3. The target re-reads the exact frozen candidate bytes and exact authorization before replacing code.
4. The upgraded target preserves storage and ProofPatch interface compatibility.
5. The finalized callback moves the proposal from `UPGRADE_QUEUED` to `VERIFIED`.
6. The governor's current code hash equals the installed candidate hash.
7. Acceptance is **not** treated as successful execution; receipts must show successful contract execution and finality.
8. Old/stale/expired authorizations cannot install code.
9. The repository source hash, deployed source returned by RPC, and submitted Explorer contract all match.

This boundary is intentional: Direct Mode is for deterministic/consensus unit behavior; Bradbury is the source of truth for cross-contract message/finality behavior.
