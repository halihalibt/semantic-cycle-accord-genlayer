# SCA-3 V1 — Phase 1 Acceptance Report

## Current limited hardening amendment

The three authorized corrections are complete: pre-mutation ACTIVE counter
validation; centralized ABORTED/EXPIRED counter preflight including the decline
marker ordering; and machine-checked schema validation in verify_local.py.
The canonical source changed only by ten added lines. No protocol version,
storage schema, signatures, ring rules, snapshot identity or AI logic changed.

Starting branch HEAD: `f70005c0251dc1a6dfb0752a8037941e7c65065e`.
Patched implementation commit is recorded in evidence/phase1/publication.json;
the latest reporting HEAD is the existing Draft PR's head_sha.
Original canonical SHA256: `628742fbceec1e8e343dc35bd2f15b78b286e7953eaaf725b5597f139fff1306`.
Current canonical SHA256: `8a44df900eb2e286e1a035db4e7496c8923b8c7e9389dbccaf40c98a68e7c48c`.

Full regression: **229 PASS / 0 FAIL / 0 SKIP / applicable NOT RUN 0**.
All 176 original cases retained; 53 new cases (9 counter cases, 44 schema cases).
GenVM v0.2.16 lint: 3 PASS, zero warnings; SDK semantic validation: 12 methods.
Schema: PASS, exactly 6 writes and 6 views, no private or AI entry point.
Ruff lint and format: PASS, 11 Python files. Locked dependencies unchanged.

Evidence: local-results.json preserves the original 176-test record, names all
new cases and records the actual current digest/results. genvm-check.json and
schema.json are regenerated from the pinned toolchain; hardening-verification.txt
records the observed complete verification result. No RPC request was sent in
this amendment. The prior metadata check below is historical.

No remaining patch blocker. Ready for independent Phase 1 review and merge
approval; PR remains Draft and unmerged. Full WASM, deployment and consensus
remain outside this patch and unverified. No Phase 2 work is authorized.

The original implementation report follows for historical provenance.

## Original implementation result

Deterministic Phase 1 implementation is complete and locally verified. The
checkpoint is for review on `phase1-deterministic-core`; main is not merged.
Tested implementation commit: `76f0b6ba8515132a6468ad5f9f67067fb932861d`.
Draft PR: https://github.com/halihalibt/semantic-cycle-accord-genlayer/pull/1 — OPEN, DRAFT, NOT MERGED.
Publication metadata is in `evidence/phase1/publication.json`. A reporting-only
follow-up records these IDs without changing tested source or tests. No fabricated URL, hash, deployment or
consensus claim is used.

Repository: https://github.com/halihalibt/semantic-cycle-accord-genlayer
Owner: halihalibt. Visibility: Public. License: MIT, original attribution retained.
Initial main HEAD: `98784894a470c31ca1ebe2e075092582bb88403e`.

## Original implementation verification

| Check | Actual result |
| --- | --- |
| Deterministic suite, locked environment | 176 PASS, 0 FAIL, 0 SKIP; applicable NOT RUN 0 |
| Required A–F matrix | Executed; see TEST_AND_ACCEPTANCE.md |
| Storage serialization, byte restoration, resumed activation | PASS, included in suite |
| Public-method calldata roundtrips | PASS, included in suite |
| GenVM AST lint | PASS, 3 checks, zero warnings |
| Fixed SDK semantic validation | PASS, 12 methods, 0 constructor parameters |
| Schema export | PASS, 6 writes / 6 views; private seam absent |
| Ruff lint / format | PASS; 10 Python files formatted |
| Stable metadata | Read-only eth_chainId = 0xf22f = 61999 |
| Real deployment / transactions / consensus | NOT RUN, prohibited in Phase 1 |

Validated versions: Python 3.12.14, official GenVM v0.2.16 runner/stdlib,
genlayer-test 0.29.2, genvm-linter 0.11.0, pytest 9.1.1, Ruff 0.14.0.
The SDK-bundled cloudpickle dependency is 3.1.0.dev0 with an exact frozen
content identity. It is not a newly selected tooling or network release candidate.
genlayer-js 1.1.8 is a JavaScript reference, not a Python contract SDK; it is
not used in this phase. Exact identities/checks are in STABLE_COMPATIBILITY.md.

Reproduction: `uv sync --frozen`, `uv run python scripts/bootstrap_sdk.py`, then
`uv run python scripts/verify_local.py`. Actual machine-readable final results,
source digest, schema and linter output are in `evidence/phase1/`.

## Delivered implementation

Writes: create_intent, update_intent, cancel_intent, confirm_cycle, decline_cycle,
expire_cycle. Views: get_intent, get_cycle, get_intents_page, get_cycles_page,
get_owner_records, get_protocol_stats. INV-01 through INV-16 are mapped to actual
enforcement and executed tests in DETERMINISTIC_INVARIANTS.md.

The canonical contract uses correctly declared persistent maps/arrays/dataclasses,
fixed-width counters/versions/timestamps, exact full conditions snapshots,
direction-preserving proposal identity, owner controls, five unfinished Intent
slots, bounded histories, state preflights, terminal consumption, isolated
reservation release, deadlines and permanent duplicate/declined replay protection.

The accepted-result seam has no public call path. No AI classification,
Leader/Validator code, prompt, equivalence engine or fake assessment record is
implemented. Local fixture PENDING/ACTIVE Cycles are explicitly simulated
deterministic states, not real matching or onchain evidence.

## Files delivered

- Canonical contracts/semantic_cycle_accord.py.
- tests/conftest.py and deterministic, security and state-machine test modules.
- scripts/bootstrap_sdk.py and scripts/verify_local.py.
- pyproject.toml, uv.lock and .gitignore.
- Updated README.md; retained LICENSE.
- docs/PROTOCOL_SPEC.md, STATE_MACHINE.md, DETERMINISTIC_INVARIANTS.md,
  STABLE_COMPATIBILITY.md, TEST_AND_ACCEPTANCE.md and PHASE_1_REPORT.md.
- WORK_MASTER_PLAN.md and PROJECT_CHECKPOINT.md.
- evidence/phase1/ execution and publication records.

No other repository was modified. No frontend, Repository B or deployment
package was created. No private keys, wallet credentials or signatures were
read, stored or requested. Development used no paid service.

## Risks, limitations and Phase 2 readiness

No unresolved critical deterministic blocker remains. Compatibility is proven
at pinned SDK/Direct Mode/schema level, not through full GenVM WASM execution,
real Validator consensus, live race/concurrency behavior or onchain finality.
Intent services remain unverified until legitimate Phase 2 semantics exist.
Persistent history/replay indexes grow with activity, while each public operation
remains bounded. Effective global statistics require aggregating pages under
the same timestamp; page counts are explicitly named to prevent misinterpretation.

Ordinary pickle cannot serialize dynamic SDK descriptors; the fixed runtime's
own cloudpickle passes, with independent persisted-byte reconstruction. Python
3.12.14 on this environment is verified; cross-platform execution is not claimed.

**Ready for separate Phase 2 review, subject to explicit approval.** This is
not a production-readiness or onchain-success conclusion. Phase 2, merge,
deployment, transactions, signing, Repository B, frontend and Portal remain
unauthorized. Execution stops after publishing this Phase 1 Draft checkpoint.
