# SCA-3 V1 — Phase 4A report

**PHASE 4A COMPLETE — MANUAL DEPLOYMENT PACKAGE READY — AWAITING USER APPROVAL**

Repository: https://github.com/halihalibt/semantic-cycle-accord-genlayer. Starting main: `7906f4e3c7c619ffdef0ae12147a78f5d018cebb`. Work branch: phase4a-deployment-preflight. Draft PR #4: https://github.com/halihalibt/semantic-cycle-accord-genlayer/pull/4 — verified OPEN, DRAFT, unmerged. Tested package commit: `26cf84e81619ec8cacf46aa2fc07ae3a1dcd7935`, tree `4d6fdee2c5a654c70d5ebaed1cc4625c97d479f1`; reporting-only follow-up does not change tested source or evidence. Publication metadata is added to evidence/phase4a/publication.json after the first published commit; final work HEAD and Draft PR must be resolved from current GitHub. No self-referential final HEAD is invented in this report.

566 PASS / 0 FAIL / 0 SKIP, all original tests unchanged. Ruff, GenVM AST 3 checks, SDK semantic validation, exact 7 WRITE + 7 VIEW, storage/calldata and original byte compatibility PASS. Python/toolchain/uv.lock unchanged. Four real isolated native v0.2.16 WASM Return/exit-0 smoke invocations reproduced; no network consensus inferred.

Contract: `88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442`. Trusted prompt: `8a7b279a3594397802c71fef4df9b4d30db1ff528177d0bf05c80a62397192d3`. Manifest distinguishes the constant and full Markdown digest. No contract, prompt, schema, ABI or protocol change.

Read-only checks confirm Stable 61999/0xf22f and Studio/Explorer HTTP 200. Status and Ethereum transaction-query dispatchers recognize missing transaction_hash; no real project hash was queried. gen_getTransactionReceipt, sim_getTransactionByHash, gen_simulate and web3_clientVersion return method-not-found. Unsupported methods are not network failures. eth_gasPrice returns 0; method-specific GEN fees, budgets and consumed fees remain UNKNOWN. eth_estimateGas recognizes a missing transaction; no actual estimate or contract simulation executed. Do not assume v0.6 APIs or zero protocol fees.

Manual deployment uses the official hosted Studio, full byte-identical file and NO constructor args. Public UI observed; deploy/fee/signature dialog and exact current labels NEEDS MANUAL CONFIRMATION. Hosted exact-runner availability/real classification/consensus/finality/rollback remain unverified. No known critical source bug discovered. Readiness is for review of the manual package, not automatic deployment or production.

## Prepared package

- docs/PHASE_4A_DEPLOYMENT_PREFLIGHT.md: baseline, actual probes, fee findings and readiness limits.
- docs/MANUAL_STUDIO_EXECUTION_PACKAGE.md: beginner Chinese steps, source URL/hash, no-argument constructor, signer/network/fee checks, actual deployment evidence template and fresh stats expectations.
- docs/ONCHAIN_E2E_TEST_VECTORS.md: exact three-wallet text, signature and parameter order; runtime seven-day expiry, actual ID/version/snapshot gates; negative and non-executable UNSURE plan.
- docs/REAL_ONCHAIN_ACCEPTANCE_PLAN.md: finalized successful execution PLUS independent consensus evidence and persisted-state acceptance.
- docs/MANUAL_FAILURE_RECOVERY.md: conservative failure/status/read-first retry guidance.
- evidence/phase4a/: raw network, preflight JSON, checksum manifest, exact vector JSON, verifier and native WASM outputs; publication metadata after publication.
- PROJECT_CHECKPOINT.md and WORK_MASTER_PLAN.md: current verified status only. Historical README/phase documents are intentionally retained as past checkpoints; this report overrides their old pending statuses using actual GitHub state.

Positive logical ring A→C→B→A: copywriting→chart provider→logo provider→copywriting provider in directed supply order. Conditional actual IDs A=1,B=2,C=3 use ids [1,3,2], versions [1,1,1], edges [[1,3],[3,2],[2,1]]. After actual assessment/read, A/B/C independently confirm the SAME real snapshot. Negative uses a fresh trio with B offering PNG only while A requires SVG plus PNG; intended B→A NO_FIT leads to successful stored NOT_MATCHED/no reservation if actual network agrees. Labels are semantic expectations, never network facts. All exact text and gates are in the vector document.

Future evidence: signer, exact arguments, hash, original receipt/status, execution result/return, independent Validator rounds/participants/agreement, actual Explorer link, relevant reads, fees separated and errors/trace. FINALIZED alone is insufficient; Leader alone is insufficient. Unexpected real-node mid-write rollback remains a residual limitation; never trigger destructive hosted faults to close it.

## Fresh Phase 4B handoff — copy only after approval

```text
SCA-3 V1 — PHASE 4B MANUAL DEPLOYMENT ONLY.
Account halihalibt; Repository A halihalibt/semantic-cycle-accord-genlayer.
Read current GitHub Phase 4A Draft PR and PROJECT_CHECKPOINT.md, PHASE_4A_REPORT,
PHASE_4A_DEPLOYMENT_PREFLIGHT, MANUAL_STUDIO_EXECUTION_PACKAGE,
ONCHAIN_E2E_TEST_VECTORS, REAL_ONCHAIN_ACCEPTANCE_PLAN and MANUAL_FAILURE_RECOVERY.
Resolve actual Phase 4A PR number and current work HEAD from GitHub/publication.json.
Do not assume the Draft PR was merged. Verify approved reviewed source from main
7906f4e3c7c619ffdef0ae12147a78f5d018cebb or the subsequently approved merge baseline.
Canonical contracts/semantic_cycle_accord.py SHA256:
88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442.
Trusted prompt SHA256:
8a7b279a3594397802c71fef4df9b4d30db1ff528177d0bf05c80a62397192d3.
Stable Studionet only: 61999, https://studio.genlayer.com/api,
https://studio.genlayer.com/. Constructor args: none ([]).
User personally controls and signs in their own browser. Work must not inspect,
store or output private keys/seed/credentials or create/import a signing wallet.
First resolve current network, actual signer, fee display/budget and balance.
Fees UNKNOWN until observed; gasPrice=0 is not a protocol fee guarantee.
Assist with one user-authorized manual canonical deployment and collect actual
hash/address, FINALIZED status, successful execution and available consensus/logs.
Then perform authorized read-only get_protocol_stats(0,50), checking fresh state.
No deployment facts exist at handoff; never invent them. If an operation fails,
preserve evidence and STOP. No assess/create/confirm transactions in this
minimum Phase 4B scope: later three-wallet E2E requires explicit added approval.
No source/prompt changes, fee API upgrades, alternate chains, PR merge,
Repository B/frontend, Portal or Phase 4C. Report evidence and STOP.
```

No deployments, blockchain submissions, signatures, network contract execution, private material, signing wallet creation/import, paid APIs, main changes, merge, Repository B, frontend or Portal occurred. STOP after verified Draft publication; do not start Phase 4B.
