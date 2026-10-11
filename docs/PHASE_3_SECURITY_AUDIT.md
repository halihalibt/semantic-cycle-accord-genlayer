# SCA-3 V1 — Phase 3 Security Audit

Status: local security closure complete, awaiting independent review. No confirmed
production defect was reproduced; canonical source is unchanged. Findings below
are explicitly distinguished from exploitable implementation vulnerabilities.

## Verified baseline and reviewed material

Account/owner halihalibt; PUBLIC; MIT. GitHub PR #1 and #2 were verified MERGED.
Main and local clone: `87fb4c080f6a9c9518e7eb345af0991a24003c47`.
Source SHA256: `88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442`.
Prompt SHA256: `8a7b279a3594397802c71fef4df9b4d30db1ff528177d0bf05c80a62397192d3`.
Original 505 tests actually reproduced before new coverage. The README, checkpoint,
master plan, protocol, state machine, all 16 invariants, Stable compatibility,
prompt, equivalence, Phase 2 report/acceptance, canonical source, verifier, every
existing test module/fixture and Phase 2 results/API probe were inspected.
Historical PR status statements were not treated as current GitHub state.

## Findings register

Severity is impact of the stated risk, not a claim of a reproduced exploit.
No critical/high confirmed vulnerability; CONFIRMED FIXED: none;
CONFIRMED UNRESOLVED production vulnerability: none. No source patch was justified.

| ID | Severity | Affected function / area | Reproduction / root cause | Remediation / regression | Status | Remaining risk |
| --- | --- | --- | --- | --- | --- | --- |
| S3-01 | Medium, runtime dependency | All multi-record write blocks | Direct Mode last-write faults visibly retain partial state; runtime/node controls commit | 27 cases in test_storage_write_faults_explicit_host_boundary; no fake production compensation | NOT TESTED for actual node rollback | Successful smoke does not prove failure rollback or chain atomicity |
| S3-02 | Medium, semantic | _assessment_prompt, _classify, _consensus_decisions | Independent models can share errors; mocks choose their own canned labels | Existing parser/Validator suite plus Unicode and maximum-input tests; trusted prompt unchanged | DESIGN LIMITATION | Real prompt-injection success rate and semantic false acceptance NOT TESTED |
| S3-03 | Low, long-term capacity | create_intent, owner indexes, TreeMaps | Repeated create/cancel grows retained history; SDK DynArray length and storage offsets use u32 | 200-record probe, 5 slots, 50-item pages; existing capacity/history tests | DESIGN LIMITATION | Finite SDK storage capacity precedes u64 ID exhaustion; no global history cap or exact maximum measured |
| S3-04 | Low, cost/griefing | update_intent → assess_cycle | Same text update increments version; new snapshot may request fresh AI; failed consensus does not persist replay marker | test_negative_version_retry_and_history_growth_are_explicit_design_limits | DESIGN LIMITATION | Participant can repeat versions/failed attempts; no per-wallet rate budget in frozen protocol |
| S3-05 | Informational | Public calldata/type boundary | Malformed container may raise TypeError; float/surrogate rejected by SDK encoder | test_malformed_ring_containers_fail_before_native_llm; integer/text tests check bytes unchanged | NOT REPRODUCED as state/acceptance bypass | Exact error presentation differs by failure layer; no API redesign applied |
| S3-06 | Informational | Public authorization and consensus paths | Attempted outsider actions, malformed vectors/wrappers, stale/corrupt snapshots | Existing full suite and added adversarial cases | NOT REPRODUCED | Local tests do not establish live consensus or concurrency |

No substantive prompt, equivalence, persistent schema or API change is proposed.
Fixing cumulative capacity with a new data layout, or preventing version-based
reassessment with changed business rules, would require separate authorization.
These design limits do not create a locally reproduced unauthorized activation.

## Public attack surface review

