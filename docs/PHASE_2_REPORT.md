# SCA-3 V1 — Phase 2 Report

Local implementation/validation is complete. GitHub Draft publication identifiers
will be added after the verified implementation commit is published.

| Identity / check | Actual value |
| --- | --- |
| Repository A | https://github.com/halihalibt/semantic-cycle-accord-genlayer |
| Authenticated account / visibility | halihalibt / PUBLIC / MIT |
| Work branch | phase2-consensus-core; main untouched |
| Starting main | cc773e936cf6184d0b3f9447771ac804e597bfe7; Phase 1 PR #1 merged |
| Canonical source | contracts/semantic_cycle_accord.py |
| Source SHA256 | 88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442 |
| Prompt identifier | SCA3-CANONICAL-CLASSIFICATION-V1 |
| Prompt SHA256 | 8a7b279a3594397802c71fef4df9b4d30db1ff528177d0bf05c80a62397192d3 |
| Tests | 505 PASS / 0 FAIL / 0 SKIP / applicable NOT RUN 0 |
| Baseline | 229 reproduced before changes; retained/adapted; no deletion/skip |
| New coverage | 276 cases: 272 new-module cases plus 4 expanded schema parameters |
| GenVM v0.2.16 | AST lint 3 PASS, SDK validation PASS, 14 methods, zero constructor parameters |
| Schema | Exactly 7 writes / 7 views; strict readonly checks PASS |
| Ruff | Lint and format PASS, 17 Python files |
| Storage / calldata | Root/bytes/restored assessment/resumed activation/calldata PASS; actual Phase 1 bytes remain readable |

## Implemented behavior

Leader: deterministic preflight freezes canonical three-edge input; a closure
capturing only immutable prompt text calls native exec_prompt in pinned JSON
mode, strictly validates the exact object and returns only three labels.

Validator: accepts only the actual Return wrapper with a structurally valid
Leader vector, independently calls the native LLM on the same full input,
strictly parses its own result and compares all three positions. Errors/malformed
values reject. No convenience equivalence wrapper, leader-comparative prompt,
score threshold, administrator, fake voting or external verdict setter exists.

Equivalence is Full Three-Edge Decision Equivalence. A matching NOT_MATCHED vector
can have Validator agreement; agreement is distinct from business acceptance.
Exactly three FIT labels create MATCHED plus PENDING through the existing private
reservation seam. Other vectors persist NOT_MATCHED, cycle_id=0, original labels
and reconstructable snapshot without reserving Intents. Negative replay blocks
unchanged snapshots across callers/rotations before LLM. Meaningful version updates
and reversed assignment create distinct snapshots under frozen Phase 1 rules.

assess_cycle repeats authoritative preflight, exact snapshot/caller/replay/counter
checks after accepted output. Complete local Assessment allocation precedes writes.
All original deterministic methods/signatures/field prefix and INV-01–16 are
retained; only the private seam's documentation and stats availability/count
change. Public methods are the original six writes/six views plus assess_cycle
(WRITE) and get_assessment (VIEW). Assessments do not fabricate finality or votes.

## Verification and limits

The fixed v0.2.16 artifact was checksum verified and custom API probed before
production edits. Native JSON dict responses, Return/UserError/VMError forms,
separate captured Validator execution, malformed responses and exceptions passed.
No SDK, Python, dependency lock or target network was upgraded.

The 505-case suite tests all 27 label vectors, prompt/hash/order/UTF-8/data
boundaries, independent native mocked Validator execution, exact schema security,
pre/post-consensus safety, replay, counters, allocations, lifecycle and storage.
Thirteen semantic fixtures document intended FIT/NO_FIT/UNSURE expectations and
scope/quantity/format/language/deadline/missing/exclusion cases; they are canned
LLM orchestration tests, not proof of real-model classification accuracy.

Predictable errors and local-record/reservation-preflight failures preserve actual
serialized storage **without rollback**. Three unexpected persistence faults are
verified only through explicitly simulated Direct Mode snapshot/revert transaction
boundaries. Production relies on GenVM transactional rollback for runtime failures
inside multi-record writes, as Phase 1 does. Full WASM rollback is **NOT RUN**.

Direct Mode runs the Leader then captures the Validator; it does not gate state
writes on network consensus. Actual captured callbacks are executed using
vm.run_validator with independently swapped native mocks. VM termination is
separately fault injected, not a replacement fake voting mechanism.

Remaining excluded NOT RUN: full WASM, real model accuracy, network consensus,
live concurrency, deployment/transactions/finality, cross-platform execution,
frontend/Repository B/Portal. Independent re-execution cannot rule out systematic
model errors or prompt injection. No applicable authorized local test is unresolved.
No critical local implementation blocker remains; Phase 3 may be considered only
after independent review and separate explicit authorization.

## Files and reproducibility

Changed original files: contracts/semantic_cycle_accord.py, scripts/verify_local.py,
tests/deterministic/test_reads_storage.py, tests/security/test_integrity.py,
tests/security/test_verify_local.py, README.md, WORK_MASTER_PLAN.md,
docs/PROTOCOL_SPEC.md and PROJECT_CHECKPOINT.md.

Added: docs/CANONICAL_CLASSIFICATION_PROMPT_V1.md,
docs/CONSENSUS_AND_EQUIVALENCE_V1.md, docs/PHASE_2_TEST_AND_ACCEPTANCE.md,
docs/PHASE_2_REPORT.md; tests/consensus/__init__.py, test_prompt_parser.py,
test_validators.py, test_semantic_fixtures.py, classification-fixtures.json;
tests/integration/test_assessments.py; tests/security/test_consensus_safety.py;
evidence/phase2/ baseline-verification.txt, stable-api-probe-source.txt,
stable-api-probe.json, verification.txt, genvm-check.json, schema.json,
local-results.json and publication.json (added after publication).

Phase 1 evidence and historical report/specs remain byte-for-byte unchanged;
uv.lock, pyproject.toml, bootstrap and SDK identities are unchanged.

Reproduce uv sync --frozen, uv run python scripts/bootstrap_sdk.py, then
uv run python scripts/verify_local.py. Keep local git history for the frozen
Phase 1 byte-layout test. Per-file counts and every node ID are in local-results.

No deployment, blockchain transaction, wallet signing/credential access, paid
external AI, alternate network, Repository B, frontend, PR merge or Portal work
occurred. Phase 2 publication is the sole remaining step; execution then STOPs.
