# SCA-3 V1 — Phase 4C current checkpoint

**REAL POSITIVE / NEGATIVE E2E RESULTS INDEPENDENTLY VERIFIED — DRAFT REVIEW — STOP**

Repository A: `halihalibt/semantic-cycle-accord-genlayer` (public, MIT).
Verified merged main baseline: `2215e6fac7d4922b50ff1546bae76b6e4e3a530c`.
Branch: `phase4c-real-e2e-evidence`; published HEAD and Draft PR resolve in GitHub
and the execution report. No merge is authorized.

Stable Studionet 61999; canonical contract
`0x84e9284448D4cd16dcBBCbd8104449B11209C6F0`.
Source SHA256 `88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442`;
trusted Prompt SHA256 `8a7b279a3594397802c71fef4df9b4d30db1ff528177d0bf05c80a62397192d3`.
Fresh deployment source bytes match the frozen source. All 11 specified writes
independently FINALIZED / SUCCESS / MAJORITY_AGREE, with cryptographically recovered
expected A/B/C signatures in domain 61999; each has one Accepted round/zero rotations.
Both assessment maps have 3 agree + 2 idle quorum cancellations, not five unanimity.

Assessment #1: MATCHED, FIT/FIT/FIT, directed ring 1→3→2→1.
Cycle #1 ACTIVE, confirmation_count 3, flags true/true/true, original snapshot
`48e1c68d358f67368c5d8b478e9d450401be06cdf91e90b6b8b94932d2951ede`.
Intents #1–#3 CONSUMED / cycle_id 1.
Assessment #2: NOT_MATCHED, FIT/FIT/NO_FIT, directed ring 4→6→5→4,
cycle_id 0 / cycle_status NONE. Intents #4–#6 OPEN / cycle_id 0.
No Cycle #2; original Cycle #1 remains ACTIVE. Final counters: 6 Intents,
2 Assessments, 1 Cycle, 1 ACTIVE, 3 CONSUMED, 3 OPEN, 0 RESERVED, 0 aborted.

Read [Phase 4C report](docs/PHASE_4C_REPORT.md),
[acceptance matrix](docs/PHASE_4C_ACCEPTANCE_MATRIX.md),
[E2E index](docs/PHASE_4C_E2E_EVIDENCE_INDEX.md) and `evidence/phase4c/` first.
51 raw read-only RPC envelopes, four matching repeated reads, 60 original user
screenshots were privately verified; their metadata and 11 visibly verified Explorer
detail URLs are archived publicly. Automatic approval review rejected public PNG
upload pending explicit user approval; no original screenshots are in this PR.
Original historical intermediate-read JSON is unavailable; screenshot evidence
is preserved separately. Fees and full per-Validator model transcripts remain gaps.
Local evidence verification PASS; contract regression NOT RUN in this evidence-only
phase. Unexpected mid-write node rollback, delivery and production certification
remain NOT RUN/UNVERIFIED. ACTIVE means accepted commitment, never delivery.

Frozen implementation/Prompt/locks/vectors/acceptance plan and historical evidence
remain unchanged. No write transaction, redeployment, upgrade, signing, Repository B,
frontend, Portal or merge performed. STOP immediately after Draft PR publication.
Return to ordinary chat for independent review and separate merge approval.

---

The following Phase 4B checkpoint is preserved verbatim as historical evidence;
its former forward-looking limitations are superseded only where Phase 4C above
provides new evidence.

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
