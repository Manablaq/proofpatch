#!/usr/bin/env python3
"""Validate the checked-in schema contracts without network or optional packages."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "evidence-v2.schema.json": "ProofPatch Pre-install Evidence v2",
    "assurance-evidence-v1.schema.json": "ProofPatch Assurance Evidence v1",
    "assurance-manifest-v1.schema.json": "ProofPatch Assurance Manifest v1",
    "incident-evidence-v1.schema.json": "ProofPatch Incident Evidence v1",
    "recovery-capsule-v1.schema.json": "ProofPatch Recovery Capsule v1",
}


def main() -> int:
    schema_dir = ROOT / "schemas"
    for filename, title in EXPECTED.items():
        path = schema_dir / filename
        document = json.loads(path.read_text(encoding="utf-8"))
        if document.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise ValueError(f"{filename}: wrong JSON Schema dialect")
        if document.get("title") != title:
            raise ValueError(f"{filename}: wrong title")
        if document.get("type") != "object" or document.get("additionalProperties") is not False:
            raise ValueError(f"{filename}: schema must be a closed object")
        required = document.get("required")
        properties = document.get("properties")
        if not isinstance(required, list) or not isinstance(properties, dict):
            raise ValueError(f"{filename}: required/properties missing")
        if set(required) - set(properties):
            raise ValueError(f"{filename}: required field is not declared")
    print(f"SCHEMAS: PASS ({len(EXPECTED)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
