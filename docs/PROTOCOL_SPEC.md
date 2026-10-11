# SCA-3 V1 Protocol Specification

## Product and phase boundary

Exactly three different wallets exchange digital services in one directed ring:
A supplies B, B supplies C, C supplies A. Each supply must satisfy its recipient's
need, including limitations and requirements. `ACTIVE` means every participant
accepted the same commitment; it does not mean services have been delivered.
No payment, custody, reputation, delivery, arbitration, token, privileged
operator, upgrade authority, frontend, or centralized matching service exists.

Phase 2 adds native custom nondeterministic Leader/Validator execution on the
unchanged Phase 1 core. Every Validator independently classifies all three edges
and compares exact position-sensitive FIT / NO_FIT / UNSURE labels. Only three
FIT labels produce MATCHED/PENDING. All other valid vectors persist NOT_MATCHED.
See CONSENSUS_AND_EQUIVALENCE_V1.md for the exact mechanism and offline limits.

## Storage schema

All persistent fields are declared in `SemanticCycleAccord`. IDs, counters,
versions, and timestamps use `u64`; numeric record-map keys use supported `u256`.
Histories, slots, terms, and confirmation flags use typed `DynArray`. Maps use
fully parameterized `TreeMap`; structured values are `@allow_storage`
dataclasses. There are no undeclared persistent fields or Python list/dict
storage annotations.

| Intent field | Meaning |
| --- | --- |
| intent_id | Monotonic unique identifier, starting at 1 |
| owner | Lowercase address of actual immediate caller |
| offer_description / offer_limitations | Service offered and restrictions |
| need_description / need_requirements | Required service and acceptance conditions |
| version | Starts at 1; every successful OPEN update increments once |
| expires_at | Absolute Unix transaction-time deadline |
| status | OPEN, RESERVED, CONSUMED, CANCELLED, or EXPIRED |
| cycle_id | 0 when not reserved/consumed; commitment ID otherwise |

All four text fields are limited to 512 UTF-8 bytes, not 512 characters. Offer
and need descriptions must contain non-whitespace content; limitations and
requirements may be empty. Text is preserved exactly, without semantic
normalization. Validity is inclusively 1–30 days from the create/update
transaction timestamp. Integer IDs and timestamps must fit unsigned 64 bits.

Each wallet may have at most five effectively OPEN or RESERVED Intents. A
bounded five-slot working index supports the check independently of historical
record count. Terminal and logically expired entries are removed from this
index when replaced. Historical owner indexes remain append-only and paginated.

| Cycle field | Meaning |
| --- | --- |
| cycle_id | Unique monotonically increasing identifier |
| snapshot_id | SHA-256 of canonical frozen terms and domain |
| canonical_snapshot | Exact canonical JSON, retained for integrity checks |
| terms | Three immutable snapshots; each includes every Intent field relevant to matching and outgoing recipient Intent ID |
| confirmations | Three independent flags indexed by canonical owner order |
| created_at | Transaction timestamp when accepted transition reserves records |
| confirmation_deadline | min(created_at + 72 hours, earliest Intent expiration) |
| status | PENDING, ACTIVE, ABORTED, or EXPIRED |

Each `Terms` record contains intent_id, owner, offer_description,
offer_limitations, need_description, need_requirements, version, expires_at,
and supplies_to. Snapshots never alias mutable Intent content.

## Exact public methods

Constructor: no arguments. It rejects any chain ID other than 61999 and stores
the actual network/contract identity. It establishes no administrator.

| Write method | Arguments | Result and checks |
| --- | --- | --- |
| create_intent | offer_description, offer_limitations, need_description, need_requirements, expires_at | New ID; text, validity, capacity, overflow checks |
| update_intent | intent_id, expected_version, four text fields, expires_at | New version; actual owner, expected version, unexpired OPEN required |
| cancel_intent | intent_id, expected_version | Owner-only; cancels OPEN or safely aborts eligible PENDING reservation and cancels its Intent |
| confirm_cycle | cycle_id, snapshot_id | True for a new confirmation; False for a duplicate while eligible PENDING; actual participant and all authoritative snapshots checked |
| decline_cycle | cycle_id, snapshot_id | Eligible participant aborts PENDING and permanently blocks this exact snapshot |
| expire_cycle | cycle_id | Permissionless cleanup at/after deadline; True once, False for an already cleaned EXPIRED cycle |

Phase 2 adds `assess_cycle(intent_ids, versions, edges)` as the seventh write,
returning `{assessment_id, result, cycle_id}`. Its parameters are three IDs,
three expected versions and three directed edges. Caller must be an actual
participant. Preflight runs before AI and again after accepted VM output;
immutable content is rechecked. No public method accepts a supplied verdict.

`get_assessment(assessment_id)` is the seventh view. Valid missing IDs return
found=false; invalid IDs reject. Existing records return stored canonical
snapshot, derived IDs/versions/edges, decisions, result, cycle association,
current effective cycle_status (NONE for negative), proposer, timestamp and
prompt version/digest. No view calls the LLM or mutates protocol storage.

| View | Arguments | Result |
| --- | --- | --- |
| get_intent | intent_id | found flag; effective and stored status plus record |
| get_cycle | cycle_id | found flag; frozen snapshot, edges, versions, confirmations, timestamps and statuses |
| get_intents_page | offset=0, limit=20 | Ascending-ID records, total, next_offset, has_more |
| get_cycles_page | offset=0, limit=20 | Ascending-ID records, total, next_offset, has_more |
| get_owner_records | owner, offset=0, limit=20 | Independent Intent/Cycle history pages at the same offset, totals, next_offset, has_more and bounded effective unfinished_count |
| get_protocol_stats | offset=0, limit=50 | Global cumulative counters and explicitly labeled effective Intent counts for the requested page |

