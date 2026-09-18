# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import*;from genlayer.py.public_abi import StorageType;from datetime import datetime;import json,typing;ZERO='0x0000000000000000000000000000000000000000'
@gl.contract_interface
class ProofPatchGovernor:
	class View:
		def get_state_record(self,kind:str,key:str)->str:...
class ProofPatchSummaryEngine(gl.Contract):
	admin:Address;governor:Address
	def __init__(self):self.admin=gl.message.sender_address;self.governor=Address(ZERO)
	@gl.public.write
	def bind_governor(self,governor:str)->None:
		if gl.message.sender_address!=self.admin:raise gl.vm.UserError('Only admin may bind governor')
		if self.governor!=Address(ZERO):raise gl.vm.UserError('Governor is already bound')
		candidate=Address(governor)
		if candidate==Address(ZERO):raise gl.vm.UserError('Governor cannot be the zero address')
		self.governor=candidate
	def _get(self,kind:str,key:str)->typing.Any:
		try:return json.loads(ProofPatchGovernor(self.governor).view(state=StorageType.LATEST_FINAL).get_state_record(kind,key))
		except Exception:return
	def _now(self)->int:return int(datetime.fromisoformat(str(gl.message_raw['datetime']).replace('Z','+00:00')).timestamp())
	def _missing(self,value:typing.Any)->bool:return value is None or value.get('status')=='UNKNOWN'
	def _json(self,value:typing.Any,fields:tuple[str,...])->str:return json.dumps({field:value[field]for field in fields},separators=(',',':'))
	@gl.public.view
	def get_proposal_summary(self,proposal_id:u256)->str:
		value=self._get('proposal',str(int(proposal_id)))
		if value is None or value.get('status')=='UNKNOWN':return json.dumps({'status':'UNKNOWN'},separators=(',',':'))
		value['release_id']='release-'+str(value['proposal_id'])+'-'+value['candidate_code_hash'][:16];return self._json(value,('proposal_id','target','parent_version','parent_code_hash','candidate_version','candidate_code_hash','policy_fingerprint','evidence_set_hash','assurance_manifest_hash','recovery_mode','recovery_release_id','recovery_capsule_hash','release_id','status','last_review_code','created_at','expires_at','reviewed_at','execution_deadline'))
	@gl.public.view
	def get_release_summary(self,release_id:str)->str:
		value=self._get('release',release_id)
		if value is None or value.get('status')=='UNKNOWN':return json.dumps({'status':'UNKNOWN'},separators=(',',':'))
		return self._json(value,('release_id','target','version','parent_release_id','parent_code_hash','code_hash','proposal_id','policy_fingerprint','evidence_set_hash','assurance_manifest_hash','recovery_capsule_hash','installed_at','certified_at','status','recovered_from_release_id','recovery_incident_id','lineage_hash'))
	@gl.public.view
	def get_incident_summary(self,incident_id:str)->str:
		value=self._get('incident',incident_id)
		if value is None or value.get('status')=='UNKNOWN':return json.dumps({'status':'UNKNOWN'},separators=(',',':'))
		return self._json(value,('incident_id','target','release_id','installed_code_hash','incident_type','policy_fingerprint','recovery_capsule_hash','opened_at','expires_at','reviewed_at','recovery_deadline','status','last_review_code','recovery_authorized'))
	@gl.public.view
	def get_candidate_code(self,proposal_id:u256)->bytes:
		value=self._get('proposal',str(int(proposal_id)))
		if value is None:raise gl.vm.UserError('Unknown proposal')
		if value['status']!='UPGRADE_QUEUED':raise gl.vm.UserError('Candidate is not authorized for installation')
		if self._now()>int(value['execution_deadline']):raise gl.vm.UserError('Upgrade authorization expired')
		return bytes.fromhex(value['candidate_code'])
	@gl.public.view
	def get_recovery_release_id(self,incident_id:str)->str:
		value=self._get('incident',incident_id)
		if value is None:return''
		release=self._get('release',value['release_id'])
		if release is None:return''
		proposal=self._get('proposal',str(release['proposal_id']));return''if proposal is None else proposal['recovery_release_id']
	@gl.public.view
	def get_recovery_code(self,incident_id:str)->bytes:
		incident=self._get('incident',incident_id)
		if incident is None:raise gl.vm.UserError('Unknown incident')
		if incident['status']not in('INCIDENT_CONFIRMED','RECOVERY_QUEUED','RECOVERY_RETRY_REQUIRED'):raise gl.vm.UserError('Recovery is not authorized')
		release=self._get('release',incident['release_id']);proposal=self._get('proposal',str(release['proposal_id']));return bytes.fromhex(proposal['recovery_code'])
	@gl.public.view
	def is_upgrade_authorized(self,proposal_id:u256,target:str,candidate_hash:str)->bool:
		p=self._get('proposal',str(int(proposal_id)))
		if self._missing(p)or p['status']!='UPGRADE_QUEUED'or p['target'].lower()!=str(Address(target)).lower()or p['candidate_code_hash']!=candidate_hash.lower()or self._now()>int(p['execution_deadline']):return False
		return int(self._get('active',p['target'])['value'])==int(proposal_id)
	@gl.public.view
	def is_activation_authorized(self,proposal_id:u256,release_id:str,candidate_hash:str)->bool:p=self._get('proposal',str(int(proposal_id)));r=self._get('release',release_id);return not self._missing(p)and not self._missing(r)and p['status']=='CERTIFICATION_QUEUED'and release_id=='release-'+str(p['proposal_id'])+'-'+p['candidate_code_hash'][:16]and candidate_hash.lower()==p['candidate_code_hash']and r['status']=='CERTIFICATION_QUEUED'
	@gl.public.view
	def is_registration_authorized(self,target:str,release_id:str,code_hash:str)->bool:p=self._get('policy',target);r=self._get('release',release_id);return not self._missing(p)and not self._missing(r)and p['current_release_id']==release_id and p['current_code_hash']==code_hash.lower()and r['status']=='REGISTERED_PARENT'
	@gl.public.view
	def is_recovery_authorized(self,incident_id:str,release_id:str,recovery_hash:str)->bool:i=self._get('incident',incident_id);r=self._get('release',release_id);return not self._missing(i)and not self._missing(r)and i['status']in('INCIDENT_CONFIRMED','RECOVERY_QUEUED','RECOVERY_RETRY_REQUIRED')and i['recovery_authorized']and i['release_id']==release_id and i['recovery_capsule_hash']==recovery_hash.lower()
	@gl.public.view
	def get_proposal_count(self)->u256:value=self._get('counts','');return u256(0 if self._missing(value)else value['proposal_count'])
	@gl.public.view
	def get_proposal_status(self,proposal_id:u256)->str:value=self._get('proposal',str(int(proposal_id)));return'UNKNOWN'if self._missing(value)else value['status']
	@gl.public.view
	def get_candidate_hash(self,proposal_id:u256)->str:value=self._get('proposal',str(int(proposal_id)));return''if self._missing(value)else value['candidate_code_hash']
	@gl.public.view
	def get_proposal_release_id(self,proposal_id:u256)->str:value=self._get('proposal',str(int(proposal_id)));return''if self._missing(value)else'release-'+str(value['proposal_id'])+'-'+value['candidate_code_hash'][:16]
	@gl.public.view
	def get_evidence_set_hash(self,proposal_id:u256)->str:value=self._get('proposal',str(int(proposal_id)));return''if self._missing(value)else value['evidence_set_hash']
	@gl.public.view
	def get_policy_fingerprint(self,target:str)->str:value=self._get('policy',target);return''if self._missing(value)else value['policy_fingerprint']
	@gl.public.view
	def get_policy_kernel_hash(self,target:str)->str:value=self._get('policy',target);return''if self._missing(value)else value['proofpatch_kernel_hash']
	@gl.public.view
	def get_current_code_hash(self,target:str)->str:value=self._get('policy',target);return''if self._missing(value)else value['current_code_hash']
	@gl.public.view
	def get_current_version(self,target:str)->str:value=self._get('policy',target);return''if self._missing(value)else value['current_version']
	@gl.public.view
	def get_current_release_id(self,target:str)->str:value=self._get('policy',target);return''if self._missing(value)else value['current_release_id']
	@gl.public.view
	def get_active_proposal(self,target:str)->u256:value=self._get('active',target);return u256(0 if self._missing(value)else value['value'])
	@gl.public.view
	def read(self,kind:str,key:str)->str:
		if kind.endswith('_summary'):return getattr(self,'get_'+kind)(key if kind!='proposal_summary'else u256(int(key)))
		if kind in('candidate_code','recovery_code'):return(self.get_candidate_code(u256(int(key)))if kind=='candidate_code'else self.get_recovery_code(key)).hex()
		if kind=='recovery_release_id':return self.get_recovery_release_id(key)
		if kind.startswith('is_'):args=json.loads(key);result=getattr(self,kind)(*args);return'1'if result else'0'
		if kind=='proposal_count':return str(int(self.get_proposal_count()))
		if kind=='active_proposal':return str(int(self.get_active_proposal(key)))
		return str(getattr(self,'get_'+kind)(u256(int(key)))if kind in('proposal_status','candidate_hash','proposal_release_id','evidence_set_hash')else getattr(self,'get_'+kind)(key))
