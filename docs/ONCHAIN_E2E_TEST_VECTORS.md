# SCA-3 V1 — Exact manual E2E vectors

DOCUMENTED BUT NOT EXECUTED. No wallet addresses, contract address, transaction hashes or snapshot IDs exist in this package. Strings below are exact calldata, each under 512 UTF-8 bytes. All future writes require separate authorization and the user's own signing.

## Execution-time variables

1. Record actual distinct wallet addresses as A, B and C. Choose only accounts personally controlled by the user. Record the finalized deployed contract address.
2. Immediately before creating Intents, calculate `expires_at = floor(current Unix time in seconds) + 604800`. Windows PowerShell: `[DateTimeOffset]::UtcNow.ToUnixTimeSeconds() + 604800`. JavaScript console in the user's own browser: `Math.floor(Date.now()/1000) + 604800`. These calculations do not sign or send anything.
3. Replace the final placeholder below with that integer, without quotes. Check the wallet/network clock against observed transaction timestamps. At actual execution the difference must be 86400–2592000 seconds inclusive. Recalculate if delayed; never reuse a date printed in an old guide. Three recent creates may use the same freshly computed seven-day expiry.
4. Each field-based Studio form uses plain string content for the four text fields and an integer for expires_at. The JSON arrays below show ordered arguments, not guaranteed Studio JSON-envelope syntax; inspect the current form before using JSON mode.

## Positive exchange: A → C → B → A

A supplies homepage copy to C. C supplies a chart to B. B supplies a logo to A. Same scope, quantity, format, language and relative delivery deadline appear on both sides of each edge. Intended classification is three FIT labels, subject to actual independent model judgment; never force that result.

Exact signature: `create_intent(offer_description, offer_limitations, need_description, need_requirements, expires_at)`.

### Wallet A: create_intent

```json
[
  "Write one English homepage for a digital-service exchange: one headline, one subheading and three service paragraphs; 300 words total; deliver one UTF-8 TXT file within 48 hours after cycle activation.",
  "Exactly one 300-word English homepage; TXT only; no website coding or publication; delivery within 48 hours after cycle activation.",
  "Design one original typographic logo reading SCA-3; deliver one editable SVG vector file and one transparent 1024x1024 PNG within 48 hours after cycle activation.",
  "Exactly one typographic SCA-3 logo; editable SVG and transparent 1024x1024 PNG; no animation or brand guide; delivery within 48 hours after cycle activation.",
  "REPLACE_WITH_EXECUTION_TIME_PLUS_604800"
]
```

### Wallet B: create_intent

```json
[
  "Design one original typographic logo reading SCA-3; deliver one editable SVG vector file and one transparent 1024x1024 PNG within 48 hours after cycle activation.",
  "Exactly one typographic SCA-3 logo; editable SVG and transparent 1024x1024 PNG; no animation or brand guide; delivery within 48 hours after cycle activation.",
  "Create one bar chart from the fixed data Copy=10, Logo=20, Chart=30; include category labels and values; deliver one SVG vector file and one 1600x900 PNG within 48 hours after cycle activation.",
  "Exactly one labeled bar chart using only Copy=10, Logo=20, Chart=30; SVG and 1600x900 PNG; no interactive dashboard; delivery within 48 hours after cycle activation.",
  "REPLACE_WITH_EXECUTION_TIME_PLUS_604800"
]
```

### Wallet C: create_intent

```json
[
  "Create one bar chart from the fixed data Copy=10, Logo=20, Chart=30; include category labels and values; deliver one SVG vector file and one 1600x900 PNG within 48 hours after cycle activation.",
  "Exactly one labeled bar chart using only Copy=10, Logo=20, Chart=30; SVG and 1600x900 PNG; no interactive dashboard; delivery within 48 hours after cycle activation.",
  "Write one English homepage for a digital-service exchange: one headline, one subheading and three service paragraphs; 300 words total; deliver one UTF-8 TXT file within 48 hours after cycle activation.",
  "Exactly one 300-word English homepage; TXT only; no website coding or publication; delivery within 48 hours after cycle activation.",
  "REPLACE_WITH_EXECUTION_TIME_PLUS_604800"
]
```

## Read gates and assessment

After EACH future create, require finalized successful execution and record the returned integer ID. Read `get_intent(actual_id)` and check found=true, actual owner, exact four strings, expiry, version=1, status=OPEN, stored_status=OPEN and cycle_id=0. If the return ID is not exposed, inspect owner records `get_owner_records(actual_owner,0,50)` and match all terms plus the transaction evidence; do not guess.

