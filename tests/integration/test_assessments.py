import itertools
import json
import pickle

import pytest

FIT = ["FIT"] * 3


def assess(h, decisions=FIT, ids=None, versions=None):
    ids = ids or [1, 2, 3]
    versions = versions or [int(h.c.intents[i].version) for i in ids]
    h.sender(ids[0] - 1)
    h.vm.clear_mocks()
    h.vm.mock_llm("You are the semantic compatibility classifier", json.dumps({"decisions": decisions}))
    result = h.c.assess_cycle(ids, versions, [[ids[i], ids[(i + 1) % 3]] for i in range(3)])
    assert h.vm.run_validator() is True
    return result


@pytest.mark.parametrize("decisions", list(itertools.product(["FIT", "NO_FIT", "UNSURE"], repeat=3)))
def test_all_27_business_outcomes_and_persisted_reads(h, contract_module, decisions):
    ids = h.ring()
    result = assess(h, list(decisions), ids)
    matched = list(decisions) == FIT
    assert result == {
        "assessment_id": 1,
        "result": "MATCHED" if matched else "NOT_MATCHED",
        "cycle_id": 1 if matched else 0,
    }
    record = h.c.get_assessment(1)
    assert record["found"] is True and record["decisions"] == list(decisions)
    assert record["result"] == result["result"]
    assert record["edges"] == [[1, 2], [2, 3], [3, 1]] and record["versions"] == [1] * 3
    assert record["intent_ids"] == ids and record["assessed_at"] == h.now
    assert record["proposer"] == str(h.accounts[0]).lower()
    assert record["prompt_version"] == contract_module.PROMPT_VERSION
    assert record["prompt_sha256"] == contract_module.PROMPT_SHA256
    assert record["cycle_status"] == ("PENDING" if matched else "NONE")
    assert not any(key in record for key in ("finalized", "validators", "votes", "consensus_logs"))
    assert h.c.get_protocol_stats()["assessment_total"] == 1
    assert h.c.get_protocol_stats()["cycle_total"] == (1 if matched else 0)
    for i in ids:
        assert h.c.get_intent(i)["status"] == ("RESERVED" if matched else "OPEN")
    if matched:
        assert record["canonical_snapshot"] == h.c.get_cycle(1)["canonical_snapshot"]
        assert record["snapshot_id"] == h.c.get_cycle(1)["snapshot_id"]
        assert h.c.get_cycle(1)["confirmations"] == [False] * 3


@pytest.mark.parametrize("ids", [[1, 2, 3], [2, 3, 1], [3, 1, 2]])
@pytest.mark.parametrize("caller", [0, 1, 2])
def test_negative_replay_prevents_llm_across_rotation_and_owner(h, ids, caller):
    h.ring()
    assess(h, ["FIT", "UNSURE", "FIT"])
    h.sender(caller)
    h.vm.clear_mocks()
    h.vm.clear_validators()
    before = h.storage()
    with pytest.raises(Exception, match="DUPLICATE_ASSESSMENT"):
        h.c.assess_cycle(ids, [1] * 3, [[ids[i], ids[(i + 1) % 3]] for i in range(3)])
    assert h.storage() == before and not h.vm._captured_validators
    assert h.c.get_protocol_stats()["assessment_total"] == 1


def test_meaningful_update_new_snapshot_preserves_old_negative_terms(h):
    h.ring()
    assess(h, ["NO_FIT", "FIT", "FIT"])
    original = h.c.get_assessment(1)
    h.sender(0)
    h.update(1, offer_description="Revised material service scope")
    result = assess(h)
    assert result["assessment_id"] == 2 and result["cycle_id"] == 1
    assert h.c.get_assessment(1) == original
    assert original["snapshot_id"] != h.c.get_assessment(2)["snapshot_id"]
    assert h.c.get_assessment(2)["versions"] == [2, 1, 1]


