# Canonical deployment manifest — Stable Studionet

Current E2E evidence: [Phase 4C report](PHASE_4C_REPORT.md) and
[E2E index](PHASE_4C_E2E_EVIDENCE_INDEX.md). The same deployment is unchanged;
current state has one ACTIVE positive Cycle and one negative NOT_MATCHED Assessment.
The following deployment and empty-initial-state records describe Phase 4B.

Phase 4B verified deployment only. Authoritative machine-readable record:
[deployment-record.json](../evidence/phase4b/deployment-record.json).

- Chain: 61999 / 0xf22f; RPC https://studio.genlayer.com/api.
- Approved source baseline: `61f2149996be02a0da4646082a66f3f03a3cb33c`.
- Full canonical source: [semantic_cycle_accord.py](../contracts/semantic_cycle_accord.py).
- Source SHA256: `88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442`.
- Contract: `0x84e9284448D4cd16dcBBCbd8104449B11209C6F0`.
- Deployment hash: `0x3bf2036d9683c6ab55b09cacf54bdeb8ecfa7cb8e7864b832ae7041067f196cc`.
- Deployer: `0x22Acaa233b7b985b36ef168F2DE9295334065B15`.
- Constructor: `[]`. Transaction source verified byte-for-byte.
- FINALIZED, Leader SUCCESS, receipt status 0x1, one Accepted round.
- Fresh stats independently verified via latest-final read; no Intent or cycle.
- Fees UNKNOWN; no verified Explorer deep URL acquired.

This manifest describes the user's existing deployment; it is not permission to
redeploy or modify it. See [Phase 4B report](PHASE_4B_REPORT.md) for raw evidence,
consensus cancellation detail and remaining acceptance limitations.
