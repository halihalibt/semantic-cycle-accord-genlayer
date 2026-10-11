# SCA-3 V1 — Deployment preflight

**PHASE 4A COMPLETE — MANUAL DEPLOYMENT PACKAGE READY — AWAITING USER APPROVAL**

Manual package readiness only: no deployment authorization, production-readiness claim or real consensus claim. Source/spec/ABI/storage/prompt/tests/toolchain/historical evidence remain unchanged.

## Verified baseline

- Public owner/repository: halihalibt/semantic-cycle-accord-genlayer, MIT retained.
- Exact main: `7906f4e3c7c619ffdef0ae12147a78f5d018cebb`; GitHub PRs #1/#2/#3 actually MERGED. Older pending references are historical.
- Source SHA256: `88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442`.
- Trusted CANONICAL_PROMPT constant SHA256: `8a7b279a3594397802c71fef4df9b4d30db1ff528177d0bf05c80a62397192d3` (not the Markdown file digest).
- Python 3.12.14 / official GenVM v0.2.16 / genlayer-test 0.29.2 / genvm-linter 0.11.0 / pytest 9.1.1 / Ruff 0.14.0; frozen uv.lock unchanged.
- uv sync --frozen, bootstrap_sdk and verify_local all exit 0. 566 PASS, 0 FAIL, 0 SKIP. GenVM AST 3 PASS, SDK validation and 7 WRITE + 7 VIEW schema PASS, Ruff PASS. Storage/calldata/Phase 1 byte compatibility remain covered.
- Four isolated native WASM invocations reproduced: constructor, get_protocol_stats, create_intent, get_intent; Return/exit 0. Disposable offline host only, no network execution or consensus proof.

## Actual read-only network observations

Timestamped exact requests/responses/errors are in evidence/phase4a/read-only-network-checks.json. Parameter-dependent methods were probed with empty params: no invented hashes, addresses, simulated contract or real network execution. Invalid-params proves dispatcher presence only, never a successful transaction query.

| Probe | Actual response | Evidence level |
| --- | --- | --- |
| `eth_chainId` | `0xf22f` | VERIFIED: actual read-only response |
| `eth_blockNumber` | `0x6acba7e9` | VERIFIED: actual read-only response |
| `eth_syncing` | `False` | VERIFIED: actual read-only response |
| `web3_clientVersion` | `Method not found: web3_clientVersion` | UNSUPPORTED |
| `eth_gasPrice` | `0x0` | VERIFIED: actual read-only response |
| `eth_estimateGas` | `Missing required parameter: transaction` | LIMITED: dispatcher recognized; missing params; runtime semantics not proven |
| `gen_getTransactionReceipt` | `Method not found: gen_getTransactionReceipt` | UNSUPPORTED |
| `gen_getTransactionStatus` | `Missing required parameter: transaction_hash` | LIMITED: dispatcher recognized; missing params; runtime semantics not proven |
| `eth_getTransactionReceipt` | `Missing required parameter: transaction_hash` | LIMITED: dispatcher recognized; missing params; runtime semantics not proven |
| `eth_getTransactionByHash` | `Missing required parameter: transaction_hash` | LIMITED: dispatcher recognized; missing params; runtime semantics not proven |
| `sim_getTransactionByHash` | `Method not found: sim_getTransactionByHash` | UNSUPPORTED |
| `gen_simulate` | `Method not found: gen_simulate` | UNSUPPORTED |
| `https://studio.genlayer.com/` | `200` | VERIFIED: actual read-only response |
| `https://explorer-studio.genlayer.com/` | `200` | VERIFIED: actual read-only response |

Python urllib initially returned 403 on three methods and a disconnect on client version; recorded curl transport then succeeded. No 429 was observed. The site itself was reachable; do not label client transport errors a network outage. The initial separate curl identity check also returned 0xf22f.

Stable status expects `transaction_hash` according to its actual error, unlike newer docs' object `txId` examples. Use future actual project hashes to verify Stable's precise shape. `gen_getTransactionReceipt` and `gen_simulate` are unavailable here; do not switch to another network or SDK. `eth_blockNumber` may be a Studio compatibility value; it is not live-chain/finality evidence. `eth_syncing=false` likewise does not prove runtime compatibility.

## Deployment path and compatibility

Official hosted Studio is the selected manual path. The public page actually loaded at https://studio.genlayer.com/contracts with Your Contracts, an upload icon, templates, account/balance and logs. Official docs describe file upload, editor/run-debug, constructor detection, deployment, methods and result inspection. Exact current controls, fee panel and signing interaction remain NEEDS MANUAL CONFIRMATION; no deployment form was opened and no contract was uploaded. No constructor arguments are required, confirmed from canonical source and actual SDK schema.

Pinned runner passes local SDK/native checks. Hosted availability of the exact runner, production assessment and independent Validators cannot be proven by read-only identity/status RPC. These are future execution gates, not silently upgraded compatibility. No known critical source defect was discovered; actual first execution remains unverified.

## Fees

| Operation | Exact current Stable estimate | Required future procedure |
| --- | --- | --- |
| Deploy | UNKNOWN | Inspect actual Studio/wallet display with full canonical source and no constructor args before personal signature |
| create_intent | UNKNOWN | Inspect actual per-call display with verified five arguments |
| assess_cycle | UNKNOWN | Inspect full three-edge call estimate/budget; account for independent Leader/Validator runs; never multiply an invented fixed cost |
| confirm_cycle | UNKNOWN | Inspect actual call using verified cycle ID/snapshot |
| decline_cycle | UNKNOWN | Inspect only if separately authorized later; do not execute for fee measurement |
| expire_cycle | UNKNOWN | Inspect only if separately authorized later; do not execute for fee measurement |

Estimated fee, user fee budget, observed consumption, test GEN balance and cash spending are separate. No actual user balance was checked and no consumed fee exists for this project. eth_gasPrice=0 and recognized eth_estimateGas do not establish protocol cost or a method-specific GEN estimate. No concrete estimateGas transaction was supplied. The gen_simulate dispatcher is absent; no simulation executed. Current v0.6 estimate/distribution APIs are documentation context, not verified Stable support. No newer SDK installed. No obsolete sim_getFeeConfig call. The plan is free hosted testing; no paid API or cash purchase was used. If fees are unavailable, keep UNKNOWN and require manual inspection before signing; stop if the cost cannot be understood.

## Decision

VERIFIED: baseline, identity hashes, frozen environment, unchanged regressions, isolated deterministic WASM, Stable chain ID and site accessibility.
DOCUMENTED BUT NOT EXECUTED: manual deployment, initial read, positive/negative vectors, all future signatures and evidence gates.
UNKNOWN: precise fees/budget/consumption, user wallet balance/signature UI, hosted exact-runner execution and real consensus/finality/rollback.
BLOCKED gates: any future write until separate approval, actual user review of fees/network/signer, and each prerequisite finalizes successfully. Missing actual agreement evidence blocks E2E acceptance. These gates do not prevent publication of this preparation-only package. If any source repair is needed, STOP rather than patch production.
