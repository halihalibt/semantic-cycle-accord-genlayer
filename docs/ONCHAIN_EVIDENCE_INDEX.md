# SCA-3 V1 — Onchain evidence index

Phase 4B deployment and empty initial read only. Full interpretation and limits:
[PHASE_4B_REPORT.md](PHASE_4B_REPORT.md). No Phase 4C evidence exists.

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
