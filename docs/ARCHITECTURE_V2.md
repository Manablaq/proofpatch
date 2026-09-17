# ProofPatch v2 architecture

ProofPatch v2 keeps the accepted v1 deployment immutable and adds a fresh governor/target pair for continuous release assurance:

```text
VERIFY → INSTALL → ASSURE → CERTIFY → CHALLENGE → APPEAL → RECOVER
```

The v1 baseline remains historical. It is tagged locally as `proofpatch-accepted-v1` at the accepted repository head `f7fb6869cd6e53ddf460ae3145e0685ebd7ef815`; it is not migrated, replayed, or repurposed.

## Trust boundaries

The governor and target contracts decide authorization. The browser and any future keeper only read finalized state or submit permissionless lifecycle calls. No backend or UI value can certify a release, activate code, or choose a recovery implementation.

The target stores an append-only ProofPatch kernel prefix. Its write guard allows application writes only in `ACTIVE` or `RECOVERED` mode. Installation sets `PROVISIONAL`, and activation is a separate finalized message after assurance consensus.

## Frozen proposal identity

Each v2 proposal commits the target, certified parent release, candidate bytes/hash, immutable source/CI/audit references, canonical assurance manifest/hash, recovery mode, recovery release identity, recovery source, and recovery capsule bytes/hash. Repair changes only explicitly repairable evidence URLs and IDs; it cannot change code, parent, policy, manifest, or capsule.

## Recovery safety

`EXACT_PARENT` requires the capsule bytes and version to match the current certified parent. `RECOVERY_CANDIDATE` stores a separate frozen recovery implementation and source identity. Incident review can authorize only the stored capsule hash. Recovery is emitted on finality and confirmed through finalized target metadata.

## Evidence and consensus

Pre-install semantic review uses an expanded exact boolean vector. Assurance and incident review independently fetch two bound evidence packages, validate schemas/timestamps/identity, and compare the complete result object. `REPAIR`, `RETRY`, and `DECISION` remain distinct. No confidence score authorizes a consequence.

## Current status

The v2 contracts and local console are development artifacts until a fresh deployment packet, compatible network validation, finalized source parity, and live lifecycle evidence are complete. No v2 address is claimed here before that proof exists.
