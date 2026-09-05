# ProofPatch reviewer coverage audit

This file separates what is proved in Direct Mode from what must be proved
on Bradbury. ProofPatch does not fake IC-to-IC finality in unit tests.

## Frozen governor deployment already proved

- Network: Bradbury Testnet
- Deployment transaction:
  `0x238c570b475aa3c888f5ef81ba58c3d31ea0fd26195cd6a538f58c4bee2c254e`
- Governor:
  `0xc0100eFD567CD9dCcC8b9D17E381774fC4113ade`
- Frozen source commit:
  `cf97f0403706a3cbf3ec762052b514929f3d5173`
- Frozen source tag:
  `proofpatch-bradbury-candidate-v1`
- Governor SHA-256:
  `3f6f3b2c75582a47230a1d860d79645a16428000ae60f695deba878bf55fdcde`
- Stored deployment status was independently read as `Finalized` / `7`.
- Finalized receipt execution result was `1` (`FinishedWithReturn`).
- `gen_getContractCode` with `status=finalized` was decoded and compared
  byte-for-byte with both the local contract and immutable tag source.

## Direct Mode proof

The Direct Mode suite is responsible for deterministic policy and consensus
logic that does not require an actual cross-contract finalized message.

Covered after the reviewer-coverage patch:

- immutable, publisher-bound source/CI/audit authority policy;
- independent audit GitHub publisher;
- rejection of mutable branch URLs;
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
- retry state recovery through a fresh review;
- repair with fresh immutable URLs and fresh evidence IDs while candidate
  bytes/hash remain unchanged;
- stale evidence cannot authorize;
- evidence identity is isolated by target;
- mutation of one consequential consensus binding causes validator disagreement;
- an exact all-true approval vector is accepted by the captured validator
  only when every binding and semantic boolean matches.

## Bradbury-only proof boundary

The following remain network integration gates because Direct Mode does not
support real IC-to-IC calls/finality:

1. Deploy and byte-verify `ProtectedTarget v1`.
2. Register the target and prove the finalized registration child executes.
3. Query and archive policy fingerprint, current version and current hash.
4. Publish immutable source, CI and independently-owned audit evidence.
5. Submit the exact safe-v2 bytes and run a real all-true validator review.
6. Prove the review reaches `UPGRADE_QUEUED`.
7. Preserve appeal/accepted/finalized lifecycle evidence.
8. Prove exactly one finalized child upgrade executes successfully.
9. Prove the target re-reads authorization and exact frozen candidate bytes.
10. Prove the finalized install callback reaches `VERIFIED`.
11. Prove storage and ProofPatch interface compatibility after upgrade.
12. Prove governor current version/hash changes only after install confirmation.
13. Prove finalized target source equals exact safe-v2 repository bytes.
14. Run an unsafe candidate negative proof with real semantic rejection or
    validator disagreement.
15. Prove expired/stale authorization cannot install code.
16. Prove execution timeout/recovery if a queued child cannot complete.
17. Archive successful execution result fields, transaction IDs and Explorer
    links for every consequential step.

## Stop rule

Do not call ProofPatch submission-ready until every applicable Bradbury-only
gate above has recorded evidence. `Accepted` is never described as
`Finalized`, and `Finalized` is never treated as execution success without
the execution result.
