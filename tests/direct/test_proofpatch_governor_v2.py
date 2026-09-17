import hashlib
import json
import re
import time


CONSTITUTION = """
ProofPatch v2 Security Constitution
1. ProofPatch remains the only code upgrade authority.
2. Provisional releases cannot perform protected writes.
3. Certification and recovery require exact finality-bound consensus.
4. Recovery must use the precommitted capsule only.
5. Release lineage and evidence identities are append-only.
""".strip()

SOURCE_PREFIX = "https://raw.githubusercontent.com/proofpatch-v2/source/"
CI_PREFIX = "https://raw.githubusercontent.com/proofpatch-v2-ci/ci/"
AUDIT_PREFIX = "https://raw.githubusercontent.com/proofpatch-v2-audit/audit/"
ASSURANCE_PREFIX = "https://raw.githubusercontent.com/proofpatch-v2-assurance/assurance/"
ASSURANCE_CORROBORATION_PREFIX = "https://raw.githubusercontent.com/proofpatch-v2-corroboration/corroboration/"
SOURCE_AUTHORITY = "proofpatch-v2/source"
CI_AUTHORITY = "proofpatch-v2-ci/ci"
AUDIT_AUTHORITY = "proofpatch-v2-audit/audit"
ASSURANCE_AUTHORITY = "proofpatch-v2-assurance/assurance"
ASSURANCE_CORROBORATION_AUTHORITY = "proofpatch-v2-corroboration/corroboration"

PARENT_BYTES = b"parent-v2-source\n"
CANDIDATE_BYTES = b"candidate-v3-source\n"
PARENT_HASH = hashlib.sha256(PARENT_BYTES).hexdigest()
CANDIDATE_HASH = hashlib.sha256(CANDIDATE_BYTES).hexdigest()
KERNEL_SOURCE = "\n".join((
    "owner: Address",
    "proofpatch_governor: Address",
    "proofpatch_kernel_hash: str",
    "proofpatch_registered: bool",
    "installed_release_id: str",
    "installed_proposal_id: u256",
    "installed_code_hash: str",
    "release_mode: str",
    "pending_release_id: str",
    "pending_code_hash: str",
    "last_recovery_incident_id: str",
    "last_recovery_release_id: str",
)) + "\n"
KERNEL_HASH = hashlib.sha256(KERNEL_SOURCE.encode("utf-8")).hexdigest()

PARENT_URL = SOURCE_PREFIX + "a" * 40 + "/contracts/parent.py"
CANDIDATE_URL = SOURCE_PREFIX + "b" * 40 + "/contracts/candidate.py"
CI_URL = CI_PREFIX + "c" * 40 + "/evidence/ci.json"
AUDIT_URL = AUDIT_PREFIX + "d" * 40 + "/evidence/audit.json"
RECOVERY_URL = SOURCE_PREFIX + "a" * 40 + "/contracts/parent.py"


def _address_arg(value) -> str:
    if isinstance(value, (bytes, bytearray)):
        return "0x" + bytes(value).hex()
    return str(value)


def _manifest(target, candidate_hash):
    return json.dumps({
        "assurance_deadline_seconds": 7200,
        "candidate_sha256": candidate_hash,
        "ci_assurance_evidence_required": True,
        "expected_kernel_hash": KERNEL_HASH,
        "expected_release_version": "3.0.0",
        "independent_assurance_required": True,
        "observation_delay_seconds": 3600,
        "policy_fingerprint": "0" * 64,
        "required_canary_checks": ["release_mode_is_provisional"],
        "required_readback_checks": ["installed_hash_matches"],
        "required_state_checks": ["owner_preserved"],
        "schema": "proofpatch-assurance-v1",
        "target": _address_arg(target),
    }, sort_keys=True, separators=(",", ":"))


