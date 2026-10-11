# SCA-3 V1 — Phase 1 Checkpoint

## Identity and baseline

- Repository A: https://github.com/halihalibt/semantic-cycle-accord-genlayer
- Owner: `halihalibt`; visibility PUBLIC; MIT License retained.
- Work branch: `phase1-deterministic-core`; target base: `main`.
- Initial main baseline: `98784894a470c31ca1ebe2e075092582bb88403e`.
- Main contained only the new project's README and MIT License; no unrelated work.
- Publication identifiers are recorded in `evidence/phase1/publication.json`
  after the implementation commit is created. The draft PR's head is the latest
  checkpoint; any reporting-only follow-up does not change the tested source.

## Current acceptance

Phase 1 deterministic implementation and local verification are complete.
**176 PASS / 0 FAIL / 0 SKIP**, storage serialization/reconstruction and calldata
checks included. Ruff and pinned GenVM lint/semantic/schema checks passed.
There is no deployment, consensus result, contract address, transaction hash,
wallet signature, frontend, Repository B, Portal entry, or merged PR.

## Canonical source and toolchain

Single canonical file: `contracts/semantic_cycle_accord.py`. Source SHA-256 is
in `evidence/phase1/local-results.json`. Preserve its pinned GenVM v0.2.16
`py-genlayer` header. Python 3.12.14; genlayer-test 0.29.2; genvm-linter 0.11.0;
pytest 9.1.1; Ruff 0.14.0. Use `uv.lock` and the checksum-verifying SDK bootstrap.
Stable target remains 61999 / `https://studio.genlayer.com/api` exclusively.

## Read in full before continuation

1. README.md
2. docs/PROTOCOL_SPEC.md
3. docs/STATE_MACHINE.md
4. docs/DETERMINISTIC_INVARIANTS.md
5. docs/STABLE_COMPATIBILITY.md
6. docs/TEST_AND_ACCEPTANCE.md
7. docs/PHASE_1_REPORT.md
8. WORK_MASTER_PLAN.md
9. contracts/semantic_cycle_accord.py and all tests

## Implemented boundary

Six approved writes and six approved views are public. They enforce owner and
participant authority, full snapshots, versions, ring topology, capacity,
expiration, reservation isolation, three confirmations, consumption, terminal
states, declined identity protection and failure atomicity. Owner working slots
are bounded at five; historical reads and effective statistics are paginated.
ACTIVE means accepted commitment, not delivered service.

`_prepare_cycle` is a read-only deterministic preflight. Private, undecorated
`_reserve_accepted_cycle` consumes only topology and version inputs, reruns
preflight, reserves the three Intents and creates PENDING. Only offline fixtures
call this seam now. `assess_cycle` and `get_assessment` are absent; no verdict,
prompt, fake consensus record, classification bypass or privileged approver
exists. The public surface therefore cannot yet initiate real matching.

## Frozen future consensus requirements

On a separately authorized Phase 2, implement custom nondeterministic
Leader/Validator classification of the complete three-edge ring. Validators
independently repeat the full assessment; compare decisions rather than schema.
Decisions are FIT / NO_FIT / UNSURE; every required edge must be FIT. After
accepted legitimate consensus, rerun deterministic preflight before reserving.
Do not expose FIT injection or let a centralized operator approve matching.
Phase 1 has no canonical AI prompt and no executed semantic acceptance tests.

## Verification and remaining limits

```bash
uv sync --frozen
uv run python scripts/bootstrap_sdk.py
uv run python scripts/verify_local.py
```

Tests are offline with socket access blocked and pytest plugin autoload disabled.
The official bundle's cloudpickle serializes SDK roots; byte restoration into
a new manager is separately tested. Ordinary pickle of dynamic SDK descriptors
is unsupported. The SDK linter validated the exact runner and exports 12 methods.
This is not full WASM execution or live consensus. No critical deterministic
compatibility blocker remains; real-network evidence is intentionally deferred.

## Required stop and next action

STOP after this checkpoint. Do not merge, implement Phase 2, deploy, sign,
submit a transaction, create Repository B/frontend, or submit to Portal without
new explicit authorization. The next step is owner review of the Draft PR and
Phase 1 report in the separate strategy conversation. Readiness for Phase 2 is
technical readiness for review only; it is not authorization to start.
