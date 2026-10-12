# Semantic Cycle Accord — Intelligent Contracts

## Submission fields

| Field | Value |
| --- | --- |
| Title | Semantic Cycle Accord |
| Summary | A reusable GenLayer primitive for AI-assessed, snapshot-bound three-party service commitments. |
| Repository | https://github.com/halihalibt/semantic-cycle-accord-genlayer |
| Contract | https://explorer-studio.genlayer.com/address/0x84e9284448D4cd16dcBBCbd8104449B11209C6F0 |
| Network | Stable Studionet, Chain ID 61999 |
| Complete source | https://github.com/halihalibt/semantic-cycle-accord-genlayer/blob/main/contracts/semantic_cycle_accord.py |
| Proof materials | https://github.com/halihalibt/semantic-cycle-accord-genlayer/blob/main/docs/VERIFIED_ONCHAIN_EXAMPLES.md |
| Supplemental information | https://github.com/halihalibt/semantic-cycle-accord-genlayer/blob/main/README.md |
| License | MIT |

## Description

Semantic Cycle Accord enables a directed service exchange between three distinct
owners: A supplies B, B supplies C, and C supplies A. Each publishes a versioned
Intent containing natural-language offers, needs, limitations and requirements.
GenLayer's Leader classifies all three relationships, and Validators independently
classify the same immutable input and compare all three ordered decisions.
Only FIT / FIT / FIT creates a pending commitment.

A canonical snapshot binds exact owners, terms, versions, expirations, chain and
contract. Each owner must separately confirm that snapshot before ACTIVE. Version
checks, reservations and replay restrictions prevent stale confirmations and
conflicting use. Decline and deadline-based cleanup provide bounded exit paths.
ACTIVE means accepted commitment, not completed service delivery.

The contribution is the independently reusable semantic-compatibility and
commitment primitive. Other interfaces can integrate its seven writes and seven
views without depending on Semantic Cycle Exchange. The separate Projects
submission contributes the application workflows and transaction integration,
rather than claiming a second distinct implementation of the same contract.

## Integration

Create Intents, read versions and call `assess_cycle(intent_ids, versions, edges)`
as a participant. The returned Assessment identifies any linked Cycle. Read its
snapshot and obtain the three separate `confirm_cycle(cycle_id, snapshot_id)`
decisions, or an eligible `decline_cycle(cycle_id, snapshot_id)`. Cleanup uses
`expire_cycle(cycle_id)` only at or after the real deadline. Full parameter
semantics are in the source and protocol specification; `assess_cycle` does not
accept a caller-supplied snapshot or verdict argument.

## Evidence and limitations

Original real positive/negative E2E evidence includes Assessment #1 MATCHED,
Cycle #1 ACTIVE with three owner confirmations, and Assessment #2 NOT_MATCHED
with a NO_FIT edge and no generated Cycle. Public RPC and Explorer evidence
independently establish FINALIZED / MAJORITY_AGREE / SUCCESS. Browser operations
were user-executed, separately from receipt verification.

The archived contract offline suite records 566 PASS; mocks and captured Validator
callbacks are not measurements of live model accuracy. The canonical source is
32,040 bytes, SHA256 `88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442`.
Historical screenshot metadata is available; public image bytes and full Validator
model transcripts are not established by that index. Unexpected storage faults
rely on GenVM rollback; simulated offline faults do not prove full production rollback.

Later application evidence includes Cycle #2 ACTIVE, Cycle #3 ABORTED and Intent #8
CANCELLED. Positive live expiration remains **NOT RUN / TIME-GATED** for Cycle #4,
ring `12 → 13 → 14 → 12`, deadline **2026-10-15 05:16:08 UTC+8** (`1792012568`).
There are no payments, custody, escrow, fulfillment guarantees or dispute resolution.

The proof and supplementary URLs differ from those in the Projects submission.
They share the deployed contract intentionally. These prepared fields do not
represent Portal submission, approval or a guarantee of separate category credit.