def _register(governor, vm, target, owner):
    vm.sender = target
    # Manifest policy fingerprint is filled after registration in the test helper.
    governor.register_target(
        _address_arg(owner), CONSTITUTION, SOURCE_AUTHORITY, CI_AUTHORITY,
        AUDIT_AUTHORITY, SOURCE_PREFIX, CI_PREFIX, AUDIT_PREFIX,
        ASSURANCE_AUTHORITY, ASSURANCE_PREFIX,
        ASSURANCE_CORROBORATION_AUTHORITY, ASSURANCE_CORROBORATION_PREFIX,
        KERNEL_HASH, "2.0.0", PARENT_URL, PARENT_HASH,
        86_400, 172_800, 86_400, 3_600, 7_200, 16_000, 512_000,
    )


def _create(governor, vm, target, owner):
    vm.sender = owner
    policy_hash = governor.get_policy_fingerprint(_address_arg(target))
    manifest = json.loads(_manifest(target, CANDIDATE_HASH))
    manifest["policy_fingerprint"] = policy_hash
    manifest = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
    return governor.create_proposal(
        _address_arg(target), "3.0.0", CANDIDATE_URL, CANDIDATE_BYTES,
        CI_URL, "ci-v2-001", AUDIT_URL, "audit-v2-001", manifest,
        "EXACT_PARENT", "root-" + PARENT_HASH[:16],
        "2.0.0", RECOVERY_URL, PARENT_BYTES,
    )


def _semantic_checks():
    return {key: True for key in (
        "storage_layout_compatible", "forward_storage_compatible",
        "reverse_storage_compatible_or_recovery_safe", "user_rights_preserved",
        "no_privilege_escalation", "proofpatch_kernel_preserved",
        "upgrade_authority_preserved", "provisional_guard_preserved",
        "consensus_binding_preserved", "evidence_trust_preserved",
        "finality_safety_preserved", "liveness_preserved",
        "no_hidden_value_transfer", "assurance_manifest_sufficient",
        "assurance_path_preserved", "recovery_capsule_valid",
        "recovery_path_preserved", "constitution_satisfied",
    )}


def _mock_review(vm, proposal_id, governor, target):
    summary = json.loads(governor.get_proposal_summary(proposal_id))
    now = int(time.time())
    common = {
        "schema": "proofpatch-evidence-v2",
        "target": _address_arg(target),
        "parent_sha256": summary["parent_code_hash"],
        "candidate_sha256": summary["candidate_code_hash"],
        "policy_fingerprint": summary["policy_fingerprint"],
        "published_at": now - 20,
        "expires_at": now + 3600,
    }
    ci = {**common, "kind": "ci", "evidence_id": "ci-v2-001", "issuer": CI_AUTHORITY,
          "checks": {"genvm_lint": True, "typecheck": True, "schema": True, "direct_tests": True,
                      "adversarial_tests": True, "proofpatch_interface_tests": True}}
    audit = {**common, "kind": "audit", "evidence_id": "audit-v2-001", "issuer": AUDIT_AUTHORITY,
             "verdict": "PASS", "independent_review": True}
    vm.mock_web(re.escape(PARENT_URL), {"status": 200, "body": PARENT_BYTES.decode()})
    vm.mock_web(re.escape(CANDIDATE_URL), {"status": 200, "body": CANDIDATE_BYTES.decode()})
    vm.mock_web(re.escape(RECOVERY_URL), {"status": 200, "body": PARENT_BYTES.decode()})
    vm.mock_web(re.escape(CI_URL), {"status": 200, "body": json.dumps(ci)})
    vm.mock_web(re.escape(AUDIT_URL), {"status": 200, "body": json.dumps(audit)})
    vm.mock_llm(r"PROOFPATCH_SEMANTIC_REVIEW_V2", json.dumps(_semantic_checks()))


