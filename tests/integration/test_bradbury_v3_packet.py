from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "deployments" / "bradbury-v3-deployment.json"
FACADE = ROOT / "contracts" / "proofpatch_governor_v3_facade.py"
PREFLIGHT = ROOT / "scripts" / "preflight.py"

ADDRESS = re.compile(r"^0x[0-9A-Fa-f]{40}$")
TX = re.compile(r"^0x[0-9A-Fa-f]{64}$")

CONST_TO_COMPONENT = {
    "REVIEW_ENGINE": "proposal_review",
    "ASSURANCE_REVIEW_ENGINE": "fact_review",
    "POLICY_ENGINE": "create_policy",
    "REPAIR_POLICY_ENGINE": "repair_policy",
    "INCIDENT_POLICY_ENGINE": "incident_policy",
    "REGISTRATION_ENGINE": "registration",
    "ASSURANCE_ENGINE": "assurance",
    "SUMMARY_ENGINE": "summary",
    "INSTALL_LIFECYCLE_ENGINE": "install_lifecycle",
    "TIMEOUT_LIFECYCLE_ENGINE": "timeout_lifecycle",
    "ACTIVATION_LIFECYCLE_ENGINE": "activation_lifecycle",
    "RECOVERY_LIFECYCLE_ENGINE": "recovery_lifecycle",
    "LIFECYCLE_REQUEST_ENGINE": "lifecycle_request",
    "REVIEW_COMMIT_ENGINE": "review_commit",
    "REVIEW_REQUEST_ENGINE": "review_request",
}

def packet():
    return json.loads(PACKET.read_text())

def test_packet_shape_and_identity_are_canonical():
    data = packet()
    assert data["schema"] == "proofpatch-bradbury-v3-deployment-v1"
    assert data["network"] == "GenLayer Bradbury Testnet"
    assert data["rpc"] == "https://rpc-bradbury.genlayer.com"
    assert ADDRESS.fullmatch(data["facade"])
    assert len(data["deployments"]) == 16
    assert len(data["governor_bindings"]) == 15
    assert len(data["executor_bindings"]) == 4

    addresses = [item["address"].lower() for item in data["deployments"]]
    assert len(addresses) == len(set(addresses))
    tx_ids = [
        *[item["tx"].lower() for item in data["deployments"]],
        *[item["tx"].lower() for item in data["governor_bindings"]],
        *[item["tx"].lower() for item in data["executor_bindings"]],
    ]
    assert len(tx_ids) == 35
    assert len(tx_ids) == len(set(tx_ids))
    assert all(ADDRESS.fullmatch(item["address"]) for item in data["deployments"])
    assert all(TX.fullmatch(tx) for tx in tx_ids)

def test_packet_matches_facade_component_constants():
    data = packet()
    by_name = {item["name"]: item for item in data["deployments"]}
    source = FACADE.read_text()
    assert by_name["facade"]["address"].lower() == data["facade"].lower()
    for constant, component in CONST_TO_COMPONENT.items():
        match = re.search(
            rf"^{constant}\s*=\s*['\"](0x[0-9A-Fa-f]{{40}})['\"]",
            source,
            re.MULTILINE,
        )
        assert match, constant
        assert match.group(1).lower() == by_name[component]["address"].lower()

def test_every_deployed_artifact_is_in_authoritative_preflight():
    data = packet()
    source = PREFLIGHT.read_text()
    for item in data["deployments"]:
        assert item["artifact"] in source, item["artifact"]

def test_binding_sets_cover_exact_expected_components():
    data = packet()
    deployment_names = {item["name"] for item in data["deployments"]}
    governor = {item["component"] for item in data["governor_bindings"]}
    executors = {item["component"] for item in data["executor_bindings"]}
    assert governor == deployment_names - {"facade"}
    assert executors == {
        "install_lifecycle",
        "timeout_lifecycle",
        "activation_lifecycle",
        "recovery_lifecycle",
    }
