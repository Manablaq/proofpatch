# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
from dataclasses import dataclass
import hashlib
import json
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
ZERO = '0x0000000000000000000000000000000000000000'

@gl.contract_interface
class ProofPatchTarget:

    class View:

        def proofpatch_installed_release_id(self) -> str:
            ...

        def proofpatch_release_mode(self) -> str:
            ...

@gl.contract_interface
class ProofPatchGovernor:

    class View:

        def get_state_record(self, kind: str, key: str) -> str:
            ...

    class Write:

        def apply_policy_result(self, operation: str, payload: str) -> None:
            ...

class ProofPatchRegistrationLogic:

    def _hash_text_parts(self, parts: list[str]) -> str:
        return hashlib.sha256('\x1f'.join(parts).encode('utf-8')).hexdigest()

    def _is_hex_hash(self, value: str) -> bool:
        if len(value) != 64:
            return False
        for char in value:
            if char not in '0123456789abcdef':
                return False
        return True

    def _check_text(self, value: str, label: str, minimum: int, maximum: int) -> None:
        encoded_len = len(value.encode('utf-8'))
        if encoded_len < minimum or encoded_len > maximum:
            raise gl.vm.UserError(f'{label} length is invalid')

    def _check_range(self, value: int, label: str, minimum: int, maximum: int) -> None:
        if value < minimum or value > maximum:
            raise gl.vm.UserError(f'{label} is outside supported bounds')

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

    def _policy_fingerprint(self, target: Address, owner: Address, constitution: str, source_authority: str, ci_authority: str, audit_authority: str, source_prefix: str, ci_prefix: str, audit_prefix: str, max_evidence_age_seconds: int, proposal_ttl_seconds: int, execution_timeout_seconds: int, assurance_authority: str, assurance_prefix: str, assurance_corroboration_authority: str, assurance_corroboration_prefix: str, proofpatch_kernel_hash: str, assurance_observation_delay_seconds: int, assurance_deadline_seconds: int, max_manifest_bytes: int, max_capsule_bytes: int) -> str:
        return self._hash_text_parts([SCHEMA_VERSION, str(target), str(owner), constitution, source_authority, ci_authority, audit_authority, source_prefix, ci_prefix, audit_prefix, str(max_evidence_age_seconds), str(proposal_ttl_seconds), str(execution_timeout_seconds), assurance_authority, assurance_prefix, assurance_corroboration_authority, assurance_corroboration_prefix, proofpatch_kernel_hash, str(assurance_observation_delay_seconds), str(assurance_deadline_seconds), str(max_manifest_bytes), str(max_capsule_bytes)])

    def _inactive_proposal(self) -> u256:
        return u256(0)

    def _lineage_hash(self, target: Address, previous_lineage_hash: str, release_id: str, parent_release_id: str, version: str, code_hash: str, policy_fingerprint: str, evidence_set_hash: str, assurance_manifest_hash: str, recovery_capsule_hash: str) -> str:
        return self._hash_text_parts([SCHEMA_VERSION, str(target), previous_lineage_hash, release_id, parent_release_id, version, code_hash, policy_fingerprint, evidence_set_hash, assurance_manifest_hash, recovery_capsule_hash])

    def _register_target(self, owner: str, constitution: str, source_authority: str, ci_authority: str, audit_authority: str, source_prefix: str, ci_prefix: str, audit_prefix: str, assurance_authority: str, assurance_prefix: str, assurance_corroboration_authority: str, assurance_corroboration_prefix: str, proofpatch_kernel_hash: str, current_version: str, current_source_url: str, current_code_hash: str, max_evidence_age_seconds: int, proposal_ttl_seconds: int, execution_timeout_seconds: int, assurance_observation_delay_seconds: int, assurance_deadline_seconds: int, max_manifest_bytes: int, max_capsule_bytes: int) -> None:
        """Register the calling target itself; caller address becomes target identity.

        The target should expose an owner-only registration method that emits this call
        to ProofPatch on finality. A contract cannot register another target address.
        """
        target = self.actor
        owner_address = Address(owner)
        if target in self.policies:
            raise gl.vm.UserError('Target is already registered; policy is immutable')
        if owner_address == Address('0x0000000000000000000000000000000000000000'):
            raise gl.vm.UserError('Owner cannot be the zero address')
        self._check_text(constitution, 'constitution', 80, MAX_CONSTITUTION_BYTES)
        self._check_text(source_authority, 'source_authority', 3, 160)
        self._check_text(ci_authority, 'ci_authority', 3, 160)
        self._check_text(audit_authority, 'audit_authority', 3, 160)
        self._check_text(assurance_authority, 'assurance_authority', 3, 160)
        self._check_text(assurance_corroboration_authority, 'assurance_corroboration_authority', 3, 160)
        self._check_text(current_version, 'current_version', 1, MAX_VERSION_BYTES)
        if len({source_authority, ci_authority, audit_authority, assurance_authority, assurance_corroboration_authority}) != 5:
            raise gl.vm.UserError('Publisher authorities must be distinct')
        if not self._is_authority_prefix(source_prefix):
            raise gl.vm.UserError('Invalid immutable source authority prefix')
        if not self._is_authority_prefix(ci_prefix):
            raise gl.vm.UserError('Invalid immutable CI authority prefix')
        if not self._is_authority_prefix(audit_prefix):
            raise gl.vm.UserError('Invalid immutable audit authority prefix')
        if not self._is_authority_prefix(assurance_prefix):
            raise gl.vm.UserError('Invalid immutable assurance authority prefix')
        if not self._is_authority_prefix(assurance_corroboration_prefix):
            raise gl.vm.UserError('Invalid immutable assurance corroboration prefix')
        if len({source_prefix, ci_prefix, audit_prefix, assurance_prefix, assurance_corroboration_prefix}) != 5:
            raise gl.vm.UserError('Publisher repositories must be distinct')
        if self._raw_github_owner(source_prefix).lower() == self._raw_github_owner(audit_prefix).lower():
            raise gl.vm.UserError('Independent audit authority must have a distinct GitHub publisher')
        if self._raw_github_owner(source_prefix).lower() == self._raw_github_owner(assurance_prefix).lower():
            raise gl.vm.UserError('Independent assurance authority must have a distinct GitHub publisher')
        if self._raw_github_owner(assurance_prefix).lower() == self._raw_github_owner(assurance_corroboration_prefix).lower():
            raise gl.vm.UserError('Independent assurance corroboration must have a distinct GitHub publisher')
        proofpatch_kernel_hash = proofpatch_kernel_hash.lower()
        if not self._is_hex_hash(proofpatch_kernel_hash):
            raise gl.vm.UserError('proofpatch_kernel_hash must be a lowercase SHA-256 hex digest')
        current_code_hash = current_code_hash.lower()
        if not self._is_hex_hash(current_code_hash):
            raise gl.vm.UserError('current_code_hash must be a lowercase SHA-256 hex digest')
        if not self._is_immutable_url(current_source_url, source_prefix):
            raise gl.vm.UserError('Current source must use the approved immutable commit URL')
        self._check_range(max_evidence_age_seconds, 'max_evidence_age_seconds', MIN_WINDOW_SECONDS, MAX_EVIDENCE_AGE_SECONDS)
        self._check_range(proposal_ttl_seconds, 'proposal_ttl_seconds', MIN_WINDOW_SECONDS, MAX_PROPOSAL_TTL_SECONDS)
        self._check_range(execution_timeout_seconds, 'execution_timeout_seconds', MIN_WINDOW_SECONDS, MAX_EXECUTION_TIMEOUT_SECONDS)
        self._check_range(assurance_observation_delay_seconds, 'assurance_observation_delay_seconds', MIN_WINDOW_SECONDS, MAX_EXECUTION_TIMEOUT_SECONDS)
        self._check_range(assurance_deadline_seconds, 'assurance_deadline_seconds', assurance_observation_delay_seconds, MAX_EXECUTION_TIMEOUT_SECONDS)
        self._check_range(max_manifest_bytes, 'max_manifest_bytes', 256, 128000)
        self._check_range(max_capsule_bytes, 'max_capsule_bytes', 1, MAX_CANDIDATE_BYTES)
        fingerprint = self._policy_fingerprint(target, owner_address, constitution, source_authority, ci_authority, audit_authority, source_prefix, ci_prefix, audit_prefix, max_evidence_age_seconds, proposal_ttl_seconds, execution_timeout_seconds, assurance_authority, assurance_prefix, assurance_corroboration_authority, assurance_corroboration_prefix, proofpatch_kernel_hash, assurance_observation_delay_seconds, assurance_deadline_seconds, max_manifest_bytes, max_capsule_bytes)
        self.policies[target] = TargetPolicy(owner=owner_address, target=target, constitution=constitution, policy_fingerprint=fingerprint, source_authority=source_authority, ci_authority=ci_authority, audit_authority=audit_authority, source_prefix=source_prefix, ci_prefix=ci_prefix, audit_prefix=audit_prefix, assurance_authority=assurance_authority, assurance_prefix=assurance_prefix, assurance_corroboration_authority=assurance_corroboration_authority, assurance_corroboration_prefix=assurance_corroboration_prefix, proofpatch_kernel_hash=proofpatch_kernel_hash, current_version=current_version, current_source_url=current_source_url, current_code_hash=current_code_hash, current_release_id='', max_evidence_age_seconds=u64(max_evidence_age_seconds), proposal_ttl_seconds=u64(proposal_ttl_seconds), execution_timeout_seconds=u64(execution_timeout_seconds), assurance_observation_delay_seconds=u64(assurance_observation_delay_seconds), assurance_deadline_seconds=u64(assurance_deadline_seconds), max_manifest_bytes=u64(max_manifest_bytes), max_capsule_bytes=u64(max_capsule_bytes), active=True)
        root_release_id = 'root-' + current_code_hash[:16]
        root_lineage_hash = self._lineage_hash(target, '', root_release_id, '', current_version, current_code_hash, fingerprint, '', '', '')
        self.releases[root_release_id] = ReleaseRecord(release_id=root_release_id, target=target, version=current_version, parent_release_id='', parent_code_hash='', source_url=current_source_url, code_hash=current_code_hash, proposal_id=u256(0), policy_fingerprint=fingerprint, evidence_set_hash='', assurance_manifest_hash='', recovery_capsule_hash='', installed_at=u64(self.now), certified_at=u64(self.now), status='REGISTERED_PARENT', recovered_from_release_id='', recovery_incident_id='', lineage_hash=root_lineage_hash)
        self.policies[target].current_release_id = root_release_id
        self.active_proposal_by_target[target] = self._inactive_proposal()

