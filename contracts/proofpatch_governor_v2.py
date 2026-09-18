# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
from dataclasses import dataclass
from datetime import datetime
from genlayer.py.public_abi import StorageType
import hashlib
import json
import typing


SCHEMA_VERSION = "proofpatch-v2"
EVIDENCE_SCHEMA = "proofpatch-evidence-v2"
ASSURANCE_SCHEMA = "proofpatch-assurance-v1"
INCIDENT_SCHEMA = "proofpatch-incident-v1"

MODE_BOOTSTRAP = "BOOTSTRAP"
MODE_ACTIVE = "ACTIVE"
MODE_PROVISIONAL = "PROVISIONAL"
MODE_RECOVERY_PENDING = "RECOVERY_PENDING"
MODE_RECOVERED = "RECOVERED"

STATUS_PROPOSED = "PROPOSED"
STATUS_REPAIR = "EVIDENCE_REPAIR_REQUIRED"
STATUS_RETRY = "REVIEW_RETRY_REQUIRED"
STATUS_REJECTED = "REJECTED"
STATUS_QUEUED = "UPGRADE_QUEUED"
STATUS_INSTALLED_PROVISIONAL = "INSTALLED_PROVISIONAL"
STATUS_ASSURANCE_PENDING = "ASSURANCE_PENDING"
STATUS_ASSURANCE_REPAIR = "ASSURANCE_REPAIR_REQUIRED"
STATUS_ASSURANCE_RETRY = "ASSURANCE_RETRY_REQUIRED"
STATUS_CERTIFICATION_QUEUED = "CERTIFICATION_QUEUED"
STATUS_CERTIFIED = "CERTIFIED"
STATUS_VERIFIED = STATUS_CERTIFIED
STATUS_EXPIRED = "EXPIRED"
STATUS_CANCELLED = "CANCELLED"
STATUS_EXECUTION_FAILED = "EXECUTION_FAILED"
STATUS_INCIDENT_OPEN = "INCIDENT_OPEN"
STATUS_INCIDENT_REPAIR = "INCIDENT_REPAIR_REQUIRED"
STATUS_INCIDENT_RETRY = "INCIDENT_RETRY_REQUIRED"
STATUS_INCIDENT_CONFIRMED = "INCIDENT_CONFIRMED"
STATUS_INCIDENT_DISMISSED = "INCIDENT_DISMISSED"
STATUS_RECOVERY_QUEUED = "RECOVERY_QUEUED"
STATUS_RECOVERY_RETRY = "RECOVERY_RETRY_REQUIRED"
STATUS_RECOVERED = "RECOVERED"

REVIEW_REPAIR = "REPAIR"
REVIEW_RETRY = "RETRY"
REVIEW_DECISION = "DECISION"
DECISION_APPROVE = "APPROVE"
DECISION_REJECT = "REJECT"

ASSURANCE_KEYS = (
    "installed_hash_matches",
    "kernel_binding_matches",
    "governor_binding_matches",
    "critical_state_preserved",
    "interface_requirements_hold",
    "canary_requirements_hold",
    "runtime_evidence_valid",
    "no_post_install_security_regression",
    "recovery_path_live",
    "assurance_manifest_satisfied",
)

INCIDENT_KEYS = (
    "incident_evidence_authentic",
    "incident_affects_exact_release",
    "incident_reproducible_or_sufficiently_established",
    "constitution_breached",
    "continued_operation_unsafe",
    "recovery_capsule_applicable",
    "recovery_safer_than_continuation",
    "recovery_path_preserves_rights",
    "recovery_path_preserves_governance",
)

MAX_CONSTITUTION_BYTES = 16_000
MAX_CANDIDATE_BYTES = 512_000
MAX_URL_BYTES = 1_024
MAX_ID_BYTES = 160
MAX_VERSION_BYTES = 96
MAX_EVIDENCE_AGE_SECONDS = 30 * 24 * 60 * 60
MAX_PROPOSAL_TTL_SECONDS = 14 * 24 * 60 * 60
MAX_EXECUTION_TIMEOUT_SECONDS = 7 * 24 * 60 * 60
MIN_WINDOW_SECONDS = 60

SEMANTIC_KEYS = (
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
)

REVIEW_ENGINE = "0x827798efCcE0a74a8dEc44bBA7A73445786A1c4C"
STATUS_REVIEW_PENDING = "REVIEW_PENDING"
STATUS_INCIDENT_REVIEW_PENDING = "INCIDENT_REVIEW_PENDING"


@gl.contract_interface
class ProofPatchReviewEngine:
    class View:
        def get_proposal_result(self, proposal_id: u256) -> str: ...
        def get_assurance_result(self, proposal_id: u256) -> str: ...
        def get_incident_result(self, incident_id: str) -> str: ...

    class Write:
        def review_proposal(self, proposal_id: u256, snapshot: str) -> None: ...
        def assure_release(self, proposal_id: u256, snapshot: str) -> None: ...
        def review_incident(self, incident_id: str, snapshot: str) -> None: ...


@allow_storage
@dataclass
class TargetPolicy:
    owner: Address
    target: Address
    constitution: str
    policy_fingerprint: str
    source_authority: str
    ci_authority: str
    audit_authority: str
    source_prefix: str
    ci_prefix: str
    audit_prefix: str
    assurance_authority: str
    assurance_prefix: str
    assurance_corroboration_authority: str
    assurance_corroboration_prefix: str
    proofpatch_kernel_hash: str
    current_version: str
    current_source_url: str
    current_code_hash: str
    current_release_id: str
    max_evidence_age_seconds: u64
    proposal_ttl_seconds: u64
    execution_timeout_seconds: u64
    assurance_observation_delay_seconds: u64
    assurance_deadline_seconds: u64
    max_manifest_bytes: u64
    max_capsule_bytes: u64
    active: bool


@allow_storage
@dataclass
class UpgradeProposal:
    proposal_id: u256
    target: Address
    proposer: Address
    parent_version: str
    parent_source_url: str
    parent_code_hash: str
    candidate_version: str
    candidate_source_url: str
    candidate_code: bytes
    candidate_code_hash: str
    ci_evidence_url: str
    ci_evidence_id: str
    audit_evidence_url: str
    audit_evidence_id: str
    assurance_manifest: str
    assurance_manifest_hash: str
    recovery_mode: str
    recovery_release_id: str
    recovery_version: str
    recovery_source_url: str
    recovery_code: bytes
    recovery_code_hash: str
    recovery_capsule_hash: str
    evidence_set_hash: str
    policy_fingerprint: str
    created_at: u64
    expires_at: u64
    reviewed_at: u64
    execution_deadline: u64
    status: str
    last_review_code: str


@allow_storage
@dataclass
class ReleaseRecord:
    release_id: str
    target: Address
    version: str
    parent_release_id: str
    parent_code_hash: str
    source_url: str
    code_hash: str
    proposal_id: u256
    policy_fingerprint: str
    evidence_set_hash: str
    assurance_manifest_hash: str
    recovery_capsule_hash: str
    installed_at: u64
    certified_at: u64
    status: str
    recovered_from_release_id: str
    recovery_incident_id: str
    lineage_hash: str


@allow_storage
@dataclass
class IncidentRecord:
    incident_id: str
    target: Address
    release_id: str
    installed_code_hash: str
    incident_type: str
    primary_url: str
    primary_evidence_id: str
    corroboration_url: str
    corroboration_evidence_id: str
    policy_fingerprint: str
    assurance_manifest_hash: str
    recovery_capsule_hash: str
    opened_at: u64
    expires_at: u64
    reviewed_at: u64
    recovery_deadline: u64
    status: str
    last_review_code: str
    recovery_authorized: bool


@gl.contract_interface
class ProofPatchTarget:
    class View:
        def proofpatch_installed_proposal_id(self) -> u256: ...
        def proofpatch_installed_candidate_hash(self) -> str: ...
        def proofpatch_installed_release_id(self) -> str: ...
        def proofpatch_release_mode(self) -> str: ...
        def get_proofpatch_kernel_hash(self) -> str: ...
        def get_proofpatch_governor(self) -> Address: ...

    class Write:
        def proofpatch_confirm_registration(self, release_id: str, code_hash: str) -> None: ...
        def proofpatch_upgrade(self, proposal_id: u256, candidate_hash: str) -> None: ...
        def proofpatch_activate(self, release_id: str, candidate_hash: str) -> None: ...
        def proofpatch_recover(self, incident_id: str, release_id: str, recovery_hash: str) -> None: ...






























