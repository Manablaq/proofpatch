# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_s0='ProofPatch invariant'
_s1='finalized'
_s2='proposal_count'
_s3='incident'
_s4='release_count'
_s5='proposal'
_s6='assurance'
_s7='register'
_s8='UpgradeProposal'
_s9='IncidentRecord'
_s10='ReleaseRecord'
_s11='TargetPolicy'
_s12='proposal_id'
_s13='candidate'
_s14='evidence'
from genlayer import*
_cr='EVIDENCE_'
_ct='MANIFEST_'
_cp='ASSURANCE_'
_cs='INCIDENT_'
_cu='RECOVERY_'
_cq='CANDIDATE_'
_co='CI_'
_cn='AUDIT_'
from dataclasses import dataclass
from datetime import datetime
from genlayer.py.public_abi import StorageType
import json
_ae='0x9840cCf5DBdf4AE5945Ca73367e8336cCBEF578e'
_er='0x32E5eFAF7558B65f72dA2B2B27f040e74fA148BC'

@gl.contract_interface
class _dm:

    class _ea:

        def get_proposal_result(self,_b:u256)->str:
            ...

        def get_assurance_result(self,_b:u256)->str:
            ...

        def get_incident_result(self,_g:str)->str:
            ...

    class _dy:

        def review_proposal(self,_b:u256,_r:str)->None:
            ...

        def assure_release(self,_b:u256,_r:str)->None:
            ...

        def review_incident(self,_g:str,_r:str)->None:
            ...

@allow_storage
@dataclass
class _dw:
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
class _dq:
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
class _du:
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
class _ds:
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
_af={_s11:'owner,target,constitution,policy_fingerprint,source_authority,ci_authority,audit_authority,source_prefix,ci_prefix,audit_prefix,assurance_authority,assurance_prefix,assurance_corroboration_authority,assurance_corroboration_prefix,proofpatch_kernel_hash,current_version,current_source_url,current_code_hash,current_release_id,max_evidence_age_seconds,proposal_ttl_seconds,execution_timeout_seconds,assurance_observation_delay_seconds,assurance_deadline_seconds,max_manifest_bytes,max_capsule_bytes,active'.split(','),_s8:'proposal_id,target,proposer,parent_version,parent_source_url,parent_code_hash,candidate_version,candidate_source_url,candidate_code,candidate_code_hash,ci_evidence_url,ci_evidence_id,audit_evidence_url,audit_evidence_id,assurance_manifest,assurance_manifest_hash,recovery_mode,recovery_release_id,recovery_version,recovery_source_url,recovery_code,recovery_code_hash,recovery_capsule_hash,evidence_set_hash,policy_fingerprint,created_at,expires_at,reviewed_at,execution_deadline,status,last_review_code'.split(','),_s10:'release_id,target,version,parent_release_id,parent_code_hash,source_url,code_hash,proposal_id,policy_fingerprint,evidence_set_hash,assurance_manifest_hash,recovery_capsule_hash,installed_at,certified_at,status,recovered_from_release_id,recovery_incident_id,lineage_hash'.split(','),_s9:'incident_id,target,release_id,installed_code_hash,incident_type,primary_url,primary_evidence_id,corroboration_url,corroboration_evidence_id,policy_fingerprint,assurance_manifest_hash,recovery_capsule_hash,opened_at,expires_at,reviewed_at,recovery_deadline,status,last_review_code,recovery_authorized'.split(',')}

@gl.contract_interface
class _do:

    class _ea:

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

    class _dy:

        def proofpatch_confirm_registration(self,_h:str,_ah:str)->None:
            ...

        def proofpatch_upgrade(self,_b:u256,_m:str)->None:
            ...

        def proofpatch_activate(self,_h:str,_m:str)->None:
            ...

        def proofpatch_recover(self,_g:str,_h:str,_ag:str)->None:
            ...
_bm='0xCe91B262d6358dFd95A32a56fd577b71FB0DdC7F'
_bh='0x3De9294a39A4b9e31975a74426a3f29C32E0829E'
_bi='0x59A065F97a4d475Fc60AC350aDF5163AbfE27F91'
_av='0xF7e1F1D31f60e866E2f0a1367834BEF7abC77b43'
_bf='0x6740374AA335c4e02EC079d3d1E5A2198A28320F'
_bz='0x209343F604Ec7A53339C3F555D5Cf333F4BEf4FD'
_by='0xE7F337c2Bc992a94f213C41B66d7E49381F31145'
_l1='0xd73FF76b1A2438eAD59DA4072F9484aED25C7865'
_l2='0x429A733D5949bCB0DE97E32Da58E8d192acC41Ca'
_l3='0xebf47F06759481606910dA564FF48203e386b95E'
_bx='0xC01B9D36B3eEe2A563A4E7FA688b9a799fa759E2'
_as='0x50d787E2078683Bbc27462208475578cE7295aF9'
_at='0xef8F5C807117b2A606B861e947F2ff5756Db8CE7'

