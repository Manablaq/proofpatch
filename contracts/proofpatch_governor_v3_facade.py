# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownParameterType=false, reportMissingParameterType=false, reportInvalidTypeForm=false, reportOptionalMemberAccess=false, reportUnboundVariable=false, reportOptionalSubscript=false, reportGeneralTypeIssues=false, reportAssignmentType=false, reportIndexIssue=false, reportCallIssue=false, reportUnnecessaryCast=false, reportPrivateUsage=false, reportUnusedFunction=false, reportUnusedImport=false
from genlayer import *
from dataclasses import dataclass
from datetime import datetime
from genlayer.py.public_abi import StorageType
import json
REVIEW_ENGINE = '0x9840cCf5DBdf4AE5945Ca73367e8336cCBEF578e'
ASSURANCE_REVIEW_ENGINE = '0x32E5eFAF7558B65f72dA2B2B27f040e74fA148BC'

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

SERIAL_FIELDS = {'TargetPolicy':'owner,target,constitution,policy_fingerprint,source_authority,ci_authority,audit_authority,source_prefix,ci_prefix,audit_prefix,assurance_authority,assurance_prefix,assurance_corroboration_authority,assurance_corroboration_prefix,proofpatch_kernel_hash,current_version,current_source_url,current_code_hash,current_release_id,max_evidence_age_seconds,proposal_ttl_seconds,execution_timeout_seconds,assurance_observation_delay_seconds,assurance_deadline_seconds,max_manifest_bytes,max_capsule_bytes,active'.split(','),'UpgradeProposal':'proposal_id,target,proposer,parent_version,parent_source_url,parent_code_hash,candidate_version,candidate_source_url,candidate_code,candidate_code_hash,ci_evidence_url,ci_evidence_id,audit_evidence_url,audit_evidence_id,assurance_manifest,assurance_manifest_hash,recovery_mode,recovery_release_id,recovery_version,recovery_source_url,recovery_code,recovery_code_hash,recovery_capsule_hash,evidence_set_hash,policy_fingerprint,created_at,expires_at,reviewed_at,execution_deadline,status,last_review_code'.split(','),'ReleaseRecord':'release_id,target,version,parent_release_id,parent_code_hash,source_url,code_hash,proposal_id,policy_fingerprint,evidence_set_hash,assurance_manifest_hash,recovery_capsule_hash,installed_at,certified_at,status,recovered_from_release_id,recovery_incident_id,lineage_hash'.split(','),'IncidentRecord':'incident_id,target,release_id,installed_code_hash,incident_type,primary_url,primary_evidence_id,corroboration_url,corroboration_evidence_id,policy_fingerprint,assurance_manifest_hash,recovery_capsule_hash,opened_at,expires_at,reviewed_at,recovery_deadline,status,last_review_code,recovery_authorized'.split(',')}


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
POLICY_ENGINE = '0xCe91B262d6358dFd95A32a56fd577b71FB0DdC7F'
INCIDENT_POLICY_ENGINE = '0x3De9294a39A4b9e31975a74426a3f29C32E0829E'
REPAIR_POLICY_ENGINE = '0x59A065F97a4d475Fc60AC350aDF5163AbfE27F91'
REGISTRATION_ENGINE = '0xF7e1F1D31f60e866E2f0a1367834BEF7abC77b43'
ASSURANCE_ENGINE = '0x6740374AA335c4e02EC079d3d1E5A2198A28320F'
SUMMARY_ENGINE = '0x209343F604Ec7A53339C3F555D5Cf333F4BEf4FD'
INSTALL_LIFECYCLE_ENGINE = '0xE7F337c2Bc992a94f213C41B66d7E49381F31145'
TIMEOUT_LIFECYCLE_ENGINE = '0xd73FF76b1A2438eAD59DA4072F9484aED25C7865'
ACTIVATION_LIFECYCLE_ENGINE = '0x429A733D5949bCB0DE97E32Da58E8d192acC41Ca'
RECOVERY_LIFECYCLE_ENGINE = '0xebf47F06759481606910dA564FF48203e386b95E'
LIFECYCLE_REQUEST_ENGINE = '0xC01B9D36B3eEe2A563A4E7FA688b9a799fa759E2'

