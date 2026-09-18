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
class ProofPatchPolicyLogic:

    def _sha256_hex(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def _hash_text_parts(self, parts: list[str]) -> str:
        return hashlib.sha256('\x1f'.join(parts).encode('utf-8')).hexdigest()

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

    def _reserve_evidence_id(self, target: Address, issuer: str, kind: str, evidence_id: str) -> None:
        self._check_text(evidence_id, 'evidence_id', 8, MAX_ID_BYTES)
        reuse_key = self._hash_text_parts([str(target), issuer, kind, evidence_id])
        if self.used_evidence_ids.get(reuse_key, False):
            raise gl.vm.UserError('Evidence identifier has already been used')
        self.used_evidence_ids[reuse_key] = True

    def _installed_candidate_key(self, target: Address, candidate_hash: str) -> str:
        return self._hash_text_parts([str(target), candidate_hash])

    def _create_proposal(self, target: str, candidate_version: str, candidate_source_url: str, candidate_code: bytes, ci_evidence_url: str, ci_evidence_id: str, audit_evidence_url: str, audit_evidence_id: str, assurance_manifest: str, recovery_mode: str, recovery_release_id: str, recovery_version: str, recovery_source_url: str, recovery_code: bytes) -> u256:
        target_address = Address(target)
        policy = self._require_policy_owner(target_address)
        active = self.active_proposal_by_target.get(target_address, self._inactive_proposal())
        if active != self._inactive_proposal():
            raise gl.vm.UserError('Target already has an active proposal')
        self._check_text(candidate_version, 'candidate_version', 1, MAX_VERSION_BYTES)
        if candidate_version == policy.current_version:
            raise gl.vm.UserError('Candidate version must differ from current version')
        if len(candidate_code) == 0 or len(candidate_code) > MAX_CANDIDATE_BYTES:
            raise gl.vm.UserError('Candidate source bytes are empty or too large')
        if not self._is_immutable_url(candidate_source_url, policy.source_prefix):
            raise gl.vm.UserError('Candidate source URL is not an approved immutable source')
        if not self._is_immutable_url(ci_evidence_url, policy.ci_prefix):
            raise gl.vm.UserError('CI evidence URL is not an approved immutable source')
        if not self._is_immutable_url(audit_evidence_url, policy.audit_prefix):
            raise gl.vm.UserError('Audit evidence URL is not an approved immutable source')
        if not self._is_immutable_url(recovery_source_url, policy.source_prefix):
            raise gl.vm.UserError('Recovery source URL is not an approved immutable source')
        if ci_evidence_id == audit_evidence_id:
            raise gl.vm.UserError('CI and audit evidence identifiers must be distinct')
        if recovery_mode not in ('EXACT_PARENT', 'RECOVERY_CANDIDATE'):
            raise gl.vm.UserError('Unsupported recovery mode')
        if len(recovery_code) == 0 or len(recovery_code) > int(policy.max_capsule_bytes):
            raise gl.vm.UserError('Recovery capsule is empty or too large')
        self._check_text(recovery_version, 'recovery_version', 1, MAX_VERSION_BYTES)
        candidate_hash = self._sha256_hex(candidate_code)
        if candidate_hash == policy.current_code_hash:
            raise gl.vm.UserError('Candidate code is identical to current code')
        if self.installed_candidate_hashes.get(self._installed_candidate_key(target_address, candidate_hash), False):
            raise gl.vm.UserError('This candidate hash has already been installed for this target')
        recovery_hash = self._sha256_hex(recovery_code)
        if recovery_mode == 'EXACT_PARENT':
            if recovery_release_id != policy.current_release_id:
                raise gl.vm.UserError('EXACT_PARENT recovery must name the current certified release')
            if recovery_hash != policy.current_code_hash:
                raise gl.vm.UserError('EXACT_PARENT capsule bytes must match the current release')
            if recovery_version != policy.current_version:
                raise gl.vm.UserError('EXACT_PARENT capsule version must match the current release')
        else:
            if recovery_release_id != 'recovery-' + recovery_hash[:16]:
                raise gl.vm.UserError('Recovery candidate release ID must bind its capsule hash')
            if recovery_hash == candidate_hash:
                raise gl.vm.UserError('Recovery candidate must differ from the candidate')
        (assurance_manifest_hash, _) = self._canonical_json_hash(assurance_manifest)
        if assurance_manifest_hash in ('INVALID', 'NONCANONICAL'):
            raise gl.vm.UserError('Assurance manifest must be canonical JSON')
        manifest_error = self._validate_manifest(assurance_manifest, target_address, candidate_hash, policy.policy_fingerprint, policy.proofpatch_kernel_hash, policy)
        if manifest_error:
            raise gl.vm.UserError(manifest_error)
        self._reserve_evidence_id(target_address, policy.ci_authority, 'ci', ci_evidence_id)
        self._reserve_evidence_id(target_address, policy.audit_authority, 'audit', audit_evidence_id)
        now = self.now
        proposal_id = u256(int(self.proposal_count) + 1)
        evidence_set_hash = self._evidence_set_hash(candidate_source_url, ci_evidence_url, ci_evidence_id, audit_evidence_url, audit_evidence_id, assurance_manifest_hash, recovery_hash)
        self.proposals[proposal_id] = UpgradeProposal(proposal_id=proposal_id, target=target_address, proposer=policy.owner, parent_version=policy.current_version, parent_source_url=policy.current_source_url, parent_code_hash=policy.current_code_hash, candidate_version=candidate_version, candidate_source_url=candidate_source_url, candidate_code=candidate_code, candidate_code_hash=candidate_hash, ci_evidence_url=ci_evidence_url, ci_evidence_id=ci_evidence_id, audit_evidence_url=audit_evidence_url, audit_evidence_id=audit_evidence_id, assurance_manifest=assurance_manifest, assurance_manifest_hash=assurance_manifest_hash, recovery_mode=recovery_mode, recovery_release_id=recovery_release_id, recovery_version=recovery_version, recovery_source_url=recovery_source_url, recovery_code=recovery_code, recovery_code_hash=recovery_hash, recovery_capsule_hash=recovery_hash, evidence_set_hash=evidence_set_hash, policy_fingerprint=policy.policy_fingerprint, created_at=u64(now), expires_at=u64(now + int(policy.proposal_ttl_seconds)), reviewed_at=u64(0), execution_deadline=u64(0), status=STATUS_PROPOSED, last_review_code='')
        self.proposal_count = proposal_id
        self.active_proposal_by_target[target_address] = proposal_id
        return proposal_id

class ProofPatchPolicyEngine(gl.Contract):
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

    def _load(self, logic: ProofPatchPolicyLogic, data: dict[object, object]) -> None:
        if str(data.get('operation', '')) != 'create':
            raise gl.vm.UserError('Unknown policy operation')
        args = data['args']
        args[3] = bytes.fromhex(args[3])
        args[13] = bytes.fromhex(args[13])
        view = ProofPatchGovernor(self.governor).view(state=StorageType.LATEST_FINAL)

        def get(kind: str, key: str) -> dict[object, object]:
            return typing.cast(dict[object, object], json.loads(view.get_state_record(kind, key)))

        def flag(kind: str, key: str, destination: str) -> None:
            if get(kind, key).get('value', False):
                data[destination][key] = True

        def evidence_key(target: str, issuer: str, kind: str, evidence_id: str) -> str:
            return hashlib.sha256('\\x1f'.join([target, issuer, kind, evidence_id]).encode()).hexdigest()

        target = str(args[0])
        data['policy'] = get('policy', target)
        active = get('active', target)
        data['active_target'] = target
        data['active_value'] = active.get('value', 0)
        data['used_evidence_ids'] = {}
        data['installed_candidate_hashes'] = {}
        policy = data['policy']
        flag('evidence', evidence_key(target, policy['ci_authority'], 'ci', args[5]), 'used_evidence_ids')
        flag('evidence', evidence_key(target, policy['audit_authority'], 'audit', args[7]), 'used_evidence_ids')
        candidate_hash = hashlib.sha256(args[3]).hexdigest()
        flag('candidate', hashlib.sha256('\\x1f'.join([target, candidate_hash]).encode()).hexdigest(), 'installed_candidate_hashes')

        logic.policies = {}
        logic.proposals = {}
        logic.active_proposal_by_target = {}
        logic.used_evidence_ids = typing.cast(dict[object, bool], data['used_evidence_ids'])
        logic.installed_candidate_hashes = typing.cast(dict[object, bool], data['installed_candidate_hashes'])
        logic.proposal_count = u256(get('counts', '').get('proposal_count', 0))
        policy_record = self._record(TargetPolicy, data['policy'])
        logic.policies[policy_record.target] = policy_record
        if data.get('active_target') is not None:
            logic.active_proposal_by_target[Address(data['active_target'])] = u256(data.get('active_value', 0))
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
        value[1] = Address(value[1])
        if cls is TargetPolicy:
            value[0] = Address(value[0])
        return cls(**dict(zip(cls.__annotations__.keys(), value)))

    def _patch(self, logic: ProofPatchPolicyLogic) -> dict[object, object]:
        result = {'operation': 'create', 'policies': [], 'proposals': [], 'releases': [], 'incidents': [], 'active': [], 'used_evidence_ids': logic.used_evidence_ids, 'installed_candidate_hashes': logic.installed_candidate_hashes, 'used_incident_ids': {}, 'proposal_count': int(logic.proposal_count)}
        for value in logic.policies.values():
            result['policies'].append(self._encode(value))
        for target, value in logic.active_proposal_by_target.items():
            result['active'].append([str(target), int(value)])
        return result

    @gl.public.write
    def execute(self, operation: str, request: str) -> None:
        if gl.message.sender_address != self.governor:
            raise gl.vm.UserError('Only the bound governor may execute policy logic')
        if operation != 'create':
            raise gl.vm.UserError('Unknown policy operation')
        data = json.loads(request)
        data['operation'] = operation
        logic = ProofPatchPolicyLogic()
        self._load(logic, data)
        logic._create_proposal(*data['args'])
        ProofPatchGovernor(self.governor).emit(on='finalized').apply_policy_result(operation, json.dumps(self._patch(logic), separators=(',', ':')))
