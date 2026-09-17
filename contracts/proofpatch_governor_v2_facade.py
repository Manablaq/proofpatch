# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
from dataclasses import dataclass
from datetime import datetime
from genlayer.py.public_abi import StorageType
import hashlib
import json
import typing
SCHEMA_VERSION = 'proofpatch-v2'
EVIDENCE_SCHEMA = 'proofpatch-evidence-v2'
ASSURANCE_SCHEMA = 'proofpatch-assurance-v1'
INCIDENT_SCHEMA = 'proofpatch-incident-v1'
MODE_BOOTSTRAP = 'BOOTSTRAP'
MODE_ACTIVE = 'ACTIVE'
MODE_PROVISIONAL = 'PROVISIONAL'
MODE_RECOVERY_PENDING = 'RECOVERY_PENDING'
MODE_RECOVERED = 'RECOVERED'
STATUS_PROPOSED = 'PROPOSED'
STATUS_REPAIR = 'EVIDENCE_REPAIR_REQUIRED'
STATUS_RETRY = 'REVIEW_RETRY_REQUIRED'
STATUS_REJECTED = 'REJECTED'
STATUS_QUEUED = 'UPGRADE_QUEUED'
STATUS_INSTALLED_PROVISIONAL = 'INSTALLED_PROVISIONAL'
STATUS_ASSURANCE_PENDING = 'ASSURANCE_PENDING'
STATUS_ASSURANCE_REPAIR = 'ASSURANCE_REPAIR_REQUIRED'
STATUS_ASSURANCE_RETRY = 'ASSURANCE_RETRY_REQUIRED'
STATUS_CERTIFICATION_QUEUED = 'CERTIFICATION_QUEUED'
STATUS_CERTIFIED = 'CERTIFIED'
STATUS_VERIFIED = STATUS_CERTIFIED
STATUS_EXPIRED = 'EXPIRED'
STATUS_CANCELLED = 'CANCELLED'
STATUS_EXECUTION_FAILED = 'EXECUTION_FAILED'
STATUS_INCIDENT_OPEN = 'INCIDENT_OPEN'
STATUS_INCIDENT_REPAIR = 'INCIDENT_REPAIR_REQUIRED'
STATUS_INCIDENT_RETRY = 'INCIDENT_RETRY_REQUIRED'
STATUS_INCIDENT_CONFIRMED = 'INCIDENT_CONFIRMED'
STATUS_INCIDENT_DISMISSED = 'INCIDENT_DISMISSED'
STATUS_RECOVERY_QUEUED = 'RECOVERY_QUEUED'
STATUS_RECOVERY_RETRY = 'RECOVERY_RETRY_REQUIRED'
STATUS_RECOVERED = 'RECOVERED'
REVIEW_REPAIR = 'REPAIR'
REVIEW_RETRY = 'RETRY'
REVIEW_DECISION = 'DECISION'
DECISION_APPROVE = 'APPROVE'
DECISION_REJECT = 'REJECT'
ASSURANCE_KEYS = ('installed_hash_matches', 'kernel_binding_matches', 'governor_binding_matches', 'critical_state_preserved', 'interface_requirements_hold', 'canary_requirements_hold', 'runtime_evidence_valid', 'no_post_install_security_regression', 'recovery_path_live', 'assurance_manifest_satisfied')
INCIDENT_KEYS = ('incident_evidence_authentic', 'incident_affects_exact_release', 'incident_reproducible_or_sufficiently_established', 'constitution_breached', 'continued_operation_unsafe', 'recovery_capsule_applicable', 'recovery_safer_than_continuation', 'recovery_path_preserves_rights', 'recovery_path_preserves_governance')
MAX_CONSTITUTION_BYTES = 16000
MAX_CANDIDATE_BYTES = 512000
MAX_URL_BYTES = 1024
MAX_ID_BYTES = 160
MAX_VERSION_BYTES = 96
MAX_EVIDENCE_AGE_SECONDS = 30 * 24 * 60 * 60
MAX_PROPOSAL_TTL_SECONDS = 14 * 24 * 60 * 60
MAX_EXECUTION_TIMEOUT_SECONDS = 7 * 24 * 60 * 60
MIN_WINDOW_SECONDS = 60
SEMANTIC_KEYS = ('storage_layout_compatible', 'forward_storage_compatible', 'reverse_storage_compatible_or_recovery_safe', 'user_rights_preserved', 'no_privilege_escalation', 'proofpatch_kernel_preserved', 'upgrade_authority_preserved', 'provisional_guard_preserved', 'consensus_binding_preserved', 'evidence_trust_preserved', 'finality_safety_preserved', 'liveness_preserved', 'no_hidden_value_transfer', 'assurance_manifest_sufficient', 'assurance_path_preserved', 'recovery_capsule_valid', 'recovery_path_preserved', 'constitution_satisfied')
REVIEW_ENGINE = '0x827798efCcE0a74a8dEc44bBA7A73445786A1c4C'
STATUS_REVIEW_PENDING = 'REVIEW_PENDING'
STATUS_INCIDENT_REVIEW_PENDING = 'INCIDENT_REVIEW_PENDING'

