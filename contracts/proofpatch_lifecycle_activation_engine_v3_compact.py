# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_D='release_count';_C='proposal_count';_B='RECOVERED';_A=None;from genlayer import*;from dataclasses import dataclass;from datetime import datetime;from genlayer.py.public_abi import StorageType;import hashlib,json,typing;SCHEMA_VERSION='proofpatch-v2';EVIDENCE_SCHEMA='proofpatch-evidence-v2';ASSURANCE_SCHEMA='proofpatch-assurance-v1';INCIDENT_SCHEMA='proofpatch-incident-v1';MODE_BOOTSTRAP='BOOTSTRAP';MODE_ACTIVE='ACTIVE';MODE_PROVISIONAL='PROVISIONAL';MODE_RECOVERY_PENDING='RECOVERY_PENDING';MODE_RECOVERED=_B;STATUS_PROPOSED='PROPOSED';STATUS_REPAIR='EVIDENCE_REPAIR_REQUIRED';STATUS_RETRY='REVIEW_RETRY_REQUIRED';STATUS_REJECTED='REJECTED';STATUS_QUEUED='UPGRADE_QUEUED';STATUS_INSTALLED_PROVISIONAL='INSTALLED_PROVISIONAL';STATUS_ASSURANCE_PENDING='ASSURANCE_PENDING';STATUS_ASSURANCE_REPAIR='ASSURANCE_REPAIR_REQUIRED';STATUS_ASSURANCE_RETRY='ASSURANCE_RETRY_REQUIRED';STATUS_CERTIFICATION_QUEUED='CERTIFICATION_QUEUED';STATUS_CERTIFIED='CERTIFIED';STATUS_VERIFIED=STATUS_CERTIFIED;STATUS_EXPIRED='EXPIRED';STATUS_CANCELLED='CANCELLED';STATUS_EXECUTION_FAILED='EXECUTION_FAILED';STATUS_INCIDENT_OPEN='INCIDENT_OPEN';STATUS_INCIDENT_REPAIR='INCIDENT_REPAIR_REQUIRED';STATUS_INCIDENT_RETRY='INCIDENT_RETRY_REQUIRED';STATUS_INCIDENT_CONFIRMED='INCIDENT_CONFIRMED';STATUS_INCIDENT_DISMISSED='INCIDENT_DISMISSED';STATUS_RECOVERY_QUEUED='RECOVERY_QUEUED';STATUS_RECOVERY_RETRY='RECOVERY_RETRY_REQUIRED';STATUS_RECOVERED=_B;REVIEW_REPAIR='REPAIR';REVIEW_RETRY='RETRY';REVIEW_DECISION='DECISION';DECISION_APPROVE='APPROVE';DECISION_REJECT='REJECT';ASSURANCE_KEYS='installed_hash_matches','kernel_binding_matches','governor_binding_matches','critical_state_preserved','interface_requirements_hold','canary_requirements_hold','runtime_evidence_valid','no_post_install_security_regression','recovery_path_live','assurance_manifest_satisfied';INCIDENT_KEYS='incident_evidence_authentic','incident_affects_exact_release','incident_reproducible_or_sufficiently_established','constitution_breached','continued_operation_unsafe','recovery_capsule_applicable','recovery_safer_than_continuation','recovery_path_preserves_rights','recovery_path_preserves_governance';MAX_CONSTITUTION_BYTES=16000;MAX_CANDIDATE_BYTES=512000;MAX_URL_BYTES=1024;MAX_ID_BYTES=160;MAX_VERSION_BYTES=96;MAX_EVIDENCE_AGE_SECONDS=2592000;MAX_PROPOSAL_TTL_SECONDS=1209600;MAX_EXECUTION_TIMEOUT_SECONDS=604800;MIN_WINDOW_SECONDS=60;SEMANTIC_KEYS='storage_layout_compatible','forward_storage_compatible','reverse_storage_compatible_or_recovery_safe','user_rights_preserved','no_privilege_escalation','proofpatch_kernel_preserved','upgrade_authority_preserved','provisional_guard_preserved','consensus_binding_preserved','evidence_trust_preserved','finality_safety_preserved','liveness_preserved','no_hidden_value_transfer','assurance_manifest_sufficient','assurance_path_preserved','recovery_capsule_valid','recovery_path_preserved','constitution_satisfied';REVIEW_ENGINE='0x9840cCf5DBdf4AE5945Ca73367e8336cCBEF578e';STATUS_REVIEW_PENDING='REVIEW_PENDING';STATUS_INCIDENT_REVIEW_PENDING='INCIDENT_REVIEW_PENDING';ZERO='0x0000000000000000000000000000000000000000'
@allow_storage
@dataclass
class TargetPolicy:owner:Address;target:Address;constitution:str;policy_fingerprint:str;source_authority:str;ci_authority:str;audit_authority:str;source_prefix:str;ci_prefix:str;audit_prefix:str;assurance_authority:str;assurance_prefix:str;assurance_corroboration_authority:str;assurance_corroboration_prefix:str;proofpatch_kernel_hash:str;current_version:str;current_source_url:str;current_code_hash:str;current_release_id:str;max_evidence_age_seconds:u64;proposal_ttl_seconds:u64;execution_timeout_seconds:u64;assurance_observation_delay_seconds:u64;assurance_deadline_seconds:u64;max_manifest_bytes:u64;max_capsule_bytes:u64;active:bool
@allow_storage
@dataclass
class UpgradeProposal:proposal_id:u256;target:Address;proposer:Address;parent_version:str;parent_source_url:str;parent_code_hash:str;candidate_version:str;candidate_source_url:str;candidate_code:bytes;candidate_code_hash:str;ci_evidence_url:str;ci_evidence_id:str;audit_evidence_url:str;audit_evidence_id:str;assurance_manifest:str;assurance_manifest_hash:str;recovery_mode:str;recovery_release_id:str;recovery_version:str;recovery_source_url:str;recovery_code:bytes;recovery_code_hash:str;recovery_capsule_hash:str;evidence_set_hash:str;policy_fingerprint:str;created_at:u64;expires_at:u64;reviewed_at:u64;execution_deadline:u64;status:str;last_review_code:str
@allow_storage
@dataclass
class ReleaseRecord:release_id:str;target:Address;version:str;parent_release_id:str;parent_code_hash:str;source_url:str;code_hash:str;proposal_id:u256;policy_fingerprint:str;evidence_set_hash:str;assurance_manifest_hash:str;recovery_capsule_hash:str;installed_at:u64;certified_at:u64;status:str;recovered_from_release_id:str;recovery_incident_id:str;lineage_hash:str
@gl.contract_interface
class ProofPatchGovernorV2:
	class Write:
		def apply_lifecycle_result(self,operation:str,payload:str)->_A:...