class ProofPatchGovernorV2(gl.Contract):
    """Immutable consensus governor for continuous release assurance.

    Security model:
    - each target self-registers an immutable policy;
    - the target makes this governor its sole GenVM upgrader;
    - every candidate is frozen by exact bytes + SHA-256 before review;
    - authority prefixes are immutable raw GitHub repository prefixes;
    - audit evidence must come from a GitHub owner distinct from the source owner;
    - validators independently fetch and re-evaluate the exact evidence and source;
    - all authorization-driving semantic booleans must match exactly;
    - approved upgrade messages are emitted only on GenLayer finality;
    - installation creates a PROVISIONAL release;
    - only finalized assurance activates a release;
    - only a precommitted recovery capsule can recover a release.

    This contract intentionally has no self-upgrade entry point.
    """

    policies: TreeMap[Address, TargetPolicy]
    proposals: TreeMap[u256, UpgradeProposal]
    releases: TreeMap[str, ReleaseRecord]
    incidents: TreeMap[str, IncidentRecord]
    active_proposal_by_target: TreeMap[Address, u256]
    used_evidence_ids: TreeMap[str, bool]
    installed_candidate_hashes: TreeMap[str, bool]
    used_incident_ids: TreeMap[str, bool]
    proposal_count: u256
    release_count: u256

    def __init__(self):
        self.proposal_count = u256(0)
        self.release_count = u256(0)

    # ---------------------------------------------------------------------
    # Deterministic helpers
    # ---------------------------------------------------------------------

    def _now(self) -> int:
        raw = str(gl.message_raw["datetime"])
        return int(datetime.fromisoformat(raw.replace("Z", "+00:00")).timestamp())

    def _sha256_hex(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def _hash_text_parts(self, parts: list[str]) -> str:
        return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()

    def _is_hex_hash(self, value: str) -> bool:
        if len(value) != 64:
            return False
        for char in value:
            if char not in "0123456789abcdef":
                return False
        return True

    def _canonical_json_hash(self, value: str) -> tuple[str, object]:
        try:
            parsed = json.loads(value)
            canonical = json.dumps(parsed, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            if canonical != value:
                return "NONCANONICAL", parsed
            return self._sha256_hex(canonical.encode("utf-8")), parsed
        except Exception:
            return "INVALID", None

    def _validate_manifest(
        self,
        manifest: str,
        expected_target: Address,
        expected_candidate_hash: str,
        expected_policy_hash: str,
        expected_kernel_hash: str,
        policy: TargetPolicy,
    ) -> str:
        if len(manifest.encode("utf-8")) > int(policy.max_manifest_bytes):
            return "MANIFEST_TOO_LARGE"
        manifest_hash, parsed = self._canonical_json_hash(manifest)
        if manifest_hash in ("INVALID", "NONCANONICAL") or not isinstance(parsed, dict):
            return "MANIFEST_NOT_CANONICAL_JSON"
        obj = typing.cast(dict[object, object], parsed)
        required = (
            "schema", "target", "candidate_sha256", "policy_fingerprint",
            "expected_kernel_hash", "expected_release_version",
            "observation_delay_seconds", "assurance_deadline_seconds",
            "ci_assurance_evidence_required", "independent_assurance_required",
        )
        for key in required:
            if key not in obj:
                return "MANIFEST_MISSING_" + key.upper()
        if obj.get("schema") != ASSURANCE_SCHEMA:
            return "MANIFEST_SCHEMA_MISMATCH"
        target_value = obj.get("target")
        if not isinstance(target_value, str) or target_value.lower() != str(expected_target).lower():
            return "MANIFEST_TARGET_MISMATCH"
        if obj.get("candidate_sha256") != expected_candidate_hash:
            return "MANIFEST_CANDIDATE_HASH_MISMATCH"
        if obj.get("policy_fingerprint") != expected_policy_hash:
            return "MANIFEST_POLICY_MISMATCH"
        if obj.get("expected_kernel_hash") != expected_kernel_hash:
            return "MANIFEST_KERNEL_MISMATCH"
        if type(obj.get("observation_delay_seconds")) is not int:
            return "MANIFEST_OBSERVATION_DELAY_INVALID"
        if type(obj.get("assurance_deadline_seconds")) is not int:
            return "MANIFEST_ASSURANCE_DEADLINE_INVALID"
        if obj.get("observation_delay_seconds") != int(policy.assurance_observation_delay_seconds):
            return "MANIFEST_OBSERVATION_DELAY_MISMATCH"
        if obj.get("assurance_deadline_seconds") != int(policy.assurance_deadline_seconds):
            return "MANIFEST_ASSURANCE_DEADLINE_MISMATCH"
        if obj.get("ci_assurance_evidence_required") is not True:
            return "MANIFEST_CI_ASSURANCE_REQUIRED"
        if obj.get("independent_assurance_required") is not True:
            return "MANIFEST_INDEPENDENT_ASSURANCE_REQUIRED"
        for list_key in ("required_state_checks", "required_readback_checks", "required_canary_checks"):
            value_raw = obj.get(list_key, [])
            if not isinstance(value_raw, list):
                return "MANIFEST_" + list_key.upper() + "_INVALID"
            value = typing.cast(list[object], value_raw)
            if len(value) > 32:
                return "MANIFEST_" + list_key.upper() + "_INVALID"
            for item in value:
                if not isinstance(item, str) or len(item.encode("utf-8")) > 160:
                    return "MANIFEST_" + list_key.upper() + "_ITEM_INVALID"
        return ""

    def _check_text(self, value: str, label: str, minimum: int, maximum: int) -> None:
        encoded_len = len(value.encode("utf-8"))
        if encoded_len < minimum or encoded_len > maximum:
            raise gl.vm.UserError(f"{label} length is invalid")

    def _check_range(self, value: int, label: str, minimum: int, maximum: int) -> None:
        if value < minimum or value > maximum:
            raise gl.vm.UserError(f"{label} is outside supported bounds")

    def _is_canonical_raw_segment(self, value: str) -> bool:
        """Accept only a single parser-stable raw-GitHub path representation.

        ProofPatch compares the raw URL before GenVM hands it to an HTTP URL
        parser. Restricting every path component to this canonical ASCII form
        prevents dot-segment, percent-encoding, backslash, control-character,
        repeated-separator, and Unicode-normalization aliases from changing the
        resource that is actually fetched.
        """
        if not value or value in (".", ".."):
            return False

        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
        for char in value:
            if char not in allowed:
                return False
        return True

    def _raw_github_owner(self, prefix: str) -> str:
        base = "https://raw.githubusercontent.com/"
        if not prefix.startswith(base) or not prefix.endswith("/"):
            return ""

        rest = prefix[len(base):]
        parts = rest.split("/")
        if len(parts) != 3 or parts[2] != "":
            return ""

        owner = parts[0]
        repository = parts[1]

        if not self._is_canonical_raw_segment(owner):
            return ""
        if not self._is_canonical_raw_segment(repository):
            return ""

        return owner

    def _is_authority_prefix(self, prefix: str) -> bool:
        return self._raw_github_owner(prefix) != ""

    def _is_immutable_url(self, url: str, prefix: str) -> bool:
        if len(url.encode("utf-8")) > MAX_URL_BYTES:
            return False

        if not self._is_authority_prefix(prefix):
            return False

        if not url.startswith(prefix):
            return False

        suffix = url[len(prefix):]
        parts = suffix.split("/", 1)
        if len(parts) != 2:
            return False

        commit, path = parts

        if len(commit) != 40:
            return False
        for char in commit:
            if char not in "0123456789abcdef":
                return False

        path_segments = path.split("/")
        if not path_segments:
            return False

        for segment in path_segments:
            if not self._is_canonical_raw_segment(segment):
                return False

        return True

    def _policy_fingerprint(
        self,
        target: Address,
        owner: Address,
        constitution: str,
        source_authority: str,
        ci_authority: str,
        audit_authority: str,
        source_prefix: str,
        ci_prefix: str,
        audit_prefix: str,
        max_evidence_age_seconds: int,
        proposal_ttl_seconds: int,
        execution_timeout_seconds: int,
        assurance_authority: str,
        assurance_prefix: str,
        assurance_corroboration_authority: str,
        assurance_corroboration_prefix: str,
        proofpatch_kernel_hash: str,
        assurance_observation_delay_seconds: int,
        assurance_deadline_seconds: int,
        max_manifest_bytes: int,
        max_capsule_bytes: int,
    ) -> str:
        return self._hash_text_parts([
            SCHEMA_VERSION,
            str(target),
            str(owner),
            constitution,
            source_authority,
            ci_authority,
            audit_authority,
            source_prefix,
            ci_prefix,
            audit_prefix,
            str(max_evidence_age_seconds),
            str(proposal_ttl_seconds),
            str(execution_timeout_seconds),
            assurance_authority,
            assurance_prefix,
            assurance_corroboration_authority,
            assurance_corroboration_prefix,
            proofpatch_kernel_hash,
            str(assurance_observation_delay_seconds),
            str(assurance_deadline_seconds),
            str(max_manifest_bytes),
            str(max_capsule_bytes),
        ])

    def _evidence_set_hash(
        self,
        candidate_source_url: str,
        ci_evidence_url: str,
        ci_evidence_id: str,
        audit_evidence_url: str,
        audit_evidence_id: str,
        assurance_manifest_hash: str,
        recovery_capsule_hash: str,
    ) -> str:
        return self._hash_text_parts([
            SCHEMA_VERSION,
            candidate_source_url,
            ci_evidence_url,
            ci_evidence_id,
            audit_evidence_url,
            audit_evidence_id,
            assurance_manifest_hash,
            recovery_capsule_hash,
        ])

    def _inactive_proposal(self) -> u256:
        return u256(0)

    def _require_policy_owner(self, target: Address) -> TargetPolicy:
        if target not in self.policies:
            raise gl.vm.UserError("Target is not registered")
        policy = self.policies[target]
        if gl.message.sender_address != policy.owner:
            raise gl.vm.UserError("Only the registered target owner may perform this action")
        if not policy.active:
            raise gl.vm.UserError("Target policy is inactive")
        return policy

    def _require_proposal(self, proposal_id: u256) -> UpgradeProposal:
        if proposal_id not in self.proposals:
            raise gl.vm.UserError("Unknown proposal")
        return self.proposals[proposal_id]

    def _release_active(self, target: Address, proposal_id: u256) -> None:
        active = self.active_proposal_by_target.get(target, self._inactive_proposal())
        if active == proposal_id:
            self.active_proposal_by_target[target] = self._inactive_proposal()

    def _reserve_evidence_id(self, target: Address, issuer: str, kind: str, evidence_id: str) -> None:
        self._check_text(evidence_id, "evidence_id", 8, MAX_ID_BYTES)
        # Scope anti-reuse by protected target + registered issuer + evidence kind.
        # This prevents cross-target namespace squatting while still blocking replay for the same authority.
        reuse_key = self._hash_text_parts([str(target), issuer, kind, evidence_id])
        if self.used_evidence_ids.get(reuse_key, False):
            raise gl.vm.UserError("Evidence identifier has already been used")
        self.used_evidence_ids[reuse_key] = True

    def _installed_candidate_key(self, target: Address, candidate_hash: str) -> str:
        return self._hash_text_parts([str(target), candidate_hash])

    def _proposal_release_id(self, proposal: UpgradeProposal) -> str:
        return "release-" + str(proposal.proposal_id) + "-" + proposal.candidate_code_hash[:16]

    def _recovery_release_id(self, proposal: UpgradeProposal) -> str:
        if proposal.recovery_mode == "EXACT_PARENT":
            return proposal.recovery_release_id
        return proposal.recovery_release_id

    def _lineage_hash(
        self,
        target: Address,
        previous_lineage_hash: str,
        release_id: str,
        parent_release_id: str,
        version: str,
        code_hash: str,
        policy_fingerprint: str,
        evidence_set_hash: str,
        assurance_manifest_hash: str,
        recovery_capsule_hash: str,
    ) -> str:
        return self._hash_text_parts([
            SCHEMA_VERSION,
            str(target),
            previous_lineage_hash,
            release_id,
            parent_release_id,
            version,
            code_hash,
            policy_fingerprint,
            evidence_set_hash,
            assurance_manifest_hash,
            recovery_capsule_hash,
        ])

    def _record_verified_install(
        self,
        proposal_id: u256,
        proposal: UpgradeProposal,
        review_code: str,
    ) -> None:
        """Record exact installation without confusing it with certification."""
        policy = self.policies[proposal.target]
        if policy.current_code_hash != proposal.parent_code_hash:
            raise gl.vm.UserError("Target policy parent changed before installation reconciliation")

        release_id = self._proposal_release_id(proposal)
        if release_id in self.releases:
            existing = self.releases[release_id]
            if existing.code_hash != proposal.candidate_code_hash:
                raise gl.vm.UserError("Conflicting release identity")
            proposal.status = STATUS_INSTALLED_PROVISIONAL
            return
        parent_release = self.releases.get(policy.current_release_id)
        if parent_release is None:
            raise gl.vm.UserError("Current certified release is missing")
        now = self._now()
        lineage_hash = self._lineage_hash(
            proposal.target,
            parent_release.lineage_hash,
            release_id,
            policy.current_release_id,
            proposal.candidate_version,
            proposal.candidate_code_hash,
            proposal.policy_fingerprint,
            proposal.evidence_set_hash,
            proposal.assurance_manifest_hash,
            proposal.recovery_capsule_hash,
        )
        self.releases[release_id] = ReleaseRecord(
            release_id=release_id,
            target=proposal.target,
            version=proposal.candidate_version,
            parent_release_id=policy.current_release_id,
            parent_code_hash=proposal.parent_code_hash,
            source_url=proposal.candidate_source_url,
            code_hash=proposal.candidate_code_hash,
            proposal_id=proposal_id,
            policy_fingerprint=proposal.policy_fingerprint,
            evidence_set_hash=proposal.evidence_set_hash,
            assurance_manifest_hash=proposal.assurance_manifest_hash,
            recovery_capsule_hash=proposal.recovery_capsule_hash,
            installed_at=u64(now),
            certified_at=u64(0),
            status=STATUS_INSTALLED_PROVISIONAL,
            recovered_from_release_id="",
            recovery_incident_id="",
            lineage_hash=lineage_hash,
        )
        proposal.status = STATUS_INSTALLED_PROVISIONAL
        proposal.last_review_code = review_code
        self.installed_candidate_hashes[
            self._installed_candidate_key(proposal.target, proposal.candidate_code_hash)
        ] = True

    def _engine(self):
        return ProofPatchReviewEngine(Address(REVIEW_ENGINE))

    def _engine_result(self, raw: str, expected: dict[str, object]) -> dict[object, object]:
        try:
            decoded: object = json.loads(raw)
        except Exception:
            raise gl.vm.UserError("Review engine returned invalid JSON")
        if not isinstance(decoded, dict):
            raise gl.vm.UserError("Review engine returned an invalid result")
        value = typing.cast(dict[str, object], decoded)
        for key, expected_value in expected.items():
            if value.get(key) != expected_value:
                raise gl.vm.UserError("Review engine result binding mismatch")
        return typing.cast(dict[object, object], value)

    def _proposal_review_snapshot(self, proposal: UpgradeProposal, policy: TargetPolicy, now: int) -> str:
        manifest_error = self._validate_manifest(
            proposal.assurance_manifest, proposal.target, proposal.candidate_code_hash,
            proposal.policy_fingerprint, policy.proofpatch_kernel_hash, policy,
        )
        return json.dumps({
            "proposal_id": int(proposal.proposal_id), "target": str(proposal.target),
            "parent_version": proposal.parent_version, "parent_source_url": proposal.parent_source_url,
            "parent_code_hash": proposal.parent_code_hash, "candidate_version": proposal.candidate_version,
            "candidate_source_url": proposal.candidate_source_url, "candidate_code_hash": proposal.candidate_code_hash,
            "candidate_code_hex": proposal.candidate_code.hex(), "ci_evidence_url": proposal.ci_evidence_url,
            "ci_evidence_id": proposal.ci_evidence_id, "audit_evidence_url": proposal.audit_evidence_url,
            "audit_evidence_id": proposal.audit_evidence_id, "assurance_manifest": proposal.assurance_manifest,
            "assurance_manifest_hash": proposal.assurance_manifest_hash, "recovery_mode": proposal.recovery_mode,
            "recovery_release_id": proposal.recovery_release_id, "recovery_version": proposal.recovery_version,
            "recovery_source_url": proposal.recovery_source_url, "recovery_code_hash": proposal.recovery_code_hash,
            "recovery_capsule_hash": proposal.recovery_capsule_hash, "recovery_code_hex": proposal.recovery_code.hex(),
            "evidence_set_hash": proposal.evidence_set_hash, "policy_fingerprint": proposal.policy_fingerprint,
            "constitution": policy.constitution, "kernel_hash": policy.proofpatch_kernel_hash,
            "ci_authority": policy.ci_authority, "audit_authority": policy.audit_authority,
            "max_evidence_age_seconds": int(policy.max_evidence_age_seconds),
            "max_manifest_bytes": int(policy.max_manifest_bytes),
            "observation_delay_seconds": int(policy.assurance_observation_delay_seconds),
            "assurance_deadline_seconds": int(policy.assurance_deadline_seconds),
            "review_now": now, "manifest_error": manifest_error,
        }, sort_keys=True, separators=(",", ":"))

    def _apply_proposal_review(self, proposal_id: u256, result: dict[object, object]) -> None:
        proposal = self._require_proposal(proposal_id)
        policy = self.policies[proposal.target]
        if result["kind"] == REVIEW_REPAIR:
            proposal.status = STATUS_REPAIR
            proposal.last_review_code = str(result.get("error_code", ""))
            return
        if result["kind"] == REVIEW_RETRY:
            proposal.status = STATUS_RETRY
            proposal.last_review_code = str(result.get("error_code", ""))
            return
        if result["kind"] != REVIEW_DECISION:
            raise gl.vm.UserError("Unexpected review result")
        proposal.last_review_code = str(result.get("error_code", ""))
        if result["decision"] == DECISION_REJECT:
            proposal.status = STATUS_REJECTED
            self._release_active(proposal.target, proposal_id)
            return
        if result["decision"] != DECISION_APPROVE:
            raise gl.vm.UserError("Unexpected decision")
        proposal.status = STATUS_QUEUED
        proposal.execution_deadline = u64(self._now() + int(policy.execution_timeout_seconds))
        ProofPatchTarget(proposal.target).emit(on="finalized").proofpatch_upgrade(
            proposal_id, proposal.candidate_code_hash,
        )

    def _assurance_snapshot(self, proposal: UpgradeProposal, policy: TargetPolicy, release_id: str,
                            primary_url: str, primary_id: str, corroboration_url: str,
                            corroboration_id: str, now: int, target_view: typing.Any) -> str:
        return json.dumps({
            "target": str(proposal.target), "proposal_id": int(proposal.proposal_id),
            "release_id": release_id, "candidate_code_hash": proposal.candidate_code_hash,
            "policy_fingerprint": proposal.policy_fingerprint, "assurance_manifest_hash": proposal.assurance_manifest_hash,
            "primary_url": primary_url, "primary_evidence_id": primary_id,
            "corroboration_url": corroboration_url, "corroboration_evidence_id": corroboration_id,
            "assurance_authority": policy.assurance_authority,
            "corroboration_authority": policy.assurance_corroboration_authority,
            "max_evidence_age_seconds": int(policy.max_evidence_age_seconds), "review_now": now,
            "installed_proposal_id": int(target_view.proofpatch_installed_proposal_id()),
            "installed_candidate_hash": target_view.proofpatch_installed_candidate_hash(),
            "installed_release_id": target_view.proofpatch_installed_release_id(),
            "installed_mode": target_view.proofpatch_release_mode(),
            "installed_kernel_hash": target_view.get_proofpatch_kernel_hash(),
            "target_governor": str(target_view.get_proofpatch_governor()),
            "expected_governor": str(gl.message.contract_address),
            "kernel_hash": policy.proofpatch_kernel_hash,
            "assurance_manifest": proposal.assurance_manifest,
            "recovery_release_id": proposal.recovery_release_id,
        }, sort_keys=True, separators=(",", ":"))

    def _apply_assurance_result(self, proposal_id: u256, result: dict[object, object],
                                primary_url: str, primary_id: str, corroboration_url: str,
                                corroboration_id: str) -> None:
        proposal = self._require_proposal(proposal_id)
        release_id = self._proposal_release_id(proposal)
        if result["kind"] == REVIEW_REPAIR:
            proposal.status = STATUS_ASSURANCE_REPAIR
            proposal.last_review_code = str(result.get("error_code", ""))
            return
        if result["kind"] == REVIEW_RETRY:
            proposal.status = STATUS_ASSURANCE_RETRY
            proposal.last_review_code = str(result.get("error_code", ""))
            return
        proposal.last_review_code = str(result.get("error_code", ""))
        if result.get("decision") == DECISION_APPROVE:
            proposal.status = STATUS_CERTIFICATION_QUEUED
            self.releases[release_id].status = STATUS_CERTIFICATION_QUEUED
            ProofPatchTarget(proposal.target).emit(on="finalized").proofpatch_activate(
                release_id, proposal.candidate_code_hash,
            )
            return
        proposal.status = STATUS_INCIDENT_OPEN
        now = self._now()
        policy = self.policies[proposal.target]
        self.incidents["assurance-" + release_id] = IncidentRecord(
            incident_id="assurance-" + release_id, target=proposal.target, release_id=release_id,
            installed_code_hash=proposal.candidate_code_hash, incident_type="ASSURANCE_FAILURE",
            primary_url=primary_url, primary_evidence_id=primary_id, corroboration_url=corroboration_url,
            corroboration_evidence_id=corroboration_id, policy_fingerprint=proposal.policy_fingerprint,
            assurance_manifest_hash=proposal.assurance_manifest_hash, recovery_capsule_hash=proposal.recovery_capsule_hash,
            opened_at=u64(now), expires_at=u64(now + int(policy.proposal_ttl_seconds)), reviewed_at=u64(now),
            recovery_deadline=u64(0), status=STATUS_INCIDENT_OPEN, last_review_code="ASSURANCE_FAILED",
            recovery_authorized=False,
        )
        self.releases[release_id].status = STATUS_INCIDENT_OPEN

    def _incident_snapshot(self, incident: IncidentRecord, policy: TargetPolicy, release: ReleaseRecord,
                           proposal: UpgradeProposal, now: int) -> str:
        return json.dumps({
            "incident_id": incident.incident_id, "target": str(incident.target), "release_id": incident.release_id,
            "installed_code_hash": incident.installed_code_hash, "incident_type": incident.incident_type,
            "primary_url": incident.primary_url, "primary_evidence_id": incident.primary_evidence_id,
            "corroboration_url": incident.corroboration_url, "corroboration_evidence_id": incident.corroboration_evidence_id,
            "policy_fingerprint": incident.policy_fingerprint, "recovery_capsule_hash": incident.recovery_capsule_hash,
            "audit_authority": policy.audit_authority, "corroboration_authority": policy.assurance_corroboration_authority,
            "max_evidence_age_seconds": int(policy.max_evidence_age_seconds), "review_now": now,
            "release_code_hash": release.code_hash, "proposal_recovery_capsule_hash": proposal.recovery_capsule_hash,
            "proposal_recovery_release_id": proposal.recovery_release_id,
        }, sort_keys=True, separators=(",", ":"))

    def _apply_incident_result(self, incident_id: str, result: dict[object, object]) -> None:
        incident = self.incidents[incident_id]
        release = self.releases[incident.release_id]
        proposal = self.proposals[release.proposal_id]
        incident.reviewed_at = u64(self._now())
        incident.last_review_code = str(result.get("error_code", ""))
        if result["kind"] == REVIEW_REPAIR:
            incident.status = STATUS_INCIDENT_REPAIR
            return
        if result["kind"] == REVIEW_RETRY:
            incident.status = STATUS_INCIDENT_RETRY
            return
        if result.get("decision") != DECISION_APPROVE:
            incident.status = STATUS_INCIDENT_DISMISSED
            mode = ProofPatchTarget(incident.target).view(state=StorageType.LATEST_FINAL).proofpatch_release_mode()
            release.status = STATUS_INSTALLED_PROVISIONAL if mode == MODE_PROVISIONAL else STATUS_CERTIFIED
            proposal.status = STATUS_INSTALLED_PROVISIONAL if mode == MODE_PROVISIONAL else STATUS_CERTIFIED
            return
        incident.status = STATUS_INCIDENT_CONFIRMED
        incident.recovery_authorized = True
        incident.recovery_deadline = u64(self._now() + int(self.policies[incident.target].execution_timeout_seconds))
        release.status = STATUS_INCIDENT_CONFIRMED
        ProofPatchTarget(incident.target).emit(on="finalized").proofpatch_recover(
            incident_id, incident.release_id, incident.recovery_capsule_hash,
        )

    # ---------------------------------------------------------------------
    # Registration and immutable policy
    # ---------------------------------------------------------------------

    @gl.public.write
    def register_target(
        self,
        owner: str,
        constitution: str,
        source_authority: str,
        ci_authority: str,
        audit_authority: str,
        source_prefix: str,
        ci_prefix: str,
        audit_prefix: str,
        assurance_authority: str,
        assurance_prefix: str,
        assurance_corroboration_authority: str,
        assurance_corroboration_prefix: str,
        proofpatch_kernel_hash: str,
        current_version: str,
        current_source_url: str,
        current_code_hash: str,
        max_evidence_age_seconds: int,
        proposal_ttl_seconds: int,
        execution_timeout_seconds: int,
        assurance_observation_delay_seconds: int,
        assurance_deadline_seconds: int,
        max_manifest_bytes: int,
        max_capsule_bytes: int,
    ) -> None:
        """Register the calling target itself; caller address becomes target identity.

        The target should expose an owner-only registration method that emits this call
        to ProofPatch on finality. A contract cannot register another target address.
        """
        target = gl.message.sender_address
        owner_address = Address(owner)

        if target in self.policies:
            raise gl.vm.UserError("Target is already registered; policy is immutable")
        if owner_address == Address("0x0000000000000000000000000000000000000000"):
            raise gl.vm.UserError("Owner cannot be the zero address")

        self._check_text(constitution, "constitution", 80, MAX_CONSTITUTION_BYTES)
        self._check_text(source_authority, "source_authority", 3, 160)
        self._check_text(ci_authority, "ci_authority", 3, 160)
        self._check_text(audit_authority, "audit_authority", 3, 160)
        self._check_text(assurance_authority, "assurance_authority", 3, 160)
        self._check_text(assurance_corroboration_authority, "assurance_corroboration_authority", 3, 160)
        self._check_text(current_version, "current_version", 1, MAX_VERSION_BYTES)

        if len({source_authority, ci_authority, audit_authority, assurance_authority, assurance_corroboration_authority}) != 5:
            raise gl.vm.UserError("Publisher authorities must be distinct")
        if not self._is_authority_prefix(source_prefix):
            raise gl.vm.UserError("Invalid immutable source authority prefix")
        if not self._is_authority_prefix(ci_prefix):
            raise gl.vm.UserError("Invalid immutable CI authority prefix")
        if not self._is_authority_prefix(audit_prefix):
            raise gl.vm.UserError("Invalid immutable audit authority prefix")
        if not self._is_authority_prefix(assurance_prefix):
            raise gl.vm.UserError("Invalid immutable assurance authority prefix")
        if not self._is_authority_prefix(assurance_corroboration_prefix):
            raise gl.vm.UserError("Invalid immutable assurance corroboration prefix")
        if len({source_prefix, ci_prefix, audit_prefix, assurance_prefix, assurance_corroboration_prefix}) != 5:
            raise gl.vm.UserError("Publisher repositories must be distinct")
        if self._raw_github_owner(source_prefix).lower() == self._raw_github_owner(audit_prefix).lower():
            raise gl.vm.UserError("Independent audit authority must have a distinct GitHub publisher")
        if self._raw_github_owner(source_prefix).lower() == self._raw_github_owner(assurance_prefix).lower():
            raise gl.vm.UserError("Independent assurance authority must have a distinct GitHub publisher")
        if self._raw_github_owner(assurance_prefix).lower() == self._raw_github_owner(assurance_corroboration_prefix).lower():
            raise gl.vm.UserError("Independent assurance corroboration must have a distinct GitHub publisher")

        proofpatch_kernel_hash = proofpatch_kernel_hash.lower()
        if not self._is_hex_hash(proofpatch_kernel_hash):
            raise gl.vm.UserError("proofpatch_kernel_hash must be a lowercase SHA-256 hex digest")

        current_code_hash = current_code_hash.lower()
        if not self._is_hex_hash(current_code_hash):
            raise gl.vm.UserError("current_code_hash must be a lowercase SHA-256 hex digest")
        if not self._is_immutable_url(current_source_url, source_prefix):
            raise gl.vm.UserError("Current source must use the approved immutable commit URL")

        self._check_range(max_evidence_age_seconds, "max_evidence_age_seconds", MIN_WINDOW_SECONDS, MAX_EVIDENCE_AGE_SECONDS)
        self._check_range(proposal_ttl_seconds, "proposal_ttl_seconds", MIN_WINDOW_SECONDS, MAX_PROPOSAL_TTL_SECONDS)
        self._check_range(execution_timeout_seconds, "execution_timeout_seconds", MIN_WINDOW_SECONDS, MAX_EXECUTION_TIMEOUT_SECONDS)
        self._check_range(assurance_observation_delay_seconds, "assurance_observation_delay_seconds", MIN_WINDOW_SECONDS, MAX_EXECUTION_TIMEOUT_SECONDS)
        self._check_range(assurance_deadline_seconds, "assurance_deadline_seconds", assurance_observation_delay_seconds, MAX_EXECUTION_TIMEOUT_SECONDS)
        self._check_range(max_manifest_bytes, "max_manifest_bytes", 256, 128_000)
        self._check_range(max_capsule_bytes, "max_capsule_bytes", 1, MAX_CANDIDATE_BYTES)

        fingerprint = self._policy_fingerprint(
            target,
            owner_address,
            constitution,
            source_authority,
            ci_authority,
            audit_authority,
            source_prefix,
            ci_prefix,
            audit_prefix,
            max_evidence_age_seconds,
            proposal_ttl_seconds,
            execution_timeout_seconds,
            assurance_authority,
            assurance_prefix,
            assurance_corroboration_authority,
            assurance_corroboration_prefix,
            proofpatch_kernel_hash,
            assurance_observation_delay_seconds,
            assurance_deadline_seconds,
            max_manifest_bytes,
            max_capsule_bytes,
        )

        self.policies[target] = TargetPolicy(
            owner=owner_address,
            target=target,
            constitution=constitution,
            policy_fingerprint=fingerprint,
            source_authority=source_authority,
            ci_authority=ci_authority,
            audit_authority=audit_authority,
            source_prefix=source_prefix,
            ci_prefix=ci_prefix,
            audit_prefix=audit_prefix,
            assurance_authority=assurance_authority,
            assurance_prefix=assurance_prefix,
            assurance_corroboration_authority=assurance_corroboration_authority,
            assurance_corroboration_prefix=assurance_corroboration_prefix,
            proofpatch_kernel_hash=proofpatch_kernel_hash,
            current_version=current_version,
            current_source_url=current_source_url,
            current_code_hash=current_code_hash,
            current_release_id="",
            max_evidence_age_seconds=u64(max_evidence_age_seconds),
            proposal_ttl_seconds=u64(proposal_ttl_seconds),
            execution_timeout_seconds=u64(execution_timeout_seconds),
            assurance_observation_delay_seconds=u64(assurance_observation_delay_seconds),
            assurance_deadline_seconds=u64(assurance_deadline_seconds),
            max_manifest_bytes=u64(max_manifest_bytes),
            max_capsule_bytes=u64(max_capsule_bytes),
            active=True,
        )
        root_release_id = "root-" + current_code_hash[:16]
        root_lineage_hash = self._lineage_hash(
            target,
            "",
            root_release_id,
            "",
            current_version,
            current_code_hash,
            fingerprint,
            "",
            "",
            "",
        )
        self.releases[root_release_id] = ReleaseRecord(
            release_id=root_release_id,
            target=target,
            version=current_version,
            parent_release_id="",
            parent_code_hash="",
            source_url=current_source_url,
            code_hash=current_code_hash,
            proposal_id=u256(0),
            policy_fingerprint=fingerprint,
            evidence_set_hash="",
            assurance_manifest_hash="",
            recovery_capsule_hash="",
            installed_at=u64(self._now()),
            certified_at=u64(self._now()),
            status="REGISTERED_PARENT",
            recovered_from_release_id="",
            recovery_incident_id="",
            lineage_hash=root_lineage_hash,
        )
        self.policies[target].current_release_id = root_release_id
        self.active_proposal_by_target[target] = self._inactive_proposal()
        ProofPatchTarget(target).emit(on="finalized").proofpatch_confirm_registration(
            root_release_id,
            current_code_hash,
        )

    # ---------------------------------------------------------------------
    # Proposal lifecycle
    # ---------------------------------------------------------------------

    @gl.public.write
    def create_proposal(
        self,
        target: str,
        candidate_version: str,
        candidate_source_url: str,
        candidate_code: bytes,
        ci_evidence_url: str,
        ci_evidence_id: str,
        audit_evidence_url: str,
        audit_evidence_id: str,
        assurance_manifest: str,
        recovery_mode: str,
        recovery_release_id: str,
        recovery_version: str,
        recovery_source_url: str,
        recovery_code: bytes,
    ) -> u256:
        target_address = Address(target)
        policy = self._require_policy_owner(target_address)

        active = self.active_proposal_by_target.get(target_address, self._inactive_proposal())
        if active != self._inactive_proposal():
            raise gl.vm.UserError("Target already has an active proposal")

        self._check_text(candidate_version, "candidate_version", 1, MAX_VERSION_BYTES)
        if candidate_version == policy.current_version:
            raise gl.vm.UserError("Candidate version must differ from current version")
        if len(candidate_code) == 0 or len(candidate_code) > MAX_CANDIDATE_BYTES:
            raise gl.vm.UserError("Candidate source bytes are empty or too large")
        if not self._is_immutable_url(candidate_source_url, policy.source_prefix):
            raise gl.vm.UserError("Candidate source URL is not an approved immutable source")
        if not self._is_immutable_url(ci_evidence_url, policy.ci_prefix):
            raise gl.vm.UserError("CI evidence URL is not an approved immutable source")
        if not self._is_immutable_url(audit_evidence_url, policy.audit_prefix):
            raise gl.vm.UserError("Audit evidence URL is not an approved immutable source")
        if not self._is_immutable_url(recovery_source_url, policy.source_prefix):
            raise gl.vm.UserError("Recovery source URL is not an approved immutable source")
        if ci_evidence_id == audit_evidence_id:
            raise gl.vm.UserError("CI and audit evidence identifiers must be distinct")
        if recovery_mode not in ("EXACT_PARENT", "RECOVERY_CANDIDATE"):
            raise gl.vm.UserError("Unsupported recovery mode")
        if len(recovery_code) == 0 or len(recovery_code) > int(policy.max_capsule_bytes):
            raise gl.vm.UserError("Recovery capsule is empty or too large")
        self._check_text(recovery_version, "recovery_version", 1, MAX_VERSION_BYTES)

        candidate_hash = self._sha256_hex(candidate_code)
        if candidate_hash == policy.current_code_hash:
            raise gl.vm.UserError("Candidate code is identical to current code")
        if self.installed_candidate_hashes.get(self._installed_candidate_key(target_address, candidate_hash), False):
            raise gl.vm.UserError("This candidate hash has already been installed for this target")

        recovery_hash = self._sha256_hex(recovery_code)
        if recovery_mode == "EXACT_PARENT":
            if recovery_release_id != policy.current_release_id:
                raise gl.vm.UserError("EXACT_PARENT recovery must name the current certified release")
            if recovery_hash != policy.current_code_hash:
                raise gl.vm.UserError("EXACT_PARENT capsule bytes must match the current release")
            if recovery_version != policy.current_version:
                raise gl.vm.UserError("EXACT_PARENT capsule version must match the current release")
        else:
            if recovery_release_id != "recovery-" + recovery_hash[:16]:
                raise gl.vm.UserError("Recovery candidate release ID must bind its capsule hash")
            if recovery_hash == candidate_hash:
                raise gl.vm.UserError("Recovery candidate must differ from the candidate")

        assurance_manifest_hash, _ = self._canonical_json_hash(assurance_manifest)
        if assurance_manifest_hash in ("INVALID", "NONCANONICAL"):
            raise gl.vm.UserError("Assurance manifest must be canonical JSON")
        manifest_error = self._validate_manifest(
            assurance_manifest,
            target_address,
            candidate_hash,
            policy.policy_fingerprint,
            policy.proofpatch_kernel_hash,
            policy,
        )
        if manifest_error:
            raise gl.vm.UserError(manifest_error)

        self._reserve_evidence_id(target_address, policy.ci_authority, "ci", ci_evidence_id)
        self._reserve_evidence_id(target_address, policy.audit_authority, "audit", audit_evidence_id)

        now = self._now()
        proposal_id = u256(int(self.proposal_count) + 1)
        evidence_set_hash = self._evidence_set_hash(
            candidate_source_url,
            ci_evidence_url,
            ci_evidence_id,
            audit_evidence_url,
            audit_evidence_id,
            assurance_manifest_hash,
            recovery_hash,
        )

        self.proposals[proposal_id] = UpgradeProposal(
            proposal_id=proposal_id,
            target=target_address,
            proposer=policy.owner,
            parent_version=policy.current_version,
            parent_source_url=policy.current_source_url,
            parent_code_hash=policy.current_code_hash,
            candidate_version=candidate_version,
            candidate_source_url=candidate_source_url,
            candidate_code=candidate_code,
            candidate_code_hash=candidate_hash,
            ci_evidence_url=ci_evidence_url,
            ci_evidence_id=ci_evidence_id,
            audit_evidence_url=audit_evidence_url,
            audit_evidence_id=audit_evidence_id,
            assurance_manifest=assurance_manifest,
            assurance_manifest_hash=assurance_manifest_hash,
            recovery_mode=recovery_mode,
            recovery_release_id=recovery_release_id,
            recovery_version=recovery_version,
            recovery_source_url=recovery_source_url,
            recovery_code=recovery_code,
            recovery_code_hash=recovery_hash,
            recovery_capsule_hash=recovery_hash,
            evidence_set_hash=evidence_set_hash,
            policy_fingerprint=policy.policy_fingerprint,
            created_at=u64(now),
            expires_at=u64(now + int(policy.proposal_ttl_seconds)),
            reviewed_at=u64(0),
            execution_deadline=u64(0),
            status=STATUS_PROPOSED,
            last_review_code="",
        )
        self.proposal_count = proposal_id
        self.active_proposal_by_target[target_address] = proposal_id
        return proposal_id

    @gl.public.write
    def repair_evidence(
        self,
        proposal_id: u256,
        candidate_source_url: str,
        ci_evidence_url: str,
        ci_evidence_id: str,
        audit_evidence_url: str,
        audit_evidence_id: str,
    ) -> None:
        proposal = self._require_proposal(proposal_id)
        policy = self._require_policy_owner(proposal.target)
        if proposal.status != STATUS_REPAIR:
            raise gl.vm.UserError("Evidence can only be replaced from EVIDENCE_REPAIR_REQUIRED")
        if self._now() > int(proposal.expires_at):
            raise gl.vm.UserError("Proposal has expired")
        if not self._is_immutable_url(candidate_source_url, policy.source_prefix):
            raise gl.vm.UserError("Replacement candidate source URL is not approved and immutable")
        if not self._is_immutable_url(ci_evidence_url, policy.ci_prefix):
            raise gl.vm.UserError("Replacement CI evidence URL is not approved and immutable")
        if not self._is_immutable_url(audit_evidence_url, policy.audit_prefix):
            raise gl.vm.UserError("Replacement audit evidence URL is not approved and immutable")
        if ci_evidence_id == audit_evidence_id:
            raise gl.vm.UserError("CI and audit evidence identifiers must be distinct")

        self._reserve_evidence_id(proposal.target, policy.ci_authority, "ci", ci_evidence_id)
        self._reserve_evidence_id(proposal.target, policy.audit_authority, "audit", audit_evidence_id)

        # Critical invariant: candidate bytes/hash, target, parent, and policy fingerprint are frozen.
        proposal.candidate_source_url = candidate_source_url
        proposal.ci_evidence_url = ci_evidence_url
        proposal.ci_evidence_id = ci_evidence_id
        proposal.audit_evidence_url = audit_evidence_url
        proposal.audit_evidence_id = audit_evidence_id
        proposal.evidence_set_hash = self._evidence_set_hash(
            candidate_source_url,
            ci_evidence_url,
            ci_evidence_id,
            audit_evidence_url,
            audit_evidence_id,
            proposal.assurance_manifest_hash,
            proposal.recovery_capsule_hash,
        )
        proposal.status = STATUS_PROPOSED
        proposal.last_review_code = ""

    @gl.public.write
    def cancel_proposal(self, proposal_id: u256) -> None:
        proposal = self._require_proposal(proposal_id)
        self._require_policy_owner(proposal.target)
        if proposal.status not in (STATUS_PROPOSED, STATUS_REPAIR, STATUS_RETRY):
            raise gl.vm.UserError("Proposal can no longer be cancelled")
        proposal.status = STATUS_CANCELLED
        proposal.last_review_code = "OWNER_CANCELLED"
        self._release_active(proposal.target, proposal_id)

    @gl.public.write
    def expire_proposal(self, proposal_id: u256) -> None:
        proposal = self._require_proposal(proposal_id)
        if proposal.status not in (STATUS_PROPOSED, STATUS_REPAIR, STATUS_RETRY):
            raise gl.vm.UserError("Proposal is not expirable")
        if self._now() <= int(proposal.expires_at):
            raise gl.vm.UserError("Proposal has not expired")
        proposal.status = STATUS_EXPIRED
        proposal.last_review_code = "PROPOSAL_EXPIRED"
        self._release_active(proposal.target, proposal_id)

    # ---------------------------------------------------------------------
    # Nondeterministic evidence + semantic review
    # ---------------------------------------------------------------------

    @gl.public.write
    def review_proposal(self, proposal_id: u256) -> None:
        if gl.message.sender_address == Address(REVIEW_ENGINE):
            proposal = self._require_proposal(proposal_id)
            if proposal.status != STATUS_REVIEW_PENDING:
                raise gl.vm.UserError("Proposal is not awaiting review callback")
            raw = self._engine().view(state=StorageType.LATEST_FINAL).get_proposal_result(proposal_id)
            result = self._engine_result(raw, {"target": str(proposal.target), "proposal_id": int(proposal_id), "parent_code_hash": proposal.parent_code_hash, "candidate_code_hash": proposal.candidate_code_hash, "policy_fingerprint": proposal.policy_fingerprint, "evidence_set_hash": proposal.evidence_set_hash, "assurance_manifest_hash": proposal.assurance_manifest_hash, "recovery_capsule_hash": proposal.recovery_capsule_hash})
            proposal.reviewed_at = u64(self._now())
            self._apply_proposal_review(proposal_id, result)
            return
        proposal = self._require_proposal(proposal_id)
        if proposal.status not in (STATUS_PROPOSED, STATUS_RETRY, STATUS_REVIEW_PENDING):
            raise gl.vm.UserError("Proposal is not reviewable")
        now = self._now()
        if now > int(proposal.expires_at):
            raise gl.vm.UserError("Proposal has expired; call expire_proposal")
        policy = self.policies[proposal.target]
        if not policy.active or policy.policy_fingerprint != proposal.policy_fingerprint or policy.current_code_hash != proposal.parent_code_hash:
            raise gl.vm.UserError("Proposal policy snapshot is no longer current")
        proposal.status = STATUS_REVIEW_PENDING
        proposal.reviewed_at = u64(now)
        proposal.last_review_code = "ENGINE_PENDING"
        self._engine().emit(on="finalized").review_proposal(
            proposal_id, self._proposal_review_snapshot(proposal, policy, now),
        )


    # ---------------------------------------------------------------------
    # Finalized installation authorization + confirmation
    # ---------------------------------------------------------------------

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def is_upgrade_authorized(self, proposal_id: u256, target: str, candidate_hash: str) -> bool:
        if proposal_id not in self.proposals:
            return False
        proposal = self.proposals[proposal_id]
        if proposal.status != STATUS_QUEUED:
            return False
        if str(proposal.target).lower() != str(Address(target)).lower():
            return False
        if proposal.candidate_code_hash != candidate_hash.lower():
            return False
        if self._now() > int(proposal.execution_deadline):
            return False
        if self.active_proposal_by_target.get(proposal.target, self._inactive_proposal()) != proposal_id:
            return False
        return True

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_candidate_code(self, proposal_id: u256) -> bytes:
        if proposal_id not in self.proposals:
            raise gl.vm.UserError("Unknown proposal")
        proposal = self.proposals[proposal_id]
        if proposal.status != STATUS_QUEUED:
            raise gl.vm.UserError("Candidate is not authorized for installation")
        if self._now() > int(proposal.execution_deadline):
            raise gl.vm.UserError("Upgrade authorization expired")
        return proposal.candidate_code

    @gl.public.write
    def confirm_install(self, proposal_id: u256, candidate_hash: str) -> None:
        proposal = self._require_proposal(proposal_id)
        if gl.message.sender_address != proposal.target:
            raise gl.vm.UserError("Only the protected target may confirm installation")

        normalized_hash = candidate_hash.lower()
        if proposal.status in (
            STATUS_INSTALLED_PROVISIONAL,
            STATUS_ASSURANCE_PENDING,
            STATUS_CERTIFICATION_QUEUED,
            STATUS_CERTIFIED,
        ):
            if normalized_hash != proposal.candidate_code_hash:
                raise gl.vm.UserError("Conflicting duplicate installation confirmation")
            return
        if proposal.status != STATUS_QUEUED:
            raise gl.vm.UserError("Proposal is not awaiting installation confirmation")
        if normalized_hash != proposal.candidate_code_hash:
            raise gl.vm.UserError("Installed hash does not match approved candidate")

        target_view = ProofPatchTarget(proposal.target).view(
            state=StorageType.LATEST_FINAL
        )
        installed_proposal_id = target_view.proofpatch_installed_proposal_id()
        installed_candidate_hash = target_view.proofpatch_installed_candidate_hash()
        if installed_proposal_id != proposal_id:
            raise gl.vm.UserError("Target has not finalized this proposal")
        if installed_candidate_hash != proposal.candidate_code_hash:
            raise gl.vm.UserError(
                "Finalized target code hash does not match approved candidate"
            )
        installed_release_id = target_view.proofpatch_installed_release_id()
        if installed_release_id != self._proposal_release_id(proposal):
            raise gl.vm.UserError("Target release identity does not match proposal")
        if target_view.proofpatch_release_mode() != MODE_PROVISIONAL:
            raise gl.vm.UserError("Target did not enter PROVISIONAL mode")
        if target_view.get_proofpatch_kernel_hash() != self.policies[proposal.target].proofpatch_kernel_hash:
            raise gl.vm.UserError("Target ProofPatch kernel hash changed")

        self._record_verified_install(proposal_id, proposal, "INSTALL_VERIFIED")

    @gl.public.write
    def reconcile_install(self, proposal_id: u256) -> None:
        proposal = self._require_proposal(proposal_id)
        self._require_policy_owner(proposal.target)
        if proposal.status != STATUS_QUEUED:
            raise gl.vm.UserError("Proposal is not awaiting installation")

        target_view = ProofPatchTarget(proposal.target).view(
            state=StorageType.LATEST_FINAL
        )
        installed_proposal_id = target_view.proofpatch_installed_proposal_id()
        installed_candidate_hash = target_view.proofpatch_installed_candidate_hash()

        if installed_proposal_id != proposal_id:
            raise gl.vm.UserError("Target has not finalized this proposal")
        if installed_candidate_hash != proposal.candidate_code_hash:
            raise gl.vm.UserError(
                "Finalized target code hash does not match approved candidate"
            )
        if target_view.proofpatch_installed_release_id() != self._proposal_release_id(proposal):
            raise gl.vm.UserError("Target release identity does not match proposal")
        if target_view.proofpatch_release_mode() != MODE_PROVISIONAL:
            raise gl.vm.UserError("Target did not enter PROVISIONAL mode")

        self._record_verified_install(proposal_id, proposal, "INSTALL_RECONCILED")

    @gl.public.write
    def mark_execution_timeout(self, proposal_id: u256) -> None:
        proposal = self._require_proposal(proposal_id)
        policy = self._require_policy_owner(proposal.target)
        if proposal.status != STATUS_QUEUED:
            raise gl.vm.UserError("Proposal is not awaiting installation")
        if self._now() <= int(proposal.execution_deadline):
            raise gl.vm.UserError("Execution deadline has not passed")

        # Timeout is a recovery path, not permission to promote provisional
        # cross-contract state. Only an exact FINALIZED target attestation may
        # advance the governor to VERIFIED.
        target = ProofPatchTarget(proposal.target)

        finalized_view = target.view(state=StorageType.LATEST_FINAL)
        finalized_proposal_id = (
            finalized_view.proofpatch_installed_proposal_id()
        )
        finalized_candidate_hash = (
            finalized_view.proofpatch_installed_candidate_hash()
        )

        if (
            finalized_proposal_id == proposal_id
            and finalized_candidate_hash == proposal.candidate_code_hash
        ):
            self._record_verified_install(
                proposal_id,
                proposal,
                "INSTALL_RECONCILED_TIMEOUT",
            )
            return

        finalized_still_on_known_parent = (
            (
                finalized_proposal_id == self._inactive_proposal()
                and finalized_candidate_hash == ""
            )
            or (
                finalized_proposal_id != proposal_id
                and finalized_candidate_hash == policy.current_code_hash
            )
        )

        if not finalized_still_on_known_parent:
            raise gl.vm.UserError(
                "Finalized target installation attestation is inconsistent; "
                "active proposal remains locked"
            )

        nonfinal_view = target.view(state=StorageType.LATEST_NON_FINAL)
        nonfinal_proposal_id = (
            nonfinal_view.proofpatch_installed_proposal_id()
        )
        nonfinal_candidate_hash = (
            nonfinal_view.proofpatch_installed_candidate_hash()
        )

        if (
            nonfinal_proposal_id == proposal_id
            and nonfinal_candidate_hash == proposal.candidate_code_hash
        ):
            raise gl.vm.UserError(
                "Target installation is pending finality; "
                "active proposal remains locked"
            )

        if (
            nonfinal_proposal_id != finalized_proposal_id
            or nonfinal_candidate_hash != finalized_candidate_hash
        ):
            raise gl.vm.UserError(
                "Target non-final installation attestation is inconsistent; "
                "active proposal remains locked"
            )

        proposal.status = STATUS_EXECUTION_FAILED
        proposal.last_review_code = "EXECUTION_TIMEOUT"
        self._release_active(proposal.target, proposal_id)

    # ---------------------------------------------------------------------
    # Post-install assurance and finality-gated activation
    # ---------------------------------------------------------------------

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def is_activation_authorized(self, proposal_id: u256, release_id: str, candidate_hash: str) -> bool:
        if proposal_id not in self.proposals:
            return False
        proposal = self.proposals[proposal_id]
        return (
            proposal.status == STATUS_CERTIFICATION_QUEUED
            and release_id == self._proposal_release_id(proposal)
            and candidate_hash.lower() == proposal.candidate_code_hash
            and release_id in self.releases
            and self.releases[release_id].status == STATUS_CERTIFICATION_QUEUED
        )

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def is_registration_authorized(self, target: str, release_id: str, code_hash: str) -> bool:
        target_address = Address(target)
        if target_address not in self.policies:
            return False
        policy = self.policies[target_address]
        return (
            policy.current_release_id == release_id
            and policy.current_code_hash == code_hash.lower()
            and release_id in self.releases
            and self.releases[release_id].status == "REGISTERED_PARENT"
        )

    @gl.public.write
    def assure_release(self, proposal_id: u256, primary_url: str, primary_evidence_id: str, corroboration_url: str, corroboration_evidence_id: str) -> None:
        proposal = self._require_proposal(proposal_id)
        release_id = self._proposal_release_id(proposal)
        if gl.message.sender_address == Address(REVIEW_ENGINE):
            if proposal.status != STATUS_ASSURANCE_PENDING:
                raise gl.vm.UserError("Release is not awaiting assurance callback")
            raw = self._engine().view(state=StorageType.LATEST_FINAL).get_assurance_result(proposal_id)
            result = self._engine_result(raw, {"target": str(proposal.target), "proposal_id": int(proposal_id), "release_id": release_id, "candidate_code_hash": proposal.candidate_code_hash, "policy_fingerprint": proposal.policy_fingerprint, "assurance_manifest_hash": proposal.assurance_manifest_hash})
            self._apply_assurance_result(proposal_id, result, primary_url, primary_evidence_id, corroboration_url, corroboration_evidence_id)
            return
        if proposal.status not in (STATUS_INSTALLED_PROVISIONAL, STATUS_ASSURANCE_REPAIR, STATUS_ASSURANCE_RETRY, STATUS_ASSURANCE_PENDING):
            raise gl.vm.UserError("Release is not awaiting assurance")
        if release_id not in self.releases:
            raise gl.vm.UserError("Provisional release is missing")
        release = self.releases[release_id]
        policy = self.policies[proposal.target]
        now = self._now()
        if now < int(release.installed_at) + int(policy.assurance_observation_delay_seconds):
            raise gl.vm.UserError("Assurance observation period has not elapsed")
        if now > int(release.installed_at) + int(policy.assurance_deadline_seconds):
            raise gl.vm.UserError("Assurance deadline has passed")
        if not self._is_immutable_url(primary_url, policy.assurance_prefix) or not self._is_immutable_url(corroboration_url, policy.assurance_corroboration_prefix):
            raise gl.vm.UserError("Assurance evidence URL is not approved and immutable")
        if primary_evidence_id == corroboration_evidence_id:
            raise gl.vm.UserError("Assurance evidence identifiers must be distinct")
        self._reserve_evidence_id(proposal.target, policy.assurance_authority, "assurance_primary", primary_evidence_id)
        self._reserve_evidence_id(proposal.target, policy.assurance_corroboration_authority, "assurance_corroboration", corroboration_evidence_id)
        view = ProofPatchTarget(proposal.target).view(state=StorageType.LATEST_FINAL)
        proposal.status = STATUS_ASSURANCE_PENDING
        proposal.reviewed_at = u64(now)
        proposal.last_review_code = "ENGINE_PENDING"
        snapshot = self._assurance_snapshot(proposal, policy, release_id, primary_url, primary_evidence_id, corroboration_url, corroboration_evidence_id, now, view)
        self._engine().emit(on="finalized").assure_release(proposal_id, snapshot)


    @gl.public.write
    def confirm_activation(self, proposal_id: u256, release_id: str, candidate_hash: str) -> None:
        proposal = self._require_proposal(proposal_id)
        if gl.message.sender_address != proposal.target:
            raise gl.vm.UserError("Only the protected target may confirm activation")
        if proposal.status == STATUS_CERTIFIED:
            return
        if proposal.status != STATUS_CERTIFICATION_QUEUED:
            raise gl.vm.UserError("Proposal is not awaiting activation confirmation")
        if release_id != self._proposal_release_id(proposal) or candidate_hash.lower() != proposal.candidate_code_hash:
            raise gl.vm.UserError("Activation identity does not match proposal")
        view = ProofPatchTarget(proposal.target).view(state=StorageType.LATEST_FINAL)
        if view.proofpatch_installed_release_id() != release_id:
            raise gl.vm.UserError("Finalized target release does not match")
        if view.proofpatch_installed_candidate_hash() != proposal.candidate_code_hash:
            raise gl.vm.UserError("Finalized target hash does not match")
        if view.proofpatch_release_mode() != MODE_ACTIVE:
            raise gl.vm.UserError("Target has not finalized ACTIVE mode")
        release = self.releases[release_id]
        now = self._now()
        release.status = STATUS_CERTIFIED
        release.certified_at = u64(now)
        proposal.status = STATUS_CERTIFIED
        proposal.last_review_code = "CERTIFICATION_VERIFIED"
        policy = self.policies[proposal.target]
        policy.current_version = proposal.candidate_version
        policy.current_source_url = proposal.candidate_source_url
        policy.current_code_hash = proposal.candidate_code_hash
        policy.current_release_id = release_id
        self._release_active(proposal.target, proposal_id)

    @gl.public.write
    def expire_provisional_release(self, release_id: str) -> None:
        if release_id not in self.releases:
            raise gl.vm.UserError("Unknown release")
        release = self.releases[release_id]
        if release.status not in (STATUS_INSTALLED_PROVISIONAL, STATUS_ASSURANCE_PENDING, STATUS_ASSURANCE_REPAIR, STATUS_ASSURANCE_RETRY):
            raise gl.vm.UserError("Release is not provisionally installed")
        policy = self.policies[release.target]
        if self._now() <= int(release.installed_at) + int(policy.assurance_deadline_seconds):
            raise gl.vm.UserError("Assurance deadline has not passed")
        incident_id = "timeout-" + release_id
        if incident_id not in self.incidents:
            proposal = self.proposals[release.proposal_id]
            self.incidents[incident_id] = IncidentRecord(
                incident_id=incident_id,
                target=release.target,
                release_id=release_id,
                installed_code_hash=release.code_hash,
                incident_type="ASSURANCE_TIMEOUT",
                primary_url="",
                primary_evidence_id="",
                corroboration_url="",
                corroboration_evidence_id="",
                policy_fingerprint=release.policy_fingerprint,
                assurance_manifest_hash=release.assurance_manifest_hash,
                recovery_capsule_hash=release.recovery_capsule_hash,
                opened_at=u64(self._now()),
                expires_at=u64(self._now() + int(policy.proposal_ttl_seconds)),
                reviewed_at=u64(0),
                recovery_deadline=u64(0),
                status=STATUS_INCIDENT_OPEN,
                last_review_code="ASSURANCE_DEADLINE_EXPIRED",
                recovery_authorized=False,
            )
            proposal.status = STATUS_INCIDENT_OPEN
        release.status = STATUS_INCIDENT_OPEN

    @gl.public.write
    def open_incident(
        self,
        target: str,
        release_id: str,
        incident_type: str,
        primary_url: str,
        primary_evidence_id: str,
        corroboration_url: str,
        corroboration_evidence_id: str,
    ) -> str:
        target_address = Address(target)
        if target_address not in self.policies or release_id not in self.releases:
            raise gl.vm.UserError("Unknown target or release")
        release = self.releases[release_id]
        if release.target != target_address:
            raise gl.vm.UserError("Incident release belongs to another target")
        if incident_type not in (
            "STATE_INVARIANT_VIOLATION", "AUTHORIZATION_REGRESSION", "UPGRADE_BYPASS",
            "CONSENSUS_BINDING_REGRESSION", "EVIDENCE_TRUST_REGRESSION", "FINALITY_REGRESSION",
            "LIVENESS_REGRESSION", "HIDDEN_VALUE_TRANSFER", "KERNEL_INTEGRITY_FAILURE",
            "REQUIRED_INTERFACE_FAILURE", "OTHER_CONSTITUTIONAL_BREACH",
        ):
            raise gl.vm.UserError("Unsupported incident type")
        policy = self.policies[target_address]
        if not self._is_immutable_url(primary_url, policy.audit_prefix):
            raise gl.vm.UserError("Incident primary evidence URL is not approved and immutable")
        if not self._is_immutable_url(corroboration_url, policy.assurance_corroboration_prefix):
            raise gl.vm.UserError("Incident corroboration URL is not approved and immutable")
        if primary_evidence_id == corroboration_evidence_id:
            raise gl.vm.UserError("Incident evidence identifiers must be distinct")
        self._reserve_evidence_id(target_address, policy.audit_authority, "incident_primary", primary_evidence_id)
        self._reserve_evidence_id(
            target_address,
            policy.assurance_corroboration_authority,
            "incident_corroboration",
            corroboration_evidence_id,
        )
        target_view = ProofPatchTarget(target_address).view(state=StorageType.LATEST_FINAL)
        if target_view.proofpatch_installed_release_id() != release_id:
            raise gl.vm.UserError("Incident release is not the target's finalized release")
        if target_view.proofpatch_release_mode() not in (MODE_ACTIVE, MODE_PROVISIONAL, MODE_RECOVERED):
            raise gl.vm.UserError("Incident target is not in a challengeable release mode")
        if release.recovery_capsule_hash == "":
            raise gl.vm.UserError("Release has no precommitted recovery capsule")
        if release.status not in (
            STATUS_CERTIFIED,
            STATUS_INSTALLED_PROVISIONAL,
            STATUS_ASSURANCE_PENDING,
            STATUS_ASSURANCE_REPAIR,
            STATUS_ASSURANCE_RETRY,
            STATUS_INCIDENT_OPEN,
        ):
            raise gl.vm.UserError("Release is not challengeable in its current lifecycle state")
        incident_id = "incident-" + str(self._now()) + "-" + primary_evidence_id
        if incident_id in self.incidents:
            raise gl.vm.UserError("Incident identifier already exists")
        incident_replay_key = self._hash_text_parts([str(target_address), release_id, primary_evidence_id, corroboration_evidence_id])
        if self.used_incident_ids.get(incident_replay_key, False):
            raise gl.vm.UserError("Incident evidence has already been used for this release")
        self.used_incident_ids[incident_replay_key] = True
        self.incidents[incident_id] = IncidentRecord(
            incident_id=incident_id,
            target=target_address,
            release_id=release_id,
            installed_code_hash=release.code_hash,
            incident_type=incident_type,
            primary_url=primary_url,
            primary_evidence_id=primary_evidence_id,
            corroboration_url=corroboration_url,
            corroboration_evidence_id=corroboration_evidence_id,
            policy_fingerprint=release.policy_fingerprint,
            assurance_manifest_hash=release.assurance_manifest_hash,
            recovery_capsule_hash=release.recovery_capsule_hash,
            opened_at=u64(self._now()),
            expires_at=u64(self._now() + int(policy.proposal_ttl_seconds)),
            reviewed_at=u64(0),
            recovery_deadline=u64(0),
            status=STATUS_INCIDENT_OPEN,
            last_review_code="",
            recovery_authorized=False,
        )
        release.status = STATUS_INCIDENT_OPEN
        return incident_id

    @gl.public.write
    def review_incident(self, incident_id: str) -> None:
        if incident_id not in self.incidents:
            raise gl.vm.UserError("Unknown incident")
        incident = self.incidents[incident_id]
        if gl.message.sender_address == Address(REVIEW_ENGINE):
            if incident.status != STATUS_INCIDENT_REVIEW_PENDING:
                raise gl.vm.UserError("Incident is not awaiting review callback")
            raw = self._engine().view(state=StorageType.LATEST_FINAL).get_incident_result(incident_id)
            result = self._engine_result(raw, {"incident_id": incident_id, "target": str(incident.target), "release_id": incident.release_id, "installed_code_hash": incident.installed_code_hash, "policy_fingerprint": incident.policy_fingerprint, "recovery_capsule_hash": incident.recovery_capsule_hash})
            self._apply_incident_result(incident_id, result)
            return
        if incident.status not in (STATUS_INCIDENT_OPEN, STATUS_INCIDENT_RETRY, STATUS_INCIDENT_REVIEW_PENDING):
            raise gl.vm.UserError("Incident is not reviewable")
        if self._now() > int(incident.expires_at):
            raise gl.vm.UserError("Incident review window has expired")
        policy = self.policies[incident.target]
        release = self.releases[incident.release_id]
        proposal = self.proposals[release.proposal_id]
        now = self._now()
        incident.status = STATUS_INCIDENT_REVIEW_PENDING
        incident.reviewed_at = u64(now)
        incident.last_review_code = "ENGINE_PENDING"
        self._engine().emit(on="finalized").review_incident(
            incident_id, self._incident_snapshot(incident, policy, release, proposal, now),
        )


    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def is_recovery_authorized(self, incident_id: str, release_id: str, recovery_hash: str) -> bool:
        if incident_id not in self.incidents or release_id not in self.releases:
            return False
        incident = self.incidents[incident_id]
        return (
            incident.status in (STATUS_INCIDENT_CONFIRMED, STATUS_RECOVERY_QUEUED, STATUS_RECOVERY_RETRY)
            and incident.recovery_authorized
            and incident.release_id == release_id
            and incident.recovery_capsule_hash == recovery_hash.lower()
        )

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_recovery_release_id(self, incident_id: str) -> str:
        if incident_id not in self.incidents:
            return ""
        incident = self.incidents[incident_id]
        if incident.release_id not in self.releases:
            return ""
        release = self.releases[incident.release_id]
        if release.proposal_id not in self.proposals:
            return ""
        return self._recovery_release_id(self.proposals[release.proposal_id])

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_recovery_code(self, incident_id: str) -> bytes:
        if incident_id not in self.incidents:
            raise gl.vm.UserError("Unknown incident")
        incident = self.incidents[incident_id]
        release = self.releases[incident.release_id]
        proposal = self.proposals[release.proposal_id]
        if incident.status not in (STATUS_INCIDENT_CONFIRMED, STATUS_RECOVERY_QUEUED, STATUS_RECOVERY_RETRY):
            raise gl.vm.UserError("Recovery is not authorized")
        return proposal.recovery_code

    def _complete_recovery(self, incident_id: str, release_id: str, recovery_hash: str) -> None:
        if incident_id not in self.incidents:
            raise gl.vm.UserError("Unknown incident")
        incident = self.incidents[incident_id]
        if incident.status == STATUS_RECOVERED:
            return
        if incident.status not in (STATUS_INCIDENT_CONFIRMED, STATUS_RECOVERY_QUEUED, STATUS_RECOVERY_RETRY) or release_id != incident.release_id:
            raise gl.vm.UserError("Incident is not awaiting recovery confirmation")
        if recovery_hash.lower() != incident.recovery_capsule_hash:
            raise gl.vm.UserError("Recovery hash does not match precommitted capsule")
        view = ProofPatchTarget(incident.target).view(state=StorageType.LATEST_FINAL)
        proposal = self.proposals[self.releases[release_id].proposal_id]
        expected_recovery_release_id = self._recovery_release_id(proposal)
        if view.proofpatch_installed_release_id() != expected_recovery_release_id:
            raise gl.vm.UserError("Finalized target recovery release does not match")
        if view.proofpatch_installed_candidate_hash() != recovery_hash.lower():
            raise gl.vm.UserError("Finalized target recovery hash does not match")
        if view.proofpatch_release_mode() != MODE_RECOVERED:
            raise gl.vm.UserError("Target has not finalized RECOVERED mode")
        incident.status = STATUS_RECOVERED
        incident.last_review_code = "RECOVERY_VERIFIED"
        self.releases[release_id].status = STATUS_RECOVERED
        self.releases[release_id].recovery_incident_id = incident_id
        policy = self.policies[incident.target]
        proposal = self.proposals[self.releases[release_id].proposal_id]
        recovery_release_id = expected_recovery_release_id
        if proposal.recovery_mode == "RECOVERY_CANDIDATE":
            if recovery_release_id in self.releases:
                existing_recovery = self.releases[recovery_release_id]
                if existing_recovery.code_hash != recovery_hash.lower():
                    raise gl.vm.UserError("Conflicting recovery release identity")
            else:
                affected_release = self.releases[release_id]
                recovery_lineage_hash = self._lineage_hash(
                    incident.target,
                    affected_release.lineage_hash,
                    recovery_release_id,
                    release_id,
                    proposal.recovery_version,
                    recovery_hash.lower(),
                    proposal.policy_fingerprint,
                    proposal.evidence_set_hash,
                    proposal.assurance_manifest_hash,
                    proposal.recovery_capsule_hash,
                )
                self.releases[recovery_release_id] = ReleaseRecord(
                    release_id=recovery_release_id,
                    target=incident.target,
                    version=proposal.recovery_version,
                    parent_release_id=release_id,
                    parent_code_hash=incident.installed_code_hash,
                    source_url=proposal.recovery_source_url,
                    code_hash=recovery_hash.lower(),
                    proposal_id=proposal.proposal_id,
                    policy_fingerprint=proposal.policy_fingerprint,
                    evidence_set_hash=proposal.evidence_set_hash,
                    assurance_manifest_hash=proposal.assurance_manifest_hash,
                    recovery_capsule_hash=proposal.recovery_capsule_hash,
                    installed_at=u64(self._now()),
                    certified_at=u64(self._now()),
                    status=STATUS_RECOVERED,
                    recovered_from_release_id=release_id,
                    recovery_incident_id=incident_id,
                    lineage_hash=recovery_lineage_hash,
                )
        elif recovery_release_id not in self.releases:
            raise gl.vm.UserError("Exact-parent recovery release is missing")
        policy.current_version = proposal.recovery_version
        policy.current_source_url = proposal.recovery_source_url
        policy.current_code_hash = recovery_hash.lower()
        policy.current_release_id = recovery_release_id
        self._release_active(incident.target, proposal.proposal_id)

    @gl.public.write
    def confirm_recovery(self, incident_id: str, release_id: str, recovery_hash: str) -> None:
        if incident_id not in self.incidents:
            raise gl.vm.UserError("Unknown incident")
        incident = self.incidents[incident_id]
        if gl.message.sender_address != incident.target:
            raise gl.vm.UserError("Only the protected target may confirm recovery")
        if incident.status != STATUS_RECOVERED and self._now() > int(incident.recovery_deadline):
            raise gl.vm.UserError("Recovery confirmation deadline has passed")
        self._complete_recovery(incident_id, release_id, recovery_hash)

    @gl.public.write
    def reconcile_recovery(self, incident_id: str) -> None:
        if incident_id not in self.incidents:
            raise gl.vm.UserError("Unknown incident")
        incident = self.incidents[incident_id]
        if incident.status not in (STATUS_INCIDENT_CONFIRMED, STATUS_RECOVERY_QUEUED, STATUS_RECOVERY_RETRY):
            raise gl.vm.UserError("Incident is not awaiting recovery reconciliation")
        self._complete_recovery(incident_id, incident.release_id, incident.recovery_capsule_hash)

    @gl.public.write
    def expire_recovery(self, incident_id: str) -> None:
        if incident_id not in self.incidents:
            raise gl.vm.UserError("Unknown incident")
        incident = self.incidents[incident_id]
        if incident.status not in (STATUS_INCIDENT_CONFIRMED, STATUS_RECOVERY_QUEUED):
            raise gl.vm.UserError("Incident is not awaiting recovery")
        if self._now() <= int(incident.recovery_deadline):
            raise gl.vm.UserError("Recovery deadline has not passed")
        view = ProofPatchTarget(incident.target).view(state=StorageType.LATEST_FINAL)
        if view.proofpatch_release_mode() == MODE_RECOVERED:
            self._complete_recovery(incident_id, incident.release_id, incident.recovery_capsule_hash)
            return
        incident.status = STATUS_RECOVERY_RETRY
        self.releases[incident.release_id].status = STATUS_RECOVERY_RETRY

    @gl.public.write
    def retry_recovery(self, incident_id: str) -> None:
        if incident_id not in self.incidents:
            raise gl.vm.UserError("Unknown incident")
        incident = self.incidents[incident_id]
        if incident.status != STATUS_RECOVERY_RETRY:
            raise gl.vm.UserError("Recovery is not retryable")
        policy = self.policies[incident.target]
        now = self._now()
        incident.status = STATUS_INCIDENT_CONFIRMED
        incident.recovery_deadline = u64(now + int(policy.execution_timeout_seconds))
        self.releases[incident.release_id].status = STATUS_INCIDENT_CONFIRMED
        ProofPatchTarget(incident.target).emit(on="finalized").proofpatch_recover(
            incident_id,
            incident.release_id,
            incident.recovery_capsule_hash,
        )

    # ---------------------------------------------------------------------
    # Reviewer-friendly read API
    # ---------------------------------------------------------------------

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_proposal_count(self) -> u256:
        return self.proposal_count

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_proposal_status(self, proposal_id: u256) -> str:
        if proposal_id not in self.proposals:
            return "UNKNOWN"
        return self.proposals[proposal_id].status

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_candidate_hash(self, proposal_id: u256) -> str:
        if proposal_id not in self.proposals:
            return ""
        return self.proposals[proposal_id].candidate_code_hash

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_proposal_release_id(self, proposal_id: u256) -> str:
        if proposal_id not in self.proposals:
            return ""
        return self._proposal_release_id(self.proposals[proposal_id])

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_evidence_set_hash(self, proposal_id: u256) -> str:
        if proposal_id not in self.proposals:
            return ""
        return self.proposals[proposal_id].evidence_set_hash

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_policy_fingerprint(self, target: str) -> str:
        target_address = Address(target)
        if target_address not in self.policies:
            return ""
        return self.policies[target_address].policy_fingerprint

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_policy_kernel_hash(self, target: str) -> str:
        target_address = Address(target)
        if target_address not in self.policies:
            return ""
        return self.policies[target_address].proofpatch_kernel_hash

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_current_code_hash(self, target: str) -> str:
        target_address = Address(target)
        if target_address not in self.policies:
            return ""
        return self.policies[target_address].current_code_hash

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_current_version(self, target: str) -> str:
        target_address = Address(target)
        if target_address not in self.policies:
            return ""
        return self.policies[target_address].current_version

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_current_release_id(self, target: str) -> str:
        target_address = Address(target)
        if target_address not in self.policies:
            return ""
        return self.policies[target_address].current_release_id

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_active_proposal(self, target: str) -> u256:
        target_address = Address(target)
        return self.active_proposal_by_target.get(target_address, self._inactive_proposal())

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_proposal_summary(self, proposal_id: u256) -> str:
        if proposal_id not in self.proposals:
            return json.dumps({"status": "UNKNOWN"}, separators=(",", ":"))
        proposal = self.proposals[proposal_id]
        return json.dumps({
            "proposal_id": int(proposal.proposal_id),
            "target": str(proposal.target),
            "parent_version": proposal.parent_version,
            "parent_code_hash": proposal.parent_code_hash,
            "candidate_version": proposal.candidate_version,
            "candidate_code_hash": proposal.candidate_code_hash,
            "policy_fingerprint": proposal.policy_fingerprint,
            "evidence_set_hash": proposal.evidence_set_hash,
            "assurance_manifest_hash": proposal.assurance_manifest_hash,
            "recovery_mode": proposal.recovery_mode,
            "recovery_release_id": proposal.recovery_release_id,
            "recovery_capsule_hash": proposal.recovery_capsule_hash,
            "release_id": self._proposal_release_id(proposal),
            "status": proposal.status,
            "last_review_code": proposal.last_review_code,
            "created_at": int(proposal.created_at),
            "expires_at": int(proposal.expires_at),
            "reviewed_at": int(proposal.reviewed_at),
            "execution_deadline": int(proposal.execution_deadline),
        }, separators=(",", ":"))

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_release_summary(self, release_id: str) -> str:
        if release_id not in self.releases:
            return json.dumps({"status": "UNKNOWN"}, separators=(",", ":"))
        release = self.releases[release_id]
        return json.dumps({
            "release_id": release.release_id,
            "target": str(release.target),
            "version": release.version,
            "parent_release_id": release.parent_release_id,
            "parent_code_hash": release.parent_code_hash,
            "code_hash": release.code_hash,
            "proposal_id": int(release.proposal_id),
            "policy_fingerprint": release.policy_fingerprint,
            "evidence_set_hash": release.evidence_set_hash,
            "assurance_manifest_hash": release.assurance_manifest_hash,
            "recovery_capsule_hash": release.recovery_capsule_hash,
            "installed_at": int(release.installed_at),
            "certified_at": int(release.certified_at),
            "status": release.status,
            "recovered_from_release_id": release.recovered_from_release_id,
            "recovery_incident_id": release.recovery_incident_id,
            "lineage_hash": release.lineage_hash,
        }, separators=(",", ":"))

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_incident_summary(self, incident_id: str) -> str:
        if incident_id not in self.incidents:
            return json.dumps({"status": "UNKNOWN"}, separators=(",", ":"))
        incident = self.incidents[incident_id]
        return json.dumps({
            "incident_id": incident.incident_id,
            "target": str(incident.target),
            "release_id": incident.release_id,
            "installed_code_hash": incident.installed_code_hash,
            "incident_type": incident.incident_type,
            "policy_fingerprint": incident.policy_fingerprint,
            "recovery_capsule_hash": incident.recovery_capsule_hash,
            "opened_at": int(incident.opened_at),
            "expires_at": int(incident.expires_at),
            "reviewed_at": int(incident.reviewed_at),
            "recovery_deadline": int(incident.recovery_deadline),
            "status": incident.status,
            "last_review_code": incident.last_review_code,
            "recovery_authorized": incident.recovery_authorized,
        }, separators=(",", ":"))
