# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
from genlayer.py.public_abi import StorageType
import hashlib
import json

ZERO = '0x0000000000000000000000000000000000000000'
LIFECYCLE_ENGINE = '0x8948b524adbfA84eBDEb39bFF925695fF111FCbD'

@gl.contract_interface
class ProofPatchGovernor:
    class View:
        def get_state_record(self, kind: str, key: str) -> str:
            ...

@gl.contract_interface
class ProofPatchTarget:
    class View:
        def proofpatch_installed_proposal_id(self) -> u256: ...
        def proofpatch_installed_candidate_hash(self) -> str: ...
        def proofpatch_installed_release_id(self) -> str: ...
        def proofpatch_release_mode(self) -> str: ...
        def get_proofpatch_kernel_hash(self) -> str: ...

@gl.contract_interface
class ProofPatchLifecycleEngine:
    class Write:
        def execute(self, operation: str, request: str) -> None: ...

class ProofPatchLifecycleRequestEngine(gl.Contract):
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

    def _read(self, view, kind, key):
        return json.loads(view.get_state_record(kind, key))

    def _maybe(self, view, kind, key):
        try:
            return self._read(view, kind, key)
        except Exception:
            return None

    def _prepare(self, operation, data):
        view = ProofPatchGovernor(self.governor).view(state=StorageType.LATEST_FINAL)
        args = data['args']
        records = {}
        if operation == 'expire_provisional':
            records['release'] = self._read(view, 'release', args[0])
            target = records['release']['target']
            records['proposal'] = self._read(view, 'proposal', str(records['release']['proposal_id']))
        elif operation in ('confirm_recovery', 'reconcile_recovery', 'expire_recovery', 'retry_recovery'):
            records['incident'] = self._read(view, 'incident', args[0])
            records['release'] = self._read(view, 'release', records['incident']['release_id'])
            records['proposal'] = self._read(view, 'proposal', str(records['release']['proposal_id']))
            target = records['incident']['target']
        else:
            records['proposal'] = self._read(view, 'proposal', str(int(args[0])))
            target = records['proposal']['target']
            if operation == 'confirm_activation':
                records['release'] = self._read(view, 'release', args[1])
        records['policy'] = self._read(view, 'policy', target)
        proposal = records.get('proposal')
        if proposal is not None and operation in ('confirm_install', 'reconcile_install', 'timeout'):
            records['parent_release'] = self._read(view, 'release', records['policy']['current_release_id'])
        if proposal is not None and proposal['recovery_mode'] == 'RECOVERY_CANDIDATE':
            recovery_release = self._maybe(view, 'release', proposal['recovery_release_id'])
            if recovery_release is not None:
                records['recovery_release'] = recovery_release
        prepared = {'args': args, 'actor': data['actor'], 'now': data['now'], 'records': records}
        counts = self._read(view, 'counts', '')
        prepared['proposal_count'] = counts['proposal_count']
        prepared['release_count'] = counts['release_count']
        active = self._read(view, 'active', target)
        prepared['active_target'] = target
        prepared['active_value'] = active['value']
        if proposal is not None:
            key = hashlib.sha256('\x1f'.join([target, proposal['candidate_code_hash']]).encode()).hexdigest()
            used = self._maybe(view, 'candidate', key)
            prepared['installed_candidate_hashes'] = {key: True} if used is not None and used.get('value', False) else {}
        if operation == 'expire_provisional':
            prepared['incident_exists'] = self._maybe(view, 'incident', 'timeout-' + args[0]) is not None
        target_view = ProofPatchTarget(Address(target)).view(state=StorageType.LATEST_FINAL)
        prepared['target_final'] = {'proposal_id': int(target_view.proofpatch_installed_proposal_id()), 'candidate_hash': target_view.proofpatch_installed_candidate_hash(), 'release_id': target_view.proofpatch_installed_release_id(), 'mode': target_view.proofpatch_release_mode(), 'kernel_hash': target_view.get_proofpatch_kernel_hash()}
        nonfinal_view = ProofPatchTarget(Address(target)).view(state=StorageType.LATEST_NON_FINAL)
        prepared['target_nonfinal'] = {'proposal_id': int(nonfinal_view.proofpatch_installed_proposal_id()), 'candidate_hash': nonfinal_view.proofpatch_installed_candidate_hash()}
        return prepared

    @gl.public.write
    def execute(self, operation: str, request: str) -> None:
        if gl.message.sender_address != self.governor:
            raise gl.vm.UserError('Only the bound governor may prepare lifecycle execution')
        prepared = self._prepare(operation, json.loads(request))
        ProofPatchLifecycleEngine(Address(LIFECYCLE_ENGINE)).emit(on='finalized').execute(operation, json.dumps(prepared, sort_keys=True, separators=(',', ':')))
