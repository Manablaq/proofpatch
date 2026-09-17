# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_s0='ProofPatch invariant'
_s1='used_evidence_ids'
_s2='installed_candidate_hashes'
_s3='assurance_deadline_seconds'
_s4='used_incident_ids'
_s5='observation_delay_seconds'
_s6='proposal_count'
_s7='release_count'
_s8='proposal'
_s9='ci_assurance_evidence_required'
_s10='independent_assurance_required'
_s11='audit_authority'
_s12='active_target'
_s13='NONCANONICAL'
_s14='evidence'
_s15='releases'
_s16='incident_corroboration'
_s17='expected_kernel_hash'
_s18='policy_fingerprint'
_s19='incidents'
_s20='operation'
_s21='target_release_id'
_s22='candidate_sha256'
_s23='incident_primary'
_s24='REPAIR_REQUIRED'
_s25='EXACT_PARENT'
_s26='active_value'
_s27='ci_authority'
_s28='target_mode'
_s29='proposals'
_s30='_INVALID'
_s31='incident'
_s32='policies'
from genlayer import*
_ei='EVIDENCE_'
_ek='MANIFEST_'
_eg='ASSURANCE_'
_ej='INCIDENT_'
_el='RECOVERY_'
_eh='CANDIDATE_'
_ee='CI_'
_ed='AUDIT_'
from dataclasses import dataclass
import hashlib
import json
_cj='proofpatch-v2'
_ce='proofpatch-assurance-v1'
_co='ACTIVE'
_cf='PROVISIONAL'
_ci='RECOVERED'
_be='PROPOSED'
_cl=_ei+_s24
_bw='INSTALLED_PROVISIONAL'
_bx=_eg+'PENDING'
_by=_eg+_s24
_ca=_eg+'RETRY_REQUIRED'
_cg='CERTIFIED'
_as=_ej+'OPEN'
_di=16000
_cd=512000
_ck=1024
_cn=160
_bd=96
_df=30*24*60*60
_dg=14*24*60*60
_dd=7*24*60*60
_dn=60

@allow_storage
@dataclass
class _fa:
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
class _eu:
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
class _ey:
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
class _ew:
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
_ax='0x0000000000000000000000000000000000000000'

@gl.contract_interface
class _es:

    class _fe:

        def proofpatch_installed_release_id(self)->str:
            ...

        def proofpatch_release_mode(self)->str:
            ...

@gl.contract_interface
class _eq:

    class _fe:

        def get_state_record(self,_n:str,_r:str)->str:
            ...

    class _fc:

        def apply_policy_result(self,_s:str,_ec:str)->None:
            ...

