# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_s0='ProofPatch invariant'
_s1='REPAIR_REQUIRED'
_s2='RETRY_REQUIRED'
_s3='installed_candidate_hashes'
_s4='REVIEW_PENDING'
_s5='candidate_hash'
_s6='proposal_count'
_s7='active_target'
_s8='release_count'
_s9='proposal_id'
_s10='RECOVERED'
_s11='incidents'
_s12='proposals'
_s13='incident'
_s14='policies'
_s15='proposal'
_s16='releases'
from genlayer import*
_dn='EVIDENCE_'
_dp='MANIFEST_'
_dl='ASSURANCE_'
_do='INCIDENT_'
_dq='RECOVERY_'
_dm='CANDIDATE_'
_dj='CI_'
_di='AUDIT_'
from dataclasses import dataclass
from datetime import datetime
from genlayer.py.public_abi import StorageType
import hashlib
import json
_bh='proofpatch-v2'
_cq='proofpatch-evidence-v2'
_cm='proofpatch-assurance-v1'
_cr='proofpatch-incident-v1'
_cx='BOOTSTRAP'
_bj='ACTIVE'
_bf='PROVISIONAL'
_ca=_dq+'PENDING'
_aq=_s10
_ap='PROPOSED'
_as=_dn+_s1
_at='REVIEW_RETRY_REQUIRED'
_ct='REJECTED'
_ak='UPGRADE_QUEUED'
_s='INSTALLED_PROVISIONAL'
_an=_dl+'PENDING'
_ba=_dl+_s1
_bc=_dl+_s2
_am='CERTIFICATION_QUEUED'
_w='CERTIFIED'
_cu=_w
_bi='EXPIRED'
_bg='CANCELLED'
_bb='EXECUTION_FAILED'
_ai=_do+'OPEN'
_bz=_do+_s1
_cb=_do+_s2
_t=_do+'CONFIRMED'
_bt=_do+'DISMISSED'
_ah=_dq+'QUEUED'
_u=_dq+_s2
_x=_s10
_db='REPAIR'
_df='RETRY'
_cs='DECISION'
_cn='APPROVE'
_cp='REJECT'
_cw=('installed_hash_matches','kernel_binding_matches','governor_binding_matches','critical_state_preserved','interface_requirements_hold','canary_requirements_hold','runtime_evidence_valid','no_post_install_security_regression','recovery_path_live','assurance_manifest_satisfied')
_cy=('incident_evidence_authentic','incident_affects_exact_release','incident_reproducible_or_sufficiently_established','constitution_breached','continued_operation_unsafe','recovery_capsule_applicable','recovery_safer_than_continuation','recovery_path_preserves_rights','recovery_path_preserves_governance')
_by=16000
_cg=512000
_cz=1024
_de=160
_ck=96
_bu=30*24*60*60
_bv=14*24*60*60
_bs=7*24*60*60
_ch=60
_dc=('storage_layout_compatible','forward_storage_compatible','reverse_storage_compatible_or_recovery_safe','user_rights_preserved','no_privilege_escalation','proofpatch_kernel_preserved','upgrade_authority_preserved','provisional_guard_preserved','consensus_binding_preserved','evidence_trust_preserved','finality_safety_preserved','liveness_preserved','no_hidden_value_transfer','assurance_manifest_sufficient','assurance_path_preserved','recovery_capsule_valid','recovery_path_preserved','constitution_satisfied')
_da='0xD0dFE03E1bFe2EC221Cb505B6a9321e1dA2bD333'
_cc=_s4
_br=_do+_s4

@allow_storage
@dataclass
class _ef:
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
class _dz:
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
class _ed:
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
class _eb:
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

