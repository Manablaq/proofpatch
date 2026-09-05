import hashlib
import json
import re
import time


CONSTITUTION = """
ProofPatch Security Constitution v1
1. Preserve every existing user withdrawal and owner-control invariant.
2. Never introduce an unrestricted administrative value-transfer or mutation path.
3. ProofPatch must remain the only contract-code upgrade authority.
4. Consequential authorization decisions require exact validator agreement.
5. Evidence must remain bound to approved immutable publishers, freshness, and independent corroboration.
6. Irreversible cross-contract consequences must execute only after GenLayer finality.
7. Every bounded workflow must retain expiry/recovery semantics.
8. The persistent storage layout must remain backward compatible.
9. No alternate method may bypass a suspension, challenge, policy, or upgrade consequence.
""".strip()

SOURCE_PREFIX = "https://raw.githubusercontent.com/proofpatch-labs/protected-app/"
CI_PREFIX = "https://raw.githubusercontent.com/proofpatch-labs/protected-app-ci/"
AUDIT_PREFIX = "https://raw.githubusercontent.com/independent-audit-labs/proofpatch-audits/"
SOURCE_AUTHORITY = "proofpatch-labs/protected-app"
CI_AUTHORITY = "proofpatch-labs/protected-app-ci"
AUDIT_AUTHORITY = "independent-audit-labs/proofpatch-audits"

PARENT_COMMIT = "a" * 40
CANDIDATE_COMMIT = "b" * 40
REPAIRED_CANDIDATE_COMMIT = "d" * 40
CI_COMMIT = "c" * 40
AUDIT_COMMIT = "e" * 40

PARENT_URL = SOURCE_PREFIX + PARENT_COMMIT + "/contracts/protected_target_v1.py"
CANDIDATE_URL = SOURCE_PREFIX + CANDIDATE_COMMIT + "/contracts/protected_target_v2.py"
REPAIRED_CANDIDATE_URL = SOURCE_PREFIX + REPAIRED_CANDIDATE_COMMIT + "/contracts/protected_target_v2.py"
CI_URL = CI_PREFIX + CI_COMMIT + "/evidence/ci.json"
AUDIT_URL = AUDIT_PREFIX + AUDIT_COMMIT + "/evidence/audit.json"

PARENT_BYTES = b"parent-source-v1\n"
CANDIDATE_BYTES = b"candidate-source-v2\n"
PARENT_HASH = hashlib.sha256(PARENT_BYTES).hexdigest()
CANDIDATE_HASH = hashlib.sha256(CANDIDATE_BYTES).hexdigest()


def _address_arg(value) -> str:
    """Serialize Direct Mode fixture addresses without Python bytes repr leakage."""
    if isinstance(value, (bytes, bytearray)):
        raw = bytes(value)
        if len(raw) != 20:
            raise AssertionError(f"Direct Mode address must be 20 bytes, got {len(raw)}")
        return "0x" + raw.hex()
    return str(value)


def _register(governor, direct_vm, target, owner):
    direct_vm.sender = target
    governor.register_target(
        _address_arg(owner),
        CONSTITUTION,
        SOURCE_AUTHORITY,
        CI_AUTHORITY,
        AUDIT_AUTHORITY,
        SOURCE_PREFIX,
        CI_PREFIX,
        AUDIT_PREFIX,
        "1.0.0",
        PARENT_URL,
        PARENT_HASH,
        24 * 60 * 60,
        2 * 24 * 60 * 60,
        24 * 60 * 60,
    )


def _create(governor, direct_vm, target, owner, *, ci_id="ci-proof-001", audit_id="audit-proof-001"):
    direct_vm.sender = owner
    return governor.create_proposal(
        _address_arg(target),
        "2.0.0",
        CANDIDATE_URL,
        CANDIDATE_BYTES,
        CI_URL,
        ci_id,
        AUDIT_URL,
        audit_id,
    )


