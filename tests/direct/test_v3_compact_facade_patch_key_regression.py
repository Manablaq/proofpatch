from pathlib import Path
import ast
import pytest

ROOT = Path(__file__).resolve().parents[2]
FACADE = ROOT / "contracts" / "proofpatch_governor_v3_facade_compact.py"


def _contract_tree():
    return ast.parse(FACADE.read_text())


def _class_fields(tree, name):
    cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == name)
    return {
        item.target.id
        for item in cls.body
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name)
    }


def test_compact_facade_patch_store_selectors_name_real_compact_fields():
    text = FACADE.read_text()
    expected = (
        "for(_i,cls,_aj,_cb)in("
        "('policies',_dw,self.policies,'fbw'),"
        "('proposals',_dq,self.proposals,'fbc'),"
        "('releases',_du,self.releases,'fbq'),"
        "('incidents',_ds,self.incidents,'faj')):"
    )
    assert expected in text

    tree = _contract_tree()
    assert "fbw" in _class_fields(tree, "_dw")
    assert "fbc" in _class_fields(tree, "_dq")
    assert "fbq" in _class_fields(tree, "_du")
    assert "faj" in _class_fields(tree, "_ds")


def test_compact_facade_patch_store_selectors_do_not_use_readable_attribute_names():
    text = FACADE.read_text()
    assert "self.policies,'target'" not in text
    assert "self.proposals,_s12" not in text
    assert "self.releases,'release_id'" not in text
    assert "self.incidents,'incident_id'" not in text


@pytest.mark.parametrize(
    "contract_path",
    (
        "contracts/proofpatch_governor_v3_facade.py",
        "contracts/proofpatch_governor_v3_facade_compact.py",
    ),
)
def test_facade_state_record_serializes_storage_backed_dataclasses_in_direct_mode(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    contract_path,
):
    import json

    def address_arg(value):
        if isinstance(value, (bytes, bytearray)):
            raw = bytes(value)
            assert len(raw) == 20
            return "0x" + raw.hex()
        return str(value)

    owner = address_arg(direct_alice)
    target = address_arg(direct_bob)

    code_hash = "ab" * 32
    policy_fingerprint = "cd" * 32
    kernel_hash = "ef" * 32
    release_id = "root-" + code_hash[:16]

    policy = {
        "owner": owner,
        "target": target,
        "constitution": "slot serialization regression",
        "policy_fingerprint": policy_fingerprint,
        "source_authority": "example/source",
        "ci_authority": "example/ci",
        "audit_authority": "example/audit",
        "source_prefix": "https://example.invalid/source/",
        "ci_prefix": "https://example.invalid/ci/",
        "audit_prefix": "https://example.invalid/audit/",
        "assurance_authority": "example/assurance",
        "assurance_prefix": "https://example.invalid/assurance/",
        "assurance_corroboration_authority": "example/corroboration",
        "assurance_corroboration_prefix": "https://example.invalid/corroboration/",
        "proofpatch_kernel_hash": kernel_hash,
        "current_version": "2.0.0",
        "current_source_url": "https://example.invalid/source/commit/target.py",
        "current_code_hash": code_hash,
        "current_release_id": release_id,
        "max_evidence_age_seconds": 86400,
        "proposal_ttl_seconds": 172800,
        "execution_timeout_seconds": 86400,
        "assurance_observation_delay_seconds": 3600,
        "assurance_deadline_seconds": 7200,
        "max_manifest_bytes": 16000,
        "max_capsule_bytes": 512000,
        "active": True,
    }

    release = {
        "release_id": release_id,
        "target": target,
        "version": "2.0.0",
        "parent_release_id": "",
        "parent_code_hash": "",
        "source_url": "https://example.invalid/source/commit/target.py",
        "code_hash": code_hash,
        "proposal_id": 0,
        "policy_fingerprint": policy_fingerprint,
        "evidence_set_hash": "",
        "assurance_manifest_hash": "",
        "recovery_capsule_hash": "",
        "installed_at": 123,
        "certified_at": 123,
        "status": "REGISTERED_PARENT",
        "recovered_from_release_id": "",
        "recovery_incident_id": "",
        "lineage_hash": "12" * 32,
    }

    patch = json.dumps(
        {
            "policies": [policy],
            "proposals": [],
            "releases": [release],
            "incidents": [],
            "active": [[target, 0]],
            "used_evidence_ids": {},
            "installed_candidate_hashes": {},
            "used_incident_ids": {},
            "proposal_count": 0,
            "release_count": 0,
        },
        separators=(",", ":"),
    )

    review_commit_sender = bytes.fromhex(
        "ef8F5C807117b2A606B861e947F2ff5756Db8CE7"
    )

    # One deployment per pytest case is intentional. GenLayer Direct Mode
    # allows only one main contract class in a single fixture/runtime.
    facade = direct_deploy(contract_path)

    direct_vm.sender = review_commit_sender

    # Exercise the real facade patch-storage path without emitting a target
    # action, then read the persisted dataclasses through get_state_record().
    facade.apply_review_result(
        "register",
        patch,
    )

    policy_state = json.loads(
        facade.get_state_record(
            "policy",
            target,
        )
    )

    release_state = json.loads(
        facade.get_state_record(
            "release",
            release_id,
        )
    )

    assert policy_state["owner"].lower() == owner.lower()
    assert policy_state["target"].lower() == target.lower()
    assert policy_state["current_release_id"] == release_id
    assert policy_state["current_code_hash"] == code_hash
    assert policy_state["active"] is True

    assert release_state["release_id"] == release_id
    assert release_state["target"].lower() == target.lower()
    assert release_state["code_hash"] == code_hash
    assert release_state["status"] == "REGISTERED_PARENT"
