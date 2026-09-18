# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownParameterType=false, reportMissingParameterType=false, reportInvalidTypeForm=false, reportOptionalMemberAccess=false, reportUnboundVariable=false, reportOptionalSubscript=false, reportGeneralTypeIssues=false, reportAssignmentType=false, reportIndexIssue=false, reportCallIssue=false, reportUnnecessaryCast=false, reportPrivateUsage=false, reportUnusedFunction=false, reportUnusedImport=false
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
REVIEW_ENGINE = '0x9840cCf5DBdf4AE5945Ca73367e8336cCBEF578e'
ASSURANCE_REVIEW_ENGINE = '0x32E5eFAF7558B65f72dA2B2B27f040e74fA148BC'
STATUS_REVIEW_PENDING = 'REVIEW_PENDING'
STATUS_INCIDENT_REVIEW_PENDING = 'INCIDENT_REVIEW_PENDING'

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

class ProofPatchReviewCommitLogic:

    def __init__(self):
        self.policies = {}
        self.proposals = {}
        self.releases = {}
        self.incidents = {}
        self.active_proposal_by_target = {}
        self.actions = []

    def _now(self):
        return self.now

    def _require_proposal(self, proposal_id):
        if proposal_id not in self.proposals:
            raise gl.vm.UserError('Unknown proposal')
        return self.proposals[proposal_id]

    def _release_active(self, target, proposal_id):
        if self.active_proposal_by_target.get(target, u256(0)) == proposal_id:
            self.active_proposal_by_target[target] = u256(0)

    def _proposal_release_id(self, proposal):
        return 'release-' + str(proposal.proposal_id) + '-' + proposal.candidate_code_hash[:16]

    def proposal(self, proposal_id, result):
        proposal = self._require_proposal(proposal_id)
        policy = self.policies[proposal.target]
        proposal.reviewed_at = u64(self._now())
        proposal.last_review_code = str(result.get('error_code', ''))
        if result['kind'] == REVIEW_REPAIR:
            proposal.status = STATUS_REPAIR
            return
        if result['kind'] == REVIEW_RETRY:
            proposal.status = STATUS_RETRY
            return
        if result['kind'] != REVIEW_DECISION:
            raise gl.vm.UserError('Unexpected review result')
        if result['decision'] == DECISION_REJECT:
            proposal.status = STATUS_REJECTED
            self._release_active(proposal.target, proposal_id)
            return
        if result['decision'] != DECISION_APPROVE:
            raise gl.vm.UserError('Unexpected decision')
        proposal.status = STATUS_QUEUED
        proposal.execution_deadline = u64(self._now() + int(policy.execution_timeout_seconds))
        self.actions.append({'kind': 'upgrade', 'args': [str(proposal.target), int(proposal_id), proposal.candidate_code_hash]})

    def assurance(self, proposal_id, result, primary_url, primary_id, corroboration_url, corroboration_id):
        proposal = self._require_proposal(proposal_id)
        release_id = self._proposal_release_id(proposal)
        if result['kind'] == REVIEW_REPAIR:
            proposal.status = STATUS_ASSURANCE_REPAIR
            proposal.last_review_code = str(result.get('error_code', ''))
            return
        if result['kind'] == REVIEW_RETRY:
            proposal.status = STATUS_ASSURANCE_RETRY
            proposal.last_review_code = str(result.get('error_code', ''))
            return
        proposal.last_review_code = str(result.get('error_code', ''))
        if result.get('decision') == DECISION_APPROVE:
            proposal.status = STATUS_CERTIFICATION_QUEUED
            self.releases[release_id].status = STATUS_CERTIFICATION_QUEUED
            self.actions.append({'kind': 'activate', 'args': [str(proposal.target), release_id, proposal.candidate_code_hash]})
            return
        proposal.status = STATUS_INCIDENT_OPEN
        now = self._now()
        policy = self.policies[proposal.target]
        self.incidents['assurance-' + release_id] = IncidentRecord(incident_id='assurance-' + release_id, target=proposal.target, release_id=release_id, installed_code_hash=proposal.candidate_code_hash, incident_type='ASSURANCE_FAILURE', primary_url=primary_url, primary_evidence_id=primary_id, corroboration_url=corroboration_url, corroboration_evidence_id=corroboration_id, policy_fingerprint=proposal.policy_fingerprint, assurance_manifest_hash=proposal.assurance_manifest_hash, recovery_capsule_hash=proposal.recovery_capsule_hash, opened_at=u64(now), expires_at=u64(now + int(policy.proposal_ttl_seconds)), reviewed_at=u64(now), recovery_deadline=u64(0), status=STATUS_INCIDENT_OPEN, last_review_code='ASSURANCE_FAILED', recovery_authorized=False)
        self.releases[release_id].status = STATUS_INCIDENT_OPEN

    def incident(self, incident_id, result):
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
            release.status = STATUS_INSTALLED_PROVISIONAL if self.target_mode == MODE_PROVISIONAL else STATUS_CERTIFIED
            proposal.status = STATUS_INSTALLED_PROVISIONAL if self.target_mode == MODE_PROVISIONAL else STATUS_CERTIFIED
            return
        incident.status = STATUS_INCIDENT_CONFIRMED
        incident.recovery_authorized = True
        incident.recovery_deadline = u64(self._now() + int(self.policies[incident.target].execution_timeout_seconds))
        release.status = STATUS_INCIDENT_CONFIRMED
        self.actions.append({'kind': 'recover', 'args': [incident_id, incident.release_id, incident.recovery_capsule_hash]})