| Method | Authorization / authoritative data | Failure and resource review |
| --- | --- | --- |
| create_intent | Permissionless; owner derived from actual sender | 4×512 UTF-8 bytes; validity and 5 effective slots; u64 counter checked before writes |
| update_intent | Actual owner, expected version, unexpired OPEN | Text/validity/version-overflow checked before replacement; no owner override |
| cancel_intent | Actual owner/current version; eligible reservation checks | Full frozen snapshot and finish-counter before abort; target cancelled after release |
| assess_cycle | Actual member of authoritative 3-owner ring | Shape/ring/version/expiry/replay/counters before AI and again after; no supplied verdict |
| confirm_cycle | Actual frozen participant and same supplied snapshot ID | Full three-record verification, deadline and final counter before any flag; duplicate eligible confirmation no-op |
| decline_cycle | Actual frozen participant, same snapshot | Full verification and counter before marker; releases only own eligible reservations |
| expire_cycle | Intentionally permissionless | Deadline and PENDING required; all records resolved/counter checked before cleanup; repeated EXPIRED no-op |
| get_intent | Public record by validated positive ID | Detached view, no AI, no protocol write |
| get_cycle | Public frozen/effective state by ID | Detached lists; no caller-controlled state |
| get_assessment | Public persisted assessment by ID | Stored result, prompt hash and canonical evidence; current cycle status is derived; no fabricated votes/finality |
| get_intents_page | Public, validated offset and 1–50 limit | At most 50 records; out-of-range offset yields empty page |
| get_cycles_page | Public, validated offset and 1–50 limit | At most 50 three-party records |
| get_owner_records | Public valid address; independent history pages | At most 50 of each kind plus bounded 5 slots; deliberately public history |
| get_protocol_stats | Public, validated page | Cumulative counters distinct from effective page counts; at most 50 Intents |

Internal functions are undecorated and absent from SDK schema. No external
contract calls or message sends occur; there is no public reentrancy callback.
Native nondeterministic closures capture immutable prompt text only. The actual
Return wrapper and exact 3-label vector are required; errors cannot authorize
acceptance. Every valid Validator independently executes all three classifications
on identical authoritative input without receiving Leader decisions as evidence.
Negative agreement remains NOT_MATCHED; exact negative replay rejects before LLM.

Invalid calldata, Unicode surrogates, corrupted owner/content/version fixtures,
terminal operations, overlaps and bad snapshots reject without new writes.
Synthetic corruption tests probe defense in depth; they are not evidence that a
public caller can modify storage directly. Repeated views and mutation of returned
objects do not mutate authoritative storage. INV-01–16 remain covered unchanged.

## Multi-record transition and atomicity map

Storage assignments below also expand into multiple SDK byte writes. Injections
operate at actual InmemManager.do_write calls, not just top-level map assignments.

| Transition | Ordered logical writes | Predictable failures before first mutation | Runtime failures / evidence boundary |
| --- | --- | --- | --- |
| Create Intent | Intent; working slots; optional owner history init; append history; intent_count | Text, expiry, capacity, u64 counter | Allocation/SDK capacity/persistence during block needs VM/node boundary; first/middle/last injected |
| Update Intent | Replace full Intent record | Owner, expected version, OPEN, expiry, text, version capacity | Replacement serializes multiple fields; 3 injected boundaries |
| Cancel OPEN | status CANCELLED; cycle_id 0 | Owner/version/expiry/cancellable | 3 injected boundaries |
| MATCHED assessment | Cycle; each Intent RESERVED+cycle ID; optional owner cycle index init/append; proposals; cycle_count; Assessment; assessed_snapshots; assessment_count | Full pre/post consensus checks, local Assessment construction, reservation preflight | Unexpected failure between any subwrites requires commit boundary; 3 added byte-level and original map faults |
| NOT_MATCHED assessment | Assessment; assessed_snapshots; assessment_count | Same eligibility/replay/counter/output checks | 3 added byte-level boundaries; Intents stay OPEN |
| First/second confirmation | One confirmation flag | Participant/hash/full snapshot/deadline | Runtime write failure requires boundary; existing tests cover predictable failures |
| Third confirmation | Confirmation flag; 3 CONSUMED statuses; ACTIVE; active_count | Same checks plus active_count capacity | 3 byte-level boundaries; no early flag or consumption on predictable failure |
| Decline | declined marker; eligible release statuses+cycle IDs; ABORTED; aborted_count | Participant/hash/snapshot/counter, all records exist | 3 boundaries; original snapshot/overflow safety retained |
| Reserved cancellation | eligible release statuses+cycle IDs; ABORTED; aborted_count; target CANCELLED+cycle ID 0 | Owner/version/expiry/snapshot/finish-counter | 3 boundaries including final target cancellation |
| Expiration cleanup | eligible release statuses+cycle IDs; EXPIRED; expired_cycle_count | PENDING/deadline/all records/counter | 3 boundaries; foreign and terminal records never reopen; repeat no-op |

