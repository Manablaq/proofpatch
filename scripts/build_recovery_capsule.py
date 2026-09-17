#!/usr/bin/env python3
"""Build the canonical metadata record for a precommitted recovery capsule."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("EXACT_PARENT", "RECOVERY_CANDIDATE"), required=True)
    parser.add_argument("--release-id", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--code", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    code = args.code.read_bytes()
    capsule = {
        "mode": args.mode,
        "recovery_code_sha256": hashlib.sha256(code).hexdigest(),
        "recovery_release_id": args.release_id,
        "recovery_source_url": args.source_url,
        "recovery_version": args.version,
        "schema": "proofpatch-recovery-capsule-v1",
    }
    encoded = json.dumps(capsule, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(encoded + "\n", encoding="utf-8")
    print(hashlib.sha256(encoded.encode("utf-8")).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
