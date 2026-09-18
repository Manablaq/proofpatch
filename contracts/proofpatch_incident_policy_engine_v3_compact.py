# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
_N='Unknown incident policy operation';_M='repair_incident';_L='Incident evidence identifiers must be distinct';_K='operation';_J='utf-8';_I='used_incident_ids';_H='incident_corroboration';_G='incident_primary';_F='releases';_E='used_evidence_ids';_D=True;_C='incident';_B=None;_A=False;from genlayer import*;from dataclasses import dataclass;from genlayer.py.public_abi import StorageType;import hashlib,json,typing;SCHEMA_VERSION='proofpatch-v2';ASSURANCE_SCHEMA='proofpatch-assurance-v1';MODE_ACTIVE='ACTIVE';MODE_PROVISIONAL='PROVISIONAL';MODE_RECOVERED='RECOVERED';STATUS_PROPOSED='PROPOSED';STATUS_REPAIR='EVIDENCE_REPAIR_REQUIRED';STATUS_INSTALLED_PROVISIONAL='INSTALLED_PROVISIONAL';STATUS_ASSURANCE_PENDING='ASSURANCE_PENDING';STATUS_ASSURANCE_REPAIR='ASSURANCE_REPAIR_REQUIRED';STATUS_ASSURANCE_RETRY='ASSURANCE_RETRY_REQUIRED';STATUS_CERTIFIED='CERTIFIED';STATUS_INCIDENT_OPEN='INCIDENT_OPEN';STATUS_INCIDENT_REPAIR='INCIDENT_REPAIR_REQUIRED';STATUS_INCIDENT_RETRY='INCIDENT_RETRY_REQUIRED';MAX_CONSTITUTION_BYTES=16000;MAX_CANDIDATE_BYTES=512000;MAX_URL_BYTES=1024;MAX_ID_BYTES=160;MAX_VERSION_BYTES=96;MAX_EVIDENCE_AGE_SECONDS=2592000;MAX_PROPOSAL_TTL_SECONDS=1209600;MAX_EXECUTION_TIMEOUT_SECONDS=604800;MIN_WINDOW_SECONDS=60
@allow_storage
@dataclass
class TargetPolicy:owner:Address;target:Address;constitution:str;policy_fingerprint:str;source_authority:str;ci_authority:str;audit_authority:str;source_prefix:str;ci_prefix:str;audit_prefix:str;assurance_authority:str;assurance_prefix:str;assurance_corroboration_authority:str;assurance_corroboration_prefix:str;proofpatch_kernel_hash:str;current_version:str;current_source_url:str;current_code_hash:str;current_release_id:str;max_evidence_age_seconds:u64;proposal_ttl_seconds:u64;execution_timeout_seconds:u64;assurance_observation_delay_seconds:u64;assurance_deadline_seconds:u64;max_manifest_bytes:u64;max_capsule_bytes:u64;active:bool
@allow_storage
@dataclass
class ReleaseRecord:release_id:str;target:Address;version:str;parent_release_id:str;parent_code_hash:str;source_url:str;code_hash:str;proposal_id:u256;policy_fingerprint:str;evidence_set_hash:str;assurance_manifest_hash:str;recovery_capsule_hash:str;installed_at:u64;certified_at:u64;status:str;recovered_from_release_id:str;recovery_incident_id:str;lineage_hash:str
@allow_storage
@dataclass
class IncidentRecord:incident_id:str;target:Address;release_id:str;installed_code_hash:str;incident_type:str;primary_url:str;primary_evidence_id:str;corroboration_url:str;corroboration_evidence_id:str;policy_fingerprint:str;assurance_manifest_hash:str;recovery_capsule_hash:str;opened_at:u64;expires_at:u64;reviewed_at:u64;recovery_deadline:u64;status:str;last_review_code:str;recovery_authorized:bool
ZERO='0x0000000000000000000000000000000000000000'
@gl.contract_interface
class ProofPatchTarget:
	class View:
		def proofpatch_installed_release_id(self)->str:...
		def proofpatch_release_mode(self)->str:...
@gl.contract_interface
class ProofPatchGovernor:
	class View:
		def get_state_record(self,kind:str,key:str)->str:...
	class Write:
		def apply_policy_result(self,operation:str,payload:str)->_B:...
