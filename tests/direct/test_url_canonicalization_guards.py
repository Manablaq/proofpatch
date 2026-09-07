import hashlib


CONSTITUTION = """
ProofPatch Security Constitution v1
1. Preserve every existing user withdrawal and owner-control invariant.
2. Never introduce an unrestricted administrative value-transfer or mutation path.
3. ProofPatch must remain the only contract-code upgrade authority.
4. Consequential authorization decisions require exact validator agreement.
5. Evidence must remain bound to approved immutable publishers, freshness, and independent corroboration.
6. Irreversible cross-contract consequences must execute only after GenLayer finality.
7. Every bounded workflow must retain expiry/recovery semantics.
8. The persistent storage layout must remain backward compatible.
9. No alternate method may bypass a suspension, challenge, policy, or upgrade consequence.
""".strip()

SOURCE_PREFIX = "https://raw.githubusercontent.com/proofpatch-labs/protected-app/"
CI_PREFIX = "https://raw.githubusercontent.com/proofpatch-labs/protected-app-ci/"
AUDIT_PREFIX = "https://raw.githubusercontent.com/independent-audit-labs/proofpatch-audits/"

SOURCE_AUTHORITY = "proofpatch-labs/protected-app"
CI_AUTHORITY = "proofpatch-labs/protected-app-ci"
AUDIT_AUTHORITY = "independent-audit-labs/proofpatch-audits"

PARENT_COMMIT = "a" * 40
CANDIDATE_COMMIT = "b" * 40
CI_COMMIT = "c" * 40
AUDIT_COMMIT = "e" * 40

PARENT_BYTES = b"parent-source-v1\n"
CANDIDATE_BYTES = b"candidate-source-v2\n"

PARENT_HASH = hashlib.sha256(PARENT_BYTES).hexdigest()

PARENT_URL = (
    SOURCE_PREFIX
    + PARENT_COMMIT
    + "/contracts/protected_target_v1.py"
)

CANDIDATE_URL = (
    SOURCE_PREFIX
    + CANDIDATE_COMMIT
    + "/contracts/protected_target_v2.py"
)

CI_URL = (
    CI_PREFIX
    + CI_COMMIT
    + "/evidence/ci.json"
)

AUDIT_URL = (
    AUDIT_PREFIX
    + AUDIT_COMMIT
    + "/evidence/audit.json"
)


def _address_arg(value) -> str:
    if isinstance(value, (bytes, bytearray)):
        raw = bytes(value)
        if len(raw) != 20:
            raise AssertionError(
                f"Direct Mode address must be 20 bytes, got {len(raw)}"
            )
        return "0x" + raw.hex()
    return str(value)


def _register(
    governor,
    direct_vm,
    target,
    owner,
    *,
    source_prefix=SOURCE_PREFIX,
    current_source_url=PARENT_URL,
):
    direct_vm.sender = target
    governor.register_target(
        _address_arg(owner),
        CONSTITUTION,
        SOURCE_AUTHORITY,
        CI_AUTHORITY,
        AUDIT_AUTHORITY,
        source_prefix,
        CI_PREFIX,
        AUDIT_PREFIX,
        "1.0.0",
        current_source_url,
        PARENT_HASH,
        24 * 60 * 60,
        2 * 24 * 60 * 60,
        24 * 60 * 60,
    )


def test_registration_rejects_noncanonical_authority_prefixes(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
):
    governor = direct_deploy("contracts/proofpatch_governor.py")

    bad_prefixes = (
        "https://raw.githubusercontent.com/proofpatch-labs/../",
        "https://raw.githubusercontent.com/proofpatch-labs/%2e%2e/",
        "https://raw.githubusercontent.com/proofpatch-labs/protected\\app/",
        "https://raw.githubusercontent.com/proofpatch-labs/protected%2dapp/",
    )

    for bad_prefix in bad_prefixes:
        bad_current = (
            bad_prefix
            + PARENT_COMMIT
            + "/contracts/protected_target_v1.py"
        )

        with direct_vm.expect_revert(
            "Invalid immutable source authority prefix"
        ):
            _register(
                governor,
                direct_vm,
                direct_bob,
                direct_alice,
                source_prefix=bad_prefix,
                current_source_url=bad_current,
            )