@gl.contract_interface
class ProofPatchPolicyEngine:

    class Write:

        def execute(self, operation: str, request: str) -> None:
            ...

@gl.contract_interface
class ProofPatchSummaryEngine:

    class View:

        def read(self, kind: str, key: str) -> str:
            ...

REVIEW_COMMIT_ENGINE = '0xef8F5C807117b2A606B861e947F2ff5756Db8CE7'
REVIEW_REQUEST_ENGINE = '0x50d787E2078683Bbc27462208475578cE7295aF9'
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

    def _engine(self):
        return ProofPatchReviewEngine(Address(REVIEW_ENGINE))

    def _fact_engine(self):
        return ProofPatchReviewEngine(Address(ASSURANCE_REVIEW_ENGINE))

    def _summary(self, kind: str, key: str) -> str:
        return ProofPatchSummaryEngine(Address(SUMMARY_ENGINE)).view(state=StorageType.LATEST_FINAL).read(kind, str(key))

    @gl.public.write
    def review_proposal(self, proposal_id: u256) -> None:
        if gl.message.sender_address == Address(REVIEW_ENGINE):
            self._submit_review('proposal', [proposal_id], str(gl.message.sender_address))
            return
        self._submit_review_request('proposal', [proposal_id])

    @gl.public.view
    def is_upgrade_authorized(self, proposal_id: u256, target: str, candidate_hash: str) -> bool:
        return self._summary('is_upgrade_authorized', json.dumps([int(proposal_id), target, candidate_hash], separators=(',', ':'))) == '1'

    @gl.public.view
    def get_candidate_code(self, proposal_id: u256) -> bytes:
        return bytes.fromhex(self._summary('candidate_code', str(int(proposal_id))))

    @gl.public.view
    def is_activation_authorized(self, proposal_id: u256, release_id: str, candidate_hash: str) -> bool:
        return self._summary('is_activation_authorized', json.dumps([int(proposal_id), release_id, candidate_hash], separators=(',', ':'))) == '1'

    @gl.public.view
    def is_registration_authorized(self, target: str, release_id: str, code_hash: str) -> bool:
        return self._summary('is_registration_authorized', json.dumps([target, release_id, code_hash], separators=(',', ':'))) == '1'

    @gl.public.write
    def review_incident(self, incident_id: str) -> None:
        if gl.message.sender_address == Address(ASSURANCE_REVIEW_ENGINE):
            self._submit_review('incident', [incident_id], str(gl.message.sender_address))
            return
        self._submit_review_request('incident', [incident_id])

    @gl.public.view
    def is_recovery_authorized(self, incident_id: str, release_id: str, recovery_hash: str) -> bool:
        return self._summary('is_recovery_authorized', json.dumps([incident_id, release_id, recovery_hash], separators=(',', ':'))) == '1'

    @gl.public.view
    def get_recovery_release_id(self, incident_id: str) -> str:
        return self._summary('recovery_release_id', incident_id)

    @gl.public.view
    def get_recovery_code(self, incident_id: str) -> bytes:
        return bytes.fromhex(self._summary('recovery_code', incident_id))

    @gl.public.view
    def get_proposal_count(self) -> u256:
        return u256(int(self._summary('proposal_count', '')))

    @gl.public.view
    def get_proposal_status(self, proposal_id: u256) -> str:
        return self._summary('proposal_status', str(int(proposal_id)))

    @gl.public.view
    def get_candidate_hash(self, proposal_id: u256) -> str:
        return self._summary('candidate_hash', str(int(proposal_id)))

    @gl.public.view
    def get_proposal_release_id(self, proposal_id: u256) -> str:
        return self._summary('proposal_release_id', str(int(proposal_id)))

    @gl.public.view
    def get_evidence_set_hash(self, proposal_id: u256) -> str:
        return self._summary('evidence_set_hash', str(int(proposal_id)))

    @gl.public.view
    def get_policy_fingerprint(self, target: str) -> str:
        return self._summary('policy_fingerprint', target)

    @gl.public.view
    def get_policy_kernel_hash(self, target: str) -> str:
        return self._summary('policy_kernel_hash', target)

    @gl.public.view
    def get_current_code_hash(self, target: str) -> str:
        return self._summary('current_code_hash', target)

    @gl.public.view
    def get_current_version(self, target: str) -> str:
        return self._summary('current_version', target)

    @gl.public.view
    def get_current_release_id(self, target: str) -> str:
        return self._summary('current_release_id', target)

    @gl.public.view
    def get_active_proposal(self, target: str) -> u256:
        return u256(int(self._summary('active_proposal', target)))

    @gl.public.view
    def get_proposal_summary(self, proposal_id: u256) -> str:
        return self._summary('proposal_summary', str(int(proposal_id)))

    @gl.public.view
    def get_release_summary(self, release_id: str) -> str:
        return self._summary('release_summary', release_id)

    @gl.public.view
    def get_incident_summary(self, incident_id: str) -> str:
        return self._summary('incident_summary', incident_id)

    @gl.public.view
    def get_state_record(self, kind: str, key: str) -> str:
        key = str(key)
        if kind == 'policy':
            value = self.policies.get(Address(key), None)
        elif kind == 'proposal':
            value = self.proposals.get(u256(int(key)), None)
        elif kind == 'release':
            value = self.releases.get(key, None)
        elif kind == 'incident':
            value = self.incidents.get(key, None)
        elif kind == 'active':
            value = {'value': self.active_proposal_by_target.get(Address(key), u256(0))}
        elif kind == 'counts':
            value = {'proposal_count': self.proposal_count, 'release_count': self.release_count}
        elif kind in ('evidence', 'candidate', 'incident_evidence'):
            value = {'value': bool(self.used_evidence_ids.get(key, False) if kind == 'evidence' else self.installed_candidate_hashes.get(key, False) if kind == 'candidate' else self.used_incident_ids.get(key, False))}
        else:
            raise gl.vm.UserError('Unknown state record')
        if value is None:
            return json.dumps({'status': 'UNKNOWN'}, separators=(',', ':'))
        return json.dumps(self._encode(value), separators=(',', ':'))

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
            fields = SERIAL_FIELDS['TargetPolicy'] if isinstance(value, TargetPolicy) else SERIAL_FIELDS['UpgradeProposal'] if isinstance(value, UpgradeProposal) else SERIAL_FIELDS['ReleaseRecord'] if isinstance(value, ReleaseRecord) else SERIAL_FIELDS['IncidentRecord'] if isinstance(value, IncidentRecord) else None
            if fields is not None:
                return {key: self._encode(raw) for (key, raw) in zip(fields, value.__dict__.values())}
            return {k: self._encode(v) for (k, v) in value.__dict__.items()}
        return value

    def _record(self, cls: object, raw: dict[object, object]) -> object:
        value = list(raw.values())
        value[1] = Address(value[1])
        if cls is TargetPolicy:
            value[0] = Address(value[0])
        elif cls is UpgradeProposal:
            value[2] = Address(value[2])
            if isinstance(value[8], str): value[8] = bytes.fromhex(value[8])
            if isinstance(value[20], str): value[20] = bytes.fromhex(value[20])
        return cls(**dict(zip(cls.__annotations__.keys(), value)))

    def _apply_patch(self, payload: str) -> dict[object, object]:
        patch = json.loads(payload)
        for (kind, cls, store, field) in (('policies', TargetPolicy, self.policies, 'target'), ('proposals', UpgradeProposal, self.proposals, 'proposal_id'), ('releases', ReleaseRecord, self.releases, 'release_id'), ('incidents', IncidentRecord, self.incidents, 'incident_id')):
            for raw in patch.get(kind, []):
                value = self._record(cls, raw)
                store[getattr(value, field)] = value
        for (target, value) in patch.get('active', []):
            self.active_proposal_by_target[Address(target)] = u256(value)
        for (kind, store) in (('used_evidence_ids', self.used_evidence_ids), ('installed_candidate_hashes', self.installed_candidate_hashes), ('used_incident_ids', self.used_incident_ids)):
            for (key, value) in patch.get(kind, {}).items():
                store[key] = bool(value)
        if 'proposal_count' in patch:
            self.proposal_count = u256(patch['proposal_count'])
        if 'release_count' in patch:
            self.release_count = u256(patch['release_count'])
        return patch

    def _submit_policy(self, operation: str, args: list[object], actor: str, **fields: object) -> None:
        data = {'args': self._encode(args), 'actor': actor, 'now': self._now()}
        for (key, value) in fields.items():
            data[key] = self._encode(value)
        if operation == 'register':
            address = REGISTRATION_ENGINE
        elif operation == 'assure':
            address = ASSURANCE_ENGINE
        elif operation in ('incident', 'repair_incident'):
            address = INCIDENT_POLICY_ENGINE
        elif operation == 'repair':
            address = REPAIR_POLICY_ENGINE
        else:
            address = POLICY_ENGINE
        ProofPatchPolicyEngine(Address(address)).emit(on='finalized').execute(operation, json.dumps(data, sort_keys=True, separators=(',', ':')))

    def _submit_lifecycle(self, operation: str, args: list[object], actor: str, **fields: object) -> None:
        data = {'args': self._encode(args), 'actor': actor, 'now': self._now()}
        for (key, value) in fields.items():
            data[key] = self._encode(value)
        ProofPatchPolicyEngine(Address(LIFECYCLE_REQUEST_ENGINE)).emit(on='finalized').execute(operation, json.dumps(data, sort_keys=True, separators=(',', ':')))

    def _submit_review_request(self, operation: str, args: list[object]) -> None:
        request = {'args': self._encode(args), 'now': self._now()}
        ProofPatchPolicyEngine(Address(REVIEW_REQUEST_ENGINE)).emit(on='finalized').execute(operation, json.dumps(request, separators=(',', ':')))

    def _submit_review(self, operation: str, args: list[object], actor: str, **fields: object) -> None:
        data = {'args': self._encode(args), 'actor': actor, 'now': self._now()}
        for (key, value) in fields.items():
            data[key] = self._encode(value)
        ProofPatchPolicyEngine(Address(REVIEW_COMMIT_ENGINE)).emit(on='finalized').execute(operation, json.dumps(data, sort_keys=True, separators=(',', ':')))

    def _emit_actions(self, actions: list[object]) -> None:
        for action in actions:
            kind = action.get('kind')
            args = action.get('args', [])
            if kind == 'upgrade':
                ProofPatchTarget(Address(args[0])).emit(on='finalized').proofpatch_upgrade(u256(args[1]), args[2])
            elif kind == 'activate':
                ProofPatchTarget(Address(args[0])).emit(on='finalized').proofpatch_activate(args[1], args[2])
            elif kind == 'recover':
                ProofPatchTarget(self.incidents[args[0]].target).emit(on='finalized').proofpatch_recover(args[0], args[1], args[2])
            else:
                raise gl.vm.UserError('Unknown finalized action')

    @gl.public.write
    def apply_review_request(self, operation: str, request: str) -> None:
        if gl.message.sender_address != Address(REVIEW_REQUEST_ENGINE):
            raise gl.vm.UserError('Only review request engine may start review')
        data = json.loads(request)
        args = data['args']
        patch = data.get('patch', {})
        if patch:
            self._apply_patch(json.dumps(patch, separators=(',', ':')))
        snapshot = data['snapshot']
        if operation == 'proposal':
            self._engine().emit(on='finalized').review_proposal(u256(args[0]), snapshot)
        elif operation == 'assurance':
            self._fact_engine().emit(on='finalized').assure_release(u256(args[0]), snapshot)
        elif operation == 'incident':
            self._fact_engine().emit(on='finalized').review_incident(args[0], snapshot)
        else:
            raise gl.vm.UserError('Unknown review request')

    @gl.public.write
    def apply_review_result(self, operation: str, payload: str) -> None:
        if gl.message.sender_address != Address(REVIEW_COMMIT_ENGINE):
            raise gl.vm.UserError('Only review commit engine may apply state')
        patch = self._apply_patch(payload)
        self._emit_actions(patch.get('actions', []))

    @gl.public.write
    def apply_policy_result(self, operation: str, payload: str) -> None:
        if gl.message.sender_address not in (Address(POLICY_ENGINE), Address(INCIDENT_POLICY_ENGINE), Address(REPAIR_POLICY_ENGINE), Address(REGISTRATION_ENGINE), Address(ASSURANCE_ENGINE)):
            raise gl.vm.UserError('Only a bound policy engine may apply state')
        patch = self._apply_patch(payload)
        if operation == 'register':
            target = Address(patch['registration_target'])
            p = self.policies[target]
            ProofPatchTarget(target).emit(on='finalized').proofpatch_confirm_registration(p.current_release_id, p.current_code_hash)
        elif operation == 'assure':
            review = patch.get('review', {})
            self._submit_review_request('assurance', [review['proposal_id'], review['primary_url'], review['primary_evidence_id'], review['corroboration_url'], review['corroboration_evidence_id']])

    @gl.public.write
    def apply_lifecycle_result(self, operation: str, payload: str) -> None:
        if gl.message.sender_address not in (Address(INSTALL_LIFECYCLE_ENGINE), Address(TIMEOUT_LIFECYCLE_ENGINE), Address(ACTIVATION_LIFECYCLE_ENGINE), Address(RECOVERY_LIFECYCLE_ENGINE)):
            raise gl.vm.UserError('Only a bound lifecycle engine may apply state')
        patch = self._apply_patch(payload)
        for action in patch.get('actions', []):
            if action.get('kind') == 'recover':
                args = action['args']
                ProofPatchTarget(self.incidents[args[0]].target).emit(on='finalized').proofpatch_recover(args[0], args[1], args[2])
            else:
                raise gl.vm.UserError('Unknown lifecycle action')

    @gl.public.write
    def register_target(self, owner: str, constitution: str, source_authority: str, ci_authority: str, audit_authority: str, source_prefix: str, ci_prefix: str, audit_prefix: str, assurance_authority: str, assurance_prefix: str, assurance_corroboration_authority: str, assurance_corroboration_prefix: str, proofpatch_kernel_hash: str, current_version: str, current_source_url: str, current_code_hash: str, max_evidence_age_seconds: u64, proposal_ttl_seconds: u64, execution_timeout_seconds: u64, assurance_observation_delay_seconds: u64, assurance_deadline_seconds: u64, max_manifest_bytes: u64, max_capsule_bytes: u64) -> None:
        self._submit_policy('register', [owner, constitution, source_authority, ci_authority, audit_authority, source_prefix, ci_prefix, audit_prefix, assurance_authority, assurance_prefix, assurance_corroboration_authority, assurance_corroboration_prefix, proofpatch_kernel_hash, current_version, current_source_url, current_code_hash, max_evidence_age_seconds, proposal_ttl_seconds, execution_timeout_seconds, assurance_observation_delay_seconds, assurance_deadline_seconds, max_manifest_bytes, max_capsule_bytes], str(gl.message.sender_address))

    @gl.public.write
    def create_proposal(self, target: str, candidate_version: str, candidate_source_url: str, candidate_code: bytes, ci_evidence_url: str, ci_evidence_id: str, audit_evidence_url: str, audit_evidence_id: str, assurance_manifest: str, recovery_mode: str, recovery_release_id: str, recovery_version: str, recovery_source_url: str, recovery_code: bytes) -> u256:
        self._submit_policy('create', [target, candidate_version, candidate_source_url, candidate_code, ci_evidence_url, ci_evidence_id, audit_evidence_url, audit_evidence_id, assurance_manifest, recovery_mode, recovery_release_id, recovery_version, recovery_source_url, recovery_code], str(gl.message.sender_address))
        return u256(int(self.proposal_count) + 1)

    @gl.public.write
    def repair_evidence(self, proposal_id: u256, candidate_source_url: str, ci_evidence_url: str, ci_evidence_id: str, audit_evidence_url: str, audit_evidence_id: str) -> None:
        self._submit_policy('repair', [proposal_id, candidate_source_url, ci_evidence_url, ci_evidence_id, audit_evidence_url, audit_evidence_id], str(gl.message.sender_address))

    @gl.public.write
    def assure_release(self, proposal_id: u256, primary_url: str, primary_evidence_id: str, corroboration_url: str, corroboration_evidence_id: str) -> None:
        if gl.message.sender_address == Address(ASSURANCE_REVIEW_ENGINE):
            self._submit_review('assurance', [proposal_id, primary_url, primary_evidence_id, corroboration_url, corroboration_evidence_id], str(gl.message.sender_address))
            return
        self._submit_policy('assure', [proposal_id, primary_url, primary_evidence_id, corroboration_url, corroboration_evidence_id], str(gl.message.sender_address))

    @gl.public.write
    def open_incident(self, target: str, release_id: str, incident_type: str, primary_url: str, primary_evidence_id: str, corroboration_url: str, corroboration_evidence_id: str) -> str:
        now = self._now()
        self._submit_policy('incident', [target, release_id, incident_type, primary_url, primary_evidence_id, corroboration_url, corroboration_evidence_id], str(gl.message.sender_address))
        return 'incident-' + str(now) + '-' + primary_evidence_id

    @gl.public.write
    def repair_incident(self, incident_id: str, primary_url: str, primary_evidence_id: str, corroboration_url: str, corroboration_evidence_id: str) -> None:
        self._submit_policy('repair_incident', [incident_id, primary_url, primary_evidence_id, corroboration_url, corroboration_evidence_id], str(gl.message.sender_address))

    @gl.public.write
    def cancel_proposal(self, proposal_id: u256):
        self._submit_lifecycle('cancel', [proposal_id], str(gl.message.sender_address))

    @gl.public.write
    def expire_proposal(self, proposal_id: u256):
        self._submit_lifecycle('expire', [proposal_id], str(gl.message.sender_address))

    @gl.public.write
    def confirm_install(self, proposal_id: u256, candidate_hash: str):
        self._submit_lifecycle('confirm_install', [proposal_id, candidate_hash], str(gl.message.sender_address))

    @gl.public.write
    def reconcile_install(self, proposal_id: u256):
        self._submit_lifecycle('reconcile_install', [proposal_id], str(gl.message.sender_address))

    @gl.public.write
    def mark_execution_timeout(self, proposal_id: u256):
        self._submit_lifecycle('timeout', [proposal_id], str(gl.message.sender_address))

    @gl.public.write
    def confirm_activation(self, proposal_id: u256, release_id: str, candidate_hash: str):
        self._submit_lifecycle('confirm_activation', [proposal_id, release_id, candidate_hash], str(gl.message.sender_address))

    @gl.public.write
    def expire_provisional_release(self, release_id: str):
        self._submit_lifecycle('expire_provisional', [release_id], str(gl.message.sender_address))

    @gl.public.write
    def confirm_recovery(self, incident_id: str, release_id: str, recovery_hash: str):
        self._submit_lifecycle('confirm_recovery', [incident_id, release_id, recovery_hash], str(gl.message.sender_address))

    @gl.public.write
    def reconcile_recovery(self, incident_id: str):
        self._submit_lifecycle('reconcile_recovery', [incident_id], str(gl.message.sender_address))

    @gl.public.write
    def expire_recovery(self, incident_id: str):
        self._submit_lifecycle('expire_recovery', [incident_id], str(gl.message.sender_address))

    @gl.public.write
    def retry_recovery(self, incident_id: str):
        self._submit_lifecycle('retry_recovery', [incident_id], str(gl.message.sender_address))
