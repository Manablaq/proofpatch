# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import hashlib


PROOFPATCH_KERNEL_SOURCE = "\n".join((
    "owner: Address",
    "proofpatch_governor: Address",
    "proofpatch_kernel_hash: str",
    "proofpatch_registered: bool",
    "installed_release_id: str",
    "installed_proposal_id: u256",
    "installed_code_hash: str",
    "release_mode: str",
    "pending_release_id: str",
    "pending_code_hash: str",
    "last_recovery_incident_id: str",
    "last_recovery_release_id: str",
)) + "\n"
PROOFPATCH_KERNEL_HASH = hashlib.sha256(PROOFPATCH_KERNEL_SOURCE.encode("utf-8")).hexdigest()


@gl.contract_interface
class ProofPatchGovernorV2:
    class View:
        def is_upgrade_authorized(self, proposal_id: u256, target: str, candidate_hash: str) -> bool: ...
        def get_candidate_code(self, proposal_id: u256) -> bytes: ...
        def get_proposal_release_id(self, proposal_id: u256) -> str: ...
        def get_policy_kernel_hash(self, target: str) -> str: ...
        def is_activation_authorized(self, proposal_id: u256, release_id: str, candidate_hash: str) -> bool: ...
        def is_registration_authorized(self, target: str, release_id: str, code_hash: str) -> bool: ...
        def is_recovery_authorized(self, incident_id: str, release_id: str, recovery_hash: str) -> bool: ...
        def get_recovery_release_id(self, incident_id: str) -> str: ...
        def get_recovery_code(self, incident_id: str) -> bytes: ...

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
            assurance_authority: str,
            assurance_prefix: str,
            assurance_corroboration_authority: str,
            assurance_corroboration_prefix: str,
            proofpatch_kernel_hash: str,
            current_version: str,
            current_source_url: str,
            current_code_hash: str,
            max_evidence_age_seconds: int,
            proposal_ttl_seconds: int,
            execution_timeout_seconds: int,
            assurance_observation_delay_seconds: int,
            assurance_deadline_seconds: int,
            max_manifest_bytes: int,
            max_capsule_bytes: int,
        ) -> None: ...
        def confirm_install(self, proposal_id: u256, candidate_hash: str) -> None: ...
        def confirm_activation(self, proposal_id: u256, release_id: str, candidate_hash: str) -> None: ...
        def confirm_recovery(self, incident_id: str, release_id: str, recovery_hash: str) -> None: ...