def test_reverse_can_be_assessed_as_distinct_assignment(h):
    h.ring()
    assess(h, ["NO_FIT"] * 3)
    assess(h, ["UNSURE"] * 3, [1, 3, 2])
    assert h.c.get_assessment(1)["snapshot_id"] != h.c.get_assessment(2)["snapshot_id"]
    assert h.c.get_assessment(2)["edges"] == [[1, 3], [3, 2], [2, 1]]


@pytest.mark.parametrize("action", ["confirm", "decline", "cancel", "expire"])
def test_legitimate_assessment_existing_state_machine_regression(h, action):
    h.ring()
    assess(h)
    record = h.c.get_assessment(1)
    before = h.storage()
    with pytest.raises(Exception, match="INTENT_UNAVAILABLE"):
        h.c.assess_cycle([1, 2, 3], [1] * 3, [[1, 2], [2, 3], [3, 1]])
    assert h.storage() == before
    if action == "confirm":
        for i in range(3):
            h.confirm(owner=i)
            assert h.c.get_cycle(1)["status"] == ("ACTIVE" if i == 2 else "PENDING")
        assert all(h.c.get_intent(i)["status"] == "CONSUMED" for i in (1, 2, 3))
        assert h.c.get_protocol_stats()["active_total"] == 1
        expected = "ACTIVE"
    elif action == "decline":
        h.sender(1)
        h.c.decline_cycle(1, record["snapshot_id"])
        expected = "ABORTED"
    elif action == "cancel":
        h.sender(1)
        h.c.cancel_intent(2, 1)
        expected = "ABORTED"
    else:
        h.warp(h.now + 3 * 86400)
        h.c.expire_cycle(1)
        expected = "EXPIRED"
    assert h.c.get_assessment(1)["cycle_status"] == expected
    assert h.c.get_assessment(1)["result"] == "MATCHED"
    assert h.c.get_protocol_stats()["assessment_total"] == 1
    if action == "decline":
        before = h.storage()
        with pytest.raises(Exception, match="DECLINED_SNAPSHOT"):
            h.c.assess_cycle([1, 2, 3], [1] * 3, [[1, 2], [2, 3], [3, 1]])
        assert h.storage() == before
    if action == "expire":
        with pytest.raises(Exception, match="DUPLICATE_PROPOSAL"):
            h.c.assess_cycle([1, 2, 3], [1] * 3, [[1, 2], [2, 3], [3, 1]])


@pytest.mark.parametrize("decisions", [FIT, ["NO_FIT", "FIT", "UNSURE"]])
def test_fresh_persisted_bytes_and_sdk_root_restoration(h, contract_module, decisions):
    import cloudpickle
    from genlayer.py.storage import ROOT_SLOT_ID
    from genlayer.py.storage._internal.generate import _storage_build
    from gltest.direct.vm import InmemManager

    h.ring()
    assess(h, decisions)
    if decisions == FIT:
        h.confirm(owner=0)
    expected = h.c.get_assessment(1)
    root = object.__getattribute__(h.c, "_instance")
    restored = cloudpickle.loads(cloudpickle.dumps(root))
    assert restored.get_assessment(1) == expected
    manager = InmemManager()
    manager.restore(pickle.loads(pickle.dumps(h.vm._storage.snapshot())))
    descriptor = _storage_build(contract_module.SemanticCycleAccord, {})
    rebound = descriptor.get(manager.get_store_slot(ROOT_SLOT_ID), 0)
    assert rebound.get_assessment(1) == expected
    assert rebound.get_intent(1) == h.c.get_intent(1)
    if decisions == FIT:
        for i in (1, 2):
            h.sender(i)
            assert rebound.confirm_cycle(1, expected["snapshot_id"])
        assert rebound.get_cycle(1)["status"] == "ACTIVE"
        assert rebound.get_assessment(1)["cycle_status"] == "ACTIVE"
        assert h.c.get_cycle(1)["status"] == "PENDING"
    else:
        before = {k: v.rstrip(b"\0") for k, v in manager.snapshot().items() if v.rstrip(b"\0")}
        with pytest.raises(Exception, match="DUPLICATE_ASSESSMENT"):
            rebound.assess_cycle([1, 2, 3], [1] * 3, [[1, 2], [2, 3], [3, 1]])
        assert {k: v.rstrip(b"\0") for k, v in manager.snapshot().items() if v.rstrip(b"\0")} == before


