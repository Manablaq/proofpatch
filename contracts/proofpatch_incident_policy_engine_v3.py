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
class IncidentPolicyLogic:
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
    def _require_policy_owner(self, target: Address) -> TargetPolicy:
        if target not in self.policies:
            raise gl.vm.UserError('Target is not registered')
        policy = self.policies[target]
        if self.actor != policy.owner:
            raise gl.vm.UserError('Only the registered target owner may perform this action')
        if not policy.active:
            raise gl.vm.UserError('Target policy is inactive')
        return policy
    def _reserve_evidence_id(self, target: Address, issuer: str, kind: str, evidence_id: str) -> None:
        self._check_text(evidence_id, 'evidence_id', 8, MAX_ID_BYTES)
        reuse_key = self._hash_text_parts([str(target), issuer, kind, evidence_id])
        if self.used_evidence_ids.get(reuse_key, False):
            raise gl.vm.UserError('Evidence identifier has already been used')
        self.used_evidence_ids[reuse_key] = True

    def _open_incident(self, target: str, release_id: str, incident_type: str, primary_url: str, primary_evidence_id: str, corroboration_url: str, corroboration_evidence_id: str) -> str:
        target_address = Address(target)
        if target_address not in self.policies or release_id not in self.releases:
            raise gl.vm.UserError('Unknown target or release')
        release = self.releases[release_id]
        if release.target != target_address:
            raise gl.vm.UserError('Incident release belongs to another target')
        if incident_type not in ('STATE_INVARIANT_VIOLATION', 'AUTHORIZATION_REGRESSION', 'UPGRADE_BYPASS', 'CONSENSUS_BINDING_REGRESSION', 'EVIDENCE_TRUST_REGRESSION', 'FINALITY_REGRESSION', 'LIVENESS_REGRESSION', 'HIDDEN_VALUE_TRANSFER', 'KERNEL_INTEGRITY_FAILURE', 'REQUIRED_INTERFACE_FAILURE', 'OTHER_CONSTITUTIONAL_BREACH'):
            raise gl.vm.UserError('Unsupported incident type')
        policy = self.policies[target_address]
        if not self._is_immutable_url(primary_url, policy.audit_prefix):
            raise gl.vm.UserError('Incident primary evidence URL is not approved and immutable')
        if not self._is_immutable_url(corroboration_url, policy.assurance_corroboration_prefix):
            raise gl.vm.UserError('Incident corroboration URL is not approved and immutable')
        if primary_evidence_id == corroboration_evidence_id:
            raise gl.vm.UserError('Incident evidence identifiers must be distinct')
        self._reserve_evidence_id(target_address, policy.audit_authority, 'incident_primary', primary_evidence_id)
        self._reserve_evidence_id(target_address, policy.assurance_corroboration_authority, 'incident_corroboration', corroboration_evidence_id)
        if self.target_release_id != release_id:
            raise gl.vm.UserError("Incident release is not the target's finalized release")
        if self.target_mode not in (MODE_ACTIVE, MODE_PROVISIONAL, MODE_RECOVERED):
            raise gl.vm.UserError('Incident target is not in a challengeable release mode')
        if release.recovery_capsule_hash == '':
            raise gl.vm.UserError('Release has no precommitted recovery capsule')
        if release.status not in (STATUS_CERTIFIED, STATUS_INSTALLED_PROVISIONAL, STATUS_ASSURANCE_PENDING, STATUS_ASSURANCE_REPAIR, STATUS_ASSURANCE_RETRY, STATUS_INCIDENT_OPEN):
            raise gl.vm.UserError('Release is not challengeable in its current lifecycle state')
        incident_id = 'incident-' + str(self.now) + '-' + primary_evidence_id
        if incident_id in self.incidents:
            raise gl.vm.UserError('Incident identifier already exists')
        incident_replay_key = self._hash_text_parts([str(target_address), release_id, primary_evidence_id, corroboration_evidence_id])
        if self.used_incident_ids.get(incident_replay_key, False):
            raise gl.vm.UserError('Incident evidence has already been used for this release')
        self.used_incident_ids[incident_replay_key] = True
        self.incidents[incident_id] = IncidentRecord(incident_id=incident_id, target=target_address, release_id=release_id, installed_code_hash=release.code_hash, incident_type=incident_type, primary_url=primary_url, primary_evidence_id=primary_evidence_id, corroboration_url=corroboration_url, corroboration_evidence_id=corroboration_evidence_id, policy_fingerprint=release.policy_fingerprint, assurance_manifest_hash=release.assurance_manifest_hash, recovery_capsule_hash=release.recovery_capsule_hash, opened_at=u64(self.now), expires_at=u64(self.now + int(policy.proposal_ttl_seconds)), reviewed_at=u64(0), recovery_deadline=u64(0), status=STATUS_INCIDENT_OPEN, last_review_code='', recovery_authorized=False)
        release.status = STATUS_INCIDENT_OPEN
        return incident_id

    def _repair_incident(self, incident_id: str, primary_url: str, primary_evidence_id: str, corroboration_url: str, corroboration_evidence_id: str) -> None:
        if incident_id not in self.incidents:
            raise gl.vm.UserError('Unknown incident')
        incident = self.incidents[incident_id]
        policy = self._require_policy_owner(incident.target)
        if incident.status not in (STATUS_INCIDENT_REPAIR, STATUS_INCIDENT_RETRY):
            raise gl.vm.UserError('Incident evidence can only be replaced after a repairable review result')
        if self.now > int(incident.expires_at):
            raise gl.vm.UserError('Incident review window has expired')
        if not self._is_immutable_url(primary_url, policy.audit_prefix):
            raise gl.vm.UserError('Replacement incident primary URL is not approved and immutable')
        if not self._is_immutable_url(corroboration_url, policy.assurance_corroboration_prefix):
            raise gl.vm.UserError('Replacement incident corroboration URL is not approved and immutable')
        if primary_evidence_id == corroboration_evidence_id:
            raise gl.vm.UserError('Incident evidence identifiers must be distinct')
        self._reserve_evidence_id(incident.target, policy.audit_authority, 'incident_primary', primary_evidence_id)
        self._reserve_evidence_id(incident.target, policy.assurance_corroboration_authority, 'incident_corroboration', corroboration_evidence_id)
        incident.primary_url = primary_url
        incident.primary_evidence_id = primary_evidence_id
        incident.corroboration_url = corroboration_url
        incident.corroboration_evidence_id = corroboration_evidence_id
        incident.reviewed_at = u64(0)
        incident.last_review_code = ''
        incident.status = STATUS_INCIDENT_OPEN
        self.releases[incident.release_id].status = STATUS_INCIDENT_OPEN

