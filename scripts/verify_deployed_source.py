#!/usr/bin/env python3
"""Fail closed if local contract source does not exactly match finalized deployed source."""
from pathlib import Path
import argparse
import base64
import hashlib
import json
import subprocess
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


def cli_code(rpc_url: str, address: str) -> bytes:
    """Use the supported CLI when the public RPC blocks direct code RPC calls."""
    result = subprocess.run(
        ["genlayer", "code", address, "--rpc", rpc_url],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    marker = "Result:\n"
    if marker not in result.stdout:
        raise RuntimeError("genlayer code output did not contain a Result section")
    return result.stdout.split(marker, 1)[1].encode()


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare local source to finalized GenLayer deployed source exactly.")
    parser.add_argument("--rpc", required=True, help="GenLayer JSON-RPC URL")
    parser.add_argument("--address", required=True, help="Deployed Intelligent Contract address")
    parser.add_argument("--source", required=True, type=Path, help="Local source file expected to match deployment")
    parser.add_argument("--status", choices=("finalized", "accepted"), default="finalized")
    args = parser.parse_args()

    local = args.source.read_bytes()
    try:
        result = rpc_call(
            args.rpc,
            "gen_getContractCode",
            [{"address": args.address, "status": args.status}],
        )
        deployed = base64.b64decode(result, validate=True)
        retrieval = "rpc"
    except urllib.error.HTTPError as exc:
        if exc.code != 403:
            raise
        deployed = cli_code(args.rpc, args.address)
        retrieval = "genlayer-cli"

    # The CLI wrapper appends a blank transport line after the returned source;
    # source bytes themselves must remain identical.
    local_normalized = local.rstrip(b"\n")
    deployed_normalized = deployed.rstrip(b"\n")
    local_hash = hashlib.sha256(local_normalized).hexdigest()
    deployed_hash = hashlib.sha256(deployed_normalized).hexdigest()

    print(f"LOCAL_SHA256    = {local_hash}")
    print(f"DEPLOYED_SHA256 = {deployed_hash}")
    print(f"STATUS           = {args.status}")
    print(f"RETRIEVAL       = {retrieval}")
    if local_normalized != deployed_normalized:
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