def test_new_methods_calldata_and_readonly_no_llm(h, contract_module, monkeypatch):
    from genlayer.py import calldata

    h.ring()
    result = assess(h, ["UNSURE"] * 3)
    assert calldata.decode(calldata.encode(result)) == result
    h.vm.clear_mocks()
    before = h.storage()

    def forbidden(*args, **kwargs):
        pytest.fail("View must not classify")

    monkeypatch.setattr(contract_module.gl.nondet, "exec_prompt", forbidden)
    record = h.c.get_assessment(1)
    assert calldata.decode(calldata.encode(record)) == record
    assert h.c.get_assessment(99) == {"found": False}
    assert h.storage() == before


@pytest.mark.parametrize("invalid", [0, -1, 2**64, True, "1", None])
def test_assessment_read_invalid_ids(h, invalid):
    before = h.storage()
    with pytest.raises(Exception, match="INVALID_INTEGER"):
        h.c.get_assessment(invalid)
    assert h.storage() == before


def test_phase1_persistent_layout_is_retained_by_appended_fields(h, contract_module, tmp_path):
    import subprocess
    import sys
    from genlayer.py.storage import ROOT_SLOT_ID
    from genlayer.py.storage._internal.generate import _storage_build
    from gltest.direct.vm import InmemManager

    baseline = subprocess.run(
        ["git", "show", "cc773e936cf6184d0b3f9447771ac804e597bfe7:contracts/semantic_cycle_accord.py"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    fixture = tmp_path / "phase1_layout_fixture.py"
    fixture.write_text(baseline)
    serialized = tmp_path / "phase1-bytes.pickle"
    # The SDK registers one Contract per interpreter. Use an isolated process;
    # do not patch its registration or the storage descriptor implementation.
    script = """
import pickle, socket, sys
from pathlib import Path
from gltest.direct import VMContext, create_address, deploy_contract
socket.socket.connect = lambda *a: (_ for _ in ()).throw(AssertionError('offline only'))
vm=VMContext(); vm._chain_id=61999; vm.sender=create_address('sca3-test-0')
vm.warp('2026-10-11T12:00:00+00:00')
with vm.activate():
    old=deploy_contract(Path(sys.argv[1]),vm,sdk_version='v0.2.16')
    for i in range(3):
        vm.sender=create_address(f'sca3-test-{i}')
        old.create_intent('Logo design','PNG','Page translation','English',1791720000+864000)
    old._reserve_accepted_cycle([1,2,3],[1]*3,[[1,2],[2,3],[3,1]])
    vm.sender=create_address('sca3-test-0')
    old.confirm_cycle(1,old.get_cycle(1)['snapshot_id'])
    Path(sys.argv[2]).write_bytes(pickle.dumps((vm._storage.snapshot(),old.get_cycle(1),old.get_intent(1))))
"""
    subprocess.run(
        [sys.executable, "-c", script, str(fixture), str(serialized)],
        check=True,
        capture_output=True,
        text=True,
    )
    stored_bytes, expected, expected_intent = pickle.loads(serialized.read_bytes())
    manager = InmemManager()
    manager.restore(stored_bytes)
    descriptor = _storage_build(contract_module.SemanticCycleAccord, {})
    rebound = descriptor.get(manager.get_store_slot(ROOT_SLOT_ID), 0)
    assert rebound.get_cycle(1) == expected
    assert rebound.get_intent(1) == expected_intent
    assert rebound.get_protocol_stats()["assessment_total"] == 0
    assert rebound.get_assessment(1) == {"found": False}
    h.sender(1)
    rebound.confirm_cycle(1, expected["snapshot_id"])
    h.sender(2)
    rebound.confirm_cycle(1, expected["snapshot_id"])
    assert rebound.get_cycle(1)["status"] == "ACTIVE"
    # Offline byte-layout compatibility; no onchain upgrade/deployment occurred.
