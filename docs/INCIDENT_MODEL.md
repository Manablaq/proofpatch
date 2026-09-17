# ProofPatch v2 incident model

An incident is an append-only, release-bound challenge. Its type is an enum, and its primary/corroborating evidence URLs and IDs are immutable, fresh, target-bound, release-bound, and publisher-bound. Evidence must carry a complete incident boolean vector.

Incident review is permissionless but consensus-governed. Validators independently fetch both reports and compare the exact decision-bearing identity fields and booleans. A confirmed decision authorizes only the capsule hash already committed to the affected release. A dismissed decision restores an active release to `CERTIFIED` or a provisional release to `INSTALLED_PROVISIONAL` without deleting incident history.

Native GenLayer transaction lifecycle and appeal state belong to the transaction layer. The frontend uses the actual GenLayerJS appeal API and shows decided, appealable, appealed, under-review, and finalized separately. A provisional incident verdict never changes target code; the recovery message is emitted only from the finalized review outcome.
