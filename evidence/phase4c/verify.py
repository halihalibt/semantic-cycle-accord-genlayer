"""Offline evidence verification only; no RPC, accounts, signing, or transactions.

Run with the frozen lock's genlayer-py 0.16.3 and eth-account dependencies.
Signature recovery consumes public signed bytes; it never accesses a private key.
"""
import ast
import argparse
import base64
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

from eth_abi import decode as abi_decode
from eth_account import Account
from genlayer_py.abi import calldata
import rlp

ROOT = Path(__file__).resolve().parents[2]
E = ROOT / "evidence/phase4c"
BASE = "2215e6fac7d4922b50ff1546bae76b6e4e3a530c"
CONTRACT = "0x84e9284448d4cd16dcbbcbd8104449b11209c6f0"
WALLETS = ["0x22acaa233b7b985b36ef168f2de9295334065b15",
           "0x418c0a70603f8231cd99b1f37dfc49300dcd024e",
           "0xbe8567fd2294f3ec8e68f08b58abeb5b2d28ad61"]
SNAPSHOT = "48e1c68d358f67368c5d8b478e9d450401be06cdf91e90b6b8b94932d2951ede"
SOURCE_HASH = "88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442"
PROMPT_HASH = "8a7b279a3594397802c71fef4df9b4d30db1ff528177d0bf05c80a62397192d3"


def load(path):
    return json.loads((E / path).read_text())


def raw(label):
    entry = load(f"rpc/{label}.json")
    assert entry["exit_code"] == 0 and entry["stderr"] == ""
    response = json.loads(entry["stdout"])
    assert response["id"] == entry["request"]["id"] and "error" not in response
    return response["result"]