@gl.contract_interface
class ProofPatchReviewEngine:

    class View:

        def get_proposal_result(self, proposal_id: u256) -> str:
            ...

        def get_assurance_result(self, proposal_id: u256) -> str:
            ...

        def get_incident_result(self, incident_id: str) -> str:
            ...

    class Write:

        def review_proposal(self, proposal_id: u256, snapshot: str) -> None:
            ...

        def assure_release(self, proposal_id: u256, snapshot: str) -> None:
            ...

        def review_incident(self, incident_id: str, snapshot: str) -> None:
            ...

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

        def proofpatch_installed_proposal_id(self) -> u256:
            ...

        def proofpatch_installed_candidate_hash(self) -> str:
            ...

        def proofpatch_installed_release_id(self) -> str:
            ...

        def proofpatch_release_mode(self) -> str:
            ...

        def get_proofpatch_kernel_hash(self) -> str:
            ...

    class Write:

        def proofpatch_confirm_registration(self, release_id: str, code_hash: str) -> None:
            ...

        def proofpatch_upgrade(self, proposal_id: u256, candidate_hash: str) -> None:
            ...

        def proofpatch_activate(self, release_id: str, candidate_hash: str) -> None:
            ...

        def proofpatch_recover(self, incident_id: str, release_id: str, recovery_hash: str) -> None:
            ...
POLICY_ENGINE = '0x2e0D1B38BA35186188c9D543dE63989A1BF922a5'

@gl.contract_interface
class ProofPatchPolicyEngine:

    class Write:

        def execute(self, operation: str, request: str) -> None:
            ...

@gl.contract_interface
class ProofPatchGovernorCallback:

    class Write:

        def apply_policy_result(self, operation: str, payload: str) -> None:
            ...

