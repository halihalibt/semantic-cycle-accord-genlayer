# SCA-3 V1 — Phase 4C positive / negative E2E evidence index

Frozen merged main baseline: `2215e6fac7d4922b50ff1546bae76b6e4e3a530c`.
See [report](PHASE_4C_REPORT.md) and [acceptance matrix](PHASE_4C_ACCEPTANCE_MATRIX.md)
for provenance distinctions and remaining limitations.

All rows below independently verify FINALIZED + receipt 0x1 + Leader SUCCESS +
MAJORITY_AGREE + one Accepted round + zero rotations. Signatures were recovered
from public signed bytes in chain domain 61999. A/C/B is the canonical ring order.
Verified Explorer detail URLs were actually opened, not assumed.

| ID | Case / method | Signer | Successful Return | Actual votes | Transaction / raw record |
| --- | --- | --- | --- | --- | --- |
| tx01 | Positive / create_intent | A | `1` | 3 agree + 2 idle | [0xce94c5a03d32d0af9592ee1060667ccff19e8c47e3d4f56f1e1e4f0636c19e92](https://explorer-studio.genlayer.com/tx/0xce94c5a03d32d0af9592ee1060667ccff19e8c47e3d4f56f1e1e4f0636c19e92) · [raw transaction](../evidence/phase4c/rpc/tx01-transaction.json) · [receipt](../evidence/phase4c/rpc/tx01-receipt.json) · [status](../evidence/phase4c/rpc/tx01-status.json) |
| tx02 | Positive / create_intent | B | `2` | 5 agree | [0xc02f228c9d13dd57ffe0df063ba4032d4a1e6b4a86769ebc59557f611b257e45](https://explorer-studio.genlayer.com/tx/0xc02f228c9d13dd57ffe0df063ba4032d4a1e6b4a86769ebc59557f611b257e45) · [raw transaction](../evidence/phase4c/rpc/tx02-transaction.json) · [receipt](../evidence/phase4c/rpc/tx02-receipt.json) · [status](../evidence/phase4c/rpc/tx02-status.json) |
| tx03 | Positive / create_intent | C | `3` | 3 agree + 2 idle | [0xdf3cc58f55e7ad77bcbcb4d2e4f46d05131da80e0b2946ce0d60de2b2d8b149d](https://explorer-studio.genlayer.com/tx/0xdf3cc58f55e7ad77bcbcb4d2e4f46d05131da80e0b2946ce0d60de2b2d8b149d) · [raw transaction](../evidence/phase4c/rpc/tx03-transaction.json) · [receipt](../evidence/phase4c/rpc/tx03-receipt.json) · [status](../evidence/phase4c/rpc/tx03-status.json) |
| tx04 | Positive / assess_cycle | A | `{"assessment_id":1,"cycle_id":1,"result":"MATCHED"}` | 3 agree + 2 idle | [0xc71701f70199e4d65565adb2bbee2592e4e463f3fbf81b25d99b10c9de703968](https://explorer-studio.genlayer.com/tx/0xc71701f70199e4d65565adb2bbee2592e4e463f3fbf81b25d99b10c9de703968) · [raw transaction](../evidence/phase4c/rpc/tx04-transaction.json) · [receipt](../evidence/phase4c/rpc/tx04-receipt.json) · [status](../evidence/phase4c/rpc/tx04-status.json) |
| tx05 | Positive / confirm_cycle | A | `true` | 3 agree + 2 idle | [0x48c3a1d262adba989c1f37520b871919b619a61e9bb721e14eeffeac6ca1b34b](https://explorer-studio.genlayer.com/tx/0x48c3a1d262adba989c1f37520b871919b619a61e9bb721e14eeffeac6ca1b34b) · [raw transaction](../evidence/phase4c/rpc/tx05-transaction.json) · [receipt](../evidence/phase4c/rpc/tx05-receipt.json) · [status](../evidence/phase4c/rpc/tx05-status.json) |
| tx06 | Positive / confirm_cycle | B | `true` | 3 agree + 2 idle | [0x4736fce42672766d2b589eab8a73d8bee56caf202c7ceaf1c83ada8b9fbd4531](https://explorer-studio.genlayer.com/tx/0x4736fce42672766d2b589eab8a73d8bee56caf202c7ceaf1c83ada8b9fbd4531) · [raw transaction](../evidence/phase4c/rpc/tx06-transaction.json) · [receipt](../evidence/phase4c/rpc/tx06-receipt.json) · [status](../evidence/phase4c/rpc/tx06-status.json) |
| tx07 | Positive / confirm_cycle | C | `true` | 3 agree + 2 idle | [0xcc310816d39b379189690be115241f594719c44959351232908b9ab85ee8ef82](https://explorer-studio.genlayer.com/tx/0xcc310816d39b379189690be115241f594719c44959351232908b9ab85ee8ef82) · [raw transaction](../evidence/phase4c/rpc/tx07-transaction.json) · [receipt](../evidence/phase4c/rpc/tx07-receipt.json) · [status](../evidence/phase4c/rpc/tx07-status.json) |
| tx08 | Negative / create_intent | A | `4` | 3 agree + 2 idle | [0x0de8eae342b2ee8f957fa81b079c0bfa1e8ad5d9f1e59a0cb6892ef24e48ef86](https://explorer-studio.genlayer.com/tx/0x0de8eae342b2ee8f957fa81b079c0bfa1e8ad5d9f1e59a0cb6892ef24e48ef86) · [raw transaction](../evidence/phase4c/rpc/tx08-transaction.json) · [receipt](../evidence/phase4c/rpc/tx08-receipt.json) · [status](../evidence/phase4c/rpc/tx08-status.json) |
| tx09 | Negative / create_intent | B | `5` | 3 agree + 2 idle | [0x0508f72d44c7d6d92db5b89cd9d2bbca0917f9518fc96b207b4fda748f8f3064](https://explorer-studio.genlayer.com/tx/0x0508f72d44c7d6d92db5b89cd9d2bbca0917f9518fc96b207b4fda748f8f3064) · [raw transaction](../evidence/phase4c/rpc/tx09-transaction.json) · [receipt](../evidence/phase4c/rpc/tx09-receipt.json) · [status](../evidence/phase4c/rpc/tx09-status.json) |
| tx10 | Negative / create_intent | C | `6` | 3 agree + 2 idle | [0xdd549213898fc72d7c4414868f417af8ca8467a8f4369dcd86235294a3ace674](https://explorer-studio.genlayer.com/tx/0xdd549213898fc72d7c4414868f417af8ca8467a8f4369dcd86235294a3ace674) · [raw transaction](../evidence/phase4c/rpc/tx10-transaction.json) · [receipt](../evidence/phase4c/rpc/tx10-receipt.json) · [status](../evidence/phase4c/rpc/tx10-status.json) |
| tx11 | Negative / assess_cycle | A | `{"assessment_id":2,"cycle_id":0,"result":"NOT_MATCHED"}` | 3 agree + 2 idle | [0x0bb517817a4dd54ec6afb1b1d04223fb78804ed3f6e561f2ca65ca31d2b3234f](https://explorer-studio.genlayer.com/tx/0x0bb517817a4dd54ec6afb1b1d04223fb78804ed3f6e561f2ca65ca31d2b3234f) · [raw transaction](../evidence/phase4c/rpc/tx11-transaction.json) · [receipt](../evidence/phase4c/rpc/tx11-receipt.json) · [status](../evidence/phase4c/rpc/tx11-status.json) |

## Independent final reads and hashes

- [Final state](../evidence/phase4c/final-state.json): six Intents, two Assessments,
  Cycle #1, absence of Cycle #2, full Cycle page and protocol statistics.
- [Repeated state](../evidence/phase4c/repeated-state.json): second matching reads
  of both Assessments, Cycle #1 and statistics.
- [Transaction details](../evidence/phase4c/transactions.json): exact typed calldata,
  addresses, recovered signatures, original Return bytes, decoded Returns,
  Validator records, votes, LLM statistics, rounds, rotations and explicit unknown fees.
- [Source identity](../evidence/phase4c/source-identity.json): fresh deployment
  source byte comparison, frozen source and trusted Prompt hash.
- [Explorer inspection](../evidence/phase4c/explorer-observations.json): derived
  record of all 11 visibly verified detail pages.
- [Checksum manifest](../evidence/phase4c/checksum-manifest.json),
  [offline verifier](../evidence/phase4c/verify.py),
  [actual verification result](../evidence/phase4c/verification.json).

Positive snapshot: `48e1c68d358f67368c5d8b478e9d450401be06cdf91e90b6b8b94932d2951ede`.
Negative snapshot: `dffd6337478c50f2285a66d715d8e1ad0f65814d92602d7d64f51b1c85fb990d`.

## Original screenshot inventory — public images blocked

Automatic approval review rejected publishing original images to the public repository.
This table and the manifest preserve filename/hash metadata; image bytes remain private.
These are user-uploaded historical observations, not independent historical RPC
or fresh agent screenshots. [Manifest](../evidence/phase4c/screenshots.json) preserves
each original filename/byte length/hash. Partial crops remain partial evidence.

| Original upload | Preserved original bytes |
| --- | --- |
| image(20261011-191130).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-191134).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-191419).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-191731).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-191738).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-191908).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-191925).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-191929).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-191943).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-192518).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-192527).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-192709).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-192724).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-192750).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-192806).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-192817).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-192857).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-192907).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-192919).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-193030).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-193035).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-193445).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-193456).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-193505).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-193512).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-193911).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-194157).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-194304).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-194330).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-194643).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-194651).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-194700).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-194706).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-194715).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-194722).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-194744).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-194752).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-194800).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-195422).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-195441).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-195642).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-195701).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-195918).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-195922).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-195956).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-200129).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-200135).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-200201).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-200459).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-200555).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-200947).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-200953).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-201001).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-201018).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-201044).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-201107).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-201126).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-201211).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-201217).png | Original retained privately; public PNG upload awaiting explicit approval |
| image(20261011-201225).png | Original retained privately; public PNG upload awaiting explicit approval |

Key historical views: OPEN #1–#3 `191419 / 191908 / 191943`; MATCHED/PENDING
`192709 / 192724`; zero-confirmation cycle `192750 / 192806 / 192817`;
RESERVED #1–#3 `192857 / 192907 / 192919`; count 1 `193911`; count 2 `194157`;
ACTIVE/count 3 `194304`; positive-only counters `194330 / 195422`; positive
CONSUMED #1–#3 `194744 / 194752 / 194800`; negative assessment `200459 / 201126`;
negative persisted Assessment #2 `200555`; final negative OPEN #4–#6
`200947 / 200953 / 201001`; final counters `201018`; original ACTIVE cycle
after negative `201044`; negative consensus `201211 / 201217 / 201225`.
All abbreviated numbers refer to the timestamp suffix of the indexed originals.
