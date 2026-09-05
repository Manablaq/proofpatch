# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import hashlib


@gl.contract_interface
class ProofPatchGovernor:
    class View:
        def is_upgrade_authorized(self, proposal_id: u256, target: str, candidate_hash: str) -> bool: ...
        def get_candidate_code(self, proposal_id: u256) -> bytes: ...
    class Write:
        def confirm_install(self, proposal_id: u256, candidate_hash: str) -> None: ...


class ProtectedTarget(gl.Contract):
    # Deliberately unsafe candidate used only as adversarial review evidence.
    # Storage layout is kept compatible so semantic authorization must catch behavior regressions.
    owner: Address
    proofpatch_governor: Address
    product_name: str
    protected_value: str
    installed_proposal_id: u256
    installed_candidate_hash: str
    registered_with_proofpatch: bool

    def __init__(self):
        pass

    @gl.public.write
    def set_protected_value(self, value: str) -> None:
        # SECURITY REGRESSION: v1 was owner-only; this lets any caller mutate protected state.
        self.protected_value = value

    @gl.public.write
    def proofpatch_upgrade(self, proposal_id: u256, candidate_hash: str) -> None:
        if gl.message.sender_address != self.proofpatch_governor:
            raise gl.vm.UserError("Only ProofPatch governor may enter the upgrade path")

        governor = ProofPatchGovernor(self.proofpatch_governor)
        normalized_hash = candidate_hash.lower()
        if not governor.view().is_upgrade_authorized(proposal_id, str(gl.message.contract_address), normalized_hash):
            raise gl.vm.UserError("Missing ProofPatch authorization")
        candidate_code = governor.view().get_candidate_code(proposal_id)
        actual_hash = hashlib.sha256(candidate_code).hexdigest()
        if actual_hash != normalized_hash:
            raise gl.vm.UserError("Candidate hash mismatch")

        # SECURITY REGRESSION: because this method is entered by the authorized governor,
        # this write to the locked upgrader list can succeed. It permanently grants the owner
        # a competing native upgrade capability, defeating ProofPatch on subsequent upgrades.
        root = gl.storage.Root.get()
        root.upgraders.get().append(self.owner)

        self.installed_proposal_id = proposal_id
        self.installed_candidate_hash = actual_hash
        code = root.code.get()
        code.truncate()
        code.extend(candidate_code)
        governor.emit(on="finalized").confirm_install(proposal_id, actual_hash)

    @gl.public.write
    def owner_upgrade_after_escalation(self, new_code: bytes) -> None:
        if gl.message.sender_address != self.owner:
            raise gl.vm.UserError("Only owner")
        root = gl.storage.Root.get()
        code = root.code.get()
        code.truncate()
        code.extend(new_code)

    @gl.public.view
    def proofpatch_installed_proposal_id(self) -> u256:
        return self.installed_proposal_id

    @gl.public.view
    def proofpatch_installed_candidate_hash(self) -> str:
        return self.installed_candidate_hash
