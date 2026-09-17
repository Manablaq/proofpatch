# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_s0='ProofPatch invariant'
_s1='proposal'
_s2='proposal_id'
_s3='incident'
_s4='expire_provisional'
_s5='candidate_hash'
_s6='proposal_count'
_s7='release_count'
_s8='release_id'
from genlayer import*
_aa='EVIDENCE_'
_ac='MANIFEST_'
_y='ASSURANCE_'
_ab='INCIDENT_'
_ad='RECOVERY_'
_z='CANDIDATE_'
_w='CI_'
_v='AUDIT_'
from genlayer.py.public_abi import StorageType
import hashlib
import json
_k='0x0000000000000000000000000000000000000000'
_s='0x8948b524adbfA84eBDEb39bFF925695fF111FCbD'

@gl.contract_interface
class _aj:

    class _ap:

        def get_state_record(self,_j:str,_f:str)->str:
            ...

@gl.contract_interface
class _al:

    class _ap:

        def proofpatch_installed_proposal_id(self)->u256:
            ...

        def proofpatch_installed_candidate_hash(self)->str:
            ...

        def proofpatch_installed_release_id(self)->str:
            ...

        def proofpatch_release_mode(self)->str:
            ...

        def get_proofpatch_kernel_hash(self)->str:
            ...

@gl.contract_interface
class _ah:

    class _an:

        def execute(self,_d:str,_p:str)->None:
            ...

class _af(gl.Contract):
    admin:Address
    governor:Address

    def __init__(self):
        self.admin=gl.message.sender_address
        self.governor=Address(_k)

    @gl.public.write
    def bind_governor(self,governor:str)->None:
        if gl.message.sender_address!=self.admin:
            raise gl.vm.UserError(_s0)
        if self.governor!=Address(_k):
            raise gl.vm.UserError(_s0)
        _o=Address(governor)
        if _o==Address(_k):
            raise gl.vm.UserError(_s0)
        self.governor=_o

    def _ae(self,_b,_j,_f):
        return json.loads(_b.get_state_record(_j,_f))

    def _x(self,_b,_j,_f):
        try:
            return self._ae(_b,_j,_f)
        except Exception:
            return None

    def _u(self,_d,_l):
        _b=_aj(self.governor).view(state=StorageType.LATEST_FINAL)
        _h=_l['args']
        _a={}
        if _d==_s4:
            _a['release']=self._ae(_b,'release',_h[0])
            _e=_a['release']['target']
            _a[_s1]=self._ae(_b,_s1,str(_a['release'][_s2]))
        elif _d in('confirm_recovery','reconcile_recovery','expire_recovery','retry_recovery'):
            _a[_s3]=self._ae(_b,_s3,_h[0])
            _a['release']=self._ae(_b,'release',_a[_s3][_s8])
            _a[_s1]=self._ae(_b,_s1,str(_a['release'][_s2]))
            _e=_a[_s3]['target']
        else:
            _a[_s1]=self._ae(_b,_s1,str(int(_h[0])))
            _e=_a[_s1]['target']
            if _d=='confirm_activation':
                _a['release']=self._ae(_b,'release',_h[1])
        _a['policy']=self._ae(_b,'policy',_e)
        _g=_a.get(_s1)
        if _g is not None and _d in('confirm_install','reconcile_install','timeout'):
            _a['parent_release']=self._ae(_b,'release',_a['policy']['current_release_id'])
        if _g is not None and _g['recovery_mode']==_ad+'CANDIDATE':
            _m=self._x(_b,'release',_g['recovery_release_id'])
            if _m is not None:
                _a['recovery_release']=_m
        _c={'args':_h,'actor':_l['actor'],'now':_l['now'],'records':_a}
        _q=self._ae(_b,'counts','')
        _c[_s6]=_q[_s6]
        _c[_s7]=_q[_s7]
        _t=self._ae(_b,'active',_e)
        _c['active_target']=_e
        _c['active_value']=_t['value']
        if _g is not None:
            _f=hashlib.sha256('\x1f'.join([_e,_g['candidate_code_hash']]).encode()).hexdigest()
            _r=self._x(_b,'candidate',_f)
            _c['installed_candidate_hashes']={_f:True}if _r is not None and _r.get('value',False)else{}
        if _d==_s4:
            _c['incident_exists']=self._x(_b,_s3,'timeout-'+_h[0])is not None
        _i=_al(Address(_e)).view(state=StorageType.LATEST_FINAL)
        _c['target_final']={_s2:int(_i.proofpatch_installed_proposal_id()),_s5:_i.proofpatch_installed_candidate_hash(),_s8:_i.proofpatch_installed_release_id(),'mode':_i.proofpatch_release_mode(),'kernel_hash':_i.get_proofpatch_kernel_hash()}
        _n=_al(Address(_e)).view(state=StorageType.LATEST_NON_FINAL)
        _c['target_nonfinal']={_s2:int(_n.proofpatch_installed_proposal_id()),_s5:_n.proofpatch_installed_candidate_hash()}
        return _c

    @gl.public.write
    def execute(self,_d:str,_p:str)->None:
        if gl.message.sender_address!=self.governor:
            raise gl.vm.UserError(_s0)
        _c=self._u(_d,json.loads(_p))
        _ah(Address(_s)).emit(on='finalized').execute(_d,json.dumps(_c,sort_keys=True,separators=(',',':')))
