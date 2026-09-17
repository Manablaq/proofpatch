# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_s0='ProofPatch invariant'
_s1='0x0000000000000000000000000000000000000000'
_s2='0123456789abcdef'
_s3='REPAIR_REQUIRED'
_s4='incidents'
_s5='operation'
_s6='proposals'
_s7='policies'
_s8='releases'
from genlayer import*
_df='EVIDENCE_'
_dh='MANIFEST_'
_dd='ASSURANCE_'
_dg='INCIDENT_'
_di='RECOVERY_'
_de='CANDIDATE_'
_db='CI_'
_da='AUDIT_'
from dataclasses import dataclass
import hashlib
import json
_ay='proofpatch-v2'
_cj='proofpatch-assurance-v1'
_cv='ACTIVE'
_ck='PROVISIONAL'
_cp='RECOVERED'
_co='PROPOSED'
_cq=_df+_s3
_by='INSTALLED_PROVISIONAL'
_ca=_dd+'PENDING'
_cb=_dd+_s3
_cc=_dd+'RETRY_REQUIRED'
_cl='CERTIFIED'
_cd=_dg+'OPEN'
_bj=16000
_bl=512000
_bo=1024
_cs=160
_bm=96
_bh=30*24*60*60
_bi=14*24*60*60
_am=7*24*60*60
_aj=60

@allow_storage
@dataclass
class _dz:
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
class _dt:
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
class _dx:
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
class _dv:
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
_au=_s1

@gl.contract_interface
class _dr:

    class _ed:

        def proofpatch_installed_release_id(self)->str:
            ...

        def proofpatch_release_mode(self)->str:
            ...

@gl.contract_interface
class _dp:

    class _ed:

        def get_state_record(self,_dk:str,_bg:str)->str:
            ...

    class _eb:

        def apply_policy_result(self,_t:str,_cz:str)->None:
            ...

