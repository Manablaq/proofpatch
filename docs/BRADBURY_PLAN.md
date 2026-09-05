# Bradbury Verification Plan

Do this only after `python scripts/preflight.py` is completely green.

## Deployment order

1. Deploy `ProofPatchGovernor`.
2. Record exact local source SHA-256.
3. Verify finalized deployed governor source with `scripts/verify_deployed_source.py`.
4. Deploy `ProtectedTarget v1` with the governor address.
5. Verify finalized deployed target source with the same parity script.
6. Call target `register_with_proofpatch(...)` using the reviewed immutable constitution and authority prefixes.
7. Wait for the registration parent and generated governor child transaction to finalize successfully.
8. Query the governor fingerprint and current hash/version.

## Safe upgrade proof

1. Commit `protected_target_v2_safe.py` to an immutable source commit.
2. Run full lint/typecheck/schema/Direct tests against the exact committed candidate.
3. Publish CI evidence at an immutable approved CI commit.
4. Obtain independent audit evidence from the registered distinct audit publisher.
5. Create the proposal using the **exact bytes** of the committed candidate.
6. Review it.
7. Capture receipt lifecycle and execution result.
8. Keep the appeal path visible until the review finalizes.
9. Confirm the finalized child upgrade transaction executes successfully.
10. Confirm the finalized install callback executes successfully.
11. Query `VERIFIED`, current version/hash, and target install metadata.
12. Run finalized source parity against the target and ensure it equals the exact v2 candidate file.

## Negative proof

Run a separate proposal using `protected_target_v2_unsafe.py` or an equivalent immutable adversarial candidate. Validators must not be treated as compatible if one approves and another rejects a privilege-changing semantic outcome.

## Evidence archive

For submission, preserve:

- repository commit SHA;
- governor source SHA-256;
- target v1 source SHA-256;
- candidate source SHA-256;
- policy fingerprint;
- evidence-set hash;
- immutable evidence URLs and IDs;
- deployment addresses;
- finalized RPC source-parity output;
- review transaction receipt;
- generated upgrade child receipt;
- install confirmation receipt;
- successful execution result fields;
- Explorer URLs for the **matching final deployments**.