@gl.contract_interface
class _dk:

    class _dy:

        def execute(self,_e:str,_l:str)->None:
            ...

@gl.contract_interface
class _di:

    class _ea:

        def read(self,_i:str,_f:str)->str:
            ...

class ProofPatchGovernorV2(gl.Contract):
    policies:TreeMap[Address,_dw]
    proposals:TreeMap[u256,_dq]
    releases:TreeMap[str,_du]
    incidents:TreeMap[str,_ds]
    active_proposal_by_target:TreeMap[Address,u256]
    used_evidence_ids:TreeMap[str,bool]
    installed_candidate_hashes:TreeMap[str,bool]
    used_incident_ids:TreeMap[str,bool]
    proposal_count:u256
    release_count:u256

    def __init__(self):
        self.proposal_count=u256(0)
        self.release_count=u256(0)

    def _cv(self):
        _p=str(gl.message_raw['datetime'])
        return int(datetime.fromisoformat(_p.replace('Z','+00:00')).timestamp())

    def _cl(self):
        return _dm(Address(_ae))

    def _ck(self):
        return _dm(Address(_er))

    def _cj(self,_i,_f):
        return _di(Address(_bz)).view(state=StorageType.LATEST_FINAL).read(_i,str(_f))

    @gl.public.write
    def review_proposal(self,_b:u256)->None:
        if gl.message.sender_address==Address(_ae):
            self._cg(_s5,[_b],str(gl.message.sender_address))
            return
        self._cd(_s5,[_b])

    @gl.public.view
    def is_upgrade_authorized(self,_b:u256,_c:str,_m:str)->bool:
        return self._cj('is_upgrade_authorized',json.dumps([int(_b),_c,_m],separators=(',',':')))=='1'

    @gl.public.view
    def get_candidate_code(self,_b:u256)->bytes:
        return bytes.fromhex(self._cj('candidate_code',str(int(_b))))

    @gl.public.view
    def is_activation_authorized(self,_b:u256,_h:str,_m:str)->bool:
        return self._cj('is_activation_authorized',json.dumps([int(_b),_h,_m],separators=(',',':')))=='1'

    @gl.public.view
    def is_registration_authorized(self,_c:str,_h:str,_ah:str)->bool:
        return self._cj('is_registration_authorized',json.dumps([_c,_h,_ah],separators=(',',':')))=='1'

    @gl.public.write
    def review_incident(self,_g:str)->None:
        if gl.message.sender_address==Address(_er):
            self._cg(_s3,[_g],str(gl.message.sender_address))
            return
        self._cd(_s3,[_g])

    @gl.public.view
    def is_recovery_authorized(self,_g:str,_h:str,_ag:str)->bool:
        return self._cj('is_recovery_authorized',json.dumps([_g,_h,_ag],separators=(',',':')))=='1'

    @gl.public.view
    def get_recovery_release_id(self,_g:str)->str:
        return self._cj('recovery_release_id',_g)

    @gl.public.view
    def get_recovery_code(self,_g:str)->bytes:
        return bytes.fromhex(self._cj('recovery_code',_g))

    @gl.public.view
    def get_proposal_count(self)->u256:
        return u256(int(self._cj(_s2,'')))

    @gl.public.view
    def get_proposal_status(self,_b:u256)->str:
        return self._cj('proposal_status',str(int(_b)))

    @gl.public.view
    def get_candidate_hash(self,_b:u256)->str:
        return self._cj('candidate_hash',str(int(_b)))

    @gl.public.view
    def get_proposal_release_id(self,_b:u256)->str:
        return self._cj('proposal_release_id',str(int(_b)))

    @gl.public.view
    def get_evidence_set_hash(self,_b:u256)->str:
        return self._cj('evidence_set_hash',str(int(_b)))

    @gl.public.view
    def get_policy_fingerprint(self,_c:str)->str:
        return self._cj('policy_fingerprint',_c)

    @gl.public.view
    def get_policy_kernel_hash(self,_c:str)->str:
        return self._cj('policy_kernel_hash',_c)

    @gl.public.view
    def get_current_code_hash(self,_c:str)->str:
        return self._cj('current_code_hash',_c)

    @gl.public.view
    def get_current_version(self,_c:str)->str:
        return self._cj('current_version',_c)

    @gl.public.view
    def get_current_release_id(self,_c:str)->str:
        return self._cj('current_release_id',_c)

    @gl.public.view
    def get_active_proposal(self,_c:str)->u256:
        return u256(int(self._cj('active_proposal',_c)))

    @gl.public.view
    def get_proposal_summary(self,_b:u256)->str:
        return self._cj('proposal_summary',str(int(_b)))

    @gl.public.view
    def get_release_summary(self,_h:str)->str:
        return self._cj('release_summary',_h)

    @gl.public.view
    def get_incident_summary(self,_g:str)->str:
        return self._cj('incident_summary',_g)

    @gl.public.view
    def get_state_record(self,_i:str,_f:str)->str:
        _f=str(_f)
        if _i=='policy':
            _a=self.policies.get(Address(_f),None)
        elif _i==_s5:
            _a=self.proposals.get(u256(int(_f)),None)
        elif _i=='release':
            _a=self.releases.get(_f,None)
        elif _i==_s3:
            _a=self.incidents.get(_f,None)
        elif _i=='active':
            _a={'value':self.active_proposal_by_target.get(Address(_f),u256(0))}
        elif _i=='counts':
            _a={_s2:self.proposal_count,_s4:self.release_count}
        elif _i in(_s14,_s13,'incident_evidence'):
            _a={'value':bool(self.used_evidence_ids.get(_f,False)if _i==_s14 else self.installed_candidate_hashes.get(_f,False)if _i==_s13 else self.used_incident_ids.get(_f,False))}
        else:
            raise gl.vm.UserError(_s0)
        if _a is None:
            return json.dumps({'status':'UNKNOWN'},separators=(',',':'))
        return json.dumps(self._ck(_a),separators=(',',':'))

    def _ck(self,_a):
        if isinstance(_a,Address):
            return str(_a)
        if isinstance(_a,bytes):
            return _a.hex()
        if isinstance(_a,bool):
            return _a
        if isinstance(_a,int):
            return int(_a)
        if isinstance(_a,dict):
            return{str(_ak):self._ck(_y)for(_ak,_y)in _a.items()}
        if isinstance(_a,list):
            return[self._ck(_y)for _y in _a]
        if hasattr(_a,'__dict__'):
            _n=_af[_s11]if isinstance(_a,_dw)else _af[_s8]if isinstance(_a,_dq)else _af[_s10]if isinstance(_a,_du)else _af[_s9]if isinstance(_a,_ds)else None
            if _n is not None:
                return{_f:self._ck(_p)for(_f,_p)in zip(_n,_a.__dict__.values())}
            return{_ak:self._ck(_y)for(_ak,_y)in _a.__dict__.items()}
        return _a

    def _cm(self,cls,_p):
        _a=list(_p.values())
        _a[1]=Address(_a[1])
        if cls is _dw:
            _a[0]=Address(_a[0])
        elif cls is _dq:
            _a[2]=Address(_a[2])
            if isinstance(_a[8],str):
                _a[8]=bytes.fromhex(_a[8])
            if isinstance(_a[20],str):
                _a[20]=bytes.fromhex(_a[20])
        return cls(**dict(zip(cls.__annotations__.keys(),_a)))

    def _ci(self,_o):
        _j=json.loads(_o)
        for(_i,cls,_aj,_cb)in(('policies',_dw,self.policies,'target'),('proposals',_dq,self.proposals,_s12),('releases',_du,self.releases,'release_id'),('incidents',_ds,self.incidents,'incident_id')):
            for _p in _j.get(_i,[]):
                _a=self._cm(cls,_p)
                _aj[getattr(_a,_cb)]=_a
        for(_c,_a)in _j.get('active',[]):
            self.active_proposal_by_target[Address(_c)]=u256(_a)
        for(_i,_aj)in(('used_evidence_ids',self.used_evidence_ids),('installed_candidate_hashes',self.installed_candidate_hashes),('used_incident_ids',self.used_incident_ids)):
            for(_f,_a)in _j.get(_i,{}).items():
                _aj[_f]=bool(_a)
        if _s2 in _j:
            self.proposal_count=u256(_j[_s2])
        if _s4 in _j:
            self.release_count=u256(_j[_s4])
        return _j

    def _cf(self,_e,_d,_x,**_n):
        _k={'args':self._ck(_d),'actor':_x,'now':self._cv()}
        for(_f,_a)in _n.items():
            _k[_f]=self._ck(_a)
        if _e==_s7:
            _ai=_dk(Address(_av))
        elif _e=='assure':
            _ai=_dk(Address(_bf))
        elif _e in('incident','repair_incident'):
            _ai=_dk(Address(_bh))
        elif _e=='repair':
            _ai=_dk(Address(_bi))
        else:
            _ai=_dk(Address(_bm))
        _ai.emit(on=_s1).execute(_e,json.dumps(_k,sort_keys=True,separators=(',',':')))

    def _ce(self,_e,_d,_x,**_n):
        _k={'args':self._ck(_d),'actor':_x,'now':self._cv()}
        for(_f,_a)in _n.items():
            _k[_f]=self._ck(_a)
        _dk(Address(_bx)).emit(on=_s1).execute(_e,json.dumps(_k,sort_keys=True,separators=(',',':')))

    def _cd(self,_e,_d):
        _l={'args':self._ck(_d),'now':self._cv()}
        _dk(Address(_as)).emit(on=_s1).execute(_e,json.dumps(_l,separators=(',',':')))

    def _cg(self,_e,_d,_x,**_n):
        _k={'args':self._ck(_d),'actor':_x,'now':self._cv()}
        for(_f,_a)in _n.items():
            _k[_f]=self._ck(_a)
        _dk(Address(_at)).emit(on=_s1).execute(_e,json.dumps(_k,sort_keys=True,separators=(',',':')))

    def _ch(self,_ca):
        for _v in _ca:
            _i=_v.get('kind')
            _d=_v.get('args',[])
            if _i=='upgrade':
                _do(Address(_d[0])).emit(on=_s1).proofpatch_upgrade(u256(_d[1]),_d[2])
            elif _i=='activate':
                _do(Address(_d[0])).emit(on=_s1).proofpatch_activate(_d[1],_d[2])
            elif _i=='recover':
                _do(self.incidents[_d[0]].fbw).emit(on=_s1).proofpatch_recover(_d[0],_d[1],_d[2])
            else:
                raise gl.vm.UserError(_s0)

    @gl.public.write
    def apply_review_request(self,_e:str,_l:str)->None:
        if gl.message.sender_address!=Address(_as):
            raise gl.vm.UserError(_s0)
        _k=json.loads(_l)
        _d=_k['args']
        _j=_k.get('patch',{})
        if _j:
            self._ci(json.dumps(_j,separators=(',',':')))
        _r=_k['snapshot']
        if _e==_s5:
            self._cl().emit(on=_s1).review_proposal(u256(_d[0]),_r)
        elif _e==_s6:
            self._ck().emit(on=_s1).assure_release(u256(_d[0]),_r)
        elif _e==_s3:
            self._ck().emit(on=_s1).review_incident(_d[0],_r)
        else:
            raise gl.vm.UserError(_s0)

    @gl.public.write
    def apply_review_result(self,_e:str,_o:str)->None:
        if gl.message.sender_address!=Address(_at):
            raise gl.vm.UserError(_s0)
        _j=self._ci(_o)
        self._ch(_j.get('actions',[]))

    @gl.public.write
    def apply_policy_result(self,_e:str,_o:str)->None:
        if gl.message.sender_address not in(Address(_bm),Address(_bh),Address(_bi),Address(_av),Address(_bf)):
            raise gl.vm.UserError(_s0)
        _j=self._ci(_o)
        if _e==_s7:
            _c=Address(_j['registration_target'])
            _bw=self.policies[_c]
            _do(_c).emit(on=_s1).proofpatch_confirm_registration(_bw.fac,_bw.fab)
        elif _e=='assure':
            _w=_j.get('review',{})
            self._cd(_s6,[_w[_s12],_w['primary_url'],_w['primary_evidence_id'],_w['corroboration_url'],_w['corroboration_evidence_id']])

    @gl.public.write
    def apply_lifecycle_result(self,_e:str,_o:str)->None:
        if gl.message.sender_address not in(Address(_by),Address(_l1),Address(_l2),Address(_l3)):
            raise gl.vm.UserError(_s0)
        _j=self._ci(_o)
        for _v in _j.get('actions',[]):
            if _v.get('kind')=='recover':
                _d=_v['args']
                _do(self.incidents[_d[0]].fbw).emit(on=_s1).proofpatch_recover(_d[0],_d[1],_d[2])
            else:
                raise gl.vm.UserError(_s0)

    @gl.public.write
    def register_target(self,_bv:str,_bt:str,_bi:str,_bs:str,_bj:str,_bq:str,_bu:str,_br:str,_aw:str,_bg:str,_am:str,_an:str,_ar:str,_bk:str,_ba:str,_bd:str,_aq:u64,_au:u64,_ap:u64,_al:u64,_ao:u64,_bb:u64,_be:u64)->None:
        self._cf(_s7,[_bv,_bt,_bi,_bs,_bj,_bq,_bu,_br,_aw,_bg,_am,_an,_ar,_bk,_ba,_bd,_aq,_au,_ap,_al,_ao,_bb,_be],str(gl.message.sender_address))

    @gl.public.write
    def create_proposal(self,_c:str,_bc:str,_z:str,_bl:bytes,_ac:str,_ad:str,_aa:str,_ab:str,_az:str,_bp:str,_ax:str,_bh:str,_ay:str,_bo:bytes)->u256:
        self._cf('create',[_c,_bc,_z,_bl,_ac,_ad,_aa,_ab,_az,_bp,_ax,_bh,_ay,_bo],str(gl.message.sender_address))
        return u256(int(self.proposal_count)+1)

    @gl.public.write
    def repair_evidence(self,_b:u256,_z:str,_ac:str,_ad:str,_aa:str,_ab:str)->None:
        self._cf('repair',[_b,_z,_ac,_ad,_aa,_ab],str(gl.message.sender_address))

    @gl.public.write
    def assure_release(self,_b:u256,_u:str,_q:str,_t:str,_s:str)->None:
        if gl.message.sender_address==Address(_er):
            self._cg(_s6,[_b,_u,_q,_t,_s],str(gl.message.sender_address))
            return
        self._cf('assure',[_b,_u,_q,_t,_s],str(gl.message.sender_address))

    @gl.public.write
    def open_incident(self,_c:str,_h:str,_bn:str,_u:str,_q:str,_t:str,_s:str)->str:
        _cc=self._cv()
        self._cf(_s3,[_c,_h,_bn,_u,_q,_t,_s],str(gl.message.sender_address))
        return 'incident-'+str(_cc)+'-'+_q

    @gl.public.write
    def repair_incident(self,_g:str,_u:str,_q:str,_t:str,_s:str)->None:
        self._cf('repair_incident',[_g,_u,_q,_t,_s],str(gl.message.sender_address))

    @gl.public.write
    def cancel_proposal(self,_b:u256):
        self._ce('cancel',[_b],str(gl.message.sender_address))

    @gl.public.write
    def expire_proposal(self,_b:u256):
        self._ce('expire',[_b],str(gl.message.sender_address))

    @gl.public.write
    def confirm_install(self,_b:u256,_m:str):
        self._ce('confirm_install',[_b,_m],str(gl.message.sender_address))

    @gl.public.write
    def reconcile_install(self,_b:u256):
        self._ce('reconcile_install',[_b],str(gl.message.sender_address))

    @gl.public.write
    def mark_execution_timeout(self,_b:u256):
        self._ce('timeout',[_b],str(gl.message.sender_address))

    @gl.public.write
    def confirm_activation(self,_b:u256,_h:str,_m:str):
        self._ce('confirm_activation',[_b,_h,_m],str(gl.message.sender_address))

    @gl.public.write
    def expire_provisional_release(self,_h:str):
        self._ce('expire_provisional',[_h],str(gl.message.sender_address))

    @gl.public.write
    def confirm_recovery(self,_g:str,_h:str,_ag:str):
        self._ce('confirm_recovery',[_g,_h,_ag],str(gl.message.sender_address))

    @gl.public.write
    def reconcile_recovery(self,_g:str):
        self._ce('reconcile_recovery',[_g],str(gl.message.sender_address))

    @gl.public.write
    def expire_recovery(self,_g:str):
        self._ce('expire_recovery',[_g],str(gl.message.sender_address))

    @gl.public.write
    def retry_recovery(self,_g:str):
        self._ce('retry_recovery',[_g],str(gl.message.sender_address))