class IncidentPolicyLogic:
	def _hash_text_parts(self,parts:list[str])->str:return hashlib.sha256('\x1f'.join(parts).encode(_J)).hexdigest()
	def _check_text(self,value:str,label:str,minimum:int,maximum:int)->_B:
		encoded_len=len(value.encode(_J))
		if encoded_len<minimum or encoded_len>maximum:raise gl.vm.UserError(f"{label} length is invalid")
	def _is_canonical_raw_segment(self,value:str)->bool:
		if not value or value in('.','..'):return _A
		allowed='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'
		for char in value:
			if char not in allowed:return _A
		return _D
	def _raw_github_owner(self,prefix:str)->str:
		base='https://raw.githubusercontent.com/'
		if not prefix.startswith(base)or not prefix.endswith('/'):return''
		rest=prefix[len(base):];parts=rest.split('/')
		if len(parts)!=3 or parts[2]!='':return''
		owner=parts[0];repository=parts[1]
		if not self._is_canonical_raw_segment(owner):return''
		if not self._is_canonical_raw_segment(repository):return''
		return owner
	def _is_authority_prefix(self,prefix:str)->bool:return self._raw_github_owner(prefix)!=''
	def _is_immutable_url(self,url:str,prefix:str)->bool:
		if len(url.encode(_J))>MAX_URL_BYTES:return _A
		if not self._is_authority_prefix(prefix):return _A
		if not url.startswith(prefix):return _A
		suffix=url[len(prefix):];parts=suffix.split('/',1)
		if len(parts)!=2:return _A
		commit,path=parts
		if len(commit)!=40:return _A
		for char in commit:
			if char not in'0123456789abcdef':return _A
		path_segments=path.split('/')
		if not path_segments:return _A
		for segment in path_segments:
			if not self._is_canonical_raw_segment(segment):return _A
		return _D
	def _require_policy_owner(self,target:Address)->TargetPolicy:
		if target not in self.policies:raise gl.vm.UserError('Target is not registered')
		policy=self.policies[target]
		if self.actor!=policy.owner:raise gl.vm.UserError('Only the registered target owner may perform this action')
		if not policy.active:raise gl.vm.UserError('Target policy is inactive')
		return policy
	def _reserve_evidence_id(self,target:Address,issuer:str,kind:str,evidence_id:str)->_B:
		self._check_text(evidence_id,'evidence_id',8,MAX_ID_BYTES);reuse_key=self._hash_text_parts([str(target),issuer,kind,evidence_id])
		if self.used_evidence_ids.get(reuse_key,_A):raise gl.vm.UserError('Evidence identifier has already been used')
		self.used_evidence_ids[reuse_key]=_D
	def _open_incident(self,target:str,release_id:str,incident_type:str,primary_url:str,primary_evidence_id:str,corroboration_url:str,corroboration_evidence_id:str)->str:
		target_address=Address(target)
		if target_address not in self.policies or release_id not in self.releases:raise gl.vm.UserError('Unknown target or release')
		release=self.releases[release_id]
		if release.target!=target_address:raise gl.vm.UserError('Incident release belongs to another target')
		if incident_type not in('STATE_INVARIANT_VIOLATION','AUTHORIZATION_REGRESSION','UPGRADE_BYPASS','CONSENSUS_BINDING_REGRESSION','EVIDENCE_TRUST_REGRESSION','FINALITY_REGRESSION','LIVENESS_REGRESSION','HIDDEN_VALUE_TRANSFER','KERNEL_INTEGRITY_FAILURE','REQUIRED_INTERFACE_FAILURE','OTHER_CONSTITUTIONAL_BREACH'):raise gl.vm.UserError('Unsupported incident type')
		policy=self.policies[target_address]
		if not self._is_immutable_url(primary_url,policy.audit_prefix):raise gl.vm.UserError('Incident primary evidence URL is not approved and immutable')
		if not self._is_immutable_url(corroboration_url,policy.assurance_corroboration_prefix):raise gl.vm.UserError('Incident corroboration URL is not approved and immutable')
		if primary_evidence_id==corroboration_evidence_id:raise gl.vm.UserError(_L)
		self._reserve_evidence_id(target_address,policy.audit_authority,_G,primary_evidence_id);self._reserve_evidence_id(target_address,policy.assurance_corroboration_authority,_H,corroboration_evidence_id)
		if self.target_release_id!=release_id:raise gl.vm.UserError("Incident release is not the target's finalized release")
		if self.target_mode not in(MODE_ACTIVE,MODE_PROVISIONAL,MODE_RECOVERED):raise gl.vm.UserError('Incident target is not in a challengeable release mode')
		if release.recovery_capsule_hash=='':raise gl.vm.UserError('Release has no precommitted recovery capsule')
		if release.status not in(STATUS_CERTIFIED,STATUS_INSTALLED_PROVISIONAL,STATUS_ASSURANCE_PENDING,STATUS_ASSURANCE_REPAIR,STATUS_ASSURANCE_RETRY,STATUS_INCIDENT_OPEN):raise gl.vm.UserError('Release is not challengeable in its current lifecycle state')
		incident_id='incident-'+str(self.now)+'-'+primary_evidence_id
		if incident_id in self.incidents:raise gl.vm.UserError('Incident identifier already exists')
		incident_replay_key=self._hash_text_parts([str(target_address),release_id,primary_evidence_id,corroboration_evidence_id])
		if self.used_incident_ids.get(incident_replay_key,_A):raise gl.vm.UserError('Incident evidence has already been used for this release')
		self.used_incident_ids[incident_replay_key]=_D;self.incidents[incident_id]=IncidentRecord(incident_id=incident_id,target=target_address,release_id=release_id,installed_code_hash=release.code_hash,incident_type=incident_type,primary_url=primary_url,primary_evidence_id=primary_evidence_id,corroboration_url=corroboration_url,corroboration_evidence_id=corroboration_evidence_id,policy_fingerprint=release.policy_fingerprint,assurance_manifest_hash=release.assurance_manifest_hash,recovery_capsule_hash=release.recovery_capsule_hash,opened_at=u64(self.now),expires_at=u64(self.now+int(policy.proposal_ttl_seconds)),reviewed_at=u64(0),recovery_deadline=u64(0),status=STATUS_INCIDENT_OPEN,last_review_code='',recovery_authorized=_A);release.status=STATUS_INCIDENT_OPEN;return incident_id
	def _repair_incident(self,incident_id:str,primary_url:str,primary_evidence_id:str,corroboration_url:str,corroboration_evidence_id:str)->_B:
		if incident_id not in self.incidents:raise gl.vm.UserError('Unknown incident')
		incident=self.incidents[incident_id];policy=self._require_policy_owner(incident.target)
		if incident.status not in(STATUS_INCIDENT_REPAIR,STATUS_INCIDENT_RETRY):raise gl.vm.UserError('Incident evidence can only be replaced after a repairable review result')
		if self.now>int(incident.expires_at):raise gl.vm.UserError('Incident review window has expired')
		if not self._is_immutable_url(primary_url,policy.audit_prefix):raise gl.vm.UserError('Replacement incident primary URL is not approved and immutable')
		if not self._is_immutable_url(corroboration_url,policy.assurance_corroboration_prefix):raise gl.vm.UserError('Replacement incident corroboration URL is not approved and immutable')
		if primary_evidence_id==corroboration_evidence_id:raise gl.vm.UserError(_L)
		self._reserve_evidence_id(incident.target,policy.audit_authority,_G,primary_evidence_id);self._reserve_evidence_id(incident.target,policy.assurance_corroboration_authority,_H,corroboration_evidence_id);incident.primary_url=primary_url;incident.primary_evidence_id=primary_evidence_id;incident.corroboration_url=corroboration_url;incident.corroboration_evidence_id=corroboration_evidence_id;incident.reviewed_at=u64(0);incident.last_review_code='';incident.status=STATUS_INCIDENT_OPEN;self.releases[incident.release_id].status=STATUS_INCIDENT_OPEN
