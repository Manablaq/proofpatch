import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


CASES = (
    ("proofpatch_policy_engine_v3", {"admin", "governor"}),
    ("proofpatch_registration_engine_v3", {"admin", "governor"}),
    ("proofpatch_assurance_engine_v3", {"admin", "governor"}),
    ("proofpatch_summary_engine_v3", {"admin", "governor"}),
    ("proofpatch_lifecycle_request_engine_v3", {"admin", "governor"}),
    ("proofpatch_lifecycle_engine_v3", {"admin", "governor", "executor"}),
    ("proofpatch_review_commit_engine_v3", {"admin", "governor"}),
    ("proofpatch_review_request_engine_v3", {"admin", "governor"}),
    ("proofpatch_governor_v3_facade", {
        "policies", "proposals", "releases", "incidents", "active_proposal_by_target",
        "used_evidence_ids", "installed_candidate_hashes", "used_incident_ids",
        "proposal_count", "release_count",
    }),
)


def _contract_class(path: Path) -> ast.ClassDef:
    tree = ast.parse(path.read_text())
    return next(
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and any(
            (isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name) and base.value.id == "gl" and base.attr == "Contract")
            or (isinstance(base, ast.Name) and base.id == "ProofPatchGovernorV2")
            for base in node.bases
        )
    )


def _storage_fields(node: ast.ClassDef) -> set[str]:
    return {
        item.target.id
        for item in node.body
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name)
    }


def _public_methods(node: ast.ClassDef) -> set[str]:
    return {
        item.name
        for item in node.body
        if isinstance(item, ast.FunctionDef) and not item.name.startswith("_")
    }


def test_v3_compact_artifacts_preserve_contract_storage_fields():
    for stem, expected in CASES:
        readable = _storage_fields(_contract_class(ROOT / "contracts" / f"{stem}.py"))
        compact = _storage_fields(_contract_class(ROOT / "contracts" / f"{stem}_compact.py"))
        assert readable == expected
        assert compact == expected


def test_v3_facade_preserves_the_v2_public_governor_surface():
    original_tree = ast.parse((ROOT / "contracts" / "proofpatch_governor_v2.py").read_text())
    original = next(node for node in original_tree.body if isinstance(node, ast.ClassDef) and node.name == "ProofPatchGovernorV2")
    facade_paths = (
        ROOT / "contracts" / "proofpatch_governor_v3_facade.py",
        ROOT / "contracts" / "proofpatch_governor_v3_facade_compact.py",
    )
    expected = _public_methods(original)
    for path in facade_paths:
        tree = ast.parse(path.read_text())
        facade = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "ProofPatchGovernorV2")
        assert expected <= _public_methods(facade)


def test_facade_summary_helper_keeps_the_cross_contract_read_boundary():
    readable = (ROOT / "contracts" / "proofpatch_governor_v3_facade.py").read_text()
    compact = (ROOT / "contracts" / "proofpatch_governor_v3_facade_compact.py").read_text()
    assert "def _summary(self, kind: str, key: str)" in readable
    assert "return ProofPatchSummaryEngine(Address(SUMMARY_ENGINE))" in readable
    assert "read(kind, str(key))" in readable
    assert "key = str(key)" in readable
    assert "self.releases.get(key, None)" in readable
    assert "def _cj(self,_i," in compact
    assert "return self._cj(_i,_g)" not in compact
    assert "read(_i,str(_" in compact
    assert "=str(_" in compact


def test_v3_serializers_use_runner_safe_integer_checks():
    for path in (ROOT / "contracts").glob("proofpatch_*v3*.py"):
        text = path.read_text()
        assert "u256,u64" not in text
        assert "u256, u64" not in text
