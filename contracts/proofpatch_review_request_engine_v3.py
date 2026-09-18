# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownParameterType=false, reportMissingParameterType=false, reportInvalidTypeForm=false, reportOptionalMemberAccess=false, reportUnboundVariable=false, reportOptionalSubscript=false, reportGeneralTypeIssues=false, reportAssignmentType=false, reportIndexIssue=false, reportCallIssue=false, reportUnnecessaryCast=false, reportPrivateUsage=false, reportUnusedFunction=false, reportUnusedImport=false
from genlayer import *
from genlayer.py.public_abi import StorageType
import json
ZERO='0x0000000000000000000000000000000000000000'
STATUS_PROPOSED='PROPOSED'
STATUS_RETRY='REVIEW_RETRY_REQUIRED'
STATUS_REVIEW_PENDING='REVIEW_PENDING'
STATUS_INCIDENT_OPEN='INCIDENT_OPEN'
STATUS_INCIDENT_RETRY='INCIDENT_RETRY_REQUIRED'
STATUS_INCIDENT_REVIEW_PENDING='INCIDENT_REVIEW_PENDING'
@gl.contract_interface
class ProofPatchGovernorV2:
    class View:
        def get_state_record(self, kind: str, key: str) -> str: ...
    class Write:
        def apply_review_request(self, operation: str, request: str) -> None: ...
@gl.contract_interface
class ProofPatchTarget:
    class View:
        def proofpatch_installed_proposal_id(self) -> u256: ...
        def proofpatch_installed_candidate_hash(self) -> str: ...
        def proofpatch_installed_release_id(self) -> str: ...
        def proofpatch_release_mode(self) -> str: ...
        def get_proofpatch_kernel_hash(self) -> str: ...
        def get_proofpatch_governor(self) -> Address: ...
