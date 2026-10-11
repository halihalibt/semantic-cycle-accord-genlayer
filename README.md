# Semantic Cycle Accord — SCA-3 V1

SCA-3 models a reciprocal exchange between exactly three different wallets:
**A supplies B, B supplies C, and C supplies A.** Each participant publishes a
digital service offer and a need. A future GenLayer semantic assessment must
verify all three supply-to-need relationships before a commitment can be proposed.

This repository currently implements the **Phase 1 deterministic contract core**.
Intent ownership, versions, expiration, directed topology, immutable snapshots,
reservations, confirmations, rejection, consumption, pagination, and replay
protection are implemented. All three owners must independently confirm the
same unchanged snapshot before its cycle becomes `ACTIVE`.

`ACTIVE` records agreement to the reciprocal commitment. It does not establish
that services were delivered. SCA-3 does not handle payments, custody, tokens,
reputation, arbitration, or service delivery.

## Current execution boundary

Semantic fit depends on natural-language offers, limitations, needs, and
requirements. Deterministic string matching cannot establish that fit; the
planned Phase 2 assessment requires independent GenLayer Leader/Validator
classification of the full three-edge ring.

**Real semantic matching is not implemented.** `assess_cycle` and `get_assessment`
are unavailable. There is no public method for injecting `FIT` verdicts, no
matching administrator, and no artificial consensus engine. The private,
undecorated `_reserve_accepted_cycle` seam is exercised only by offline test
fixtures in Phase 1. With the present public API, users can maintain Intents but
cannot create Cycles. Local fixture cycles are not onchain evidence.

## Verified development environment

- Stable Studionet only: chain ID **61999**, RPC `https://studio.genlayer.com/api`.
- Python **3.12.14**; project supports Python 3.12.
- Official GenVM **v0.2.16** runner and its exact transitive SDK dependencies.
- `genlayer-test` **0.29.2**, `genvm-linter` **0.11.0**, pytest **9.1.1**, Ruff **0.14.0**.
- Python runtime SDK identity is the pinned `py-genlayer` runner, not the
  JavaScript package `genlayer-js 1.1.8`. No JavaScript SDK is needed in Phase 1.

Latest versions and release candidates are deliberately not selected. The
contract header pins its runner by content identity. No contract was deployed
and no blockchain transaction was submitted.

## Reproduce local verification

Install [uv](https://docs.astral.sh/uv/), then from this repository:

```bash
uv sync --frozen
uv run python scripts/bootstrap_sdk.py
uv run python scripts/verify_local.py
```

Bootstrap downloads and verifies the official runtime archive (about 207 MiB);
it does not connect to a blockchain. The verification script disables pytest
plugin autoload, pins the linter to v0.2.16, and executes only offline tests.
Tests also block socket connections. Pre-cache the SDK before running tests.

Phase 1 after the limited security hardening amendment: **229 tests passed, 0 failed, 0 skipped**
(original checkpoint: 176 passed). SDK storage
serialization/reconstruction and calldata compatibility are included. GenVM
AST lint and SDK semantic validation passed; schema export contains exactly
six writes and six views. See [test acceptance](docs/TEST_AND_ACCEPTANCE.md).

## Specification and checkpoint

- [Protocol specification](docs/PROTOCOL_SPEC.md)
- [State machine](docs/STATE_MACHINE.md)
- [INV-01 through INV-16](docs/DETERMINISTIC_INVARIANTS.md)
- [Stable compatibility and limits of verification](docs/STABLE_COMPATIBILITY.md)
- [Phase 1 report](docs/PHASE_1_REPORT.md)
- [Continuation checkpoint](PROJECT_CHECKPOINT.md)
- [Remaining phases](WORK_MASTER_PLAN.md)

## Security and status

All public state transitions validate the actual caller and authoritative
storage. Confirmations re-check every frozen term and reservation; a supplied
digest alone is insufficient. Expiration uses the deterministic transaction
clock, with `now >= deadline` expired. Histories and effective statistics are
paginated; time-dependent page counts must not be treated as global totals.

This is an undeployed development checkpoint, not a production-ready protocol.
Direct Mode and SDK checks do not prove real Validator agreement, service
compatibility, onchain finality, or live concurrency behavior. Phase 2 requires
separate authorization; further phases will add the product and real evidence.

MIT License. Copyright attribution in [LICENSE](LICENSE) is retained.