Offsets are zero-based nonnegative u64-compatible integers. Limits are 1–50.
Missing positive record IDs return `found=false`; zero, negative, out-of-range,
or malformed IDs reject. Out-of-history offsets return empty pages. Do not
assume SDK schema export conveys Python defaults: external callers may supply
offset and limit explicitly.

Protocol statistics distinguish global cumulative created/activated/aborted
counts from time-dependent effective page counts. Aggregate all pages under
the same transaction-time context for an exact effective global distribution.
`expired_cycles_cleaned` counts completed cleanup, not uncleaned overdue cycles.
No expired OPEN Intent is eligible or counted OPEN merely because stored status
has not yet been cleaned.

## Deterministic accepted-result seam

`_prepare_cycle(intent_ids, versions, edges)` validates exactly three distinct
Intent IDs, three distinct owners, exactly three correctly ordered directed
edges, matching versions, OPEN/unreserved states, and expiration. It performs
no protocol writes. Input order defines the ring: edge i must be
`[intent_ids[i], intent_ids[(i+1)%3]]`.

`_reserve_accepted_cycle` is private and undecorated. It accepts topology and
version inputs, not classifications, and remains private/undecorated. Phase 2 assess_cycle invokes it only after
accepted legitimate custom consensus returns exactly three FIT labels. It reruns
preparation immediately before writing all three reservations and one PENDING
Cycle. Historical Phase 1 test fixtures still call it internally; those fixture
Cycles alone are not evidence of semantic acceptance.

## Snapshot identity and integrity

Normalize ring rotations by starting at the smallest Intent ID. Preserve the
directed order; never sort all IDs or normalize reversal. Canonical JSON is:

```text
["SCA-3-V1", chain_id, lowercase_contract_address,
 [[id, owner, offer, limitations, need, requirements, version, expires_at, supplies_to], ...]]
```

There are exactly three inner entries. Serialize UTF-8 with
`ensure_ascii=False` and separators `(',', ':')`. Digest is lowercase SHA-256
hex. Caller identity is not part of proposal identity, preventing proposer
changes from bypassing replay restrictions.

Every confirmation checks all three authoritative Intent records against the
actual frozen content, owner, version, expiration, and outgoing edge; every
Intent must still be RESERVED by that Cycle. It also rechecks canonical JSON,
digest, ring identity, cardinality, and deadline calculation. A supplied hash
cannot replace these checks. This happens before the first, second, and third
confirmation and before an eligible decline or reserved cancellation.

## Replay and terminal behavior

All proposal identities are recorded permanently. An identical proposal cannot
reserve the same snapshot a second time, including after expiration. A declined
snapshot is explicitly marked and rejected regardless of caller or cyclic
rotation. At least one Intent version must change before the declined exact
snapshot can be proposed again. Reversed assignments are different snapshots.

Duplicate confirmations on eligible PENDING Cycles are no-ops and never increase
count. Confirmations against terminal or overdue Cycles reject. Every distinct
owner confirms only its own flag. Three true flags activate and consume all
three Intents exactly once. ACTIVE cannot be aborted, expired, or reopened.

Cleanup resolves all three records before any change, then releases only
RESERVED records whose cycle_id matches. Expired records become EXPIRED;
eligible records become OPEN. CANCELLED, EXPIRED, CONSUMED, and another Cycle's
reservation are never reopened. A cancelled reserved Intent becomes CANCELLED
after eligible releases; the aborted Cycle's immutable snapshot is retained.

## Errors, bounded work and atomicity

Errors use `gl.vm.UserError` with stable codes for invalid integers/text/validity,
missing IDs, unauthorized caller, stale version, capacity, overflow, invalid
ring, duplicate owner/Intent/proposal, unavailable/expired Intent, snapshot or
reservation mismatch, declined snapshot, invalid state, or unreached deadline.
No failing validation is treated as an accepted commitment.

Public mutation preflights precede write blocks. Intent capacity scans at most
five slots; cycle operations resolve three records; pages scan at most fifty
records. Fixed-size content is checked before storage. No public operation
scans a wallet's complete history or all global records. Terminal mutations
reject or are explicit idempotent expiration no-ops.

## Phase 2 assessment storage and replay

Append exactly three root fields after all original fields: typed
`assessments: TreeMap[u256, Assessment]`, `assessed_snapshots: TreeMap[str, u64]`,
and `assessment_count: u64`. The bounded @allow_storage Assessment contains ID,
snapshot digest, canonical full snapshot, exactly three labels in DynArray[str],
MATCHED/NOT_MATCHED result, linked cycle ID (0 when negative), transaction timestamp,
actual proposer and constant prompt version/hash. Full snapshot preservation is
necessary for negative records after editable Intents change; derived ID/edge
arrays are not redundantly persisted. Historical root/Intent/Cycle layouts remain
readable in the offline byte reconstruction test. This is not an onchain upgrade.

Identical canonical negative snapshots reject DUPLICATE_ASSESSMENT before LLM
invocation. Positive proposals/reservations and declined/expired protections
retain original behavior. A successful version update changes the snapshot.
Stats retain original global counters/page meanings, set semantic_matching_available
true and add assessment_total. Fixture-created Cycles are not relabeled assessments.

All predictable state/counter errors and bounded local record construction precede
writes. Unexpected storage faults within the commit block depend on VM transaction
rollback. Direct Mode validates expected safety without rollback and tests unexpected
faults only with an explicitly simulated transaction boundary. Full WASM is NOT RUN.

MATCHED/PENDING is distinct from wallet confirmations, ACTIVE and network FINALIZED.
A stored assessment reflects successful contract execution, not independently
verified blockchain finality. No finality fields, vote counts or Validator IDs are
invented. No real transaction finality was tested in Phase 2.
