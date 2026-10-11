import pickle

import pytest


def test_missing_ids_and_owner(h):
    assert h.c.get_intent(999) == h.c.get_cycle(999) == {"found": False}
    records = h.c.get_owner_records(str(h.accounts[9]))
    assert records["intents"] == records["cycles"] == []
    assert records["unfinished_count"] == 0


@pytest.mark.parametrize("method", ["get_intents_page", "get_cycles_page", "get_protocol_stats"])
@pytest.mark.parametrize(
    "offset,limit,error",
    [
        (-1, 20, "INVALID_INTEGER"),
        (0, 0, "INVALID_INTEGER"),
        (0, 51, "PAGE_TOO_LARGE"),
        (0, 2**64, "INVALID_INTEGER"),
    ],
)
def test_invalid_pagination(h, method, offset, limit, error):
    with pytest.raises(Exception, match=error):
        getattr(h.c, method)(offset, limit)


def test_pagination_exact_boundaries_and_owner_indexes(h):
    h.reserve()
    assert len(h.c.get_intents_page(0, 2)["records"]) == 2
    assert h.c.get_intents_page(0, 2)["has_more"]
    assert h.c.get_intents_page(2, 2)["next_offset"] == 3
    assert h.c.get_intents_page(3, 2)["records"] == []
    assert h.c.get_intents_page(999, 2)["records"] == []
    assert h.c.get_cycles_page(0, 1)["records"][0]["cycle_id"] == 1
    assert h.c.get_cycles_page(1, 1)["records"] == []
    for owner in range(3):
        result = h.c.get_owner_records(str(h.accounts[owner]).upper().replace("0X", "0x"), 0, 1)
        assert result["intents"][0]["intent_id"] == owner + 1
        assert result["cycles"][0]["cycle_id"] == 1
    with pytest.raises(Exception, match="INVALID_ADDRESS"):
        h.c.get_owner_records("bad")


def test_stats_effective_pages_and_lifecycle_counters(h):
    h.reserve()
    for owner in range(3):
        h.confirm(owner=owner)
    h.reserve(h.ring((3, 4, 5)))
    h.sender(3)
    h.c.decline_cycle(2, h.c.get_cycle(2)["snapshot_id"])
    h.create(6, expires=h.now + 86400)
    h.warp(h.now + 86400)
    a, b = h.c.get_protocol_stats(0, 3), h.c.get_protocol_stats(3, 50)
    assert a["intent_total"] == 7 and a["cycle_total"] == 2
    assert a["active_total"] == a["aborted_total"] == 1
    assert a["effective_intent_counts_page"]["CONSUMED"] == 3
    assert b["effective_intent_counts_page"]["OPEN"] == 3
    assert b["effective_intent_counts_page"]["EXPIRED"] == 1
    assert (
        sum(a["effective_intent_counts_page"].values()) + sum(b["effective_intent_counts_page"].values()) == 7
    )
    assert a["semantic_matching_available"] is False


def test_persistent_storage_pickle_and_fresh_root_rebind(h, contract_module):
    h.reserve()
    h.confirm(owner=0)
    expected = h.c.get_cycle(1)
    expected_owner = h.c.get_owner_records(str(h.accounts[0]))
    # Serialize the actual SDK-backed root and read it after unpickling.
    instance = object.__getattribute__(h.c, "_instance")
    import cloudpickle

    restored = cloudpickle.loads(cloudpickle.dumps(instance))
    assert restored.get_cycle(1) == expected
    assert restored.get_owner_records(str(h.accounts[0])) == expected_owner
    # Rebind a new SDK root to a deserialized byte-storage manager, without init.
    from genlayer.py.storage import ROOT_SLOT_ID
    from genlayer.py.storage._internal.generate import _storage_build
    from gltest.direct.vm import InmemManager

    manager = InmemManager()
    manager.restore(pickle.loads(pickle.dumps(h.vm._storage.snapshot())))
    td = _storage_build(contract_module.SemanticCycleAccord, {})
    rebound = td.get(manager.get_store_slot(ROOT_SLOT_ID), 0)
    assert rebound.get_cycle(1) == expected
    assert rebound.get_intent(1)["status"] == "RESERVED"
    assert rebound.get_owner_records(str(h.accounts[0])) == expected_owner
    h.sender(1)
    assert rebound.confirm_cycle(1, expected["snapshot_id"])
    h.sender(2)
    assert rebound.confirm_cycle(1, expected["snapshot_id"])
    assert rebound.get_cycle(1)["status"] == "ACTIVE"
    assert h.c.get_cycle(1) == expected  # The original storage is isolated.


def test_context_clock_tracks_warp_not_host_time(h):
    h.create()
    assert h.c.get_intent(1)["expires_at"] == 1791720000 + 864000
    h.warp(1791720000 + 864000)
    assert h.c.get_intent(1)["status"] == "EXPIRED"
