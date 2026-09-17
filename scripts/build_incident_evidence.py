#!/usr/bin/env python3
"""Build canonical, hashable incident evidence bound to one exact release."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


CHECKS = (
    "incident_evidence_authentic",
    "incident_affects_exact_release",
    "incident_reproducible_or_sufficiently_established",
    "constitution_breached",
    "continued_operation_unsafe",
    "recovery_capsule_applicable",
    "recovery_safer_than_continuation",
    "recovery_path_preserves_rights",
    "recovery_path_preserves_governance",
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
    parser.add_argument("--kind", choices=("incident_primary", "incident_corroboration"), required=True)
    parser.add_argument("--evidence-id", required=True)
    parser.add_argument("--issuer", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--release-id", required=True)
    parser.add_argument("--installed-code-sha256", required=True)
    parser.add_argument("--incident-type", required=True)
    parser.add_argument("--policy-fingerprint", required=True)
    parser.add_argument("--published-at", type=int, required=True)
    parser.add_argument("--expires-at", type=int, required=True)
    parser.add_argument("--check", action="append", default=[])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    if args.published_at > args.expires_at:
        raise ValueError("published_at cannot be later than expires_at")
    record = {
        "checks": parse_checks(args.check),
        "evidence_id": args.evidence_id,
        "expires_at": args.expires_at,
        "incident_type": args.incident_type,
        "installed_code_hash": args.installed_code_sha256.lower(),
        "issuer": args.issuer,
        "kind": args.kind,
        "policy_fingerprint": args.policy_fingerprint.lower(),
        "published_at": args.published_at,
        "release_id": args.release_id,
        "schema": "proofpatch-incident-v1",
        "target": args.target,
    }
    encoded = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(encoded + "\n", encoding="utf-8")
    print(hashlib.sha256(encoded.encode("utf-8")).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