class _dn:

    def _cm(self,_g):
        return hashlib.sha256('\x1f'.join(_g).encode('utf-8')).hexdigest()

    def _cu(self,_a):
        if len(_a)!=64:
            return False
        for _af in _a:
            if _af not in _s2:
                return False
        return True

    def _cw(self,_a,_at,_as,_ar):
        _ba=len(_a.encode('utf-8'))
        if _ba<_as or _ba>_ar:
            raise gl.vm.UserError(f'{_at} length is invalid')

    def _ct(self,_a,_at,_as,_ar):
        if _a<_as or _a>_ar:
            raise gl.vm.UserError(f'{_at} is outside supported bounds')

    def _bz(self,_a):
        if not _a or _a in('.','..'):
            return False
        _bq='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'
        for _af in _a:
            if _af not in _bq:
                return False
        return True

    def _ci(self,_f):
        _bf='https://raw.githubusercontent.com/'
        if not _f.startswith(_bf)or not _f.endswith('/'):
            return ''
        _bw=_f[len(_bf):]
        _g=_bw.split('/')
        if len(_g)!=3 or _g[2]!='':
            return ''
        _v=_g[0]
        _bp=_g[1]
        if not self._bz(_v):
            return ''
        if not self._bz(_bp):
            return ''
        return _v

    def _ce(self,_f):
        return self._ci(_f)!=''

    def _ch(self,_av,_f):
        if len(_av.encode('utf-8'))>_bo:
            return False
        if not self._ce(_f):
            return False
        if not _av.startswith(_f):
            return False
        _bt=_av[len(_f):]
        _g=_bt.split('/',1)
        if len(_g)!=2:
            return False
        (_be,_bv)=_g
        if len(_be)!=40:
            return False
        for _af in _be:
            if _af not in _s2:
                return False
        _az=_bv.split('/')
        if not _az:
            return False
        for _bs in _az:
            if not self._bz(_bs):
                return False
        return True

    def _cf(self,_c,_v,_ac,_p,_r,_q,_d,_s,_k,_y,_z,_x,_o,_e,_n,_h,_i,_m,_w,_aa,_ab):
        return self._cm([_ay,str(_c),str(_v),_ac,_p,_r,_q,_d,_s,_k,str(_y),str(_z),str(_x),_o,_e,_n,_h,_i,str(_m),str(_w),str(_aa),str(_ab)])

    def _cg(self):
        return u256(0)

    def _cr(self,_c,_bk,_aq,_ax,_bd,_bc,_ad,_an,_ah,_ai):
        return self._cm([_ay,str(_c),_bk,_aq,_ax,_bd,_bc,_ad,_an,_ah,_ai])

    def _cn(self,_v,_ac,_p,_r,_q,_d,_s,_k,_o,_e,_n,_h,_i,_ae,_ak,_j,_y,_z,_x,_m,_w,_aa,_ab):
        _c=self.actor
        _ao=Address(_v)
        if _c in self.policies:
            raise gl.vm.UserError(_s0)
        if _ao==Address(_s1):
            raise gl.vm.UserError(_s0)
        self._cw(_ac,'constitution',80,_bj)
        self._cw(_p,'source_authority',3,160)
        self._cw(_r,'ci_authority',3,160)
        self._cw(_q,'audit_authority',3,160)
        self._cw(_o,'assurance_authority',3,160)
        self._cw(_n,'assurance_corroboration_authority',3,160)
        self._cw(_ae,'current_version',1,_bm)
        if len({_p,_r,_q,_o,_n})!=5:
            raise gl.vm.UserError(_s0)
        if not self._ce(_d):
            raise gl.vm.UserError(_s0)
        if not self._ce(_s):
            raise gl.vm.UserError(_s0)
        if not self._ce(_k):
            raise gl.vm.UserError(_s0)
        if not self._ce(_e):
            raise gl.vm.UserError(_s0)
        if not self._ce(_h):
            raise gl.vm.UserError(_s0)
        if len({_d,_s,_k,_e,_h})!=5:
            raise gl.vm.UserError(_s0)
        if self._ci(_d).lower()==self._ci(_k).lower():
            raise gl.vm.UserError(_s0)
        if self._ci(_d).lower()==self._ci(_e).lower():
            raise gl.vm.UserError(_s0)
        if self._ci(_e).lower()==self._ci(_h).lower():
            raise gl.vm.UserError(_s0)
        _i=_i.lower()
        if not self._cu(_i):
            raise gl.vm.UserError(_s0)
        _j=_j.lower()
        if not self._cu(_j):
            raise gl.vm.UserError(_s0)
        if not self._ch(_ak,_d):
            raise gl.vm.UserError(_s0)
        self._ct(_y,'max_evidence_age_seconds',_aj,_bh)
        self._ct(_z,'proposal_ttl_seconds',_aj,_bi)
        self._ct(_x,'execution_timeout_seconds',_aj,_am)
        self._ct(_m,'assurance_observation_delay_seconds',_aj,_am)
        self._ct(_w,'assurance_deadline_seconds',_m,_am)
        self._ct(_aa,'max_manifest_bytes',256,128000)
        self._ct(_ab,'max_capsule_bytes',1,_bl)
        _ap=self._cf(_c,_ao,_ac,_p,_r,_q,_d,_s,_k,_y,_z,_x,_o,_e,_n,_h,_i,_m,_w,_aa,_ab)
        self.policies[_c]=_dz(fat=_ao,fbw=_c,fx=_ac,fay=_ap,fbs=_p,fs=_r,fj=_q,fbt=_d,fv=_s,fm=_k,fb=_o,fi=_e,fc=_n,fd=_h,fbb=_i,fae=_ae,fad=_ak,fab=_j,fac='',faq=u64(_y),fbd=u64(_z),fah=u64(_x),fh=u64(_m),fe=u64(_w),far=u64(_aa),fap=u64(_ab),fa=True)
        _al='root-'+_j[:16]
        _bn=self._cr(_c,'',_al,'',_ae,_j,_ap,'','','')
        self.releases[_al]=_dx(fbq=_al,fbw=_c,fbx=_ae,fav='',fau='',fbu=_ak,fw=_j,fbc=u256(0),fay=_ap,faf='',fg='',fbh='',fal=u64(self.now),fr=u64(self.now),fbv='REGISTERED_PARENT',fbf='',fbl='',fao=_bn)
        self.policies[_c].fac=_al
        self.active_proposal_by_target[_c]=self._cg()

