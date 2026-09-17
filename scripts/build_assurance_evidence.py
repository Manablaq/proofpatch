#!/usr/bin/env python3
"""Build canonical, hashable assurance evidence for a frozen v2 release."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


CHECKS = (
    "installed_hash_matches",
    "kernel_binding_matches",
    "governor_binding_matches",
    "critical_state_preserved",
    "interface_requirements_hold",
    "canary_requirements_hold",
    "runtime_evidence_valid",
    "no_post_install_security_regression",
    "recovery_path_live",
    "assurance_manifest_satisfied",
)


def parse_checks(values: list[str]) -> dict[str, bool]:
    checks = {key: True for key in CHECKS}
    for value in values:
        name, separator, raw = value.partition("=")
        if separator != "=" or name not in checks or raw not in ("true", "false"):
            raise ValueError(f"check must be NAME=true|false for one of: {', '.join(CHECKS)}")
        checks[name] = raw == "true"
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=("assurance_primary", "assurance_corroboration"), required=True)
    parser.add_argument("--evidence-id", required=True)
    parser.add_argument("--issuer", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--release-id", required=True)
    parser.add_argument("--proposal-id", type=int, required=True)
    parser.add_argument("--candidate-sha256", required=True)
    parser.add_argument("--policy-fingerprint", required=True)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--published-at", type=int, required=True)
    parser.add_argument("--expires-at", type=int, required=True)
    parser.add_argument("--check", action="append", default=[])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    if args.published_at > args.expires_at:
        raise ValueError("published_at cannot be later than expires_at")
    record = {
        "candidate_sha256": args.candidate_sha256.lower(),
        "checks": parse_checks(args.check),
        "evidence_id": args.evidence_id,
        "expires_at": args.expires_at,
        "issuer": args.issuer,
        "kind": args.kind,
        "manifest_sha256": args.manifest_sha256.lower(),
        "policy_fingerprint": args.policy_fingerprint.lower(),
        "proposal_id": args.proposal_id,
        "published_at": args.published_at,
        "release_id": args.release_id,
        "schema": "proofpatch-assurance-v1",
        "target": args.target,
    }
    encoded = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(encoded + "\n", encoding="utf-8")
    print(hashlib.sha256(encoded.encode("utf-8")).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
