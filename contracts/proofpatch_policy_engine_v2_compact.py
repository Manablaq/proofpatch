# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_s0='ProofPatch invariant'
_s1='assurance_deadline_seconds'
_s2='observation_delay_seconds'
_s3='0x0000000000000000000000000000000000000000'
_s4='ci_assurance_evidence_required'
_s5='independent_assurance_required'
_s6='installed_candidate_hashes'
_s7='active_proposal_by_target'
_s8='NONCANONICAL'
_s9='expected_kernel_hash'
_s10='policy_fingerprint'
_s11='used_evidence_ids'
_s12='used_incident_ids'
_s13='0123456789abcdef'
_s14='candidate_sha256'
_s15='REPAIR_REQUIRED'
_s16='proposal_count'
_s17='release_count'
_s18='EXACT_PARENT'
_s19='incidents'
_s20='proposals'
_s21='_INVALID'
_s22='policies'
_s23='releases'
from genlayer import*
_fk='EVIDENCE_'
_fm='MANIFEST_'
_fi='ASSURANCE_'
_fl='INCIDENT_'
_fn='RECOVERY_'
_fj='CANDIDATE_'
_fh='CI_'
_fg='AUDIT_'
from dataclasses import dataclass
import hashlib
import json
_bu='proofpatch-v2'
_dm='proofpatch-assurance-v1'
_dw='ACTIVE'
_dn='PROVISIONAL'
_dq='RECOVERED'
_cg='PROPOSED'
_dt=_fk+_s15
_da='INSTALLED_PROVISIONAL'
_dd=_fi+'PENDING'
_de=_fi+_s15
_dh=_fi+'RETRY_REQUIRED'
_do='CERTIFIED'
_bq=_fl+'OPEN'
_dg=16000
_cd=512000
_ds=1024
_dv=160
_bs=96
_db=30*24*60*60
_dc=14*24*60*60
_bp=7*24*60*60
_bh=60

@allow_storage
@dataclass
class _gb:
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
class _fv:
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
class _fz:
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
class _fx:
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

