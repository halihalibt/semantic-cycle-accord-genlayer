# Phase 2 Test and Acceptance

The historical 229-test baseline was reproduced before source edits: 229 PASS,
0 FAIL, 0 SKIP. Its historical source/evidence are untouched. The final exact
counts, collected node IDs and checks are in `evidence/phase2/local-results.json`.

## Executed coverage

| Area | Evidence |
| --- | --- |
| Canonical prompt | Exact doc/constant/hash, all 15 rules, three complete edges, UTF-8, stable order, rotations, reversed direction, all four fields |
| Parser | Every one of 27 vectors; malformed JSON/wire values, missing/extra fields, invalid labels/types, null, nested and oversized output |
| Independent Validator | Actual captured callback via vm.run_validator; native JSON mocks; same complete input, separate LLM call, each-edge and multi-edge disagreement, negative agreement, wrappers/errors/exceptions, serialized closures |
| Integration | Every one of 27 business outcomes, correct persisted labels/snapshots, MATCHED linking PENDING, negative OPEN/no reservations, distinct changed/reversed snapshots |
| Replay | Unchanged negative across three callers and three rotations triggers no new LLM; positive/declined/expired proposal protections retained |
| Safety | Pre-LLM invalid owner/topology/caller/state/version/expiry/counters; post-block caller/content/version/state/expiry/replay/counters; invalid VM result and failed VM execution |
| Atomicity | Complete normalized storage unchanged without rollback for predictable/local-allocation/preflight errors; explicit boundary simulation for cycle/assessment/replay storage faults |
| Lifecycle | Three simulated senders confirm independently to ACTIVE/exactly three CONSUMED; decline/cancel/expiry regressions after public assessment |
| Injection | Eight adversarial strings across four fields plus native independently disagreeing Validator; escaped delimiter/JSON boundaries; no public verdict argument |
| Persistence | Pinned cloudpickle root, bytes/new manager, positive and negative restoration, resumed confirmation; actual frozen Phase 1 bytes readable using appended Phase 2 fields |
| Schema | Exact 7 writes / 7 views; missing/extra/private/verdict-setter methods and readonly errors reject; SDK export and calldata |
| Regression | All original deterministic invariant coverage; AST comparison proves original methods/fields/signatures retained except documented stats additions |

## Intended semantic fixtures

Every row has full source text and expected decision in
`tests/consensus/classification-fixtures.json`. Tests submit that source through
the native LLM mock, inspect all three prompt edges, invoke the captured Validator,
and verify persistence/state effects. These tests do **not** prove a real model
would choose these labels. All three edges use each fixture's same terms.

| Fixture | Intended label | Basis |
| --- | --- | --- |
| affirmative_fit | FIT | Every stated deliverable and material requirement is affirmatively supported. |
| explicit_exclusion | NO_FIT | Mandatory artwork is explicitly excluded. |
| quantity_mismatch | NO_FIT | Two articles cannot meet an explicit minimum of five. |
| format_mismatch | NO_FIT | Required vector format is excluded. |
| language_mismatch | NO_FIT | Mandatory Chinese output conflicts with the English-only scope. |
| deadline_mismatch | NO_FIT | Earliest supported delivery misses the mandatory deadline. |
| scope_mismatch | NO_FIT | Explicitly excluded research and rewriting are required. |
| similar_keywords | NO_FIT | A shared code-review topic does not supply the required security analysis. |
| ambiguous_scope | UNSURE | Vague help does not affirmatively establish video editing capability. |
| missing_material_information | UNSURE | Provider does not state supported translation language. |
| contradictory_critical_limitation | UNSURE | Conflicting statements prevent reliable acceptance. |
| partial_compatibility | NO_FIT | One supported deliverable cannot compensate for the excluded video. |
| multilingual_fit | FIT | Chinese material terms are explicitly satisfied. |

## Exact Phase-1-only expectations adapted

1. `test_stats_effective_pages_and_lifecycle_counters`: matching availability
   False -> True; adds assessment_total=0 for fixture-only historical cycles.
   Existing state/page/counter assertions are retained.
2. `test_only_authorized_public_surface_and_no_ai` becomes
   `test_only_authorized_public_surface_and_no_bypass`: adds exactly the two
   approved methods; permits required run_nondet/exec_prompt calls; retains all
   convenience-wrapper/mock/private-key restrictions. The word "requests" in
   the frozen prompt is data, so forbidden external libraries are now checked
   as AST imports, including import-from, rather than as prose substrings.
3. Schema expected names/strict flags expand 12 -> 14. The extra-method rejection
   for formerly absent assess_cycle becomes set_assessment_verdict rejection;
   private seam, arbitrary injected verdict and unexpected view still reject.
   Missing-name and reversed-readonly parameterizations automatically add four
   cases for the two approved methods. No test is deleted or skipped.

The resulting suite retains/adapts 229 baseline cases, adds four schema cases,
and adds the new consensus/integration/security cases named in local-results.

## Actual verification levels

Reproduce with `uv sync --frozen`, `uv run python scripts/bootstrap_sdk.py`, then
`uv run python scripts/verify_local.py`. Python and uv.lock are unchanged.
Socket connections are blocked in tests. Baseline byte-layout subprocess also
blocks socket access and loads only the already cached v0.2.16 artifact.

The verifier runs full pytest, Ruff lint/format, pinned GenVM AST/SDK semantic
validation and strict SDK public schema validation. Evidence contains the actual
stdout, schema, lint JSON, collected cases, artifact digests and canonical hashes.

Storage-allocation/preflight errors are checked without rollback. Unexpected
mid-write storage faults use explicitly simulated transaction rollback and
remain a full-WASM verification limitation. Direct Mode does not enforce real
consensus. No deployment, transaction, signature, wallet operation, paid API,
real model evaluation, network race, live finality or frontend was tested.
