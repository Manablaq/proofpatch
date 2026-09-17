# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_s0='ProofPatch invariant'
_s1='candidate_code_hash'
_s2='policy_fingerprint'
_s3='proposal'
_s4='assurance_manifest_hash'
_s5='recovery_capsule_hash'
_s6='proposal_id'
_s7='error_code'
_s8='incident'
_s9='REPAIR_REQUIRED'
_s10='release_id'
_s11='RETRY_REQUIRED'
_s12='active_target'
_s13='decision'
_s14='installed_code_hash'
_s15='evidence_set_hash'
_s16='parent_code_hash'
_s17='release-'
_s18='REVIEW_PENDING'
_s19='active_value'
_s20='target_mode'
_s21='assurance-'
_s22='RECOVERED'
_s23='assurance'
_s24='incidents'
_s25='proposals'
_s26='policies'
_s27='releases'
from genlayer import*
_cs='EVIDENCE_'
_cu='MANIFEST_'
_cq='ASSURANCE_'
_ct='INCIDENT_'
_cv='RECOVERY_'
_cr='CANDIDATE_'
_cn='CI_'
_cm='AUDIT_'
from dataclasses import dataclass
from datetime import datetime
from genlayer.py.public_abi import StorageType
import hashlib
import json
_cb='proofpatch-v2'
_bt='proofpatch-evidence-v2'
_bq='proofpatch-assurance-v1'
_bu='proofpatch-incident-v1'
_bz='BOOTSTRAP'
_ci='ACTIVE'
_ae='PROVISIONAL'
_bj=_cv+'PENDING'
_ca=_s22
_bv='PROPOSED'
_aw=_cs+_s9
_ax='REVIEW_RETRY_REQUIRED'
_au='REJECTED'
_av='UPGRADE_QUEUED'
_aa='INSTALLED_PROVISIONAL'
_al=_cq+'PENDING'
_am=_cq+_s9
_an=_cq+_s11
_ab='CERTIFICATION_QUEUED'
_s='CERTIFIED'
_bw=_s
_cc='EXPIRED'
_br='CANCELLED'
_bg='EXECUTION_FAILED'
_q=_ct+'OPEN'
_ao=_ct+_s9
_ap=_ct+_s11
_ac=_ct+'CONFIRMED'
_ak=_ct+'DISMISSED'
_bi=_cv+'QUEUED'
_bk=_cv+_s11
_bs=_s22
_u='REPAIR'
_v='RETRY'
_at='DECISION'
_r='APPROVE'
_as='REJECT'
_by=('installed_hash_matches','kernel_binding_matches','governor_binding_matches','critical_state_preserved','interface_requirements_hold','canary_requirements_hold','runtime_evidence_valid','no_post_install_security_regression','recovery_path_live','assurance_manifest_satisfied')
_ce=('incident_evidence_authentic','incident_affects_exact_release','incident_reproducible_or_sufficiently_established','constitution_breached','continued_operation_unsafe','recovery_capsule_applicable','recovery_safer_than_continuation','recovery_path_preserves_rights','recovery_path_preserves_governance')
_bh=16000
_bm=512000
_cf=1024
_ch=160
_bo=96
_be=30*24*60*60
_bf=14*24*60*60
_bd=7*24*60*60
_bn=60
_cg=('storage_layout_compatible','forward_storage_compatible','reverse_storage_compatible_or_recovery_safe','user_rights_preserved','no_privilege_escalation','proofpatch_kernel_preserved','upgrade_authority_preserved','provisional_guard_preserved','consensus_binding_preserved','evidence_trust_preserved','finality_safety_preserved','liveness_preserved','no_hidden_value_transfer','assurance_manifest_sufficient','assurance_path_preserved','recovery_capsule_valid','recovery_path_preserved','constitution_satisfied')
_t='0xD0dFE03E1bFe2EC221Cb505B6a9321e1dA2bD333'
_aq=_s18
_aj=_ct+_s18

@allow_storage
@dataclass
class _do:
    fat:Address
    fbw:Address
    fx:str
    fay:str
    fbs:str
    fs:str
    fj:str
    fbt:str
    fv:str
    fm:str
    fb:str
    fi:str
    fc:str
    fd:str
    fbb:str
    fae:str
    fad:str
    fab:str
    fac:str
    faq:u64
    fbd:u64
    fah:u64
    fh:u64
    fe:u64
    far:u64
    fap:u64
    fa:bool

