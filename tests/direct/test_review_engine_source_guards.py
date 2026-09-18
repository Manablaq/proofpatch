from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "contracts" / "proofpatch_review_engine_v2.py"
COMPACT_ENGINE = ROOT / "contracts" / "proofpatch_review_engine_v2_compact.py"
FACT_ENGINE = ROOT / "contracts" / "proofpatch_fact_review_engine_v3.py"
COMPACT_FACT_ENGINE = ROOT / "contracts" / "proofpatch_fact_review_engine_v3_compact.py"


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


def test_fact_review_engine_has_independent_assurance_and_incident_vectors():
    source = FACT_ENGINE.read_text()
    assert "def assure_release(" in source
    assert "def review_incident(" in source
    assert "ASSURANCE_KEYS" in source
    assert "INCIDENT_KEYS" in source
    assert "vectors[0] != vectors[1]" in source
    assert "def _semantic_facts(" in source
    assert "def _assurance_facts_error(" in source
    assert "def _incident_facts_error(" in source
    assert 'item.get("facts")' in source
    assurance = source.rsplit("    def assure_release(", 1)[1].split("    def review_incident(", 1)[0]
    incident = source.rsplit("    def review_incident(", 1)[1]
    assert "item.get(\"checks\")" not in assurance
    assert "item.get(\"checks\")" not in incident
    assert "_semantic_facts(_assurance_prompt" in assurance
    assert "_semantic_facts(_incident_prompt" in incident


def test_compact_review_engines_preserve_the_split_review_surface():
    readable = ENGINE.read_text()
    compact = COMPACT_ENGINE.read_text()
    for marker in (
        "bind_governor", "get_proposal_result", "review_proposal", "run_nondet_unsafe",
        "ProofPatchGovernorV2", "emit", "finalized",
    ):
        assert marker in readable
        assert marker in compact
    assert COMPACT_ENGINE.stat().st_size < ENGINE.stat().st_size
    fact_readable = FACT_ENGINE.read_text()
    fact_compact = COMPACT_FACT_ENGINE.read_text()
    for marker in (
        "bind_governor", "get_assurance_result", "get_incident_result",
        "assure_release", "review_incident", "run_nondet_unsafe",
        "PROOFPATCH_ASSURANCE_FACT_REVIEW_V1", "PROOFPATCH_INCIDENT_FACT_REVIEW_V1",
    ):
        assert marker in fact_readable
        assert marker in fact_compact
    assert COMPACT_FACT_ENGINE.stat().st_size < FACT_ENGINE.stat().st_size
