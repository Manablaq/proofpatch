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
    "method:_kernel_method_digest:a16e3dd87e652f28ed622b1e2d8e16677dd61f5de6036300c5832d267bdf93cd",
    "method:_only_owner:12632df4486f8159733db9fcb434f5ce995f04c5811443cbd2ab4d13348f7ac5",
    "method:_only_governor:6aafabb1c65bee4198588d92fad908ce041b240caac7d98e5d2d8ff14f449004",
    "method:_require_active_release:7c24465b0aef58865edaaebb926825e37d8ed6dc0bcc970b9fd42421492b9f5c",
    "method:_require_kernel_binding:6ea876d1cd6e7a548bc50727d1e9fad65eac1231c2979f7bec93423b0a786e71",
    "method:proofpatch_confirm_registration:b8729d963a677dd093c586927dfdebfaa0cdbdfe7a65a07ea96a08c3834c86ff",
    "method:proofpatch_upgrade:229fa0c58ef8eb73d46c64bd5235a7ddb044ef77de2607f67ce8b42e9af7a89c",
    "method:proofpatch_activate:5eef835283b3f14ea78a3ff1c42cb2cbbb2ce02681ba3a4ae9f88493d2d27983",
    "method:proofpatch_recover:33be12f2dfac13ef60ec25fd0176fb1db712db0ba016ffce61ba14c6dad7b696",
    "method:get_proofpatch_governor:f80077cd0f6e72975cf1965087b92a66df5b01b83e48645cc72214dfa89b8ada",
    "method:proofpatch_installed_proposal_id:1eb453af4aeb1971a3ee55970002f9213a49d0f98f656d309f7ee53cbd0024c9",
    "method:proofpatch_installed_candidate_hash:e4997fef5abf8697a21f5383b77820d73a8c69e8f8e4f79e4d726b86e2282ac8",
    "method:proofpatch_installed_release_id:3367fd4c16c8409ae2695e8321830a24761ab9813b994414ea76ee3471965e76",
    "method:proofpatch_release_mode:602abb31465bc9ad120ca258eca3d825788391a870c3fd9e8a9a9e233bf9ab94",
    "method:get_proofpatch_kernel_hash:1d0fbad12f87eb719bbb0606a65192249bc66a48a8722e43976e09ab5bcb5d13",
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

    def _kernel_method_digest(self, source: str, name: str) -> str:
        lines = source.splitlines()
        matches = [index for index, line in enumerate(lines) if line.startswith("    def " + name + "(")]
        if len(matches) != 1:
            raise gl.vm.UserError("Candidate ProofPatch kernel method is not unique")
        index = matches[0]
        start = index
        while start > 0 and lines[start - 1].startswith("    @"):
            start -= 1
        end = len(lines)
        for cursor in range(index + 1, len(lines)):
            if lines[cursor].startswith("    def ") or lines[cursor].startswith("    @gl.public"):
                end = cursor
                break
        normalized = "\n".join(line.rstrip() for line in lines[start:end]).strip() + "\n"
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

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
        storage_source = "\n".join(PROOFPATCH_KERNEL_SOURCE.splitlines()[:12]) + "\n"
        if actual_kernel_source != storage_source:
            raise gl.vm.UserError("Candidate ProofPatch kernel storage prefix changed")
        if hashlib.sha256(PROOFPATCH_KERNEL_SOURCE.encode("utf-8")).hexdigest() != expected_hash.lower():
            raise gl.vm.UserError("Candidate does not preserve the registered ProofPatch kernel")
        entries: list[tuple[str, str]] = []
        for line in PROOFPATCH_KERNEL_SOURCE.splitlines():
            if line.startswith("method:"):
                parts = line.split(":")
                if len(parts) != 3:
                    raise gl.vm.UserError("ProofPatch kernel manifest is malformed")
                entries.append((parts[1], parts[2]))
        if len(entries) != 15:
            raise gl.vm.UserError("ProofPatch kernel manifest is incomplete")
        for name, digest in entries:
            if self._kernel_method_digest(source, name) != digest:
                raise gl.vm.UserError("Candidate ProofPatch security implementation changed")

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

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def get_release_label(self) -> str:
        return "ProtectedTarget/v3-recovery-capsule"

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
