# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_s0='ProofPatch invariant'
_s1='candidate_code_hash'
_s2='proposal'
_s3='proposal_id'
_s4='recovery_capsule_hash'
_s5='release_id'
_s6='policy_fingerprint'
_s7='evidence_set_hash'
_s8='recovery_release_id'
_s9='execution_deadline'
_s10='candidate_code'
_s11='incident'
_s12='assurance_manifest_hash'
_s13='CERTIFICATION_QUEUED'
_s14='recovery_authorized'
_s15='current_release_id'
_s16='current_code_hash'
_s17='last_review_code'
_s18='parent_code_hash'
_s19='release-'
_s20='RETRY_REQUIRED'
_s21='UPGRADE_QUEUED'
_s22='proposal_count'
_s23='recovery_code'
_s24='reviewed_at'
_s25='expires_at'
_s26='CONFIRMED'
from genlayer import*
_ab='EVIDENCE_'
_ad='MANIFEST_'
_z='ASSURANCE_'
_ac='INCIDENT_'
_ae='RECOVERY_'
_aa='CANDIDATE_'
_y='CI_'
_x='AUDIT_'
from genlayer.py.public_abi import StorageType
from datetime import datetime
import json
_o='0x0000000000000000000000000000000000000000'

@gl.contract_interface
class _ak:

    class _am:

        def get_state_record(self,_c:str,_f:str)->str:
            ...

