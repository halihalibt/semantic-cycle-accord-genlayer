# SCA-3 V1 — Onchain evidence index

Current Phase 4C positive/negative E2E:
[report](PHASE_4C_REPORT.md), [E2E transaction/screenshot index](PHASE_4C_E2E_EVIDENCE_INDEX.md),
[acceptance matrix](PHASE_4C_ACCEPTANCE_MATRIX.md). Machine-readable evidence:
[transactions](../evidence/phase4c/transactions.json), [final state](../evidence/phase4c/final-state.json),
[raw records](../evidence/phase4c/rpc/), [verification](../evidence/phase4c/verification.json).
11 successful finalized writes; positive ACTIVE Cycle #1; negative NOT_MATCHED/no
new Cycle. Historical intermediate raw-read gaps remain explicit.

## Preserved Phase 4B deployment evidence

The records and limitations below describe the historical Phase 4B checkpoint.
Its initial empty state is a historical read, not the current contract state.
Full Phase 4B interpretation: [PHASE_4B_REPORT.md](PHASE_4B_REPORT.md).

| Artifact | Provenance / contents |
| --- | --- |
| [RPC queries](../evidence/phase4b/rpc-queries.json) | Independent live requests and original responses: eth_chainId, gen_getTransactionStatus, eth_getTransactionReceipt, eth_getTransactionByHash, gen_call. Includes full source, monitoring, votes, Leader/Validator receipts and raw state output |
| [Deployment record](../evidence/phase4b/deployment-record.json) | Derived identity, byte comparison, votes, individual Validator results, explicit unknowns |
| [Initial state](../evidence/phase4b/initial-state.json) | Decoded latest-final get_protocol_stats(0,50) |
| [Verification](../evidence/phase4b/verification.json) | Checks, NOT RUN/UNKNOWN distinctions and Explorer application error |
| [Screenshot manifest](../evidence/phase4b/screenshots.json) | Original upload mapping and SHA256; user-supplied, not independently captured |
| [Stats screenshot](../evidence/phase4b/screenshots/protocol-stats.png) | download(1).png; Finalized response with zero counters |
| [Explorer overview](../evidence/phase4b/screenshots/explorer-overview.png) | download(2).png; hash, FINALIZED, Deploy, signer/address, 5 initial validators, 0 rotations, Accepted |
| [Explorer execution](../evidence/phase4b/screenshots/explorer-execution.png) | download(3).png; contract, SUCCESS, Return, null, empty stdout/stderr |
| [Studio deployed](../evidence/phase4b/screenshots/studio-deployed.png) | download(4).png; deployed UI, FINALIZED log and truncated schema-query warnings |

No verified Explorer detail URL, fee estimate/budget/consumed GEN, wallet signature
transcript or full Studio schema-error stderr acquired. Raw RPC Validator details
were acquired; 2 idle cancellations must not be omitted or counted as agree.
Historic Phase 4A documents describe pre-deployment facts at their checkpoint;
current status is defined by Phase 4B report and PROJECT_CHECKPOINT.md.