@allow_storage
@dataclass
class _di:
    fbc:u256
    fbw:Address
    fbe:Address
    fax:str
    faw:str
    fau:str
    fq:str
    fp:str
    fn:bytes
    fo:str
    fu:str
    ft:str
    fl:str
    fk:str
    ff:str
    fg:str
    fbm:str
    fbn:str
    fbp:str
    fbo:str
    fbi:bytes
    fbj:str
    fbh:str
    faf:str
    fay:str
    faa:u64
    fai:u64
    fbr:u64
    fag:u64
    fbv:str
    fan:str

@allow_storage
@dataclass
class _dm:
    fbq:str
    fbw:Address
    fbx:str
    fav:str
    fau:str
    fbu:str
    fw:str
    fbc:u256
    fay:str
    faf:str
    fg:str
    fbh:str
    fal:u64
    fr:u64
    fbv:str
    fbf:str
    fbl:str
    fao:str

@allow_storage
@dataclass
class _dk:
    faj:str
    fbw:Address
    fbq:str
    fam:str
    fak:str
    fba:str
    faz:str
    fz:str
    fy:str
    fay:str
    fg:str
    fbh:str
    fas:u64
    fai:u64
    fbr:u64
    fbk:u64
    fbv:str
    fan:str
    fbg:bool

class _da:

    def __init__(self):
        self.policies={}
        self.proposals={}
        self.releases={}
        self.incidents={}
        self.active_proposal_by_target={}
        self.actions=[]

    def _cx(self):
        return self.now

    def _bp(self,_h):
        if _h not in self.proposals:
            raise gl.vm.UserError(_s0)
        return self.proposals[_h]

    def _bx(self,_m,_h):
        if self.active_proposal_by_target.get(_m,u256(0))==_h:
            self.active_proposal_by_target[_m]=u256(0)

    def _bl(self,_a):
        return _s17+str(_a.fbc)+'-'+_a.fo[:16]

    def _a(self,_h,_c):
        _a=self._bp(_h)
        _k=self.policies[_a.fbw]
        _a.fbr=u64(self._cx())
        _a.fan=str(_c.get(_s7,''))
        if _c['kind']==_u:
            _a.fbv=_aw
            return
        if _c['kind']==_v:
            _a.fbv=_ax
            return
        if _c['kind']!=_at:
            raise gl.vm.UserError(_s0)
        if _c[_s13]==_as:
            _a.fbv=_au
            self._bx(_a.fbw,_h)
            return
        if _c[_s13]!=_r:
            raise gl.vm.UserError(_s0)
        _a.fbv=_av
        _a.fag=u64(self._cx()+int(_k.fah))
        self.actions.append({'kind':'upgrade','args':[str(_a.fbw),int(_h),_a.fo]})

    def assurance(self,_h,_c,_af,_az,_ad,_ar):
        _a=self._bp(_h)
        release_id=self._bl(_a)
        if _c['kind']==_u:
            _a.fbv=_am
            _a.fan=str(_c.get(_s7,''))
            return
        if _c['kind']==_v:
            _a.fbv=_an
            _a.fan=str(_c.get(_s7,''))
            return
        _a.fan=str(_c.get(_s7,''))
        if _c.get(_s13)==_r:
            _a.fbv=_ab
            self.releases[release_id].fbv=_ab
            self.actions.append({'kind':'activate','args':[str(_a.fbw),release_id,_a.fo]})
            return
        _a.fbv=_q
        _x=self._cx()
        _k=self.policies[_a.fbw]
        self.incidents[_s21+release_id]=_dk(faj=_s21+release_id,fbw=_a.fbw,fbq=release_id,fam=_a.fo,fak=_cq+'FAILURE',fba=_af,faz=_az,fz=_ad,fy=_ar,fay=_a.fay,fg=_a.fg,fbh=_a.fbh,fas=u64(_x),fai=u64(_x+int(_k.fbd)),fbr=u64(_x),fbk=u64(0),fbv=_q,fan=_cq+'FAILED',fbg=False)
        self.releases[release_id].fbv=_q

    def incident(self,_p,_c):
        incident=self.incidents[_p]
        _l=self.releases[incident.fbq]
        _a=self.proposals[_l.fbc]
        incident.fbr=u64(self._cx())
        incident.fan=str(_c.get(_s7,''))
        if _c['kind']==_u:
            incident.fbv=_ao
            return
        if _c['kind']==_v:
            incident.fbv=_ap
            return
        if _c.get(_s13)!=_r:
            incident.fbv=_ak
            _l.fbv=_aa if self.target_mode==_ae else _s
            _a.fbv=_aa if self.target_mode==_ae else _s
            return
        incident.fbv=_ac
        incident.fbg=True
        incident.fbk=u64(self._cx()+int(self.policies[incident.fbw].fah))
        _l.fbv=_ac
        self.actions.append({'kind':'recover','args':[_p,incident.fbq,incident.fbh]})
