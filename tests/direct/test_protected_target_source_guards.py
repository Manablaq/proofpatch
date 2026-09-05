from pathlib import Path
import ast


ROOT = Path(__file__).resolve().parents[2]
V1 = ROOT / "contracts" / "protected_target_v1.py"
V2_SAFE = ROOT / "contracts" / "protected_target_v2_safe.py"
V2_UNSAFE = ROOT / "contracts" / "protected_target_v2_unsafe.py"

EXPECTED_STORAGE_FIELDS = [
    "owner",
    "proofpatch_governor",
    "product_name",
    "protected_value",
    "installed_proposal_id",
    "installed_candidate_hash",
    "registered_with_proofpatch",
]


def _storage_fields(path: Path):
    tree = ast.parse(path.read_text())
    contract = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "ProtectedTarget")
    fields = []
    for node in contract.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            fields.append(node.target.id)
    return fields


def test_safe_upgrade_preserves_exact_storage_field_order():
    assert _storage_fields(V1) == EXPECTED_STORAGE_FIELDS
    assert _storage_fields(V2_SAFE) == EXPECTED_STORAGE_FIELDS


def test_v1_has_no_owner_upgrade_bypass():
    source = V1.read_text()
    assert "root.upgraders.get().append(governor)" in source
    assert "root.upgraders.get().append(self.owner)" not in source
    assert "owner_upgrade" not in source
    assert "Only ProofPatch governor may upgrade this target" in source


def test_safe_v2_preserves_proofpatch_upgrade_interface():
    source = V2_SAFE.read_text()
    assert "def proofpatch_upgrade(" in source
    assert "def proofpatch_installed_proposal_id(" in source
    assert "def proofpatch_installed_candidate_hash(" in source
    assert 'governor.emit(on="finalized").confirm_install' in source


def test_adversarial_candidate_contains_regressions_for_semantic_review_fixture():
    source = V2_UNSAFE.read_text()
    assert "owner_upgrade_after_escalation" in source
    assert "root.upgraders.get().append(self.owner)" in source
    assert "self.protected_value = value" in source

def test_v1_constructor_uses_native_address_calldata_boundary():
    # Regression for the Bradbury CLI native-address constructor calldata path.
    source = V1.read_text()
    tree = ast.parse(source)
    contract = next(
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "ProtectedTarget"
    )
    constructor = next(
        node
        for node in contract.body
        if isinstance(node, ast.FunctionDef) and node.name == "__init__"
    )

    params = constructor.args.args
    assert [param.arg for param in params] == [
        "self",
        "proofpatch_governor",
        "product_name",
        "initial_value",
    ]

    governor_param = params[1]
    assert isinstance(governor_param.annotation, ast.Name)
    assert governor_param.annotation.id == "Address"

    # A native Address decoded from calldata must not be wrapped in Address(...)
    # a second time. Bradbury proved that double conversion raises TypeError.
    assert "governor = proofpatch_governor" in source
    assert "Address(proofpatch_governor)" not in source