def test_registration_rejects_normalization_sensitive_current_source_urls(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
):
    governor = direct_deploy("contracts/proofpatch_governor.py")

    bad_urls = (
        SOURCE_PREFIX
        + PARENT_COMMIT
        + "/../main/contracts/protected_target_v1.py",

        SOURCE_PREFIX
        + PARENT_COMMIT
        + "/contracts/../protected_target_v1.py",

        SOURCE_PREFIX
        + PARENT_COMMIT
        + "/./contracts/protected_target_v1.py",

        SOURCE_PREFIX
        + PARENT_COMMIT
        + "/%2e%2e/main/contracts/protected_target_v1.py",

        SOURCE_PREFIX
        + PARENT_COMMIT
        + "/%2E%2E/main/contracts/protected_target_v1.py",

        SOURCE_PREFIX
        + PARENT_COMMIT
        + "/contracts\\..\\protected_target_v1.py",

        SOURCE_PREFIX
        + PARENT_COMMIT
        + "/contracts//protected_target_v1.py",

        SOURCE_PREFIX
        + PARENT_COMMIT
        + "/contracts/protected%5ftarget_v1.py",

        SOURCE_PREFIX
        + PARENT_COMMIT
        + "/contracts/protected target_v1.py",

        SOURCE_PREFIX
        + PARENT_COMMIT.upper()
        + "/contracts/protected_target_v1.py",
    )

    for bad_url in bad_urls:
        with direct_vm.expect_revert(
            "Current source must use the approved immutable commit URL"
        ):
            _register(
                governor,
                direct_vm,
                direct_bob,
                direct_alice,
                current_source_url=bad_url,
            )


def test_candidate_url_canonicalization_aliases_are_rejected(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(
        governor,
        direct_vm,
        direct_bob,
        direct_alice,
    )

    direct_vm.sender = direct_alice

    bad_candidate_urls = (
        SOURCE_PREFIX
        + CANDIDATE_COMMIT
        + "/../main/contracts/protected_target_v2.py",

        SOURCE_PREFIX
        + CANDIDATE_COMMIT
        + "/contracts/../protected_target_v2.py",

        SOURCE_PREFIX
        + CANDIDATE_COMMIT
        + "/contracts/./protected_target_v2.py",

        SOURCE_PREFIX
        + CANDIDATE_COMMIT
        + "/%2e%2e/main/contracts/protected_target_v2.py",

        SOURCE_PREFIX
        + CANDIDATE_COMMIT
        + "/%2E%2E/main/contracts/protected_target_v2.py",

        SOURCE_PREFIX
        + CANDIDATE_COMMIT
        + "/contracts\\..\\protected_target_v2.py",

        SOURCE_PREFIX
        + CANDIDATE_COMMIT
        + "/contracts//protected_target_v2.py",

        SOURCE_PREFIX
        + CANDIDATE_COMMIT
        + "/contracts/protected%5ftarget_v2.py",

        SOURCE_PREFIX
        + CANDIDATE_COMMIT
        + "/contracts/protected target_v2.py",

        SOURCE_PREFIX
        + CANDIDATE_COMMIT.upper()
        + "/contracts/protected_target_v2.py",
    )

    for index, bad_url in enumerate(bad_candidate_urls):
        with direct_vm.expect_revert(
            "Candidate source URL is not an approved immutable source"
        ):
            governor.create_proposal(
                _address_arg(direct_bob),
                "2.0.0",
                bad_url,
                CANDIDATE_BYTES,
                CI_URL,
                f"ci-candidate-canon-{index:03d}",
                AUDIT_URL,
                f"audit-candidate-canon-{index:03d}",
            )


def test_evidence_url_canonicalization_aliases_are_rejected(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
):
    governor = direct_deploy("contracts/proofpatch_governor.py")
    _register(
        governor,
        direct_vm,
        direct_bob,
        direct_alice,
    )

    direct_vm.sender = direct_alice

    bad_ci = (
        CI_PREFIX
        + CI_COMMIT
        + "/../main/evidence/ci.json"
    )

    with direct_vm.expect_revert(
        "CI evidence URL is not an approved immutable source"
    ):
        governor.create_proposal(
            _address_arg(direct_bob),
            "2.0.0",
            CANDIDATE_URL,
            CANDIDATE_BYTES,
            bad_ci,
            "ci-canon-bad-001",
            AUDIT_URL,
            "audit-canon-good-001",
        )

    bad_audit = (
        AUDIT_PREFIX
        + AUDIT_COMMIT
        + "/%2e%2e/main/evidence/audit.json"
    )

    with direct_vm.expect_revert(
        "Audit evidence URL is not an approved immutable source"
    ):
        governor.create_proposal(
            _address_arg(direct_bob),
            "2.0.0",
            CANDIDATE_URL,
            CANDIDATE_BYTES,
            CI_URL,
            "ci-canon-good-002",
            bad_audit,
            "audit-canon-bad-002",
        )