class ProofPatchReviewRequestEngine(gl.Contract):
    admin: Address
    governor: Address
    def __init__(self):
        self.admin=gl.message.sender_address; self.governor=Address(ZERO)
    @gl.public.write
    def bind_governor(self, governor: str) -> None:
        if gl.message.sender_address!=self.admin: raise gl.vm.UserError('Only admin may bind governor')
        if self.governor!=Address(ZERO): raise gl.vm.UserError('Governor is already bound')
        self.governor=Address(governor)
    def _get(self, view, kind, key):
        return json.loads(view.get_state_record(kind,key))
    def _proposal(self, v, a, now):
        p=self._get(v,'proposal',str(int(a[0]))); q=self._get(v,'policy',p['target'])
        if p['status'] not in (STATUS_PROPOSED,STATUS_RETRY,STATUS_REVIEW_PENDING): raise gl.vm.UserError('Proposal is not reviewable')
        if now>int(p['expires_at']): raise gl.vm.UserError('Proposal has expired; call expire_proposal')
        if not q['active'] or q['policy_fingerprint']!=p['policy_fingerprint'] or q['current_code_hash']!=p['parent_code_hash']: raise gl.vm.UserError('Proposal policy snapshot is no longer current')
        p['status']=STATUS_REVIEW_PENDING; p['reviewed_at']=now; p['last_review_code']='ENGINE_PENDING'
        s={'proposal_id':p['proposal_id'],'target':p['target'],'parent_version':p['parent_version'],'parent_source_url':p['parent_source_url'],'parent_code_hash':p['parent_code_hash'],'candidate_version':p['candidate_version'],'candidate_source_url':p['candidate_source_url'],'candidate_code_hash':p['candidate_code_hash'],'candidate_code_hex':p['candidate_code'],'ci_evidence_url':p['ci_evidence_url'],'ci_evidence_id':p['ci_evidence_id'],'audit_evidence_url':p['audit_evidence_url'],'audit_evidence_id':p['audit_evidence_id'],'assurance_manifest':p['assurance_manifest'],'assurance_manifest_hash':p['assurance_manifest_hash'],'recovery_mode':p['recovery_mode'],'recovery_release_id':p['recovery_release_id'],'recovery_version':p['recovery_version'],'recovery_source_url':p['recovery_source_url'],'recovery_code_hash':p['recovery_code_hash'],'recovery_capsule_hash':p['recovery_capsule_hash'],'recovery_code_hex':p['recovery_code'],'evidence_set_hash':p['evidence_set_hash'],'policy_fingerprint':p['policy_fingerprint'],'constitution':q['constitution'],'kernel_hash':q['proofpatch_kernel_hash'],'ci_authority':q['ci_authority'],'audit_authority':q['audit_authority'],'max_evidence_age_seconds':q['max_evidence_age_seconds'],'max_manifest_bytes':q['max_manifest_bytes'],'observation_delay_seconds':q['assurance_observation_delay_seconds'],'assurance_deadline_seconds':q['assurance_deadline_seconds'],'review_now':now,'manifest_error':''}
        return s,{'proposals':[p]}
    def _assurance(self, v, a, now):
        p=self._get(v,'proposal',str(int(a[0]))); q=self._get(v,'policy',p['target']); rid='release-'+str(p['proposal_id'])+'-'+p['candidate_code_hash'][:16]; t=ProofPatchTarget(Address(p['target'])).view(state=StorageType.LATEST_FINAL)
        return {'target':p['target'],'proposal_id':p['proposal_id'],'release_id':rid,'candidate_code_hash':p['candidate_code_hash'],'policy_fingerprint':p['policy_fingerprint'],'assurance_manifest_hash':p['assurance_manifest_hash'],'assurance_manifest':p['assurance_manifest'],'recovery_release_id':p['recovery_release_id'],'primary_url':a[1],'primary_evidence_id':a[2],'corroboration_url':a[3],'corroboration_evidence_id':a[4],'assurance_authority':q['assurance_authority'],'corroboration_authority':q['assurance_corroboration_authority'],'max_evidence_age_seconds':q['max_evidence_age_seconds'],'review_now':now,'installed_proposal_id':int(t.proofpatch_installed_proposal_id()),'installed_candidate_hash':t.proofpatch_installed_candidate_hash(),'installed_release_id':t.proofpatch_installed_release_id(),'installed_mode':t.proofpatch_release_mode(),'installed_kernel_hash':t.get_proofpatch_kernel_hash(),'target_governor':str(t.get_proofpatch_governor()),'expected_governor':str(self.governor),'kernel_hash':q['proofpatch_kernel_hash']}
    def _incident(self, v, a, now):
        i=self._get(v,'incident',a[0]); r=self._get(v,'release',i['release_id']); p=self._get(v,'proposal',str(r['proposal_id'])); q=self._get(v,'policy',i['target'])
        if i['status'] not in (STATUS_INCIDENT_OPEN,'INCIDENT_REPAIR_REQUIRED',STATUS_INCIDENT_RETRY,STATUS_INCIDENT_REVIEW_PENDING): raise gl.vm.UserError('Incident is not reviewable')
        if now>int(i['expires_at']): raise gl.vm.UserError('Incident review window has expired')
        i['status']=STATUS_INCIDENT_REVIEW_PENDING; i['reviewed_at']=now; i['last_review_code']='ENGINE_PENDING'
        s={'incident_id':i['incident_id'],'target':i['target'],'release_id':i['release_id'],'installed_code_hash':i['installed_code_hash'],'incident_type':i['incident_type'],'primary_url':i['primary_url'],'primary_evidence_id':i['primary_evidence_id'],'corroboration_url':i['corroboration_url'],'corroboration_evidence_id':i['corroboration_evidence_id'],'policy_fingerprint':i['policy_fingerprint'],'recovery_capsule_hash':i['recovery_capsule_hash'],'audit_authority':q['audit_authority'],'corroboration_authority':q['assurance_corroboration_authority'],'max_evidence_age_seconds':q['max_evidence_age_seconds'],'review_now':now,'release_code_hash':r['code_hash'],'proposal_recovery_capsule_hash':p['recovery_capsule_hash'],'proposal_recovery_release_id':p['recovery_release_id']}
        return s,{'incidents':[i]}
    @gl.public.write
    def execute(self, operation: str, request: str) -> None:
        if gl.message.sender_address!=self.governor: raise gl.vm.UserError('Only the bound governor may build review snapshots')
        d=json.loads(request); a=d['args']; now=int(d.get('now',0)); v=ProofPatchGovernorV2(self.governor).view(state=StorageType.LATEST_FINAL)
        patch={}
        if operation=='proposal': s,patch=self._proposal(v,a,now)
        elif operation=='assurance': s=self._assurance(v,a,now)
        elif operation=='incident': s,patch=self._incident(v,a,now)
        else: raise gl.vm.UserError('Unknown review request')
        ProofPatchGovernorV2(self.governor).emit(on='finalized').apply_review_request(operation,json.dumps({'args':a,'snapshot':json.dumps(s,sort_keys=True,separators=(',',':')),'patch':patch},separators=(',',':')))