Only if actual reads prove A=1, B=2, C=3 and all versions=1:

- Wallet A (or B/C, each an actual participant) calls `assess_cycle(intent_ids, versions, edges)`.
- intent_ids: `[1,3,2]`
- versions: `[1,1,1]`
- edges: `[[1,3],[3,2],[2,1]]`
- Ordered arguments: `[[1,3,2],[1,1,1],[[1,3],[3,2],[2,1]]]`.

Otherwise replace 1/2/3 by actual A/B/C IDs and use their actual corresponding versions in A,C,B order. Construct edges A→C, C→B, B→A. Do not sort the ring. The contract rotates to the smallest ID while preserving direction; use the stored assessment order when comparing classifications.

Require finalized successful assessment plus independent Validator agreement evidence. Record returned assessment_id and cycle_id. Read `get_assessment(actual_assessment_id)` and `get_cycle(actual_cycle_id)`. Require MATCHED, three FIT labels, PENDING cycle, the expected owners/terms/versions/edges, zero confirmations, correct prompt hash and each Intent RESERVED by that cycle. Read the real `snapshot_id` from get_cycle. If result is NOT_MATCHED, preserve evidence and STOP for review; do not run confirmations or try the unchanged assessment again.

## Three confirmations

Exact signature: `confirm_cycle(cycle_id, snapshot_id)`.

For each of A, then B, then C, enter:

1. cycle_id: the actual integer returned and read from the successful assessment (1 only if verified).
2. snapshot_id: the exact string read from `get_cycle(actual_cycle_id)`; no hand-crafted digest.

Ordered argument template: `[ACTUAL_CYCLE_ID, "ACTUAL_GET_CYCLE_SNAPSHOT_ID"]` (template, not executable JSON). Use the SAME values for all three wallets. Recheck actual active signer before every write and finish before `confirmation_deadline = min(created_at+259200, earliest expires_at)`.

After A: one flag true, PENDING, all three RESERVED. After B: two flags true, PENDING, all three RESERVED. After C: all flags true, confirmation_count=3, ACTIVE, all three Intents CONSUMED and associated with the same cycle. Flag positions follow canonical A,C,B terms for conditional IDs 1,3,2, so after B expect `[true,false,true]`; do not confuse wallet order with flag order. Activation proves commitment, not delivery.

## Unambiguous negative case — three fresh Intents

Do not reuse the positive cycle's CONSUMED Intents. After separate authorization create a fresh A/B/C trio, using the same positive arguments above EXCEPT replacing negative Wallet B's first two fields with:

- offer_description: `Design one original typographic logo reading SCA-3; deliver only one transparent 1024x1024 PNG within 48 hours after cycle activation.`
- offer_limitations: `PNG raster output only. SVG vector output and editable vector source are explicitly unavailable. Exactly one logo; no animation or brand guide.`

B's need/requirements remain the chart fields above. A still explicitly requires editable SVG plus PNG. C retains the copy need. Recompute the execution-time seven-day expiry for all creates. This completely defines the five arguments for each negative create; only B's stated two fields differ.

Read the actual new IDs, owners and versions. If they happen to be A=4,B=5,C=6, versions=1, assessment arguments are `[[4,6,5],[1,1,1],[[4,6],[6,5],[5,4]]]`; these IDs are conditional, not real facts. Use verified IDs otherwise. An actual participant submits exactly one assessment after authorization.

Intended canonical vector for the conditional ring is `["FIT","FIT","NO_FIT"]`: B→A contradicts the mandatory SVG requirement. It is a semantic expectation, not a forced model return. IF the network finalizes successful agreement on a negative vector, require stored NOT_MATCHED, cycle_id=0, cycle_status=NONE, no new Cycle, no reservations and all three fresh Intents OPEN/cycle_id=0. Compare cycle_total before/after; existing positive ACTIVE Cycle remains unchanged. A successful negative business judgment is not a failed transaction. If the actual judgment unexpectedly accepts, preserve all evidence and STOP; do not confirm or silently change prompt/source.

## Ambiguous UNSURE plan — NOT FOR EXECUTION

A separate future authorized trio could replace B's offer with `Design one logo.` and limitations with `Delivery format, size, editability and delivery deadline are unspecified.` while A still requires SVG/PNG, size and deadline. The legal ring stays A→C→B→A. Expected B→A is UNSURE for material missing conditions, which should lead to NOT_MATCHED if valid negative agreement finalizes. Do not run now; prioritize one positive full cycle and one negative assessment. No guarantee that actual models choose the expected label.