_w='0x0000000000000000000000000000000000000000'

@gl.contract_interface
class _de:

    class _ds:

        def get_state_record(self,_ai:str,_g:str)->str:
            ...

    class _dq:

        def apply_review_result(self,_i:str,_ah:str)->None:
            ...

@gl.contract_interface
class _dc:

    class _ds:

        def get_proposal_result(self,_h:u256)->str:
            ...

        def get_assurance_result(self,_h:u256)->str:
            ...

        def get_incident_result(self,_p:str)->str:
            ...

@gl.contract_interface
class _dg:

    class _ds:

        def proofpatch_release_mode(self)->str:
            ...

class _cy(gl.Contract):
    admin:Address
    governor:Address

    def __init__(self):
        self.admin=gl.message.sender_address
        self.governor=Address(_w)

    @gl.public.write
    def bind_governor(self,governor:str)->None:
        if gl.message.sender_address!=self.admin:
            raise gl.vm.UserError(_s0)
        if self.governor!=Address(_w):
            raise gl.vm.UserError(_s0)
        _ag=Address(governor)
        if _ag==Address(_w):
            raise gl.vm.UserError(_s0)
        self.governor=_ag

    def _cj(self,_b):
        if isinstance(_b,Address):
            return str(_b)
        if isinstance(_b,bytes):
            return _b.hex()
        if isinstance(_b,bool):
            return _b
        if isinstance(_b,int):
            return int(_b)
        if isinstance(_b,dict):
            return{str(_z):self._cj(_o)for(_z,_o)in _b.items()}
        if isinstance(_b,list):
            return[self._cj(_o)for _o in _b]
        if hasattr(_b,'__dict__'):
            return{_z:self._cj(_o)for(_z,_o)in _b.__dict__.items()}
        return _b

    def _ck(self,cls,_y):
        _b=list(_y.values())
        if cls is _do or cls is _di or cls is _dm or(cls is _dk):
            _b[1]=Address(_b[1])
        if cls is _do:
            _b[0]=Address(_b[0])
        elif cls is _di:
            _b[2]=Address(_b[2])
            if isinstance(_b[8],str):
                _b[8]=bytes.fromhex(_b[8])
            if isinstance(_b[20],str):
                _b[20]=bytes.fromhex(_b[20])
        return cls(**dict(zip(cls.__annotations__.keys(),_b)))

    def _cw(self,_d,_f):
        _d.actor=Address(_f['actor'])
        _d.now=int(_f['now'])
        for(_g,cls,_bc)in(('policy',_do,_d.policies),(_s3,_di,_d.proposals),('release',_dm,_d.releases),(_s8,_dk,_d.incidents)):
            if _f.get(_g)is not None:
                _b=self._ck(cls,_f[_g])
                _bc[_b.fbw if _g=='policy' else _b.fbc if _g==_s3 else _b.fbq if _g=='release' else _b.faj]=_b
        if _f.get(_s12)is not None:
            _d.active_proposal_by_target[Address(_f[_s12])]=u256(_f.get(_s19,0))
        _d.target_mode=str(_f.get(_s20,''))

    def _cl(self,_y,_ba):
        try:
            _c=json.loads(_y)
        except Exception:
            raise gl.vm.UserError(_s0)
        if not isinstance(_c,dict):
            raise gl.vm.UserError(_s0)
        for(_g,_b)in _ba.items():
            if _c.get(_g)!=_b:
                raise gl.vm.UserError(_s0)
        return _c

    def _cp(self,_j,_ai,_g):
        return json.loads(_j.get_state_record(_ai,_g))

    def _cd(self,_i,_f,_j):
        _e=_f.get('args',[])
        if _i==_s3:
            _a=self._cp(_j,_s3,str(int(_e[0])))
            _k=self._cp(_j,'policy',_a['target'])
            _c=self._cl(_dc(Address(_t)).view(state=StorageType.LATEST_FINAL).get_proposal_result(u256(_e[0])),{'target':_a['target'],_s6:int(_e[0]),_s16:_a[_s16],_s1:_a[_s1],_s2:_a[_s2],_s15:_a[_s15],_s4:_a[_s4],_s5:_a[_s5]})
            if _a['status']!=_aq:
                raise gl.vm.UserError(_s0)
            return{_s3:_a,'policy':_k,_s12:_a['target'],_s19:self._cp(_j,'active',_a['target'])['value'],'result':_c}
        if _i==_s23:
            _a=self._cp(_j,_s3,str(int(_e[0])))
            _k=self._cp(_j,'policy',_a['target'])
            _c=self._cl(_dc(Address(_t)).view(state=StorageType.LATEST_FINAL).get_assurance_result(u256(_e[0])),{'target':_a['target'],_s6:int(_e[0]),_s10:_s17+str(_a[_s6])+'-'+_a[_s1][:16],_s1:_a[_s1],_s2:_a[_s2],_s4:_a[_s4]})
            if _a['status']!=_al:
                raise gl.vm.UserError(_s0)
            return{_s3:_a,'policy':_k,'release':self._cp(_j,'release',_s17+str(_a[_s6])+'-'+_a[_s1][:16]),'result':_c}
        if _i==_s8:
            incident=self._cp(_j,_s8,_e[0])
            _l=self._cp(_j,'release',incident[_s10])
            _a=self._cp(_j,_s3,str(_l[_s6]))
            _k=self._cp(_j,'policy',incident['target'])
            _c=self._cl(_dc(Address(_t)).view(state=StorageType.LATEST_FINAL).get_incident_result(_e[0]),{'incident_id':_e[0],'target':incident['target'],_s10:incident[_s10],_s14:incident[_s14],_s2:incident[_s2],_s5:incident[_s5]})
            if incident['status']!=_aj:
                raise gl.vm.UserError(_s0)
            _ay=_dg(Address(incident['target'])).view(state=StorageType.LATEST_FINAL).proofpatch_release_mode()
            return{_s8:incident,'release':_l,_s3:_a,'policy':_k,_s20:_ay,'result':_c}
        raise gl.vm.UserError(_s0)

    def _co(self,_d,_i):
        _n={'operation':_i,_s26:[],_s25:[],_s27:[],_s24:[],'active':[],'actions':_d.actions}
        for _b in _d.policies.values():
            _n[_s26].append(self._cj(_b))
        for _b in _d.proposals.values():
            _n[_s25].append(self._cj(_b))
        for _b in _d.releases.values():
            _n[_s27].append(self._cj(_b))
        for _b in _d.incidents.values():
            _n[_s24].append(self._cj(_b))
        for(_g,_b)in _d.active_proposal_by_target.items():
            _n['active'].append([str(_g),int(_b)])
        return _n

    @gl.public.write
    def execute(self,_i:str,_bb:str)->None:
        if gl.message.sender_address!=self.governor:
            raise gl.vm.UserError(_s0)
        _f=json.loads(_bb)
        state=self._cd(_i,_f,_de(self.governor).view(state=StorageType.LATEST_FINAL))
        for(_g,_b)in state.items():
            if _g!='result':
                _f[_g]=_b
        _d=_da()
        self._cw(_d,_f)
        _e=_f.get('args',[])
        if _i==_s3:
            _d.proposal(_e[0],state['result'])
        elif _i==_s23:
            _d.assurance(_e[0],state['result'],_e[1],_e[2],_e[3],_e[4])
        elif _i==_s8:
            _d.incident(_e[0],state['result'])
        else:
            raise gl.vm.UserError(_s0)
        _ah=json.dumps(self._co(_d,_i),separators=(',',':'))
        _de(self.governor).emit(on='finalized').apply_review_result(_i,_ah)
