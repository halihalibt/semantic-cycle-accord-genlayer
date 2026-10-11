# Deterministic Invariants and Executed Coverage

All invariants below are implemented in the canonical contract and exercised
offline. Reservation uses the internal accepted-result seam; no test provides
real semantic consensus evidence.

| Invariant | Enforcement | Representative executed tests |
| --- | --- | --- |
| INV-01: exactly three distinct Intent IDs | Cardinality and uniqueness preflight | bad_topology_atomic, valid_ring_snapshot_and_rotation |
| INV-02: exactly three owners | Authoritative owner set has size three | duplicate_owner |
| INV-03: complete directed ring | Each edge must be source to next recipient | bad_topology_atomic, reversed_ring_and_contract_network_identity |
| INV-04: valid, unexpired, version-matched and available | Re-read all three immediately before reservation | expired_matching_boundary, changed_terms_change_identity_and_reject_old_version |
| INV-05: no simultaneous double reservation | OPEN and cycle_id=0 required for every Intent | second_cycle_cannot_reserve_or_consume_shared_intent |
| INV-06: only own participation can be confirmed | Actual sender must match one frozen owner | unrelated_wallet_and_wrong_digest |
| INV-07: one effective confirmation per owner | Own flag; repeated eligible confirmation returns False | duplicate_confirmation_noop |
| INV-08: original immutable snapshot | Full authoritative terms, ring, canonical JSON and digest checks | authoritative_intent_substitution_rejected_atomic, supplied_digest_cannot_authorize_substituted_snapshot |
| INV-09: stale/invalid/expired cannot activate | All snapshots and deadlines checked before each flag | expiration_before_final_activation_has_no_partial_consumption, corrupt_cycle_metadata_rejected |
| INV-10: all three confirmations required | PENDING until three distinct flags true | three_separate_confirmations_and_terminal_consumption |
| INV-11: consume exactly once | All three consumed in activation block; ACTIVE terminal | three_separate_confirmations_and_terminal_consumption, terminal_cycle_immutable |
| INV-12: release only own eligible reservations | Complete three-record preflight; state and cycle_id guards | cleanup_releases_only_its_reservation, cleanup_never_reopens_terminal_intent, earliest_intent_deadline_and_no_reopen_expired |
| INV-13: identical proposals cannot duplicate commitments | Permanent domain-separated snapshot identity map | duplicate_proposal_and_rotation_no_new_cycle, expired_identical_proposal_not_replayed |
| INV-14: declined identical snapshot requires version change | Declined identity independent of proposer | declined_snapshot_blocked_across_callers_until_version_change |
| INV-15: actual caller and current storage validated | No caller override input or operator path; owner/participant checks | non_owner_rejected, decline_unauthorized_and_mismatched_digest_atomic, missing_write_target |
| INV-16: failed validation leaves no partial state | Preflight before mutation, including cleanup | bad_topology_atomic, update_validation_atomicity, cleanup_missing_record_preflight_is_atomic, overflow and snapshot corruption tests |

Storage comparisons use actual serialized SDK storage bytes. The in-memory
manager may allocate zero-filled buffers on reads; tests normalize these read
allocations so they do not mistake a read for a protocol write. No failure test
uses rollback to conceal partially modified state.

## Phase 1 hardening amendment — INV-16

Final confirmation checks active_count before changing its flag or consuming
Intents. A private counter preflight runs before _finish releases reservations
and before decline writes its replay marker. Cancellation and expiration inherit
the _finish preflight. At MAX_U64 these four public paths reject with
COUNTER_OVERFLOW and preserve serialized storage. At MAX_U64 - 1 all four
transitions succeed; non-final/duplicate confirmations retain their semantics.
Executed cases: test_terminal_counter_overflow_leaves_all_storage_unchanged,
test_terminal_counter_last_increment_succeeds and
test_nonfinal_and_duplicate_confirmations_preserved_at_counter_limit.
