# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer.py.public_abi import StorageType
_C='policy';_B='status';_A='target';_s0='ProofPatch invariant';_s1='policy_fingerprint';_s2='max_evidence_age_seconds';_s3='recovery_capsule_hash';_s4='candidate_code_hash';_s5='assurance_manifest_hash';_s6='proposal_id';_s7='corroboration_evidence_id';_s8='audit_authority';_s9='primary_evidence_id';_s10='corroboration_url';_s11='assurance_corroboration_authority';_s12='parent_code_hash';_s13='release_id';_s14='assurance_deadline_seconds';_s15='proposal';_s16='corroboration_authority';_s17='proofpatch_kernel_hash';_s18='primary_url';_s19='candidate_source_url';_s20='review_now';_s21='assurance_authority';_s22='installed_code_hash';_s23='recovery_release_id';_s24='recovery_source_url';_s25='assurance_manifest';_s26='audit_evidence_url';_s27='max_manifest_bytes';_s28='recovery_code_hash';_s29='audit_evidence_id';_s30='candidate_version';_s31='evidence_set_hash';_s32='parent_source_url';_s33='last_review_code';_s34='recovery_version';_s35='ci_evidence_url';_s36='ENGINE_PENDING';_s37='REVIEW_PENDING';_s38='ci_evidence_id';_s39='parent_version';_s40='incident_type';_s41='recovery_mode';_s42='ci_authority';_s43='constitution';_s44='incident_id';_s45='kernel_hash';_s46='reviewed_at';_s47='expires_at';_s48='incident';from genlayer import*;_af='EVIDENCE_';_ah='MANIFEST_';_ad='ASSURANCE_';_ag='INCIDENT_';_ai='RECOVERY_';_ae='CANDIDATE_';_ac='CI_';_ab='AUDIT_';import json;_n='0x0000000000000000000000000000000000000000';_u='PROPOSED';_v='REVIEW_RETRY_REQUIRED';_l=_s37;_t=_ag+'OPEN';_s=_ag+'RETRY_REQUIRED';_k=_ag+_s37
@gl.contract_interface
class _am:
	class _as:
		def get_state_record(self,_o:str,_p:str)->str:...
	class _aq:
		def apply_review_request(self,_h:str,_m:str)->None:...
@gl.contract_interface
class _ao:
	class _as:
		def proofpatch_installed_proposal_id(self)->u256:...
		def proofpatch_installed_candidate_hash(self)->str:...
		def proofpatch_installed_release_id(self)->str:...
		def proofpatch_release_mode(self)->str:...
		def get_proofpatch_kernel_hash(self)->str:...
		def get_proofpatch_governor(self)->Address:...
