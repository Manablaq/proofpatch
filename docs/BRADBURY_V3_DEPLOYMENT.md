# ProofPatch V3 Bradbury Deployment

## Canonical V3 release — 2026-09-20

Facade: `0x46eE236d3812A4c71F09eBdf641963bFc6ea8c6D`

Protected target: `0x9e8ACf20747B8d18D54b3c45e0510003029BCf4f`

Root release: `root-9da36f69837321c9`

Target mode: `ACTIVE`

Registration closure: five of five consequential GenLayer transactions finalized successfully. Exact policy/root materialization passed. All older graph records below are historical provenance.


## Current corrected graph

The current submission is the corrected graph below. The previous graph in the historical section was superseded after an audit found that its compact facade omitted two review callback address constants. Every address below was freshly deployed from the compact artifact named in the last column, and every governor/executor binding was submitted with a state-changing `genlayer write` transaction.

```text
Network:  GenLayer Bradbury Testnet
RPC:      https://rpc-bradbury.genlayer.com
Worker:   0x1f87Ae197af539253978d435aD45cCf28Fb95024
Facade:   0x1DB03E1F4D7F1F9af5C6f0Abc1A320CA2506F4A6
Facade deployment: 0x1925ad0f82726902391397a99837f607db9bcea8b1afbe29a90f87bf324879c9
```

| Component | Address | Deployment transaction | Artifact |
| --- | --- | --- | --- |
| Proposal review | `0x9840cCf5DBdf4AE5945Ca73367e8336cCBEF578e` | `0x22fb47f32562c30d7656206a346d4c04976e27544b6d3b07146c7a6227bece54` | `proofpatch_review_engine_v2_compact.py` |
| Fact review | `0x32E5eFAF7558B65f72dA2B2B27f040e74fA148BC` | `0x30fdf5c8b33270820edb9337d13deac67f5a2ae6d30b174bbd8546908f59a274` | `proofpatch_fact_review_engine_v3_compact.py` |
| Create policy | `0xCe91B262d6358dFd95A32a56fd577b71FB0DdC7F` | `0x612284169c8f60f6ccab30dd51e42c1334603d175537224796d675337f8585ec` | `proofpatch_policy_engine_v3_compact.py` |
| Repair policy | `0x59A065F97a4d475Fc60AC350aDF5163AbfE27F91` | `0x1ba87b1e9cb28d85445899ac62cea36ddb492ccd9eac4fdf698da3922d21e41c` | `proofpatch_repair_policy_engine_v3_compact.py` |
| Incident policy | `0x3De9294a39A4b9e31975a74426a3f29C32E0829E` | `0x3c7cf80c6be2e616fa2dba9ea2a7026a53f0011533068dad590fbbf0975e997b` | `proofpatch_incident_policy_engine_v3_compact.py` |
| Registration | `0xF7e1F1D31f60e866E2f0a1367834BEF7abC77b43` | `0xbeaf4bc538db0692d94fbd548e86c843476a83e33d48eda7a3511e3ece12f120` | `proofpatch_registration_engine_v3_compact.py` |
| Assurance | `0x6740374AA335c4e02EC079d3d1E5A2198A28320F` | `0x39a4ac2a4513789d31ab80f725aa542e4d0287937770f36a3b6b4486b89bb3b5` | `proofpatch_assurance_engine_v3_compact.py` |
| Summary | `0x209343F604Ec7A53339C3F555D5Cf333F4BEf4FD` | `0x3e50f76583ea3b5a9157a7de4690978667f973c8ff0c063e31737720b8b6e45b` | `proofpatch_summary_engine_v3_compact.py` |
| Install lifecycle | `0xE7F337c2Bc992a94f213C41B66d7E49381F31145` | `0x24eb93f23e5ff04af26b455cb599cf1f764aaffdeea5eade9cff59c1f74b70c4` | `proofpatch_lifecycle_install_engine_v3_compact.py` |
| Timeout lifecycle | `0xd73FF76b1A2438eAD59DA4072F9484aED25C7865` | `0xc14e73bd985b56e484782d8d480ff9ec1afbfdff5f0f9aa7636e533239c9d158` | `proofpatch_lifecycle_timeout_engine_v3_compact.py` |
| Activation lifecycle | `0x429A733D5949bCB0DE97E32Da58E8d192acC41Ca` | `0x8c278ad5c07d8d8c3804b20bd1e23bb3a8df1baaaf0d4f7bad057534b6d2072c` | `proofpatch_lifecycle_activation_engine_v3_compact.py` |
| Recovery lifecycle | `0xebf47F06759481606910dA564FF48203e386b95E` | `0xd146bcf878c2352d58bad59c070ad9f8bf5460e7b3f437ee5ebe8765dbd6a844` | `proofpatch_lifecycle_recovery_engine_v3_compact.py` |
| Lifecycle request | `0xC01B9D36B3eEe2A563A4E7FA688b9a799fa759E2` | `0x4a2eb20cf3e57f7df2dc3aee141cc757a460e5e23ce0e8aa7db00171deb9bc90` | `proofpatch_lifecycle_request_engine_v3_compact.py` |
| Review commit | `0xef8F5C807117b2A606B861e947F2ff5756Db8CE7` | `0xb366c52016bedea170dacfbdfc0e746c6862e22ec78ca0c300c3f5e93dd4bc75` | `proofpatch_review_commit_engine_v3_compact.py` |
| Review request | `0x50d787E2078683Bbc27462208475578cE7295aF9` | `0x0eecac51106535ccb933eb3e8c3009c95e1bcf9b2f1c063c8b459a18493b4966` | `proofpatch_review_request_engine_v3_compact.py` |
| Corrected facade | `0x1DB03E1F4D7F1F9af5C6f0Abc1A320CA2506F4A6` | `0x1925ad0f82726902391397a99837f607db9bcea8b1afbe29a90f87bf324879c9` | `proofpatch_governor_v3_facade_compact.py` |

