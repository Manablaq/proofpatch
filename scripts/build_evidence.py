#!/usr/bin/env python3
"""Build ProofPatch evidence from verified inputs.

CI claims are derived from a successful preflight manifest rather than being
self-asserted here. Independent-audit claims must arrive in a separate audit
report; this script validates and preserves them but never invents them.
"""

from pathlib import Path
import argparse
import hashlib
import json
import time
from typing import Any


REQUIRED_CHECKS = (
    "genvm_lint",
    "typecheck",
    "schema",
    "direct_tests",
    "adversarial_tests",
    "proofpatch_interface_tests",
)

REQUIRED_REVIEWER_REGRESSIONS = (
    "test_timeout_reconciles_installed_but_unconfirmed_exact_install",
    "test_timeout_marks_genuinely_uninstalled_proposal_failed_and_releases_slot",
    "test_registration_rejects_noncanonical_authority_prefixes",
    "test_registration_rejects_normalization_sensitive_current_source_urls",
    "test_candidate_url_canonicalization_aliases_are_rejected",
    "test_evidence_url_canonicalization_aliases_are_rejected",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def require_preflight(
    preflight_path: Path,
    parent_hash: str,
    candidate_hash: str,
) -> tuple[dict[str, Any], str]:
    preflight = load_json(preflight_path)

    if preflight.get("status") != "PASS":
        raise ValueError("preflight manifest is not PASS")

    checks = preflight.get("checks")
    if not isinstance(checks, dict):
        raise ValueError("preflight manifest is missing checks")

    for check in REQUIRED_CHECKS:
        if checks.get(check) is not True:
            raise ValueError(f"preflight check is not proven: {check}")

    contract_hashes = preflight.get("contract_sha256")
    if not isinstance(contract_hashes, dict):
        raise ValueError("preflight contract hash map is missing")

    proven_hashes = set(contract_hashes.values())
    if parent_hash not in proven_hashes:
        raise ValueError("parent source hash is not covered by preflight")
    if candidate_hash not in proven_hashes:
        raise ValueError("candidate source hash is not covered by preflight")

    direct_hashes = preflight.get("direct_test_sha256")
    if not isinstance(direct_hashes, dict) or not direct_hashes:
        raise ValueError("Direct Mode test hashes are missing")

    reviewer_docs = preflight.get("reviewer_document_sha256")
    if not isinstance(reviewer_docs, dict) or not reviewer_docs:
        raise ValueError("reviewer document hashes are missing")

    regressions = preflight.get("reviewer_regressions")
    if not isinstance(regressions, list):
        raise ValueError("reviewer regression manifest is missing")

    for regression in REQUIRED_REVIEWER_REGRESSIONS:
        if regression not in regressions:
            raise ValueError(f"required reviewer regression missing: {regression}")

    strict_hashes = preflight.get("strict_typecheck_sha256")
    if not isinstance(strict_hashes, dict) or not strict_hashes:
        raise ValueError("strict typecheck proof hashes are missing")

    return preflight, sha256(preflight_path)


def validate_external_audit(
    audit: dict[str, Any],
    *,
    target: str,
    parent_hash: str,
    candidate_hash: str,
    policy_fingerprint: str,
    audit_id: str,
    audit_issuer: str,
) -> None:
    expected = {
        "schema": "proofpatch-evidence-v1",
        "kind": "audit",
        "evidence_id": audit_id,
        "issuer": audit_issuer,
        "target": target,
        "parent_sha256": parent_hash,
        "candidate_sha256": candidate_hash,
        "policy_fingerprint": policy_fingerprint,
    }

    for key, value in expected.items():
        if audit.get(key) != value:
            raise ValueError(f"external audit mismatch: {key}")

    if audit.get("verdict") != "PASS":
        raise ValueError("external audit verdict is not PASS")
    if audit.get("independent_review") is not True:
        raise ValueError("external audit does not assert independent review")

    published = audit.get("published_at")
    expires = audit.get("expires_at")
    if isinstance(published, bool) or not isinstance(published, int):
        raise ValueError("external audit published_at is invalid")
    if isinstance(expires, bool) or not isinstance(expires, int):
        raise ValueError("external audit expires_at is invalid")
    if expires < published:
        raise ValueError("external audit expiry precedes publication")


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
    parser.add_argument(
        "--audit-report",
        type=Path,
        required=True,
        help="Existing independent audit JSON; ProofPatch does not create this assertion.",
    )

    parser.add_argument(
        "--preflight",
        type=Path,
        default=Path("artifacts/local-preflight.json"),
    )
    parser.add_argument("--ttl", type=int, default=86400)
    parser.add_argument("--out", type=Path, default=Path("evidence/generated"))
    args = parser.parse_args()

    parent_hash = sha256(args.parent)
    candidate_hash = sha256(args.candidate)

    preflight, preflight_hash = require_preflight(
        args.preflight,
        parent_hash,
        candidate_hash,
    )

    audit = load_json(args.audit_report)
    validate_external_audit(
        audit,
        target=args.target,
        parent_hash=parent_hash,
        candidate_hash=candidate_hash,
        policy_fingerprint=args.policy_fingerprint,
        audit_id=args.audit_id,
        audit_issuer=args.audit_issuer,
    )

    now = int(time.time())

    common = {
        "schema": "proofpatch-evidence-v1",
        "target": args.target,
        "parent_sha256": parent_hash,
        "candidate_sha256": candidate_hash,
        "policy_fingerprint": args.policy_fingerprint,
        "published_at": now,
        "expires_at": now + args.ttl,
    }

    proven_checks = preflight["checks"]

    ci = {
        **common,
        "kind": "ci",
        "evidence_id": args.ci_id,
        "issuer": args.ci_issuer,
        "checks": {
            key: proven_checks[key]
            for key in REQUIRED_CHECKS
        },
        "proof": {
            "preflight_sha256": preflight_hash,
            "contract_sha256": preflight["contract_sha256"],
            "direct_test_sha256": preflight["direct_test_sha256"],
            "strict_typecheck_sha256": preflight["strict_typecheck_sha256"],
            "reviewer_document_sha256": preflight["reviewer_document_sha256"],
            "reviewer_regressions": preflight["reviewer_regressions"],
        },
    }

    write_json(args.out / "ci.json", ci)

    # Preserve the independently supplied audit byte-for-byte in meaning.
    write_json(args.out / "audit.json", audit)

    print(args.out / "ci.json")
    print(args.out / "audit.json")
    print(f"CI_PREFLIGHT_SHA256={preflight_hash}")
    print(f"EXTERNAL_AUDIT_SHA256={sha256(args.audit_report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
