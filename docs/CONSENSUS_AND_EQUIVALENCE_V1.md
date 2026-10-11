# SCA-3 V1 Consensus and Equivalence

## Full Three-Edge Decision Equivalence

Structural validity means one native JSON object with exactly the `decisions`
key, whose value is a list of exactly three strings from FIT / NO_FIT / UNSURE.
No prose, extra keys, nested values, nulls or scores are accepted. The Leader
returns only that validated list, in canonical directed edge order.

Material equivalence means the Validator receives the SDK's actual `gl.vm.Return`
wrapper, validates the Leader's list, independently calls the native LLM on the
same immutable complete three-edge prompt, parses its own list, and compares
all three positions. It does not pass the Leader's verdict to its classifier.
A valid Leader always triggers a full independent classification before True
is possible. Invalid Leader wrappers/values are rejected before wasting an LLM
call. UserError, VMError, malformed Validator values and execution exceptions
return False; no error is treated as agreement.

| Leader | Independent Validator | Equivalence | Business outcome if accepted by network |
| --- | --- | --- | --- |
| FIT, FIT, FIT | FIT, FIT, FIT | True | MATCHED; PENDING commitment |
| FIT, FIT, FIT | FIT, UNSURE, FIT | False | This Validator disagrees |
| FIT, NO_FIT, FIT | FIT, NO_FIT, FIT | True | NOT_MATCHED; no reservations |

No convenience equivalence wrapper, vote counter, administrator, similarity
threshold or two-out-of-three-edge acceptance substitutes for these rules.
The network controls consensus rounds and final outcomes: one callback returning
False does not by itself establish final transaction rejection.

## Frozen Stable API

The checksum-verified official GenVM v0.2.16 artifact implements:

- `gl.vm.run_nondet_unsafe(leader_fn, validator_fn)`; validator argument is Result.
- `gl.vm.Return.calldata`, `gl.vm.UserError`, `gl.vm.VMError`.
- `gl.nondet.exec_prompt(prompt, response_format="json")`; JSON response is dict.

The unsafe API propagates Leader failures and treats Validator exceptions as
disagreement. This contract explicitly rejects errors instead of comparing two
errors as an accepted classification. Production closures capture only immutable
prompt text, not a contract/storage root. Both perform local parsing and one
native LLM call for all three edges; neither reads nor writes contract storage.
Captured closures also roundtrip through the pinned bundled cloudpickle.

The actual artifact paths/signatures/digests and pre-source-edit probe are in
`evidence/phase2/stable-api-probe.json`. Public docs were reviewed, but the pinned
artifact determines API compatibility; no newer SDK or network was selected.

## Deterministic state integration

`assess_cycle(intent_ids, versions, edges)` requires exactly three valid
participating Intents, existing Phase 1 topology/version/expiry/replay preflight,
and an actual participant caller. There is no supplied verdict argument.
It checks assessment/cycle counter capacity and prior assessment identity before
any native LLM call. It constructs the prompt from the frozen canonical snapshot.

After the VM returns, it strictly validates the vector, repeats full preflight,
compares exact snapshot content/identity, repeats caller/replay/counter checks,
and allocates a complete bounded local Assessment record before mutations.
Exactly three FIT decisions call the existing private `_reserve_accepted_cycle`,
which repeats preflight and produces PENDING with three false confirmation flags.
Other vectors persist NOT_MATCHED with cycle_id=0 and leave Intents OPEN.

The permanent `assessed_snapshots` index rejects identical negative snapshots,
including across callers/rotations, before a new LLM call. Positive replay remains
blocked by original reservations/proposals/declined rules. A version update creates
a new snapshot. Reversal remains a distinct assignment. Assessment records retain
the bounded canonical full snapshot so later Intent updates cannot erase negative
assessment evidence. They retain actual labels, proposer, transaction timestamp,
prompt version and digest. No fabricated vote/finality fields exist.

`get_assessment` reads stored data only. `cycle_status` is the related Cycle's
current effective state or NONE; `result` remains the original semantic outcome.
MATCHED is not ACTIVE; ACTIVE is agreement, not service delivery. No transaction
has been verified FINALIZED in this phase.

## Atomicity verification boundary

Predictable failures, including local record allocation and reservation
preflight failure, are tested against unchanged serialized storage **without
rollback**. Original INV-01–16 tests remain effective. A byte-layout check
restores Phase 1 persisted Intents/Cycle into a new Phase 2 root and finishes
confirmation; new root fields are appended after all original fields.

As with Phase 1's multi-record writes, unexpected storage/runtime faults after
the mutation block begins rely on GenVM transaction rollback. Direct Mode does
not provide that automatically. Three storage-fault tests explicitly simulate
the transaction boundary using its supported snapshot/revert API; they are
not proof of full WASM rollback. No production compensating-write/rollback
mechanism or fake Validator enforcement was added.

## Offline evidence limits

Direct Mode 0.29.2 runs the Leader, captures the Validator callback and returns
the Leader value immediately. It does NOT gate deterministic writes on network
consensus. `vm.run_validator()` explicitly executes the captured real production
callback against separate native LLM mocks. Agreement, each-position disagreement,
malformed results and independent calls are tested with that supported mechanism.

VM consensus termination is a separate fault-injection test of deterministic
failure handling; it is not fake voting or a replacement for captured callback
checks. Semantic fixture labels are canned expectations, not measured LLM
accuracy. Prompt/data boundaries and independent comparison are tested, but
systematic model error and prompt injection are not eliminated. Full GenVM WASM,
live consensus/finality, races and cross-platform execution remain NOT RUN.
