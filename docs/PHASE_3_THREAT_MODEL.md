# SCA-3 V1 — Phase 3 Threat Model

Scope: the frozen Repository A contract at main
`87fb4c080f6a9c9518e7eb345af0991a24003c47`, Stable Studionet 61999 only.
No product redesign, schema/API change, wallet or network execution is included.

## Assets and trust boundaries

Protect actual Intent ownership, immutable directed snapshot identity, version
freshness, exclusive reservation, three independent confirmations, permanent
replay indexes, honest Assessment evidence and coherent counters/indexes.
All service text and public calldata are hostile. Owners may collude or submit
misleading descriptions. An outsider may call any public method or read history.
A participant may replay calls, reorder/rotate/reverse a ring, race competing
proposals or intentionally cause classification disagreement.

The SDK supplies sender/contract addresses and transaction time; users cannot
supply an authoritative owner, clock, verdict or confirmation flag through the
public API. The runtime/node controls serialized transaction execution, consensus
termination, resource quotas and committing successful state deltas. Those are
explicit trust boundaries, not properties proved by Direct Mode.

Leader and Validators may disagree, return malformed classifications or make a
shared semantic mistake. Independent classification and exact equality constrain
acceptance, but do not establish truth or eliminate correlated model failures.
No administrative actor, funds, private keys, service-delivery verifier, reputation
system or fulfillment guarantee is part of this contract.

## Attacks and controls

| Attack | Existing control | Evidence level / remaining condition |
| --- | --- | --- |
| Impersonate another owner | SDK sender; owner and frozen-participant checks | Offline unauthorized writes reject; actual node identity remains trusted |
| Inject verdict / call reservation seam | Exact 14-method schema; undecorated private helpers | SDK schema, AST and captured callbacks; no public verdict field |
| Reorder or substitute terms | Direction-preserving rotation; version/content/domain digest | INV-01–09 and fixed-seed metamorphic tests |
| Reserve twice / overlap cycles | Full OPEN/unreserved preflight, repeated after nondeterminism | Offline sequential overlapping calls; live scheduling NOT TESTED |
| Activate early / replay confirmation | Three owner-indexed flags; snapshot check before each flag | Deterministic lifecycle and terminal-state tests |
| Manipulate model through text | Frozen trusted prompt, escaped JSON/delimiters, strict parser, independent full-ring Validator | Mock orchestration only; real injection immunity NOT TESTED |
| Fail during persistence | Predictable preflight plus runtime/node commit boundary | 27 actual SDK write fault cases, manual restoration; actual node rollback NOT TESTED |
| Exhaust resources | 512-byte fields, 3 edges, 5 working slots, 50-record pages, u64 counter checks | Local measurements; persistent histories and retries remain design limits |

## Accepted limits of this audit

All records are deliberately public; do not place secrets in service descriptions.
ACTIVE represents acceptance of a commitment, never performance of services.
No financial or identity verification is asserted. Zero-cost development does not
mean production AI/storage can never consume network resources. This audit adds
no deposits, rate tokens, private data controls or alternative network.
