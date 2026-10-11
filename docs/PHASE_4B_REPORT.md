# SCA-3 V1 — Phase 4B real deployment evidence closure

**DEPLOYMENT VERIFIED — INITIAL STATE VERIFIED — DRAFT REVIEW — STOP BEFORE PHASE 4C**

Repository A: halihalibt/semantic-cycle-accord-genlayer (public, MIT).
Approved Phase 4A merged main baseline: `61f2149996be02a0da4646082a66f3f03a3cb33c`.
Branch: `phase4b-real-deployment-evidence`. The user personally deployed; this
phase performed read-only verification and evidence publication only.

## Verified deployment and source identity

| Field | Verified value / evidence |
| --- | --- |
| Network | Stable Studionet, eth_chainId `0xf22f` / 61999 |
| Contract | `0x84e9284448D4cd16dcBBCbd8104449B11209C6F0` |
| Transaction | `0x3bf2036d9683c6ab55b09cacf54bdeb8ecfa7cb8e7864b832ae7041067f196cc` |
| Deployer / origin | `0x22Acaa233b7b985b36ef168F2DE9295334065B15` |
| Finality | gen_getTransactionStatus and transaction object: FINALIZED |
| Successful execution | eth receipt status `0x1`; original Leader receipt execution_result SUCCESS; user Explorer Return screenshot |
| Consensus | Original consensus_history: one `Accepted` round |
| Source | 32,040 decoded transaction contract_code bytes, byte-for-byte identical to canonical repository source |
| SHA256 | `88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442` |
| Trusted prompt constant SHA256 | `8a7b279a3594397802c71fef4df9b4d30db1ff528177d0bf05c80a62397192d3` |
| Constructor | Original calldata `Bg==`, decoded as `[]`; no arguments |
| Initial validators / rotations | User overview screenshot: 5 / 0; raw data has 1 Leader + 4 Validator receipts and one Accepted round |

Full original requests, timestamps, stdout responses and transport exit codes
are in `evidence/phase4b/rpc-queries.json`. No transaction fields were filled from
assumptions. Source comparison used decoded transaction `data.contract_code`,
not a screenshot or local filename. The exact prompt was extracted via AST from
the unchanged source. Original Leader result bytes are `0000` (`AAA=`); Return
and null are visible in the supplied Explorer execution screenshot.

## Actual consensus evidence

The raw votes map records **3 agree (including the Leader address) and 2 idle**.
The 4 Validator receipts contain 2 SUCCESS/agree and 2 ERROR/idle. Both idle
receipts explicitly say `Validator execution cancelled after quorum`, with
`CONSENSUS_VALIDATOR_QUORUM_REACHED`. Preserve these cancellation records;
never rewrite them as five successful agreeing Validators, five independent
semantic classifications, or a failed deployment. Leader SUCCESS, accepted
round, FINALIZED status and initial persisted reads establish deployment success.
Addresses and individual receipt outcomes are in deployment-record.json;
complete receipt and monitoring histories remain in rpc-queries.json.

Deployment initializes deterministic state. It does not call `assess_cycle`.
Model names in node configuration do not prove that any LLM was invoked.
`semantic_matching_available=true` indicates an implemented path, not successful
live AI matching. No MAJORITY_AGREE literal was invented.

## Independent initial read

A single `gen_call` used type read, the public deployer address as from, exact
`get_protocol_stats` arguments `[0,50]`, and `latest-final`. No signing account,
private key or client wallet was instantiated. Frozen-lock genlayer-py 0.16.3
calldata helpers encoded/decoded the request/result; no dependency was upgraded.
The raw response and exact request are archived. `initial-state.json` contains
the decoded output, independently matching the supplied screenshot:

- protocol SCA-3-V1; network_id 61999; semantic_matching_available true.
- intent_total, cycle_total, assessment_total, active_total, aborted_total and
  expired_cycles_cleaned all 0.
- CANCELLED, CONSUMED, EXPIRED, OPEN and RESERVED page counts all 0.
- offset 0, next_offset 0, has_more false.

This establishes the observed empty state at the recorded read time, not a
permanent guarantee that other callers cannot subsequently write.

## Raw-data caveats and remaining limitations

The compatibility receipt has contractAddress null, blockNumber `0x0`, and
blockHash equal to the transaction hash. Its to/log address and the transaction
`data.contract_address` link to the actual contract, independently readable.
Do not reinterpret compatibility block/gas fields as conventional EVM evidence.
Receipt gasUsed `0x7a1200` and effectiveGasPrice `0x0`, transaction gaslimit 48,
nonce 48, and Leader/Validator gas_used fields are preserved exactly; none
establishes the real GEN fee. Fee estimate, user budget and consumed GEN remain
UNKNOWN. No signature transcript was acquired; transaction r/s/v are null.

Explorer home returned a server-side application error (Digest 2144917332)
in this browser. No verified deep Explorer detail URL was obtained; its field
remains null. The supplied Explorer screenshots are original user evidence,
not screenshots captured by this phase. The Studio screenshot also contains
schema-query errors whose full stderr is not visible/acquired. These are retained
as a UI limitation and were not hidden by modifying production source.

Real semantic accuracy, independent AI classification, three-wallet E2E,
reservations, confirmations, ACTIVE cycle, negative acceptance and unexpected
mid-write real-node rollback remain UNVERIFIED / NOT RUN. ACTIVE, when eventually
reached, means accepted commitment, never delivery.

## Validation and stop

Evidence assertions passed: baseline, chain, address/deployer, finality, receipt,
source byte identity/hash, prompt hash, accepted round and empty initial state.
JSON parsing, local document links, screenshot byte checksums and git scope
integrity were checked. Production source, Canonical Prompt, specifications,
tests, lockfile and all historical evidence remain unchanged. No regression
suite was rerun for this documentation/evidence-only phase; prior 566 PASS is
historical, not a new result. Publication metadata identifies the actual
published package commit and PR; final branch HEAD resolves from GitHub.

No transaction sent, deployment repeated, wallet signature performed, Intent
created, AI matching called, Phase 4C entered, Repository B created, frontend
built, PR merged or Portal submitted. STOP for independent review in ordinary chat.
