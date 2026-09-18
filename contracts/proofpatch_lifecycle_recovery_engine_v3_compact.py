# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_H='installed_candidate_hashes';_G='release_count';_F='proposal_count';_E='recover';_D='RECOVERED';_C='args';_B='Unknown incident';_A=None;from genlayer import*;from dataclasses import dataclass;import hashlib,json;SCHEMA_VERSION='proofpatch-v2';MODE_RECOVERED=_D;STATUS_INSTALLED_PROVISIONAL='INSTALLED_PROVISIONAL';STATUS_ASSURANCE_PENDING='ASSURANCE_PENDING';STATUS_ASSURANCE_REPAIR='ASSURANCE_REPAIR_REQUIRED';STATUS_ASSURANCE_RETRY='ASSURANCE_RETRY_REQUIRED';STATUS_INCIDENT_CONFIRMED='INCIDENT_CONFIRMED';STATUS_RECOVERY_QUEUED='RECOVERY_QUEUED';STATUS_RECOVERY_RETRY='RECOVERY_RETRY_REQUIRED';STATUS_RECOVERED=_D;ZERO='0x0000000000000000000000000000000000000000'
class TargetPolicy:owner:Address;target:Address;constitution:str;policy_fingerprint:str;source_authority:str;ci_authority:str;audit_authority:str;source_prefix:str;ci_prefix:str;audit_prefix:str;assurance_authority:str;assurance_prefix:str;assurance_corroboration_authority:str;assurance_corroboration_prefix:str;proofpatch_kernel_hash:str;current_version:str;current_source_url:str;current_code_hash:str;current_release_id:str;max_evidence_age_seconds:u64;proposal_ttl_seconds:u64;execution_timeout_seconds:u64;assurance_observation_delay_seconds:u64;assurance_deadline_seconds:u64;max_manifest_bytes:u64;max_capsule_bytes:u64;active:bool
class UpgradeProposal:proposal_id:u256;target:Address;proposer:Address;parent_version:str;parent_source_url:str;parent_code_hash:str;candidate_version:str;candidate_source_url:str;candidate_code:bytes;candidate_code_hash:str;ci_evidence_url:str;ci_evidence_id:str;audit_evidence_url:str;audit_evidence_id:str;assurance_manifest:str;assurance_manifest_hash:str;recovery_mode:str;recovery_release_id:str;recovery_version:str;recovery_source_url:str;recovery_code:bytes;recovery_code_hash:str;recovery_capsule_hash:str;evidence_set_hash:str;policy_fingerprint:str;created_at:u64;expires_at:u64;reviewed_at:u64;execution_deadline:u64;status:str;last_review_code:str
class ReleaseRecord:release_id:str;target:Address;version:str;parent_release_id:str;parent_code_hash:str;source_url:str;code_hash:str;proposal_id:u256;policy_fingerprint:str;evidence_set_hash:str;assurance_manifest_hash:str;recovery_capsule_hash:str;installed_at:u64;certified_at:u64;status:str;recovered_from_release_id:str;recovery_incident_id:str;lineage_hash:str
class IncidentRecord:incident_id:str;target:Address;release_id:str;installed_code_hash:str;incident_type:str;primary_url:str;primary_evidence_id:str;corroboration_url:str;corroboration_evidence_id:str;policy_fingerprint:str;assurance_manifest_hash:str;recovery_capsule_hash:str;opened_at:u64;expires_at:u64;reviewed_at:u64;recovery_deadline:u64;status:str;last_review_code:str;recovery_authorized:bool
@gl.contract_interface
class ProofPatchGovernorV2:
	class Write:
		def apply_lifecycle_result(self,operation:str,payload:str)->_A:...
