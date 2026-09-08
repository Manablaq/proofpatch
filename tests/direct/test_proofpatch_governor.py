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


def _evidence(
    governor,
    target,
    proposal_id,
    *,
    now=None,
    ci_id="ci-proof-001",
    audit_id="audit-proof-001",
):
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
        "evidence_id": ci_id,
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
        "evidence_id": audit_id,
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


def test_expired_proposal_releases_target_and_cannot_remain_active(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    summary = json.loads(governor.get_proposal_summary(proposal_id))
    expires_at = int(summary["expires_at"])
    warped = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ",
        time.gmtime(expires_at + 1),
    )

    # genlayer-test 0.29.2 Direct Mode stores the warped datetime on the VM,
    # but its _refresh_gl_message() path does not propagate datetime into the
    # already-loaded SDK's gl.message_raw. ProofPatch reads the deterministic
    # transaction timestamp from gl.message_raw["datetime"], so mirror the
    # documented transaction-context value here for this pinned runner only.
    direct_vm.warp(warped)
    import sys

    contract_module = sys.modules[governor.__class__.__module__]
    contract_module.gl.message_raw["datetime"] = warped

    governor.expire_proposal(proposal_id)

    assert governor.get_proposal_status(proposal_id) == "EXPIRED"
    assert int(governor.get_active_proposal(_address_arg(direct_bob))) == 0


