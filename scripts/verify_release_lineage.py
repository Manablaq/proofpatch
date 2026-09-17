#!/usr/bin/env python3
"""Verify deterministic release lineage records exported from finalized state."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def hash_parts(parts: list[str]) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--records", type=Path, required=True, help="JSON array of finalized release summaries")
    args = parser.parse_args()
    records = json.loads(args.records.read_text(encoding="utf-8"))
    if not isinstance(records, list) or not records:
        raise ValueError("records must be a non-empty JSON array")
    by_id: dict[str, dict[str, Any]] = {}
    for item in records:
        if not isinstance(item, dict) or not isinstance(item.get("release_id"), str):
            raise ValueError("every release record must contain release_id")
        if item.get("target", "").lower() != args.target.lower():
            raise ValueError(f"release target mismatch: {item.get('release_id')}")
        release_id = item["release_id"]
        if release_id in by_id:
            raise ValueError(f"duplicate release ID: {release_id}")
        by_id[release_id] = item

    roots = 0
    for item in by_id.values():
        parent_id = str(item.get("parent_release_id", ""))
        parent = by_id.get(parent_id) if parent_id else None
        if parent_id and parent is None:
            raise ValueError(f"missing parent release: {parent_id}")
        if not parent_id:
            roots += 1
        previous_lineage = str(parent.get("lineage_hash", "")) if parent else ""
        expected = hash_parts([
            "proofpatch-v2",
            args.target,
            previous_lineage,
            str(item["release_id"]),
            parent_id,
            str(item.get("version", "")),
            str(item.get("code_hash", "")),
            str(item.get("policy_fingerprint", "")),
            str(item.get("evidence_set_hash", "")),
            str(item.get("assurance_manifest_hash", "")),
            str(item.get("recovery_capsule_hash", "")),
        ])
        if item.get("lineage_hash") != expected:
            raise ValueError(f"lineage hash mismatch: {item['release_id']}")
    if roots != 1:
        raise ValueError(f"expected exactly one root release, found {roots}")
    print(f"LINEAGE: PASS ({len(by_id)} releases, one root)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
