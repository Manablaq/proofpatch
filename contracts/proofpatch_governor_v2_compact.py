# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_s0='ProofPatch invariant'
_s1='policy_fingerprint'
_s2='recovery_capsule_hash'
_s3='assurance_manifest_hash'
_s4='assurance_deadline_seconds'
_s5='candidate_code_hash'
_s6='observation_delay_seconds'
_s7='max_evidence_age_seconds'
_s8='finalized'
_s9='error_code'
_s10='release_id'
_s11='proposal_id'
_s12='evidence_set_hash'
_s13='parent_code_hash'
_s14='installed_code_hash'
_s15='candidate_version'
_s16='ci_assurance_evidence_required'
_s17='independent_assurance_required'
_s18='REPAIR_REQUIRED'
_s19='audit_authority'
_s20='ENGINE_PENDING'
_s21='RETRY_REQUIRED'
_s22='corroboration_evidence_id'
_s23='EXACT_PARENT'
_s24='NONCANONICAL'
_s25='decision'
_s26='corroboration_authority'
_s27='incident_id'
_s28='expected_kernel_hash'
_s29='review_now'
_s30='assurance_authority'
_s31='primary_evidence_id'
_s32='recovery_release_id'
_s33='max_manifest_bytes'
_s34='REGISTERED_PARENT'
_s35='corroboration_url'
_s36='0123456789abcdef'
_s37='candidate_sha256'
_s38='last_review_code'
_s39='recovery_version'
_s40='REVIEW_PENDING'
_s41='parent_version'
_s42='incident_type'
_s43='recovery_mode'
_s44='ci_authority'
_s45='constitution'
_s46='kernel_hash'
_s47='primary_url'
_s48='reviewed_at'
_s49='assurance-'
_s50='expires_at'
_s51='CANDIDATE'
_s52='RECOVERED'
_s53='_INVALID'
from genlayer import*
_hn='EVIDENCE_'
_hp='MANIFEST_'
_hl='ASSURANCE_'
_ho='INCIDENT_'
_hq='RECOVERY_'
_hm='CANDIDATE_'
_hk='CI_'
_hj='AUDIT_'
from dataclasses import dataclass
from datetime import datetime
from genlayer.py.public_abi import StorageType
import hashlib
import json
_cx='proofpatch-v2'
_gu='proofpatch-evidence-v2'
_ew='proofpatch-assurance-v1'
_gv='proofpatch-incident-v1'
_gz='BOOTSTRAP'
_dv='ACTIVE'
_bn='PROVISIONAL'
_gc=_hq+'PENDING'
_cw=_s52
_bp='PROPOSED'
_ch=_hn+_s18
_cj='REVIEW_RETRY_REQUIRED'
_fb='REJECTED'
_bh='UPGRADE_QUEUED'
_ae='INSTALLED_PROVISIONAL'
_bb=_hl+'PENDING'
_bx=_hl+_s18
_by=_hl+_s21
_ay='CERTIFICATION_QUEUED'
_an='CERTIFIED'
_gw=_an
_fd='EXPIRED'
_ex='CANCELLED'
_el='EXECUTION_FAILED'
_z=_ho+'OPEN'
_eo=_ho+_s18
_dk=_ho+_s21
_af=_ho+'CONFIRMED'
_ei=_ho+'DISMISSED'
_bk=_hq+'QUEUED'
_ar=_hq+_s21
_bo=_s52
_cy='REPAIR'
_db='RETRY'
_fa='DECISION'
_cu='APPROVE'
_ez='REJECT'
_gy=('installed_hash_matches','kernel_binding_matches','governor_binding_matches','critical_state_preserved','interface_requirements_hold','canary_requirements_hold','runtime_evidence_valid','no_post_install_security_regression','recovery_path_live','assurance_manifest_satisfied')
_hb=('incident_evidence_authentic','incident_affects_exact_release','incident_reproducible_or_sufficiently_established','constitution_breached','continued_operation_unsafe','recovery_capsule_applicable','recovery_safer_than_continuation','recovery_path_preserves_rights','recovery_path_preserves_governance')
_en=16000
_dm=512000
_ff=1024
_fh=160
_ct=96
_ej=30*24*60*60
_ek=14*24*60*60
_co=7*24*60*60
_ca=60
_hc=('storage_layout_compatible','forward_storage_compatible','reverse_storage_compatible_or_recovery_safe','user_rights_preserved','no_privilege_escalation','proofpatch_kernel_preserved','upgrade_authority_preserved','provisional_guard_preserved','consensus_binding_preserved','evidence_trust_preserved','finality_safety_preserved','liveness_preserved','no_hidden_value_transfer','assurance_manifest_sufficient','assurance_path_preserved','recovery_capsule_valid','recovery_path_preserved','constitution_satisfied')
_cg='0x827798efCcE0a74a8dEc44bBA7A73445786A1c4C'
_cq=_s40
_cn=_ho+_s40

@gl.contract_interface
class _ht:

    class _ih:

        def get_proposal_result(self,_d:u256)->str:
            ...

        def get_assurance_result(self,_d:u256)->str:
            ...

        def get_incident_result(self,_g:str)->str:
            ...

    class _if:

        def review_proposal(self,_d:u256,_cl:str)->None:
            ...

        def assure_release(self,_d:u256,_cl:str)->None:
            ...

        def review_incident(self,_g:str,_cl:str)->None:
            ...

@allow_storage
@dataclass
class _id:
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
class _hx:
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
class _ib:
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
class _hz:
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

@gl.contract_interface
class _hv:

    class _ih:

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

    class _if:

        def proofpatch_confirm_registration(self,_e:str,_bu:str)->None:
            ...

        def proofpatch_upgrade(self,_d:u256,_o:str)->None:
            ...

        def proofpatch_activate(self,_e:str,_o:str)->None:
            ...

        def proofpatch_recover(self,_g:str,_e:str,_n:str)->None:
            ...

