# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import*;from genlayer.py.public_abi import StorageType;import hashlib,json,typing;ZERO='0x0000000000000000000000000000000000000000';MAX_URL_BYTES=1024;MAX_ID_BYTES=160;STATUS_INSTALLED_PROVISIONAL='INSTALLED_PROVISIONAL';STATUS_ASSURANCE_PENDING='ASSURANCE_PENDING';STATUS_ASSURANCE_REPAIR='ASSURANCE_REPAIR_REQUIRED';STATUS_ASSURANCE_RETRY='ASSURANCE_RETRY_REQUIRED'
@gl.contract_interface
class ProofPatchGovernorV2:
	class View:
		def get_state_record(self,kind:str,key:str)->str:...
	class Write:
		def apply_policy_result(self,operation:str,payload:str)->None:...
class ProofPatchAssuranceLogic:
	def _hash_text_parts(self,parts:list[str])->str:return hashlib.sha256('\x1f'.join(parts).encode('utf-8')).hexdigest()
	def _check_text(self,value:str,label:str,minimum:int,maximum:int)->None:
		size=len(value.encode('utf-8'))
		if size<minimum or size>maximum:raise gl.vm.UserError(f"{label} length is invalid")
	def _is_canonical_raw_segment(self,value:str)->bool:
		if not value or value in('.','..'):return False
		allowed='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-';return all(char in allowed for char in value)
	def _raw_github_owner(self,prefix:str)->str:
		base='https://raw.githubusercontent.com/'
		if not prefix.startswith(base)or not prefix.endswith('/'):return''
		parts=prefix[len(base):].split('/')
		if len(parts)!=3 or parts[2]!='':return''
		if not self._is_canonical_raw_segment(parts[0])or not self._is_canonical_raw_segment(parts[1]):return''
		return parts[0]
	def _is_immutable_url(self,url:str,prefix:str)->bool:
		if len(url.encode('utf-8'))>MAX_URL_BYTES or self._raw_github_owner(prefix)=='':return False
		if not url.startswith(prefix):return False
		parts=url[len(prefix):].split('/',1)
		if len(parts)!=2 or len(parts[0])!=40 or any(char not in'0123456789abcdef'for char in parts[0]):return False
		return all(self._is_canonical_raw_segment(segment)for segment in parts[1].split('/'))
	def _reserve(self,view:typing.Any,patch:dict[str,typing.Any],target:str,issuer:str,kind:str,evidence_id:str)->None:
		self._check_text(evidence_id,'evidence_id',8,MAX_ID_BYTES);key=self._hash_text_parts([target,issuer,kind,evidence_id])
		if json.loads(view.get_state_record('evidence',key)).get('value',False)or patch['used_evidence_ids'].get(key,False):raise gl.vm.UserError('Evidence identifier has already been used')
		patch['used_evidence_ids'][key]=True
	def _assure(self,view:typing.Any,args:list[typing.Any],now:int)->dict[object,object]:
		proposal_id=int(args[0]);proposal=json.loads(view.get_state_record('proposal',str(proposal_id)));policy=json.loads(view.get_state_record('policy',proposal['target']));release_id='release-'+str(proposal['proposal_id'])+'-'+proposal['candidate_code_hash'][:16];release=json.loads(view.get_state_record('release',release_id))
		if proposal['status']not in(STATUS_INSTALLED_PROVISIONAL,STATUS_ASSURANCE_REPAIR,STATUS_ASSURANCE_RETRY,STATUS_ASSURANCE_PENDING):raise gl.vm.UserError('Release is not awaiting assurance')
		if now<int(release['installed_at'])+int(policy['assurance_observation_delay_seconds']):raise gl.vm.UserError('Assurance observation period has not elapsed')
		if now>int(release['installed_at'])+int(policy['assurance_deadline_seconds']):raise gl.vm.UserError('Assurance deadline has passed')
		if not self._is_immutable_url(args[1],policy['assurance_prefix'])or not self._is_immutable_url(args[3],policy['assurance_corroboration_prefix']):raise gl.vm.UserError('Assurance evidence URL is not approved and immutable')
		if args[2]==args[4]:raise gl.vm.UserError('Assurance evidence identifiers must be distinct')
		patch={'operation':'assure','proposals':[proposal],'releases':[],'used_evidence_ids':{}};self._reserve(view,patch,proposal['target'],policy['assurance_authority'],'assurance_primary',args[2]);self._reserve(view,patch,proposal['target'],policy['assurance_corroboration_authority'],'assurance_corroboration',args[4]);proposal['status']=STATUS_ASSURANCE_PENDING;proposal['reviewed_at']=now;proposal['last_review_code']='ENGINE_PENDING';patch['proposals']=[proposal];patch['review']={'proposal_id':proposal_id,'primary_url':args[1],'primary_evidence_id':args[2],'corroboration_url':args[3],'corroboration_evidence_id':args[4]};return patch
class ProofPatchAssuranceEngine(gl.Contract):
	admin:Address;governor:Address
	def __init__(self):self.admin=gl.message.sender_address;self.governor=Address(ZERO)
	@gl.public.write
	def bind_governor(self,governor:str)->None:
		if gl.message.sender_address!=self.admin:raise gl.vm.UserError('Only admin may bind governor')
		if self.governor!=Address(ZERO):raise gl.vm.UserError('Governor is already bound')
		candidate=Address(governor)
		if candidate==Address(ZERO):raise gl.vm.UserError('Governor cannot be the zero address')
		self.governor=candidate
	@gl.public.write
	def execute(self,operation:str,request:str)->None:
		if gl.message.sender_address!=self.governor:raise gl.vm.UserError('Only the bound governor may execute assurance logic')
		if operation!='assure':raise gl.vm.UserError('Unknown assurance operation')
		data=json.loads(request);view=ProofPatchGovernorV2(self.governor).view(state=StorageType.LATEST_FINAL);patch=ProofPatchAssuranceLogic()._assure(view,data['args'],int(data['now']));ProofPatchGovernorV2(self.governor).emit(on='finalized').apply_policy_result(operation,json.dumps(patch,separators=(',',':')))
