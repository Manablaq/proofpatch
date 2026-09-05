#!/usr/bin/env python3
"""Fail closed if local contract source does not exactly match finalized deployed source."""
from pathlib import Path
import argparse
import base64
import hashlib
import json
import urllib.request
import urllib.error


def rpc_call(rpc_url: str, method: str, params: list):
    payload = json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}).encode()
    request = urllib.request.Request(rpc_url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        body = json.loads(response.read().decode())
    if "error" in body:
        raise RuntimeError(json.dumps(body["error"], sort_keys=True))
    if "result" not in body:
        raise RuntimeError("RPC response has no result")
    return body["result"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare local source to finalized GenLayer deployed source exactly.")
    parser.add_argument("--rpc", required=True, help="GenLayer JSON-RPC URL")
    parser.add_argument("--address", required=True, help="Deployed Intelligent Contract address")
    parser.add_argument("--source", required=True, type=Path, help="Local source file expected to match deployment")
    parser.add_argument("--status", choices=("finalized", "accepted"), default="finalized")
    args = parser.parse_args()

    local = args.source.read_bytes()
    result = rpc_call(
        args.rpc,
        "gen_getContractCode",
        [{"address": args.address, "status": args.status}],
    )
    deployed = base64.b64decode(result, validate=True)

    local_hash = hashlib.sha256(local).hexdigest()
    deployed_hash = hashlib.sha256(deployed).hexdigest()

    print(f"LOCAL_SHA256    = {local_hash}")
    print(f"DEPLOYED_SHA256 = {deployed_hash}")
    print(f"STATUS           = {args.status}")
    if local != deployed:
        print("SOURCE_PARITY     = FAIL")
        return 1
    print("SOURCE_PARITY     = PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (urllib.error.URLError, ValueError, RuntimeError) as exc:
        print(f"SOURCE_PARITY     = ERROR: {exc}")
        raise SystemExit(2)
