# SCA-3 V1 — Real onchain acceptance plan

DOCUMENTED BUT NOT EXECUTED. No deployment or network contract execution exists for this project in Phase 4A. Direct Mode, canned labels, isolated native WASM and a Leader result alone cannot prove independent Validator consensus.

## Evidence per future write

Archive actual signer, Stable chain ID, canonical source hash, method and exact submitted arguments (including execution-time expiry), transaction hash, original status/receipt, execution result, method return, independent Validator/round/vote information when exposed, actual copied Explorer detail URL, relevant final read results and full error/trace if unsuccessful. Record timestamp and fee estimate/budget/consumption separately. Include raw JSON or screenshots; do not replace raw evidence with a summary. No private material.

PENDING means awaiting processing. ACCEPTED is a materialized consensus stage and is not FINALIZED. FINALIZED establishes protocol finality but may accompany execution failure. SUCCESSFUL EXECUTION requires the actual successful Return/result and verified state; FAILED EXECUTION requires preserving the error and must not be accepted as success. UNDETERMINED has no accepted outcome. VALIDATOR DISAGREEMENT may belong to one round and is not necessarily the final outcome; archive all rounds/rotations and stop for review if the final decision is not verifiably successful. Do not use newer numeric status codes to interpret Stable without actual endpoint evidence.

Require durable FINALIZED AND successful execution before accepting every important write. For assess_cycle additionally require independent network Validator agreement evidence (for example actual MAJORITY_AGREE/consensus result and participants/rounds if the Stable receipt exposes these fields), not just Leader output. If unavailable, mark the consensus acceptance gate BLOCKED rather than fabricate votes. Discover the actual Stable receipt shape using the future real hash and preserve it.

## Positive gates

1. Deployment finalized successfully, actual address recorded, uploaded source identity verified, fresh get_protocol_stats(0,50) matches the execution package.
2. Three distinct actual owners create Intents. Every create finalizes successfully. Read owners, terms, versions, expiry, OPEN and cycle_id=0; derive actual IDs rather than assume 1/2/3.
3. Participant assess_cycle on A→C→B→A finalizes with successful execution AND actual independent full-ring agreement evidence.
4. Persisted get_assessment(actual_id) reports MATCHED, three FIT decisions, actual topology, proposer, prompt version/hash and positive cycle_id. get_cycle(actual_id) shows PENDING, immutable terms, three owners, versions/edges, correct snapshot, zero flags and deadline. Three get_intent reads show RESERVED with that cycle.
5. A/B/C confirm the exact same real snapshot with their distinct actual addresses before the deadline. Each transaction finalizes successfully. Read after each: 1/2/3 confirmations; first two PENDING, third ACTIVE. Final three Intents are CONSUMED; their cycle_id is identical.
6. Repeat read-only queries to reproduce final state. Final assessment remains MATCHED and current cycle_status=ACTIVE. On a fresh isolated positive-only run, stats show intent_total=3, assessment_total=1, cycle_total=1, active_total=1, CONSUMED page count=3. If other operations exist compare deltas instead of imposing these totals. ACTIVE proves commitment, never service delivery.

## Negative gates

Use three fresh, genuinely incompatible Intents from the vectors; no consumed reuse. Archive before/after stats and positive Cycle state. One successful finalized negative assessment with independent Validator agreement must persist NOT_MATCHED, one or more NO_FIT/UNSURE labels, cycle_id=0/cycle_status=NONE, no new Cycle, no reservations and all valid negative Intents OPEN/cycle_id=0. On a fresh positive-plus-negative-only run: six Intents, two Assessments, one ACTIVE Cycle. A successful business rejection is not a transaction error. Unexpected FIT acceptance is a semantic finding: preserve evidence, stop, never confirm it or relabel it PASS.

## Residual limitations and stop

Actual real-node rollback for unexpected mid-write failures remains UNVERIFIED. Do not deliberately inject destructive hosted storage faults. Normal successful transactions do not close this risk. If documented node guarantees and safe separately authorized evidence cannot close it, keep it as a residual limitation. Real model correlated errors, prompt injection, live races, finite growing history, version-based retries and real resource limits remain distinct risks. Source/prompt/equivalence changes require a separate review, never a silent patch to obtain acceptance.

No Portal, Repository B, frontend or later phase work is authorized here. Do not turn this plan into transactions in Phase 4A.
