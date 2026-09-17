# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_s0='ProofPatch invariant'
_s1='used_evidence_ids'
_s2='installed_at'
_s3='proposal_id'
_s4='proposals'
from genlayer import*
_ax='EVIDENCE_'
_az='MANIFEST_'
_av='ASSURANCE_'
_ay='INCIDENT_'
_ba='RECOVERY_'
_aw='CANDIDATE_'
_au='CI_'
_at='AUDIT_'
import hashlib
import json
_k='0x0000000000000000000000000000000000000000'
_aa=1024
_ab=160
_x='INSTALLED_PROVISIONAL'
_o=_av+'PENDING'
_y=_av+'REPAIR_REQUIRED'
_z=_av+'RETRY_REQUIRED'

@gl.contract_interface
class _bf:

    class _bj:

        def get_state_record(self,_v:str,_i:str)->str:
            ...

    class _bh:

        def apply_policy_result(self,_j:str,_as:str)->None:
            ...

class _bd:

    def _ao(self,_a):
        return hashlib.sha256('\x1f'.join(_a).encode('utf-8')).hexdigest()

    def _ap(self,_h,_ak,_af,_ae):
        _w=len(_h.encode('utf-8'))
        if _w<_af or _w>_ae:
            raise gl.vm.UserError(f'{_ak} length is invalid')

    def _al(self,_h):
        if not _h or _h in('.','..'):
            return False
        _ad='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'
        return all((_l in _ad for _l in _h))

    def _an(self,_f):
        _t='https://raw.githubusercontent.com/'
        if not _f.startswith(_t)or not _f.endswith('/'):
            return ''
        _a=_f[len(_t):].split('/')
        if len(_a)!=3 or _a[2]!='':
            return ''
        if not self._al(_a[0])or not self._al(_a[1]):
            return ''
        return _a[0]

    def _am(self,_n,_f):
        if len(_n.encode('utf-8'))>_aa or self._an(_f)=='':
            return False
        if not _n.startswith(_f):
            return False
        _a=_n[len(_f):].split('/',1)
        if len(_a)!=2 or len(_a[0])!=40 or any((_l not in '0123456789abcdef' for _l in _a[0])):
            return False
        return all((self._al(_ah)for _ah in _a[1].split('/')))

    def _aq(self,_e,_d,_aj,_ai,_v,_p):
        self._ap(_p,'evidence_id',8,_ab)
        _i=self._ao([_aj,_ai,_v,_p])
        if json.loads(_e.get_state_record('evidence',_i)).get('value',False)or _d[_s1].get(_i,False):
            raise gl.vm.UserError(_s0)
        _d[_s1][_i]=True

    def _ar(self,_e,_c,_m):
        _q=int(_c[0])
        _b=json.loads(_e.get_state_record('proposal',str(_q)))
        _g=json.loads(_e.get_state_record('policy',_b['target']))
        _ac='release-'+str(_b[_s3])+'-'+_b['candidate_code_hash'][:16]
        _s=json.loads(_e.get_state_record('release',_ac))
        if _b['status']not in(_x,_y,_z,_o):
            raise gl.vm.UserError(_s0)
        if _m<int(_s[_s2])+int(_g['assurance_observation_delay_seconds']):
            raise gl.vm.UserError(_s0)
        if _m>int(_s[_s2])+int(_g['assurance_deadline_seconds']):
            raise gl.vm.UserError(_s0)
        if not self._am(_c[1],_g['assurance_prefix'])or not self._am(_c[3],_g['assurance_corroboration_prefix']):
            raise gl.vm.UserError(_s0)
        if _c[2]==_c[4]:
            raise gl.vm.UserError(_s0)
        _d={'operation':'assure',_s4:[_b],'releases':[],_s1:{}}
        self._aq(_e,_d,_b['target'],_g['assurance_authority'],'assurance_primary',_c[2])
        self._aq(_e,_d,_b['target'],_g['assurance_corroboration_authority'],'assurance_corroboration',_c[4])
        _b['status']=_o
        _b['reviewed_at']=_m
        _b['last_review_code']='ENGINE_PENDING'
        _d[_s4]=[_b]
        _d['review']={_s3:_q,'primary_url':_c[1],'primary_evidence_id':_c[2],'corroboration_url':_c[3],'corroboration_evidence_id':_c[4]}
        return _d

class _bb(gl.Contract):
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
        _r=Address(governor)
        if _r==Address(_k):
            raise gl.vm.UserError(_s0)
        self.governor=_r

    @gl.public.write
    def execute(self,_j:str,_ag:str)->None:
        if gl.message.sender_address!=self.governor:
            raise gl.vm.UserError(_s0)
        if _j!='assure':
            raise gl.vm.UserError(_s0)
        _u=json.loads(_ag)
        _e=_bf(self.governor).view(state=StorageType.LATEST_FINAL)
        _d=_bd()._ar(_e,_u['args'],int(_u['now']))
        _bf(self.governor).emit(on='finalized').apply_policy_result(_j,json.dumps(_d,separators=(',',':')))