class ProofPatchRecoveryLifecycleLogic:
	def __init__(self):self.policies={};self.proposals={};self.releases={};self.incidents={};self.active_proposal_by_target={};self.installed_candidate_hashes={};self.proposal_count=u256(0);self.release_count=u256(0);self.actions=[]
	def _now(self)->int:return self.now
	def _hash_text_parts(self,parts:list[str])->str:return hashlib.sha256('\x1f'.join(parts).encode('utf-8')).hexdigest()
	def _release_active(self,target:Address,proposal_id:u256)->_A:
		if self.active_proposal_by_target.get(target,self._inactive_proposal())==proposal_id:self.active_proposal_by_target[target]=self._inactive_proposal()
	def _recovery_release_id(self,proposal:UpgradeProposal)->str:return proposal.recovery_release_id
	def _lineage_hash(self,target:Address,previous_lineage_hash:str,release_id:str,parent_release_id:str,version:str,code_hash:str,policy_fingerprint:str,evidence_set_hash:str,assurance_manifest_hash:str,recovery_capsule_hash:str)->str:return self._hash_text_parts([SCHEMA_VERSION,str(target),previous_lineage_hash,release_id,parent_release_id,version,code_hash,policy_fingerprint,evidence_set_hash,assurance_manifest_hash,recovery_capsule_hash])
	def _complete_recovery(self,incident_id:str,release_id:str,recovery_hash:str)->_A:
		if incident_id not in self.incidents:raise gl.vm.UserError(_B)
		incident=self.incidents[incident_id]
		if incident.status==STATUS_RECOVERED:return
		if incident.status not in(STATUS_INCIDENT_CONFIRMED,STATUS_RECOVERY_QUEUED,STATUS_RECOVERY_RETRY)or release_id!=incident.release_id:raise gl.vm.UserError('Incident is not awaiting recovery confirmation')
		if recovery_hash.lower()!=incident.recovery_capsule_hash:raise gl.vm.UserError('Recovery hash does not match precommitted capsule')
		proposal=self.proposals[self.releases[release_id].proposal_id];expected=self._recovery_release_id(proposal)
		if self.target_final_release_id!=expected:raise gl.vm.UserError('Finalized target recovery release does not match')
		if self.target_final_candidate_hash!=recovery_hash.lower():raise gl.vm.UserError('Finalized target recovery hash does not match')
		if self.target_final_mode!=MODE_RECOVERED:raise gl.vm.UserError('Target has not finalized RECOVERED mode')
		incident.status=STATUS_RECOVERED;incident.last_review_code='RECOVERY_VERIFIED';self.releases[release_id].status=STATUS_RECOVERED;self.releases[release_id].recovery_incident_id=incident_id;policy=self.policies[incident.target]
		if proposal.recovery_mode=='RECOVERY_CANDIDATE':
			if expected in self.releases:
				if self.releases[expected].code_hash!=recovery_hash.lower():raise gl.vm.UserError('Conflicting recovery release identity')
			else:affected=self.releases[release_id];lineage=self._lineage_hash(incident.target,affected.lineage_hash,expected,release_id,proposal.recovery_version,recovery_hash.lower(),proposal.policy_fingerprint,proposal.evidence_set_hash,proposal.assurance_manifest_hash,proposal.recovery_capsule_hash);self.releases[expected]=ReleaseRecord(release_id=expected,target=incident.target,version=proposal.recovery_version,parent_release_id=release_id,parent_code_hash=incident.installed_code_hash,source_url=proposal.recovery_source_url,code_hash=recovery_hash.lower(),proposal_id=proposal.proposal_id,policy_fingerprint=proposal.policy_fingerprint,evidence_set_hash=proposal.evidence_set_hash,assurance_manifest_hash=proposal.assurance_manifest_hash,recovery_capsule_hash=proposal.recovery_capsule_hash,installed_at=u64(self._now()),certified_at=u64(self._now()),status=STATUS_RECOVERED,recovered_from_release_id=release_id,recovery_incident_id=incident_id,lineage_hash=lineage);self.release_count=u256(int(self.release_count)+1)
		elif expected not in self.releases:raise gl.vm.UserError('Exact-parent recovery release is missing')
		policy.current_version=proposal.recovery_version;policy.current_source_url=proposal.recovery_source_url;policy.current_code_hash=recovery_hash.lower();policy.current_release_id=expected;self._release_active(incident.target,proposal.proposal_id)
	def expire_provisional(self,release_id:str)->_A:
		if release_id not in self.releases:raise gl.vm.UserError('Unknown release')
		release=self.releases[release_id]
		if release.status not in(STATUS_INSTALLED_PROVISIONAL,STATUS_ASSURANCE_PENDING,STATUS_ASSURANCE_REPAIR,STATUS_ASSURANCE_RETRY):raise gl.vm.UserError('Release is not provisionally installed')
		policy=self.policies[release.target]
		if self._now()<=int(release.installed_at)+int(policy.assurance_deadline_seconds):raise gl.vm.UserError('Assurance deadline has not passed')
		incident_id='timeout-'+release_id
		if incident_id not in self.incidents:proposal=self.proposals[release.proposal_id];now=self._now();self.incidents[incident_id]=IncidentRecord(incident_id=incident_id,target=release.target,release_id=release_id,installed_code_hash=release.code_hash,incident_type='ASSURANCE_TIMEOUT',primary_url='',primary_evidence_id='',corroboration_url='',corroboration_evidence_id='',policy_fingerprint=release.policy_fingerprint,assurance_manifest_hash=release.assurance_manifest_hash,recovery_capsule_hash=release.recovery_capsule_hash,opened_at=u64(now),expires_at=u64(now+int(policy.proposal_ttl_seconds)),reviewed_at=u64(0),recovery_deadline=u64(now+int(policy.execution_timeout_seconds)),status=STATUS_INCIDENT_CONFIRMED,last_review_code='ASSURANCE_DEADLINE_EXPIRED',recovery_authorized=True);proposal.status=STATUS_INCIDENT_CONFIRMED;self.actions.append({'kind':_E,_C:[incident_id,release_id,release.recovery_capsule_hash]})
		release.status=STATUS_INCIDENT_CONFIRMED
	def confirm_recovery(self,incident_id:str,release_id:str,recovery_hash:str)->_A:
		if incident_id not in self.incidents:raise gl.vm.UserError(_B)
		incident=self.incidents[incident_id]
		if self.actor!=incident.target:raise gl.vm.UserError('Only the protected target may confirm recovery')
		if incident.status!=STATUS_RECOVERED and self._now()>int(incident.recovery_deadline):raise gl.vm.UserError('Recovery confirmation deadline has passed')
		self._complete_recovery(incident_id,release_id,recovery_hash)
	def reconcile_recovery(self,incident_id:str)->_A:
		if incident_id not in self.incidents:raise gl.vm.UserError(_B)
		incident=self.incidents[incident_id]
		if incident.status not in(STATUS_INCIDENT_CONFIRMED,STATUS_RECOVERY_QUEUED,STATUS_RECOVERY_RETRY):raise gl.vm.UserError('Incident is not awaiting recovery reconciliation')
		self._complete_recovery(incident_id,incident.release_id,incident.recovery_capsule_hash)
	def expire_recovery(self,incident_id:str)->_A:
		if incident_id not in self.incidents:raise gl.vm.UserError(_B)
		incident=self.incidents[incident_id]
		if incident.status not in(STATUS_INCIDENT_CONFIRMED,STATUS_RECOVERY_QUEUED):raise gl.vm.UserError('Incident is not awaiting recovery')
		if self._now()<=int(incident.recovery_deadline):raise gl.vm.UserError('Recovery deadline has not passed')
		if self.target_final_mode==MODE_RECOVERED:self._complete_recovery(incident_id,incident.release_id,incident.recovery_capsule_hash);return
		incident.status=STATUS_RECOVERY_RETRY;self.releases[incident.release_id].status=STATUS_RECOVERY_RETRY
	def retry_recovery(self,incident_id:str)->_A:
		if incident_id not in self.incidents:raise gl.vm.UserError(_B)
		incident=self.incidents[incident_id]
		if incident.status!=STATUS_RECOVERY_RETRY:raise gl.vm.UserError('Recovery is not retryable')
		policy=self.policies[incident.target];now=self._now();incident.status=STATUS_INCIDENT_CONFIRMED;incident.recovery_deadline=u64(now+int(policy.execution_timeout_seconds));self.releases[incident.release_id].status=STATUS_INCIDENT_CONFIRMED;self.actions.append({'kind':_E,_C:[incident_id,incident.release_id,incident.recovery_capsule_hash]})