class _dl(gl.Contract):
    admin:Address
    governor:Address

    def __init__(self):
        self.admin=gl.message.sender_address
        self.governor=Address(_au)

    @gl.public.write
    def bind_governor(self,governor:str)->None:
        if gl.message.sender_address!=self.admin:
            raise gl.vm.UserError(_s0)
        if self.governor!=Address(_au):
            raise gl.vm.UserError(_s0)
        _bb=Address(governor)
        if _bb==Address(_au):
            raise gl.vm.UserError(_s0)
        self.governor=_bb

    def _dj(self,_b,_l):
        _b.policies={}
        _b.proposals={}
        _b.releases={}
        _b.incidents={}
        _b.active_proposal_by_target={}
        _b.used_evidence_ids={}
        _b.installed_candidate_hashes={}
        _b.used_incident_ids={}
        _b.proposal_count=u256(0)
        _b.release_count=u256(0)
        _b.actor=Address(_l['actor'])
        _b.now=int(_l['now'])
        _b.target_release_id=''
        _b.target_mode=''

    def _cx(self,_a):
        if isinstance(_a,Address):
            return str(_a)
        if isinstance(_a,bytes):
            return _a.hex()
        if isinstance(_a,bool):
            return _a
        if isinstance(_a,int):
            return int(_a)
        if isinstance(_a,dict):
            return{str(_aw):self._cx(_ag)for(_aw,_ag)in _a.items()}
        if isinstance(_a,list):
            return[self._cx(_ag)for _ag in _a]
        if hasattr(_a,'__dict__'):
            return{_aw:self._cx(_ag)for(_aw,_ag)in _a.__dict__.items()}
        return _a

    def _cy(self,cls,_bx):
        _a=list(_bx.values())
        if cls is _dz or cls is _dt or cls is _dx or(cls is _dv):
            _a[1]=Address(_a[1])
        if cls is _dz:
            _a[0]=Address(_a[0])
        elif cls is _dt:
            _a[2]=Address(_a[2])
            if isinstance(_a[8],str):
                _a[8]=bytes.fromhex(_a[8])
            if isinstance(_a[20],str):
                _a[20]=bytes.fromhex(_a[20])
        return cls(**dict(zip(cls.__annotations__.keys(),_a)))

    def _dc(self,_b,_t,_l):
        _u={_s5:_t,_s7:[],_s6:[],_s8:[],_s4:[],'active':[],'used_evidence_ids':_b.used_evidence_ids,'installed_candidate_hashes':_b.installed_candidate_hashes,'used_incident_ids':_b.used_incident_ids,'proposal_count':int(_b.proposal_count),'release_count':int(_b.release_count)}
        _u['registration_target']=str(_b.actor)
        for _a in _b.policies.values():
            _u[_s7].append(self._cx(_a))
        for _a in _b.proposals.values():
            _u[_s6].append(self._cx(_a))
        for _a in _b.releases.values():
            _u[_s8].append(self._cx(_a))
        for _a in _b.incidents.values():
            _u[_s4].append(self._cx(_a))
        for(_bg,_a)in _b.active_proposal_by_target.items():
            _u['active'].append([str(_bg),int(_a)])
        return _u

    @gl.public.write
    def execute(self,_t:str,_br:str)->None:
        if gl.message.sender_address!=self.governor:
            raise gl.vm.UserError(_s0)
        _l=json.loads(_br)
        _l[_s5]=_t
        _b=_dn()
        self._dj(_b,_l)
        _bu=_l['args']
        if _t=='register':
            _b._cn(*_bu)
        else:
            raise gl.vm.UserError(_s0)
        _dp(self.governor).emit(on='finalized').apply_policy_result(_t,json.dumps(self._dc(_b,_t,_l),separators=(',',':')))
