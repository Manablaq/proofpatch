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
REVIEW_ENGINE = '0xe33d03511EC85bccfAa1b2F93C2685F21eFA326e'
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
ZERO = '0x0000000000000000000000000000000000000000'
@gl.contract_interface
class ProofPatchGovernorV2:

    class Write:

        def apply_lifecycle_result(self, operation: str, payload: str) -> None:
            ...
class ProofPatchLifecycleLogic:

    def __init__(self):
        self.policies = {}
        self.proposals = {}
        self.releases = {}
        self.incidents = {}
        self.active_proposal_by_target = {}
        self.installed_candidate_hashes = {}
        self.proposal_count = u256(0)
        self.release_count = u256(0)
        self.actions = []

    def _now(self) -> int:
        return self.now

    def _hash_text_parts(self, parts: list[str]) -> str:
        return hashlib.sha256('\x1f'.join(parts).encode('utf-8')).hexdigest()

    def _inactive_proposal(self) -> u256:
        return u256(0)

    def _require_policy_owner(self, target: Address) -> TargetPolicy:
        if target not in self.policies:
            raise gl.vm.UserError('Target is not registered')
        policy = self.policies[target]
        if self.actor != policy.owner:
            raise gl.vm.UserError('Only the registered target owner may perform this action')
        if not policy.active:
            raise gl.vm.UserError('Target policy is inactive')
        return policy

    def _require_proposal(self, proposal_id: u256) -> UpgradeProposal:
        if proposal_id not in self.proposals:
            raise gl.vm.UserError('Unknown proposal')
        return self.proposals[proposal_id]

    def _release_active(self, target: Address, proposal_id: u256) -> None:
        if self.active_proposal_by_target.get(target, self._inactive_proposal()) == proposal_id:
            self.active_proposal_by_target[target] = self._inactive_proposal()

    def _proposal_release_id(self, proposal: UpgradeProposal) -> str:
        return 'release-' + str(proposal.proposal_id) + '-' + proposal.candidate_code_hash[:16]

    def _lineage_hash(self, target: Address, previous_lineage_hash: str, release_id: str, parent_release_id: str, version: str, code_hash: str, policy_fingerprint: str, evidence_set_hash: str, assurance_manifest_hash: str, recovery_capsule_hash: str) -> str:
        return self._hash_text_parts([SCHEMA_VERSION, str(target), previous_lineage_hash, release_id, parent_release_id, version, code_hash, policy_fingerprint, evidence_set_hash, assurance_manifest_hash, recovery_capsule_hash])

    def _record_verified_install(self, proposal_id: u256, proposal: UpgradeProposal, review_code: str) -> None:
        policy = self.policies[proposal.target]
        if policy.current_code_hash != proposal.parent_code_hash:
            raise gl.vm.UserError('Target policy parent changed before installation reconciliation')
        release_id = self._proposal_release_id(proposal)
        if release_id in self.releases:
            existing = self.releases[release_id]
            if existing.code_hash != proposal.candidate_code_hash:
                raise gl.vm.UserError('Conflicting release identity')
            proposal.status = STATUS_INSTALLED_PROVISIONAL
            return
        parent_release = self.releases.get(policy.current_release_id)
        if parent_release is None:
            raise gl.vm.UserError('Current certified release is missing')
        now = self._now()
        lineage_hash = self._lineage_hash(proposal.target, parent_release.lineage_hash, release_id, policy.current_release_id, proposal.candidate_version, proposal.candidate_code_hash, proposal.policy_fingerprint, proposal.evidence_set_hash, proposal.assurance_manifest_hash, proposal.recovery_capsule_hash)
        self.releases[release_id] = ReleaseRecord(release_id=release_id, target=proposal.target, version=proposal.candidate_version, parent_release_id=policy.current_release_id, parent_code_hash=proposal.parent_code_hash, source_url=proposal.candidate_source_url, code_hash=proposal.candidate_code_hash, proposal_id=proposal_id, policy_fingerprint=proposal.policy_fingerprint, evidence_set_hash=proposal.evidence_set_hash, assurance_manifest_hash=proposal.assurance_manifest_hash, recovery_capsule_hash=proposal.recovery_capsule_hash, installed_at=u64(now), certified_at=u64(0), status=STATUS_INSTALLED_PROVISIONAL, recovered_from_release_id='', recovery_incident_id='', lineage_hash=lineage_hash)
        self.release_count = u256(int(self.release_count) + 1)
        proposal.status = STATUS_INSTALLED_PROVISIONAL
        proposal.last_review_code = review_code
        self.installed_candidate_hashes[self._hash_text_parts([str(proposal.target), proposal.candidate_code_hash])] = True

    def cancel(self, proposal_id: u256) -> None:
        proposal = self._require_proposal(proposal_id)
        self._require_policy_owner(proposal.target)
        if proposal.status not in (STATUS_PROPOSED, STATUS_REPAIR, STATUS_RETRY):
            raise gl.vm.UserError('Proposal can no longer be cancelled')
        proposal.status = STATUS_CANCELLED
        proposal.last_review_code = 'OWNER_CANCELLED'
        self._release_active(proposal.target, proposal_id)

    def expire(self, proposal_id: u256) -> None:
        proposal = self._require_proposal(proposal_id)
        if proposal.status not in (STATUS_PROPOSED, STATUS_REPAIR, STATUS_RETRY):
            raise gl.vm.UserError('Proposal is not expirable')
        if self._now() <= int(proposal.expires_at):
            raise gl.vm.UserError('Proposal has not expired')
        proposal.status = STATUS_EXPIRED
        proposal.last_review_code = 'PROPOSAL_EXPIRED'
        self._release_active(proposal.target, proposal_id)

    def _check_install_readback(self, proposal_id: u256, proposal: UpgradeProposal, policy: TargetPolicy) -> None:
        if self.target_final_proposal_id != proposal_id:
            raise gl.vm.UserError('Target has not finalized this proposal')
        if self.target_final_candidate_hash != proposal.candidate_code_hash:
            raise gl.vm.UserError('Finalized target code hash does not match approved candidate')
        if self.target_final_release_id != self._proposal_release_id(proposal):
            raise gl.vm.UserError('Target release identity does not match proposal')
        if self.target_final_mode != MODE_PROVISIONAL:
            raise gl.vm.UserError('Target did not enter PROVISIONAL mode')
        if self.target_final_kernel_hash != policy.proofpatch_kernel_hash:
            raise gl.vm.UserError('Target ProofPatch kernel hash changed')

    def confirm_install(self, proposal_id: u256, candidate_hash: str) -> None:
        proposal = self._require_proposal(proposal_id)
        if self.actor != proposal.target:
            raise gl.vm.UserError('Only the protected target may confirm installation')
        if proposal.status in (STATUS_INSTALLED_PROVISIONAL, STATUS_ASSURANCE_PENDING, STATUS_CERTIFICATION_QUEUED, STATUS_CERTIFIED):
            if candidate_hash.lower() != proposal.candidate_code_hash:
                raise gl.vm.UserError('Conflicting duplicate installation confirmation')
            return
        if proposal.status != STATUS_QUEUED:
            raise gl.vm.UserError('Proposal is not awaiting installation confirmation')
        if candidate_hash.lower() != proposal.candidate_code_hash:
            raise gl.vm.UserError('Installed hash does not match approved candidate')
        self._check_install_readback(proposal_id, proposal, self.policies[proposal.target])
        self._record_verified_install(proposal_id, proposal, 'INSTALL_VERIFIED')

    def reconcile_install(self, proposal_id: u256) -> None:
        proposal = self._require_proposal(proposal_id)
        self._require_policy_owner(proposal.target)
        if proposal.status != STATUS_QUEUED:
            raise gl.vm.UserError('Proposal is not awaiting installation')
        self._check_install_readback(proposal_id, proposal, self.policies[proposal.target])
        self._record_verified_install(proposal_id, proposal, 'INSTALL_RECONCILED')

    def mark_timeout(self, proposal_id: u256) -> None:
        proposal = self._require_proposal(proposal_id)
        policy = self._require_policy_owner(proposal.target)
        if proposal.status != STATUS_QUEUED:
            raise gl.vm.UserError('Proposal is not awaiting installation')
        if self._now() <= int(proposal.execution_deadline):
            raise gl.vm.UserError('Execution deadline has not passed')
        if self.target_final_proposal_id == proposal_id and self.target_final_candidate_hash == proposal.candidate_code_hash:
            self._check_install_readback(proposal_id, proposal, policy)
            self._record_verified_install(proposal_id, proposal, 'INSTALL_RECONCILED_TIMEOUT')
            return
        finalized_still_parent = self.target_final_proposal_id == self._inactive_proposal() and self.target_final_candidate_hash == '' or (self.target_final_proposal_id != proposal_id and self.target_final_candidate_hash == policy.current_code_hash)
        if not finalized_still_parent:
            raise gl.vm.UserError('Finalized target installation attestation is inconsistent; active proposal remains locked')
        if self.target_nonfinal_proposal_id == proposal_id and self.target_nonfinal_candidate_hash == proposal.candidate_code_hash:
            raise gl.vm.UserError('Target installation is pending finality; active proposal remains locked')
        if self.target_nonfinal_proposal_id != self.target_final_proposal_id or self.target_nonfinal_candidate_hash != self.target_final_candidate_hash:
            raise gl.vm.UserError('Target non-final installation attestation is inconsistent; active proposal remains locked')
        proposal.status = STATUS_EXECUTION_FAILED
        proposal.last_review_code = 'EXECUTION_TIMEOUT'
        self._release_active(proposal.target, proposal_id)