class _dv:

    def __init__(self):
        self.policies={}
        self.proposals={}
        self.releases={}
        self.incidents={}
        self.active_proposal_by_target={}
        self.installed_candidate_hashes={}
        self.proposal_count=u256(0)
        self.release_count=u256(0)
        self.actions=[]

    def _ds(self):
        return self.now

    def _co(self,_bp):
        return hashlib.sha256('\x1f'.join(_bp).encode('utf-8')).hexdigest()

    def _cj(self):
        return u256(0)

    def _cd(self,_l):
        if _l not in self.policies:
            raise gl.vm.UserError(_s0)
        _g=self.policies[_l]
        if self.actor!=_g.fat:
            raise gl.vm.UserError(_s0)
        if not _g.fa:
            raise gl.vm.UserError(_s0)
        return _g

    def _cl(self,_d):
        if _d not in self.proposals:
            raise gl.vm.UserError(_s0)
        return self.proposals[_d]

    def _cv(self,_l,_d):
        if self.active_proposal_by_target.get(_l,self._cj())==_d:
            self.active_proposal_by_target[_l]=self._cj()

    def _ce(self,_a):
        return 'release-'+str(_a.fbc)+'-'+_a.fo[:16]

    def _cf(self,_a):
        return _a.fbn

    def _dd(self,_l,_be,_f,_ao,_ax,_au,_v,_aj,_ad,_ae):
        return self._co([_bh,str(_l),_be,_f,_ao,_ax,_au,_v,_aj,_ad,_ae])

    def _bw(self,_d,_a,_bk):
        _g=self.policies[_a.fbw]
        if _g.fab!=_a.fau:
            raise gl.vm.UserError(_s0)
        _f=self._ce(_a)
        if _f in self.releases:
            _bm=self.releases[_f]
            if _bm.fw!=_a.fo:
                raise gl.vm.UserError(_s0)
            _a.fbv=_s
            return
        _ar=self.releases.get(_g.fac)
        if _ar is None:
            raise gl.vm.UserError(_s0)
        _aa=self._ds()
        lineage_hash=self._dd(_a.fbw,_ar.fao,_f,_g.fac,_a.fq,_a.fo,_a.fay,_a.faf,_a.fg,_a.fbh)
        self.releases[_f]=_ed(fbq=_f,fbw=_a.fbw,fbx=_a.fq,fav=_g.fac,fau=_a.fau,fbu=_a.fp,fw=_a.fo,fbc=_d,fay=_a.fay,faf=_a.faf,fg=_a.fg,fbh=_a.fbh,fal=u64(_aa),fr=u64(0),fbv=_s,fbf='',fbl='',fao=lineage_hash)
        self.release_count=u256(int(self.release_count)+1)
        _a.fbv=_s
        _a.fan=_bk
        self.installed_candidate_hashes[self._co([str(_a.fbw),_a.fo])]=True

    def _ci(self,_h,_f,_n):
        if _h not in self.incidents:
            raise gl.vm.UserError(_s0)
        _e=self.incidents[_h]
        if _e.fbv==_x:
            return
        if _e.fbv not in(_t,_ah,_u)or _f!=_e.fbq:
            raise gl.vm.UserError(_s0)
        if _n.lower()!=_e.fbh:
            raise gl.vm.UserError(_s0)
        _a=self.proposals[self.releases[_f].fbc]
        _o=self._cf(_a)
        if self.target_final_release_id!=_o:
            raise gl.vm.UserError(_s0)
        if self.target_final_candidate_hash!=_n.lower():
            raise gl.vm.UserError(_s0)
        if self.target_final_mode!=_aq:
            raise gl.vm.UserError(_s0)
        _e.fbv=_x
        _e.fan=_dq+'VERIFIED'
        self.releases[_f].fbv=_x
        self.releases[_f].fbl=_h
        _g=self.policies[_e.fbw]
        if _a.fbm==_dq+'CANDIDATE':
            if _o in self.releases:
                if self.releases[_o].fw!=_n.lower():
                    raise gl.vm.UserError(_s0)
            else:
                _bl=self.releases[_f]
                _bn=self._dd(_e.fbw,_bl.fao,_o,_f,_a.fbp,_n.lower(),_a.fay,_a.faf,_a.fg,_a.fbh)
                self.releases[_o]=_ed(fbq=_o,fbw=_e.fbw,fbx=_a.fbp,fav=_f,fau=_e.fam,fbu=_a.fbo,fw=_n.lower(),fbc=_a.fbc,fay=_a.fay,faf=_a.faf,fg=_a.fg,fbh=_a.fbh,fal=u64(self._ds()),fr=u64(self._ds()),fbv=_x,fbf=_f,fbl=_h,fao=_bn)
                self.release_count=u256(int(self.release_count)+1)
        elif _o not in self.releases:
            raise gl.vm.UserError(_s0)
        _g.fae=_a.fbp
        _g.fad=_a.fbo
        _g.fab=_n.lower()
        _g.fac=_o
        self._cv(_e.fbw,_a.fbc)

    def cancel(self,_d:u256)->None:
        _a=self._cl(_d)
        self._cd(_a.fbw)
        if _a.fbv not in(_ap,_as,_at):
            raise gl.vm.UserError(_s0)
        _a.fbv=_bg
        _a.fan='OWNER_CANCELLED'
        self._cv(_a.fbw,_d)

    def expire(self,_d:u256)->None:
        _a=self._cl(_d)
        if _a.fbv not in(_ap,_as,_at):
            raise gl.vm.UserError(_s0)
        if self._ds()<=int(_a.fai):
            raise gl.vm.UserError(_s0)
        _a.fbv=_bi
        _a.fan='PROPOSAL_EXPIRED'
        self._cv(_a.fbw,_d)

    def _bx(self,_d,_a,_g):
        if self.target_final_proposal_id!=_d:
            raise gl.vm.UserError(_s0)
        if self.target_final_candidate_hash!=_a.fo:
            raise gl.vm.UserError(_s0)
        if self.target_final_release_id!=self._ce(_a):
            raise gl.vm.UserError(_s0)
        if self.target_final_mode!=_bf:
            raise gl.vm.UserError(_s0)
        if self.target_final_kernel_hash!=_g.fbb:
            raise gl.vm.UserError(_s0)

    def confirm_install(self,_d:u256,_af:str)->None:
        _a=self._cl(_d)
        if self.actor!=_a.fbw:
            raise gl.vm.UserError(_s0)
        if _a.fbv in(_s,_an,_am,_w):
            if _af.lower()!=_a.fo:
                raise gl.vm.UserError(_s0)
            return
        if _a.fbv!=_ak:
            raise gl.vm.UserError(_s0)
        if _af.lower()!=_a.fo:
            raise gl.vm.UserError(_s0)
        self._bx(_d,_a,self.policies[_a.fbw])
        self._bw(_d,_a,'INSTALL_VERIFIED')

    def reconcile_install(self,_d:u256)->None:
        _a=self._cl(_d)
        self._cd(_a.fbw)
        if _a.fbv!=_ak:
            raise gl.vm.UserError(_s0)
        self._bx(_d,_a,self.policies[_a.fbw])
        self._bw(_d,_a,'INSTALL_RECONCILED')

    def mark_timeout(self,_d:u256)->None:
        _a=self._cl(_d)
        _g=self._cd(_a.fbw)
        if _a.fbv!=_ak:
            raise gl.vm.UserError(_s0)
        if self._ds()<=int(_a.fag):
            raise gl.vm.UserError(_s0)
        if self.target_final_proposal_id==_d and self.target_final_candidate_hash==_a.fo:
            self._bx(_d,_a,_g)
            self._bw(_d,_a,'INSTALL_RECONCILED_TIMEOUT')
            return
        _bd=self.target_final_proposal_id==self._cj()and self.target_final_candidate_hash=='' or(self.target_final_proposal_id!=_d and self.target_final_candidate_hash==_g.fab)
        if not _bd:
            raise gl.vm.UserError(_s0)
        if self.target_nonfinal_proposal_id==_d and self.target_nonfinal_candidate_hash==_a.fo:
            raise gl.vm.UserError(_s0)
        if self.target_nonfinal_proposal_id!=self.target_final_proposal_id or self.target_nonfinal_candidate_hash!=self.target_final_candidate_hash:
            raise gl.vm.UserError(_s0)
        _a.fbv=_bb
        _a.fan='EXECUTION_TIMEOUT'
        self._cv(_a.fbw,_d)

    def confirm_activation(self,_d:u256,_f:str,_af:str)->None:
        _a=self._cl(_d)
        if self.actor!=_a.fbw:
            raise gl.vm.UserError(_s0)
        if _a.fbv==_w:
            return
        if _a.fbv!=_am:
            raise gl.vm.UserError(_s0)
        if _f!=self._ce(_a)or _af.lower()!=_a.fo:
            raise gl.vm.UserError(_s0)
        if self.target_final_release_id!=_f:
            raise gl.vm.UserError(_s0)
        if self.target_final_candidate_hash!=_a.fo:
            raise gl.vm.UserError(_s0)
        if self.target_final_mode!=_bj:
            raise gl.vm.UserError(_s0)
        _k=self.releases[_f]
        _aa=self._ds()
        _k.fbv=_w
        _k.fr=u64(_aa)
        _a.fbv=_w
        _a.fan='CERTIFICATION_VERIFIED'
        _g=self.policies[_a.fbw]
        _g.fae=_a.fq
        _g.fad=_a.fp
        _g.fab=_a.fo
        _g.fac=_f
        self._cv(_a.fbw,_d)

    def expire_provisional(self,_f:str)->None:
        if _f not in self.releases:
            raise gl.vm.UserError(_s0)
        _k=self.releases[_f]
        if _k.fbv not in(_s,_an,_ba,_bc):
            raise gl.vm.UserError(_s0)
        _g=self.policies[_k.fbw]
        if self._ds()<=int(_k.fal)+int(_g.fe):
            raise gl.vm.UserError(_s0)
        _h='timeout-'+_f
        if not self.incident_exists:
            _a=self.proposals[_k.fbc]
            self.incidents[_h]=_eb(faj=_h,fbw=_k.fbw,fbq=_f,fam=_k.fw,fak=_dl+'TIMEOUT',fba='',faz='',fz='',fy='',fay=_k.fay,fg=_k.fg,fbh=_k.fbh,fas=u64(self._ds()),fai=u64(self._ds()+int(_g.fbd)),fbr=u64(0),fbk=u64(0),fbv=_ai,fan=_dl+'DEADLINE_EXPIRED',fbg=False)
            _a.fbv=_ai
        _k.fbv=_ai

    def confirm_recovery(self,_h:str,_f:str,_n:str)->None:
        if _h not in self.incidents:
            raise gl.vm.UserError(_s0)
        _e=self.incidents[_h]
        if self.actor!=_e.fbw:
            raise gl.vm.UserError(_s0)
        if _e.fbv!=_x and self._ds()>int(_e.fbk):
            raise gl.vm.UserError(_s0)
        self._ci(_h,_f,_n)

    def reconcile_recovery(self,_h:str)->None:
        if _h not in self.incidents:
            raise gl.vm.UserError(_s0)
        _e=self.incidents[_h]
        if _e.fbv not in(_t,_ah,_u):
            raise gl.vm.UserError(_s0)
        self._ci(_h,_e.fbq,_e.fbh)

    def expire_recovery(self,_h:str)->None:
        if _h not in self.incidents:
            raise gl.vm.UserError(_s0)
        _e=self.incidents[_h]
        if _e.fbv not in(_t,_ah):
            raise gl.vm.UserError(_s0)
        if self._ds()<=int(_e.fbk):
            raise gl.vm.UserError(_s0)
        if self.target_final_mode==_aq:
            self._ci(_h,_e.fbq,_e.fbh)
            return
        _e.fbv=_u
        self.releases[_e.fbq].fbv=_u

    def retry_recovery(self,_h:str)->None:
        if _h not in self.incidents:
            raise gl.vm.UserError(_s0)
        _e=self.incidents[_h]
        if _e.fbv!=_u:
            raise gl.vm.UserError(_s0)
        _g=self.policies[_e.fbw]
        _aa=self._ds()
        _e.fbv=_t
        _e.fbk=u64(_aa+int(_g.fah))
        self.releases[_e.fbq].fbv=_t
        self.actions.append({'kind':'recover','args':[_h,_e.fbq,_e.fbh]})