class ProtectedTarget(gl.Contract):
    # PROOFPATCH_KERNEL_BEGIN
    # This prefix is append-only and must retain its order in every release.
    owner: Address
    proofpatch_governor: Address
    proofpatch_kernel_hash: str
    proofpatch_registered: bool
    installed_release_id: str
    installed_proposal_id: u256
    installed_code_hash: str
    release_mode: str
    pending_release_id: str
    pending_code_hash: str
    last_recovery_incident_id: str
    last_recovery_release_id: str
    # PROOFPATCH_KERNEL_END

    product_name: str
    protected_value: str

    def __init__(self, proofpatch_governor: Address, product_name: str, initial_value: str):
        self.owner = gl.message.sender_address
        self.proofpatch_governor = proofpatch_governor
        self.proofpatch_kernel_hash = PROOFPATCH_KERNEL_HASH
        self.proofpatch_registered = False
        self.installed_release_id = ""
        self.installed_proposal_id = u256(0)
        self.installed_code_hash = ""
        self.release_mode = "BOOTSTRAP"
        self.pending_release_id = ""
        self.pending_code_hash = ""
        self.last_recovery_incident_id = ""
        self.last_recovery_release_id = ""
        self.product_name = product_name
        self.protected_value = initial_value

        root = gl.storage.Root.get()
        root.upgraders.get().append(proofpatch_governor)

    def _only_owner(self) -> None:
        if gl.message.sender_address != self.owner:
            raise gl.vm.UserError("Only owner")

    def _only_governor(self) -> None:
        if gl.message.sender_address != self.proofpatch_governor:
            raise gl.vm.UserError("Only ProofPatch governor")

    def _require_active_release(self) -> None:
        if self.release_mode not in ("ACTIVE", "RECOVERED"):
            raise gl.vm.UserError("Protected writes are disabled until release certification")

    def _require_kernel_binding(self, code: bytes, expected_hash: str) -> None:
        try:
            source = code.decode("utf-8")
        except Exception:
            raise gl.vm.UserError("Candidate source is not UTF-8")
        begin = "# " + "PROOFPATCH_KERNEL_BEGIN"
        end = "# " + "PROOFPATCH_KERNEL_END"
        if source.count(begin) != 1 or source.count(end) != 1:
            raise gl.vm.UserError("Candidate kernel markers are not unique")
        start = source.index(begin) + len(begin)
        finish = source.index(end, start)
        normalized_lines = [
            line.strip()
            for line in source[start:finish].splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        actual_kernel_source = "\n".join(normalized_lines) + "\n"
        required_methods = (
            "proofpatch_confirm_registration(",
            "proofpatch_upgrade(",
            "proofpatch_activate(",
            "proofpatch_recover(",
            "get_proofpatch_kernel_hash(",
        )
        if actual_kernel_source != PROOFPATCH_KERNEL_SOURCE:
            raise gl.vm.UserError("Candidate ProofPatch kernel storage prefix changed")
        if any(source.count("def " + method) != 1 for method in required_methods):
            raise gl.vm.UserError("Candidate ProofPatch kernel interface is not unique")
        if expected_hash.lower() != PROOFPATCH_KERNEL_HASH:
            raise gl.vm.UserError("Candidate does not preserve the registered ProofPatch kernel")

    @gl.public.write
    def set_protected_value(self, value: str) -> None:
        self._only_owner()
        self._require_active_release()
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

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def proofpatch_installed_proposal_id(self) -> u256:
        return self.installed_proposal_id

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def proofpatch_installed_candidate_hash(self) -> str:
        return self.installed_code_hash

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def proofpatch_installed_release_id(self) -> str:
        return self.installed_release_id

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def proofpatch_release_mode(self) -> str:
        return self.release_mode

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_proofpatch_kernel_hash(self) -> str:
        return self.proofpatch_kernel_hash

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
        assurance_authority: str,
        assurance_prefix: str,
        assurance_corroboration_authority: str,
        assurance_corroboration_prefix: str,
        current_version: str,
        current_source_url: str,
        current_code_hash: str,
        max_evidence_age_seconds: int,
        proposal_ttl_seconds: int,
        execution_timeout_seconds: int,
        assurance_observation_delay_seconds: int,
        assurance_deadline_seconds: int,
        max_manifest_bytes: int,
        max_capsule_bytes: int,
    ) -> None:
        self._only_owner()
        if self.proofpatch_registered:
            raise gl.vm.UserError("Already registered with ProofPatch")
        self.proofpatch_registered = True
        ProofPatchGovernorV2(self.proofpatch_governor).emit(on="finalized").register_target(
            str(self.owner),
            constitution,
            source_authority,
            ci_authority,
            audit_authority,
            source_prefix,
            ci_prefix,
            audit_prefix,
            assurance_authority,
            assurance_prefix,
            assurance_corroboration_authority,
            assurance_corroboration_prefix,
            self.proofpatch_kernel_hash,
            current_version,
            current_source_url,
            current_code_hash,
            max_evidence_age_seconds,
            proposal_ttl_seconds,
            execution_timeout_seconds,
            assurance_observation_delay_seconds,
            assurance_deadline_seconds,
            max_manifest_bytes,
            max_capsule_bytes,
        )

    @gl.public.write
    def proofpatch_confirm_registration(self, release_id: str, code_hash: str) -> None:
        self._only_governor()
        governor = ProofPatchGovernorV2(self.proofpatch_governor)
        if not governor.view().is_registration_authorized(
            str(gl.message.contract_address), release_id, code_hash.lower()
        ):
            raise gl.vm.UserError("Registration authorization is absent or stale")
        if self.release_mode != "BOOTSTRAP":
            if self.installed_release_id == release_id and self.installed_code_hash == code_hash.lower():
                return
            raise gl.vm.UserError("Conflicting registration confirmation")
        self.installed_release_id = release_id
        self.installed_code_hash = code_hash.lower()
        self.release_mode = "ACTIVE"

    @gl.public.write
    def proofpatch_upgrade(self, proposal_id: u256, candidate_hash: str) -> None:
        self._only_governor()
        governor = ProofPatchGovernorV2(self.proofpatch_governor)
        normalized_hash = candidate_hash.lower()
        if not governor.view().is_upgrade_authorized(proposal_id, str(gl.message.contract_address), normalized_hash):
            raise gl.vm.UserError("ProofPatch authorization is absent, stale, or mismatched")
        candidate_code = governor.view().get_candidate_code(proposal_id)
        actual_hash = hashlib.sha256(candidate_code).hexdigest()
        if actual_hash != normalized_hash:
            raise gl.vm.UserError("Approved candidate bytes do not match approved hash")
        self._require_kernel_binding(
            candidate_code,
            governor.view().get_policy_kernel_hash(str(gl.message.contract_address)),
        )
        self.installed_proposal_id = proposal_id
        release_id = governor.view().get_proposal_release_id(proposal_id)
        self.installed_release_id = release_id
        self.installed_code_hash = actual_hash
        self.pending_release_id = release_id
        self.pending_code_hash = actual_hash
        self.release_mode = "PROVISIONAL"
        root = gl.storage.Root.get()
        code = root.code.get()
        code.truncate()
        code.extend(candidate_code)
        governor.emit(on="finalized").confirm_install(proposal_id, actual_hash)

    @gl.public.write
    def proofpatch_activate(self, release_id: str, candidate_hash: str) -> None:
        self._only_governor()
        governor = ProofPatchGovernorV2(self.proofpatch_governor)
        if not governor.view().is_activation_authorized(
            self.installed_proposal_id,
            release_id,
            candidate_hash.lower(),
        ):
            raise gl.vm.UserError("Certification authorization is absent or stale")
        if self.release_mode != "PROVISIONAL" or self.pending_code_hash != candidate_hash.lower():
            raise gl.vm.UserError("Target is not the exact provisional release")
        self.installed_release_id = release_id
        self.pending_release_id = ""
        self.pending_code_hash = ""
        self.release_mode = "ACTIVE"

        # The governor receives final target metadata before it marks the release CERTIFIED.
        governor.emit(on="finalized").confirm_activation(
            self.installed_proposal_id,
            release_id,
            candidate_hash.lower(),
        )

    @gl.public.write
    def proofpatch_recover(self, incident_id: str, release_id: str, recovery_hash: str) -> None:
        self._only_governor()
        governor = ProofPatchGovernorV2(self.proofpatch_governor)
        if not governor.view().is_recovery_authorized(incident_id, release_id, recovery_hash.lower()):
            raise gl.vm.UserError("Recovery authorization is absent, stale, or mismatched")
        if self.installed_release_id != release_id or self.installed_code_hash == "":
            raise gl.vm.UserError("Target no longer holds the challenged release")
        recovery_release_id = governor.view().get_recovery_release_id(incident_id)
        if recovery_release_id == "":
            raise gl.vm.UserError("Recovery release identity is absent")
        recovery_code = governor.view().get_recovery_code(incident_id)
        actual_hash = hashlib.sha256(recovery_code).hexdigest()
        if actual_hash != recovery_hash.lower():
            raise gl.vm.UserError("Recovery capsule bytes do not match approved hash")
        self._require_kernel_binding(
            recovery_code,
            governor.view().get_policy_kernel_hash(str(gl.message.contract_address)),
        )
        self.last_recovery_incident_id = incident_id
        self.last_recovery_release_id = recovery_release_id
        self.pending_release_id = recovery_release_id
        self.pending_code_hash = actual_hash
        self.installed_release_id = recovery_release_id
        self.installed_code_hash = actual_hash
        self.release_mode = "RECOVERED"
        root = gl.storage.Root.get()
        code = root.code.get()
        code.truncate()
        code.extend(recovery_code)
        governor.emit(on="finalized").confirm_recovery(incident_id, release_id, actual_hash)