def _semantic_checks(all_true: bool):
    return {
        "storage_layout_compatible": all_true,
        "user_rights_preserved": all_true,
        "no_privilege_escalation": all_true,
        "upgrade_authority_preserved": all_true,
        "consensus_binding_preserved": all_true,
        "evidence_trust_preserved": all_true,
        "finality_safety_preserved": all_true,
        "liveness_preserved": all_true,
        "no_hidden_value_transfer": all_true,
        "constitution_satisfied": all_true,
    }


def _evidence(governor, target, proposal_id, *, now=None):
    now = int(time.time()) if now is None else now
    summary = json.loads(governor.get_proposal_summary(proposal_id))
    common = {
        "schema": "proofpatch-evidence-v1",
        "target": _address_arg(target),
        "parent_sha256": summary["parent_code_hash"],
        "candidate_sha256": summary["candidate_code_hash"],
        "policy_fingerprint": summary["policy_fingerprint"],
        "published_at": now - 30,
        "expires_at": now + 3600,
    }
    ci = {
        **common,
        "kind": "ci",
        "evidence_id": "ci-proof-001",
        "issuer": CI_AUTHORITY,
        "checks": {
            "genvm_lint": True,
            "typecheck": True,
            "schema": True,
            "direct_tests": True,
            "adversarial_tests": True,
            "proofpatch_interface_tests": True,
        },
    }
    audit = {
        **common,
        "kind": "audit",
        "evidence_id": "audit-proof-001",
        "issuer": AUDIT_AUTHORITY,
        "verdict": "PASS",
        "independent_review": True,
    }
    return ci, audit


def _mock_valid_evidence(direct_vm, governor, target, proposal_id, *, semantic_all_true=False):
    ci, audit = _evidence(governor, target, proposal_id)
    direct_vm.mock_web(re.escape(PARENT_URL), {"status": 200, "body": PARENT_BYTES.decode()})
    direct_vm.mock_web(re.escape(CANDIDATE_URL), {"status": 200, "body": CANDIDATE_BYTES.decode()})
    direct_vm.mock_web(re.escape(CI_URL), {"status": 200, "body": json.dumps(ci)})
    direct_vm.mock_web(re.escape(AUDIT_URL), {"status": 200, "body": json.dumps(audit)})
    direct_vm.mock_llm(r"PROOFPATCH_SEMANTIC_REVIEW_V1", json.dumps(_semantic_checks(semantic_all_true)))


