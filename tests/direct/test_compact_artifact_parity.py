import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
READABLE = ROOT / "contracts" / "proofpatch_governor_v2.py"
COMPACT = ROOT / "contracts" / "proofpatch_governor_v2_compact.py"


def _class(path: Path, name: str) -> ast.ClassDef:
    tree = ast.parse(path.read_text())
    return next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == name)


def _public_methods(node: ast.ClassDef) -> set[str]:
    return {
        item.name
        for item in node.body
        if isinstance(item, ast.FunctionDef) and not item.name.startswith("_")
    }


def _storage_fields(node: ast.ClassDef) -> set[str]:
    return {
        item.target.id
        for item in node.body
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name)
    }


def test_compact_governor_preserves_public_surface_and_storage_surface():
    readable = _class(READABLE, "ProofPatchGovernorV2")
    compact = _class(COMPACT, "ProofPatchGovernorV2")
    assert _public_methods(compact) == _public_methods(readable)
    assert _storage_fields(compact) == _storage_fields(readable)


def test_compact_governor_preserves_lifecycle_and_semantic_literals():
    readable = ast.parse(READABLE.read_text())
    compact = ast.parse(COMPACT.read_text())
    required = {
        "BOOTSTRAP", "ACTIVE", "PROVISIONAL", "RECOVERY_PENDING", "RECOVERED",
        "PROPOSED", "EVIDENCE_REPAIR_REQUIRED", "REVIEW_RETRY_REQUIRED", "REJECTED",
        "UPGRADE_QUEUED", "INSTALLED_PROVISIONAL", "ASSURANCE_PENDING",
        "ASSURANCE_REPAIR_REQUIRED", "ASSURANCE_RETRY_REQUIRED", "CERTIFICATION_QUEUED",
        "CERTIFIED", "EXPIRED", "CANCELLED", "EXECUTION_FAILED", "INCIDENT_OPEN",
        "INCIDENT_REPAIR_REQUIRED", "INCIDENT_RETRY_REQUIRED", "INCIDENT_CONFIRMED",
        "INCIDENT_DISMISSED", "RECOVERY_QUEUED", "RECOVERY_RETRY_REQUIRED",
        "REPAIR", "RETRY", "DECISION", "APPROVE", "REJECT",
        "storage_layout_compatible", "forward_storage_compatible",
        "reverse_storage_compatible_or_recovery_safe", "user_rights_preserved",
        "no_privilege_escalation", "proofpatch_kernel_preserved",
        "upgrade_authority_preserved", "provisional_guard_preserved",
        "consensus_binding_preserved", "evidence_trust_preserved",
        "finality_safety_preserved", "liveness_preserved", "no_hidden_value_transfer",
        "assurance_manifest_sufficient", "assurance_path_preserved",
        "recovery_capsule_valid", "recovery_path_preserved", "constitution_satisfied",
    }
    def string_literals(tree):
        env = {}

        def evaluate(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                return node.value
            if isinstance(node, ast.Name):
                return env.get(node.id)
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                left, right = evaluate(node.left), evaluate(node.right)
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
            return None

        values = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                value = evaluate(node.value)
                if isinstance(value, str):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            env[target.id] = value
                            values.add(value)
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                values.add(node.value)
            else:
                value = evaluate(node)
                if isinstance(value, str):
                    values.add(value)
        return values

    readable_literals = string_literals(readable)
    compact_literals = string_literals(compact)
    assert required <= readable_literals
    assert required <= compact_literals


def test_compact_artifact_is_smaller_than_bradbury_baseline():
    assert COMPACT.stat().st_size < 60_000
