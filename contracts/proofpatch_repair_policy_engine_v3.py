# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownParameterType=false, reportMissingParameterType=false, reportInvalidTypeForm=false, reportOptionalMemberAccess=false, reportUnboundVariable=false, reportOptionalSubscript=false, reportGeneralTypeIssues=false, reportAssignmentType=false, reportIndexIssue=false, reportCallIssue=false, reportUnnecessaryCast=false, reportPrivateUsage=false, reportUnusedFunction=false, reportUnusedImport=false
from genlayer import *
from dataclasses import dataclass
from genlayer.py.public_abi import StorageType
import hashlib
import json
import typing
SCHEMA_VERSION = 'proofpatch-v2'
ASSURANCE_SCHEMA = 'proofpatch-assurance-v1'
MODE_ACTIVE = 'ACTIVE'
MODE_PROVISIONAL = 'PROVISIONAL'
MODE_RECOVERED = 'RECOVERED'
STATUS_PROPOSED = 'PROPOSED'
STATUS_REPAIR = 'EVIDENCE_REPAIR_REQUIRED'
STATUS_INSTALLED_PROVISIONAL = 'INSTALLED_PROVISIONAL'
STATUS_ASSURANCE_PENDING = 'ASSURANCE_PENDING'
STATUS_ASSURANCE_REPAIR = 'ASSURANCE_REPAIR_REQUIRED'
STATUS_ASSURANCE_RETRY = 'ASSURANCE_RETRY_REQUIRED'
STATUS_CERTIFIED = 'CERTIFIED'
STATUS_INCIDENT_OPEN = 'INCIDENT_OPEN'
STATUS_INCIDENT_REPAIR = 'INCIDENT_REPAIR_REQUIRED'
STATUS_INCIDENT_RETRY = 'INCIDENT_RETRY_REQUIRED'
MAX_CONSTITUTION_BYTES = 16000
MAX_CANDIDATE_BYTES = 512000
MAX_URL_BYTES = 1024
MAX_ID_BYTES = 160
MAX_VERSION_BYTES = 96
MAX_EVIDENCE_AGE_SECONDS = 30 * 24 * 60 * 60
MAX_PROPOSAL_TTL_SECONDS = 14 * 24 * 60 * 60
MAX_EXECUTION_TIMEOUT_SECONDS = 7 * 24 * 60 * 60
MIN_WINDOW_SECONDS = 60
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
ZERO = '0x0000000000000000000000000000000000000000'
@gl.contract_interface
class ProofPatchGovernor:

    class View:

        def get_state_record(self, kind: str, key: str) -> str:
            ...

    class Write:

        def apply_policy_result(self, operation: str, payload: str) -> None:
            ...
class RepairPolicyLogic:
    def _hash_text_parts(self, parts: list[str]) -> str:
        return hashlib.sha256('\x1f'.join(parts).encode('utf-8')).hexdigest()
    def _check_text(self, value: str, label: str, minimum: int, maximum: int) -> None:
        encoded_len = len(value.encode('utf-8'))
        if encoded_len < minimum or encoded_len > maximum:
            raise gl.vm.UserError(f'{label} length is invalid')
    def _is_canonical_raw_segment(self, value: str) -> bool:
        """Accept only a single parser-stable raw-GitHub path representation.

            ProofPatch compares the raw URL before GenVM hands it to an HTTP URL
            parser. Restricting every path component to this canonical ASCII form
            prevents dot-segment, percent-encoding, backslash, control-character,
            repeated-separator, and Unicode-normalization aliases from changing the
            resource that is actually fetched.
            """
        if not value or value in ('.', '..'):
            return False
        allowed = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'
        for char in value:
            if char not in allowed:
                return False
        return True
    def _raw_github_owner(self, prefix: str) -> str:
        base = 'https://raw.githubusercontent.com/'
        if not prefix.startswith(base) or not prefix.endswith('/'):
            return ''
        rest = prefix[len(base):]
        parts = rest.split('/')
        if len(parts) != 3 or parts[2] != '':
            return ''
        owner = parts[0]
        repository = parts[1]
        if not self._is_canonical_raw_segment(owner):
            return ''
        if not self._is_canonical_raw_segment(repository):
            return ''
        return owner
    def _is_authority_prefix(self, prefix: str) -> bool:
        return self._raw_github_owner(prefix) != ''
    def _is_immutable_url(self, url: str, prefix: str) -> bool:
        if len(url.encode('utf-8')) > MAX_URL_BYTES:
            return False
        if not self._is_authority_prefix(prefix):
            return False
        if not url.startswith(prefix):
            return False
        suffix = url[len(prefix):]
        parts = suffix.split('/', 1)
        if len(parts) != 2:
            return False
        (commit, path) = parts
        if len(commit) != 40:
            return False
        for char in commit:
            if char not in '0123456789abcdef':
                return False
        path_segments = path.split('/')
        if not path_segments:
            return False
        for segment in path_segments:
            if not self._is_canonical_raw_segment(segment):
                return False
        return True
    def _evidence_set_hash(self, candidate_source_url: str, ci_evidence_url: str, ci_evidence_id: str, audit_evidence_url: str, audit_evidence_id: str, assurance_manifest_hash: str, recovery_capsule_hash: str) -> str:
        return self._hash_text_parts([SCHEMA_VERSION, candidate_source_url, ci_evidence_url, ci_evidence_id, audit_evidence_url, audit_evidence_id, assurance_manifest_hash, recovery_capsule_hash])
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
    def _reserve_evidence_id(self, target: Address, issuer: str, kind: str, evidence_id: str) -> None:
        self._check_text(evidence_id, 'evidence_id', 8, MAX_ID_BYTES)
        reuse_key = self._hash_text_parts([str(target), issuer, kind, evidence_id])
        if self.used_evidence_ids.get(reuse_key, False):
            raise gl.vm.UserError('Evidence identifier has already been used')
        self.used_evidence_ids[reuse_key] = True
    def _repair_evidence(self, proposal_id: u256, candidate_source_url: str, ci_evidence_url: str, ci_evidence_id: str, audit_evidence_url: str, audit_evidence_id: str) -> None:
        proposal = self._require_proposal(proposal_id)
        policy = self._require_policy_owner(proposal.target)
        if proposal.status != STATUS_REPAIR:
            raise gl.vm.UserError('Evidence can only be replaced from EVIDENCE_REPAIR_REQUIRED')
        if self.now > int(proposal.expires_at):
            raise gl.vm.UserError('Proposal has expired')
        if not self._is_immutable_url(candidate_source_url, policy.source_prefix):
            raise gl.vm.UserError('Replacement candidate source URL is not approved and immutable')
        if not self._is_immutable_url(ci_evidence_url, policy.ci_prefix):
            raise gl.vm.UserError('Replacement CI evidence URL is not approved and immutable')
        if not self._is_immutable_url(audit_evidence_url, policy.audit_prefix):
            raise gl.vm.UserError('Replacement audit evidence URL is not approved and immutable')
        if ci_evidence_id == audit_evidence_id:
            raise gl.vm.UserError('CI and audit evidence identifiers must be distinct')
        self._reserve_evidence_id(proposal.target, policy.ci_authority, 'ci', ci_evidence_id)
        self._reserve_evidence_id(proposal.target, policy.audit_authority, 'audit', audit_evidence_id)
        proposal.candidate_source_url = candidate_source_url
        proposal.ci_evidence_url = ci_evidence_url
        proposal.ci_evidence_id = ci_evidence_id
        proposal.audit_evidence_url = audit_evidence_url
        proposal.audit_evidence_id = audit_evidence_id
        proposal.evidence_set_hash = self._evidence_set_hash(candidate_source_url, ci_evidence_url, ci_evidence_id, audit_evidence_url, audit_evidence_id, proposal.assurance_manifest_hash, proposal.recovery_capsule_hash)
        proposal.status = STATUS_PROPOSED
        proposal.last_review_code = ''

