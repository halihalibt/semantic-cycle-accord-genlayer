# Semantic Cycle Accord

Semantic Cycle Accord (SCA-3 V1) is a GenLayer Intelligent Contract for three-party
service exchange. Each participant offers a service and requests another. The
contract assesses whether **A can supply B, B can supply C, and C can supply A**,
then binds compatible terms to a commitment that requires all three owners' consent.

The protocol is independently reusable. [Semantic Cycle Exchange](https://github.com/halihalibt/semantic-cycle-exchange)
is one application built on it; the contract does not depend on that frontend.

## The problem

A copywriter, a designer and a data-visualization specialist may each need a
service offered by another participant. A direct two-person swap cannot satisfy
all three. Even after forming a ring, matching keywords cannot establish whether
the offered format, scope, restrictions and timing satisfy each recipient's need.
Compatibility and consent are separate questions: a plausible match should not
commit anyone automatically.

## Protocol overview

1. Three distinct owners publish versioned **Intents** containing offers, needs,
   restrictions and expiration times.
2. A participant proposes a directed ring with exact Intent IDs and versions.
3. GenLayer assesses all three offer-to-need relationships. Only `FIT / FIT / FIT`
   creates a `MATCHED` Assessment and a `PENDING` Cycle, reserving the three Intents.
4. Each owner independently confirms the same immutable snapshot.
5. The third valid confirmation makes the Cycle `ACTIVE` and its Intents `CONSUMED`.
   Participants can decline an eligible pending commitment; overdue cycles have
   a permissionless cleanup path.

**ACTIVE means accepted commitment, not confirmed service delivery.**

## Why GenLayer

The compatibility question involves natural-language meaning rather than a fixed
numeric predicate. A Leader classifies the complete ring through GenLayer's native
LLM. Each Validator independently classifies the same immutable input and compares
all three labels in their directed order. The contract applies an accepted result
through deterministic state transitions; network consensus remains responsible
for transaction acceptance and finality.

## Three-party directed exchange

Each edge compares the supplier's offer and limitations with the recipient's need
and requirements. Ring rotation is normalized; reversing the direction is a
different proposal. Exactly three distinct Intents and three distinct owners are
required. There is no automatic global search or privileged matching operator.

The [verified positive example](docs/VERIFIED_ONCHAIN_EXAMPLES.md) exchanges product
copy, a logo and a chart in the ring `1 → 3 → 2 → 1`. The negative example includes
an SVG requirement incompatible with a PNG-only offer.

## AI-assessed semantic compatibility

The canonical classifier returns exactly three labels: `FIT`, `NO_FIT` or `UNSURE`.
Any `NO_FIT` or `UNSURE` yields `NOT_MATCHED`, with no linked Cycle or reservation.
Validators compare every position, not just the overall match result. No public
method accepts a caller-supplied verdict. Identical unchanged snapshots cannot
be reassessed to search for a favorable answer.

See [consensus and equivalence](docs/CONSENSUS_AND_EQUIVALENCE_V1.md) and the
[canonical classification prompt](docs/CANONICAL_CLASSIFICATION_PROMPT_V1.md).

## Deterministic safety and snapshot binding

The snapshot binds the chain, contract, exact owners, offer/need text, limitations,
requirements, Intent versions, expirations and outgoing recipients. Its SHA-256
identity is checked against the authoritative records before confirmations.
Expected-version checks reject stale edits. Reservations prevent conflicting use
of an Intent. A declined snapshot cannot be proposed again unchanged.

Each text field is limited to 512 UTF-8 bytes. Intent validity is 1–30 days, with
at most five effectively unfinished Intents per owner. Confirmation ends at the
earlier of Cycle creation plus 72 hours or the earliest Intent expiration.
See the [protocol specification](docs/PROTOCOL_SPEC.md) and
[deterministic invariants](docs/DETERMINISTIC_INVARIANTS.md).

## State machine

| State | Meaning | Next eligible outcome |
| --- | --- | --- |
| OPEN Intent | Available, unexpired offer and need | Update, cancel or reserve after a matched assessment |
| PENDING Cycle | Compatible terms reserved; owner consent incomplete | ACTIVE, ABORTED or EXPIRED |
| ACTIVE Cycle | Three owners confirmed the exact snapshot | Terminal commitment; Intents CONSUMED |
| ABORTED Cycle | Eligible participant declined or cancelled a reserved Intent | Terminal; eligible reservations released |
| EXPIRED Cycle | Confirmation deadline reached | Permissionless cleanup releases eligible reservations |

Reads distinguish effective expiry from stored state; reads never perform cleanup.
See the [complete state machine](docs/STATE_MACHINE.md).

## Contract interface

Constructor: no arguments; deployment is restricted to chain **61999**.

| Write method | Purpose |
| --- | --- |
| `create_intent` | Publish an offer and need with a deadline |
| `update_intent` | Owner updates an OPEN Intent using its expected version |
| `cancel_intent` | Owner cancels an eligible Intent |
| `assess_cycle` | Assess exact IDs, versions and directed edges |
| `confirm_cycle` | Participant confirms the snapshot ID |
| `decline_cycle` | Participant declines an eligible pending snapshot |
| `expire_cycle` | Clean up a Cycle at or after its deadline |

Views: `get_intent`, `get_cycle`, `get_assessment`, `get_intents_page`,
`get_cycles_page`, `get_owner_records`, `get_protocol_stats`.
Exact signatures, result meanings and pagination are in the
[specification](docs/PROTOCOL_SPEC.md) and [complete source](contracts/semantic_cycle_accord.py).

## Deployment information

| Item | Value |
| --- | --- |
| Network | Stable GenLayer Studionet, Chain ID 61999 |
| RPC | https://studio.genlayer.com/api |
| Contract | [0x84e9284448D4cd16dcBBCbd8104449B11209C6F0](https://explorer-studio.genlayer.com/address/0x84e9284448D4cd16dcBBCbd8104449B11209C6F0) |
| Source | [contracts/semantic_cycle_accord.py](contracts/semantic_cycle_accord.py), 32,040 bytes |
| Source SHA256 | `88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442` |

The [deployment manifest](docs/DEPLOYMENT_MANIFEST_STUDIONET.md) links the original
transaction and source verification. This release uses the existing deployment.

## Verified onchain examples

| Example | Verified outcome |
| --- | --- |
| Assessment #1 | MATCHED, FIT / FIT / FIT; linked Cycle #1 ACTIVE, 3 / 3 confirmations |
| Assessment #2 | NOT_MATCHED, FIT / FIT / NO_FIT; cycle_id=0, no Cycle created by this assessment |

[Case descriptions and transaction links](docs/VERIFIED_ONCHAIN_EXAMPLES.md) ·
[wallet-free live inspection](https://halihalibt.github.io/semantic-cycle-exchange/?w=1) ·
[full historical E2E evidence](docs/PHASE_4C_E2E_EVIDENCE_INDEX.md).
Later application examples include Cycle #2 ACTIVE and Cycle #3 ABORTED; these are
additional records on the same contract, not a replacement for the original cases.

## Integration and local testing

Create Intents, read current versions and construct the three directed edges.
Call `assess_cycle(intent_ids, versions, edges)` as a participating owner. Read the
returned Assessment and linked Cycle; obtain each owner's separate
`confirm_cycle(cycle_id, snapshot_id)` or `decline_cycle(cycle_id, snapshot_id)` decision.
`expire_cycle(cycle_id)` is available only when the genuine deadline has been reached.
External callers should pass pagination offsets and limits explicitly.

The application integration uses **genlayer-js@1.1.8**. Contract checks use Python
3.12, GenVM v0.2.16 and genlayer-test 0.29.2 with the existing frozen lockfile.
Clone with Git history because the storage-layout regression reads a historical baseline.

```bash
uv sync --frozen
uv run python scripts/bootstrap_sdk.py
uv run python scripts/verify_local.py
```

The archived contract suite records **566 PASS / 0 FAIL / 0 SKIP**. Offline tests
use canned LLM responses and captured Validator callbacks; they are not measurements
of real model accuracy or network finality. Real finalized transactions are documented
separately in the onchain evidence.

## Security boundaries

There are no payments, escrow, custody, tokens, dispute resolution or automatic
service delivery. Semantic consensus can still make systematic errors; prompt
injection is a residual risk. Unexpected storage faults rely on GenVM transaction
rollback; Direct Mode fault tests simulate that boundary and do not prove full
production WASM rollback. Full Validator model transcripts and historical fees
are not established by the retained evidence.

The live positive `expire_cycle` test is **NOT RUN / TIME-GATED**. Dedicated Cycle #4
was PENDING with ring `12 → 13 → 14 → 12` and deadline **2026-10-15 05:16:08 UTC+8**
(`1792012568`). Offline expiry coverage does not establish live execution of that method.

[Security analysis](docs/PHASE_3_SECURITY_AUDIT.md) ·
[threat model](docs/PHASE_3_THREAT_MODEL.md) ·
[test provenance](docs/PHASE_3_TEST_AND_ACCEPTANCE.md).
Historical development and evidence records remain at their original paths for
reproducibility; their checkpoint statuses describe the time they were recorded.

## License

[MIT](LICENSE).
