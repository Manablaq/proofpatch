#!/usr/bin/env python3
"""Build canonical v2 CI evidence and validate an independently supplied audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


CI_CHECKS = (
    "genvm_lint",
    "typecheck",
    "schema",
    "direct_tests",
    "adversarial_tests",
    "proofpatch_interface_tests",
)


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_write(path: Path, value: dict[str, Any]) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(encoded + "\n", encoding="utf-8")
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--policy-fingerprint", required=True)
    parser.add_argument("--ci-id", required=True)
    parser.add_argument("--ci-issuer", required=True)
    parser.add_argument("--audit-id", required=True)
    parser.add_argument("--audit-issuer", required=True)
    parser.add_argument("--audit-report", type=Path, required=True)
    parser.add_argument("--preflight", type=Path, default=Path("artifacts/local-preflight.json"))
    parser.add_argument("--published-at", type=int, required=True)
    parser.add_argument("--expires-at", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    if args.published_at > args.expires_at:
        raise ValueError("published_at cannot be later than expires_at")
    preflight = load_object(args.preflight)
    if preflight.get("status") != "PASS":
        raise ValueError("preflight manifest is not PASS")
    preflight_checks = preflight.get("checks")
    if not isinstance(preflight_checks, dict) or any(preflight_checks.get(key) is not True for key in CI_CHECKS):
        raise ValueError("preflight does not prove every required CI check")
    contract_hashes = preflight.get("contract_sha256")
    if not isinstance(contract_hashes, dict):
        raise ValueError("preflight contract hashes are missing")
    parent_hash = sha256(args.parent)
    candidate_hash = sha256(args.candidate)
    if parent_hash not in contract_hashes.values() or candidate_hash not in contract_hashes.values():
        raise ValueError("parent and candidate hashes must be covered by preflight")

    common = {
        "candidate_sha256": candidate_hash,
        "expires_at": args.expires_at,
        "parent_sha256": parent_hash,
        "policy_fingerprint": args.policy_fingerprint.lower(),
        "published_at": args.published_at,
        "schema": "proofpatch-evidence-v2",
        "target": args.target,
    }
    ci = {
        **common,
        "checks": {key: True for key in CI_CHECKS},
        "evidence_id": args.ci_id,
        "issuer": args.ci_issuer,
        "kind": "ci",
    }
    audit = load_object(args.audit_report)
    expected = {
        **common,
        "evidence_id": args.audit_id,
        "issuer": args.audit_issuer,
        "kind": "audit",
    }
    for key, value in expected.items():
        if audit.get(key) != value:
            raise ValueError(f"independent audit mismatch: {key}")
    if audit.get("verdict") != "PASS" or audit.get("independent_review") is not True:
        raise ValueError("independent audit is not a passing review")

    print(f"CI_SHA256={canonical_write(args.out / 'ci.json', ci)}")
    print(f"AUDIT_SHA256={canonical_write(args.out / 'audit.json', audit)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