Tests first execute a successful transition to locate actual byte-write count,
restore its disposable fixture, then inject first/middle/last write failure.
First-write failure leaves bytes unchanged. Last-write failures retain partial
Direct Mode writes before manual vm.revert; after manual restoration all serialized
bytes match. This explicitly demonstrates why these are host-boundary simulations,
not proof of automatic transactional rollback. Actual node commit/discard behavior
and unexpected failures inside genuine WASM remain NOT TESTED.

## Resources and prompt/data trust

Each field is at most 512 UTF-8 bytes. Exactly 12 fields participate in a snapshot
and a 3-edge prompt. JSON control escaping and delimiter escaping can expand an
ASCII byte to 6 bytes. Including u64 decimal identifiers/timestamps, owners/domain,
keys and frozen instructions gives conservative bounds below 38,000 snapshot and
45,000 prompt UTF-8 bytes. Maximum-NUL sample measured 37,169 / 41,112 bytes;
local Python peak allocation 177,178 bytes for that sample, not a universal VM cap.
Fixed fields prevent unbounded contract prompt loops on supported normal inputs.
LLM response allocation/JSON parsing and incoming calldata decoding occur partly
inside SDK/runtime, before strict 3-element contract validation; network quota,
maximum response and calldata limits have not been measured.

200 repeated maximum-field create/cancel operations retained 441,043 nonzero
serialized bytes. 50-item owner pages required 2,019 SDK reads at history 50 and
2,350 at history 200, with zero SDK writes. TreeMap lookup grows with tree depth;
contract code does not scan complete history. Working slots stayed 1 in this probe.
No network gas number or practical maximum total history size is inferred.

Multilingual roles, malicious Markdown/fences, JSON-breaking strings, delimiter
escapes, bidi/isolation controls, NULs and maximum valid Unicode remain structured
untrusted data. Tests preserve all independent edges and unchanged trusted prompt.
They do not establish AI immunity or real semantic accuracy. Counter and snapshot
rechecks, strict parsing and Validator independence remain mandatory.

## Genuine offline WASM feasibility

Official release v0.2.16 source was inspected at commit
`387e1a66e920cb2dfadcdce40ab2d28da02efd1e`; executor host ABI and CLI were used.
Checksum-verified official Linux executor and runtime archives, unchanged universal
runners, and the bundled musl loader allow isolated execution in this environment.
No Localnet, GLSim, Studio-dev, manager service, wallet, deployment or LLM service
was installed or used. A disposable AF_UNIX socket-pair host serves storage reads
and receives native FullResult. Successful Return deltas are committed to its
local byte map using the documented big-endian page-index format.

Constructor → get_protocol_stats → create_intent → get_intent all returned Return,
process exit 0. Native logs identify v0.2.16 and cpython.det.wasm. View deltas were
0; constructor/create delta counts 4/14. No LLM/web module calls occurred.
This proves only these isolated paths. It is neither a network deployment nor
network-finalized execution. The runner exposes host storage deltas rather than
a standalone node transaction-rollback test method; no automatic rollback assertion
is made. Full production assessment/Validator WASM and real node rollback remain
NOT RUN. See exact commands/stdout/native stderr in offline-wasm-results.json.