class ProofPatchGovernorV2(gl.Contract):
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

    def _now(self) -> int:
        raw = str(gl.message_raw['datetime'])
        return int(datetime.fromisoformat(raw.replace('Z', '+00:00')).timestamp())

    def _sha256_hex(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def _canonical_json_hash(self, value: str) -> tuple[str, object]:
        try:
            parsed = json.loads(value)
            canonical = json.dumps(parsed, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
            if canonical != value:
                return ('NONCANONICAL', parsed)
            return (self._sha256_hex(canonical.encode('utf-8')), parsed)
        except Exception:
            return ('INVALID', None)

    def _validate_manifest(self, manifest: str, expected_target: Address, expected_candidate_hash: str, expected_policy_hash: str, expected_kernel_hash: str, policy: TargetPolicy) -> str:
        if len(manifest.encode('utf-8')) > int(policy.max_manifest_bytes):
            return 'MANIFEST_TOO_LARGE'
        (manifest_hash, parsed) = self._canonical_json_hash(manifest)
        if manifest_hash in ('INVALID', 'NONCANONICAL') or not isinstance(parsed, dict):
            return 'MANIFEST_NOT_CANONICAL_JSON'
        obj = typing.cast(dict[object, object], parsed)
        required = ('schema', 'target', 'candidate_sha256', 'policy_fingerprint', 'expected_kernel_hash', 'expected_release_version', 'observation_delay_seconds', 'assurance_deadline_seconds', 'ci_assurance_evidence_required', 'independent_assurance_required')
        for key in required:
            if key not in obj:
                return 'MANIFEST_MISSING_' + key.upper()
        if obj.get('schema') != ASSURANCE_SCHEMA:
            return 'MANIFEST_SCHEMA_MISMATCH'
        target_value = obj.get('target')
        if not isinstance(target_value, str) or target_value.lower() != str(expected_target).lower():
            return 'MANIFEST_TARGET_MISMATCH'
        if obj.get('candidate_sha256') != expected_candidate_hash:
            return 'MANIFEST_CANDIDATE_HASH_MISMATCH'
        if obj.get('policy_fingerprint') != expected_policy_hash:
            return 'MANIFEST_POLICY_MISMATCH'
        if obj.get('expected_kernel_hash') != expected_kernel_hash:
            return 'MANIFEST_KERNEL_MISMATCH'
        if type(obj.get('observation_delay_seconds')) is not int:
            return 'MANIFEST_OBSERVATION_DELAY_INVALID'
        if type(obj.get('assurance_deadline_seconds')) is not int:
            return 'MANIFEST_ASSURANCE_DEADLINE_INVALID'
        if obj.get('observation_delay_seconds') != int(policy.assurance_observation_delay_seconds):
            return 'MANIFEST_OBSERVATION_DELAY_MISMATCH'
        if obj.get('assurance_deadline_seconds') != int(policy.assurance_deadline_seconds):
            return 'MANIFEST_ASSURANCE_DEADLINE_MISMATCH'
        if obj.get('ci_assurance_evidence_required') is not True:
            return 'MANIFEST_CI_ASSURANCE_REQUIRED'
        if obj.get('independent_assurance_required') is not True:
            return 'MANIFEST_INDEPENDENT_ASSURANCE_REQUIRED'
        for list_key in ('required_state_checks', 'required_readback_checks', 'required_canary_checks'):
            value_raw = obj.get(list_key, [])
            if not isinstance(value_raw, list):
                return 'MANIFEST_' + list_key.upper() + '_INVALID'
            value = typing.cast(list[object], value_raw)
            if len(value) > 32:
                return 'MANIFEST_' + list_key.upper() + '_INVALID'
            for item in value:
                if not isinstance(item, str) or len(item.encode('utf-8')) > 160:
                    return 'MANIFEST_' + list_key.upper() + '_ITEM_INVALID'
        return ''

    def _inactive_proposal(self) -> u256:
        return u256(0)

    def _require_proposal(self, proposal_id: u256) -> UpgradeProposal:
        if proposal_id not in self.proposals:
            raise gl.vm.UserError('Unknown proposal')
        return self.proposals[proposal_id]

    def _release_active(self, target: Address, proposal_id: u256) -> None:
        active = self.active_proposal_by_target.get(target, self._inactive_proposal())
        if active == proposal_id:
            self.active_proposal_by_target[target] = self._inactive_proposal()

    def _proposal_release_id(self, proposal: UpgradeProposal) -> str:
        return 'release-' + str(proposal.proposal_id) + '-' + proposal.candidate_code_hash[:16]

    def _recovery_release_id(self, proposal: UpgradeProposal) -> str:
        if proposal.recovery_mode == 'EXACT_PARENT':
            return proposal.recovery_release_id
        return proposal.recovery_release_id

    def _engine(self):
        return ProofPatchReviewEngine(Address(REVIEW_ENGINE))

    def _engine_result(self, raw: str, expected: dict[str, object]) -> dict[object, object]:
        try:
            value = json.loads(raw)
        except Exception:
            raise gl.vm.UserError('Review engine returned invalid JSON')
        if not isinstance(value, dict):
            raise gl.vm.UserError('Review engine returned an invalid result')
        for (key, expected_value) in expected.items():
            if value.get(key) != expected_value:
                raise gl.vm.UserError('Review engine result binding mismatch')
        return value

    def _proposal_review_snapshot(self, proposal: UpgradeProposal, policy: TargetPolicy, now: int) -> str:
        manifest_error = ''
        return json.dumps({'proposal_id': int(proposal.proposal_id), 'target': str(proposal.target), 'parent_version': proposal.parent_version, 'parent_source_url': proposal.parent_source_url, 'parent_code_hash': proposal.parent_code_hash, 'candidate_version': proposal.candidate_version, 'candidate_source_url': proposal.candidate_source_url, 'candidate_code_hash': proposal.candidate_code_hash, 'candidate_code_hex': proposal.candidate_code.hex(), 'ci_evidence_url': proposal.ci_evidence_url, 'ci_evidence_id': proposal.ci_evidence_id, 'audit_evidence_url': proposal.audit_evidence_url, 'audit_evidence_id': proposal.audit_evidence_id, 'assurance_manifest': proposal.assurance_manifest, 'assurance_manifest_hash': proposal.assurance_manifest_hash, 'recovery_mode': proposal.recovery_mode, 'recovery_release_id': proposal.recovery_release_id, 'recovery_version': proposal.recovery_version, 'recovery_source_url': proposal.recovery_source_url, 'recovery_code_hash': proposal.recovery_code_hash, 'recovery_capsule_hash': proposal.recovery_capsule_hash, 'recovery_code_hex': proposal.recovery_code.hex(), 'evidence_set_hash': proposal.evidence_set_hash, 'policy_fingerprint': proposal.policy_fingerprint, 'constitution': policy.constitution, 'kernel_hash': policy.proofpatch_kernel_hash, 'ci_authority': policy.ci_authority, 'audit_authority': policy.audit_authority, 'max_evidence_age_seconds': int(policy.max_evidence_age_seconds), 'max_manifest_bytes': int(policy.max_manifest_bytes), 'observation_delay_seconds': int(policy.assurance_observation_delay_seconds), 'assurance_deadline_seconds': int(policy.assurance_deadline_seconds), 'review_now': now, 'manifest_error': manifest_error}, sort_keys=True, separators=(',', ':'))

    def _apply_proposal_review(self, proposal_id: u256, result: dict[object, object]) -> None:
        proposal = self._require_proposal(proposal_id)
        policy = self.policies[proposal.target]
        if result['kind'] == REVIEW_REPAIR:
            proposal.status = STATUS_REPAIR
            proposal.last_review_code = str(result.get('error_code', ''))
            return
        if result['kind'] == REVIEW_RETRY:
            proposal.status = STATUS_RETRY
            proposal.last_review_code = str(result.get('error_code', ''))
            return
        if result['kind'] != REVIEW_DECISION:
            raise gl.vm.UserError('Unexpected review result')
        proposal.last_review_code = str(result.get('error_code', ''))
        if result['decision'] == DECISION_REJECT:
            proposal.status = STATUS_REJECTED
            self._release_active(proposal.target, proposal_id)
            return
        if result['decision'] != DECISION_APPROVE:
            raise gl.vm.UserError('Unexpected decision')
        proposal.status = STATUS_QUEUED
        proposal.execution_deadline = u64(self._now() + int(policy.execution_timeout_seconds))
        ProofPatchTarget(proposal.target).emit(on='finalized').proofpatch_upgrade(proposal_id, proposal.candidate_code_hash)

    def _incident_snapshot(self, incident: IncidentRecord, policy: TargetPolicy, release: ReleaseRecord, proposal: UpgradeProposal, now: int) -> str:
        return json.dumps({'incident_id': incident.incident_id, 'target': str(incident.target), 'release_id': incident.release_id, 'installed_code_hash': incident.installed_code_hash, 'incident_type': incident.incident_type, 'primary_url': incident.primary_url, 'primary_evidence_id': incident.primary_evidence_id, 'corroboration_url': incident.corroboration_url, 'corroboration_evidence_id': incident.corroboration_evidence_id, 'policy_fingerprint': incident.policy_fingerprint, 'recovery_capsule_hash': incident.recovery_capsule_hash, 'audit_authority': policy.audit_authority, 'corroboration_authority': policy.assurance_corroboration_authority, 'max_evidence_age_seconds': int(policy.max_evidence_age_seconds), 'review_now': now, 'release_code_hash': release.code_hash, 'proposal_recovery_capsule_hash': proposal.recovery_capsule_hash}, sort_keys=True, separators=(',', ':'))

    def _apply_incident_result(self, incident_id: str, result: dict[object, object]) -> None:
        incident = self.incidents[incident_id]
        release = self.releases[incident.release_id]
        proposal = self.proposals[release.proposal_id]
        incident.reviewed_at = u64(self._now())
        incident.last_review_code = str(result.get('error_code', ''))
        if result['kind'] == REVIEW_REPAIR:
            incident.status = STATUS_INCIDENT_REPAIR
            return
        if result['kind'] == REVIEW_RETRY:
            incident.status = STATUS_INCIDENT_RETRY
            return
        if result.get('decision') != DECISION_APPROVE:
            incident.status = STATUS_INCIDENT_DISMISSED
            mode = ProofPatchTarget(incident.target).view(state=StorageType.LATEST_FINAL).proofpatch_release_mode()
            release.status = STATUS_INSTALLED_PROVISIONAL if mode == MODE_PROVISIONAL else STATUS_CERTIFIED
            proposal.status = STATUS_INSTALLED_PROVISIONAL if mode == MODE_PROVISIONAL else STATUS_CERTIFIED
            return
        incident.status = STATUS_INCIDENT_CONFIRMED
        incident.recovery_authorized = True
        incident.recovery_deadline = u64(self._now() + int(self.policies[incident.target].execution_timeout_seconds))
        release.status = STATUS_INCIDENT_CONFIRMED
        ProofPatchTarget(incident.target).emit(on='finalized').proofpatch_recover(incident_id, incident.release_id, incident.recovery_capsule_hash)

    @gl.public.write
    def review_proposal(self, proposal_id: u256) -> None:
        if gl.message.sender_address == Address(REVIEW_ENGINE):
            proposal = self._require_proposal(proposal_id)
            if proposal.status != STATUS_REVIEW_PENDING:
                raise gl.vm.UserError('Proposal is not awaiting review callback')
            raw = self._engine().view(state=StorageType.LATEST_FINAL).get_proposal_result(proposal_id)
            result = self._engine_result(raw, {'target': str(proposal.target), 'proposal_id': int(proposal_id), 'parent_code_hash': proposal.parent_code_hash, 'candidate_code_hash': proposal.candidate_code_hash, 'policy_fingerprint': proposal.policy_fingerprint, 'evidence_set_hash': proposal.evidence_set_hash, 'assurance_manifest_hash': proposal.assurance_manifest_hash, 'recovery_capsule_hash': proposal.recovery_capsule_hash})
            proposal.reviewed_at = u64(self._now())
            self._apply_proposal_review(proposal_id, result)
            return
        proposal = self._require_proposal(proposal_id)
        if proposal.status not in (STATUS_PROPOSED, STATUS_RETRY, STATUS_REVIEW_PENDING):
            raise gl.vm.UserError('Proposal is not reviewable')
        now = self._now()
        if now > int(proposal.expires_at):
            raise gl.vm.UserError('Proposal has expired; call expire_proposal')
        policy = self.policies[proposal.target]
        if not policy.active or policy.policy_fingerprint != proposal.policy_fingerprint or policy.current_code_hash != proposal.parent_code_hash:
            raise gl.vm.UserError('Proposal policy snapshot is no longer current')
        proposal.status = STATUS_REVIEW_PENDING
        proposal.reviewed_at = u64(now)
        proposal.last_review_code = 'ENGINE_PENDING'
        self._engine().emit(on='finalized').review_proposal(proposal_id, self._proposal_review_snapshot(proposal, policy, now))

    @gl.public.view
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

    @gl.public.view
    def get_candidate_code(self, proposal_id: u256) -> bytes:
        if proposal_id not in self.proposals:
            raise gl.vm.UserError('Unknown proposal')
        proposal = self.proposals[proposal_id]
        if proposal.status != STATUS_QUEUED:
            raise gl.vm.UserError('Candidate is not authorized for installation')
        if self._now() > int(proposal.execution_deadline):
            raise gl.vm.UserError('Upgrade authorization expired')
        return proposal.candidate_code

    @gl.public.view
    def is_activation_authorized(self, proposal_id: u256, release_id: str, candidate_hash: str) -> bool:
        if proposal_id not in self.proposals:
            return False
        proposal = self.proposals[proposal_id]
        return proposal.status == STATUS_CERTIFICATION_QUEUED and release_id == self._proposal_release_id(proposal) and (candidate_hash.lower() == proposal.candidate_code_hash) and (release_id in self.releases) and (self.releases[release_id].status == STATUS_CERTIFICATION_QUEUED)

    @gl.public.view
    def is_registration_authorized(self, target: str, release_id: str, code_hash: str) -> bool:
        target_address = Address(target)
        if target_address not in self.policies:
            return False
        policy = self.policies[target_address]
        return policy.current_release_id == release_id and policy.current_code_hash == code_hash.lower() and (release_id in self.releases) and (self.releases[release_id].status == 'REGISTERED_PARENT')

    @gl.public.write
    def review_incident(self, incident_id: str) -> None:
        if incident_id not in self.incidents:
            raise gl.vm.UserError('Unknown incident')
        incident = self.incidents[incident_id]
        if gl.message.sender_address == Address(REVIEW_ENGINE):
            if incident.status != STATUS_INCIDENT_REVIEW_PENDING:
                raise gl.vm.UserError('Incident is not awaiting review callback')
            raw = self._engine().view(state=StorageType.LATEST_FINAL).get_incident_result(incident_id)
            result = self._engine_result(raw, {'incident_id': incident_id, 'target': str(incident.target), 'release_id': incident.release_id, 'installed_code_hash': incident.installed_code_hash, 'policy_fingerprint': incident.policy_fingerprint, 'recovery_capsule_hash': incident.recovery_capsule_hash})
            self._apply_incident_result(incident_id, result)
            return
        if incident.status not in (STATUS_INCIDENT_OPEN, STATUS_INCIDENT_RETRY, STATUS_INCIDENT_REVIEW_PENDING):
            raise gl.vm.UserError('Incident is not reviewable')
        if self._now() > int(incident.expires_at):
            raise gl.vm.UserError('Incident review window has expired')
        policy = self.policies[incident.target]
        release = self.releases[incident.release_id]
        proposal = self.proposals[release.proposal_id]
        now = self._now()
        incident.status = STATUS_INCIDENT_REVIEW_PENDING
        incident.reviewed_at = u64(now)
        incident.last_review_code = 'ENGINE_PENDING'
        self._engine().emit(on='finalized').review_incident(incident_id, self._incident_snapshot(incident, policy, release, proposal, now))

    @gl.public.view
    def is_recovery_authorized(self, incident_id: str, release_id: str, recovery_hash: str) -> bool:
        if incident_id not in self.incidents or release_id not in self.releases:
            return False
        incident = self.incidents[incident_id]
        return incident.status in (STATUS_INCIDENT_CONFIRMED, STATUS_RECOVERY_QUEUED, STATUS_RECOVERY_RETRY) and incident.recovery_authorized and (incident.release_id == release_id) and (incident.recovery_capsule_hash == recovery_hash.lower())

    @gl.public.view
    def get_recovery_release_id(self, incident_id: str) -> str:
        if incident_id not in self.incidents:
            return ''
        incident = self.incidents[incident_id]
        if incident.release_id not in self.releases:
            return ''
        release = self.releases[incident.release_id]
        if release.proposal_id not in self.proposals:
            return ''
        return self._recovery_release_id(self.proposals[release.proposal_id])

    @gl.public.view
    def get_recovery_code(self, incident_id: str) -> bytes:
        if incident_id not in self.incidents:
            raise gl.vm.UserError('Unknown incident')
        incident = self.incidents[incident_id]
        release = self.releases[incident.release_id]
        proposal = self.proposals[release.proposal_id]
        if incident.status not in (STATUS_INCIDENT_CONFIRMED, STATUS_RECOVERY_QUEUED, STATUS_RECOVERY_RETRY):
            raise gl.vm.UserError('Recovery is not authorized')
        return proposal.recovery_code

    @gl.public.view
    def get_proposal_count(self) -> u256:
        return self.proposal_count

    @gl.public.view
    def get_proposal_status(self, proposal_id: u256) -> str:
        if proposal_id not in self.proposals:
            return 'UNKNOWN'
        return self.proposals[proposal_id].status

    @gl.public.view
    def get_candidate_hash(self, proposal_id: u256) -> str:
        if proposal_id not in self.proposals:
            return ''
        return self.proposals[proposal_id].candidate_code_hash

    @gl.public.view
    def get_proposal_release_id(self, proposal_id: u256) -> str:
        if proposal_id not in self.proposals:
            return ''
        return self._proposal_release_id(self.proposals[proposal_id])

    @gl.public.view
    def get_evidence_set_hash(self, proposal_id: u256) -> str:
        if proposal_id not in self.proposals:
            return ''
        return self.proposals[proposal_id].evidence_set_hash

    @gl.public.view
    def get_policy_fingerprint(self, target: str) -> str:
        target_address = Address(target)
        if target_address not in self.policies:
            return ''
        return self.policies[target_address].policy_fingerprint

    @gl.public.view
    def get_policy_kernel_hash(self, target: str) -> str:
        target_address = Address(target)
        if target_address not in self.policies:
            return ''
        return self.policies[target_address].proofpatch_kernel_hash

    @gl.public.view
    def get_current_code_hash(self, target: str) -> str:
        target_address = Address(target)
        if target_address not in self.policies:
            return ''
        return self.policies[target_address].current_code_hash

    @gl.public.view
    def get_current_version(self, target: str) -> str:
        target_address = Address(target)
        if target_address not in self.policies:
            return ''
        return self.policies[target_address].current_version

    @gl.public.view
    def get_current_release_id(self, target: str) -> str:
        target_address = Address(target)
        if target_address not in self.policies:
            return ''
        return self.policies[target_address].current_release_id

    @gl.public.view
    def get_active_proposal(self, target: str) -> u256:
        target_address = Address(target)
        return self.active_proposal_by_target.get(target_address, self._inactive_proposal())

    @gl.public.view
    def get_proposal_summary(self, proposal_id: u256) -> str:
        if proposal_id not in self.proposals:
            return json.dumps({'status': 'UNKNOWN'}, separators=(',', ':'))
        proposal = self.proposals[proposal_id]
        return json.dumps({'proposal_id': int(proposal.proposal_id), 'target': str(proposal.target), 'parent_version': proposal.parent_version, 'parent_code_hash': proposal.parent_code_hash, 'candidate_version': proposal.candidate_version, 'candidate_code_hash': proposal.candidate_code_hash, 'policy_fingerprint': proposal.policy_fingerprint, 'evidence_set_hash': proposal.evidence_set_hash, 'assurance_manifest_hash': proposal.assurance_manifest_hash, 'recovery_mode': proposal.recovery_mode, 'recovery_release_id': proposal.recovery_release_id, 'recovery_capsule_hash': proposal.recovery_capsule_hash, 'release_id': self._proposal_release_id(proposal), 'status': proposal.status, 'last_review_code': proposal.last_review_code, 'created_at': int(proposal.created_at), 'expires_at': int(proposal.expires_at), 'reviewed_at': int(proposal.reviewed_at), 'execution_deadline': int(proposal.execution_deadline)}, separators=(',', ':'))

    @gl.public.view
    def get_release_summary(self, release_id: str) -> str:
        if release_id not in self.releases:
            return json.dumps({'status': 'UNKNOWN'}, separators=(',', ':'))
        release = self.releases[release_id]
        return json.dumps({'release_id': release.release_id, 'target': str(release.target), 'version': release.version, 'parent_release_id': release.parent_release_id, 'parent_code_hash': release.parent_code_hash, 'code_hash': release.code_hash, 'proposal_id': int(release.proposal_id), 'policy_fingerprint': release.policy_fingerprint, 'evidence_set_hash': release.evidence_set_hash, 'assurance_manifest_hash': release.assurance_manifest_hash, 'recovery_capsule_hash': release.recovery_capsule_hash, 'installed_at': int(release.installed_at), 'certified_at': int(release.certified_at), 'status': release.status, 'recovered_from_release_id': release.recovered_from_release_id, 'recovery_incident_id': release.recovery_incident_id, 'lineage_hash': release.lineage_hash}, separators=(',', ':'))

    @gl.public.view
    def get_incident_summary(self, incident_id: str) -> str:
        if incident_id not in self.incidents:
            return json.dumps({'status': 'UNKNOWN'}, separators=(',', ':'))
        incident = self.incidents[incident_id]
        return json.dumps({'incident_id': incident.incident_id, 'target': str(incident.target), 'release_id': incident.release_id, 'installed_code_hash': incident.installed_code_hash, 'incident_type': incident.incident_type, 'policy_fingerprint': incident.policy_fingerprint, 'recovery_capsule_hash': incident.recovery_capsule_hash, 'opened_at': int(incident.opened_at), 'expires_at': int(incident.expires_at), 'reviewed_at': int(incident.reviewed_at), 'recovery_deadline': int(incident.recovery_deadline), 'status': incident.status, 'last_review_code': incident.last_review_code, 'recovery_authorized': incident.recovery_authorized}, separators=(',', ':'))

    def _encode(self, value: object) -> object:
        if isinstance(value, Address):
            return str(value)
        if isinstance(value, bytes):
            return value.hex()
        if isinstance(value, (u256, u64)):
            return int(value)
        if isinstance(value, dict):
            return {str(k): self._encode(v) for (k, v) in value.items()}
        if isinstance(value, list):
            return [self._encode(v) for v in value]
        if hasattr(value, '__dict__'):
            return {k: self._encode(v) for (k, v) in value.__dict__.items()}
        return value

    def _record(self, cls: object, raw: dict[object, object]) -> object:
        value = dict(raw)
        fields = {'TargetPolicy': ('owner', 'target'), 'UpgradeProposal': ('target', 'proposer'), 'ReleaseRecord': ('target',), 'IncidentRecord': ('target',)}
        for field in fields.get(cls.__name__, ()):
            value[field] = Address(value[field])
        for field in ('candidate_code', 'recovery_code'):
            if field in value and isinstance(value[field], str):
                value[field] = bytes.fromhex(value[field])
        return cls(**value)

    def _state(self) -> str:
        return json.dumps(self._encode({'policies': self.policies, 'proposals': self.proposals, 'releases': self.releases, 'incidents': self.incidents, 'active_proposal_by_target': self.active_proposal_by_target, 'used_evidence_ids': self.used_evidence_ids, 'installed_candidate_hashes': self.installed_candidate_hashes, 'used_incident_ids': self.used_incident_ids, 'proposal_count': self.proposal_count, 'release_count': self.release_count}), sort_keys=True, separators=(',', ':'))

    def _apply_state(self, raw: str) -> None:
        state = json.loads(raw)
        self.policies = {Address(k): self._record(TargetPolicy, v) for (k, v) in state.get('policies', {}).items()}
        self.proposals = {u256(int(k)): self._record(UpgradeProposal, v) for (k, v) in state.get('proposals', {}).items()}
        self.releases = {k: self._record(ReleaseRecord, v) for (k, v) in state.get('releases', {}).items()}
        self.incidents = {k: self._record(IncidentRecord, v) for (k, v) in state.get('incidents', {}).items()}
        self.active_proposal_by_target = {Address(k): u256(v) for (k, v) in state.get('active_proposal_by_target', {}).items()}
        self.used_evidence_ids = dict(state.get('used_evidence_ids', {}))
        self.installed_candidate_hashes = dict(state.get('installed_candidate_hashes', {}))
        self.used_incident_ids = dict(state.get('used_incident_ids', {}))
        self.proposal_count = u256(state.get('proposal_count', 0))
        self.release_count = u256(state.get('release_count', 0))

    def _policy_request(self, operation: str, args: list[object], actor: str, **extra: object) -> None:
        data = {'state': json.loads(self._state()), 'args': args, 'actor': actor, 'now': self._now()}
        data.update(extra)
        ProofPatchPolicyEngine(Address(POLICY_ENGINE)).emit(on='finalized').execute(operation, json.dumps(data, sort_keys=True, separators=(',', ':')))

    @gl.public.write
    def apply_policy_result(self, operation: str, payload: str) -> None:
        if gl.message.sender_address != Address(POLICY_ENGINE):
            raise gl.vm.UserError('Only policy engine may apply state')
        before = set((str(k) for k in self.policies))
        self._apply_state(payload)
        if operation == 'register':
            target = next((Address(k) for k in self.policies if str(k) not in before), None)
            if target is not None:
                policy = self.policies[target]
                ProofPatchTarget(target).emit(on='finalized').proofpatch_confirm_registration(policy.current_release_id, policy.current_code_hash)