class ProofPatchPolicyLogic:

    def __init__(self):
        self.proposal_count=u256(0)
        self.release_count=u256(0)

    def _fp(self):
        return self.now

    def _fd(self,_am):
        return hashlib.sha256(_am).hexdigest()

    def _ev(self,_v):
        return hashlib.sha256('\x1f'.join(_v).encode('utf-8')).hexdigest()

    def _fb(self,_b):
        if len(_b)!=64:
            return False
        for _bf in _b:
            if _bf not in _s13:
                return False
        return True

    def _ek(self,_b):
        try:
            _ay=json.loads(_b)
            _cm=json.dumps(_ay,sort_keys=True,separators=(',',':'),ensure_ascii=False)
            if _cm!=_b:
                return(_s8,_ay)
            return(self._fd(_cm.encode('utf-8')),_ay)
        except Exception:
            return('INVALID',None)

    def _eq(self,_cr,_dp,_df,_dk,_dj,_a):
        if len(_cr.encode('utf-8'))>int(_a.far):
            return _fm+'TOO_LARGE'
        (_du,_ay)=self._ek(_cr)
        if _du in('INVALID',_s8)or not isinstance(_ay,dict):
            return _fm+'NOT_CANONICAL_JSON'
        _h=_ay
        _dy=('schema','target',_s14,_s10,_s9,'expected_release_version',_s2,_s1,_s4,_s5)
        for _cy in _dy:
            if _cy not in _h:
                return _fm+'MISSING_'+_cy.upper()
        if _h.get('schema')!=_dm:
            return _fm+'SCHEMA_MISMATCH'
        _cj=_h.get('target')
        if not isinstance(_cj,str)or _cj.lower()!=str(_dp).lower():
            return _fm+'TARGET_MISMATCH'
        if _h.get(_s14)!=_df:
            return _fm+'CANDIDATE_HASH_MISMATCH'
        if _h.get(_s10)!=_dk:
            return _fm+'POLICY_MISMATCH'
        if _h.get(_s9)!=_dj:
            return _fm+'KERNEL_MISMATCH'
        if type(_h.get(_s2))is not int:
            return _fm+'OBSERVATION_DELAY_INVALID'
        if type(_h.get(_s1))is not int:
            return _fm+'ASSURANCE_DEADLINE_INVALID'
        if _h.get(_s2)!=int(_a.fh):
            return _fm+'OBSERVATION_DELAY_MISMATCH'
        if _h.get(_s1)!=int(_a.fe):
            return _fm+'ASSURANCE_DEADLINE_MISMATCH'
        if _h.get(_s4)is not True:
            return _fm+'CI_ASSURANCE_REQUIRED'
        if _h.get(_s5)is not True:
            return _fm+'INDEPENDENT_ASSURANCE_REQUIRED'
        for _bo in('required_state_checks','required_readback_checks','required_canary_checks'):
            _cp=_h.get(_bo,[])
            if not isinstance(_cp,list):
                return 'MANIFEST_'+_bo.upper()+_s21
            _b=_cp
            if len(_b)>32:
                return 'MANIFEST_'+_bo.upper()+_s21
            for _cx in _b:
                if not isinstance(_cx,str)or len(_cx.encode('utf-8'))>160:
                    return 'MANIFEST_'+_bo.upper()+'_ITEM_INVALID'
        return ''

    def _fc(self,_b,_cb,_ca,_bz):
        _ck=len(_b.encode('utf-8'))
        if _ck<_ca or _ck>_bz:
            raise gl.vm.UserError(f'{_cb} length is invalid')

    def _fa(self,_b,_cb,_ca,_bz):
        if _b<_ca or _b>_bz:
            raise gl.vm.UserError(f'{_cb} is outside supported bounds')

    def _eh(self,_b):
        if not _b or _b in('.','..'):
            return False
        _dz='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'
        for _bf in _b:
            if _bf not in _dz:
                return False
        return True

    def _es(self,_u):
        _cw='https://raw.githubusercontent.com/'
        if not _u.startswith(_cw)or not _u.endswith('/'):
            return ''
        _ef=_u[len(_cw):]
        _v=_ef.split('/')
        if len(_v)!=3 or _v[2]!='':
            return ''
        _al=_v[0]
        _dx=_v[1]
        if not self._eh(_al):
            return ''
        if not self._eh(_dx):
            return ''
        return _al

    def _el(self,_u):
        return self._es(_u)!=''

    def _er(self,_cc,_u):
        if len(_cc.encode('utf-8'))>_ds:
            return False
        if not self._el(_u):
            return False
        if not _cc.startswith(_u):
            return False
        _ec=_cc[len(_u):]
        _v=_ec.split('/',1)
        if len(_v)!=2:
            return False
        (_cu,_ee)=_v
        if len(_cu)!=40:
            return False
        for _bf in _cu:
            if _bf not in _s13:
                return False
        _ci=_ee.split('/')
        if not _ci:
            return False
        for _ea in _ci:
            if not self._eh(_ea):
                return False
        return True

    def _en(self,_d,_al,_aw,_ae,_ah,_af,_q,_ai,_z,_ap,_ar,_ao,_ad,_s,_ac,_w,_x,_ab,_an,_at,_au):
        return self._ev([_bu,str(_d),str(_al),_aw,_ae,_ah,_af,_q,_ai,_z,str(_ap),str(_ar),str(_ao),_ad,_s,_ac,_w,_x,str(_ab),str(_an),str(_at),str(_au)])

    def _eo(self,_n,_p,_k,_o,_j,_m,_aq):
        return self._ev([_bu,_n,_p,_k,_o,_j,_m,_aq])

    def _ep(self):
        return u256(0)

    def _ej(self,_d):
        if _d not in self.policies:
            raise gl.vm.UserError(_s0)
        _a=self.policies[_d]
        if self.actor!=_a.fat:
            raise gl.vm.UserError(_s0)
        if not _a.fa:
            raise gl.vm.UserError(_s0)
        return _a

    def _et(self,_l):
        if _l not in self.proposals:
            raise gl.vm.UserError(_s0)
        return self.proposals[_l]

    def _em(self,_d,_eb,_ed,_cl):
        self._fc(_cl,'evidence_id',8,_dv)
        _co=self._ev([str(_d),_eb,_ed,_cl])
        if self.used_evidence_ids.get(_co,False):
            raise gl.vm.UserError(_s0)
        self.used_evidence_ids[_co]=True

    def _ei(self,_d,_ag):
        return self._ev([str(_d),_ag])

    def _ez(self,_d,_di,_t,_cf,_ct,_cn,_ba,_bb,_m,_aq):
        return self._ev([_bu,str(_d),_di,_t,_cf,_ct,_cn,_ba,_bb,_m,_aq])

    def _ew(self,_al,_aw,_ae,_ah,_af,_q,_ai,_z,_ad,_s,_ac,_w,_x,_bc,_bj,_y,_ap,_ar,_ao,_ab,_an,_at,_au):
        _d=self.actor
        _bw=Address(_al)
        if _d in self.policies:
            raise gl.vm.UserError(_s0)
        if _bw==Address(_s3):
            raise gl.vm.UserError(_s0)
        self._fc(_aw,'constitution',80,_dg)
        self._fc(_ae,'source_authority',3,160)
        self._fc(_ah,'ci_authority',3,160)
        self._fc(_af,'audit_authority',3,160)
        self._fc(_ad,'assurance_authority',3,160)
        self._fc(_ac,'assurance_corroboration_authority',3,160)
        self._fc(_bc,'current_version',1,_bs)
        if len({_ae,_ah,_af,_ad,_ac})!=5:
            raise gl.vm.UserError(_s0)
        if not self._el(_q):
            raise gl.vm.UserError(_s0)
        if not self._el(_ai):
            raise gl.vm.UserError(_s0)
        if not self._el(_z):
            raise gl.vm.UserError(_s0)
        if not self._el(_s):
            raise gl.vm.UserError(_s0)
        if not self._el(_w):
            raise gl.vm.UserError(_s0)
        if len({_q,_ai,_z,_s,_w})!=5:
            raise gl.vm.UserError(_s0)
        if self._es(_q).lower()==self._es(_z).lower():
            raise gl.vm.UserError(_s0)
        if self._es(_q).lower()==self._es(_s).lower():
            raise gl.vm.UserError(_s0)
        if self._es(_s).lower()==self._es(_w).lower():
            raise gl.vm.UserError(_s0)
        _x=_x.lower()
        if not self._fb(_x):
            raise gl.vm.UserError(_s0)
        _y=_y.lower()
        if not self._fb(_y):
            raise gl.vm.UserError(_s0)
        if not self._er(_bj,_q):
            raise gl.vm.UserError(_s0)
        self._fa(_ap,'max_evidence_age_seconds',_bh,_db)
        self._fa(_ar,'proposal_ttl_seconds',_bh,_dc)
        self._fa(_ao,'execution_timeout_seconds',_bh,_bp)
        self._fa(_ab,'assurance_observation_delay_seconds',_bh,_bp)
        self._fa(_an,_s1,_ab,_bp)
        self._fa(_at,'max_manifest_bytes',256,128000)
        self._fa(_au,'max_capsule_bytes',1,_cd)
        _bx=self._en(_d,_bw,_aw,_ae,_ah,_af,_q,_ai,_z,_ap,_ar,_ao,_ad,_s,_ac,_w,_x,_ab,_an,_at,_au)
        self.policies[_d]=_gb(fat=_bw,fbw=_d,fx=_aw,fay=_bx,fbs=_ae,fs=_ah,fj=_af,fbt=_q,fv=_ai,fm=_z,fb=_ad,fi=_s,fc=_ac,fd=_w,fbb=_x,fae=_bc,fad=_bj,fab=_y,fac='',faq=u64(_ap),fbd=u64(_ar),fah=u64(_ao),fh=u64(_ab),fe=u64(_an),far=u64(_at),fap=u64(_au),fa=True)
        _bm='root-'+_y[:16]
        _dl=self._ez(_d,'',_bm,'',_bc,_y,_bx,'','','')
        self.releases[_bm]=_fz(fbq=_bm,fbw=_d,fbx=_bc,fav='',fau='',fbu=_bj,fw=_y,fbc=u256(0),fay=_bx,faf='',fg='',fbh='',fal=u64(self.now),fr=u64(self.now),fbv='REGISTERED_PARENT',fbf='',fbl='',fao=_dl)
        self.policies[_d].fac=_bm
        self.active_proposal_by_target[_d]=self._ep()

    def _eu(self,_d,_bk,_n,_bd,_p,_k,_o,_j,_bi,_bn,_bg,_bl,_br,_be):
        _e=Address(_d)
        _a=self._ej(_e)
        active=self.active_proposal_by_target.get(_e,self._ep())
        if active!=self._ep():
            raise gl.vm.UserError(_s0)
        self._fc(_bk,'candidate_version',1,_bs)
        if _bk==_a.fae:
            raise gl.vm.UserError(_s0)
        if len(_bd)==0 or len(_bd)>_cd:
            raise gl.vm.UserError(_s0)
        if not self._er(_n,_a.fbt):
            raise gl.vm.UserError(_s0)
        if not self._er(_p,_a.fv):
            raise gl.vm.UserError(_s0)
        if not self._er(_o,_a.fm):
            raise gl.vm.UserError(_s0)
        if not self._er(_br,_a.fbt):
            raise gl.vm.UserError(_s0)
        if _k==_j:
            raise gl.vm.UserError(_s0)
        if _bn not in(_s18,_fn+'CANDIDATE'):
            raise gl.vm.UserError(_s0)
        if len(_be)==0 or len(_be)>int(_a.fap):
            raise gl.vm.UserError(_s0)
        self._fc(_bl,'recovery_version',1,_bs)
        _ag=self._fd(_bd)
        if _ag==_a.fab:
            raise gl.vm.UserError(_s0)
        if self.installed_candidate_hashes.get(self._ei(_e,_ag),False):
            raise gl.vm.UserError(_s0)
        _av=self._fd(_be)
        if _bn==_s18:
            if _bg!=_a.fac:
                raise gl.vm.UserError(_s0)
            if _av!=_a.fab:
                raise gl.vm.UserError(_s0)
            if _bl!=_a.fae:
                raise gl.vm.UserError(_s0)
        else:
            if _bg!='recovery-'+_av[:16]:
                raise gl.vm.UserError(_s0)
            if _av==_ag:
                raise gl.vm.UserError(_s0)
        (_m,_fq)=self._ek(_bi)
        if _m in('INVALID',_s8):
            raise gl.vm.UserError(_s0)
        _ch=self._eq(_bi,_e,_ag,_a.fay,_a.fbb,_a)
        if _ch:
            raise gl.vm.UserError(_ch)
        self._em(_e,_a.fs,'ci',_k)
        self._em(_e,_a.fj,'audit',_j)
        _cz=self.now
        _l=u256(int(self.proposal_count)+1)
        _bb=self._eo(_n,_p,_k,_o,_j,_m,_av)
        self.proposals[_l]=_fv(fbc=_l,fbw=_e,fbe=_a.fat,fax=_a.fae,faw=_a.fad,fau=_a.fab,fq=_bk,fp=_n,fn=_bd,fo=_ag,fu=_p,ft=_k,fl=_o,fk=_j,ff=_bi,fg=_m,fbm=_bn,fbn=_bg,fbp=_bl,fbo=_br,fbi=_be,fbj=_av,fbh=_av,faf=_bb,fay=_a.fay,faa=u64(_cz),fai=u64(_cz+int(_a.fbd)),fbr=u64(0),fag=u64(0),fbv=_cg,fan='')
        self.proposal_count=_l
        self.active_proposal_by_target[_e]=_l
        return _l

    def _ex(self,_l,_n,_p,_k,_o,_j):
        _f=self._et(_l)
        _a=self._ej(_f.fbw)
        if _f.fbv!=_dt:
            raise gl.vm.UserError(_s0)
        if self.now>int(_f.fai):
            raise gl.vm.UserError(_s0)
        if not self._er(_n,_a.fbt):
            raise gl.vm.UserError(_s0)
        if not self._er(_p,_a.fv):
            raise gl.vm.UserError(_s0)
        if not self._er(_o,_a.fm):
            raise gl.vm.UserError(_s0)
        if _k==_j:
            raise gl.vm.UserError(_s0)
        self._em(_f.fbw,_a.fs,'ci',_k)
        self._em(_f.fbw,_a.fj,'audit',_j)
        _f.fp=_n
        _f.fu=_p
        _f.ft=_k
        _f.fl=_o
        _f.fk=_j
        _f.faf=self._eo(_n,_p,_k,_o,_j,_f.fg,_f.fbh)
        _f.fbv=_cg
        _f.fan=''

    def _ey(self,_d,_t,_bv,_by,_as,_bt,_az):
        _e=Address(_d)
        if _e not in self.policies or _t not in self.releases:
            raise gl.vm.UserError(_s0)
        _aa=self.releases[_t]
        if _aa.fbw!=_e:
            raise gl.vm.UserError(_s0)
        if _bv not in('STATE_INVARIANT_VIOLATION','AUTHORIZATION_REGRESSION','UPGRADE_BYPASS','CONSENSUS_BINDING_REGRESSION',_fk+'TRUST_REGRESSION','FINALITY_REGRESSION','LIVENESS_REGRESSION','HIDDEN_VALUE_TRANSFER','KERNEL_INTEGRITY_FAILURE','REQUIRED_INTERFACE_FAILURE','OTHER_CONSTITUTIONAL_BREACH'):
            raise gl.vm.UserError(_s0)
        _a=self.policies[_e]
        if not self._er(_by,_a.fm):
            raise gl.vm.UserError(_s0)
        if not self._er(_bt,_a.fd):
            raise gl.vm.UserError(_s0)
        if _as==_az:
            raise gl.vm.UserError(_s0)
        self._em(_e,_a.fj,'incident_primary',_as)
        self._em(_e,_a.fc,'incident_corroboration',_az)
        if self.target_release_id!=_t:
            raise gl.vm.UserError(_s0)
        if self.target_mode not in(_dw,_dn,_dq):
            raise gl.vm.UserError(_s0)
        if _aa.fbh=='':
            raise gl.vm.UserError(_s0)
        if _aa.fbv not in(_do,_da,_dd,_de,_dh,_bq):
            raise gl.vm.UserError(_s0)
        incident_id='incident-'+str(self.now)+'-'+_as
        if incident_id in self.incidents:
            raise gl.vm.UserError(_s0)
        _ce=self._ev([str(_e),_t,_as,_az])
        if self.used_incident_ids.get(_ce,False):
            raise gl.vm.UserError(_s0)
        self.used_incident_ids[_ce]=True
        self.incidents[incident_id]=_fx(faj=incident_id,fbw=_e,fbq=_t,fam=_aa.fw,fak=_bv,fba=_by,faz=_as,fz=_bt,fy=_az,fay=_aa.fay,fg=_aa.fg,fbh=_aa.fbh,fas=u64(self.now),fai=u64(self.now+int(_a.fbd)),fbr=u64(0),fbk=u64(0),fbv=_bq,fan='',fbg=False)
        _aa.fbv=_bq
        return incident_id