def test_registration_binds_immutable_independent_authorities(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    direct_vm.sender = direct_bob

    with direct_vm.expect_revert("Independent audit authority must have a distinct GitHub publisher"):
        governor.register_target(
            _address_arg(direct_alice),
            CONSTITUTION,
            SOURCE_AUTHORITY,
            CI_AUTHORITY,
            "same-publisher-audit",
            SOURCE_PREFIX,
            CI_PREFIX,
            "https://raw.githubusercontent.com/proofpatch-labs/audits/",
            "1.0.0",
            PARENT_URL,
            PARENT_HASH,
            3600,
            3600,
            3600,
        )

    _register(governor, direct_vm, direct_bob, direct_alice)
    fingerprint = governor.get_policy_fingerprint(_address_arg(direct_bob))
    assert len(fingerprint) == 64
    assert governor.get_current_code_hash(_address_arg(direct_bob)) == PARENT_HASH

    with direct_vm.expect_revert("Target is already registered; policy is immutable"):
        _register(governor, direct_vm, direct_bob, direct_alice)


def test_mutable_branch_urls_are_rejected(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    direct_vm.sender = direct_alice

    with direct_vm.expect_revert("Candidate source URL is not an approved immutable source"):
        governor.create_proposal(
            _address_arg(direct_bob),
            "2.0.0",
            SOURCE_PREFIX + "main/contracts/protected_target_v2.py",
            CANDIDATE_BYTES,
            CI_URL,
            "ci-main-001",
            AUDIT_URL,
            "audit-main-001",
        )


def test_only_registered_owner_can_create_upgrade(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    direct_vm.sender = direct_charlie

    with direct_vm.expect_revert("Only the registered target owner may perform this action"):
        governor.create_proposal(
            _address_arg(direct_bob), "2.0.0", CANDIDATE_URL, CANDIDATE_BYTES,
            CI_URL, "ci-attacker-001", AUDIT_URL, "audit-attacker-001",
        )


def test_candidate_bytes_are_frozen_and_hash_bound(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    assert governor.get_candidate_hash(proposal_id) == CANDIDATE_HASH
    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["candidate_code_hash"] == CANDIDATE_HASH
    assert summary["parent_code_hash"] == PARENT_HASH
    assert summary["status"] == "PROPOSED"


def test_evidence_identifiers_cannot_be_reused_after_cancellation(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)
    direct_vm.sender = direct_alice
    governor.cancel_proposal(proposal_id)

    with direct_vm.expect_revert("Evidence identifier has already been used"):
        governor.create_proposal(
            _address_arg(direct_bob),
            "2.0.1",
            CANDIDATE_URL,
            CANDIDATE_BYTES + b"patch",
            CI_URL,
            "ci-proof-001",
            AUDIT_URL,
            "audit-proof-001",
        )


def test_hash_failure_becomes_repairable_state_not_terminal_refund(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    direct_vm.mock_web(re.escape(PARENT_URL), {"status": 200, "body": PARENT_BYTES.decode()})
    direct_vm.mock_web(re.escape(CANDIDATE_URL), {"status": 200, "body": "tampered candidate"})
    governor.review_proposal(proposal_id)

    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["status"] == "EVIDENCE_REPAIR_REQUIRED"
    assert summary["last_review_code"] == "CANDIDATE_SOURCE_HASH_MISMATCH"
    before_hash = governor.get_candidate_hash(proposal_id)

    direct_vm.sender = direct_alice
    governor.repair_evidence(
        proposal_id,
        REPAIRED_CANDIDATE_URL,
        CI_PREFIX + ("f" * 40) + "/evidence/ci-repaired.json",
        "ci-proof-repaired-002",
        AUDIT_PREFIX + ("1" * 40) + "/evidence/audit-repaired.json",
        "audit-proof-repaired-002",
    )

    assert governor.get_candidate_hash(proposal_id) == before_hash
    assert governor.get_proposal_status(proposal_id) == "PROPOSED"


def test_web_response_status_field_classifies_404_as_repair(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    direct_vm.mock_web(re.escape(PARENT_URL), {"status": 404, "body": "not found"})
    governor.review_proposal(proposal_id)

    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["status"] == "EVIDENCE_REPAIR_REQUIRED"
    assert summary["last_review_code"] == "PARENT_REPAIR_HTTP_4XX"


def test_web_response_status_field_classifies_500_as_retry(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    direct_vm.mock_web(re.escape(PARENT_URL), {"status": 500, "body": "temporary failure"})
    governor.review_proposal(proposal_id)

    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["status"] == "REVIEW_RETRY_REQUIRED"
    assert summary["last_review_code"] == "PARENT_RETRY_HTTP_5XX"


def test_malformed_llm_output_is_retryable_not_authorization(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)
    ci, audit = _evidence(governor, direct_bob, proposal_id)

    direct_vm.mock_web(re.escape(PARENT_URL), {"status": 200, "body": PARENT_BYTES.decode()})
    direct_vm.mock_web(re.escape(CANDIDATE_URL), {"status": 200, "body": CANDIDATE_BYTES.decode()})
    direct_vm.mock_web(re.escape(CI_URL), {"status": 200, "body": json.dumps(ci)})
    direct_vm.mock_web(re.escape(AUDIT_URL), {"status": 200, "body": json.dumps(audit)})
    direct_vm.mock_llm(r"PROOFPATCH_SEMANTIC_REVIEW_V1", '{"looks_safe": true}')

    governor.review_proposal(proposal_id)
    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["status"] == "REVIEW_RETRY_REQUIRED"
    assert summary["last_review_code"] == "LLM_SCHEMA_INVALID"



def test_evidence_timestamp_boolean_is_repairable_not_coerced(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)
    ci, audit = _evidence(governor, direct_bob, proposal_id)
    ci["published_at"] = True

    direct_vm.mock_web(re.escape(PARENT_URL), {"status": 200, "body": PARENT_BYTES.decode()})
    direct_vm.mock_web(re.escape(CANDIDATE_URL), {"status": 200, "body": CANDIDATE_BYTES.decode()})
    direct_vm.mock_web(re.escape(CI_URL), {"status": 200, "body": json.dumps(ci)})
    direct_vm.mock_web(re.escape(AUDIT_URL), {"status": 200, "body": json.dumps(audit)})

    governor.review_proposal(proposal_id)
    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["status"] == "EVIDENCE_REPAIR_REQUIRED"
    assert summary["last_review_code"] == "CI_EVIDENCE_TIMESTAMP_INVALID"


def test_evidence_identity_fields_are_not_string_coerced(direct_vm, direct_deploy, direct_alice, direct_bob):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)
    ci, audit = _evidence(governor, direct_bob, proposal_id)
    ci["target"] = 12345

    direct_vm.mock_web(re.escape(PARENT_URL), {"status": 200, "body": PARENT_BYTES.decode()})
    direct_vm.mock_web(re.escape(CANDIDATE_URL), {"status": 200, "body": CANDIDATE_BYTES.decode()})
    direct_vm.mock_web(re.escape(CI_URL), {"status": 200, "body": json.dumps(ci)})
    direct_vm.mock_web(re.escape(AUDIT_URL), {"status": 200, "body": json.dumps(audit)})

    governor.review_proposal(proposal_id)
    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["status"] == "EVIDENCE_REPAIR_REQUIRED"
    assert summary["last_review_code"] == "CI_EVIDENCE_FIELD_TYPE_INVALID_TARGET"

def test_semantic_rejection_is_persisted_and_releases_target(direct_vm, direct_deploy, direct_alice, direct_bob):
    direct_vm.check_pickling = True
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)
    _mock_valid_evidence(direct_vm, governor, direct_bob, proposal_id, semantic_all_true=False)

    governor.review_proposal(proposal_id)

    assert governor.get_proposal_status(proposal_id) == "REJECTED"
    assert int(governor.get_active_proposal(_address_arg(direct_bob))) == 0


def test_validator_must_independently_reach_same_consequential_semantics(direct_vm, direct_deploy, direct_alice, direct_bob):
    direct_vm.check_pickling = True
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)
    _mock_valid_evidence(direct_vm, governor, direct_bob, proposal_id, semantic_all_true=False)

    # Leader independently evaluates exact evidence and rejects.
    governor.review_proposal(proposal_id)
    assert governor.get_proposal_status(proposal_id) == "REJECTED"

    # A validator independently evaluating the same evidence as APPROVE must DISAGREE.
    # Shape validity alone cannot make contradictory authorization outcomes compatible.
    direct_vm.clear_mocks()
    ci, audit = _evidence(governor, direct_bob, proposal_id)
    direct_vm.mock_web(re.escape(PARENT_URL), {"status": 200, "body": PARENT_BYTES.decode()})
    direct_vm.mock_web(re.escape(CANDIDATE_URL), {"status": 200, "body": CANDIDATE_BYTES.decode()})
    direct_vm.mock_web(re.escape(CI_URL), {"status": 200, "body": json.dumps(ci)})
    direct_vm.mock_web(re.escape(AUDIT_URL), {"status": 200, "body": json.dumps(audit)})
    direct_vm.mock_llm(r"PROOFPATCH_SEMANTIC_REVIEW_V1", json.dumps(_semantic_checks(True)))

    assert direct_vm.run_validator() is False


def test_validator_agrees_only_when_full_bound_result_matches(direct_vm, direct_deploy, direct_alice, direct_bob):
    direct_vm.check_pickling = True
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)
    _mock_valid_evidence(direct_vm, governor, direct_bob, proposal_id, semantic_all_true=False)

    governor.review_proposal(proposal_id)
    # Do not let an identical generic retry result masquerade as successful
    # validator agreement. The leader must first reach the intended decision.
    assert governor.get_proposal_status(proposal_id) == "REJECTED"
    assert direct_vm.run_validator() is True