_q='0x0000000000000000000000000000000000000000'

@gl.contract_interface
class _dx:

    class _eh:

        def apply_lifecycle_result(self,_i:str,_aw:str)->None:
            ...

class _dt(gl.Contract):
    admin:Address
    governor:Address
    executor:Address

    def __init__(self):
        self.admin=gl.message.sender_address
        self.governor=Address(_q)
        self.executor=Address(_q)

    @gl.public.write
    def bind_governor(self,governor:str)->None:
        if gl.message.sender_address!=self.admin:
            raise gl.vm.UserError(_s0)
        if self.governor!=Address(_q):
            raise gl.vm.UserError(_s0)
        _y=Address(governor)
        if _y==Address(_q):
            raise gl.vm.UserError(_s0)
        self.governor=_y

    @gl.public.write
    def bind_executor(self,executor:str)->None:
        if gl.message.sender_address!=self.admin:
            raise gl.vm.UserError(_s0)
        if self.executor!=Address(_q):
            raise gl.vm.UserError(_s0)
        _y=Address(executor)
        if _y==Address(_q):
            raise gl.vm.UserError(_s0)
        self.executor=_y

    def _dg(self,_c):
        if isinstance(_c,Address):
            return str(_c)
        if isinstance(_c,bytes):
            return _c.hex()
        if isinstance(_c,bool):
            return _c
        if isinstance(_c,int):
            return int(_c)
        if isinstance(_c,dict):
            return{str(_al):self._dg(_ac)for(_al,_ac)in _c.items()}
        if isinstance(_c,list):
            return[self._dg(_ac)for _ac in _c]
        if hasattr(_c,'__dict__'):
            return{_al:self._dg(_ac)for(_al,_ac)in _c.__dict__.items()}
        return _c

    def _dh(self,cls,_bq):
        _c=list(_bq.values())
        if cls is _ef or cls is _dz or cls is _ed or(cls is _eb):
            _c[1]=Address(_c[1])
        if cls is _ef:
            _c[0]=Address(_c[0])
        elif cls is _dz:
            _c[2]=Address(_c[2])
            if isinstance(_c[8],str):
                _c[8]=bytes.fromhex(_c[8])
            if isinstance(_c[20],str):
                _c[20]=bytes.fromhex(_c[20])
        return cls(**dict(zip(cls.__annotations__.keys(),_c)))

    def _dr(self,_b,_j):
        _b.actor=Address(_j['actor'])
        _b.now=int(_j['now'])
        _p=_j.get('records',{})
        _b.proposal_count=u256(_j.get(_s6,0))
        _b.release_count=u256(_j.get(_s8,0))
        _b.used_candidate_hashes=dict(_j.get(_s3,{}))
        if _p.get('policy')is not None:
            _ab=self._dh(_ef,_p['policy'])
            _b.policies[_ab.fbw]=_ab
        if _p.get(_s15)is not None:
            _ab=self._dh(_dz,_p[_s15])
            _b.proposals[_ab.fbc]=_ab
        for _ag in('release','parent_release','recovery_release'):
            if _p.get(_ag)is not None:
                _az=self._dh(_ed,_p[_ag])
                _b.releases[_az.fbq]=_az
        if _p.get(_s13)is not None:
            _ay=self._dh(_eb,_p[_s13])
            _b.incidents[_ay.faj]=_ay
        if _j.get(_s7)is not None:
            _b.active_proposal_by_target[Address(_j[_s7])]=u256(_j.get('active_value',0))
        _b.installed_candidate_hashes=_b.used_candidate_hashes
        _b.incident_exists=bool(_j.get('incident_exists',False))
        _z=_j.get('target_final',{})
        _b.target_final_proposal_id=u256(_z.get(_s9,0))
        _b.target_final_candidate_hash=str(_z.get(_s5,''))
        _b.target_final_release_id=str(_z.get('release_id',''))
        _b.target_final_mode=str(_z.get('mode',''))
        _b.target_final_kernel_hash=str(_z.get('kernel_hash',''))
        _av=_j.get('target_nonfinal',{})
        _b.target_nonfinal_proposal_id=u256(_av.get(_s9,0))
        _b.target_nonfinal_candidate_hash=str(_av.get(_s5,''))

    def _dk(self,_b,_i):
        _r={'operation':_i,_s14:[],_s12:[],_s16:[],_s11:[],'active':[],_s3:_b.installed_candidate_hashes,_s6:int(_b.proposal_count),_s8:int(_b.release_count),'actions':_b.actions}
        for _c in _b.policies.values():
            _r[_s14].append(self._dg(_c))
        for _c in _b.proposals.values():
            _r[_s12].append(self._dg(_c))
        for _c in _b.releases.values():
            _r[_s16].append(self._dg(_c))
        for _c in _b.incidents.values():
            _r[_s11].append(self._dg(_c))
        for(_ag,_c)in _b.active_proposal_by_target.items():
            _r['active'].append([str(_ag),int(_c)])
        return _r

    @gl.public.write
    def execute(self,_i:str,_bo:str)->None:
        if gl.message.sender_address!=self.executor:
            raise gl.vm.UserError(_s0)
        _j=json.loads(_bo)
        _b=_dv()
        self._dr(_b,_j)
        _m=_j.get('args',[])
        if _i=='cancel':
            _b.cancel(*_m)
        elif _i=='expire':
            _b.expire(*_m)
        elif _i=='confirm_install':
            _b.confirm_install(*_m)
        elif _i=='reconcile_install':
            _b.reconcile_install(*_m)
        elif _i=='timeout':
            _b.mark_timeout(*_m)
        elif _i=='confirm_activation':
            _b.confirm_activation(*_m)
        elif _i=='expire_provisional':
            _b.expire_provisional(*_m)
        elif _i=='confirm_recovery':
            _b.confirm_recovery(*_m)
        elif _i=='reconcile_recovery':
            _b.reconcile_recovery(*_m)
        elif _i=='expire_recovery':
            _b.expire_recovery(*_m)
        elif _i=='retry_recovery':
            _b.retry_recovery(*_m)
        else:
            raise gl.vm.UserError(_s0)
        _aw=json.dumps(self._dk(_b,_i),separators=(',',':'))
        _dx(self.governor).emit(on='finalized').apply_lifecycle_result(_i,_aw)
