import ast
from pathlib import Path


ROOT = Path(__file__).parents[2]
GOVERNOR = ROOT / "contracts" / "proofpatch_governor_v2.py"
TARGET = ROOT / "contracts" / "protected_target_v2.py"


EXPECTED_GOVERNOR_METHODS = {
    "register_target",
    "create_proposal",
    "repair_evidence",
    "cancel_proposal",
    "expire_proposal",
    "review_proposal",
    "is_upgrade_authorized",
    "get_candidate_code",
    "confirm_install",
    "reconcile_install",
    "mark_execution_timeout",
    "is_activation_authorized",
    "is_registration_authorized",
    "assure_release",
    "confirm_activation",
    "expire_provisional_release",
    "open_incident",
    "review_incident",
    "is_recovery_authorized",
    "get_recovery_release_id",
    "get_recovery_code",
    "confirm_recovery",
    "reconcile_recovery",
    "expire_recovery",
    "retry_recovery",
    "get_proposal_count",
    "get_proposal_status",
    "get_candidate_hash",
    "get_proposal_release_id",
    "get_evidence_set_hash",
    "get_policy_fingerprint",
    "get_policy_kernel_hash",
    "get_current_code_hash",
    "get_current_version",
    "get_current_release_id",
    "get_active_proposal",
    "get_proposal_summary",
    "get_release_summary",
    "get_incident_summary",
}

EXPECTED_STORAGE_FIELDS = {
    "policies",
    "proposals",
    "releases",
    "incidents",
    "active_proposal_by_target",
    "used_evidence_ids",
    "installed_candidate_hashes",
    "used_incident_ids",
    "proposal_count",
    "release_count",
}

EXPECTED_STATE_VALUES = {
    "BOOTSTRAP",
    "ACTIVE",
    "PROVISIONAL",
    "RECOVERY_PENDING",
    "RECOVERED",
    "PROPOSED",
    "EVIDENCE_REPAIR_REQUIRED",
    "REVIEW_RETRY_REQUIRED",
    "REJECTED",
    "UPGRADE_QUEUED",
    "INSTALLED_PROVISIONAL",
    "ASSURANCE_PENDING",
    "ASSURANCE_REPAIR_REQUIRED",
    "ASSURANCE_RETRY_REQUIRED",
    "CERTIFICATION_QUEUED",
    "CERTIFIED",
    "EXPIRED",
    "CANCELLED",
    "EXECUTION_FAILED",
    "INCIDENT_OPEN",
    "INCIDENT_REPAIR_REQUIRED",
    "INCIDENT_RETRY_REQUIRED",
    "INCIDENT_CONFIRMED",
    "INCIDENT_DISMISSED",
    "RECOVERY_QUEUED",
    "RECOVERY_RETRY_REQUIRED",
    "RECOVERED",
    "REPAIR",
    "RETRY",
    "DECISION",
    "APPROVE",
    "REJECT",
}

EXPECTED_SEMANTIC_KEYS = {
    "storage_layout_compatible",
    "forward_storage_compatible",
    "reverse_storage_compatible_or_recovery_safe",
    "user_rights_preserved",
    "no_privilege_escalation",
    "proofpatch_kernel_preserved",
    "upgrade_authority_preserved",
    "provisional_guard_preserved",
    "consensus_binding_preserved",
    "evidence_trust_preserved",
    "finality_safety_preserved",
    "liveness_preserved",
    "no_hidden_value_transfer",
    "assurance_manifest_sufficient",
    "assurance_path_preserved",
    "recovery_capsule_valid",
    "recovery_path_preserved",
    "constitution_satisfied",
}

EXPECTED_TARGET_METHODS = {
    "get_product_name",
    "get_protected_value",
    "set_protected_value",
    "get_owner",
    "get_proofpatch_governor",
    "register_with_proofpatch",
    "proofpatch_upgrade",
    "proofpatch_confirm_registration",
    "proofpatch_activate",
    "proofpatch_recover",
    "proofpatch_installed_proposal_id",
    "proofpatch_installed_candidate_hash",
    "proofpatch_installed_release_id",
    "proofpatch_release_mode",
    "get_proofpatch_kernel_hash",
}


def _class(source: Path, name: str) -> ast.ClassDef:
    tree = ast.parse(source.read_text())
    return next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == name)


def _public_methods(node: ast.ClassDef) -> set[str]:
    return {
        item.name
        for item in node.body
        if isinstance(item, ast.FunctionDef)
        and not item.name.startswith("_")
    }


def _constant_values(source: Path, prefixes: tuple[str, ...]) -> set[str]:
    tree = ast.parse(source.read_text())
    values: set[str] = set()
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) for target in node.targets):
            continue
        target = next(target for target in node.targets if isinstance(target, ast.Name))
        if target.id.startswith(prefixes) and isinstance(node.value, ast.Constant):
            if isinstance(node.value.value, str):
                values.add(node.value.value)
    return values


def test_v2_governor_public_interface_and_storage_are_complete():
    governor = _class(GOVERNOR, "ProofPatchGovernorV2")
    assert _public_methods(governor) == EXPECTED_GOVERNOR_METHODS
    storage = {
        item.target.id
        for item in governor.body
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name)
    }
    assert storage == EXPECTED_STORAGE_FIELDS


def test_v2_state_machine_and_semantic_vector_are_complete():
    state_values = _constant_values(GOVERNOR, ("MODE_", "STATUS_", "REVIEW_", "DECISION_"))
    assert EXPECTED_STATE_VALUES <= state_values

    tree = ast.parse(GOVERNOR.read_text())
    semantic_assignment = next(
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "SEMANTIC_KEYS" for target in node.targets)
    )
    semantic_keys = {
        element.value
        for element in semantic_assignment.value.elts
        if isinstance(element, ast.Constant) and isinstance(element.value, str)
    }
    assert semantic_keys == EXPECTED_SEMANTIC_KEYS


def test_v2_protected_target_public_interface_is_complete():
    target = _class(TARGET, "ProtectedTarget")
    assert EXPECTED_TARGET_METHODS <= _public_methods(target)
