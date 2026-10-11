# SCA-3 V1 — Phase 4B checkpoint

**REAL DEPLOYMENT VERIFIED — EMPTY INITIAL STATE VERIFIED — DRAFT REVIEW — STOP**

Public Repository A: halihalibt/semantic-cycle-accord-genlayer, MIT.
Phase 4A merged main baseline verified: `61f2149996be02a0da4646082a66f3f03a3cb33c`.
Work branch: `phase4b-real-deployment-evidence`. Actual publication commit and Draft
PR resolve from evidence/phase4b/publication.json and GitHub; no merge authorized.

Stable Studionet 61999. User-deployed contract:
`0x84e9284448D4cd16dcBBCbd8104449B11209C6F0`.
Deployment transaction:
`0x3bf2036d9683c6ab55b09cacf54bdeb8ecfa7cb8e7864b832ae7041067f196cc`.
Deployer: `0x22Acaa233b7b985b36ef168F2DE9295334065B15`.
Canonical contracts/semantic_cycle_accord.py SHA256:
`88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442`.
Transaction source independently decoded and verified byte-for-byte against main.
Prompt constant hash remains `8a7b279a3594397802c71fef4df9b4d30db1ff528177d0bf05c80a62397192d3`.

Live RPC verifies FINALIZED, successful receipt, Leader SUCCESS and one Accepted
round. Raw votes map: 3 agree including Leader, 2 idle; actual receipts: 1 Leader
and 4 Validators. Idle Validators were cancelled after quorum, not five agrees.
User Explorer screenshot records Initial Validators 5 / Rotation Count 0.
Independent latest-final get_protocol_stats(0,50) matches all zero counters,
SCA-3-V1, network 61999 and semantic_matching_available true. The latter does not
prove live AI matching. Full requests/responses and screenshot originals archived.

Read docs/PHASE_4B_REPORT.md, docs/DEPLOYMENT_MANIFEST_STUDIONET.md,
docs/ONCHAIN_EVIDENCE_INDEX.md and evidence/phase4b/ before continuing. Phase 4A,
README and master-plan statements are historical pre-deployment checkpoints;
this checkpoint supplies the current deployment status without rewriting history.

Source, Canonical Prompt, protocol rules, tests, toolchain, uv.lock and historical
evidence unchanged. Evidence assertions and scope/checksum/link checks PASS;
regression suite NOT RUN in this evidence-only phase (prior 566 PASS historical).
Fees, wallet signature transcript, verified Explorer detail URL and full Studio
schema-error stderr not acquired. Explorer currently returned an application
error in this browser; RPC independent verification succeeded.

Three-wallet E2E, real AI classification, positive/negative matching,
reservations/confirmations/ACTIVE and unexpected mid-write real-node rollback
remain unverified. ACTIVE is commitment, never service delivery.

STOP for ordinary-chat independent review. No writes, redeployment, signing,
Intent creation, matching, Phase 4C, Repository B, frontend, PR merge or Portal.
