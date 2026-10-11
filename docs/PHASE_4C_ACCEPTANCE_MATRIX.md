# SCA-3 V1 — Phase 4C final acceptance matrix

Final positive/negative business results and the 11 successful finalized writes
are independently verified. PARTIAL means original user screenshot evidence
exists but original historical machine-readable reads were not acquired; it is
not relabeled as an independent raw PASS. UNKNOWN/UNAVAILABLE are evidence gaps,
not fabricated fields. NOT RUN is work not performed in this phase.

| Gate | Requirement | Actual result | Basis / limitation |
| --- | --- | --- | --- |
| G01 | Baseline, public owner, network and frozen deployment source/Prompt | **PASS** | GitHub main, chain-id, fresh deployment raw/source-identity |
| G02 | 11 transaction hashes, calldata, cryptographic signers, successful Returns and finality | **PASS** | 33 raw records; signed domain/payload recovery |
| G03 | Six exact frozen create vectors, IDs, owners, versions and valid expiry | **PASS** | Original raw calldata + fresh final get_intent |
| G04 | Historical post-create OPEN/zero-cycle read gates | **PARTIAL** | Original user screenshots present; original raw historical reads unavailable |
| G05 | Positive full-ring AI acceptance beyond Leader-only output | **PASS** | 3 agree/2 idle; Accepted; two non-Leader successful LLM Validator receipts |
| G06 | Assessment #1 MATCHED, FIT/FIT/FIT, topology, source Prompt hash and original snapshot | **PASS** | Fresh final get_assessment + raw Leader eq output + reconstructed digest |
| G07 | Historical zero-confirmation PENDING / RESERVED and count 1/2 reads | **PARTIAL** | Original screenshot evidence; no independently acquired historical raw state |
| G08 | Three distinct confirmations of identical snapshot before deadline | **PASS** | Recovered A/B/C signatures, exact calldata and true Returns |
| G09 | Cycle #1 ACTIVE/count 3; #1–#3 CONSUMED and cycle_id 1 | **PASS** | Fresh latest-final reads, repeated Cycle read |
| G10 | Negative full-ring NO_FIT acceptance, NOT_MATCHED/0/NONE | **PASS** | Raw accepted consensus, Leader eq output, final/repeated Assessment #2 |
| G11 | Negative #4–#6 OPEN/0; no new Cycle; original ACTIVE cycle/snapshot retained | **PASS** | Six intent reads, cycle-2 not found, full Cycle page, repeated Cycle #1 |
| G12 | Original machine-readable before-negative counters | **PARTIAL** | User screenshots of positive-only counters present; original raw counter read absent |
| G13 | Final counters 6/2/1/1 and 3 CONSUMED/3 OPEN/0 RESERVED | **PASS** | Full statistics page and second independent matching read |
| G14 | Original consensus histories/votes/leader results/rounds/rotations retained | **PASS** | Full raw transaction objects; agree/idle/cancellation distinction |
| G15 | Original screenshots, evidence schema shapes, checksums, links and scope | **PASS** | 60 original metadata records/private byte verification + public checksum manifest |
| G16 | Actual fee estimate/budget/consumed GEN | **UNKNOWN** | Compatibility receipt fields preserved; no inferred fee |
| G17 | Raw independent Validator response text/full runtime prompt transcripts | **UNAVAILABLE** | Votes and token statistics acquired; separate response text not exposed |
| G18 | Contract regression suite in this evidence-only phase | **NOT RUN** | Historical 566 PASS retained as historical |
| G19 | Unexpected mid-write real-node rollback | **NOT RUN** | No deliberately injected faults |
| G20 | Actual service delivery / complete production security certification | **NOT RUN** | ACTIVE is accepted commitment only |

| G21 | Public original PNG publication | **BLOCKED** | Automatic approval review rejected; explicit public-disclosure approval needed |

Original PNG publication is BLOCKED by automatic approval review pending explicit
public-disclosure approval; originals remain private and are not in this PR.

No FAIL or unexpected semantic acceptance was found in the acquired evidence.
The historical-read requirements remain PARTIAL; the package does not claim
that every acceptance gate has independent original raw evidence.
See [report](PHASE_4C_REPORT.md) and [evidence index](PHASE_4C_E2E_EVIDENCE_INDEX.md).
Draft publication is the stop boundary; merge is not authorized.
