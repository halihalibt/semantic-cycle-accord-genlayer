# SCA-3 V1 — Phase 3 Test and Acceptance

The starting suite was executed unchanged before production edits: **505 PASS /
0 FAIL / 0 SKIP**. No production edit was subsequently justified. Every original
module and test node remains unchanged. Final results and full collected node list
are in evidence/phase3/local-results.json and collected-tests.txt.

Added **61 targeted cases** in tests/security/test_phase3_closure.py:

| Added cases | Gap covered |
| --- | --- |
| 27 | Actual SDK byte-write faults at first/middle/last positions of 9 transitions, partial-state visibility and explicit manual restoration |
| 8 | Integer/type boundaries across 9 public record paths; SDK float encoding vs method integer validation |
| 5 | Malformed topology containers reject before any native LLM call |
| 5 | Maximum valid 512-byte fields with JSON/control/delimiter expansion and independent negative mock agreement |
| 4 | Unicode controls and multilingual fake-role strings in each service field |
| 1 | Fixed seed 61999, 12 version updates, all rotations equal and reversal distinct |
| 1 | All 7 views, repeated reads, detached-result mutation and unchanged authoritative bytes |
| 1 | Explicit version-change negative retry design limit |
| 1 | Corrupted owner fails ownership/snapshot checks without changes |
| 7 | Invalid text across create/update and all 4 fields, including SDK UTF-8 boundary |
| 1 | All pagination integer boundaries and malformed address representations |

Total: **566 PASS / 0 FAIL / 0 SKIP / applicable NOT RUN 0** in the complete
local suite. Pytest plugin autoload disabled, native sockets blocked in test
fixtures. No test deleted, bypassed or skipped. Fixed Python/uv.lock retained.
Ruff lint/format, 3 GenVM AST checks, SDK semantic validation, exact 14-method
schema, frozen prompt/hash, storage serialization, calldata and actual Phase 1
byte-layout reconstruction all passed.

## Reproduce ordinary checks

```bash
uv sync --frozen
uv run python scripts/bootstrap_sdk.py
uv run python scripts/verify_local.py
uv run python scripts/measure_phase3_resources.py
```

Retain local git history for the original Phase 1 byte-layout test. The resource
probe blocks TCP, records local Python memory/SDK storage counts, and has no gas
estimation or paid AI call. Measurements are sample observations, not benchmark
promises across systems. Original historical evidence directories are untouched.

## Reproduce isolated native WASM smoke

Prepare one local directory containing extracted official v0.2.16 artifacts:

- genvm-universal.tar.xz (SHA256 4f0b358ec98ec148be9b95cdfb0f0e1a6cbe64da0194fdfac3fffc6f5d1d93e2): runners/
- genvm-linux-amd64.tar.xz (SHA256 0e16aa26a4f70a5198eeca819a62516775a793ec96bcab4eb3f8544b55e7e75c): lib/
- genvm-linux-amd64-executor.tar.xz (SHA256 0d060cf4cceba4adf6a0dd886225be7a500ebbc2eb474c462a98a9743aa641ab): executor/v0.2.16/

Download from the official release at
https://github.com/genlayerlabs/genvm/releases/tag/v0.2.16 only if needed.
Keep the two Linux archives in that directory; the smoke script verifies their
checksums. bootstrap_sdk already verifies the universal SDK artifact. Binary
startup uses its own bundled musl loader without modifying system libraries.

```bash
uv run python scripts/offline_wasm_smoke.py --bundle /path/to/extracted-v0.2.16 --output evidence/phase3/offline-wasm-results.json
```

Actual invocation/outputs are retained. Four genuine native runs PASS: constructor,
protocol view, deterministic create, persisted Intent view. No fees, RPC, signing,
network, alternate blockchain, external AI or onchain state were involved.

## Evidence levels and excluded work

| Area | Result / evidence level |
| --- | --- |
| Original 505 tests | Actual reproduced PASS before additions |
| Complete current pytest suite | 566 PASS, Direct Mode / offline tooling |
| Four native WASM runs | PASS, actual v0.2.16 isolated executor, disposable host state |
| Predictable validation failures | Bytes unchanged without restoration |
| Unexpected byte-write faults | Partial Direct Mode state observed; manual restore only |
| Automatic node transaction rollback | NOT TESTED / NOT RUN, no supported standalone rollback test method |
| Production assessment/Validator full WASM | NOT RUN |
| Real model accuracy or injection resistance | NOT TESTED; mocked expected responses only |
| Real Stable consensus, concurrency and finality | NOT RUN |
| Live deployment, writes, wallet signatures | NOT RUN / unauthorized in this phase |
| Cross-platform, frontend, Repository B, Portal | NOT RUN / excluded |

These excluded checks are not skipped applicable pytest cases. No confirmed
critical/high defect remains locally. DESIGN LIMITATION and NOT TESTED findings
remain visible in the audit. Local closure enables consideration of a future
separately authorized deployment-preflight; it does not authorize deployment.