class IncidentPolicyEngine(gl.Contract):
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

    def _load(self, logic: IncidentPolicyLogic, data: dict[object, object]) -> None:
        operation = str(data.get('operation', ''))
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
        data['used_incident_ids'] = {}
        if operation == 'incident':
            target = str(args[0])
            release_id = str(args[1])
            data['policy'] = get('policy', target)
            data['releases'] = [get('release', release_id)]
            policy = data['policy']
            for issuer, kind, evidence_id in ((policy['audit_authority'], 'incident_primary', args[4]), (policy['assurance_corroboration_authority'], 'incident_corroboration', args[6])):
                flag('evidence', evidence_key(target, issuer, kind, evidence_id), 'used_evidence_ids')
            replay_key = hashlib.sha256('\\x1f'.join([target, release_id, args[4], args[6]]).encode()).hexdigest()
            flag('incident_evidence', replay_key, 'used_incident_ids')
            target_view = ProofPatchTarget(Address(target)).view(state=StorageType.LATEST_FINAL)
            data['target_release_id'] = target_view.proofpatch_installed_release_id()
            data['target_mode'] = target_view.proofpatch_release_mode()
        elif operation == 'repair_incident':
            data['incident'] = get('incident', str(args[0]))
            target = data['incident']['target']
            data['policy'] = get('policy', target)
            data['releases'] = [get('release', data['incident']['release_id'])]
            policy = data['policy']
            for issuer, kind, evidence_id in ((policy['audit_authority'], 'incident_primary', args[2]), (policy['assurance_corroboration_authority'], 'incident_corroboration', args[4])):
                flag('evidence', evidence_key(target, issuer, kind, evidence_id), 'used_evidence_ids')
        else:
            raise gl.vm.UserError('Unknown incident policy operation')

        logic.policies = {}
        logic.releases = {}
        logic.incidents = {}
        logic.used_evidence_ids = typing.cast(dict[object, bool], data['used_evidence_ids'])
        logic.used_incident_ids = typing.cast(dict[object, bool], data['used_incident_ids'])
        if data.get('policy') is not None:
            policy = self._record(TargetPolicy, data['policy'])
            logic.policies[policy.target] = policy
        for raw in typing.cast(list[dict[object, object]], data.get('releases', [])):
            release = self._record(ReleaseRecord, raw)
            logic.releases[release.release_id] = release
        if data.get('incident') is not None:
            incident = self._record(IncidentRecord, data['incident'])
            logic.incidents[incident.incident_id] = incident
        logic.actor = Address(data['actor'])
        logic.now = int(data['now'])
        logic.target_release_id = str(data.get('target_release_id', ''))
        logic.target_mode = str(data.get('target_mode', ''))

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
        if cls in (TargetPolicy, ReleaseRecord, IncidentRecord):
            value[1] = Address(value[1])
        if cls is TargetPolicy:
            value[0] = Address(value[0])
        return cls(**dict(zip(cls.__annotations__.keys(), value)))

    def _patch(self, logic: IncidentPolicyLogic, operation: str) -> dict[object, object]:
        result = {'operation': operation, 'policies': [], 'proposals': [], 'releases': [], 'incidents': [], 'active': [], 'used_evidence_ids': logic.used_evidence_ids, 'installed_candidate_hashes': {}, 'used_incident_ids': logic.used_incident_ids, 'proposal_count': 0}
        for value in logic.policies.values():
            result['policies'].append(self._encode(value))
        for value in logic.releases.values():
            result['releases'].append(self._encode(value))
        for value in logic.incidents.values():
            result['incidents'].append(self._encode(value))
        return result

    @gl.public.write
    def execute(self, operation: str, request: str) -> None:
        if gl.message.sender_address != self.governor:
            raise gl.vm.UserError('Only the bound governor may execute incident policy logic')
        if operation not in ('incident', 'repair_incident'):
            raise gl.vm.UserError('Unknown incident policy operation')
        data = json.loads(request)
        data['operation'] = operation
        logic = IncidentPolicyLogic()
        self._load(logic, data)
        args = data['args']
        if operation == 'incident':
            logic._open_incident(*args)
        else:
            logic._repair_incident(*args)
        ProofPatchGovernor(self.governor).emit(on='finalized').apply_policy_result(operation, json.dumps(self._patch(logic, operation), separators=(',', ':')))
