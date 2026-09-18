from pathlib import Path
import ast
import re


ROOT = Path(__file__).resolve().parents[2]
GOVERNOR = ROOT / "contracts" / "proofpatch_governor_v2.py"
TARGET = ROOT / "contracts" / "protected_target_v2.py"
RECOVERY_TARGET = ROOT / "contracts" / "protected_target_v3_recovery.py"
TARGET_VARIANTS = (
    TARGET,
    ROOT / "contracts" / "protected_target_v3_safe.py",
    ROOT / "contracts" / "protected_target_v3_latent_regression.py",
    RECOVERY_TARGET,
)


def _target_storage_fields():
    tree = ast.parse(TARGET.read_text())
    contract = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "ProtectedTarget")
    return [
        node.target.id
        for node in contract.body
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
    ]


def test_v2_kernel_prefix_is_explicit_and_stable():
    source = TARGET.read_text()
    assert sum(line.strip() == "# PROOFPATCH_KERNEL_BEGIN" for line in source.splitlines()) == 1
    assert sum(line.strip() == "# PROOFPATCH_KERNEL_END" for line in source.splitlines()) == 1
    fields = _target_storage_fields()
    assert fields[:12] == [
        "owner",
        "proofpatch_governor",
        "proofpatch_kernel_hash",
        "proofpatch_registered",
        "installed_release_id",
        "installed_proposal_id",
        "installed_code_hash",
        "release_mode",
        "pending_release_id",
        "pending_code_hash",
        "last_recovery_incident_id",
        "last_recovery_release_id",
    ]


def test_v2_has_no_owner_upgrade_bypass_and_guards_application_writes():
    source = TARGET.read_text()
    assert "root.upgraders.get().append(proofpatch_governor)" in source
    assert "root.upgraders.get().append(self.owner)" not in source
    assert "def _require_active_release(" in source
    assert "self._require_active_release()" in source
    assert "def proofpatch_upgrade(" in source
    assert "def proofpatch_activate(" in source
    assert "def proofpatch_recover(" in source
    assert 'PROOFPATCH_KERNEL_HASH = hashlib.sha256(PROOFPATCH_KERNEL_SOURCE.encode("utf-8")).hexdigest()' in source
    assert "_require_kernel_binding(" in source
    assert "actual_kernel_source != storage_source" in source
    assert "Candidate kernel markers are not unique" in source
    assert "def _kernel_method_digest(" in source
    assert "if len(entries) != 15" in source
    assert "self._kernel_method_digest(source, name) != digest" in source


def test_v2_all_consequential_cross_contract_messages_are_finality_gated():
    target = TARGET.read_text()
    governor = GOVERNOR.read_text()
    assert target.count('emit(on="finalized")') >= 4
    assert 'emit(on="accepted")' not in target
    assert 'emit(on="accepted")' not in governor


def test_v2_proposal_freezes_manifest_and_recovery_capsule():
    source = GOVERNOR.read_text()
    assert "assurance_manifest_hash" in source
    assert "recovery_capsule_hash" in source
    assert "recovery_code: bytes" in source
    assert "def _validate_manifest(" in source
    assert "def get_proposal_release_id(" in source


def test_v2_has_explicit_assurance_incident_and_recovery_lifecycle():
    source = GOVERNOR.read_text()
    for name in (
        "assure_release",
        "confirm_activation",
        "expire_provisional_release",
        "open_incident",
        "review_incident",
        "is_recovery_authorized",
        "get_recovery_release_id",
        "get_recovery_code",
        "confirm_recovery",
    ):
        assert f"def {name}(" in source
    assert "status=STATUS_INSTALLED_PROVISIONAL" in source
    assert "STATUS_CERTIFIED" in source
    assert re.search(r"incident\.status\s*=\s*STATUS_INCIDENT_CONFIRMED", source)
    assert "def reconcile_recovery(" in source
    assert "def retry_recovery(" in source


def test_v2_registration_is_bootstrap_until_finalized_governor_confirmation():
    source = TARGET.read_text()
    registration = source[source.index("def register_with_proofpatch("):source.index("def proofpatch_confirm_registration(")]
    assert 'self.release_mode = "ACTIVE"' not in registration
    assert "proofpatch_confirm_registration" in source
    assert "is_registration_authorized" in source


def test_v2_recovery_target_uses_precommitted_recovery_release_identity():
    source = TARGET.read_text()
    recovery = source[source.index("def proofpatch_recover("):]
    assert "get_recovery_release_id(incident_id)" in recovery
    assert "self.installed_release_id = recovery_release_id" in recovery


def test_recovery_fixture_retains_the_same_kernel_and_is_explicitly_named():
    source = RECOVERY_TARGET.read_text()
    assert "PROOFPATCH_KERNEL_BEGIN" in source
    assert 'return "ProtectedTarget/v3-recovery-capsule"' in source
    assert "def proofpatch_confirm_registration(" in source


def test_all_v2_target_variants_have_the_same_hashed_kernel_prefix():
    expected = [
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
    ]
    for path in TARGET_VARIANTS:
        source = path.read_text()
        start = source.index("# PROOFPATCH_KERNEL_BEGIN") + len("# PROOFPATCH_KERNEL_BEGIN")
        end = source.index("# PROOFPATCH_KERNEL_END", start)
        actual = [line.strip() for line in source[start:end].splitlines() if line.strip() and not line.strip().startswith("#")]
        assert actual == expected
        assert source.count("def proofpatch_confirm_registration(") == 1
        assert source.count("def proofpatch_upgrade(") == 1
        assert source.count("def proofpatch_activate(") == 1
        assert source.count("def proofpatch_recover(") == 1