class ProofPatchPolicyLogic:

    def _dz(self,_b):
        return hashlib.sha256(_b).hexdigest()

    def _dv(self,_u):
        return hashlib.sha256('\x1f'.join(_u).encode('utf-8')).hexdigest()

    def _dk(self,_a):
        try:
            _ad=json.loads(_a)
            _bl=json.dumps(_ad,sort_keys=True,separators=(',',':'),ensure_ascii=False)
            if _bl!=_a:
                return(_s13,_ad)
            return(self._dz(_bl.encode('utf-8')),_ad)
        except Exception:
            return('INVALID',None)

    def _dq(self,_bo,_ch,_bz,_cc,_cb,_c):
        if len(_bo.encode('utf-8'))>int(_c.far):
            return _ek+'TOO_LARGE'
        (_cm,_ad)=self._dk(_bo)
        if _cm in('INVALID',_s13)or not isinstance(_ad,dict):
            return _ek+'NOT_CANONICAL_JSON'
        _i=_ad
        _cq=('schema','target',_s22,_s18,_s17,'expected_release_version',_s5,_s3,_s9,_s10)
        for _r in _cq:
            if _r not in _i:
                return _ek+'MISSING_'+_r.upper()
        if _i.get('schema')!=_ce:
            return _ek+'SCHEMA_MISMATCH'
        _bh=_i.get('target')
        if not isinstance(_bh,str)or _bh.lower()!=str(_ch).lower():
            return _ek+'TARGET_MISMATCH'
        if _i.get(_s22)!=_bz:
            return _ek+'CANDIDATE_HASH_MISMATCH'
        if _i.get(_s18)!=_cc:
            return _ek+'POLICY_MISMATCH'
        if _i.get(_s17)!=_cb:
            return _ek+'KERNEL_MISMATCH'
        if type(_i.get(_s5))is not int:
            return _ek+'OBSERVATION_DELAY_INVALID'
        if type(_i.get(_s3))is not int:
            return _ek+'ASSURANCE_DEADLINE_INVALID'
        if _i.get(_s5)!=int(_c.fh):
            return _ek+'OBSERVATION_DELAY_MISMATCH'
        if _i.get(_s3)!=int(_c.fe):
            return _ek+'ASSURANCE_DEADLINE_MISMATCH'
        if _i.get(_s9)is not True:
            return _ek+'CI_ASSURANCE_REQUIRED'
        if _i.get(_s10)is not True:
            return _ek+'INDEPENDENT_ASSURANCE_REQUIRED'
        for _aq in('required_state_checks','required_readback_checks','required_canary_checks'):
            _bn=_i.get(_aq,[])
            if not isinstance(_bn,list):
                return 'MANIFEST_'+_aq.upper()+_s30
            _a=_bn
            if len(_a)>32:
                return 'MANIFEST_'+_aq.upper()+_s30
            for _br in _a:
                if not isinstance(_br,str)or len(_br.encode('utf-8'))>160:
                    return 'MANIFEST_'+_aq.upper()+'_ITEM_INVALID'
        return ''

    def _dy(self,_a,_cx,_ct,_cs):
        _bi=len(_a.encode('utf-8'))
        if _bi<_ct or _bi>_cs:
            raise gl.vm.UserError(f'{_cx} length is invalid')

    def _de(self,_a):
        if not _a or _a in('.','..'):
            return False
        _cr='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'
        for _az in _a:
            if _az not in _cr:
                return False
        return True

    def _ds(self,_t):
        _bq='https://raw.githubusercontent.com/'
        if not _t.startswith(_bq)or not _t.endswith('/'):
            return ''
        _da=_t[len(_bq):]
        _u=_da.split('/')
        if len(_u)!=3 or _u[2]!='':
            return ''
        owner=_u[0]
        _cp=_u[1]
        if not self._de(owner):
            return ''
        if not self._de(_cp):
            return ''
        return owner

    def _dl(self,_t):
        return self._ds(_t)!=''

    def _dr(self,_ba,_t):
        if len(_ba.encode('utf-8'))>_ck:
            return False
        if not self._dl(_t):
            return False
        if not _ba.startswith(_t):
            return False
        _cw=_ba[len(_t):]
        _u=_cw.split('/',1)
        if len(_u)!=2:
            return False
        (_bp,_cz)=_u
        if len(_bp)!=40:
            return False
        for _az in _bp:
            if _az not in '0123456789abcdef':
                return False
        _bg=_cz.split('/')
        if not _bg:
            return False
        for _cv in _bg:
            if not self._de(_cv):
                return False
        return True

    def _do(self,_o,_q,_l,_p,_k,_v,_ak):
        return self._dv([_cj,_o,_q,_l,_p,_k,_v,_ak])

    def _dp(self):
        return u256(0)

    def _dj(self,_e):
        if _e not in self.policies:
            raise gl.vm.UserError(_s0)
        _c=self.policies[_e]
        if self.actor!=_c.fat:
            raise gl.vm.UserError(_s0)
        if not _c.fa:
            raise gl.vm.UserError(_s0)
        return _c

    def _dt(self,_m):
        if _m not in self.proposals:
            raise gl.vm.UserError(_s0)
        return self.proposals[_m]

    def _dm(self,_e,_z,_n,_bj):
        self._dy(_bj,'evidence_id',8,_cn)
        _bm=self._dv([str(_e),_z,_n,_bj])
        if self.used_evidence_ids.get(_bm,False):
            raise gl.vm.UserError(_s0)
        self.used_evidence_ids[_bm]=True

    def _dh(self,_e,_x):
        return self._dv([str(_e),_x])

    def _du(self,_e,_an,_o,_ag,_q,_l,_p,_k,_am,_ap,_al,_ao,_at,_ah):
        _g=Address(_e)
        _c=self._dj(_g)
        active=self.active_proposal_by_target.get(_g,self._dp())
        if active!=self._dp():
            raise gl.vm.UserError(_s0)
        self._dy(_an,'candidate_version',1,_bd)
        if _an==_c.fae:
            raise gl.vm.UserError(_s0)
        if len(_ag)==0 or len(_ag)>_cd:
            raise gl.vm.UserError(_s0)
        if not self._dr(_o,_c.fbt):
            raise gl.vm.UserError(_s0)
        if not self._dr(_q,_c.fv):
            raise gl.vm.UserError(_s0)
        if not self._dr(_p,_c.fm):
            raise gl.vm.UserError(_s0)
        if not self._dr(_at,_c.fbt):
            raise gl.vm.UserError(_s0)
        if _l==_k:
            raise gl.vm.UserError(_s0)
        if _ap not in(_s25,_el+'CANDIDATE'):
            raise gl.vm.UserError(_s0)
        if len(_ah)==0 or len(_ah)>int(_c.fap):
            raise gl.vm.UserError(_s0)
        self._dy(_ao,'recovery_version',1,_bd)
        _x=self._dz(_ag)
        if _x==_c.fab:
            raise gl.vm.UserError(_s0)
        if self.installed_candidate_hashes.get(self._dh(_g,_x),False):
            raise gl.vm.UserError(_s0)
        _ac=self._dz(_ah)
        if _ap==_s25:
            if _al!=_c.fac:
                raise gl.vm.UserError(_s0)
            if _ac!=_c.fab:
                raise gl.vm.UserError(_s0)
            if _ao!=_c.fae:
                raise gl.vm.UserError(_s0)
        else:
            if _al!='recovery-'+_ac[:16]:
                raise gl.vm.UserError(_s0)
            if _ac==_x:
                raise gl.vm.UserError(_s0)
        (_v,_en)=self._dk(_am)
        if _v in('INVALID',_s13):
            raise gl.vm.UserError(_s0)
        _bf=self._dq(_am,_g,_x,_c.fay,_c.fbb,_c)
        if _bf:
            raise gl.vm.UserError(_bf)
        self._dm(_g,_c.fs,'ci',_l)
        self._dm(_g,_c.fj,'audit',_k)
        _bs=self.now
        _m=u256(int(self.proposal_count)+1)
        evidence_set_hash=self._do(_o,_q,_l,_p,_k,_v,_ac)
        self.proposals[_m]=_eu(fbc=_m,fbw=_g,fbe=_c.fat,fax=_c.fae,faw=_c.fad,fau=_c.fab,fq=_an,fp=_o,fn=_ag,fo=_x,fu=_q,ft=_l,fl=_p,fk=_k,ff=_am,fg=_v,fbm=_ap,fbn=_al,fbp=_ao,fbo=_at,fbi=_ah,fbj=_ac,fbh=_ac,faf=evidence_set_hash,fay=_c.fay,faa=u64(_bs),fai=u64(_bs+int(_c.fbd)),fbr=u64(0),fag=u64(0),fbv=_be,fan='')
        self.proposal_count=_m
        self.active_proposal_by_target[_g]=_m
        return _m

    def _dw(self,_m,_o,_q,_l,_p,_k):
        _h=self._dt(_m)
        _c=self._dj(_h.fbw)
        if _h.fbv!=_cl:
            raise gl.vm.UserError(_s0)
        if self.now>int(_h.fai):
            raise gl.vm.UserError(_s0)
        if not self._dr(_o,_c.fbt):
            raise gl.vm.UserError(_s0)
        if not self._dr(_q,_c.fv):
            raise gl.vm.UserError(_s0)
        if not self._dr(_p,_c.fm):
            raise gl.vm.UserError(_s0)
        if _l==_k:
            raise gl.vm.UserError(_s0)
        self._dm(_h.fbw,_c.fs,'ci',_l)
        self._dm(_h.fbw,_c.fj,'audit',_k)
        _h.fp=_o
        _h.fu=_q
        _h.ft=_l
        _h.fl=_p
        _h.fk=_k
        _h.faf=self._do(_o,_q,_l,_p,_k,_h.fg,_h.fbh)
        _h.fbv=_be
        _h.fan=''

    def _dx(self,_e,_y,_av,_aw,_ab,_au,_af):
        _g=Address(_e)
        if _g not in self.policies or _y not in self.releases:
            raise gl.vm.UserError(_s0)
        _w=self.releases[_y]
        if _w.fbw!=_g:
            raise gl.vm.UserError(_s0)
        if _av not in('STATE_INVARIANT_VIOLATION','AUTHORIZATION_REGRESSION','UPGRADE_BYPASS','CONSENSUS_BINDING_REGRESSION',_ei+'TRUST_REGRESSION','FINALITY_REGRESSION','LIVENESS_REGRESSION','HIDDEN_VALUE_TRANSFER','KERNEL_INTEGRITY_FAILURE','REQUIRED_INTERFACE_FAILURE','OTHER_CONSTITUTIONAL_BREACH'):
            raise gl.vm.UserError(_s0)
        _c=self.policies[_g]
        if not self._dr(_aw,_c.fm):
            raise gl.vm.UserError(_s0)
        if not self._dr(_au,_c.fd):
            raise gl.vm.UserError(_s0)
        if _ab==_af:
            raise gl.vm.UserError(_s0)
        self._dm(_g,_c.fj,_s23,_ab)
        self._dm(_g,_c.fc,_s16,_af)
        if self.target_release_id!=_y:
            raise gl.vm.UserError(_s0)
        if self.target_mode not in(_co,_cf,_ci):
            raise gl.vm.UserError(_s0)
        if _w.fbh=='':
            raise gl.vm.UserError(_s0)
        if _w.fbv not in(_cg,_bw,_bx,_by,_ca,_as):
            raise gl.vm.UserError(_s0)
        incident_id='incident-'+str(self.now)+'-'+_ab
        if incident_id in self.incidents:
            raise gl.vm.UserError(_s0)
        _bc=self._dv([str(_g),_y,_ab,_af])
        if self.used_incident_ids.get(_bc,False):
            raise gl.vm.UserError(_s0)
        self.used_incident_ids[_bc]=True
        self.incidents[incident_id]=_ew(faj=incident_id,fbw=_g,fbq=_y,fam=_w.fw,fak=_av,fba=_aw,faz=_ab,fz=_au,fy=_af,fay=_w.fay,fg=_w.fg,fbh=_w.fbh,fas=u64(self.now),fai=u64(self.now+int(_c.fbd)),fbr=u64(0),fbk=u64(0),fbv=_as,fan='',fbg=False)
        _w.fbv=_as
        return incident_id