def test_retry_state_can_be_retried_and_reaches_fresh_review(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    direct_vm.check_pickling = True
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    direct_vm.mock_web(
        re.escape(PARENT_URL),
        {"status": 500, "body": "temporary upstream failure"},
    )
    governor.review_proposal(proposal_id)
    assert governor.get_proposal_status(proposal_id) == "REVIEW_RETRY_REQUIRED"

    direct_vm.clear_mocks()
    _mock_valid_evidence(
        direct_vm,
        governor,
        direct_bob,
        proposal_id,
        semantic_all_true=False,
    )
    governor.review_proposal(proposal_id)

    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["status"] == "REJECTED"
    assert int(summary["reviewed_at"]) > 0
    assert int(governor.get_active_proposal(_address_arg(direct_bob))) == 0


def test_repair_uses_fresh_evidence_ids_and_fresh_review_without_candidate_mutation(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    direct_vm.check_pickling = True
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    candidate_hash_before = governor.get_candidate_hash(proposal_id)
    evidence_set_before = governor.get_evidence_set_hash(proposal_id)

    direct_vm.mock_web(
        re.escape(PARENT_URL),
        {"status": 200, "body": PARENT_BYTES.decode()},
    )
    direct_vm.mock_web(
        re.escape(CANDIDATE_URL),
        {"status": 200, "body": "tampered candidate"},
    )
    governor.review_proposal(proposal_id)
    assert governor.get_proposal_status(proposal_id) == "EVIDENCE_REPAIR_REQUIRED"

    repaired_ci_url = CI_PREFIX + ("f" * 40) + "/evidence/ci-repaired.json"
    repaired_audit_url = AUDIT_PREFIX + ("1" * 40) + "/evidence/audit-repaired.json"
    repaired_ci_id = "ci-proof-repaired-002"
    repaired_audit_id = "audit-proof-repaired-002"

    direct_vm.sender = direct_alice
    governor.repair_evidence(
        proposal_id,
        REPAIRED_CANDIDATE_URL,
        repaired_ci_url,
        repaired_ci_id,
        repaired_audit_url,
        repaired_audit_id,
    )

    assert governor.get_candidate_hash(proposal_id) == candidate_hash_before
    assert governor.get_evidence_set_hash(proposal_id) != evidence_set_before
    assert governor.get_proposal_status(proposal_id) == "PROPOSED"

    direct_vm.clear_mocks()
    ci, audit = _evidence(
        governor,
        direct_bob,
        proposal_id,
        ci_id=repaired_ci_id,
        audit_id=repaired_audit_id,
    )
    direct_vm.mock_web(
        re.escape(PARENT_URL),
        {"status": 200, "body": PARENT_BYTES.decode()},
    )
    direct_vm.mock_web(
        re.escape(REPAIRED_CANDIDATE_URL),
        {"status": 200, "body": CANDIDATE_BYTES.decode()},
    )
    direct_vm.mock_web(
        re.escape(repaired_ci_url),
        {"status": 200, "body": json.dumps(ci)},
    )
    direct_vm.mock_web(
        re.escape(repaired_audit_url),
        {"status": 200, "body": json.dumps(audit)},
    )
    direct_vm.mock_llm(
        r"PROOFPATCH_SEMANTIC_REVIEW_V1",
        json.dumps(_semantic_checks(False)),
    )

    governor.review_proposal(proposal_id)

    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["status"] == "REJECTED"
    assert int(summary["reviewed_at"]) > 0
    assert governor.get_candidate_hash(proposal_id) == candidate_hash_before


def test_stale_evidence_is_repairable_and_cannot_authorize(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    now = int(time.time())
    ci, audit = _evidence(governor, direct_bob, proposal_id, now=now)
    ci["published_at"] = now - (2 * 24 * 60 * 60)
    ci["expires_at"] = now + 3600

    direct_vm.mock_web(
        re.escape(PARENT_URL),
        {"status": 200, "body": PARENT_BYTES.decode()},
    )
    direct_vm.mock_web(
        re.escape(CANDIDATE_URL),
        {"status": 200, "body": CANDIDATE_BYTES.decode()},
    )
    direct_vm.mock_web(re.escape(CI_URL), {"status": 200, "body": json.dumps(ci)})
    direct_vm.mock_web(
        re.escape(AUDIT_URL),
        {"status": 200, "body": json.dumps(audit)},
    )

    governor.review_proposal(proposal_id)

    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["status"] == "EVIDENCE_REPAIR_REQUIRED"
    assert summary["last_review_code"] == "CI_EVIDENCE_STALE"


def test_evidence_identity_is_isolated_by_target(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie
):
    governor = direct_deploy("contracts/proofpatch_governor.py")

    _register(governor, direct_vm, direct_bob, direct_alice)
    first = _create(governor, direct_vm, direct_bob, direct_alice)

    _register(governor, direct_vm, direct_charlie, direct_alice)
    second = _create(governor, direct_vm, direct_charlie, direct_alice)

    assert int(first) == 1
    assert int(second) == 2
    assert int(governor.get_active_proposal(_address_arg(direct_bob))) == 1
    assert int(governor.get_active_proposal(_address_arg(direct_charlie))) == 2


def test_validator_rejects_single_consequential_binding_mutation(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    direct_vm.check_pickling = True
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)
    _mock_valid_evidence(
        direct_vm, governor, direct_bob, proposal_id, semantic_all_true=False
    )

    governor.review_proposal(proposal_id)
    assert governor.get_proposal_status(proposal_id) == "REJECTED"

    summary = json.loads(governor.get_proposal_summary(proposal_id))
    forged = {
        "target": summary["target"],
        "proposal_id": int(proposal_id),
        "parent_code_hash": summary["parent_code_hash"],
        "candidate_code_hash": "0" * 64,
        "policy_fingerprint": summary["policy_fingerprint"],
        "evidence_set_hash": summary["evidence_set_hash"],
        "kind": "DECISION",
        "error_code": "",
        "decision": "REJECT",
        **_semantic_checks(False),
    }

    assert direct_vm.run_validator(leader_result=forged) is False


def test_validator_agrees_on_exact_all_true_approval_vector(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    direct_vm.check_pickling = True
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    # Capture the real ProofPatch validator closure without pretending that
    # Direct Mode can execute the finalized IC->IC child upgrade.
    _mock_valid_evidence(
        direct_vm, governor, direct_bob, proposal_id, semantic_all_true=False
    )
    governor.review_proposal(proposal_id)
    assert governor.get_proposal_status(proposal_id) == "REJECTED"

    direct_vm.clear_mocks()
    _mock_valid_evidence(
        direct_vm, governor, direct_bob, proposal_id, semantic_all_true=True
    )

    summary = json.loads(governor.get_proposal_summary(proposal_id))
    approval = {
        "target": summary["target"],
        "proposal_id": int(proposal_id),
        "parent_code_hash": summary["parent_code_hash"],
        "candidate_code_hash": summary["candidate_code_hash"],
        "policy_fingerprint": summary["policy_fingerprint"],
        "evidence_set_hash": summary["evidence_set_hash"],
        "kind": "DECISION",
        "error_code": "",
        "decision": "APPROVE",
        **_semantic_checks(True),
    }

    assert direct_vm.run_validator(leader_result=approval) is True

# ---------------------------------------------------------------------------
# Reviewer regression: timeout must reconcile observable target truth first.
# Direct Mode does not route real address-based cross-contract calls, so these
# tests replace only the contract-interface adapter with a deterministic fake
# while exercising the real public governor timeout method and real storage.
# ---------------------------------------------------------------------------

def _queue_timeout_regression(governor, direct_vm, proposal_id):
    import sys

    contract_module = sys.modules[governor.__class__.__module__]
    proposal = governor.proposals[proposal_id]
    proposal.status = "UPGRADE_QUEUED"

    deadline = int(proposal.created_at) + 60
    proposal.execution_deadline = contract_module.u64(deadline)

    warped = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ",
        time.gmtime(deadline + 1),
    )
    direct_vm.warp(warped)
    contract_module.gl.message_raw["datetime"] = warped
    return contract_module


def _mock_timeout_target_view(
    monkeypatch,
    contract_module,
    installed_proposal_id,
    installed_candidate_hash,
    *,
    nonfinal_proposal_id=None,
    nonfinal_candidate_hash=None,
):
    if nonfinal_proposal_id is None:
        nonfinal_proposal_id = installed_proposal_id
    if nonfinal_candidate_hash is None:
        nonfinal_candidate_hash = installed_candidate_hash

    class _TargetView:
        def __init__(self, proposal_id, candidate_hash):
            self._proposal_id = proposal_id
            self._candidate_hash = candidate_hash

        def proofpatch_installed_proposal_id(self):
            return contract_module.u256(int(self._proposal_id))

        def proofpatch_installed_candidate_hash(self):
            return self._candidate_hash

    finalized_view = _TargetView(
        installed_proposal_id,
        installed_candidate_hash,
    )
    nonfinal_view = _TargetView(
        nonfinal_proposal_id,
        nonfinal_candidate_hash,
    )

    class _TargetInterface:
        def __init__(self, _address):
            pass

        def view(
            self,
            *,
            state=contract_module.StorageType.LATEST_NON_FINAL,
        ):
            if state == contract_module.StorageType.LATEST_FINAL:
                return finalized_view
            if state == contract_module.StorageType.LATEST_NON_FINAL:
                return nonfinal_view
            raise AssertionError(
                f"Unexpected target storage state: {state!r}"
            )

    monkeypatch.setattr(
        contract_module,
        "ProofPatchTarget",
        _TargetInterface,
    )


def test_timeout_reconciles_installed_but_unconfirmed_exact_install(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    monkeypatch,
):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    contract_module = _queue_timeout_regression(
        governor,
        direct_vm,
        proposal_id,
    )
    _mock_timeout_target_view(
        monkeypatch,
        contract_module,
        proposal_id,
        CANDIDATE_HASH,
    )

    direct_vm.sender = direct_alice
    governor.mark_execution_timeout(proposal_id)

    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["status"] == "VERIFIED"
    assert summary["last_review_code"] == "INSTALL_RECONCILED_TIMEOUT"
    assert governor.get_current_version(_address_arg(direct_bob)) == "2.0.0"
    assert governor.get_current_code_hash(_address_arg(direct_bob)) == CANDIDATE_HASH
    assert int(governor.get_active_proposal(_address_arg(direct_bob))) == 0


def test_timeout_marks_genuinely_uninstalled_proposal_failed_and_releases_slot(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    monkeypatch,
):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    contract_module = _queue_timeout_regression(
        governor,
        direct_vm,
        proposal_id,
    )
    _mock_timeout_target_view(
        monkeypatch,
        contract_module,
        0,
        "",
    )

    direct_vm.sender = direct_alice
    governor.mark_execution_timeout(proposal_id)

    summary = json.loads(governor.get_proposal_summary(proposal_id))
    assert summary["status"] == "EXECUTION_FAILED"
    assert summary["last_review_code"] == "EXECUTION_TIMEOUT"
    assert governor.get_current_version(_address_arg(direct_bob)) == "1.0.0"
    assert governor.get_current_code_hash(_address_arg(direct_bob)) == PARENT_HASH
    assert int(governor.get_active_proposal(_address_arg(direct_bob))) == 0


def test_timeout_keeps_slot_locked_on_partial_install_attestation_mismatch(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    monkeypatch,
):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    contract_module = _queue_timeout_regression(
        governor,
        direct_vm,
        proposal_id,
    )
    _mock_timeout_target_view(
        monkeypatch,
        contract_module,
        proposal_id,
        "0" * 64,
    )

    direct_vm.sender = direct_alice
    with direct_vm.expect_revert(
        "Finalized target installation attestation is inconsistent; active proposal remains locked"
    ):
        governor.mark_execution_timeout(proposal_id)

    assert governor.get_proposal_status(proposal_id) == "UPGRADE_QUEUED"
    assert int(governor.get_active_proposal(_address_arg(direct_bob))) == int(proposal_id)


def test_confirm_install_accepts_exact_finalized_install(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    monkeypatch,
):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    contract_module = _queue_timeout_regression(
        governor,
        direct_vm,
        proposal_id,
    )
    _mock_timeout_target_view(
        monkeypatch,
        contract_module,
        proposal_id,
        CANDIDATE_HASH,
    )

    direct_vm.sender = direct_bob
    governor.confirm_install(
        proposal_id,
        CANDIDATE_HASH,
    )

    summary = json.loads(
        governor.get_proposal_summary(proposal_id)
    )
    assert summary["status"] == "VERIFIED"
    assert summary["last_review_code"] == "INSTALL_VERIFIED"
    assert (
        governor.get_current_code_hash(_address_arg(direct_bob))
        == CANDIDATE_HASH
    )
    assert int(
        governor.get_active_proposal(_address_arg(direct_bob))
    ) == 0


def test_confirm_install_rejects_nonfinal_only_install(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    monkeypatch,
):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    contract_module = _queue_timeout_regression(
        governor,
        direct_vm,
        proposal_id,
    )
    _mock_timeout_target_view(
        monkeypatch,
        contract_module,
        0,
        "",
        nonfinal_proposal_id=proposal_id,
        nonfinal_candidate_hash=CANDIDATE_HASH,
    )

    direct_vm.sender = direct_bob

    with direct_vm.expect_revert(
        "Target has not finalized this proposal"
    ):
        governor.confirm_install(
            proposal_id,
            CANDIDATE_HASH,
        )

    assert (
        governor.get_proposal_status(proposal_id)
        == "UPGRADE_QUEUED"
    )
    assert (
        governor.get_current_code_hash(_address_arg(direct_bob))
        == PARENT_HASH
    )
    assert int(
        governor.get_active_proposal(_address_arg(direct_bob))
    ) == int(proposal_id)


def test_reconcile_install_accepts_exact_finalized_install(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    monkeypatch,
):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    contract_module = _queue_timeout_regression(
        governor,
        direct_vm,
        proposal_id,
    )
    _mock_timeout_target_view(
        monkeypatch,
        contract_module,
        proposal_id,
        CANDIDATE_HASH,
    )

    direct_vm.sender = direct_alice
    governor.reconcile_install(proposal_id)

    summary = json.loads(
        governor.get_proposal_summary(proposal_id)
    )
    assert summary["status"] == "VERIFIED"
    assert summary["last_review_code"] == "INSTALL_RECONCILED"
    assert (
        governor.get_current_code_hash(_address_arg(direct_bob))
        == CANDIDATE_HASH
    )
    assert int(
        governor.get_active_proposal(_address_arg(direct_bob))
    ) == 0


def test_reconcile_install_rejects_nonfinal_only_install(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    monkeypatch,
):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    contract_module = _queue_timeout_regression(
        governor,
        direct_vm,
        proposal_id,
    )
    _mock_timeout_target_view(
        monkeypatch,
        contract_module,
        0,
        "",
        nonfinal_proposal_id=proposal_id,
        nonfinal_candidate_hash=CANDIDATE_HASH,
    )

    direct_vm.sender = direct_alice

    with direct_vm.expect_revert(
        "Target has not finalized this proposal"
    ):
        governor.reconcile_install(proposal_id)

    assert (
        governor.get_proposal_status(proposal_id)
        == "UPGRADE_QUEUED"
    )
    assert (
        governor.get_current_code_hash(_address_arg(direct_bob))
        == PARENT_HASH
    )
    assert int(
        governor.get_active_proposal(_address_arg(direct_bob))
    ) == int(proposal_id)


def test_timeout_keeps_slot_locked_while_exact_install_is_nonfinal(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    monkeypatch,
):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(governor, direct_vm, direct_bob, direct_alice)
    proposal_id = _create(governor, direct_vm, direct_bob, direct_alice)

    contract_module = _queue_timeout_regression(
        governor,
        direct_vm,
        proposal_id,
    )
    _mock_timeout_target_view(
        monkeypatch,
        contract_module,
        0,
        "",
        nonfinal_proposal_id=proposal_id,
        nonfinal_candidate_hash=CANDIDATE_HASH,
    )

    direct_vm.sender = direct_alice

    with direct_vm.expect_revert(
        "Target installation is pending finality; "
        "active proposal remains locked"
    ):
        governor.mark_execution_timeout(proposal_id)

    assert (
        governor.get_proposal_status(proposal_id)
        == "UPGRADE_QUEUED"
    )
    assert (
        governor.get_current_version(_address_arg(direct_bob))
        == "1.0.0"
    )
    assert (
        governor.get_current_code_hash(_address_arg(direct_bob))
        == PARENT_HASH
    )
    assert int(
        governor.get_active_proposal(_address_arg(direct_bob))
    ) == int(proposal_id)