class IncidentPolicyEngine(gl.Contract):
	admin:Address;governor:Address
	def __init__(self):self.admin=gl.message.sender_address;self.governor=Address(ZERO)
	@gl.public.write
	def bind_governor(self,governor:str)->_B:
		if gl.message.sender_address!=self.admin:raise gl.vm.UserError('Only admin may bind governor')
		if self.governor!=Address(ZERO):raise gl.vm.UserError('Governor is already bound')
		candidate=Address(governor)
		if candidate==Address(ZERO):raise gl.vm.UserError('Governor cannot be the zero address')
		self.governor=candidate
	def _load(self,logic:IncidentPolicyLogic,data:dict[object,object])->_B:
		H='target_mode';G='target_release_id';F='evidence';E='assurance_corroboration_authority';D='audit_authority';C='release';B='\\x1f';A='policy';operation=str(data.get(_K,''));args=data['args'];view=ProofPatchGovernor(self.governor).view(state=StorageType.LATEST_FINAL)
		def get(kind:str,key:str)->dict[object,object]:return typing.cast(dict[object,object],json.loads(view.get_state_record(kind,key)))
		def flag(kind:str,key:str,destination:str)->_B:
			if get(kind,key).get('value',_A):data[destination][key]=_D
		def evidence_key(target:str,issuer:str,kind:str,evidence_id:str)->str:return hashlib.sha256(B.join([target,issuer,kind,evidence_id]).encode()).hexdigest()
		data[_E]={};data[_I]={}
		if operation==_C:
			target=str(args[0]);release_id=str(args[1]);data[A]=get(A,target);data[_F]=[get(C,release_id)];policy=data[A]
			for(issuer,kind,evidence_id)in((policy[D],_G,args[4]),(policy[E],_H,args[6])):flag(F,evidence_key(target,issuer,kind,evidence_id),_E)
			replay_key=hashlib.sha256(B.join([target,release_id,args[4],args[6]]).encode()).hexdigest();flag('incident_evidence',replay_key,_I);target_view=ProofPatchTarget(Address(target)).view(state=StorageType.LATEST_FINAL);data[G]=target_view.proofpatch_installed_release_id();data[H]=target_view.proofpatch_release_mode()
		elif operation==_M:
			data[_C]=get(_C,str(args[0]));target=data[_C]['target'];data[A]=get(A,target);data[_F]=[get(C,data[_C]['release_id'])];policy=data[A]
			for(issuer,kind,evidence_id)in((policy[D],_G,args[2]),(policy[E],_H,args[4])):flag(F,evidence_key(target,issuer,kind,evidence_id),_E)
		else:raise gl.vm.UserError(_N)
		logic.policies={};logic.releases={};logic.incidents={};logic.used_evidence_ids=typing.cast(dict[object,bool],data[_E]);logic.used_incident_ids=typing.cast(dict[object,bool],data[_I])
		if data.get(A)is not _B:policy=self._record(TargetPolicy,data[A]);logic.policies[policy.target]=policy
		for raw in typing.cast(list[dict[object,object]],data.get(_F,[])):release=self._record(ReleaseRecord,raw);logic.releases[release.release_id]=release
		if data.get(_C)is not _B:incident=self._record(IncidentRecord,data[_C]);logic.incidents[incident.incident_id]=incident
		logic.actor=Address(data['actor']);logic.now=int(data['now']);logic.target_release_id=str(data.get(G,''));logic.target_mode=str(data.get(H,''))
	def _encode(self,value:object)->object:
		if isinstance(value,Address):return str(value)
		if isinstance(value,bytes):return value.hex()
		if isinstance(value,bool):return value
		if isinstance(value,int):return int(value)
		if isinstance(value,dict):return{str(key):self._encode(item)for(key,item)in value.items()}
		if isinstance(value,list):return[self._encode(item)for item in value]
		if hasattr(value,'__dict__'):return{key:self._encode(item)for(key,item)in value.__dict__.items()}
		return value
	def _record(self,cls:typing.Any,raw:dict[object,object])->typing.Any:
		value=list(raw.values())
		if cls in(TargetPolicy,ReleaseRecord,IncidentRecord):value[1]=Address(value[1])
		if cls is TargetPolicy:value[0]=Address(value[0])
		return cls(**dict(zip(cls.__annotations__.keys(),value)))
	def _patch(self,logic:IncidentPolicyLogic,operation:str)->dict[object,object]:
		B='incidents';A='policies';result={_K:operation,A:[],'proposals':[],_F:[],B:[],'active':[],_E:logic.used_evidence_ids,'installed_candidate_hashes':{},_I:logic.used_incident_ids,'proposal_count':0}
		for value in logic.policies.values():result[A].append(self._encode(value))
		for value in logic.releases.values():result[_F].append(self._encode(value))
		for value in logic.incidents.values():result[B].append(self._encode(value))
		return result
	@gl.public.write
	def execute(self,operation:str,request:str)->_B:
		if gl.message.sender_address!=self.governor:raise gl.vm.UserError('Only the bound governor may execute incident policy logic')
		if operation not in(_C,_M):raise gl.vm.UserError(_N)
		data=json.loads(request);data[_K]=operation;logic=IncidentPolicyLogic();self._load(logic,data);args=data['args']
		if operation==_C:logic._open_incident(*args)
		else:logic._repair_incident(*args)
		ProofPatchGovernor(self.governor).emit(on='finalized').apply_policy_result(operation,json.dumps(self._patch(logic,operation),separators=(',',':')))
