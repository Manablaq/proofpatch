#!/usr/bin/env python3
"""Read-only Bradbury finality gate for the canonical ProofPatch V3 graph.

Bradbury currently exposes gen_getTransactionReceipt over curl-compatible JSON-RPC.
The current public node may not expose gen_getTransactionLifecycle even though newer
GenLayer docs describe it. Finality is therefore proven from the materialized receipt:

  status == 7 (Finalized)
  txExecutionResult == 1 (FinishedWithReturn)

gen_getTransactionStatus is used as an additional corroborating read when the live node
supports it. A method-not-found response from that optional corroboration does not
override a finalized, successfully executed receipt.

No state-changing RPC method is used.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "deployments" / "bradbury-v3-deployment.json"

STATUS_NAMES = {
    0: "Uninitialized",
    1: "Pending",
    2: "Proposing",
    3: "Committing",
    4: "Revealing",
    5: "Accepted",
    6: "Undetermined",
    7: "Finalized",
    8: "Canceled",
    9: "AppealRevealing",
    10: "AppealCommitting",
    11: "ValidatorsTimeout",
    12: "LeaderTimeout",
    13: "LeaderRevealing",
}

EXECUTION_NAMES = {
    0: "NotVoted",
    1: "FinishedWithReturn",
    2: "FinishedWithError",
    3: "Timeout",
    4: "NondetDisagree",
    5: "DeterministicViolation",
}


def _norm(value: object) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def _rpc_curl(url: str, method: str, params: list[object], timeout: float) -> object:
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params,
    }
    completed = subprocess.run(
        [
            "curl",
            "-sS",
            "--connect-timeout",
            str(min(timeout, 10.0)),
            "--max-time",
            str(timeout),
            "-X",
            "POST",
            url,
            "-H",
            "Content-Type: application/json",
            "-H",
            "Accept: application/json",
            "--data-binary",
            "@-",
            "-w",
            "\n%{http_code}",
        ],
        input=json.dumps(request, separators=(",", ":")),
        text=True,
        capture_output=True,
        check=False,
    )

    if completed.returncode != 0:
        raise RuntimeError(
            f"{method} curl transport failure rc={completed.returncode}: "
            f"{completed.stderr.strip()}"
        )

    output = completed.stdout
    if "\n" not in output:
        raise RuntimeError(f"{method} returned no HTTP status marker")

    body_text, http_text = output.rsplit("\n", 1)
    try:
        http_status = int(http_text.strip())
    except ValueError as exc:
        raise RuntimeError(
            f"{method} returned invalid HTTP status marker: {http_text!r}"
        ) from exc

    if http_status != 200:
        raise RuntimeError(
            f"{method} HTTP {http_status}: {body_text[:500]}"
        )

    try:
        decoded = json.loads(body_text)
    except Exception as exc:
        raise RuntimeError(f"{method} returned non-JSON data") from exc

    if not isinstance(decoded, dict):
        raise RuntimeError(f"{method} returned invalid JSON-RPC envelope")

    error = decoded.get("error")
    if error is not None:
        code = error.get("code") if isinstance(error, dict) else None
        if code == -32601:
            raise NotImplementedError(f"{method} method not found")
        raise RuntimeError(
            f"{method} RPC error: {json.dumps(error, sort_keys=True)}"
        )

    if "result" not in decoded:
        raise RuntimeError(f"{method} returned no result")

    return decoded["result"]


def _transactions(packet: dict[str, Any]) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for item in packet["deployments"]:
        rows.append(("deployment", str(item["name"]), str(item["tx"])))
    for item in packet["governor_bindings"]:
        rows.append(("governor_binding", str(item["component"]), str(item["tx"])))
    for item in packet["executor_bindings"]:
        rows.append(("executor_binding", str(item["component"]), str(item["tx"])))
    return rows


def _receipt_status(receipt: dict[str, Any]) -> tuple[int | None, str]:
    raw = receipt.get("status")
    code: int | None
    try:
        code = int(raw)
    except (TypeError, ValueError):
        code = None

    name = str(receipt.get("statusName") or "")
    if not name and code is not None:
        name = STATUS_NAMES.get(code, f"Unknown({code})")
    return code, name


def _receipt_execution(receipt: dict[str, Any]) -> tuple[int | None, str]:
    raw = receipt.get("txExecutionResult")
    code: int | None
    try:
        code = int(raw)
    except (TypeError, ValueError):
        code = None

    name = str(receipt.get("txExecutionResultName") or "")
    if not name and code is not None:
        name = EXECUTION_NAMES.get(code, f"Unknown({code})")
    return code, name


def _check_status_endpoint(
    rpc_url: str,
    tx_id: str,
    timeout: float,
) -> tuple[object | None, str]:
    try:
        result = _rpc_curl(
            rpc_url,
            "gen_getTransactionStatus",
            [{"txId": tx_id}],
            timeout,
        )
    except NotImplementedError as exc:
        return None, str(exc)

    if not isinstance(result, dict):
        raise RuntimeError("gen_getTransactionStatus result is not an object")

    status = result.get("status")
    status_code = result.get("statusCode")

    # Newer nodes return both fields. If either is present, it must corroborate
    # Finalized. If the endpoint shape is older/empty, fail rather than infer.
    if status is not None and _norm(status) != "finalized":
        raise RuntimeError(f"status endpoint returned status={status!r}")

    if status_code is not None:
        try:
            code = int(status_code)
        except (TypeError, ValueError) as exc:
            raise RuntimeError(
                f"status endpoint returned invalid statusCode={status_code!r}"
            ) from exc
        if code != 7:
            raise RuntimeError(
                f"status endpoint returned statusCode={code}, expected 7"
            )

    if status is None and status_code is None:
        raise RuntimeError("status endpoint returned neither status nor statusCode")

    return result, ""


def check(
    packet: dict[str, Any],
    *,
    rpc_url: str,
    timeout: float,
) -> dict[str, Any]:
    rows: list[dict[str, object]] = []
    failures = 0
    status_endpoint_supported: bool | None = None

    for index, (kind, name, tx_id) in enumerate(_transactions(packet), start=1):
        try:
            receipt = _rpc_curl(
                rpc_url,
                "gen_getTransactionReceipt",
                [{"txId": tx_id}],
                timeout,
            )
            if not isinstance(receipt, dict):
                raise RuntimeError("receipt is not an object")

            receipt_id = str(receipt.get("id") or "")
            if receipt_id.lower() != tx_id.lower():
                raise RuntimeError(
                    f"receipt tx id mismatch: {receipt_id!r} != {tx_id!r}"
                )

            status_code, status_name = _receipt_status(receipt)
            execution_code, execution_name = _receipt_execution(receipt)

            receipt_ok = (
                status_code == 7
                and execution_code == 1
            )

            status_snapshot: object | None = None
            status_warning = ""
            try:
                status_snapshot, status_warning = _check_status_endpoint(
                    rpc_url,
                    tx_id,
                    timeout,
                )
                if status_warning:
                    status_endpoint_supported = False
                elif status_endpoint_supported is not False:
                    status_endpoint_supported = True
            except RuntimeError as exc:
                raise RuntimeError(
                    f"status corroboration failed: {exc}"
                ) from exc

            ok = receipt_ok
            failure_reason = ""
            if status_code != 7:
                failure_reason = (
                    f"receipt status {status_name} ({status_code}) is not Finalized"
                )
            elif execution_code != 1:
                failure_reason = (
                    f"execution {execution_name} ({execution_code}) "
                    "is not FinishedWithReturn"
                )

            if not ok:
                failures += 1

            rows.append(
                {
                    "kind": kind,
                    "name": name,
                    "tx": tx_id,
                    "statusCode": status_code,
                    "status": status_name,
                    "txExecutionResult": execution_code,
                    "txExecutionResultName": execution_name,
                    "statusEndpoint": status_snapshot,
                    "statusEndpointWarning": status_warning,
                    "failureReason": failure_reason,
                    "ok": ok,
                }
            )

            suffix = (
                f" warning={status_warning}"
                if status_warning
                else ""
            )
            print(
                f"[{index:02d}/35] {'PASS' if ok else 'FAIL'} "
                f"{kind}:{name} "
                f"status={status_name}({status_code}) "
                f"execution={execution_name}({execution_code})"
                f"{suffix}"
            )

        except Exception as exc:
            failures += 1
            rows.append(
                {
                    "kind": kind,
                    "name": name,
                    "tx": tx_id,
                    "ok": False,
                    "failureReason": str(exc),
                }
            )
            print(
                f"[{index:02d}/35] FAIL {kind}:{name} error={exc}"
            )

    return {
        "schema": "proofpatch-bradbury-v3-finality-check-v2",
        "rpc": rpc_url,
        "facade": packet["facade"],
        "transactionCount": len(rows),
        "passCount": len(rows) - failures,
        "failureCount": failures,
        "statusEndpointSupported": status_endpoint_supported,
        "status": "PASS" if failures == 0 else "FAIL",
        "transactions": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--rpc", default="")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    packet = json.loads(args.packet.read_text())
    rpc_url = args.rpc or str(packet["rpc"])

    summary = check(
        packet,
        rpc_url=rpc_url,
        timeout=args.timeout,
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n"
        )

    print()
    print(
        f"PROOFPATCH_V3_FINALITY={summary['status']} "
        f"{summary['passCount']}/{summary['transactionCount']}"
    )
    print(
        "STATUS_ENDPOINT_SUPPORTED="
        f"{summary['statusEndpointSupported']}"
    )
    print("BLOCKCHAIN_TRANSACTION_SUBMITTED=NO")
    print("CONTRACT_WRITE_PERFORMED=NO")

    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
