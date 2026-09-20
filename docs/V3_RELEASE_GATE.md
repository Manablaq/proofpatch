# ProofPatch V3 release gate

This is the remaining non-destructive gate before any new canonical V3 lifecycle transaction is authorized.

## Deterministic repository gate

```bash
python scripts/preflight.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/integration -v
cd frontend
npm ci
npm run typecheck
npm run build
```

## Read-only Bradbury graph finality gate

```bash
python scripts/check_bradbury_v3_finality.py \
  --output artifacts/bradbury-v3-finality.json
```

This performs JSON-RPC reads only. It does not finalize, appeal, deploy, bind, write, or call a state-changing contract method.

Every deployment, governor binding, and lifecycle executor binding in `deployments/bradbury-v3-deployment.json` must be `Finalized` with `FinishedWithReturn`, and the advanced lifecycle stored status must also be `Finalized`.

Do not register a fresh V3 target if this gate fails.

## Source parity gate

After graph finality passes, rerun deployed-source parity for all 16 canonical graph artifacts against finalized Bradbury code. Accepted-state parity is not enough for the canonical release packet.

## Canonical fresh-target lifecycle

Only after the gates above pass:

1. deploy a fresh protected target;
2. register it with the corrected V3 facade;
3. confirm finalized registration;
4. create the healthy release proposal;
5. complete pre-install consensus;
6. wait for protocol finality;
7. verify exact provisional installation;
8. submit post-install assurance evidence;
9. complete assurance consensus and finality;
10. verify `CERTIFIED` / `ACTIVE`;
11. create the latent-regression release;
12. open the evidence-bound incident;
13. exercise a real native GenLayer appeal;
14. wait for the appealed decision to finalize;
15. execute the precommitted Recovery Capsule;
16. verify final `RECOVERED` state and exact code hash.

No historical V1 transaction is replayed.

## Production cutover

Production remains on the accepted V1 build until the complete V3 lifecycle proof exists. Only then bind the frontend to the canonical V3 facade/target, deploy the exact certified frontend commit, verify fail-closed finalized reads, tag the release, and prepare the Milestone comparison packet.
