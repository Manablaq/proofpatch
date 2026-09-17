# ProofPatch v2 deployment packet

This packet is a release gate, not a deployment claim. The source freeze below is the exact commit to deploy if deployment is later authorized. No V2 deployment has been broadcast from this packet.

## Frozen identity

```text
branch: proofpatch-v2-development
release commit: 408bf82f0aa0f9848828b2c454e65d69c880be59
release tree: e8707f1419a283236e20e40709b592e018ebb20c
accepted-baseline: proofpatch-accepted-v1 @ f7fb6869cd6e53ddf460ae3145e0685ebd7ef815
```

The release commit is clean and its local preflight is passing. The documentation commit that records this packet must not be substituted for the release commit when source is deployed.

### Source SHA-256

```text
contracts/proofpatch_governor_v2.py              f6783610250367e3b914d74f27a228ecee4c1b5b6388c4289ad97160df6cd019
contracts/protected_target_v2.py                  3674e1f165dd1ff2f51305492d5cfe9c77c44d2a9d7014c0d133d555e761846e
contracts/protected_target_v3_safe.py             b1708f0e9899ce66a62250cc84d127aec1a24e3575b8922343af878312be2f78
contracts/protected_target_v3_recovery.py        5adbfa804d6cdb6720ffec5b4991daf1faca0df518d55280966def081e0d9a9d
contracts/protected_target_v3_latent_regression.py eeda91b273de786076471cbadf2827b95fbaeedfcffb3f0f089d0aa87778c752
```

### ABI SHA-256

```text
abi/proofpatch_governor_v2.json                  5147e57b088fede226cb2ab6c9355acbae75fdf64673fcbd6b6c506bdadafed2
abi/protected_target_v2.json                      1cb9bc2ba541ef466a59dc4acfc92663aef47dc425483781f289c075a5a842fe
abi/protected_target_v3_safe.json                 dcc4c7bc8eb64bfd46d725b6a9156d6612a382ca730afd69950c3e466b72fcdf
abi/protected_target_v3_recovery.json             dcc4c7bc8eb64bfd46d725b6a9156d6612a382ca730afd69950c3e466b72fcdf
abi/protected_target_v3_latent_regression.json    e20963b8c4541278fd25e966a10fca8b2cf0e33e76972948429d80465d62164f
```

### Schema and preflight SHA-256

```text
schemas/assurance-evidence-v1.schema.json         f8a1fd061ce788f0d40bb655c89a87993aa75948d5e617d84ea3954f89332f61
schemas/assurance-manifest-v1.schema.json         3e110fcdccecfb73e94424b5b303e4a0376637d2c7727bc4e45f79fe2f3f01cb
schemas/evidence-v2.schema.json                   8b9bf36d5f1171e9c17991d9812f6838ee98080728a4e16e3de6185d625a45e9
schemas/incident-evidence-v1.schema.json          1e6d103937d155d72ab3ff5360b48bbb93e054309c4fa6f43b5210966d2ac1a8
schemas/recovery-capsule-v1.schema.json           c3262ab4cb9d60e31b2b151a0631730382b32345bc5bd1b1a2d776fa84b1c536
artifacts/local-preflight.json                    03a67046dd4b54f01937ff8ed53b02267923540aeed256c0e679162681358f8b
```

## Network and signer

```text
network: testnet-bradbury (GenLayer Bradbury Testnet)
rpc: https://rpc-bradbury.genlayer.com
chain-id: 4221
signer candidate: worker / 0x1f87Ae197af539253978d435aD45cCf28Fb95024
expected nonce: capture with eth_getTransactionCount(..., "pending") immediately before submission
```

The signer candidate is an inventory observation, not a deployment authorization. The signer must be unlocked and explicitly selected before deployment. The pending nonce is intentionally not guessed; the RPC query must succeed immediately before submission. Never substitute a different wallet after the packet is frozen.

## Constructor and policy inputs

Record the exact governor and target source paths, constructor arguments, immutable authority prefixes, kernel hash, policy fingerprint inputs, and root release source/hash. Record the fee envelope and the transaction hash immediately after submission. The current source-only packet does not contain deployment addresses, receipts, finality, consensus, appeal, incident, or recovery claims.

## Required gates

- `scripts/preflight.py` passes from the frozen commit.
- All generated ABI and schema hashes match the packet.
- Deployment receipts reach finality; polling failure is resumed by transaction hash.
- `scripts/verify_deployed_source.py` passes byte-for-byte for both contracts.
- Finalized reads prove the sole governor upgrader, kernel hash, root release, policy fingerprint, and target bootstrap-to-active confirmation.
- Healthy certification, native appeal inspection, incident review, and recovery evidence are recorded before the address is published.

Until every item is filled with finalized evidence, the V2 addresses remain unset development artifacts and the frontend must continue showing `LIVE STATE UNAVAILABLE`.