class _ai(gl.Contract):
    admin:Address
    governor:Address

    def __init__(self):
        self.admin=gl.message.sender_address
        self.governor=Address(_o)

    @gl.public.write
    def bind_governor(self,governor:str)->None:
        if gl.message.sender_address!=self.admin:
            raise gl.vm.UserError(_s0)
        if self.governor!=Address(_o):
            raise gl.vm.UserError(_s0)
        _p=Address(governor)
        if _p==Address(_o):
            raise gl.vm.UserError(_s0)
        self.governor=_p

    def _ag(self,_c,_f):
        try:
            return json.loads(_ak(self.governor).view(state=StorageType.LATEST_FINAL).get_state_record(_c,_f))
        except Exception:
            return None

    def _ah(self):
        return int(datetime.fromisoformat(str(gl.message_raw['datetime']).replace('Z','+00:00')).timestamp())

    def _w(self,_a):
        return _a is None or _a.get('status')=='UNKNOWN'

    def _af(self,_a,_t):
        return json.dumps({_q:_a[_q]for _q in _t},separators=(',',':'))

    @gl.public.view
    def get_proposal_summary(self,_b:u256)->str:
        _a=self._ag(_s2,str(int(_b)))
        if _a is None or _a.get('status')=='UNKNOWN':
            return json.dumps({'status':'UNKNOWN'},separators=(',',':'))
        _a[_s5]=_s19+str(_a[_s3])+'-'+_a[_s1][:16]
        return self._af(_a,(_s3,'target','parent_version',_s18,'candidate_version',_s1,_s6,_s7,_s12,'recovery_mode',_s8,_s4,_s5,'status',_s17,'created_at',_s25,_s24,_s9))

    @gl.public.view
    def get_release_summary(self,_g:str)->str:
        _a=self._ag('release',_g)
        if _a is None or _a.get('status')=='UNKNOWN':
            return json.dumps({'status':'UNKNOWN'},separators=(',',':'))
        return self._af(_a,(_s5,'target','version','parent_release_id',_s18,'code_hash',_s3,_s6,_s7,_s12,_s4,'installed_at','certified_at','status','recovered_from_release_id','recovery_incident_id','lineage_hash'))

    @gl.public.view
    def get_incident_summary(self,_h:str)->str:
        _a=self._ag(_s11,_h)
        if _a is None or _a.get('status')=='UNKNOWN':
            return json.dumps({'status':'UNKNOWN'},separators=(',',':'))
        return self._af(_a,('incident_id','target',_s5,'installed_code_hash','incident_type',_s6,_s4,'opened_at',_s25,_s24,'recovery_deadline','status',_s17,_s14))

    @gl.public.view
    def get_candidate_code(self,_b:u256)->bytes:
        _a=self._ag(_s2,str(int(_b)))
        if _a is None:
            raise gl.vm.UserError(_s0)
        if _a['status']!=_s21:
            raise gl.vm.UserError(_s0)
        if self._ah()>int(_a[_s9]):
            raise gl.vm.UserError(_s0)
        return bytes.fromhex(_a[_s10])

    @gl.public.view
    def get_recovery_release_id(self,_h:str)->str:
        _a=self._ag(_s11,_h)
        if _a is None:
            return ''
        _l=self._ag('release',_a[_s5])
        if _l is None:
            return ''
        _k=self._ag(_s2,str(_l[_s3]))
        return '' if _k is None else _k[_s8]

    @gl.public.view
    def get_recovery_code(self,_h:str)->bytes:
        _n=self._ag(_s11,_h)
        if _n is None:
            raise gl.vm.UserError(_s0)
        if _n['status']not in(_ac+_s26,_ae+'QUEUED',_ae+_s20):
            raise gl.vm.UserError(_s0)
        _l=self._ag('release',_n[_s5])
        _k=self._ag(_s2,str(_l[_s3]))
        return bytes.fromhex(_k[_s23])

    @gl.public.view
    def is_upgrade_authorized(self,_b:u256,_e:str,_m:str)->bool:
        _d=self._ag(_s2,str(int(_b)))
        if self._w(_d)or _d['status']!=_s21 or _d['target'].lower()!=str(Address(_e)).lower()or(_d[_s1]!=_m.lower())or(self._ah()>int(_d[_s9])):
            return False
        return int(self._ag('active',_d['target'])['value'])==int(_b)

    @gl.public.view
    def is_activation_authorized(self,_b:u256,_g:str,_m:str)->bool:
        _d=self._ag(_s2,str(int(_b)))
        _i=self._ag('release',_g)
        return not self._w(_d)and(not self._w(_i))and(_d['status']==_s13)and(_g==_s19+str(_d[_s3])+'-'+_d[_s1][:16])and(_m.lower()==_d[_s1])and(_i['status']==_s13)

    @gl.public.view
    def is_registration_authorized(self,_e:str,_g:str,_s:str)->bool:
        _d=self._ag('policy',_e)
        _i=self._ag('release',_g)
        return not self._w(_d)and(not self._w(_i))and(_d[_s15]==_g)and(_d[_s16]==_s.lower())and(_i['status']=='REGISTERED_PARENT')

    @gl.public.view
    def is_recovery_authorized(self,_h:str,_g:str,_r:str)->bool:
        _j=self._ag(_s11,_h)
        _i=self._ag('release',_g)
        return not self._w(_j)and(not self._w(_i))and(_j['status']in(_ac+_s26,_ae+'QUEUED',_ae+_s20))and _j[_s14]and(_j[_s5]==_g)and(_j[_s4]==_r.lower())

    @gl.public.view
    def get_proposal_count(self)->u256:
        _a=self._ag('counts','')
        return u256(0 if self._w(_a)else _a[_s22])

    @gl.public.view
    def get_proposal_status(self,_b:u256)->str:
        _a=self._ag(_s2,str(int(_b)))
        return 'UNKNOWN' if self._w(_a)else _a['status']

    @gl.public.view
    def get_candidate_hash(self,_b:u256)->str:
        _a=self._ag(_s2,str(int(_b)))
        return '' if self._w(_a)else _a[_s1]

    @gl.public.view
    def get_proposal_release_id(self,_b:u256)->str:
        _a=self._ag(_s2,str(int(_b)))
        return '' if self._w(_a)else _s19+str(_a[_s3])+'-'+_a[_s1][:16]

    @gl.public.view
    def get_evidence_set_hash(self,_b:u256)->str:
        _a=self._ag(_s2,str(int(_b)))
        return '' if self._w(_a)else _a[_s7]

    @gl.public.view
    def get_policy_fingerprint(self,_e:str)->str:
        _a=self._ag('policy',_e)
        return '' if self._w(_a)else _a[_s6]

    @gl.public.view
    def get_policy_kernel_hash(self,_e:str)->str:
        _a=self._ag('policy',_e)
        return '' if self._w(_a)else _a['proofpatch_kernel_hash']

    @gl.public.view
    def get_current_code_hash(self,_e:str)->str:
        _a=self._ag('policy',_e)
        return '' if self._w(_a)else _a[_s16]

    @gl.public.view
    def get_current_version(self,_e:str)->str:
        _a=self._ag('policy',_e)
        return '' if self._w(_a)else _a['current_version']

    @gl.public.view
    def get_current_release_id(self,_e:str)->str:
        _a=self._ag('policy',_e)
        return '' if self._w(_a)else _a[_s15]

    @gl.public.view
    def get_active_proposal(self,_e:str)->u256:
        _a=self._ag('active',_e)
        return u256(0 if self._w(_a)else _a['value'])

    @gl.public.view
    def read(self,_c:str,_f:str)->str:
        if _c.endswith('_summary'):
            return getattr(self,'get_'+_c)(_f if _c!='proposal_summary' else u256(int(_f)))
        if _c in(_s10,_s23):
            return(self.get_candidate_code(u256(int(_f)))if _c==_s10 else self.get_recovery_code(_f)).hex()
        if _c==_s8:
            return self.get_recovery_release_id(_f)
        if _c.startswith('is_'):
            _v=json.loads(_f)
            _u=getattr(self,_c)(*_v)
            return '1' if _u else '0'
        if _c==_s22:
            return str(int(self.get_proposal_count()))
        if _c=='active_proposal':
            return str(int(self.get_active_proposal(_f)))
        return str(getattr(self,'get_'+_c)(u256(int(_f)))if _c in('proposal_status','candidate_hash','proposal_release_id',_s7)else getattr(self,'get_'+_c)(_f))