class ProofPatchGovernorV2(gl.Contract):
    policies:TreeMap[Address,_id]
    proposals:TreeMap[u256,_hx]
    releases:TreeMap[str,_ib]
    incidents:TreeMap[str,_hz]
    active_proposal_by_target:TreeMap[Address,u256]
    used_evidence_ids:TreeMap[str,bool]
    installed_candidate_hashes:TreeMap[str,bool]
    used_incident_ids:TreeMap[str,bool]
    proposal_count:u256
    release_count:u256

    def __init__(self):
        self.proposal_count=u256(0)
        self.release_count=u256(0)

    def _hr(self):
        _ak=str(gl.message_raw['datetime'])
        return int(datetime.fromisoformat(_ak.replace('Z','+00:00')).timestamp())

    def _hh(self,_fr):
        return hashlib.sha256(_fr).hexdigest()

    def _gt(self,_aj):
        return hashlib.sha256('\x1f'.join(_aj).encode('utf-8')).hexdigest()

    def _hf(self,_l):
        if len(_l)!=64:
            return False
        for _bv in _l:
            if _bv not in _s36:
                return False
        return True

    def _ge(self,_l):
        try:
            _bj=json.loads(_l)
            _dy=json.dumps(_bj,sort_keys=True,separators=(',',':'),ensure_ascii=False)
            if _dy!=_l:
                return(_s24,_bj)
            return(self._hh(_dy.encode('utf-8')),_bj)
        except Exception:
            return('INVALID',None)

    def _gp(self,_eb,_fc,_em,_es,_er,_c):
        if len(_eb.encode('utf-8'))>int(_c.far):
            return _hp+'TOO_LARGE'
        (_fg,_bj)=self._ge(_eb)
        if _fg in('INVALID',_s24)or not isinstance(_bj,dict):
            return _hp+'NOT_CANONICAL_JSON'
        _p=_bj
        _fm=('schema','target',_s37,_s1,_s28,'expected_release_version',_s6,_s4,_s16,_s17)
        for _cm in _fm:
            if _cm not in _p:
                return _hp+'MISSING_'+_cm.upper()
        if _p.get('schema')!=_ew:
            return _hp+'SCHEMA_MISMATCH'
        _du=_p.get('target')
        if not isinstance(_du,str)or _du.lower()!=str(_fc).lower():
            return _hp+'TARGET_MISMATCH'
        if _p.get(_s37)!=_em:
            return _hp+'CANDIDATE_HASH_MISMATCH'
        if _p.get(_s1)!=_es:
            return _hp+'POLICY_MISMATCH'
        if _p.get(_s28)!=_er:
            return _hp+'KERNEL_MISMATCH'
        if type(_p.get(_s6))is not int:
            return _hp+'OBSERVATION_DELAY_INVALID'
        if type(_p.get(_s4))is not int:
            return _hp+'ASSURANCE_DEADLINE_INVALID'
        if _p.get(_s6)!=int(_c.fh):
            return _hp+'OBSERVATION_DELAY_MISMATCH'
        if _p.get(_s4)!=int(_c.fe):
            return _hp+'ASSURANCE_DEADLINE_MISMATCH'
        if _p.get(_s16)is not True:
            return _hp+'CI_ASSURANCE_REQUIRED'
        if _p.get(_s17)is not True:
            return _hp+'INDEPENDENT_ASSURANCE_REQUIRED'
        for _ck in('required_state_checks','required_readback_checks','required_canary_checks'):
            _ea=_p.get(_ck,[])
            if not isinstance(_ea,list):
                return 'MANIFEST_'+_ck.upper()+_s53
            _l=_ea
            if len(_l)>32:
                return 'MANIFEST_'+_ck.upper()+_s53
            for _ef in _l:
                if not isinstance(_ef,str)or len(_ef.encode('utf-8'))>160:
                    return 'MANIFEST_'+_ck.upper()+'_ITEM_INVALID'
        return ''

    def _hg(self,_l,_dg,_df,_de):
        _dw=len(_l.encode('utf-8'))
        if _dw<_df or _dw>_de:
            raise gl.vm.UserError(f'{_dg} length is invalid')

    def _he(self,_l,_dg,_df,_de):
        if _l<_df or _l>_de:
            raise gl.vm.UserError(f'{_dg} is outside supported bounds')

    def _fv(self,_l):
        if not _l or _l in('.','..'):
            return False
        _fn='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'
        for _bv in _l:
            if _bv not in _fn:
                return False
        return True

    def _gr(self,_ai):
        _ee='https://raw.githubusercontent.com/'
        if not _ai.startswith(_ee)or not _ai.endswith('/'):
            return ''
        _fu=_ai[len(_ee):]
        _aj=_fu.split('/')
        if len(_aj)!=3 or _aj[2]!='':
            return ''
        _ax=_aj[0]
        _fj=_aj[1]
        if not self._fv(_ax):
            return ''
        if not self._fv(_fj):
            return ''
        return _ax

    def _gf(self,_ai):
        return self._gr(_ai)!=''

    def _gq(self,_dh,_ai):
        if len(_dh.encode('utf-8'))>_ff:
            return False
        if not self._gf(_ai):
            return False
        if not _dh.startswith(_ai):
            return False
        _fq=_dh[len(_ai):]
        _aj=_fq.split('/',1)
        if len(_aj)!=2:
            return False
        (_ed,_ft)=_aj
        if len(_ed)!=40:
            return False
        for _bv in _ed:
            if _bv not in _s36:
                return False
        _dt=_ft.split('/')
        if not _dt:
            return False
        for _fo in _dt:
            if not self._fv(_fo):
                return False
        return True

    def _gk(self,_h,_ax,_bi,_at,_av,_au,_ad,_aw,_ao,_bc,_be,_ba,_as,_ah,_aq,_al,_am,_ap,_az,_bf,_bg):
        return self._gt([_cx,str(_h),str(_ax),_bi,_at,_av,_au,_ad,_aw,_ao,str(_bc),str(_be),str(_ba),_as,_ah,_aq,_al,_am,str(_ap),str(_az),str(_bf),str(_bg)])

    def _gm(self,_aa,_ac,_s,_ab,_r,_y,_bd):
        return self._gt([_cx,_aa,_ac,_s,_ab,_r,_y,_bd])

    def _gn(self):
        return u256(0)

    def _gd(self,_h):
        if _h not in self.policies:
            raise gl.vm.UserError(_s0)
        _c=self.policies[_h]
        if gl.message.sender_address!=_c.fat:
            raise gl.vm.UserError(_s0)
        if not _c.fa:
            raise gl.vm.UserError(_s0)
        return _c

    def _gs(self,_d):
        if _d not in self.proposals:
            raise gl.vm.UserError(_s0)
        return self.proposals[_d]

    def _gx(self,_h,_d):
        active=self.active_proposal_by_target.get(_h,self._gn())
        if active==_d:
            self.active_proposal_by_target[_h]=self._gn()

    def _gi(self,_h,_fp,_fs,_dx):
        self._hg(_dx,'evidence_id',8,_fh)
        _dz=self._gt([str(_h),_fp,_fs,_dx])
        if self.used_evidence_ids.get(_dz,False):
            raise gl.vm.UserError(_s0)
        self.used_evidence_ids[_dz]=True

    def _fx(self,_h,_o):
        return self._gt([str(_h),_o])

    def _gg(self,_a):
        return 'release-'+str(_a.fbc)+'-'+_a.fo[:16]

    def _gh(self,_a):
        if _a.fbm==_s23:
            return _a.fbn
        return _a.fbn

    def _hd(self,_h,_ep,_e,_do,_ec,_bu,_bl,_bm,_y,_bd):
        return self._gt([_cx,str(_h),_ep,_e,_do,_ec,_bu,_bl,_bm,_y,_bd])

    def _fy(self,_d,_a,_fi):
        _c=self.policies[_a.fbw]
        if _c.fab!=_a.fau:
            raise gl.vm.UserError(_s0)
        _e=self._gg(_a)
        if _e in self.releases:
            _fk=self.releases[_e]
            if _fk.fw!=_a.fo:
                raise gl.vm.UserError(_s0)
            _a.fbv=_ae
            return
        _dr=self.releases.get(_c.fac)
        if _dr is None:
            raise gl.vm.UserError(_s0)
        _j=self._hr()
        lineage_hash=self._hd(_a.fbw,_dr.fao,_e,_c.fac,_a.fq,_a.fo,_a.fay,_a.faf,_a.fg,_a.fbh)
        self.releases[_e]=_ib(fbq=_e,fbw=_a.fbw,fbx=_a.fq,fav=_c.fac,fau=_a.fau,fbu=_a.fp,fw=_a.fo,fbc=_d,fay=_a.fay,faf=_a.faf,fg=_a.fg,fbh=_a.fbh,fal=u64(_j),fr=u64(0),fbv=_ae,fbf='',fbl='',fao=lineage_hash)
        _a.fbv=_ae
        _a.fan=_fi
        self.installed_candidate_hashes[self._fx(_a.fbw,_a.fo)]=True

    def _hi(self):
        return _ht(Address(_cg))

    def _ha(self,_ak,_fl):
        try:
            _l=json.loads(_ak)
        except Exception:
            raise gl.vm.UserError(_s0)
        if not isinstance(_l,dict):
            raise gl.vm.UserError(_s0)
        for(_cm,_fe)in _fl.items():
            if _l.get(_cm)!=_fe:
                raise gl.vm.UserError(_s0)
        return _l

    def _fw(self,_a,_c,_j):
        _cf=self._gp(_a.ff,_a.fbw,_a.fo,_a.fay,_c.fbb,_c)
        return json.dumps({_s11:int(_a.fbc),'target':str(_a.fbw),_s41:_a.fax,'parent_source_url':_a.faw,_s13:_a.fau,_s15:_a.fq,'candidate_source_url':_a.fp,_s5:_a.fo,'candidate_code_hex':_a.fn.hex(),'ci_evidence_url':_a.fu,'ci_evidence_id':_a.ft,'audit_evidence_url':_a.fl,'audit_evidence_id':_a.fk,'assurance_manifest':_a.ff,_s3:_a.fg,_s43:_a.fbm,_s32:_a.fbn,_s39:_a.fbp,'recovery_source_url':_a.fbo,'recovery_code_hash':_a.fbj,_s2:_a.fbh,'recovery_code_hex':_a.fbi.hex(),_s12:_a.faf,_s1:_a.fay,_s45:_c.fx,_s46:_c.fbb,_s44:_c.fs,_s19:_c.fj,_s7:int(_c.faq),_s33:int(_c.far),_s6:int(_c.fh),_s4:int(_c.fe),_s29:_j,'manifest_error':_cf},sort_keys=True,separators=(',',':'))

    def _gb(self,_d,_k):
        _a=self._gs(_d)
        _c=self.policies[_a.fbw]
        if _k['kind']==_cy:
            _a.fbv=_ch
            _a.fan=str(_k.get(_s9,''))
            return
        if _k['kind']==_db:
            _a.fbv=_cj
            _a.fan=str(_k.get(_s9,''))
            return
        if _k['kind']!=_fa:
            raise gl.vm.UserError(_s0)
        _a.fan=str(_k.get(_s9,''))
        if _k[_s25]==_ez:
            _a.fbv=_fb
            self._gx(_a.fbw,_d)
            return
        if _k[_s25]!=_cu:
            raise gl.vm.UserError(_s0)
        _a.fbv=_bh
        _a.fag=u64(self._hr()+int(_c.fah))
        _hv(_a.fbw).emit(on=_s8).proofpatch_upgrade(_d,_a.fo)

    def _gj(self,_a,_c,_e,_v,_dd,_u,_cv,_j,_m):
        return json.dumps({'target':str(_a.fbw),_s11:int(_a.fbc),_s10:_e,_s5:_a.fo,_s1:_a.fay,_s3:_a.fg,_s47:_v,_s31:_dd,_s35:_u,_s22:_cv,_s30:_c.fb,_s26:_c.fc,_s7:int(_c.faq),_s29:_j,'installed_proposal_id':int(_m.proofpatch_installed_proposal_id()),'installed_candidate_hash':_m.proofpatch_installed_candidate_hash(),'installed_release_id':_m.proofpatch_installed_release_id(),'installed_mode':_m.proofpatch_release_mode(),'installed_kernel_hash':_m.get_proofpatch_kernel_hash(),_s46:_c.fbb},sort_keys=True,separators=(',',':'))

    def _fz(self,_d,_k,_v,_dd,_u,_cv):
        _a=self._gs(_d)
        _e=self._gg(_a)
        if _k['kind']==_cy:
            _a.fbv=_bx
            _a.fan=str(_k.get(_s9,''))
            return
        if _k['kind']==_db:
            _a.fbv=_by
            _a.fan=str(_k.get(_s9,''))
            return
        _a.fan=str(_k.get(_s9,''))
        if _k.get(_s25)==_cu:
            _a.fbv=_ay
            self.releases[_e].fbv=_ay
            _hv(_a.fbw).emit(on=_s8).proofpatch_activate(_e,_a.fo)
            return
        _a.fbv=_z
        _j=self._hr()
        _c=self.policies[_a.fbw]
        self.incidents[_s49+_e]=_hz(faj=_s49+_e,fbw=_a.fbw,fbq=_e,fam=_a.fo,fak=_hl+'FAILURE',fba=_v,faz=_dd,fz=_u,fy=_cv,fay=_a.fay,fg=_a.fg,fbh=_a.fbh,fas=u64(_j),fai=u64(_j+int(_c.fbd)),fbr=u64(_j),fbk=u64(0),fbv=_z,fan=_hl+'FAILED',fbg=False)
        self.releases[_e].fbv=_z

    def _go(self,_b,_c,_f,_a,_j):
        return json.dumps({_s27:_b.faj,'target':str(_b.fbw),_s10:_b.fbq,_s14:_b.fam,_s42:_b.fak,_s47:_b.fba,_s31:_b.faz,_s35:_b.fz,_s22:_b.fy,_s1:_b.fay,_s2:_b.fbh,_s19:_c.fj,_s26:_c.fc,_s7:int(_c.faq),_s29:_j,'release_code_hash':_f.fw,'proposal_recovery_capsule_hash':_a.fbh},sort_keys=True,separators=(',',':'))

    def _ga(self,_g,_k):
        _b=self.incidents[_g]
        _f=self.releases[_b.fbq]
        _a=self.proposals[_f.fbc]
        _b.fbr=u64(self._hr())
        _b.fan=str(_k.get(_s9,''))
        if _k['kind']==_cy:
            _b.fbv=_eo
            return
        if _k['kind']==_db:
            _b.fbv=_dk
            return
        if _k.get(_s25)!=_cu:
            _b.fbv=_ei
            _eg=_hv(_b.fbw).view(state=StorageType.LATEST_FINAL).proofpatch_release_mode()
            _f.fbv=_ae if _eg==_bn else _an
            _a.fbv=_ae if _eg==_bn else _an
            return
        _b.fbv=_af
        _b.fbg=True
        _b.fbk=u64(self._hr()+int(self.policies[_b.fbw].fah))
        _f.fbv=_af
        _hv(_b.fbw).emit(on=_s8).proofpatch_recover(_g,_b.fbq,_b.fbh)

    @gl.public.write
    def register_target(self,_ax:str,_bi:str,_at:str,_av:str,_au:str,_ad:str,_aw:str,_ao:str,_as:str,_ah:str,_aq:str,_al:str,_am:str,_bq:str,_cc:str,_ag:str,_bc:int,_be:int,_ba:int,_ap:int,_az:int,_bf:int,_bg:int)->None:
        _h=gl.message.sender_address
        _da=Address(_ax)
        if _h in self.policies:
            raise gl.vm.UserError(_s0)
        if _da==Address('0x0000000000000000000000000000000000000000'):
            raise gl.vm.UserError(_s0)
        self._hg(_bi,_s45,80,_en)
        self._hg(_at,'source_authority',3,160)
        self._hg(_av,_s44,3,160)
        self._hg(_au,_s19,3,160)
        self._hg(_as,_s30,3,160)
        self._hg(_aq,'assurance_corroboration_authority',3,160)
        self._hg(_bq,'current_version',1,_ct)
        if len({_at,_av,_au,_as,_aq})!=5:
            raise gl.vm.UserError(_s0)
        if not self._gf(_ad):
            raise gl.vm.UserError(_s0)
        if not self._gf(_aw):
            raise gl.vm.UserError(_s0)
        if not self._gf(_ao):
            raise gl.vm.UserError(_s0)
        if not self._gf(_ah):
            raise gl.vm.UserError(_s0)
        if not self._gf(_al):
            raise gl.vm.UserError(_s0)
        if len({_ad,_aw,_ao,_ah,_al})!=5:
            raise gl.vm.UserError(_s0)
        if self._gr(_ad).lower()==self._gr(_ao).lower():
            raise gl.vm.UserError(_s0)
        if self._gr(_ad).lower()==self._gr(_ah).lower():
            raise gl.vm.UserError(_s0)
        if self._gr(_ah).lower()==self._gr(_al).lower():
            raise gl.vm.UserError(_s0)
        _am=_am.lower()
        if not self._hf(_am):
            raise gl.vm.UserError(_s0)
        _ag=_ag.lower()
        if not self._hf(_ag):
            raise gl.vm.UserError(_s0)
        if not self._gq(_cc,_ad):
            raise gl.vm.UserError(_s0)
        self._he(_bc,_s7,_ca,_ej)
        self._he(_be,'proposal_ttl_seconds',_ca,_ek)
        self._he(_ba,'execution_timeout_seconds',_ca,_co)
        self._he(_ap,'assurance_observation_delay_seconds',_ca,_co)
        self._he(_az,_s4,_ap,_co)
        self._he(_bf,_s33,256,128000)
        self._he(_bg,'max_capsule_bytes',1,_dm)
        _dc=self._gk(_h,_da,_bi,_at,_av,_au,_ad,_aw,_ao,_bc,_be,_ba,_as,_ah,_aq,_al,_am,_ap,_az,_bf,_bg)
        self.policies[_h]=_id(fat=_da,fbw=_h,fx=_bi,fay=_dc,fbs=_at,fs=_av,fj=_au,fbt=_ad,fv=_aw,fm=_ao,fb=_as,fi=_ah,fc=_aq,fd=_al,fbb=_am,fae=_bq,fad=_cc,fab=_ag,fac='',faq=u64(_bc),fbd=u64(_be),fah=u64(_ba),fh=u64(_ap),fe=u64(_az),far=u64(_bf),fap=u64(_bg),fa=True)
        _br='root-'+_ag[:16]
        _ev=self._hd(_h,'',_br,'',_bq,_ag,_dc,'','','')
        self.releases[_br]=_ib(fbq=_br,fbw=_h,fbx=_bq,fav='',fau='',fbu=_cc,fw=_ag,fbc=u256(0),fay=_dc,faf='',fg='',fbh='',fal=u64(self._hr()),fr=u64(self._hr()),fbv=_s34,fbf='',fbl='',fao=_ev)
        self.policies[_h].fac=_br
        self.active_proposal_by_target[_h]=self._gn()
        _hv(_h).emit(on=_s8).proofpatch_confirm_registration(_br,_ag)

    @gl.public.write
    def create_proposal(self,_h:str,_cd:str,_aa:str,_bs:bytes,_ac:str,_s:str,_ab:str,_r:str,_cb:str,_ci:str,_q:str,_ce:str,_cs:str,_bt:bytes)->u256:
        _i=Address(_h)
        _c=self._gd(_i)
        active=self.active_proposal_by_target.get(_i,self._gn())
        if active!=self._gn():
            raise gl.vm.UserError(_s0)
        self._hg(_cd,_s15,1,_ct)
        if _cd==_c.fae:
            raise gl.vm.UserError(_s0)
        if len(_bs)==0 or len(_bs)>_dm:
            raise gl.vm.UserError(_s0)
        if not self._gq(_aa,_c.fbt):
            raise gl.vm.UserError(_s0)
        if not self._gq(_ac,_c.fv):
            raise gl.vm.UserError(_s0)
        if not self._gq(_ab,_c.fm):
            raise gl.vm.UserError(_s0)
        if not self._gq(_cs,_c.fbt):
            raise gl.vm.UserError(_s0)
        if _s==_r:
            raise gl.vm.UserError(_s0)
        if _ci not in(_s23,_hq+_s51):
            raise gl.vm.UserError(_s0)
        if len(_bt)==0 or len(_bt)>int(_c.fap):
            raise gl.vm.UserError(_s0)
        self._hg(_ce,_s39,1,_ct)
        _o=self._hh(_bs)
        if _o==_c.fab:
            raise gl.vm.UserError(_s0)
        if self.installed_candidate_hashes.get(self._fx(_i,_o),False):
            raise gl.vm.UserError(_s0)
        _n=self._hh(_bt)
        if _ci==_s23:
            if _q!=_c.fac:
                raise gl.vm.UserError(_s0)
            if _n!=_c.fab:
                raise gl.vm.UserError(_s0)
            if _ce!=_c.fae:
                raise gl.vm.UserError(_s0)
        else:
            if _q!='recovery-'+_n[:16]:
                raise gl.vm.UserError(_s0)
            if _n==_o:
                raise gl.vm.UserError(_s0)
        (_y,_hs)=self._ge(_cb)
        if _y in('INVALID',_s24):
            raise gl.vm.UserError(_s0)
        _cf=self._gp(_cb,_i,_o,_c.fay,_c.fbb,_c)
        if _cf:
            raise gl.vm.UserError(_cf)
        self._gi(_i,_c.fs,'ci',_s)
        self._gi(_i,_c.fj,'audit',_r)
        _j=self._hr()
        _d=u256(int(self.proposal_count)+1)
        _bm=self._gm(_aa,_ac,_s,_ab,_r,_y,_n)
        self.proposals[_d]=_hx(fbc=_d,fbw=_i,fbe=_c.fat,fax=_c.fae,faw=_c.fad,fau=_c.fab,fq=_cd,fp=_aa,fn=_bs,fo=_o,fu=_ac,ft=_s,fl=_ab,fk=_r,ff=_cb,fg=_y,fbm=_ci,fbn=_q,fbp=_ce,fbo=_cs,fbi=_bt,fbj=_n,fbh=_n,faf=_bm,fay=_c.fay,faa=u64(_j),fai=u64(_j+int(_c.fbd)),fbr=u64(0),fag=u64(0),fbv=_bp,fan='')
        self.proposal_count=_d
        self.active_proposal_by_target[_i]=_d
        return _d

    @gl.public.write
    def repair_evidence(self,_d:u256,_aa:str,_ac:str,_s:str,_ab:str,_r:str)->None:
        _a=self._gs(_d)
        _c=self._gd(_a.fbw)
        if _a.fbv!=_ch:
            raise gl.vm.UserError(_s0)
        if self._hr()>int(_a.fai):
            raise gl.vm.UserError(_s0)
        if not self._gq(_aa,_c.fbt):
            raise gl.vm.UserError(_s0)
        if not self._gq(_ac,_c.fv):
            raise gl.vm.UserError(_s0)
        if not self._gq(_ab,_c.fm):
            raise gl.vm.UserError(_s0)
        if _s==_r:
            raise gl.vm.UserError(_s0)
        self._gi(_a.fbw,_c.fs,'ci',_s)
        self._gi(_a.fbw,_c.fj,'audit',_r)
        _a.fp=_aa
        _a.fu=_ac
        _a.ft=_s
        _a.fl=_ab
        _a.fk=_r
        _a.faf=self._gm(_aa,_ac,_s,_ab,_r,_a.fg,_a.fbh)
        _a.fbv=_bp
        _a.fan=''

    @gl.public.write
    def cancel_proposal(self,_d:u256)->None:
        _a=self._gs(_d)
        self._gd(_a.fbw)
        if _a.fbv not in(_bp,_ch,_cj):
            raise gl.vm.UserError(_s0)
        _a.fbv=_ex
        _a.fan='OWNER_CANCELLED'
        self._gx(_a.fbw,_d)

    @gl.public.write
    def expire_proposal(self,_d:u256)->None:
        _a=self._gs(_d)
        if _a.fbv not in(_bp,_ch,_cj):
            raise gl.vm.UserError(_s0)
        if self._hr()<=int(_a.fai):
            raise gl.vm.UserError(_s0)
        _a.fbv=_fd
        _a.fan='PROPOSAL_EXPIRED'
        self._gx(_a.fbw,_d)

    @gl.public.write
    def review_proposal(self,_d:u256)->None:
        if gl.message.sender_address==Address(_cg):
            _a=self._gs(_d)
            if _a.fbv!=_cq:
                raise gl.vm.UserError(_s0)
            _ak=self._hi().view(state=StorageType.LATEST_FINAL).get_proposal_result(_d)
            _k=self._ha(_ak,{'target':str(_a.fbw),_s11:int(_d),_s13:_a.fau,_s5:_a.fo,_s1:_a.fay,_s12:_a.faf,_s3:_a.fg,_s2:_a.fbh})
            _a.fbr=u64(self._hr())
            self._gb(_d,_k)
            return
        _a=self._gs(_d)
        if _a.fbv not in(_bp,_cj,_cq):
            raise gl.vm.UserError(_s0)
        _j=self._hr()
        if _j>int(_a.fai):
            raise gl.vm.UserError(_s0)
        _c=self.policies[_a.fbw]
        if not _c.fa or _c.fay!=_a.fay or _c.fab!=_a.fau:
            raise gl.vm.UserError(_s0)
        _a.fbv=_cq
        _a.fbr=u64(_j)
        _a.fan=_s20
        self._hi().emit(on=_s8).review_proposal(_d,self._fw(_a,_c,_j))

    @gl.public.view
    def is_upgrade_authorized(self,_d:u256,_h:str,_o:str)->bool:
        if _d not in self.proposals:
            return False
        _a=self.proposals[_d]
        if _a.fbv!=_bh:
            return False
        if str(_a.fbw).lower()!=str(Address(_h)).lower():
            return False
        if _a.fo!=_o.lower():
            return False
        if self._hr()>int(_a.fag):
            return False
        if self.active_proposal_by_target.get(_a.fbw,self._gn())!=_d:
            return False
        return True

    @gl.public.view
    def get_candidate_code(self,_d:u256)->bytes:
        if _d not in self.proposals:
            raise gl.vm.UserError(_s0)
        _a=self.proposals[_d]
        if _a.fbv!=_bh:
            raise gl.vm.UserError(_s0)
        if self._hr()>int(_a.fag):
            raise gl.vm.UserError(_s0)
        return _a.fn

    @gl.public.write
    def confirm_install(self,_d:u256,_o:str)->None:
        _a=self._gs(_d)
        if gl.message.sender_address!=_a.fbw:
            raise gl.vm.UserError(_s0)
        _dp=_o.lower()
        if _a.fbv in(_ae,_bb,_ay,_an):
            if _dp!=_a.fo:
                raise gl.vm.UserError(_s0)
            return
        if _a.fbv!=_bh:
            raise gl.vm.UserError(_s0)
        if _dp!=_a.fo:
            raise gl.vm.UserError(_s0)
        _m=_hv(_a.fbw).view(state=StorageType.LATEST_FINAL)
        _cr=_m.proofpatch_installed_proposal_id()
        _cp=_m.proofpatch_installed_candidate_hash()
        if _cr!=_d:
            raise gl.vm.UserError(_s0)
        if _cp!=_a.fo:
            raise gl.vm.UserError(_s0)
        _et=_m.proofpatch_installed_release_id()
        if _et!=self._gg(_a):
            raise gl.vm.UserError(_s0)
        if _m.proofpatch_release_mode()!=_bn:
            raise gl.vm.UserError(_s0)
        if _m.get_proofpatch_kernel_hash()!=self.policies[_a.fbw].fbb:
            raise gl.vm.UserError(_s0)
        self._fy(_d,_a,'INSTALL_VERIFIED')

    @gl.public.write
    def reconcile_install(self,_d:u256)->None:
        _a=self._gs(_d)
        self._gd(_a.fbw)
        if _a.fbv!=_bh:
            raise gl.vm.UserError(_s0)
        _m=_hv(_a.fbw).view(state=StorageType.LATEST_FINAL)
        _cr=_m.proofpatch_installed_proposal_id()
        _cp=_m.proofpatch_installed_candidate_hash()
        if _cr!=_d:
            raise gl.vm.UserError(_s0)
        if _cp!=_a.fo:
            raise gl.vm.UserError(_s0)
        if _m.proofpatch_installed_release_id()!=self._gg(_a):
            raise gl.vm.UserError(_s0)
        if _m.proofpatch_release_mode()!=_bn:
            raise gl.vm.UserError(_s0)
        self._fy(_d,_a,'INSTALL_RECONCILED')

    @gl.public.write
    def mark_execution_timeout(self,_d:u256)->None:
        _a=self._gs(_d)
        _c=self._gd(_a.fbw)
        if _a.fbv!=_bh:
            raise gl.vm.UserError(_s0)
        if self._hr()<=int(_a.fag):
            raise gl.vm.UserError(_s0)
        _h=_hv(_a.fbw)
        _dq=_h.view(state=StorageType.LATEST_FINAL)
        _bz=_dq.proofpatch_installed_proposal_id()
        _bw=_dq.proofpatch_installed_candidate_hash()
        if _bz==_d and _bw==_a.fo:
            self._fy(_d,_a,'INSTALL_RECONCILED_TIMEOUT')
            return
        _eh=_bz==self._gn()and _bw=='' or(_bz!=_d and _bw==_c.fab)
        if not _eh:
            raise gl.vm.UserError(_s0)
        _ds=_h.view(state=StorageType.LATEST_NON_FINAL)
        _dl=_ds.proofpatch_installed_proposal_id()
        _dj=_ds.proofpatch_installed_candidate_hash()
        if _dl==_d and _dj==_a.fo:
            raise gl.vm.UserError(_s0)
        if _dl!=_bz or _dj!=_bw:
            raise gl.vm.UserError(_s0)
        _a.fbv=_el
        _a.fan='EXECUTION_TIMEOUT'
        self._gx(_a.fbw,_d)

    @gl.public.view
    def is_activation_authorized(self,_d:u256,_e:str,_o:str)->bool:
        if _d not in self.proposals:
            return False
        _a=self.proposals[_d]
        return _a.fbv==_ay and _e==self._gg(_a)and(_o.lower()==_a.fo)and(_e in self.releases)and(self.releases[_e].fbv==_ay)

    @gl.public.view
    def is_registration_authorized(self,_h:str,_e:str,_bu:str)->bool:
        _i=Address(_h)
        if _i not in self.policies:
            return False
        _c=self.policies[_i]
        return _c.fac==_e and _c.fab==_bu.lower()and(_e in self.releases)and(self.releases[_e].fbv==_s34)

    @gl.public.write
    def assure_release(self,_d:u256,_v:str,_t:str,_u:str,_x:str)->None:
        _a=self._gs(_d)
        _e=self._gg(_a)
        if gl.message.sender_address==Address(_cg):
            if _a.fbv!=_bb:
                raise gl.vm.UserError(_s0)
            _ak=self._hi().view(state=StorageType.LATEST_FINAL).get_assurance_result(_d)
            _k=self._ha(_ak,{'target':str(_a.fbw),_s11:int(_d),_s10:_e,_s5:_a.fo,_s1:_a.fay,_s3:_a.fg})
            self._fz(_d,_k,_v,_t,_u,_x)
            return
        if _a.fbv not in(_ae,_bx,_by,_bb):
            raise gl.vm.UserError(_s0)
        if _e not in self.releases:
            raise gl.vm.UserError(_s0)
        _f=self.releases[_e]
        _c=self.policies[_a.fbw]
        _j=self._hr()
        if _j<int(_f.fal)+int(_c.fh):
            raise gl.vm.UserError(_s0)
        if _j>int(_f.fal)+int(_c.fe):
            raise gl.vm.UserError(_s0)
        if not self._gq(_v,_c.fi)or not self._gq(_u,_c.fd):
            raise gl.vm.UserError(_s0)
        if _t==_x:
            raise gl.vm.UserError(_s0)
        self._gi(_a.fbw,_c.fb,'assurance_primary',_t)
        self._gi(_a.fbw,_c.fc,'assurance_corroboration',_x)
        _w=_hv(_a.fbw).view(state=StorageType.LATEST_FINAL)
        _a.fbv=_bb
        _a.fbr=u64(_j)
        _a.fan=_s20
        _cl=self._gj(_a,_c,_e,_v,_t,_u,_x,_j,_w)
        self._hi().emit(on=_s8).assure_release(_d,_cl)

    @gl.public.write
    def confirm_activation(self,_d:u256,_e:str,_o:str)->None:
        _a=self._gs(_d)
        if gl.message.sender_address!=_a.fbw:
            raise gl.vm.UserError(_s0)
        if _a.fbv==_an:
            return
        if _a.fbv!=_ay:
            raise gl.vm.UserError(_s0)
        if _e!=self._gg(_a)or _o.lower()!=_a.fo:
            raise gl.vm.UserError(_s0)
        _w=_hv(_a.fbw).view(state=StorageType.LATEST_FINAL)
        if _w.proofpatch_installed_release_id()!=_e:
            raise gl.vm.UserError(_s0)
        if _w.proofpatch_installed_candidate_hash()!=_a.fo:
            raise gl.vm.UserError(_s0)
        if _w.proofpatch_release_mode()!=_dv:
            raise gl.vm.UserError(_s0)
        _f=self.releases[_e]
        _j=self._hr()
        _f.fbv=_an
        _f.fr=u64(_j)
        _a.fbv=_an
        _a.fan='CERTIFICATION_VERIFIED'
        _c=self.policies[_a.fbw]
        _c.fae=_a.fq
        _c.fad=_a.fp
        _c.fab=_a.fo
        _c.fac=_e
        self._gx(_a.fbw,_d)

    @gl.public.write
    def expire_provisional_release(self,_e:str)->None:
        if _e not in self.releases:
            raise gl.vm.UserError(_s0)
        _f=self.releases[_e]
        if _f.fbv not in(_ae,_bb,_bx,_by):
            raise gl.vm.UserError(_s0)
        _c=self.policies[_f.fbw]
        if self._hr()<=int(_f.fal)+int(_c.fe):
            raise gl.vm.UserError(_s0)
        _g='timeout-'+_e
        if _g not in self.incidents:
            _a=self.proposals[_f.fbc]
            self.incidents[_g]=_hz(faj=_g,fbw=_f.fbw,fbq=_e,fam=_f.fw,fak=_hl+'TIMEOUT',fba='',faz='',fz='',fy='',fay=_f.fay,fg=_f.fg,fbh=_f.fbh,fas=u64(self._hr()),fai=u64(self._hr()+int(_c.fbd)),fbr=u64(0),fbk=u64(0),fbv=_z,fan=_hl+'DEADLINE_EXPIRED',fbg=False)
            _a.fbv=_z
        _f.fbv=_z

    @gl.public.write
    def open_incident(self,_h:str,_e:str,_cz:str,_v:str,_t:str,_u:str,_x:str)->str:
        _i=Address(_h)
        if _i not in self.policies or _e not in self.releases:
            raise gl.vm.UserError(_s0)
        _f=self.releases[_e]
        if _f.fbw!=_i:
            raise gl.vm.UserError(_s0)
        if _cz not in('STATE_INVARIANT_VIOLATION','AUTHORIZATION_REGRESSION','UPGRADE_BYPASS','CONSENSUS_BINDING_REGRESSION',_hn+'TRUST_REGRESSION','FINALITY_REGRESSION','LIVENESS_REGRESSION','HIDDEN_VALUE_TRANSFER','KERNEL_INTEGRITY_FAILURE','REQUIRED_INTERFACE_FAILURE','OTHER_CONSTITUTIONAL_BREACH'):
            raise gl.vm.UserError(_s0)
        _c=self.policies[_i]
        if not self._gq(_v,_c.fm):
            raise gl.vm.UserError(_s0)
        if not self._gq(_u,_c.fd):
            raise gl.vm.UserError(_s0)
        if _t==_x:
            raise gl.vm.UserError(_s0)
        self._gi(_i,_c.fj,'incident_primary',_t)
        self._gi(_i,_c.fc,'incident_corroboration',_x)
        _m=_hv(_i).view(state=StorageType.LATEST_FINAL)
        if _m.proofpatch_installed_release_id()!=_e:
            raise gl.vm.UserError(_s0)
        if _m.proofpatch_release_mode()not in(_dv,_bn,_cw):
            raise gl.vm.UserError(_s0)
        if _f.fbh=='':
            raise gl.vm.UserError(_s0)
        if _f.fbv not in(_an,_ae,_bb,_bx,_by,_z):
            raise gl.vm.UserError(_s0)
        _g='incident-'+str(self._hr())+'-'+_t
        if _g in self.incidents:
            raise gl.vm.UserError(_s0)
        _dn=self._gt([str(_i),_e,_t,_x])
        if self.used_incident_ids.get(_dn,False):
            raise gl.vm.UserError(_s0)
        self.used_incident_ids[_dn]=True
        self.incidents[_g]=_hz(faj=_g,fbw=_i,fbq=_e,fam=_f.fw,fak=_cz,fba=_v,faz=_t,fz=_u,fy=_x,fay=_f.fay,fg=_f.fg,fbh=_f.fbh,fas=u64(self._hr()),fai=u64(self._hr()+int(_c.fbd)),fbr=u64(0),fbk=u64(0),fbv=_z,fan='',fbg=False)
        _f.fbv=_z
        return _g

    @gl.public.write
    def review_incident(self,_g:str)->None:
        if _g not in self.incidents:
            raise gl.vm.UserError(_s0)
        _b=self.incidents[_g]
        if gl.message.sender_address==Address(_cg):
            if _b.fbv!=_cn:
                raise gl.vm.UserError(_s0)
            _ak=self._hi().view(state=StorageType.LATEST_FINAL).get_incident_result(_g)
            _k=self._ha(_ak,{_s27:_g,'target':str(_b.fbw),_s10:_b.fbq,_s14:_b.fam,_s1:_b.fay,_s2:_b.fbh})
            self._ga(_g,_k)
            return
        if _b.fbv not in(_z,_dk,_cn):
            raise gl.vm.UserError(_s0)
        if self._hr()>int(_b.fai):
            raise gl.vm.UserError(_s0)
        _c=self.policies[_b.fbw]
        _f=self.releases[_b.fbq]
        _a=self.proposals[_f.fbc]
        _j=self._hr()
        _b.fbv=_cn
        _b.fbr=u64(_j)
        _b.fan=_s20
        self._hi().emit(on=_s8).review_incident(_g,self._go(_b,_c,_f,_a,_j))

    @gl.public.view
    def is_recovery_authorized(self,_g:str,_e:str,_n:str)->bool:
        if _g not in self.incidents or _e not in self.releases:
            return False
        _b=self.incidents[_g]
        return _b.fbv in(_af,_bk,_ar)and _b.fbg and(_b.fbq==_e)and(_b.fbh==_n.lower())

    @gl.public.view
    def get_recovery_release_id(self,_g:str)->str:
        if _g not in self.incidents:
            return ''
        _b=self.incidents[_g]
        if _b.fbq not in self.releases:
            return ''
        _f=self.releases[_b.fbq]
        if _f.fbc not in self.proposals:
            return ''
        return self._gh(self.proposals[_f.fbc])

    @gl.public.view
    def get_recovery_code(self,_g:str)->bytes:
        if _g not in self.incidents:
            raise gl.vm.UserError(_s0)
        _b=self.incidents[_g]
        _f=self.releases[_b.fbq]
        _a=self.proposals[_f.fbc]
        if _b.fbv not in(_af,_bk,_ar):
            raise gl.vm.UserError(_s0)
        return _a.fbi

    def _gl(self,_g,_e,_n):
        if _g not in self.incidents:
            raise gl.vm.UserError(_s0)
        _b=self.incidents[_g]
        if _b.fbv==_bo:
            return
        if _b.fbv not in(_af,_bk,_ar)or _e!=_b.fbq:
            raise gl.vm.UserError(_s0)
        if _n.lower()!=_b.fbh:
            raise gl.vm.UserError(_s0)
        _w=_hv(_b.fbw).view(state=StorageType.LATEST_FINAL)
        _a=self.proposals[self.releases[_e].fbc]
        _di=self._gh(_a)
        if _w.proofpatch_installed_release_id()!=_di:
            raise gl.vm.UserError(_s0)
        if _w.proofpatch_installed_candidate_hash()!=_n.lower():
            raise gl.vm.UserError(_s0)
        if _w.proofpatch_release_mode()!=_cw:
            raise gl.vm.UserError(_s0)
        _b.fbv=_bo
        _b.fan=_hq+'VERIFIED'
        self.releases[_e].fbv=_bo
        self.releases[_e].fbl=_g
        _c=self.policies[_b.fbw]
        _a=self.proposals[self.releases[_e].fbc]
        _q=_di
        if _a.fbm==_hq+_s51:
            if _q in self.releases:
                _eu=self.releases[_q]
                if _eu.fw!=_n.lower():
                    raise gl.vm.UserError(_s0)
            else:
                _ey=self.releases[_e]
                _eq=self._hd(_b.fbw,_ey.fao,_q,_e,_a.fbp,_n.lower(),_a.fay,_a.faf,_a.fg,_a.fbh)
                self.releases[_q]=_ib(fbq=_q,fbw=_b.fbw,fbx=_a.fbp,fav=_e,fau=_b.fam,fbu=_a.fbo,fw=_n.lower(),fbc=_a.fbc,fay=_a.fay,faf=_a.faf,fg=_a.fg,fbh=_a.fbh,fal=u64(self._hr()),fr=u64(self._hr()),fbv=_bo,fbf=_e,fbl=_g,fao=_eq)
        elif _q not in self.releases:
            raise gl.vm.UserError(_s0)
        _c.fae=_a.fbp
        _c.fad=_a.fbo
        _c.fab=_n.lower()
        _c.fac=_q
        self._gx(_b.fbw,_a.fbc)

    @gl.public.write
    def confirm_recovery(self,_g:str,_e:str,_n:str)->None:
        if _g not in self.incidents:
            raise gl.vm.UserError(_s0)
        _b=self.incidents[_g]
        if gl.message.sender_address!=_b.fbw:
            raise gl.vm.UserError(_s0)
        if _b.fbv!=_bo and self._hr()>int(_b.fbk):
            raise gl.vm.UserError(_s0)
        self._gl(_g,_e,_n)

    @gl.public.write
    def reconcile_recovery(self,_g:str)->None:
        if _g not in self.incidents:
            raise gl.vm.UserError(_s0)
        _b=self.incidents[_g]
        if _b.fbv not in(_af,_bk,_ar):
            raise gl.vm.UserError(_s0)
        self._gl(_g,_b.fbq,_b.fbh)

    @gl.public.write
    def expire_recovery(self,_g:str)->None:
        if _g not in self.incidents:
            raise gl.vm.UserError(_s0)
        _b=self.incidents[_g]
        if _b.fbv not in(_af,_bk):
            raise gl.vm.UserError(_s0)
        if self._hr()<=int(_b.fbk):
            raise gl.vm.UserError(_s0)
        _w=_hv(_b.fbw).view(state=StorageType.LATEST_FINAL)
        if _w.proofpatch_release_mode()==_cw:
            self._gl(_g,_b.fbq,_b.fbh)
            return
        _b.fbv=_ar
        self.releases[_b.fbq].fbv=_ar

    @gl.public.write
    def retry_recovery(self,_g:str)->None:
        if _g not in self.incidents:
            raise gl.vm.UserError(_s0)
        _b=self.incidents[_g]
        if _b.fbv!=_ar:
            raise gl.vm.UserError(_s0)
        _c=self.policies[_b.fbw]
        _j=self._hr()
        _b.fbv=_af
        _b.fbk=u64(_j+int(_c.fah))
        self.releases[_b.fbq].fbv=_af
        _hv(_b.fbw).emit(on=_s8).proofpatch_recover(_g,_b.fbq,_b.fbh)

    @gl.public.view
    def get_proposal_count(self)->u256:
        return self.proposal_count

    @gl.public.view
    def get_proposal_status(self,_d:u256)->str:
        if _d not in self.proposals:
            return 'UNKNOWN'
        return self.proposals[_d].fbv

    @gl.public.view
    def get_candidate_hash(self,_d:u256)->str:
        if _d not in self.proposals:
            return ''
        return self.proposals[_d].fo

    @gl.public.view
    def get_proposal_release_id(self,_d:u256)->str:
        if _d not in self.proposals:
            return ''
        return self._gg(self.proposals[_d])

    @gl.public.view
    def get_evidence_set_hash(self,_d:u256)->str:
        if _d not in self.proposals:
            return ''
        return self.proposals[_d].faf

    @gl.public.view
    def get_policy_fingerprint(self,_h:str)->str:
        _i=Address(_h)
        if _i not in self.policies:
            return ''
        return self.policies[_i].fay

    @gl.public.view
    def get_policy_kernel_hash(self,_h:str)->str:
        _i=Address(_h)
        if _i not in self.policies:
            return ''
        return self.policies[_i].fbb

    @gl.public.view
    def get_current_code_hash(self,_h:str)->str:
        _i=Address(_h)
        if _i not in self.policies:
            return ''
        return self.policies[_i].fab

    @gl.public.view
    def get_current_version(self,_h:str)->str:
        _i=Address(_h)
        if _i not in self.policies:
            return ''
        return self.policies[_i].fae

    @gl.public.view
    def get_current_release_id(self,_h:str)->str:
        _i=Address(_h)
        if _i not in self.policies:
            return ''
        return self.policies[_i].fac

    @gl.public.view
    def get_active_proposal(self,_h:str)->u256:
        _i=Address(_h)
        return self.active_proposal_by_target.get(_i,self._gn())

    @gl.public.view
    def get_proposal_summary(self,_d:u256)->str:
        if _d not in self.proposals:
            return json.dumps({'status':'UNKNOWN'},separators=(',',':'))
        _a=self.proposals[_d]
        return json.dumps({_s11:int(_a.fbc),'target':str(_a.fbw),_s41:_a.fax,_s13:_a.fau,_s15:_a.fq,_s5:_a.fo,_s1:_a.fay,_s12:_a.faf,_s3:_a.fg,_s43:_a.fbm,_s32:_a.fbn,_s2:_a.fbh,_s10:self._gg(_a),'status':_a.fbv,_s38:_a.fan,'created_at':int(_a.faa),_s50:int(_a.fai),_s48:int(_a.fbr),'execution_deadline':int(_a.fag)},separators=(',',':'))

    @gl.public.view
    def get_release_summary(self,_e:str)->str:
        if _e not in self.releases:
            return json.dumps({'status':'UNKNOWN'},separators=(',',':'))
        _f=self.releases[_e]
        return json.dumps({_s10:_f.fbq,'target':str(_f.fbw),'version':_f.fbx,'parent_release_id':_f.fav,_s13:_f.fau,'code_hash':_f.fw,_s11:int(_f.fbc),_s1:_f.fay,_s12:_f.faf,_s3:_f.fg,_s2:_f.fbh,'installed_at':int(_f.fal),'certified_at':int(_f.fr),'status':_f.fbv,'recovered_from_release_id':_f.fbf,'recovery_incident_id':_f.fbl,'lineage_hash':_f.fao},separators=(',',':'))

    @gl.public.view
    def get_incident_summary(self,_g:str)->str:
        if _g not in self.incidents:
            return json.dumps({'status':'UNKNOWN'},separators=(',',':'))
        _b=self.incidents[_g]
        return json.dumps({_s27:_b.faj,'target':str(_b.fbw),_s10:_b.fbq,_s14:_b.fam,_s42:_b.fak,_s1:_b.fay,_s2:_b.fbh,'opened_at':int(_b.fas),_s50:int(_b.fai),_s48:int(_b.fbr),'recovery_deadline':int(_b.fbk),'status':_b.fbv,_s38:_b.fan,'recovery_authorized':_b.fbg},separators=(',',':'))