Canonical successful governor bindings to the corrected facade for all 15 components:

| Component | Governor binding transaction |
| --- | --- |
| Proposal review | `0xa0b9a46ad71eb60b4acf3656c97bb96e554c678cea432ad40d2070b623b6ae95` |
| Fact review | `0xda2c1cfbe54d9a98677f5420b8118dbf4496584222617bd61f7438b538900af6` |
| Create policy | `0x2a01d1b4afa875291d16288063b995bcfcc33d5c22ecd8b279882048982f8047` |
| Repair policy | `0x3ab7033cbaeb89d0a22406af07a430e9970a50908616a64843c5505c2e9afb4b` |
| Incident policy | `0xb0b7ceada695f80938abb2ad394d274e3aeaedfc7c84798b5329c8c56c830443` |
| Registration | `0xa883c0bbe3218dd4464237d8b57d05145ebfd78bf2be1db8a065e563cee1d36c` |
| Assurance | `0xf34ada0952608118f2dba09e814c22a58f69dcbc54f2cb3e035c7e7b9a64a0b1` |
| Summary | `0xfc8f5f4fe6bd42a9b4b8f7f8d35007da72854e980dc28a834545565b61edb6a2` |
| Install lifecycle | `0x332c3c965fb9ab56f3a4008e04cedf38a61bfd6f13c4f6a204b1c78c259a37f8` |
| Timeout lifecycle | `0x660d2565c5dac102c9c03b958e1bd1ed3eb921017b448f65c23578e9dd02ffa3` |
| Activation lifecycle | `0x79baf6748367311db3457606c6c7b146095b76a2b46046870f26e00d7156f4b9` |
| Recovery lifecycle | `0xf8d6a97d447ba88f490fd0ec50d68f05f913754e6fd1781bdb5f4c2ed14dad67` |
| Lifecycle request | `0x0eb6d17a1c7f883198f093c26dac2ebd05ed71e60cc0ba367707f1e1e86dd9ca` |
| Review commit | `0xb16939950fda023b90c3424380ec63b6068846c6cfdb7ed012122fce303057b6` |
| Review request | `0x213cc88fbe89c2bf104119666e8d7c07826e5ca749ffb9c87b352b3a2be271c8` |

Lifecycle executor bindings use the worker wallet:

| Executor | Binding transaction |
| --- | --- |
| Install lifecycle | `0x3b4f966de25b5ab7c221d3b187dfffd48b855f4dff7221a98b724d74d33b296f` |
| Timeout lifecycle | `0x2476c5ea7eafe75ba025b0c97f68adda1c3d8a736cdde2850ec7378dab2049e2` |
| Activation lifecycle | `0x4a05ca78bc995efe53066cfd9e077d4608435588620f94ada3c3e7a86414a89e` |
| Recovery lifecycle | `0x3930e8563bfe34db62205dea74c73b778ec8cdc92548c463f74efd629f2b8e2f` |

Local verification is complete: 71 direct tests passed, the full GenVM preflight passed, the frontend typecheck/build passed, and source parity passed for all 16 fresh artifacts at accepted state. Direct `get_state_record("counts", "")` returns `{"proposal_count":0,"release_count":0}`. Finality-sensitive summary reads fail closed while the deployment is still `ACCEPTED`; no fallback value is presented as verified state.

The canonical 35-transaction graph (16 deployments, 15 governor bindings, and 4 lifecycle executor bindings) has been rechecked from live Bradbury receipts: every transaction is `Finalized` with `FinishedWithReturn`. The regenerated `artifacts/bradbury-v3-finality.json` records those receipts. Twelve later duplicate/rebind attempts are intentionally excluded from the canonical binding table because they finalized with `FinishedWithError`; the historical governor-history diagnostic preserves those retries. Finalized source parity and the fresh-target V3 lifecycle proof remain separate release gates.

## Historical deployment record

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