class ProofPatchLifecycleEngine(gl.Contract):
    admin: Address
    governor: Address
    executor: Address

    def __init__(self):
        self.admin = gl.message.sender_address
        self.governor = Address(ZERO)
        self.executor = Address(ZERO)

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

    @gl.public.write
    def bind_executor(self, executor: str) -> None:
        if gl.message.sender_address != self.admin:
            raise gl.vm.UserError('Only admin may bind executor')
        if self.executor != Address(ZERO):
            raise gl.vm.UserError('Executor is already bound')
        candidate = Address(executor)
        if candidate == Address(ZERO):
            raise gl.vm.UserError('Executor cannot be the zero address')
        self.executor = candidate

    def _encode(self, value: object) -> object:
        if isinstance(value, Address):
            return str(value)
        if isinstance(value, bytes):
            return value.hex()
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return int(value)
        if isinstance(value, dict):
            return {str(key): self._encode(item) for key, item in value.items()}
        if isinstance(value, list):
            return [self._encode(item) for item in value]
        if hasattr(value, '__dict__'):
            return {key: self._encode(item) for key, item in value.__dict__.items()}
        return value

    def _record(self, cls: typing.Any, raw: dict[object, object]) -> typing.Any:
        value = list(raw.values())
        if cls in (TargetPolicy, UpgradeProposal, ReleaseRecord):
            value[1] = Address(value[1])
        if cls is TargetPolicy:
            value[0] = Address(value[0])
        elif cls is UpgradeProposal:
            value[2] = Address(value[2])
            if isinstance(value[8], str):
                value[8] = bytes.fromhex(value[8])
            if isinstance(value[20], str):
                value[20] = bytes.fromhex(value[20])
        return cls(**dict(zip(cls.__annotations__.keys(), value)))

    def _load(self, logic: ProofPatchLifecycleLogic, data: dict[object, object]) -> None:
        logic.actor = Address(data['actor'])
        logic.now = int(data['now'])
        records = typing.cast(dict[str, typing.Any], data.get('records', {}))
        logic.proposal_count = u256(data.get('proposal_count', 0))
        logic.release_count = u256(data.get('release_count', 0))
        logic.installed_candidate_hashes = typing.cast(dict[object, bool], data.get('installed_candidate_hashes', {}))
        if records.get('policy') is not None:
            policy = self._record(TargetPolicy, records['policy'])
            logic.policies[policy.target] = policy
        if records.get('proposal') is not None:
            proposal = self._record(UpgradeProposal, records['proposal'])
            logic.proposals[proposal.proposal_id] = proposal
        for key in ('release', 'parent_release'):
            if records.get(key) is not None:
                release = self._record(ReleaseRecord, records[key])
                logic.releases[release.release_id] = release
        if data.get('active_target') is not None:
            logic.active_proposal_by_target[Address(data['active_target'])] = u256(data.get('active_value', 0))
        view = typing.cast(dict[str, typing.Any], data.get('target_final', {}))
        logic.target_final_proposal_id = u256(view.get('proposal_id', 0))
        logic.target_final_candidate_hash = str(view.get('candidate_hash', ''))
        logic.target_final_release_id = str(view.get('release_id', ''))
        logic.target_final_mode = str(view.get('mode', ''))
        logic.target_final_kernel_hash = str(view.get('kernel_hash', ''))
        nonfinal = typing.cast(dict[str, typing.Any], data.get('target_nonfinal', {}))
        logic.target_nonfinal_proposal_id = u256(nonfinal.get('proposal_id', 0))
        logic.target_nonfinal_candidate_hash = str(nonfinal.get('candidate_hash', ''))

    def _patch(self, logic: ProofPatchLifecycleLogic, operation: str) -> dict[object, object]:
        out = {'operation': operation, 'policies': [], 'proposals': [], 'releases': [], 'incidents': [], 'active': [], 'installed_candidate_hashes': logic.installed_candidate_hashes, 'proposal_count': int(logic.proposal_count), 'release_count': int(logic.release_count), 'actions': logic.actions}
        for value in logic.policies.values():
            out['policies'].append(self._encode(value))
        for value in logic.proposals.values():
            out['proposals'].append(self._encode(value))
        for value in logic.releases.values():
            out['releases'].append(self._encode(value))
        for target, value in logic.active_proposal_by_target.items():
            out['active'].append([str(target), int(value)])
        return out

    @gl.public.write
    def execute(self, operation: str, request: str) -> None:
        if gl.message.sender_address != self.executor:
            raise gl.vm.UserError('Only the bound lifecycle request engine may execute lifecycle logic')
        if operation not in ('cancel', 'expire', 'confirm_install', 'reconcile_install', 'timeout'):
            raise gl.vm.UserError('Unsupported proposal lifecycle operation')
        data = json.loads(request)
        logic = ProofPatchLifecycleLogic()
        self._load(logic, data)
        args = data.get('args', [])
        if operation == 'cancel':
            logic.cancel(*args)
        elif operation == 'expire':
            logic.expire(*args)
        elif operation == 'confirm_install':
            logic.confirm_install(*args)
        elif operation == 'reconcile_install':
            logic.reconcile_install(*args)
        else:
            logic.mark_timeout(*args)
        payload = json.dumps(self._patch(logic, operation), separators=(',', ':'))
        ProofPatchGovernorV2(self.governor).emit(on='finalized').apply_lifecycle_result(operation, payload)