def return_value(encoded):
    b = base64.b64decode(encoded, validate=True)
    assert b[0] == 0
    return calldata.decode(b[1:])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screenshots-dir", type=Path, help="Private local directory of original PNG bytes")
    options = parser.parse_args()
    passed = []
    files = list((E / "rpc").glob("*.json"))
    assert len(files) == 51
    for f in files:
        entry = json.loads(f.read_text())
        request = entry["request"]
        assert entry["url"] == "https://studio.genlayer.com/api"
        assert request["method"] in {"eth_chainId", "eth_getTransactionByHash",
                                     "eth_getTransactionReceipt", "gen_getTransactionStatus", "gen_call"}
        if request["method"] == "gen_call":
            assert request["params"][0]["type"] == "read"
            assert request["params"][0]["transaction_hash_variant"] == "latest-final"
        raw(f.stem)
    assert raw("chain-id") == "0xf22f"
    passed.append("51 original RPC envelopes: parse, IDs, read-only methods and chain 61999")

    records = load("transactions.json")["transactions"]
    assert len(records) == 11 and len({r["hash"] for r in records}) == 11
    expected_signers = [0, 1, 2, 0, 0, 1, 2, 0, 1, 2, 0]
    expected_methods = ["create_intent"] * 3 + ["assess_cycle"] + ["confirm_cycle"] * 3
    expected_methods += ["create_intent"] * 3 + ["assess_cycle"]
    for i, record in enumerate(records):
        label = f"tx{i+1:02d}"
        t = raw(label + "-transaction")
        assert record["hash"] == t["hash"] == t["tx_id"]
        for suffix in ["transaction", "receipt", "status"]:
            assert load(f"rpc/{label}-{suffix}.json")["request"]["params"] == [t["hash"]]
        assert t["status"] == raw(label + "-status") == "FINALIZED"
        assert t["result_name"] == "MAJORITY_AGREE"
        receipt = raw(label + "-receipt")
        assert receipt["transactionHash"] == t["hash"] and receipt["status"] == "0x1"
        assert receipt["to"].lower() == CONTRACT
        expected = WALLETS[expected_signers[i]]
        assert t["from_address"].lower() == t["origin_address"].lower() == expected
        assert t["to_address"].lower() == CONTRACT
        signed = t["sim_config"]["signed_rollup_transaction"]
        assert Account.recover_transaction(signed).lower() == expected
        signed_fields = rlp.decode(bytes.fromhex(signed[2:]))
        v = int.from_bytes(signed_fields[-3], "big")
        assert (v - 35) // 2 == 61999
        sender, recipient, validators, rotations, inner = abi_decode(
            ["address", "address", "uint256", "uint256", "bytes"], signed_fields[5][4:])
        assert sender.lower() == expected and recipient.lower() == CONTRACT
        assert validators == 5 and rotations == 3  # configured maximum, not actual rotations
        assert inner.hex() == t["tx_data"]
        unpacked = rlp.decode(inner)
        assert unpacked[0] == base64.b64decode(t["data"]["calldata"])
        decoded = calldata.decode(unpacked[0])
        assert decoded == record["calldata"] and decoded["method"] == expected_methods[i]
        cd = t["consensus_data"]
        leader = next(x for x in cd["leader_receipt"] if x["mode"] == "leader")
        assert leader["execution_result"] == "SUCCESS"
        assert return_value(leader["result"]) == record["return"]
        assert t["leader_only"] is False and t["execution_mode"] == "NORMAL"
        assert t["sim_config"].keys() == {"signed_rollup_transaction"}
        assert int(t["num_of_rounds"]) == 1 and t["rotation_count"] == 0
        assert [x["consensus_round"] for x in t["consensus_history"]["consensus_results"]] == ["Accepted"]
        counts = Counter(cd["votes"].values())
        assert counts == record["vote_counts"]
        assert counts == ({"agree": 5} if i == 1 else {"agree": 3, "idle": 2})
        validators = [x for x in cd["leader_receipt"] + cd["validators"] if x["mode"] == "validator"]
        assert len(validators) == 5 and len({x["node_config"]["address"] for x in validators}) == 5
        assert {x["node_config"]["address"]: x["vote"] for x in validators} == cd["votes"]
        assert dict(zip(t["last_round"]["round_validators"],
                        [x.lower() for x in t["last_round"]["validator_votes_name"]])) == cd["votes"]
        for x in validators:
            assert x["nondet_disagree"] is None
            if x["vote"] == "agree":
                assert x["execution_result"] == "SUCCESS"
                assert x["result"] == leader["result"]
                assert x["contract_state_hash"] == leader["contract_state_hash"]
            else:
                assert x["vote"] == "idle" and x["execution_result"] == "ERROR"
                assert x["genvm_result"]["error_code"] == "CONSENSUS_VALIDATOR_QUORUM_REACHED"
                assert x["genvm_result"]["stderr"] == "Validator execution cancelled after quorum"
    passed.append("11 transactions: hashes, typed calldata, recovered signatures and signed chain domains")
    passed.append("11 finalized successful Returns, accepted rounds, zero actual rotations and exact vote mapping")
    passed.append("35 agree / 20 idle records; all idle ERRORs are explicit quorum cancellation, no disagreement")

    state = load("final-state.json")["reads"]
    for label, decoded in state.items():
        assert decoded == calldata.decode(bytes.fromhex(raw(label).removeprefix("0x")))
    repeated = load("repeated-state.json")["reads"]
    for label, decoded in repeated.items():
        assert decoded == calldata.decode(bytes.fromhex(raw("repeat-" + label).removeprefix("0x")))
        assert decoded == state[label]
    passed.append("12 latest-final reads and four repeated reads reproduce the persisted final state")

    vector_doc = (ROOT / "docs/ONCHAIN_E2E_TEST_VECTORS.md").read_text()
    vectors = [json.loads(s) for s in re.findall(r"```json\n(.*?)\n```", vector_doc, re.S)]
    assert len(vectors) == 3
    negatives = [v.copy() for v in vectors]
    negatives[1][0] = "Design one original typographic logo reading SCA-3; deliver only one transparent 1024x1024 PNG within 48 hours after cycle activation."
    negatives[1][1] = "PNG raster output only. SVG vector output and editable vector source are explicitly unavailable. Exactly one logo; no animation or brand guide."
    for pos, intent_id in enumerate([1, 2, 3, 4, 5, 6]):
        r = records[pos if pos < 3 else pos + 4]
        intent = state[f"intent-{intent_id}"]
        fields = ["offer_description", "offer_limitations", "need_description", "need_requirements", "expires_at"]
        args = r["calldata"]["args"]
        assert args[:4] == (vectors if pos < 3 else negatives)[pos % 3][:4]
        assert args == [intent[f] for f in fields]
        assert r["return"] == intent_id and type(r["return"]) is int
        assert intent["owner"] == WALLETS[pos % 3] and intent["version"] == 1
        assert 86400 <= args[4] - int(raw(r["label"] + "-transaction")["created_timestamp"]) <= 2592000
        assert intent["status"] == intent["stored_status"] == ("CONSUMED" if pos < 3 else "OPEN")
        assert intent["cycle_id"] == (1 if pos < 3 else 0)
    passed.append("Six create Returns/owners/versions/exact frozen vectors/expiry bounds and final intent states")

    for index, assessment_id, ids, decisions, result, cycle_id in [
        (3, 1, [1, 3, 2], ["FIT"] * 3, "MATCHED", 1),
        (10, 2, [4, 6, 5], ["FIT", "FIT", "NO_FIT"], "NOT_MATCHED", 0),
    ]:
        r = records[index]
        a = state[f"assessment-{assessment_id}"]
        edges = [[ids[n], ids[(n+1) % 3]] for n in range(3)]
        assert r["calldata"]["args"] == [ids, [1] * 3, edges]
        assert r["return"] == {"assessment_id": assessment_id, "cycle_id": cycle_id, "result": result}
        assert a["found"] and a["assessment_id"] == assessment_id
        assert a["intent_ids"] == ids and a["versions"] == [1] * 3 and a["edges"] == edges
        assert a["decisions"] == decisions and a["result"] == result and a["cycle_id"] == cycle_id
        assert a["cycle_status"] == ("ACTIVE" if cycle_id else "NONE")
        assert a["prompt_sha256"] == PROMPT_HASH and a["proposer"] == WALLETS[0]
        assert return_value(r["leader_eq_outputs"]["0"]) == decisions
        canonical = json.loads(a["canonical_snapshot"])
        assert canonical[:3] == ["SCA-3-V1", 61999, CONTRACT]
        assert json.dumps(canonical, ensure_ascii=False, separators=(",", ":")) == a["canonical_snapshot"]
        assert hashlib.sha256(a["canonical_snapshot"].encode()).hexdigest() == a["snapshot_id"]
        for n, term in enumerate(canonical[3]):
            intent = state[f"intent-{ids[n]}"]
            assert term == [ids[n], intent["owner"], intent["offer_description"], intent["offer_limitations"],
                            intent["need_description"], intent["need_requirements"], 1, intent["expires_at"], edges[n][1]]
        nonleader = [v for v in r["validators"] if v["address"] != r["leader_address"] and v["vote"] == "agree"]
        assert len(nonleader) == 2
        assert all(v["execution_stats"]["llm"]["tokens"] for v in nonleader)
    passed.append("Positive/negative assessment decisions, raw Leader eq outputs and two non-Leader agreeing AI receipts each")
    passed.append("Canonical snapshots independently rebuilt from immutable intent terms and SHA256 reproduced")

    c = state["cycle-1"]
    assert c["found"] and c["status"] == c["stored_status"] == "ACTIVE"
    assert c["confirmation_count"] == 3 and c["confirmations"] == [True] * 3
    assert c["intent_ids"] == [1, 3, 2] and c["owners"] == [WALLETS[0], WALLETS[2], WALLETS[1]]
    assert c["versions"] == [1] * 3 and c["edges"] == [[1, 3], [3, 2], [2, 1]]
    assert c["snapshot_id"] == SNAPSHOT == state["assessment-1"]["snapshot_id"]
    assert c["canonical_snapshot"] == state["assessment-1"]["canonical_snapshot"]
    assert c["terms"] == json.loads(c["canonical_snapshot"])[3]
    assert c["confirmation_deadline"] == min(c["created_at"] + 259200, min(t[7] for t in c["terms"]))
    for r in records[4:7]:
        assert r["calldata"]["args"] == [1, SNAPSHOT] and r["return"] is True
        assert c["created_at"] <= int(raw(r["label"] + "-transaction")["created_timestamp"]) < c["confirmation_deadline"]
    assert state["cycle-2"] == {"found": False}
    assert state["cycles-page"]["total"] == 1 and len(state["cycles-page"]["records"]) == 1
    stats = state["protocol-stats"]
    assert [stats[k] for k in ["intent_total", "assessment_total", "cycle_total", "active_total", "aborted_total"]] == [6, 2, 1, 1, 0]
    assert stats["effective_intent_counts_page"] == {"CONSUMED": 3, "OPEN": 3, "RESERVED": 0, "CANCELLED": 0, "EXPIRED": 0}
    assert stats["offset"] == 0 and stats["next_offset"] == 6 and not stats["has_more"]
    passed.append("Three true confirmations: identical snapshot, three distinct signatures and valid deadline")
    passed.append("ACTIVE original Cycle, no Cycle #2, exact final counters and full page coverage")

    source = (ROOT / "contracts/semantic_cycle_accord.py").read_bytes()
    deployed = base64.b64decode(raw("deployment-transaction")["data"]["contract_code"])
    assert source == deployed and hashlib.sha256(source).hexdigest() == SOURCE_HASH
    assert source == subprocess.check_output(["git", "show", BASE + ":contracts/semantic_cycle_accord.py"], cwd=ROOT)
    prompt = next(ast.literal_eval(n.value) for n in ast.parse(source).body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "CANONICAL_PROMPT" for t in n.targets))
    assert hashlib.sha256(prompt.encode()).hexdigest() == PROMPT_HASH
    assert raw("deployment-transaction")["data"]["contract_address"].lower() == CONTRACT
    identity = load("source-identity.json")
    assert identity["source_sha256"] == identity["deployment_source_sha256"] == SOURCE_HASH
    assert identity["prompt_sha256"] == PROMPT_HASH and identity["deployment_byte_identity"]
    passed.append("Fresh deployment calldata source byte identity, frozen main source and trusted Prompt SHA256")

    screenshots = load("screenshots.json")
    assert screenshots["count"] == len(screenshots["screenshots"]) == 60
    for s in screenshots["screenshots"]:
        assert s["public_path"] is None and len(s["sha256"]) == 64
        if options.screenshots_dir:
            b = (options.screenshots_dir / s["private_archive_filename"]).read_bytes()
            assert len(b) == s["bytes"] and hashlib.sha256(b).hexdigest() == s["sha256"]
            assert b.startswith(b"\x89PNG\r\n\x1a\n")
    passed.append("60 original screenshot manifest records; public upload blocked by automatic approval review")
    if options.screenshots_dir:
        passed.append("60 private original screenshot PNG signatures, lengths and SHA256")
    observations = load("explorer-observations.json")["transactions"]
    assert len(observations) == 11
    assert all(o["hash"] == r["hash"] and o["url"] == r["explorer_detail_url"]
               and o["finalized"] and o["success"] and o["accepted"] for o, r in zip(observations, records))
    passed.append("11 browser-observed Explorer URL records correspond to independently verified transaction hashes")

    allowed = {"README.md", "WORK_MASTER_PLAN.md", "PROJECT_CHECKPOINT.md",
               "docs/ONCHAIN_EVIDENCE_INDEX.md", "docs/DEPLOYMENT_MANIFEST_STUDIONET.md",
               "docs/PHASE_4C_REPORT.md", "docs/PHASE_4C_E2E_EVIDENCE_INDEX.md",
               "docs/PHASE_4C_ACCEPTANCE_MATRIX.md"}
    changes = subprocess.check_output(["git", "diff", "--name-only", BASE], cwd=ROOT, text=True).splitlines()
    untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True).splitlines()
    assert all(p in allowed or p.startswith("evidence/phase4c/") for p in changes + untracked)
    for p in ["contracts/semantic_cycle_accord.py", "docs/CANONICAL_CLASSIFICATION_PROMPT_V1.md", "uv.lock",
              "docs/ONCHAIN_E2E_TEST_VECTORS.md", "docs/REAL_ONCHAIN_ACCEPTANCE_PLAN.md"]:
        assert (ROOT / p).read_bytes() == subprocess.check_output(["git", "show", BASE + ":" + p], cwd=ROOT)
    checkpoint_old = subprocess.check_output(["git", "show", BASE + ":PROJECT_CHECKPOINT.md"], cwd=ROOT)
    assert checkpoint_old in (ROOT / "PROJECT_CHECKPOINT.md").read_bytes()
    passed.append("Evidence-only allowlist, production/Prompt/lock/vector/plan unchanged, historical checkpoint retained")
    for doc in [ROOT / p for p in allowed if p.endswith(".md") and (ROOT / p).exists()]:
        for dest in re.findall(r"\]\(([^)]+)\)", doc.read_text()):
            if "://" in dest or dest.startswith("#"):
                continue
            assert (doc.parent / dest.split("#")[0]).exists(), (doc, dest)
    passed.append("All relative Markdown links in changed documentation resolve")
    manifest = load("checksum-manifest.json")
    for path, digest in manifest["sha256"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    passed.append("Package checksum manifest: every listed raw/derived/document/script/screenshot byte hash matches")
    result = {"status": "PASS", "passed_groups": passed, "failed_groups": [],
              "not_run": ["Contract regression suite (evidence-only scope)", "Real-node unexpected mid-write rollback",
                          "Service delivery", "Complete production security certification", "New write transactions"],
              "evidence_gaps": ["Original screenshot public upload rejected by automatic approval review; private originals and public hash inventory preserved",
                                "Original machine-readable historical intermediate state reads not available; original user screenshots retained privately",
                                "Raw per-Validator model response texts/full prompts not exposed in acquired receipts",
                                "Fee estimate, budget and consumed GEN not acquired"]}
    if not options.screenshots_dir:
        result["not_run"].append("Original screenshot byte checks: supply --screenshots-dir with private original PNGs")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
