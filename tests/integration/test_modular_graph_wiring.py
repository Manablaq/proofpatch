"""Repository-level checks for the deployable V3 graph.

These tests do not fabricate cross-contract finality. They prove that the
submitted graph is internally wired and that readable and compact artifacts
expose the same public surface. Bradbury receipt tests are opt-in and belong in
the deployment evidence record because they require live addresses.
"""

from __future__ import annotations

import ast
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_DIR = ROOT / "contracts"

GRAPH = {
    "review": "proofpatch_review_engine_v2",
    "fact_review": "proofpatch_fact_review_engine_v3",
    "policy": "proofpatch_policy_engine_v3",
    "incident_policy": "proofpatch_incident_policy_engine_v3",
    "repair_policy": "proofpatch_repair_policy_engine_v3",
    "registration": "proofpatch_registration_engine_v3",
    "assurance": "proofpatch_assurance_engine_v3",
    "summary": "proofpatch_summary_engine_v3",
    "lifecycle_install": "proofpatch_lifecycle_install_engine_v3",
    "lifecycle_timeout": "proofpatch_lifecycle_timeout_engine_v3",
    "lifecycle_activation": "proofpatch_lifecycle_activation_engine_v3",
    "lifecycle_recovery": "proofpatch_lifecycle_recovery_engine_v3",
    "lifecycle_request": "proofpatch_lifecycle_request_engine_v3",
    "review_commit": "proofpatch_review_commit_engine_v3",
    "review_request": "proofpatch_review_request_engine_v3",
    "facade": "proofpatch_governor_v3_facade",
}


def _public_methods(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    methods: set[str] = set()

    def is_public(decorator: ast.AST) -> bool:
        return (
            isinstance(decorator, ast.Attribute)
            and decorator.attr in {"view", "write"}
            and isinstance(decorator.value, ast.Attribute)
            and decorator.value.attr == "public"
            and isinstance(decorator.value.value, ast.Name)
            and decorator.value.value.id == "gl"
        )

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if any(is_public(decorator) for decorator in node.decorator_list):
                methods.add(node.name)
    return methods


def test_every_graph_component_is_linted_by_preflight_in_readable_and_compact_form():
    preflight = (ROOT / "scripts" / "preflight.py").read_text()
    for stem in GRAPH.values():
        readable = CONTRACT_DIR / f"{stem}.py"
        compact = CONTRACT_DIR / f"{stem}_compact.py"
        assert readable.exists(), readable
        assert compact.exists(), compact
        assert f'"{stem}.py"' in preflight
        assert f'"{stem}_compact.py"' in preflight


def test_compact_graph_preserves_every_public_method():
    for stem in GRAPH.values():
        readable = _public_methods(CONTRACT_DIR / f"{stem}.py")
        compact = _public_methods(CONTRACT_DIR / f"{stem}_compact.py")
        assert compact == readable, stem


def test_facade_wiring_is_explicit_and_uses_distinct_component_addresses():
    source = (CONTRACT_DIR / "proofpatch_governor_v3_facade.py").read_text()
    names = (
        "REVIEW_ENGINE",
        "ASSURANCE_REVIEW_ENGINE",
        "INCIDENT_POLICY_ENGINE",
        "REPAIR_POLICY_ENGINE",
        "POLICY_ENGINE",
        "REGISTRATION_ENGINE",
        "ASSURANCE_ENGINE",
        "SUMMARY_ENGINE",
        "INSTALL_LIFECYCLE_ENGINE",
        "TIMEOUT_LIFECYCLE_ENGINE",
        "ACTIVATION_LIFECYCLE_ENGINE",
        "RECOVERY_LIFECYCLE_ENGINE",
        "LIFECYCLE_REQUEST_ENGINE",
        "REVIEW_COMMIT_ENGINE",
        "REVIEW_REQUEST_ENGINE",
    )
    addresses = []
    for name in names:
        match = re.search(rf"^{name}\s*=\s*['\"](0x[0-9A-Fa-f]{{40}})['\"]", source, re.MULTILINE)
        assert match, name
        addresses.append(match.group(1).lower())
        assert f"Address({name})" in source or f"{name})" in source
    assert len(set(addresses)) == len(addresses)


@pytest.mark.skipif(
    __import__("os").environ.get("PROOFPATCH_BRADBURY_INTEGRATION") != "1",
    reason="Set PROOFPATCH_BRADBURY_INTEGRATION=1 with a deployment evidence fixture to run live Bradbury checks",
)
def test_bradbury_integration_requires_explicit_deployment_fixture():
    fixture = ROOT / "artifacts" / "bradbury-integration.json"
    assert fixture.exists(), "Live integration requires an explicit finalized receipt fixture"