class _ak(gl.Contract):
	admin:Address;governor:Address
	def __init__(self):self.admin=gl.message.sender_address;self.governor=Address(_n)
	@gl.public.write
	def bind_governor(self,governor:str)->None:
		if gl.message.sender_address!=self.admin:raise gl.vm.UserError(_s0)
		if self.governor!=Address(_n):raise gl.vm.UserError(_s0)
		self.governor=Address(governor)
	def _aj(self,_w,_o,_p):return json.loads(_w.get_state_record(_o,_p))
	def _aa(self,_e,_d,_f):
		_a=self._aj(_e,_s15,str(int(_d[0])));_b=self._aj(_e,_C,_a[_A])
		if _a[_B]not in(_u,_v,_l):raise gl.vm.UserError(_s0)
		if _f>int(_a[_s47]):raise gl.vm.UserError(_s0)
		if not _b['active']or _b[_s1]!=_a[_s1]or _b['current_code_hash']!=_a[_s12]:raise gl.vm.UserError(_s0)
		_a[_B]=_l;_a[_s46]=_f;_a[_s33]=_s36;_g={_s6:_a[_s6],_A:_a[_A],_s39:_a[_s39],_s32:_a[_s32],_s12:_a[_s12],_s30:_a[_s30],_s19:_a[_s19],_s4:_a[_s4],'candidate_code_hex':_a['candidate_code'],_s35:_a[_s35],_s38:_a[_s38],_s26:_a[_s26],_s29:_a[_s29],_s25:_a[_s25],_s5:_a[_s5],_s41:_a[_s41],_s23:_a[_s23],_s34:_a[_s34],_s24:_a[_s24],_s28:_a[_s28],_s3:_a[_s3],'recovery_code_hex':_a['recovery_code'],_s31:_a[_s31],_s1:_a[_s1],_s43:_b[_s43],_s45:_b[_s17],_s42:_b[_s42],_s8:_b[_s8],_s2:_b[_s2],_s27:_b[_s27],'observation_delay_seconds':_b['assurance_observation_delay_seconds'],_s14:_b[_s14],_s20:_f,'manifest_error':''};return _g,{'proposals':[_a]}
	def _y(self,_e,_d,_f):_a=self._aj(_e,_s15,str(int(_d[0])));_b=self._aj(_e,_C,_a[_A]);_x='release-'+str(_a[_s6])+'-'+_a[_s4][:16];_i=_ao(Address(_a[_A])).view(state=StorageType.LATEST_FINAL);return{_A:_a[_A],_s6:_a[_s6],_s13:_x,_s4:_a[_s4],_s1:_a[_s1],_s5:_a[_s5],_s25:_a[_s25],_s23:_a[_s23],_s18:_d[1],_s9:_d[2],_s10:_d[3],_s7:_d[4],_s21:_b[_s21],_s16:_b[_s11],_s2:_b[_s2],_s20:_f,'installed_proposal_id':int(_i.proofpatch_installed_proposal_id()),'installed_candidate_hash':_i.proofpatch_installed_candidate_hash(),'installed_release_id':_i.proofpatch_installed_release_id(),'installed_mode':_i.proofpatch_release_mode(),'installed_kernel_hash':_i.get_proofpatch_kernel_hash(),'target_governor':str(_i.get_proofpatch_governor()),'expected_governor':str(self.governor),_s45:_b[_s17]}
	def _z(self,_e,_d,_f):
		_c=self._aj(_e,_s48,_d[0]);_r=self._aj(_e,'release',_c[_s13]);_a=self._aj(_e,_s15,str(_r[_s6]));_b=self._aj(_e,_C,_c[_A])
		if _c[_B]not in(_t,'INCIDENT_REPAIR_REQUIRED',_s,_k):raise gl.vm.UserError(_s0)
		if _f>int(_c[_s47]):raise gl.vm.UserError(_s0)
		_c[_B]=_k;_c[_s46]=_f;_c[_s33]=_s36;_g={_s44:_c[_s44],_A:_c[_A],_s13:_c[_s13],_s22:_c[_s22],_s40:_c[_s40],_s18:_c[_s18],_s9:_c[_s9],_s10:_c[_s10],_s7:_c[_s7],_s1:_c[_s1],_s3:_c[_s3],_s8:_b[_s8],_s16:_b[_s11],_s2:_b[_s2],_s20:_f,'release_code_hash':_r['code_hash'],'proposal_recovery_capsule_hash':_a[_s3],'proposal_recovery_release_id':_a[_s23]};return _g,{'incidents':[_c]}
	@gl.public.write
	def execute(self,_h:str,_m:str)->None:
		A='args'
		if gl.message.sender_address!=self.governor:raise gl.vm.UserError(_s0)
		_q=json.loads(_m);_d=_q[A];_f=int(_q.get('now',0));_e=_am(self.governor).view(state=StorageType.LATEST_FINAL);_j={}
		if _h==_s15:_g,_j=self._aa(_e,_d,_f)
		elif _h=='assurance':_g=self._y(_e,_d,_f)
		elif _h==_s48:_g,_j=self._z(_e,_d,_f)
		else:raise gl.vm.UserError(_s0)
		_am(self.governor).emit(on='finalized').apply_review_request(_h,json.dumps({A:_d,'snapshot':json.dumps(_g,sort_keys=True,separators=(',',':')),'patch':_j},separators=(',',':')))
