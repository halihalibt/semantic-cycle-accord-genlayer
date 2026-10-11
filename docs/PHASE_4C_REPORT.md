# SCA-3 V1 — Phase 4C real onchain E2E evidence closure

**POSITIVE AND NEGATIVE FINAL OUTCOMES INDEPENDENTLY VERIFIED — HISTORICAL READ GAP RETAINED — DRAFT REVIEW — STOP**

Repository A: `halihalibt/semantic-cycle-accord-genlayer`, public, MIT.
Verified merged main baseline: `2215e6fac7d4922b50ff1546bae76b6e4e3a530c`.
Branch: `phase4c-real-e2e-evidence`. This phase verifies the user's already completed
E2E; it performs no write transaction and does not execute the business flow again.
The published branch HEAD and Draft PR number are returned in the execution report.

## Independently acquired evidence

Stable Studionet, RPC `https://studio.genlayer.com/api`, `eth_chainId=0xf22f` (61999).
Contract: `0x84e9284448D4cd16dcBBCbd8104449B11209C6F0`.
All **11** specified Phase 4C hashes return FINALIZED, compatibility receipt
status `0x1`, successful Leader Return, `result_name=MAJORITY_AGREE`, one Accepted
round, five initial voting addresses and **zero actual rotations**. Full original
transaction objects, consensus histories, monitoring, Leader/Validator receipts,
public signed transaction bytes and raw state responses are preserved without
editing in [rpc/](../evidence/phase4c/rpc/). Each JSON envelope retains exact request,
URL, acquisition timestamp, transport exit code, stdout and stderr.

The package contains **51** independent read-only RPC responses: chain identity;
33 transaction/receipt/status responses for the 11 hashes; 12 final contract reads;
four repeated final reads; and a fresh read of the original deployment transaction.
The four repeated results match their first reads. These are separately acquired
latest-final observations, not an atomic historical state snapshot.

Each public signed rollup transaction was cryptographically recovered offline:
the recovered signer equals the actual expected A/B/C owner, and the EIP-155
signed chain domain is 61999 for all 11. The signed ABI payload's origin, recipient
and inner serialized calldata also match the RPC object. No private key, mnemonic,
signing operation or connected wallet was used. The configured rotation maximum
of 3 is distinct from the observed actual rotation count of 0.

The 11 Explorer detail pages were opened and visibly inspected; each shows the
correct hash, FINALIZED, SUCCESS and Accepted. Verified URLs are in
[Explorer observations](../evidence/phase4c/explorer-observations.json) and the
[E2E evidence index](PHASE_4C_E2E_EVIDENCE_INDEX.md). Unlike the historical Phase 4B
browser failure, Explorer was accessible during Phase 4C. This derived UI inspection
record is not an original RPC receipt. UI displays integer parameters as quoted
strings; decoding the signed/raw calldata establishes their actual integer types.

## Source and trusted Prompt identity

Fresh deployment `data.contract_code` was decoded and compared byte-for-byte
against the source at the frozen merged baseline: **32,040 bytes**.

- Canonical source SHA256: `88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442`.
- Trusted CANONICAL_PROMPT constant SHA256: `8a7b279a3594397802c71fef4df9b4d30db1ff528177d0bf05c80a62397192d3`.
- Both persisted Assessments record the same trusted Prompt hash and version
  `SCA3-CANONICAL-CLASSIFICATION-V1`.

The Prompt hash identifies the trusted constant, not the full runtime prompt
including appended immutable input. Source, Prompt document, protocol, frozen
vectors, acceptance plan, tests, dependencies and `uv.lock` remain unchanged.
[Source identity](../evidence/phase4c/source-identity.json) records the comparison.

## Positive E2E — independent final result

Actual owners: A `0x22Acaa233b7b985b36ef168F2DE9295334065B15`,
B `0x418C0A70603F8231CD99B1f37dFc49300Dcd024e`,
C `0xBE8567FD2294f3eC8E68f08b58ABEb5B2d28AD61`.
Create Returns independently decode to **1, 2, 3**. Exact four text fields match
the frozen positive vector. Submitted expiry is `1792350285`; all creates satisfy
the contract's execution-time expiry window.