class ProofPatchActivationLifecycleLogic:
	def __init__(self):self.policies={};self.proposals={};self.releases={};self.incidents={};self.active_proposal_by_target={};self.installed_candidate_hashes={};self.proposal_count=u256(0);self.release_count=u256(0);self.actions=[]
	def _now(self)->int:return self.now
	def _require_proposal(self,proposal_id:u256)->UpgradeProposal:
		if proposal_id not in self.proposals:raise gl.vm.UserError('Unknown proposal')
		return self.proposals[proposal_id]
	def _release_active(self,target:Address,proposal_id:u256)->_A:
		if self.active_proposal_by_target.get(target,self._inactive_proposal())==proposal_id:self.active_proposal_by_target[target]=self._inactive_proposal()
	def _proposal_release_id(self,proposal:UpgradeProposal)->str:return'release-'+str(proposal.proposal_id)+'-'+proposal.candidate_code_hash[:16]
class ProofPatchActivationLifecycleEngine(gl.Contract):
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
	def _encode(self,value):
		if isinstance(value,Address):return str(value)
		if isinstance(value,bytes):return value.hex()
		if isinstance(value,bool):return value
		if isinstance(value,int):return int(value)
		if isinstance(value,dict):return{str(k):self._encode(v)for(k,v)in value.items()}
		if isinstance(value,list):return[self._encode(v)for v in value]
		if hasattr(value,'__dict__'):return{k:self._encode(v)for(k,v)in value.__dict__.items()}
		return value
	def _record(self,cls,raw):
		value=list(raw.values())
		if cls in(TargetPolicy,UpgradeProposal,ReleaseRecord):value[1]=Address(value[1])
		if cls is TargetPolicy:value[0]=Address(value[0])
		elif cls is UpgradeProposal:
			value[2]=Address(value[2])
			if isinstance(value[8],str):value[8]=bytes.fromhex(value[8])
			if isinstance(value[20],str):value[20]=bytes.fromhex(value[20])
		return cls(**dict(zip(cls.__annotations__.keys(),value)))
	def _load(self,logic,data):
		C='release';B='proposal';A='policy';logic.actor=Address(data['actor']);logic.now=int(data['now']);records=data.get('records',{});logic.proposal_count=u256(data.get(_C,0));logic.release_count=u256(data.get(_D,0))
		if records.get(A)is not _A:p=self._record(TargetPolicy,records[A]);logic.policies[p.target]=p
		if records.get(B)is not _A:p=self._record(UpgradeProposal,records[B]);logic.proposals[p.proposal_id]=p
		if records.get(C)is not _A:r=self._record(ReleaseRecord,records[C]);logic.releases[r.release_id]=r
	def _patch(self,logic,operation):
		C='releases';B='proposals';A='policies';out={'operation':operation,A:[],B:[],C:[],'incidents':[],'active':[],'installed_candidate_hashes':logic.installed_candidate_hashes,_C:int(logic.proposal_count),_D:int(logic.release_count),'actions':logic.actions}
		for v in logic.policies.values():out[A].append(self._encode(v))
		for v in logic.proposals.values():out[B].append(self._encode(v))
		for v in logic.releases.values():out[C].append(self._encode(v))
		return out
	@gl.public.write
	def execute(self,operation,request):
		if gl.message.sender_address!=self.executor:raise gl.vm.UserError('Only the bound lifecycle request engine may execute lifecycle logic')
		if operation!='confirm_activation':raise gl.vm.UserError('Unsupported activation lifecycle operation')
		data=json.loads(request);logic=ProofPatchActivationLifecycleLogic();self._load(logic,data);logic.confirm_activation(*data.get('args',[]));ProofPatchGovernorV2(self.governor).emit(on='finalized').apply_lifecycle_result(operation,json.dumps(self._patch(logic,operation),separators=(',',':')))
