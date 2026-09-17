#!/usr/bin/env python3
"""Build canonical ProofPatch assurance-manifest JSON and print its SHA-256."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--candidate-sha256", required=True)
    parser.add_argument("--policy-fingerprint", required=True)
    parser.add_argument("--kernel-hash", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--observation-delay", type=int, required=True)
    parser.add_argument("--assurance-deadline", type=int, required=True)
    parser.add_argument("--state-check", action="append", default=[])
    parser.add_argument("--readback-check", action="append", default=[])
    parser.add_argument("--canary-check", action="append", default=[])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    manifest = {
        "assurance_deadline_seconds": args.assurance_deadline,
        "candidate_sha256": args.candidate_sha256.lower(),
        "ci_assurance_evidence_required": True,
        "expected_kernel_hash": args.kernel_hash.lower(),
        "expected_release_version": args.version,
        "independent_assurance_required": True,
        "observation_delay_seconds": args.observation_delay,
        "policy_fingerprint": args.policy_fingerprint.lower(),
        "required_canary_checks": args.canary_check,
        "required_readback_checks": args.readback_check,
        "required_state_checks": args.state_check,
        "schema": "proofpatch-assurance-v1",
        "target": args.target,
    }
    encoded = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(encoded + "\n", encoding="utf-8")
    print(hashlib.sha256(encoded.encode("utf-8")).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
