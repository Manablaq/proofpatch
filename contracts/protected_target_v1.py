# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import hashlib


@gl.contract_interface
class ProofPatchGovernor:
    class View:
        def is_upgrade_authorized(self, proposal_id: u256, target: str, candidate_hash: str) -> bool: ...
        def get_candidate_code(self, proposal_id: u256) -> bytes: ...

    class Write:
        def register_target(
            self,
            owner: str,
            constitution: str,
            source_authority: str,
            ci_authority: str,
            audit_authority: str,
            source_prefix: str,
            ci_prefix: str,
            audit_prefix: str,
            current_version: str,
            current_source_url: str,
            current_code_hash: str,
            max_evidence_age_seconds: int,
            proposal_ttl_seconds: int,
            execution_timeout_seconds: int,
        ) -> None: ...
        def confirm_install(self, proposal_id: u256, candidate_hash: str) -> None: ...


class ProtectedTarget(gl.Contract):
    # IMPORTANT: these fields and their order are the persistent v1 storage layout.
    owner: Address
    proofpatch_governor: Address
    product_name: str
    protected_value: str
    installed_proposal_id: u256
    installed_candidate_hash: str
    registered_with_proofpatch: bool

    def __init__(self, proofpatch_governor: str, product_name: str, initial_value: str):
        governor = Address(proofpatch_governor)
        self.owner = gl.message.sender_address
        self.proofpatch_governor = governor
        self.product_name = product_name
        self.protected_value = initial_value
        self.installed_proposal_id = u256(0)
        self.installed_candidate_hash = ""
        self.registered_with_proofpatch = False

        # ProofPatch is the sole upgrader. The owner intentionally is NOT an upgrader.
        root = gl.storage.Root.get()
        root.upgraders.get().append(governor)

    def _only_owner(self) -> None:
        if gl.message.sender_address != self.owner:
            raise gl.vm.UserError("Only owner")

    @gl.public.write
    def set_protected_value(self, value: str) -> None:
        self._only_owner()
        self.protected_value = value

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_protected_value(self) -> str:
        return self.protected_value

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_product_name(self) -> str:
        return self.product_name

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_owner(self) -> Address:
        return self.owner

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_proofpatch_governor(self) -> Address:
        return self.proofpatch_governor

    @gl.public.write
    def register_with_proofpatch(
        self,
        constitution: str,
        source_authority: str,
        ci_authority: str,
        audit_authority: str,
        source_prefix: str,
        ci_prefix: str,
        audit_prefix: str,
        current_version: str,
        current_source_url: str,
        current_code_hash: str,
        max_evidence_age_seconds: int,
        proposal_ttl_seconds: int,
        execution_timeout_seconds: int,
    ) -> None:
        self._only_owner()
        if self.registered_with_proofpatch:
            raise gl.vm.UserError("Already registered with ProofPatch")
        self.registered_with_proofpatch = True

        # Registration becomes visible to the governor only when this transaction finalizes.
        ProofPatchGovernor(self.proofpatch_governor).emit(on="finalized").register_target(
            str(self.owner),
            constitution,
            source_authority,
            ci_authority,
            audit_authority,
            source_prefix,
            ci_prefix,
            audit_prefix,
            current_version,
            current_source_url,
            current_code_hash,
            max_evidence_age_seconds,
            proposal_ttl_seconds,
            execution_timeout_seconds,
        )

    @gl.public.write
    def proofpatch_upgrade(self, proposal_id: u256, candidate_hash: str) -> None:
        if gl.message.sender_address != self.proofpatch_governor:
            raise gl.vm.UserError("Only ProofPatch governor may upgrade this target")

        governor = ProofPatchGovernor(self.proofpatch_governor)
        normalized_hash = candidate_hash.lower()
        if not governor.view().is_upgrade_authorized(
            proposal_id,
            str(gl.message.contract_address),
            normalized_hash,
        ):
            raise gl.vm.UserError("ProofPatch authorization is absent, stale, or mismatched")

        candidate_code = governor.view().get_candidate_code(proposal_id)
        actual_hash = hashlib.sha256(candidate_code).hexdigest()
        if actual_hash != normalized_hash:
            raise gl.vm.UserError("Approved candidate bytes do not match approved hash")

        # Persist install attestation BEFORE replacing code; compatible upgrades retain it.
        self.installed_proposal_id = proposal_id
        self.installed_candidate_hash = actual_hash

        root = gl.storage.Root.get()
        code = root.code.get()
        code.truncate()
        code.extend(candidate_code)

        # Confirmation itself is finality-gated and idempotent on the governor side.
        governor.emit(on="finalized").confirm_install(proposal_id, actual_hash)

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def proofpatch_installed_proposal_id(self) -> u256:
        return self.installed_proposal_id

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def proofpatch_installed_candidate_hash(self) -> str:
        return self.installed_candidate_hash