class ProofPatchRegistrationEngine(gl.Contract):
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

    def _load(self, logic, data):
        logic.policies = {}
        logic.proposals = {}
        logic.releases = {}
        logic.incidents = {}
        logic.active_proposal_by_target = {}
        logic.used_evidence_ids = {}
        logic.installed_candidate_hashes = {}
        logic.used_incident_ids = {}
        logic.proposal_count = u256(0)
        logic.release_count = u256(0)
        logic.actor = Address(data['actor'])
        logic.now = int(data['now'])
        logic.target_release_id = ''
        logic.target_mode = ''

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
            return {str(k): self._encode(v) for (k, v) in value.items()}
        if isinstance(value, list):
            return [self._encode(v) for v in value]
        if hasattr(value, '__dict__'):
            return {k: self._encode(v) for (k, v) in value.__dict__.items()}
        return value

    def _record(self, cls: object, raw: dict[object, object]) -> object:
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

    def _patch(self, logic: ProofPatchRegistrationLogic, operation: str, data: dict[object, object]) -> dict[object, object]:
        result = {'operation': operation, 'policies': [], 'proposals': [], 'releases': [], 'incidents': [], 'active': [], 'used_evidence_ids': logic.used_evidence_ids, 'installed_candidate_hashes': logic.installed_candidate_hashes, 'used_incident_ids': logic.used_incident_ids, 'proposal_count': int(logic.proposal_count), 'release_count': int(logic.release_count)}
        result['registration_target'] = str(logic.actor)
        for value in logic.policies.values():
            result['policies'].append(self._encode(value))
        for value in logic.proposals.values():
            result['proposals'].append(self._encode(value))
        for value in logic.releases.values():
            result['releases'].append(self._encode(value))
        for value in logic.incidents.values():
            result['incidents'].append(self._encode(value))
        for (key, value) in logic.active_proposal_by_target.items():
            result['active'].append([str(key), int(value)])
        return result

    @gl.public.write
    def execute(self, operation: str, request: str) -> None:
        if gl.message.sender_address != self.governor:
            raise gl.vm.UserError('Only the bound governor may execute policy logic')
        data = json.loads(request)
        data['operation'] = operation
        logic = ProofPatchRegistrationLogic()
        self._load(logic, data)
        args = data['args']
        if operation == 'register':
            logic._register_target(*args)
        else:
            raise gl.vm.UserError('Unknown policy operation')
        ProofPatchGovernor(self.governor).emit(on='finalized').apply_policy_result(operation, json.dumps(self._patch(logic, operation, data), separators=(',', ':')))
