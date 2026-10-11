# Semantic Cycle Accord — SCA-3 V1

SCA-3 is a GenLayer Intelligent Contract for reciprocal exchange between exactly
three different wallets: **A supplies B, B supplies C, C supplies A**. Participants
publish digital service offers and needs. Custom Leader/Validator assessment
classifies all three directed offer-to-need relationships as FIT / NO_FIT / UNSURE.

The Leader calls the native GenLayer LLM once for the full ring. Each Validator
independently repeats the same complete classification and must match all three
canonical labels. Exactly `[FIT, FIT, FIT]` creates a MATCHED assessment and a
PENDING commitment. Any NO_FIT or UNSURE persists NOT_MATCHED without reservation.
Identical unchanged assessment snapshots cannot be retried to fish for a verdict.

All three actual owners must then independently confirm the same immutable
snapshot. The third valid confirmation makes the Cycle ACTIVE and consumes
exactly the three Intents. **ACTIVE means accepted commitment, not delivered
services.** There are no payments, tokens, custody, reputation, arbitration,
fulfillment guarantees or matching administrator.

## Phase 2 checkpoint and execution limits

This is an undeployed Phase 2 development checkpoint awaiting independent review.
The public semantic path is implemented; offline testing uses canned native LLM
responses and explicitly invokes captured Validators through Direct Mode.
It is not evidence of real model accuracy, network consensus or finalized
transactions. No deployment or onchain transaction has occurred. No frontend or
Repository B exists. Full GenVM WASM and live execution are not verified.

The deterministic Phase 1 core, INV-01–16, original method behavior and persistent
field prefix remain intact. Assessment fields are appended; read and storage
compatibility, including actual frozen Phase 1 persisted bytes, are tested.
Seven writes and seven views are exported, with no public verdict injection seam.

## Fixed environment and reproduction

- Stable Studionet only: **61999**, `https://studio.genlayer.com/api`.
- Python **3.12.14**, official GenVM **v0.2.16** content-pinned Python runner.
- genlayer-test **0.29.2**, genvm-linter **0.11.0**, pytest **9.1.1**, Ruff **0.14.0**.
- Original `uv.lock` retained. No upgraded SDK, alternate chain or paid API.

```bash
uv sync --frozen
uv run python scripts/bootstrap_sdk.py
uv run python scripts/verify_local.py
```

Bootstrap verifies the official cached/downloaded artifact; it does not connect
to a blockchain. Verification is offline with pytest plugin autoload disabled
and test socket access blocked. The byte-layout test reads the frozen baseline
from local git history, so retain repository history when reproducing.

Phase 1 historical baseline: **229 PASS / 0 FAIL / 0 SKIP**, reproduced before edits.
Final Phase 2 results and exact hashes are in the report and machine-readable evidence.

## Specifications and evidence

- [Protocol](docs/PROTOCOL_SPEC.md) and [state machine](docs/STATE_MACHINE.md)
- [INV-01 through INV-16](docs/DETERMINISTIC_INVARIANTS.md)
- [Canonical Prompt V1](docs/CANONICAL_CLASSIFICATION_PROMPT_V1.md)
- [Custom consensus and full equivalence](docs/CONSENSUS_AND_EQUIVALENCE_V1.md)
- [Phase 2 tests, fixtures and limitations](docs/PHASE_2_TEST_AND_ACCEPTANCE.md)
- [Phase 2 report](docs/PHASE_2_REPORT.md)
- [Continuation checkpoint](PROJECT_CHECKPOINT.md)
- [Master plan](WORK_MASTER_PLAN.md)
- [Historical Phase 1 report](docs/PHASE_1_REPORT.md)

Local predictable failures are tested without rollback. Unexpected storage faults
rely on GenVM transaction rollback; Direct Mode tests explicitly simulate that
boundary and do not prove full WASM rollback. Prompt injection and systematic
semantic error remain risks despite structured boundaries and independent checks.
Further stages require separate user authorization. MIT License retained.
