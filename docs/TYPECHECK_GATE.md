# ProofPatch typecheck gate

ProofPatch uses two typecheck layers:

1. Readable contracts use `genvm-lint typecheck <contract>` as a **hard gate**. This is GenLayer's normal Pyright workflow and suppresses known SDK-internal dynamic-attribute/NewType noise.
2. Generated `*_compact.py` deployment artifacts use the same JSON diagnostic gate with an explicit allowlist for minification-only static typing diagnostics. GenVM semantic lint, schema generation, source parity, and Direct Mode still apply to every compact artifact; undefined names and any unclassified error/warning remain hard failures.
3. `genvm-lint typecheck <contract> --strict --json` is a **mandatory strict audit**. ProofPatch stages every strict diagnostic in memory, runs the complete Direct Mode suite, then archives the strict audit under `artifacts/strict-typecheck/` only after tests pass. Errors or warnings remain hard failures for readable sources, and only the documented compact allowlist is archived as information.

## Why the wrapper exists

The project pins `genvm-linter` commit `fa4a4d4536b28fdc2730e13a983ba01b69ccc6f3` (`0.10.0`). In that version, the CLI's strict typecheck exits non-zero whenever the contract has *any* Pyright diagnostic, even informational strict-mode diagnostics. This can produce a human summary of `0 error(s), 0 warning(s)` while still returning exit code 1.

ProofPatch does not disable strict checking. `scripts/preflight.py` consumes the strict JSON output, normalizes numeric/string Pyright severity encodings, stages all informational diagnostics, fails on errors/warnings, and fails conservatively if an unknown severity encoding appears. Compact artifacts keep their deployed bytes; adding readable-source suppression comments would invalidate exact source parity, so the allowlist is applied to structured diagnostics instead.

`genlayer-test` clears the repository `artifacts/` directory when Direct Mode starts. To prevent a passing preflight manifest from pointing at files that the test runner deleted, strict-audit JSON is promoted into `artifacts/strict-typecheck/` only after the Direct Mode suite succeeds. `artifacts/local-preflight.json` is written last and includes SHA-256 hashes for the promoted strict-audit files.

This keeps the build gate strict without misclassifying SDK/dynamic-type information as a contract failure, and keeps reviewer evidence intact after a successful full preflight.