class ProofPatchRepairEngine(gl.Contract):
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

    def _load(self, logic: RepairPolicyLogic, data: dict[object, object]) -> None:
        operation = str(data.get('operation', ''))
        if operation != 'repair':
            raise gl.vm.UserError('Unknown repair policy operation')
        args = data['args']
        view = ProofPatchGovernor(self.governor).view(state=StorageType.LATEST_FINAL)

        def get(kind: str, key: str) -> dict[object, object]:
            return typing.cast(dict[object, object], json.loads(view.get_state_record(kind, key)))

        def flag(kind: str, key: str, destination: str) -> None:
            if get(kind, key).get('value', False):
                data[destination][key] = True

        def evidence_key(target: str, issuer: str, kind: str, evidence_id: str) -> str:
            return hashlib.sha256('\\x1f'.join([target, issuer, kind, evidence_id]).encode()).hexdigest()

        data['used_evidence_ids'] = {}
        data['proposal'] = get('proposal', str(int(args[0])))
        target = data['proposal']['target']
        data['policy'] = get('policy', target)
        policy = data['policy']
        for issuer, kind, evidence_id in ((policy['ci_authority'], 'ci', args[3]), (policy['audit_authority'], 'audit', args[5])):
            flag('evidence', evidence_key(target, issuer, kind, evidence_id), 'used_evidence_ids')

        logic.policies = {}
        logic.proposals = {}
        logic.used_evidence_ids = typing.cast(dict[object, bool], data['used_evidence_ids'])
        logic.proposal_count = u256(get('counts', '').get('proposal_count', 0))
        policy_record = self._record(TargetPolicy, data['policy'])
        proposal_record = self._record(UpgradeProposal, data['proposal'])
        logic.policies[policy_record.target] = policy_record
        logic.proposals[proposal_record.proposal_id] = proposal_record
        logic.actor = Address(data['actor'])
        logic.now = int(data['now'])

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
        if cls in (TargetPolicy, UpgradeProposal):
            value[1] = Address(value[1])
        if cls is TargetPolicy:
            value[0] = Address(value[0])
        else:
            value[2] = Address(value[2])
            if isinstance(value[8], str):
                value[8] = bytes.fromhex(value[8])
            if isinstance(value[20], str):
                value[20] = bytes.fromhex(value[20])
        return cls(**dict(zip(cls.__annotations__.keys(), value)))

    def _patch(self, logic: RepairPolicyLogic) -> dict[object, object]:
        result = {'operation': 'repair', 'policies': [], 'proposals': [], 'releases': [], 'incidents': [], 'active': [], 'used_evidence_ids': logic.used_evidence_ids, 'installed_candidate_hashes': {}, 'used_incident_ids': {}, 'proposal_count': int(logic.proposal_count)}
        for value in logic.policies.values():
            result['policies'].append(self._encode(value))
        for value in logic.proposals.values():
            result['proposals'].append(self._encode(value))
        return result

    @gl.public.write
    def execute(self, operation: str, request: str) -> None:
        if gl.message.sender_address != self.governor:
            raise gl.vm.UserError('Only the bound governor may execute repair policy logic')
        data = json.loads(request)
        data['operation'] = operation
        logic = RepairPolicyLogic()
        self._load(logic, data)
        logic._repair_evidence(*data['args'])
        ProofPatchGovernor(self.governor).emit(on='finalized').apply_policy_result(operation, json.dumps(self._patch(logic), separators=(',', ':')))