ZERO = '0x0000000000000000000000000000000000000000'

@gl.contract_interface
class ProofPatchGovernorV2:

    class View:

        def get_state_record(self, kind: str, key: str) -> str:
            ...

    class Write:

        def apply_review_result(self, operation: str, payload: str) -> None:
            ...

@gl.contract_interface
class ProofPatchReviewEngine:

    class View:

        def get_proposal_result(self, proposal_id: u256) -> str:
            ...

        def get_assurance_result(self, proposal_id: u256) -> str:
            ...

        def get_incident_result(self, incident_id: str) -> str:
            ...

@gl.contract_interface
class ProofPatchAssuranceIncidentEngine:

    class View:

        def get_assurance_result(self, proposal_id: u256) -> str:
            ...

        def get_incident_result(self, incident_id: str) -> str:
            ...

@gl.contract_interface
class ProofPatchTarget:

    class View:

        def proofpatch_release_mode(self) -> str:
            ...

class ProofPatchReviewCommitEngine(gl.Contract):
    admin: Address
    governor: Address

    def __init__(self):
        self.admin = gl.message.sender_address
        self.governor = Address(ZERO)

    @gl.public.write
    def bind_governor(self, governor: str) -> None:
        if gl.message.sender_address != self.admin:
            raise gl.vm.UserError('Only admin may bind governor')
        if self.governor != Address(ZERO):
            raise gl.vm.UserError('Governor is already bound')
        candidate = Address(governor)
        if candidate == Address(ZERO):
            raise gl.vm.UserError('Governor cannot be the zero address')
        self.governor = candidate

    def _encode(self, value):
        if isinstance(value, Address):
            return str(value)
        if isinstance(value, bytes):
            return value.hex()
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return int(value)
        if isinstance(value, dict):
            return {str(k): self._encode(v) for (k, v) in value.items()}
        if isinstance(value, list):
            return [self._encode(v) for v in value]
        if hasattr(value, '__dict__'):
            return {k: self._encode(v) for (k, v) in value.__dict__.items()}
        return value

    def _record(self, cls, raw):
        value = list(raw.values())
        if cls is TargetPolicy or cls is UpgradeProposal or cls is ReleaseRecord or cls is IncidentRecord:
            value[1] = Address(value[1])
        if cls is TargetPolicy:
            value[0] = Address(value[0])
        elif cls is UpgradeProposal:
            value[2] = Address(value[2])
            if isinstance(value[8], str): value[8] = bytes.fromhex(value[8])
            if isinstance(value[20], str): value[20] = bytes.fromhex(value[20])
        return cls(**dict(zip(cls.__annotations__.keys(), value)))

    def _load(self, logic, data):
        logic.actor = Address(data['actor'])
        logic.now = int(data['now'])
        for (key, cls, store) in (('policy', TargetPolicy, logic.policies), ('proposal', UpgradeProposal, logic.proposals), ('release', ReleaseRecord, logic.releases), ('incident', IncidentRecord, logic.incidents)):
            if data.get(key) is not None:
                value = self._record(cls, data[key])
                store[value.target if key == 'policy' else value.proposal_id if key == 'proposal' else value.release_id if key == 'release' else value.incident_id] = value
        if data.get('active_target') is not None:
            logic.active_proposal_by_target[Address(data['active_target'])] = u256(data.get('active_value', 0))
        logic.target_mode = str(data.get('target_mode', ''))

    def _result(self, raw, expected):
        try:
            result = json.loads(raw)
        except Exception:
            raise gl.vm.UserError('Review engine returned invalid JSON')
        if not isinstance(result, dict):
            raise gl.vm.UserError('Review engine returned an invalid result')
        for (key, value) in expected.items():
            if result.get(key) != value:
                raise gl.vm.UserError('Review engine result binding mismatch')
        return result

    def _state(self, view, kind, key):
        return json.loads(view.get_state_record(kind, key))

    def _request_state(self, operation, data, view):
        args = data.get('args', [])
        if operation == 'proposal':
            proposal = self._state(view, 'proposal', str(int(args[0])))
            policy = self._state(view, 'policy', proposal['target'])
            result = self._result(ProofPatchReviewEngine(Address(REVIEW_ENGINE)).view(state=StorageType.LATEST_FINAL).get_proposal_result(u256(args[0])), {'target': proposal['target'], 'proposal_id': int(args[0]), 'parent_code_hash': proposal['parent_code_hash'], 'candidate_code_hash': proposal['candidate_code_hash'], 'policy_fingerprint': proposal['policy_fingerprint'], 'evidence_set_hash': proposal['evidence_set_hash'], 'assurance_manifest_hash': proposal['assurance_manifest_hash'], 'recovery_capsule_hash': proposal['recovery_capsule_hash']})
            if proposal['status'] != STATUS_REVIEW_PENDING:
                raise gl.vm.UserError('Proposal is not awaiting review callback')
            return {'proposal': proposal, 'policy': policy, 'active_target': proposal['target'], 'active_value': self._state(view, 'active', proposal['target'])['value'], 'result': result}
        if operation == 'assurance':
            proposal = self._state(view, 'proposal', str(int(args[0])))
            policy = self._state(view, 'policy', proposal['target'])
            result = self._result(ProofPatchAssuranceIncidentEngine(Address(ASSURANCE_REVIEW_ENGINE)).view(state=StorageType.LATEST_FINAL).get_assurance_result(u256(args[0])), {'target': proposal['target'], 'proposal_id': int(args[0]), 'release_id': 'release-' + str(proposal['proposal_id']) + '-' + proposal['candidate_code_hash'][:16], 'candidate_code_hash': proposal['candidate_code_hash'], 'policy_fingerprint': proposal['policy_fingerprint'], 'assurance_manifest_hash': proposal['assurance_manifest_hash']})
            if proposal['status'] != STATUS_ASSURANCE_PENDING:
                raise gl.vm.UserError('Release is not awaiting assurance callback')
            return {'proposal': proposal, 'policy': policy, 'release': self._state(view, 'release', 'release-' + str(proposal['proposal_id']) + '-' + proposal['candidate_code_hash'][:16]), 'result': result}
        if operation == 'incident':
            incident = self._state(view, 'incident', args[0])
            release = self._state(view, 'release', incident['release_id'])
            proposal = self._state(view, 'proposal', str(release['proposal_id']))
            policy = self._state(view, 'policy', incident['target'])
            result = self._result(ProofPatchAssuranceIncidentEngine(Address(ASSURANCE_REVIEW_ENGINE)).view(state=StorageType.LATEST_FINAL).get_incident_result(args[0]), {'incident_id': args[0], 'target': incident['target'], 'release_id': incident['release_id'], 'installed_code_hash': incident['installed_code_hash'], 'policy_fingerprint': incident['policy_fingerprint'], 'recovery_capsule_hash': incident['recovery_capsule_hash']})
            if incident['status'] != STATUS_INCIDENT_REVIEW_PENDING:
                raise gl.vm.UserError('Incident is not awaiting review callback')
            target_mode = ProofPatchTarget(Address(incident['target'])).view(state=StorageType.LATEST_FINAL).proofpatch_release_mode()
            return {'incident': incident, 'release': release, 'proposal': proposal, 'policy': policy, 'target_mode': target_mode, 'result': result}
        raise gl.vm.UserError('Unknown review operation')

    def _patch(self, logic, operation):
        out = {'operation': operation, 'policies': [], 'proposals': [], 'releases': [], 'incidents': [], 'active': [], 'actions': logic.actions}
        for value in logic.policies.values():
            out['policies'].append(self._encode(value))
        for value in logic.proposals.values():
            out['proposals'].append(self._encode(value))
        for value in logic.releases.values():
            out['releases'].append(self._encode(value))
        for value in logic.incidents.values():
            out['incidents'].append(self._encode(value))
        for (key, value) in logic.active_proposal_by_target.items():
            out['active'].append([str(key), int(value)])
        return out

    @gl.public.write
    def execute(self, operation: str, request: str) -> None:
        if gl.message.sender_address != self.governor:
            raise gl.vm.UserError('Only the bound governor may execute review commits')
        data = json.loads(request)
        state = self._request_state(operation, data, ProofPatchGovernorV2(self.governor).view(state=StorageType.LATEST_FINAL))
        for (key, value) in state.items():
            if key != 'result':
                data[key] = value
        logic = ProofPatchReviewCommitLogic()
        self._load(logic, data)
        args = data.get('args', [])
        if operation == 'proposal':
            logic.proposal(args[0], state['result'])
        elif operation == 'assurance':
            logic.assurance(args[0], state['result'], args[1], args[2], args[3], args[4])
        elif operation == 'incident':
            logic.incident(args[0], state['result'])
        else:
            raise gl.vm.UserError('Unknown review operation')
        payload = json.dumps(self._patch(logic, operation), separators=(',', ':'))
        ProofPatchGovernorV2(self.governor).emit(on='finalized').apply_review_result(operation, payload)
