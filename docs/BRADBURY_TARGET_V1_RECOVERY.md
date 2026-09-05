# Bradbury ProtectedTarget v1 deployment recovery

This record preserves the first `ProtectedTarget v1` deployment attempt as
negative integration evidence. It must not be described as a successful
deployment.

## Failed attempt

- Network: GenLayer Bradbury Testnet (`chainId 4221`)
- Governor:
  `0xc0100eFD567CD9dCcC8b9D17E381774fC4113ade`
- Transaction:
  `0xdaea806c792ebde219ec7a37a37552d5d58a5d3fd431f4e1bdca65e3c7129e41`
- Derived/ghost target address:
  `0x0722cC74F8fACAA7f09E4376FFbfF3A3322332F1`
- Submitted target-v1 source SHA-256:
  `6488e9d44acfac9997d41ce8c324fb410a469af68b96d8dbf20c50ce34b3df00`
- Stored transaction status observed: `Accepted` / status code `5`
- Consensus result observed: `AGREE`
- Execution result observed: `2` / `FINISHED_WITH_ERROR`
- `gen_getContractCode(status="accepted")` returned:
  `contract code not found`
- No registration transaction was sent for the failed address.
- No second deployment was sent during diagnosis.

## Exact execution failure

`gen_dbg_traceTransaction` round 0 returned result code `2` and the GenVM
stderr ended at the constructor boundary:

```text
File "/contract.py", line 45, in __init__
    governor = Address(proofpatch_governor)
File "/py/libs/genlayer/py/types.py", line 151, in __init__
    val = bytes(val)
TypeError: cannot convert 'Address' object to bytes
```

## Root cause

The GenLayer CLI parser treats a bare `0x` + 40-hex argument as native
`CalldataAddress`. Bradbury therefore decoded the governor argument as GenLayer
`Address`. The old target constructor declared that boundary as `str` and then
called `Address(proofpatch_governor)`, causing an invalid second conversion.

This was a deployment-boundary bug in `ProtectedTarget v1`; it was not a
governor consensus/finality failure.

## Corrective rule

The corrected target-v1 constructor accepts `proofpatch_governor: Address`
directly and stores/uses that native value without a second `Address(...)`
conversion.

The old target-v1 source hash above is retired for deployment. Before any
replacement deployment:

1. run the complete authoritative local preflight;
2. require the constructor ABI to expose the governor parameter as `address`;
3. freeze the corrected target-v1 SHA-256 in a new immutable commit/tag;
4. verify governor and safe-v2 source bytes remain unchanged;
5. deploy exactly one corrected target-v1;
6. require execution success plus finality plus exact finalized source parity;
7. only then call `register_with_proofpatch`.

The already-deployed governor and its original
`proofpatch-bradbury-candidate-v1` source tag remain unchanged.
