# ProofPatch V3 — Final Bradbury Reviewer Evidence

This is the canonical reviewer-facing evidence record for the repaired ProofPatch V3 Bradbury release.

## Canonical live release

- Network: Bradbury Testnet
- Chain ID: `4221`
- Facade: `0x46eE236d3812A4c71F09eBdf641963bFc6ea8c6D`
- Protected target: `0x9e8ACf20747B8d18D54b3c45e0510003029BCf4f`
- Registered owner: `0x1f87Ae197af539253978d435aD45cCf28Fb95024`
- Version: `2.0.0`
- Root release: `root-9da36f69837321c9`
- Root status: `REGISTERED_PARENT`
- Target mode: `ACTIVE`
- Proposal count: `0`
- Active proposal: `0`
- Target source SHA-256: `9da36f69837321c9688e6ec338dbdfbfd085a9f387361e7bb2c37037f353c9fe`
- ProofPatch kernel SHA-256: `8a5f9c864d80aa10fdcd8f2878cf5bcd3ff28e0cdb62ab11043668e215e7a930`
- Policy fingerprint: `d090b20e2eb4deeff39cc295c703b431fb7631bfb64941d80405b37c85963607`

## Repaired failure mode

The superseded graph reached the final registration confirmation path but failed while serializing storage-backed Slot fields. The compact facade now serializes declared fields through explicit attribute access. The repaired path is regression-covered and the failed graph is historical only.

## Natural-finality registration chain

All five consequential transactions independently reached Finalized with result 1 and successful execution:

1. `register_with_proofpatch` — `0xf01abff0c3f27998c0da2e212a51931ad4422ab5d4cd5ffec0b837f21d1befe9`
2. `register_target` — `0x266f30fb932aafbccb5891ca26478baea1cc0826c587a2ab8bb25facdac511ad`
3. registration-engine `execute` — `0x93493791c5a6c1b4f2c61844d25cacd8e87f39ac5889d3d8758f1e13c045ec70`
4. `apply_policy_result` — `0xa1ce343c1688372527b94e0806eed01150be88de993a3380aef6091ab038b084`
5. `proofpatch_confirm_registration` — `0x35824ed9d44dda5c25d778c009c77854b0d580e37378aa0e156dec2b2ddccfe4`

The single outer EVM registration transaction was `0x42338065634a57097b9ff051eb3167bd87993ebd4e963314fcac006d7f5208f0`. Its receipt status was 1 and the authorized nonce advanced exactly from 1327 to 1328.

After the fifth finalization, every frozen policy field matched, the root release was `REGISTERED_PARENT`, and the protected target was `ACTIVE`.

No retry, rebroadcast, replacement, alternate ABI path, or manual finalize was used.

## Reproducibility anchors

- Binding-wave plan SHA-256: `9f48ded9277e33a41617fb788a881b8901ed4f064b94e42b1eda22f8a1580071`
- Target-deployment plan SHA-256: `7e7f125493d2c5223ccbc9c3aa338bbeebdbf97c14f0b1bced2b15659a56760e`
- Registration plan SHA-256: `6f3a8a7521e620176999c83054f120fb817a119b9a4063781c1eb8f8564ee5cb`
- Registration app-data SHA-256: `47d1c2bdc8c8cddb62d411612aff26e6653220384ad0c8cb4c35cab5097139ae`
- Closure artifact SHA-256: `8520e6c71a40a834722aef1ad567d119b7f449d6f479b88975f8eda045b35af9`
- Closure manifest SHA-256: `fdc58cdc1828762dda6a68a351bcc2da307bd6a9d34806a314585b73a2443c3f`

## Production

Production application: `https://proofpatch.vercel.app`

The reviewer-facing `/app` and `/v3` routes use the canonical V3 facade and protected target. The `/legacy` route remains historical.

## Machine-readable evidence

- `deployments/bradbury-v3-canonical.json`
- `artifacts/bradbury-v3-release/registration-closure-success.json`
- `artifacts/bradbury-v3-release/final-registration-state.json`
- `artifacts/bradbury-v3-release/registration-chain.json`
- `artifacts/bradbury-v3-release/registration-execution-summary.json`
- `artifacts/bradbury-v3-release/fresh-registration-preauth-r2.json`
- `artifacts/bradbury-v3-release/fresh-registration-unsigned-payload.json`
- `artifacts/bradbury-v3-release/binding-wave-preauth.json`
- `artifacts/bradbury-v3-release/SHA256SUMS.txt`

## Replay prohibition

The completed deployment, binding, target-deployment, and registration writes must not be replayed merely to generate new evidence.