class ProofPatchRecoveryLifecycleEngine(gl.Contract):
	admin:Address;governor:Address;executor:Address
	def __init__(self):self.admin=gl.message.sender_address;self.governor=Address(ZERO);self.executor=Address(ZERO)
	@gl.public.write
	def bind_governor(self,governor:str)->_A:
		if gl.message.sender_address!=self.admin:raise gl.vm.UserError('Only admin may bind governor')
		if self.governor!=Address(ZERO):raise gl.vm.UserError('Governor is already bound')
		candidate=Address(governor)
		if candidate==Address(ZERO):raise gl.vm.UserError('Governor cannot be the zero address')
		self.governor=candidate
	@gl.public.write
	def bind_executor(self,executor:str)->_A:
		if gl.message.sender_address!=self.admin:raise gl.vm.UserError('Only admin may bind executor')
		if self.executor!=Address(ZERO):raise gl.vm.UserError('Executor is already bound')
		candidate=Address(executor)
		if candidate==Address(ZERO):raise gl.vm.UserError('Executor cannot be the zero address')
		self.executor=candidate
	def _encode(self,value:object)->object:
		if isinstance(value,Address):return str(value)
		if isinstance(value,bytes):return value.hex()
		if isinstance(value,bool):return value
		if isinstance(value,int):return int(value)
		if isinstance(value,dict):return{str(k):self._encode(v)for(k,v)in value.items()}
		if isinstance(value,list):return[self._encode(v)for v in value]
		if hasattr(value,'__dict__'):return{k:self._encode(v)for(k,v)in value.__dict__.items()}
		return value
	def _record(self,cls:object,raw:dict[object,object])->object:
		value=list(raw.values())
		if cls in(TargetPolicy,UpgradeProposal,ReleaseRecord,IncidentRecord):value[1]=Address(value[1])
		if cls is TargetPolicy:value[0]=Address(value[0])
		elif cls is UpgradeProposal:
			value[2]=Address(value[2])
			if isinstance(value[8],str):value[8]=bytes.fromhex(value[8])
			if isinstance(value[20],str):value[20]=bytes.fromhex(value[20])
		return cls(**dict(zip(cls.__annotations__.keys(),value)))
	def _load(self,logic:ProofPatchRecoveryLifecycleLogic,data:dict[object,object])->_A:
		D='active_target';C='incident';B='proposal';A='policy';logic.actor=Address(data['actor']);logic.now=int(data['now']);logic.proposal_count=u256(data.get(_F,0));logic.release_count=u256(data.get(_G,0));logic.installed_candidate_hashes=dict(data.get(_H,{}));records=data.get('records',{})
		if records.get(A)is not _A:p=self._record(TargetPolicy,records[A]);logic.policies[p.target]=p
		if records.get(B)is not _A:p=self._record(UpgradeProposal,records[B]);logic.proposals[p.proposal_id]=p
		for key in('release','parent_release','recovery_release'):
			if records.get(key)is not _A:r=self._record(ReleaseRecord,records[key]);logic.releases[r.release_id]=r
		if records.get(C)is not _A:i=self._record(IncidentRecord,records[C]);logic.incidents[i.incident_id]=i
		if data.get(D)is not _A:logic.active_proposal_by_target[Address(data[D])]=u256(data.get('active_value',0))
		view=data.get('target_final',{});logic.target_final_proposal_id=u256(view.get('proposal_id',0));logic.target_final_candidate_hash=str(view.get('candidate_hash',''));logic.target_final_release_id=str(view.get('release_id',''));logic.target_final_mode=str(view.get('mode',''));logic.target_final_kernel_hash=str(view.get('kernel_hash',''))
	def _patch(self,logic:ProofPatchRecoveryLifecycleLogic,operation:str)->dict[object,object]:
		E='active';D='incidents';C='releases';B='proposals';A='policies';out={'operation':operation,A:[],B:[],C:[],D:[],E:[],_H:logic.installed_candidate_hashes,_F:int(logic.proposal_count),_G:int(logic.release_count),'actions':logic.actions}
		for value in logic.policies.values():out[A].append(self._encode(value))
		for value in logic.proposals.values():out[B].append(self._encode(value))
		for value in logic.releases.values():out[C].append(self._encode(value))
		for value in logic.incidents.values():out[D].append(self._encode(value))
		for(key,value)in logic.active_proposal_by_target.items():out[E].append([str(key),int(value)])
		return out
	@gl.public.write
	def execute(self,operation:str,request:str)->_A:
		if gl.message.sender_address!=self.executor:raise gl.vm.UserError('Only the bound lifecycle request engine may execute lifecycle logic')
		data=json.loads(request);logic=ProofPatchRecoveryLifecycleLogic();self._load(logic,data);args=data.get(_C,[])
		if operation=='expire_provisional':logic.expire_provisional(*args)
		elif operation=='confirm_recovery':logic.confirm_recovery(*args)
		elif operation=='reconcile_recovery':logic.reconcile_recovery(*args)
		elif operation=='expire_recovery':logic.expire_recovery(*args)
		elif operation=='retry_recovery':logic.retry_recovery(*args)
		else:raise gl.vm.UserError('Unknown recovery lifecycle operation')
		payload=json.dumps(self._patch(logic,operation),separators=(',',':'));ProofPatchGovernorV2(self.governor).emit(on='finalized').apply_lifecycle_result(operation,payload)