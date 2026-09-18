# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_J='timeout';_I='reconcile_install';_H='confirm_install';_G='confirm_activation';_F='retry_recovery';_E='expire_recovery';_D='reconcile_recovery';_C='confirm_recovery';_B='expire_provisional';_A=None;from genlayer import*;from genlayer.py.public_abi import StorageType;import hashlib,json;ZERO='0x0000000000000000000000000000000000000000';INSTALL_LIFECYCLE_ENGINE='0xE7F337c2Bc992a94f213C41B66d7E49381F31145';TIMEOUT_LIFECYCLE_ENGINE='0xd73FF76b1A2438eAD59DA4072F9484aED25C7865';ACTIVATION_LIFECYCLE_ENGINE='0x429A733D5949bCB0DE97E32Da58E8d192acC41Ca';RECOVERY_LIFECYCLE_ENGINE='0xebf47F06759481606910dA564FF48203e386b95E'
@gl.contract_interface
class ProofPatchGovernor:
	class View:
		def get_state_record(self,kind:str,key:str)->str:...
@gl.contract_interface
class ProofPatchTarget:
	class View:
		def proofpatch_installed_proposal_id(self)->u256:...
		def proofpatch_installed_candidate_hash(self)->str:...
		def proofpatch_installed_release_id(self)->str:...
		def proofpatch_release_mode(self)->str:...
		def get_proofpatch_kernel_hash(self)->str:...
@gl.contract_interface
class ProofPatchLifecycleEngine:
	class Write:
		def execute(self,operation:str,request:str)->_A:...
class ProofPatchLifecycleRequestEngine(gl.Contract):
	admin:Address;governor:Address
	def __init__(self):self.admin=gl.message.sender_address;self.governor=Address(ZERO)
	@gl.public.write
	def bind_governor(self,governor:str)->_A:
		if gl.message.sender_address!=self.admin:raise gl.vm.UserError('Only admin may bind governor')
		if self.governor!=Address(ZERO):raise gl.vm.UserError('Governor is already bound')
		candidate=Address(governor)
		if candidate==Address(ZERO):raise gl.vm.UserError('Governor cannot be the zero address')
		self.governor=candidate
	def _read(self,view,kind,key):return json.loads(view.get_state_record(kind,key))
	def _maybe(self,view,kind,key):
		try:return self._read(view,kind,key)
		except Exception:return
	def _prepare(self,operation,data):
		N='candidate_hash';M='value';L='release_count';K='proposal_count';J='now';I='actor';H='release_id';G='args';F='policy';E='target';D='proposal_id';C='incident';B='proposal';A='release';view=ProofPatchGovernor(self.governor).view(state=StorageType.LATEST_FINAL);args=data[G];records={}
		if operation==_B:
			records[A]=self._read(view,A,args[0]);target=records[A][E];records[B]=self._read(view,B,str(records[A][D]));existing_incident=self._maybe(view,C,'timeout-'+args[0])
			if existing_incident is not _A:records[C]=existing_incident
		elif operation in(_C,_D,_E,_F):records[C]=self._read(view,C,args[0]);records[A]=self._read(view,A,records[C][H]);records[B]=self._read(view,B,str(records[A][D]));target=records[C][E]
		else:
			records[B]=self._read(view,B,str(int(args[0])));target=records[B][E]
			if operation==_G:records[A]=self._read(view,A,args[1])
		records[F]=self._read(view,F,target);proposal=records.get(B)
		if proposal is not _A and operation in(_H,_I,_J):records['parent_release']=self._read(view,A,records[F]['current_release_id'])
		if proposal is not _A and proposal['recovery_mode']=='RECOVERY_CANDIDATE':
			recovery_release=self._maybe(view,A,proposal['recovery_release_id'])
			if recovery_release is not _A:records['recovery_release']=recovery_release
		prepared={G:args,I:data[I],J:data[J],'records':records};counts=self._read(view,'counts','');prepared[K]=counts[K];prepared[L]=counts[L];active=self._read(view,'active',target);prepared['active_target']=target;prepared['active_value']=active[M]
		if proposal is not _A:key=hashlib.sha256('\x1f'.join([target,proposal['candidate_code_hash']]).encode()).hexdigest();used=self._maybe(view,'candidate',key);prepared['installed_candidate_hashes']={key:True}if used is not _A and used.get(M,False)else{}
		target_view=ProofPatchTarget(Address(target)).view(state=StorageType.LATEST_FINAL);prepared['target_final']={D:int(target_view.proofpatch_installed_proposal_id()),N:target_view.proofpatch_installed_candidate_hash(),H:target_view.proofpatch_installed_release_id(),'mode':target_view.proofpatch_release_mode(),'kernel_hash':target_view.get_proofpatch_kernel_hash()};nonfinal_view=ProofPatchTarget(Address(target)).view(state=StorageType.LATEST_NON_FINAL);prepared['target_nonfinal']={D:int(nonfinal_view.proofpatch_installed_proposal_id()),N:nonfinal_view.proofpatch_installed_candidate_hash()};return prepared
	@gl.public.write
	def execute(self,operation:str,request:str)->_A:
		if gl.message.sender_address!=self.governor:raise gl.vm.UserError('Only the bound governor may prepare lifecycle execution')
		prepared=self._prepare(operation,json.loads(request))
		if operation in('cancel','expire',_H,_I):engine=INSTALL_LIFECYCLE_ENGINE
		elif operation==_J:engine=TIMEOUT_LIFECYCLE_ENGINE
		elif operation==_G:engine=ACTIVATION_LIFECYCLE_ENGINE
		elif operation in(_B,_C,_D,_E,_F):engine=RECOVERY_LIFECYCLE_ENGINE
		else:raise gl.vm.UserError('Unknown lifecycle operation')
		ProofPatchLifecycleEngine(Address(engine)).emit(on='finalized').execute(operation,json.dumps(prepared,sort_keys=True,separators=(',',':')))
