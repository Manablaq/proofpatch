from pathlib import Path
import ast
import re


ROOT = Path(__file__).resolve().parents[2]


def test_all_secure_target_variants_bind_kernel_method_implementations():
    paths = [
        ROOT / "contracts" / "protected_target_v2.py",
        ROOT / "contracts" / "protected_target_v3_safe.py",
        ROOT / "contracts" / "protected_target_v3_recovery.py",
        ROOT / "contracts" / "protected_target_v3_latent_regression.py",
    ]
    manifests = []
    for path in paths:
        source = path.read_text()
        assert "def _kernel_method_digest(" in source
        assert "if len(entries) != 15" in source
        assert "self._kernel_method_digest(source, name) != digest" in source
        manifest = re.search(r"PROOFPATCH_KERNEL_SOURCE = \"\\n\"\.join\(\((.*?)\) \+ \"\\n\"", source, re.S)
        assert manifest
        methods = re.findall(r'"method:([^:]+):([0-9a-f]{64})"', manifest.group(1))
        assert len(methods) == 15
        manifests.append(manifest.group(1))
    assert len(set(manifests)) == 1


def test_assurance_timeout_is_idempotent_and_queues_bounded_recovery():
    source = (ROOT / "contracts" / "proofpatch_lifecycle_recovery_engine_v3.py").read_text()
    section = source.split("    def expire_provisional(", 1)[1].split("    def confirm_recovery(", 1)[0]
    assert "if incident_id not in self.incidents" in section
    assert "recovery_deadline=u64(now + int(policy.execution_timeout_seconds))" in section
    assert "status=STATUS_INCIDENT_CONFIRMED" in section
    assert "recovery_authorized=True" in section
    assert "self.actions.append({'kind': 'recover'" in section
    assert "if not self.incident_exists" not in section


def test_incident_repair_rebinds_only_evidence_and_is_exposed_by_both_artifacts():
    policy = (ROOT / "contracts" / "proofpatch_incident_policy_engine_v3.py").read_text()
    facade = (ROOT / "contracts" / "proofpatch_governor_v3_facade.py").read_text()
    compact = (ROOT / "contracts" / "proofpatch_governor_v3_facade_compact.py").read_text()
    assert "def _repair_incident(" in policy
    assert "STATUS_INCIDENT_REPAIR, STATUS_INCIDENT_RETRY" in policy
    assert "def repair_incident(" in facade
    assert "def repair_incident(" in compact
    assert "self._reserve_evidence_id(incident.target" in policy
    assert "incident.status = STATUS_INCIDENT_OPEN" in policy


def test_fact_builders_and_schemas_cannot_emit_publisher_verdict_vectors():
    assurance_builder = (ROOT / "scripts" / "build_assurance_evidence.py").read_text()
    incident_builder = (ROOT / "scripts" / "build_incident_evidence.py").read_text()
    assurance_schema = (ROOT / "schemas" / "assurance-evidence-v1.schema.json").read_text()
    incident_schema = (ROOT / "schemas" / "incident-evidence-v1.schema.json").read_text()
    assert "--facts" in assurance_builder and "--check" not in assurance_builder
    assert "--facts" in incident_builder and "--check" not in incident_builder
    assert '"facts"' in assurance_schema and '"facts"' in incident_schema
    assert '"checks"' not in assurance_schema and '"checks"' not in incident_schema


def test_modular_graph_is_in_preflight_contract_scope():
    preflight = (ROOT / "scripts" / "preflight.py").read_text()
    for stem in (
        "proofpatch_review_engine_v2",
        "proofpatch_fact_review_engine_v3",
        "proofpatch_incident_policy_engine_v3",
        "proofpatch_repair_policy_engine_v3",
        "proofpatch_policy_engine_v3",
        "proofpatch_registration_engine_v3",
        "proofpatch_assurance_engine_v3",
        "proofpatch_summary_engine_v3",
        "proofpatch_lifecycle_engine_v3",
        "proofpatch_lifecycle_install_engine_v3",
        "proofpatch_lifecycle_timeout_engine_v3",
        "proofpatch_lifecycle_activation_engine_v3",
        "proofpatch_lifecycle_recovery_engine_v3",
        "proofpatch_lifecycle_request_engine_v3",
        "proofpatch_review_commit_engine_v3",
        "proofpatch_review_request_engine_v3",
        "proofpatch_governor_v3_facade",
    ):
        assert f'"{stem}_compact.py"' in preflight
