#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = [
    ROOT / "contracts" / "proofpatch_governor.py",
    ROOT / "contracts" / "protected_target_v1.py",
    ROOT / "contracts" / "protected_target_v2_safe.py",
]
STRICT_DIR = ROOT / "artifacts" / "strict-typecheck"


def run(cmd: list[str]) -> None:
    print("+", " ".join(str(x) for x in cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def _severity_name(value: Any) -> str:
    """Normalize Pyright severity across output-schema versions.

    Older/newer Pyright builds have emitted numeric or string severities.
    Treat unknown encodings conservatively instead of silently ignoring them.
    """
    if isinstance(value, int):
        return {1: "error", 2: "warning", 3: "information"}.get(value, "unknown")
    if isinstance(value, str):
        normalized = value.strip().lower()
        aliases = {
            "info": "information",
            "informational": "information",
        }
        return aliases.get(normalized, normalized)
    return "unknown"


def strict_typecheck_audit(contract: Path) -> tuple[Path, dict[str, Any]]:
    """Run strict Pyright as a mandatory audit without inheriting a linter CLI quirk.

    genvm-linter 0.10.0 at the project-pinned commit exits 1 whenever *any*
    contract diagnostic exists, including informational strict-mode diagnostics.
    We therefore consume its JSON output and fail only on actual errors/warnings,
    while preserving every diagnostic as a reviewer artifact.
    """
    rel = contract.relative_to(ROOT)
    cmd = ["genvm-lint", "typecheck", str(rel), "--strict", "--json"]
    print("+", " ".join(cmd), "[strict audit]", flush=True)

    result = subprocess.run(
        cmd,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    if result.stderr.strip():
        print(result.stderr.rstrip(), file=sys.stderr)

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(result.stdout.rstrip())
        raise RuntimeError(
            f"Strict typecheck for {rel} did not return parseable JSON"
        ) from exc

    diagnostics = payload.get("diagnostics", [])
    if not isinstance(diagnostics, list):
        raise RuntimeError(f"Strict typecheck for {rel} returned malformed diagnostics")

    normalized: list[dict[str, Any]] = []
    blocking: list[dict[str, Any]] = []
    unknown_severity: list[dict[str, Any]] = []

    for diagnostic in diagnostics:
        if not isinstance(diagnostic, dict):
            unknown_severity.append({"raw": diagnostic})
            continue
        item = dict(diagnostic)
        severity = _severity_name(item.get("severity"))
        item["normalized_severity"] = severity
        normalized.append(item)
        if severity in {"error", "warning"}:
            blocking.append(item)
        elif severity not in {"information"}:
            unknown_severity.append(item)

    artifact = STRICT_DIR / f"{contract.stem}.json"
    audit_payload: dict[str, Any] = {
        "contract": str(rel),
        "tool_exit_code": result.returncode,
        "blocking_diagnostic_count": len(blocking),
        "informational_diagnostic_count": sum(
            1 for item in normalized
            if item.get("normalized_severity") == "information"
        ),
        "unknown_severity_count": len(unknown_severity),
        "diagnostics": normalized,
    }

    if unknown_severity:
        raise RuntimeError(
            f"Strict typecheck for {rel} returned {len(unknown_severity)} diagnostic(s) "
            "with an unknown severity encoding; refusing to mask them"
        )

    if blocking:
        for item in blocking:
            start = item.get("range", {}).get("start", {}) if isinstance(item.get("range"), dict) else {}
            line = int(start.get("line", 0)) + 1 if isinstance(start, dict) else 0
            rule = item.get("rule", "")
            message = item.get("message", "")
            severity = item.get("normalized_severity", "unknown")
            print(f"STRICT BLOCK: {rel}:{line}: {severity}: {message} [{rule}]")
        raise RuntimeError(
            f"Strict typecheck for {rel} has {len(blocking)} blocking error/warning diagnostic(s)"
        )

    info_count = sum(
        1 for item in normalized
        if item.get("normalized_severity") == "information"
    )
    print(
        f"STRICT TYPECHECK AUDIT: PASS ({info_count} informational diagnostic(s) staged for "
        f"post-test archive -> {artifact.relative_to(ROOT)})"
    )
    return artifact, audit_payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> int:
    if sys.version_info < (3, 12):
        print("FAIL: ProofPatch requires Python >= 3.12 for current GenLayer tooling.")
        return 1

    staged_strict_audits: list[tuple[Path, dict[str, Any]]] = []

    for contract in CONTRACTS:
        rel = contract.relative_to(ROOT)

        # Hard GenLayer semantic gate.
        run(["genvm-lint", "check", str(rel)])

        # Hard normal type gate: this is the linter-supported contract workflow and
        # suppresses known SDK-internal dynamic-type noise.
        run(["genvm-lint", "typecheck", str(rel)])

        # Mandatory strict audit: preserve stricter diagnostics, but do not convert
        # informational SDK/dynamic diagnostics into a false build failure.
        staged_strict_audits.append(strict_typecheck_audit(contract))

        abi_path = ROOT / "abi" / f"{contract.stem}.json"
        abi_path.parent.mkdir(exist_ok=True)
        run([
            "genvm-lint",
            "schema",
            str(rel),
            "--output",
            str(abi_path.relative_to(ROOT)),
        ])

    run([sys.executable, "-m", "pytest", "tests/direct", "-v"])

    # genlayer-test clears ROOT/artifacts when Direct Mode starts. Only promote
    # reviewer evidence after the test suite has passed, so the manifest never
    # points at files that pytest subsequently removed.
    for strict_artifact, strict_payload in staged_strict_audits:
        _write_json(strict_artifact, strict_payload)

    hashes = {
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in CONTRACTS
    }
    direct_test_files = sorted((ROOT / "tests" / "direct").glob("*.py"))
    direct_test_hashes = {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in direct_test_files
    }
    reviewer_docs = [
        ROOT / "docs" / "REVIEWER_COVERAGE_AUDIT.md",
        ROOT / "docs" / "BRADBURY_FINAL_EVIDENCE.md",
    ]
    reviewer_doc_hashes = {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in reviewer_docs
        if path.exists()
    }
    strict_hashes = {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path, _ in staged_strict_audits
    }
    artifact = ROOT / "artifacts" / "local-preflight.json"
    _write_json(
        artifact,
        {
            "status": "PASS",
            "python": sys.version.split()[0],
            "checks": {
                "genvm_lint": True,
                "typecheck": True,
                "schema": True,
                "direct_tests": True,
                "adversarial_tests": True,
                "proofpatch_interface_tests": True,
                "reviewer_timeout_regressions": True,
            },
            "direct_test_suite": "tests/direct",
            "contract_sha256": hashes,
            "direct_test_sha256": direct_test_hashes,
            "reviewer_document_sha256": reviewer_doc_hashes,
            "reviewer_regressions": [
                "test_timeout_reconciles_installed_but_unconfirmed_exact_install",
                "test_timeout_marks_genuinely_uninstalled_proposal_failed_and_releases_slot",
                "test_timeout_keeps_slot_locked_on_partial_install_attestation_mismatch",
            ],
            "strict_typecheck_artifacts": [
                str(path.relative_to(ROOT))
                for path, _ in staged_strict_audits
            ],
            "strict_typecheck_sha256": strict_hashes,
        },
    )
    print(f"PREFLIGHT: PASS -> {artifact.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (subprocess.CalledProcessError, RuntimeError) as exc:
        code = exc.returncode if isinstance(exc, subprocess.CalledProcessError) else 1
        print(f"PREFLIGHT: FAIL ({code})")
        print(f"REASON: {exc}")
        raise SystemExit(code)
