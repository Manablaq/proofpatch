# ProofPatch v2 assurance model

The assurance manifest is canonical JSON with sorted keys, no floats, bounded check lists, and a hash committed in the proposal. It declares the expected candidate, policy, kernel, version, state checks, readbacks, canaries, observation delay, deadline, and independent evidence requirement.

After finalized installation and the observation delay, permissionless assurance fetches primary and corroborating evidence from distinct policy-bound publishers. Each package binds the target, proposal, release, candidate hash, policy fingerprint, manifest hash, timestamps, and the complete boolean assurance vector. Validators independently repeat the evidence and compare all consequential fields.

Passing assurance queues finalized activation. Failing assurance opens an incident; it never silently certifies a release. Assurance timeout creates an incident requiring the normal consensus recovery path.
