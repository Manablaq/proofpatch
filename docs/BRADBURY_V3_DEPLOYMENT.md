# ProofPatch V3 Bradbury Deployment

This record identifies the corrected modular ProofPatch graph deployed on GenLayer Bradbury. Every deployed contract is the matching compact artifact under `contracts/`; source parity was checked against the live Bradbury code.

## Network identity

```text
Network:  GenLayer Bradbury Testnet
Worker:   0x1f87Ae197af539253978d435aD45cCf28Fb95024
RPC:      https://rpc-bradbury.genlayer.com
Facade:   0x55101577bB1F78AAe18981eFE61b16C5a984b2c9
```

## Deployment graph

| Component | Address | Deployment transaction | Submitted artifact |
| --- | --- | --- | --- |
| Review engine | `0xD0dFE03E1bFe2EC221Cb505B6a9321e1dA2bD333` | `0x04ceef71a881988e670e3624c618f9b6dd759136ef8ab992aa7542d18a6b2313` | `proofpatch_review_engine_v2_compact.py` |
| Policy engine | `0x658Dc4E784836bB7C4Ae27029703C873fbb3D16a` | `0x3469be76d72dc62876c8747bc52aca704e6ec2170ae4167e9747d0b0b598eb67` | `proofpatch_policy_engine_v3_compact.py` |
| Registration engine | `0xFF9315eE07aB08F20224BAE4e85283B1DD5F73C5` | `0xfe7026bf10f4915e90a92c3fe3d6d698f10df92c002ebe041ba14f845e849a26` | `proofpatch_registration_engine_v3_compact.py` |
| Assurance engine | `0x4fD4Ce9733D96f0fF6BD53018d2bbdd5B86898dD` | `0xa51e2f129a61f1f8665347b9639ce7396e37a543a3c965bffa73cd3e3cf745ab` | `proofpatch_assurance_engine_v3_compact.py` |
| Summary engine | `0x232B09567e83Ed76F225f653b6D485381963578C` | `0x5efa6b26b6327e5d6264163c604d48e1998f21d4900fecce45eb86fa962a3320` | `proofpatch_summary_engine_v3_compact.py` |
| Lifecycle engine | `0x8948b524adbfA84eBDEb39bFF925695fF111FCbD` | `0xed51e7add65eb6fd5b86a8b23ff3af02528e2bb93c82af8a18160a276a0a0800` | `proofpatch_lifecycle_engine_v3_compact.py` |
| Lifecycle request engine | `0x6553ce6cca1C55789E119Bedf66C26Ff4617A0b1` | `0x976cc384b0f0bf58db719c382d8d4ee1a3b4d5bedb8e67c72408ac4b1eee7c6a` | `proofpatch_lifecycle_request_engine_v3_compact.py` |
| Review commit engine | `0x1240C476C1543D2156C57A8Ba16AF51052b5d039` | `0x48c892d8e11e5b11159cd704359a66907f23906f331cc56b3a2759f7a2aa1d97` | `proofpatch_review_commit_engine_v3_compact.py` |
| Review request engine | `0x692EF6b95D76eb7a5002B4aDEF446d0Acd6d25d5` | `0x8db55364b41068959cbfb36f107b3efab26375b6de30a863154316b30d1daba3` | `proofpatch_review_request_engine_v3_compact.py` |
| Final facade | `0x55101577bB1F78AAe18981eFE61b16C5a984b2c9` | `0x379c7e9f091a4861c0e947c99de4d55daf364d7bc73ef837976b99da9c3ba9c6` | `proofpatch_governor_v3_facade_compact.py` |

The facade is wired to the component addresses above. The lifecycle request engine is wired to the lifecycle engine, and the review commit engine is wired to the fresh review engine.

## One-time bindings

| Binding | Transaction |
| --- | --- |
| Policy governor | `0x0ff4d1ec7c83055c1d3243006315f8da88777c4df39041268717e87d6728105a` |
| Registration governor | `0xbef8d380fdab2492960af5173faa56d63f0b96a46c840b0b39f0f1899b629596` |
| Assurance governor | `0xde7dfdd9613ddaa66a64374cbc0296b1ef08aa183ce6b3e72da97c78b859827a` |
| Summary governor | `0x9b567446c0f40baae34824c7ca6535840ce5d629e83819eab8ec40b64e2f8b7c` |
| Lifecycle governor | `0xe21dcd9b9e4d47cfa6da6902c4aa56c6c696f2959f8c551eea025fcfdeae71f9` |
| Lifecycle request governor | `0x27fb01e8ca0f19baa17e69418c014eeeabee6bcccbdc7318cf2240a5237c8263` |
| Lifecycle executor | `0x2eae7c43d72235639a02b66cf1920d40a42a13f2fc5792c3dd3f6ba96e6b6840` |
| Review commit governor | `0xab2196bcab46e909f3b687ce47658d9f5c4994f9cdc6e3c4feff4625489d6465` |
| Review request governor | `0x0c06bd5b6c88e650024f0f5eb117ad3818dc9d9b4f5b3f6e291c1d2168c559e6` |
| Review engine governor | `0x1be520ffce598c7db25c6fafac07df135d5c040f194115b4c2e05a66ddd867d3` |

Every listed transaction returned `ACCEPTED / AGREE / FINISHED_WITH_RETURN` at submission. Finality is tracked separately from acceptance; the finalization receipts and finalized read smoke are recorded below when complete.

## Corrections included

- Cross-contract summary reads normalize keys before crossing the contract boundary.
- Missing records return an explicit `UNKNOWN` state instead of raising or fabricating a record.
- Runtime integer serialization uses runner-safe `bool` and `int` checks.
- Finality-sensitive authorization and readback paths retain `StorageType.LATEST_FINAL`; provisional reads cannot certify a release or clear an active slot.
- The compact artifacts preserve the readable interfaces and storage fields while staying within the Bradbury deployment size limit.

## Verification

The local verification gate passed:

```text
65 direct tests passed
All readable and compact V3 contracts passed GenVM lint
Python compilation passed
Frontend typecheck and production build passed
git diff --check passed
```

Live source parity passed for all ten deployed graph contracts. The retrieved Bradbury source matched its corresponding compact artifact byte-for-byte, including the policy engine’s V3 artifact.

## Finalization record

The deployment and binding transactions were accepted at the time of submission. Their appeal deadlines were tracked from each receipt’s `validUntil` field; the last deadline was `1789685439`. After that boundary, a direct `gen_getTransactionStatus` batch query returned `Finalized` with status code `7` for all 20 deployment and binding transactions.

The installed legacy CLI briefly reported a reverted explicit finalizer call with `TransactionNotAcceptedNorUndetermined` while the queue was being materialized. The authoritative status query was already terminal for every transaction, so no duplicate finalization call was submitted.

Finalized facade smoke results:

```text
get_proposal_count()                         -> 0
get_current_version(zero address)            -> ""
get_proposal_status(0)                       -> UNKNOWN
get_proposal_summary(0)                      -> {"status":"UNKNOWN"}
get_state_record("counts", "")              -> {"proposal_count":0,"release_count":0}
get_state_record("proposal", "0")           -> {"status":"UNKNOWN"}
```

These reads execute through the finalized modular graph. No fallback value is used to represent a contract-verified state.
