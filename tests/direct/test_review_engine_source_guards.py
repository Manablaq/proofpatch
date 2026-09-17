from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "contracts" / "proofpatch_review_engine_v2.py"
COMPACT_ENGINE = ROOT / "contracts" / "proofpatch_review_engine_v2_compact.py"


def test_review_engine_is_finality_bound_and_independently_validates_results():
    source = ENGINE.read_text()
    assert "def bind_governor(" in source
    assert "self.governor != Address(ZERO)" in source
    assert "def _only_governor(" in source
    assert "run_nondet_unsafe" in source
    assert "_same(leader_result.calldata, leader(), SEMANTIC_KEYS)" in source
    assert "ProofPatchGovernorV2(self.governor).emit(on=\"finalized\")" in source
    assert "def _manifest_error(" in source
    assert '"candidate_code_hex"' in source
    assert '"recovery_code_hex"' in source


def test_review_engine_has_independent_assurance_and_incident_vectors():
    source = ENGINE.read_text()
    assert "def assure_release(" in source
    assert "def review_incident(" in source
    assert "ASSURANCE_KEYS" in source
    assert "INCIDENT_KEYS" in source
    assert "vectors[0] != vectors[1]" in source


def test_compact_review_engine_preserves_the_review_surface():
    readable = ENGINE.read_text()
    compact = COMPACT_ENGINE.read_text()
    for marker in (
        "bind_governor", "get_proposal_result", "get_assurance_result", "get_incident_result",
        "review_proposal", "assure_release", "review_incident", "run_nondet_unsafe",
        "ProofPatchGovernorV2", "emit", "finalized",
    ):
        assert marker in readable
        assert marker in compact
    assert COMPACT_ENGINE.stat().st_size < ENGINE.stat().st_size
