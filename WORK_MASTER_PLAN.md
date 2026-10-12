# Protocol development milestones

This page is a historical index for Semantic Cycle Accord (SCA-3 V1). For current protocol behavior, integration instructions and verified outcomes, begin with the [README](README.md) and [verified onchain examples](docs/VERIFIED_ONCHAIN_EXAMPLES.md).

| Milestone | Recorded outcome | Primary references |
| --- | --- | --- |
| Deterministic protocol | Typed storage, bounded operations, invariants and lifecycle rules | [Specification](docs/PROTOCOL_SPEC.md) · [Invariants](docs/DETERMINISTIC_INVARIANTS.md) |
| Semantic assessment | Leader/Validator classification and exact three-edge equivalence | [Consensus design](docs/CONSENSUS_AND_EQUIVALENCE_V1.md) |
| Security testing | 566 contract tests recorded in the release test suite | [Security audit](docs/PHASE_3_SECURITY_AUDIT.md) · [Testing](docs/PHASE_3_TEST_AND_ACCEPTANCE.md) |
| Studionet deployment | Canonical contract deployed on Stable Studionet, chain ID 61999 | [Deployment manifest](docs/DEPLOYMENT_MANIFEST_STUDIONET.md) |
| Positive and negative live cases | Cycle #1 ACTIVE after three distinct confirmations; Assessment #2 NOT_MATCHED | [Verified cases](docs/VERIFIED_ONCHAIN_EXAMPLES.md) · [Detailed receipts](docs/PHASE_4C_E2E_EVIDENCE_INDEX.md) |
| Application integration | Separate public product using the same deployed primitive | [Semantic Cycle Exchange](https://github.com/halihalibt/semantic-cycle-exchange) |

The documented protocol does not provide payment, custody, service fulfillment or dispute resolution. **ACTIVE represents accepted commitments, not completed delivery.**

Historical milestone logs, failed tests and raw transaction evidence remain at their existing `docs/` and `evidence/` paths. The original dated version of this project-management record is retained in [Git history](https://github.com/halihalibt/semantic-cycle-accord-genlayer/blob/8a09380c06f12afd6ac85197737b0018cd8e594f/WORK_MASTER_PLAN.md); earlier stop conditions apply only to the checkpoint when written. This index is not an execution authorization.
