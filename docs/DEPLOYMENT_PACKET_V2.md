# ProofPatch v2 deployment packet

This packet is a release gate, not a deployment claim. It must be completed from one frozen commit and consumed once for the canonical V2 deployment.

## Frozen identity

```text
branch: proofpatch-v2-development
commit: <fill after release freeze>
tree: <fill after release freeze>
accepted-baseline: proofpatch-accepted-v1 @ f7fb6869cd6e53ddf460ae3145e0685ebd7ef815
```

Record SHA-256 for the governor, target, recovery fixture, schemas, generated ABI, and the passing `artifacts/local-preflight.json`.

## Network and signer

```text
network: <exact GenLayer network name>
rpc: <canonical RPC URL>
chain-id: <exact chain ID>
deployer: <wallet address>
expected nonce: <nonce>
```

The signer must be unlocked and explicitly selected before deployment. Never substitute a different wallet after the packet is frozen.

## Constructor and policy inputs

Record the exact governor and target source paths, constructor arguments, immutable authority prefixes, kernel hash, policy fingerprint inputs, and root release source/hash. Record the fee envelope and the transaction hash immediately after submission.

## Required gates

- `scripts/preflight.py` passes from the frozen commit.
- All generated ABI and schema hashes match the packet.
- Deployment receipts reach finality; polling failure is resumed by transaction hash.
- `scripts/verify_deployed_source.py` passes byte-for-byte for both contracts.
- Finalized reads prove the sole governor upgrader, kernel hash, root release, policy fingerprint, and target bootstrap-to-active confirmation.
- Healthy certification, native appeal inspection, incident review, and recovery evidence are recorded before the address is published.

Until every item is filled with finalized evidence, the V2 addresses remain development artifacts.
