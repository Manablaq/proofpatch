#!/usr/bin/env python3
"""Build canonical, hashable incident evidence bound to one exact release."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


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
    parser.add_argument("--facts", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    if args.published_at > args.expires_at:
        raise ValueError("published_at cannot be later than expires_at")
    facts = json.loads(args.facts.read_text(encoding="utf-8"))
    if not isinstance(facts, dict):
        raise ValueError("facts must be a JSON object")
    record = {
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
        "facts": facts,
    }
    encoded = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(encoded + "\n", encoding="utf-8")
    print(hashlib.sha256(encoded.encode("utf-8")).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