Assessment call: `[[1,3,2],[1,1,1],[[1,3],[3,2],[2,1]]]`.
Actual topology is **A→C→B→A**; canonical owner order is A,C,B. The successful
Return is `{"assessment_id":1,"cycle_id":1,"result":"MATCHED"}`. Raw Leader
equivalence output independently decodes to `FIT / FIT / FIT`, matching persisted
Assessment #1. Snapshot `48e1c68d358f67368c5d8b478e9d450401be06cdf91e90b6b8b94932d2951ede`
is reproduced by rebuilding the canonical JSON from the stored intent terms,
owners, versions, expiries, directed edges, protocol, chain and contract identity.

All three distinct signatures confirm Cycle #1 with exactly that snapshot.
Each Return is true and each recorded creation timestamp is before the persisted
confirmation deadline `1792005850`. Current Cycle #1 is ACTIVE with three true
flags and confirmation_count 3. Intents #1–#3 are CONSUMED, version 1, cycle_id 1.
Assessment #1 remains MATCHED and its current cycle_status is ACTIVE.

Original user screenshots also preserve pre-confirmation PENDING/zero flags,
RESERVED Intents and intermediate confirmation counts 1 and 2. These privately retained screenshots
are **user-supplied historical reads**, not independently acquired historical RPC.
Successful transaction receipts plus current state support the transition, but
cannot substitute for the missing original machine-readable intermediate reads.

## Negative E2E — independent final result

Fresh create Returns independently decode to **4, 5, 6**; exact submitted terms
match the frozen negative vector, expiry `1792353240`. B offers PNG-only and
explicitly excludes editable SVG; A still requires editable SVG plus PNG.

Assessment call: `[[4,6,5],[1,1,1],[[4,6],[6,5],[5,4]]]`.
The successful Return is `{"assessment_id":2,"cycle_id":0,"result":"NOT_MATCHED"}`.
Raw Leader equivalence output and persisted Assessment #2 both show
`FIT / FIT / NO_FIT`. Snapshot #2 hash is
`dffd6337478c50f2285a66d715d8e1ad0f65814d92602d7d64f51b1c85fb990d`.
Its prompt hash, proposer, canonical terms, versions and topology also verify.
A successful negative business judgment is a **successful transaction**.

Intents #4–#6 remain OPEN, version 1, cycle_id 0. Assessment #2 has cycle_id 0 and
cycle_status NONE. get_cycle(2) returns found=false; the full Cycle page contains
only Cycle #1, still ACTIVE with its original snapshot and three confirmations.

| Final protocol value | Independently verified result |
| --- | --- |
| intent_total / assessment_total | 6 / 2 |
| cycle_total / active_total | 1 / 1 |
| CONSUMED / OPEN / RESERVED | 3 / 3 / 0 |
| aborted_total / expired_cycles_cleaned | 0 / 0 |
| CANCELLED / EXPIRED | 0 / 0 |
| Counts page coverage | offset 0, next_offset 6, has_more false |

Before-negative positive-only counters are preserved in original user screenshots;
this phase independently re-read the final totals twice. It did not acquire an
original machine-readable before-negative counter record.

## Exact consensus interpretation

Both semantic assessments have **3 agree + 2 idle**, one Accepted round and zero
rotations. Neither has five unanimous agreeing voting addresses. The 11-write
table preserves the different create #2 record, whose actual map has five agree;
this cannot be generalized to either semantic assessment.

In this live RPC format `leader_receipt` contains a `mode=leader` record and a
separate `mode=validator` record at the Leader address; `validators` contains
four other Validator records. Count by each record's **mode and address**, not
by the containing field name. The two receipts at one address do not prove two
distinct independent nodes. Across all 11 transactions the maps have 35 agree
and 20 idle votes. Every idle record has execution_result ERROR plus explicit
`CONSENSUS_VALIDATOR_QUORUM_REACHED` / `Validator execution cancelled after quorum`.
These are quorum cancellations, not genuine disagreement or failed business writes.
All acquired nondet_disagree fields are null. No disagreement was observed in
these receipts; this is not a claim about other executions.