_cv=_s3

@gl.contract_interface
class _ft:

    class _gd:

        def apply_policy_result(self,_ax:str,_cs:str)->None:
            ...

class _fr(gl.Contract):
    admin:Address
    _cq:Address

    def __init__(self):
        self.admin=gl.message.sender_address
        self.governor=Address(_cv)

    @gl.public.write
    def bind_governor(self,_cq:str)->None:
        if gl.message.sender_address!=self.admin:
            raise gl.vm.UserError(_s0)
        if self.governor!=Address(_cv):
            raise gl.vm.UserError(_s0)
        self.governor=Address(_cq)

    def _fe(self,_b):
        if isinstance(_b,Address):
            return str(_b)
        if isinstance(_b,bytes):
            return _b.hex()
        if isinstance(_b,(u256,u64)):
            return int(_b)
        if isinstance(_b,dict):
            return{str(_i):self._fe(_g)for(_i,_g)in _b.items()}
        if isinstance(_b,list):
            return[self._fe(_g)for _g in _b]
        if hasattr(_b,'__dict__'):
            return{_i:self._fe(_g)for(_i,_g)in _b.__dict__.items()}
        return _b

    def _ff(self,cls,_eg):
        _b=dict(_eg)
        _dr={'TargetPolicy':('owner','target'),'UpgradeProposal':('target','proposer'),'ReleaseRecord':('target',),'IncidentRecord':('target',)}
        for _ak in _dr.get(cls.__name__,()):
            _b[_ak]=Address(_b[_ak])
        for _ak in('candidate_code','recovery_code'):
            if _ak in _b and isinstance(_b[_ak],str):
                _b[_ak]=bytes.fromhex(_b[_ak])
        return cls(**_b)

    def _fo(self,_c,_aj):
        _r=_aj.get('state',{})
        _c.policies={Address(_i):self._ff(_gb,_g)for(_i,_g)in _r.get(_s22,{}).items()}
        _c.proposals={u256(int(_i)):self._ff(_fv,_g)for(_i,_g)in _r.get(_s20,{}).items()}
        _c.releases={_i:self._ff(_fz,_g)for(_i,_g)in _r.get(_s23,{}).items()}
        _c.incidents={_i:self._ff(_fx,_g)for(_i,_g)in _r.get(_s19,{}).items()}
        _c.active_proposal_by_target={Address(_i):u256(_g)for(_i,_g)in _r.get(_s7,{}).items()}
        _c.used_evidence_ids=dict(_r.get(_s11,{}))
        _c.installed_candidate_hashes=dict(_r.get(_s6,{}))
        _c.used_incident_ids=dict(_r.get(_s12,{}))
        _c.proposal_count=u256(_r.get(_s16,0))
        _c.release_count=u256(_r.get(_s17,0))
        _c.actor=Address(_aj['actor'])
        _c.now=int(_aj['now'])
        _c.target_release_id=str(_aj.get('target_release_id',''))
        _c.target_mode=str(_aj.get('target_mode',''))

    @gl.public.write
    def execute(self,_ax:str,_aj:str)->None:
        if gl.message.sender_address!=self.governor:
            raise gl.vm.UserError(_s0)
        _am=json.loads(_aj)
        _c=ProofPatchPolicyLogic()
        self._fo(_c,_am)
        if _ax=='register':
            _c._ew(*_am['args'])
        elif _ax=='create':
            _c._eu(*_am['args'])
        elif _ax=='repair':
            _c._ex(*_am['args'])
        elif _ax=='incident':
            _c._ey(*_am['args'])
        else:
            raise gl.vm.UserError(_s0)
        _cs=json.dumps(self._fe({_s22:_c.policies,_s20:_c.proposals,_s23:_c.releases,_s19:_c.incidents,_s7:_c.active_proposal_by_target,_s11:_c.used_evidence_ids,_s6:_c.installed_candidate_hashes,_s12:_c.used_incident_ids,_s16:_c.proposal_count,_s17:_c.release_count}),sort_keys=True,separators=(',',':'))
        _ft(self.governor).emit(on='finalized').apply_policy_result(_ax,_cs)