class _eo(gl.Contract):
    admin:Address
    governor:Address

    def __init__(self):
        self.admin=gl.message.sender_address
        self.governor=Address(_ax)

    @gl.public.write
    def bind_governor(self,governor:str)->None:
        if gl.message.sender_address!=self.admin:
            raise gl.vm.UserError(_s0)
        if self.governor!=Address(_ax):
            raise gl.vm.UserError(_s0)
        _bk=Address(governor)
        if _bk==Address(_ax):
            raise gl.vm.UserError(_s0)
        self.governor=_bk

    def _em(self,_d,_b):
        _ar=str(_b.get(_s20,''))
        _f=_b['args']
        if _ar=='create':
            _f[3]=bytes.fromhex(_f[3])
            _f[13]=bytes.fromhex(_f[13])
        _aa=_eq(self.governor).view(state=StorageType.LATEST_FINAL)

        def get(_n,_r):
            return json.loads(_aa.get_state_record(_n,_r))
        _bv=get('counts','')
        _b[_s6]=_bv.get(_s6,0)
        _b[_s7]=_bv.get(_s7,0)
        _b[_s1]={}
        _b[_s2]={}
        _b[_s4]={}

        def flag(_n,_r,_db):
            if get(_n,_r).get('value',False):
                _b[_db][_r]=True

        def ekey(_e,_z,_n,_ai):
            return hashlib.sha256('\x1f'.join([_e,_z,_n,_ai]).encode()).hexdigest()
        if _ar=='create':
            _e=str(_f[0])
            _b['policy']=get('policy',_e)
            _j=get('active',_e)
            _b[_s12]=_e
            _b[_s26]=_j.get('value',0)
            flag(_s14,ekey(_e,_b['policy'][_s27],'ci',_f[5]),_s1)
            flag(_s14,ekey(_e,_b['policy'][_s11],'audit',_f[7]),_s1)
            flag('candidate',hashlib.sha256('\x1f'.join([_e,hashlib.sha256(_f[3]).hexdigest()]).encode()).hexdigest(),_s2)
        elif _ar in('repair',):
            _b[_s8]=get(_s8,str(int(_f[0])))
            _e=_b[_s8]['target']
            _b['policy']=get('policy',_e)
            _cy=((_b['policy'][_s27],'ci',_f[3]),(_b['policy'][_s11],'audit',_f[5]))
            for(_z,_n,_ai)in _cy:
                flag(_s14,ekey(_e,_z,_n,_ai),_s1)
        elif _ar==_s31:
            _e=str(_f[0])
            _bt=str(_f[1])
            _b['policy']=get('policy',_e)
            _b[_s15]=[get('release',_bt)]
            for(_z,_n,_ai)in((_b['policy'][_s11],_s23,_f[4]),(_b['policy']['assurance_corroboration_authority'],_s16,_f[6])):
                flag(_s14,ekey(_e,_z,_n,_ai),_s1)
            _dc=hashlib.sha256('\x1f'.join([_e,_bt,_f[4],_f[6]]).encode()).hexdigest()
            flag('incident_evidence',_dc,_s4)
            _bu=_es(Address(_e)).view(state=StorageType.LATEST_FINAL)
            _b[_s21]=_bu.proofpatch_installed_release_id()
            _b[_s28]=_bu.proofpatch_release_mode()
        _d.policies={}
        _d.proposals={}
        _d.releases={}
        _d.incidents={}
        _d.active_proposal_by_target={}
        _d.used_evidence_ids=dict(_b.get(_s1,{}))
        _d.installed_candidate_hashes=dict(_b.get(_s2,{}))
        _d.used_incident_ids=dict(_b.get(_s4,{}))
        _d.proposal_count=u256(_b.get(_s6,0))
        _d.release_count=u256(_b.get(_s7,0))
        if _b.get('policy')is not None:
            _j=self._eb(_fa,_b['policy'])
            _d.policies[_j.fbw]=_j
        if _b.get(_s8)is not None:
            _j=self._eb(_eu,_b[_s8])
            _d.proposals[_j.fbc]=_j
        for _aj in _b.get(_s15,[]):
            _j=self._eb(_ey,_aj)
            _d.releases[_j.fbq]=_j
        for _aj in _b.get(_s19,[]):
            _j=self._eb(_ew,_aj)
            _d.incidents[_j.faj]=_j
        if _b.get(_s12)is not None:
            _d.active_proposal_by_target[Address(_b[_s12])]=u256(_b.get(_s26,0))
        _d.actor=Address(_b['actor'])
        _d.now=int(_b['now'])
        _d.target_release_id=str(_b.get(_s21,''))
        _d.target_mode=str(_b.get(_s28,''))

    def _ea(self,_a):
        if isinstance(_a,Address):
            return str(_a)
        if isinstance(_a,bytes):
            return _a.hex()
        if isinstance(_a,bool):
            return _a
        if isinstance(_a,int):
            return int(_a)
        if isinstance(_a,dict):
            return{str(_bb):self._ea(_aa)for(_bb,_aa)in _a.items()}
        if isinstance(_a,list):
            return[self._ea(_aa)for _aa in _a]
        if hasattr(_a,'__dict__'):
            return{_bb:self._ea(_aa)for(_bb,_aa)in _a.__dict__.items()}
        return _a

    def _eb(self,cls,_aj):
        _a=list(_aj.values())
        if cls is _fa or cls is _eu or cls is _ey or(cls is _ew):
            _a[1]=Address(_a[1])
        if cls is _fa:
            _a[0]=Address(_a[0])
        elif cls is _eu:
            _a[2]=Address(_a[2])
            if isinstance(_a[8],str):
                _a[8]=bytes.fromhex(_a[8])
            if isinstance(_a[20],str):
                _a[20]=bytes.fromhex(_a[20])
        return cls(**dict(zip(cls.__annotations__.keys(),_a)))

    def _ef(self,_d,_s,_b):
        _ae={_s20:_s,_s32:[],_s29:[],_s15:[],_s19:[],'active':[],_s1:_d.used_evidence_ids,_s2:_d.installed_candidate_hashes,_s4:_d.used_incident_ids,_s6:int(_d.proposal_count),_s7:int(_d.release_count)}
        for _a in _d.policies.values():
            _ae[_s32].append(self._ea(_a))
        for _a in _d.proposals.values():
            _ae[_s29].append(self._ea(_a))
        for _a in _d.releases.values():
            _ae[_s15].append(self._ea(_a))
        for _a in _d.incidents.values():
            _ae[_s19].append(self._ea(_a))
        for(_r,_a)in _d.active_proposal_by_target.items():
            _ae['active'].append([str(_r),int(_a)])
        return _ae

    @gl.public.write
    def execute(self,_s:str,_cu:str)->None:
        if gl.message.sender_address!=self.governor:
            raise gl.vm.UserError(_s0)
        _b=json.loads(_cu)
        _b[_s20]=_s
        _d=ProofPatchPolicyLogic()
        self._em(_d,_b)
        _ay=_b['args']
        if _s=='create':
            _d._du(*_ay)
        elif _s=='repair':
            _d._dw(*_ay)
        elif _s==_s31:
            _d._dx(*_ay)
        else:
            raise gl.vm.UserError(_s0)
        _eq(self.governor).emit(on='finalized').apply_policy_result(_s,json.dumps(self._ef(_d,_s,_b),separators=(',',':')))
