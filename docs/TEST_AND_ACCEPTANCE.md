# Phase 1 Test and Acceptance Record

Final locked-environment execution: **176 PASS / 0 FAIL / 0 SKIP**.
No applicable deterministic test is NOT RUN. Real deployment, network-backed
integration, semantic consensus, frontend and transaction tests are NOT RUN
because they are outside Phase 1. No assessment or onchain success is inferred.

## Reproduction

```bash
uv sync --frozen
uv run python scripts/bootstrap_sdk.py
uv run python scripts/verify_local.py
```

Equivalent individual checks after bootstrap:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/python -m pytest -q
.venv/bin/ruff check contracts tests scripts
.venv/bin/ruff format --check contracts tests scripts
GENVM_VERSION=v0.2.16 .venv/bin/genvm-lint check contracts/semantic_cycle_accord.py --json
GENVM_VERSION=v0.2.16 .venv/bin/genvm-lint schema contracts/semantic_cycle_accord.py --json
```

The cross-platform Python verification script sets environment variables itself.
Every contract fixture uses `sdk_version='v0.2.16'`; pytest plugin autoload is
disabled to avoid the test package's default network configuration. Test socket
connections are blocked. No Studio deploy fixture or simulated network is used.

## Required matrix

| Category | Executed coverage |
| --- | --- |
| A — Intent validation | Valid create, mandatory whitespace/empty text, all-field 512-byte ASCII/Unicode boundaries, overlong input, 1–30 day boundaries, owner capacity and logical expiration, owner-only update/cancel, versions, reserved/terminal mutation rejection |
| B — Topology | Directed ring, cardinality, duplicate ID/owner, self-loop, missing/repeated/wrong edges, stale versions, expired/unavailable records, rotation normalization and reversed direction |
| C — Snapshot safety | Full frozen contents, canonical Unicode JSON, versions and all term changes, domain/direction identity, altered stored terms/metadata, supplied hash insufficiency, preflight before final activation |
| D — State transitions | Controlled internal reservation, zero/one/two/three confirmations, duplicate/unrelated confirmation, decline, reserved cancellation, 72-hour/earliest expiry, owned reservation release, terminal immutability, state isolation and failed-operation atomicity |
| E — Replay/resources | Duplicate and rotated proposals, shared reservations/consumption, repeated decline/expiration, declined snapshot across callers and version change, expired snapshot replay, overflows, history exceeding one page, bounded service/page inputs |
| F — Reads/storage | Missing IDs, owner histories, page limits/boundaries, effective/cumulative statistics, Intent/Cycle state consistency, every view's calldata result roundtrip, transaction clock, root/cloudpickle and persisted-byte reconstruction |

Per-file counts and source digest are recorded in `evidence/phase1/local-results.json`.
Invariant mapping is in `DETERMINISTIC_INVARIANTS.md`.

## Other checks

| Check | Actual final result |
| --- | --- |
| GenVM AST lint | PASS; 3 checks passed, zero warnings |
| SDK semantic validation | PASS; canonical class, 12 methods, zero constructor parameters |
| SDK schema export | PASS; exactly 6 writes and 6 views; no private seam exposed |
| Ruff source lint | PASS; all checks passed |
| Ruff format | PASS; all 10 Python files formatted |
| Locked dependency reproduction | PASS; `uv sync --frozen` environment ran the complete suite |
| Storage/cloudpickle and fresh-root byte restoration | PASS; included in executed tests |
| Stable eth_chainId metadata | PASS; 61999; read-only environment check |

## Failures resolved without weakening acceptance

The first 154-test run had 153 passes and one failure: standard pickle could
not encode the SDK-generated descriptors. The root roundtrip uses the actual
SDK-bundled cloudpickle; byte-storage pickle/rebinding and isolated continued
activation remain required assertions. The 154-test rerun passed completely.

Additional tests initially revealed a nested test-context loading error in the
wrong-network constructor test. That test now uses a separate VM context and
asserts actual constructor rejection. A missing-record cleanup preflight was
also added to verify failure cannot release earlier records partially.

The initial linter rejected `u64` map-key annotations. They were replaced with
supported `u256` annotations while preserving the 64-bit ID limit. No warning
was suppressed. No test was deleted, skipped or relaxed to invent a PASS.

## Acceptance boundary

The public API cannot create Cycles in Phase 1. Offline fixtures exercise the
private accepted-result seam to test deterministic consequences. This proves
neither natural-language compatibility nor Validator agreement. The phase
is a tested deterministic checkpoint suitable for separate Phase 2 review,
not a deployed or production-ready application.