For each assessment, two **distinct non-Leader addresses** have successful agree
receipts, matching Return/state hashes, and nonempty LLM token statistics. Together
with the unchanged custom full-ring validator implementation and network acceptance,
these provide independent semantic consensus evidence beyond Leader output alone.
The Leader-address Validator receipt is also preserved, without treating duplicated
Leader/Validator telemetry as an additional independent node or summing it twice.
Native equivalence output exposes the Leader's canonical label vector. The acquired
Validator records do not expose raw model response text or separate decoded
three-label vectors, so none were fabricated.

## Screenshots and remaining evidence limits

**60 original** user-uploaded Studio/Explorer PNGs were materialized and checked
byte-for-byte privately;
their filenames, byte lengths, provenance and SHA256 are in
[screenshots.json](../evidence/phase4c/screenshots.json). Partial views and UI
formatting artifacts are retained. No new screenshots are represented as user
originals. Automatic approval review rejected uploading original screenshots to this public
GitHub repository: it judged the request insufficiently explicit about public
disclosure of user-provided image contents. The original image bytes are retained
privately; this public PR contains the inventory/checksums only. No screenshot
contents were uploaded via another path. The user must explicitly approve public
publication before a separate screenshot upload patch. No new screenshot capture
or re-upload is needed from the user. Screenshot timing/order is not cryptographic
proof of historical state.

Still unavailable or untested:

1. Original raw historical OPEN/RESERVED/PENDING and post-confirmation 1/2 reads,
   plus the original before-negative counter read. Privately retained original screenshots cover
   these observations; fresh latest-final reads do not reproduce past states.
2. Raw per-Validator LLM response text and complete runtime prompts; receipts
   expose votes/results/statistics, not a complete independent model transcript.
3. Actual fee estimate, user fee budget and consumed GEN remain UNKNOWN. Preserve
   compatibility receipt gasUsed/effectiveGasPrice and transaction gaslimit/nonce
   exactly; do not interpret compatibility block 0 or hash fields as ordinary EVM
   blocks or fabricate fee totals. Public signed bytes support signature recovery
   despite RPC top-level r/s/v being null; the user's wallet approval UI transcript
   was not acquired.
4. Real-node unexpected mid-write rollback, service delivery, broad semantic
   accuracy, live adversarial/race/resource scenarios and complete production
   security certification are NOT RUN / UNVERIFIED. ACTIVE means commitment,
   never actual delivery or a production security guarantee.

## Local verification and stop

Run the package's offline verifier with the frozen lock dependencies:
`uv run python evidence/phase4c/verify.py`. To reproduce private original-byte checks,
add `--screenshots-dir /path/to/private-original-pngs`; the public repository alone
cannot reproduce those PNG checks.
[verification.json](../evidence/phase4c/verification.json) records actual local PASS
groups, an empty FAIL list and explicit NOT RUN/evidence-gap items. Checks cover
RPC envelope/schema shape, typed calldata, public signature recovery, source and
Prompt SHA256, votes/rounds/rotations, frozen vectors, canonical snapshot identity,
returned IDs, final/repeated reads, privately available screenshot bytes, checksums, links and file scope. Automatic
review blocking public PNG upload is recorded separately; it is not a test failure.
The contract regression suite was NOT RUN for this evidence/documentation-only
change; historical 566 PASS is not represented as a new test result.

Historical Phase 4A/4B evidence and reports are preserved. New reports distinguish
fresh independent raw evidence from original user screenshots and missing historical
machine-readable reads. No production code, Prompt, protocol/consensus rules or
dependency lock is changed. No redeployment, upgrade, signing, business write,
Repository B, frontend, Portal submission or merge occurred.

**STOP immediately after publishing the Draft PR. Ordinary-chat independent review
and separate merge approval are required.**