def test_v2_registration_creates_immutable_root_release(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor_v2.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    root_id = "root-" + PARENT_HASH[:16]
    summary = json.loads(governor.get_release_summary(root_id))
    assert summary["status"] == "REGISTERED_PARENT"
    assert summary["code_hash"] == PARENT_HASH
    assert governor.get_current_version(_address_arg(direct_bob)) == "2.0.0"


def test_v2_proposal_requires_canonical_manifest_and_precommitted_recovery(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor_v2.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    direct_vm.sender = direct_alice
    policy_hash = governor.get_policy_fingerprint(_address_arg(direct_bob))
    manifest = json.loads(_manifest(direct_bob, CANDIDATE_HASH))
    manifest["policy_fingerprint"] = policy_hash
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
    with direct_vm.expect_revert("Assurance manifest must be canonical JSON"):
        governor.create_proposal(
            _address_arg(direct_bob), "3.0.0", CANDIDATE_URL, CANDIDATE_BYTES,
            CI_URL, "ci-v2-001", AUDIT_URL, "audit-v2-001", canonical + " ",
            "EXACT_PARENT", "root-" + PARENT_HASH[:16], "2.0.0", RECOVERY_URL, PARENT_BYTES,
        )
    proposal_id = governor.create_proposal(
        _address_arg(direct_bob), "3.0.0", CANDIDATE_URL, CANDIDATE_BYTES,
        CI_URL, "ci-v2-001", AUDIT_URL, "audit-v2-001", canonical,
        "EXACT_PARENT", "root-" + PARENT_HASH[:16], "2.0.0", RECOVERY_URL, PARENT_BYTES,
    )
    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["status"] == "PROPOSED"
    assert summary["recovery_mode"] == "EXACT_PARENT"
    assert summary["recovery_capsule_hash"] == PARENT_HASH


def test_v2_recovery_candidate_release_id_is_bound_to_capsule_hash(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor_v2.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    direct_vm.sender = direct_alice
    policy_hash = governor.get_policy_fingerprint(_address_arg(direct_bob))
    manifest = json.loads(_manifest(direct_bob, CANDIDATE_HASH))
    manifest["policy_fingerprint"] = policy_hash
    manifest = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
    recovery_bytes = b"recovery-candidate-v2-source\n"
    recovery_hash = hashlib.sha256(recovery_bytes).hexdigest()
    recovery_url = SOURCE_PREFIX + recovery_hash[:40] + "/contracts/recovery.py"
    proposal_id = governor.create_proposal(
        _address_arg(direct_bob), "3.0.0", CANDIDATE_URL, CANDIDATE_BYTES,
        CI_URL, "ci-candidate-001", AUDIT_URL, "audit-candidate-001", manifest,
        "RECOVERY_CANDIDATE", "recovery-" + recovery_hash[:16], "2.5.0", recovery_url, recovery_bytes,
    )
    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["recovery_mode"] == "RECOVERY_CANDIDATE"
    assert summary["recovery_release_id"] == "recovery-" + recovery_hash[:16]
    assert summary["recovery_capsule_hash"] == recovery_hash
    governor.cancel_proposal(proposal_id)

    candidate_v4 = b"candidate-v4-source\n"
    candidate_v4_hash = hashlib.sha256(candidate_v4).hexdigest()
    manifest_v4 = json.loads(_manifest(direct_bob, candidate_v4_hash))
    manifest_v4["policy_fingerprint"] = policy_hash
    manifest_v4 = json.dumps(manifest_v4, sort_keys=True, separators=(",", ":"))
    with direct_vm.expect_revert("Recovery candidate release ID must bind its capsule hash"):
        governor.create_proposal(
            _address_arg(direct_bob), "3.1.0", CANDIDATE_URL, candidate_v4,
            CI_URL, "ci-candidate-002", AUDIT_URL, "audit-candidate-002", manifest_v4,
            "RECOVERY_CANDIDATE", "recovery-wrong", "2.5.0", recovery_url, recovery_bytes,
        )


def test_v2_review_approves_only_with_expanded_exact_vector(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor_v2.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)
    _mock_review(direct_vm, proposal_id, governor, direct_bob)
    direct_vm.sender = direct_alice
    governor.review_proposal(proposal_id)
    assert governor.get_proposal_status(proposal_id) == "UPGRADE_QUEUED"
