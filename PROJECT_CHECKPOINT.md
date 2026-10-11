# SCA-3 V1 — Phase 2 Continuation Checkpoint

Repository A: https://github.com/halihalibt/semantic-cycle-accord-genlayer
Account: halihalibt; PUBLIC; MIT retained. Sole target: Stable Studionet 61999,
https://studio.genlayer.com/api. Original Phase 1 PR #1 is merged at authoritative
main baseline cc773e936cf6184d0b3f9447771ac804e597bfe7.

Work branch: phase2-consensus-core. Main is not modified. Draft PR publication
identifiers are added after the verified implementation commit is published.
Canonical path: contracts/semantic_cycle_accord.py.
SHA256: 88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442
Prompt: SCA3-CANONICAL-CLASSIFICATION-V1
Prompt SHA256: 8a7b279a3594397802c71fef4df9b4d30db1ff528177d0bf05c80a62397192d3

## Frozen implementation and acceptance

Phase 2 implements actual pinned custom run_nondet_unsafe Leader/Validator and
native exec_prompt JSON mode; every valid Leader result requires independent
complete three-edge classification by the Validator and exact positional equality.
Production closures capture prompt text only. Error wrappers/invalid vectors cannot
authorize acceptance. Exactly all FIT creates MATCHED/PENDING; other valid vectors
persist NOT_MATCHED with cycle_id=0 and unchanged OPEN Intents. Unchanged negative
snapshots cannot fish for a new verdict; versions/rotations/direction retain frozen
identity rules. Caller must be an actual participant. Pre/post-VM preflight and
snapshot/counter/replay checks remain mandatory. No public supplied verdict exists.

Three participant confirmations still produce ACTIVE/exactly three CONSUMED.
ACTIVE means accepted commitment, never delivered service. INV-01–16 and original
method behavior/field prefix remain intact. New typed assessment fields are appended.
Read API: 7 WRITE / 7 VIEW, original 12 plus assess_cycle/get_assessment only.
get_protocol_stats adds assessment_total and true availability without relabeling
historical fixture cycles as assessments.

Actual complete validation: 505 PASS / 0 FAIL / 0 SKIP / applicable NOT RUN 0.
229 baseline cases reproduced before edits and retained/adapted; 276 new cases.
GenVM AST lint (3), SDK semantic validation, exact schema and Ruff lint/format PASS.
Native captured Validator calls, bundled cloudpickle, stored-byte reconstruction,
calldata and original Phase 1 byte compatibility/resumed activation PASS.
Toolchain unchanged: Python 3.12.14, GenVM v0.2.16, genlayer-test 0.29.2,
genvm-linter 0.11.0, pytest 9.1.1, Ruff 0.14.0 and original uv.lock.

## Authoritative reads for a fresh conversation

Read README.md, WORK_MASTER_PLAN.md, docs/PROTOCOL_SPEC.md,
docs/STATE_MACHINE.md, docs/DETERMINISTIC_INVARIANTS.md,
docs/STABLE_COMPATIBILITY.md, docs/CANONICAL_CLASSIFICATION_PROMPT_V1.md,
docs/CONSENSUS_AND_EQUIVALENCE_V1.md, docs/PHASE_2_TEST_AND_ACCEPTANCE.md,
docs/PHASE_2_REPORT.md, canonical contract/all tests and evidence/phase2/*.json.
Phase 1 documents/evidence are historical and preserved; they do not override
this newly authorized Phase 2 boundary. Their old unmerged/unimplemented status
statements describe the checkpoint when written, not current repository status.

## Reproduce and limitations

uv sync --frozen
uv run python scripts/bootstrap_sdk.py
uv run python scripts/verify_local.py

Tests block sockets and retain local git history for the baseline-layout check.
Direct Mode runs Leader then captures the Validator without enforcing real votes;
vm.run_validator explicitly tests the actual production callback with separate
native mocks. Canned classification fixtures do not measure model accuracy.
Predictable/record-allocation/preflight failures preserve bytes without rollback;
three unexpected storage-fault tests explicitly simulate a transaction boundary.
Full WASM rollback, live consensus/finality, model accuracy, races and cross-platform
execution remain NOT RUN. No deployment or transaction occurred; no wallet secret
was accessed. Structured data boundaries do not prove prompt-injection immunity.

## Mandatory stop

After verified Draft PR publication, STOP. Await independent review. Do not merge,
start Phase 3, create Repository B/frontend, deploy, transact, sign, change toolchain
or network, use paid external AI or enter Portal without new explicit authorization.
