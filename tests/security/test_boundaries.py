from pathlib import Path

import pytest


@pytest.mark.parametrize("field", ["intent_count", "cycle_count"])
def test_counter_overflow_preflight(h, field):
    if field == "intent_count":
        h.c.intent_count = 2**64 - 1
        action = h.create
    else:
        ids = h.ring()
        h.c.cycle_count = 2**64 - 1

        def action():
            return h.reserve(ids)

    before = h.storage()
    with pytest.raises(Exception, match="COUNTER_OVERFLOW"):
        action()
    assert h.storage() == before


def test_version_overflow_preflight(h):
    h.create()
    h.c.intents[1].version = 2**64 - 1
    before = h.storage()
    with pytest.raises(Exception, match="VERSION_OVERFLOW"):
        h.update()
    assert h.storage() == before


@pytest.mark.parametrize("operation", ["update", "cancel", "confirm", "decline", "expire"])
def test_missing_write_target(h, operation):
    before = h.storage()
    with pytest.raises(Exception, match="INTENT_NOT_FOUND|CYCLE_NOT_FOUND"):
        {
            "update": lambda: h.c.update_intent(99, 1, "Offer", "", "Need", "", h.now + 86400),
            "cancel": lambda: h.c.cancel_intent(99, 1),
            "confirm": lambda: h.c.confirm_cycle(99, "bad"),
            "decline": lambda: h.c.decline_cycle(99, "bad"),
            "expire": lambda: h.c.expire_cycle(99),
        }[operation]()
    assert h.storage() == before


def test_constructor_rejects_other_network():
    from gltest.direct import VMContext, create_address, deploy_contract

    vm = VMContext()
    vm._chain_id = 1  # Invalid offline context; no other network contacted.
    vm.sender = create_address("wrong-chain")
    with vm.activate():
        with pytest.raises(Exception, match="UNSUPPORTED_NETWORK"):
            deploy_contract(Path("contracts/semantic_cycle_accord.py"), vm, sdk_version="v0.2.16")


@pytest.mark.parametrize("stage", [0, 2])
def test_expiration_before_final_activation_has_no_partial_consumption(h, stage):
    h.reserve(h.ring(expires=h.now + 86400))
    if stage:
        h.confirm(owner=0)
        h.confirm(owner=1)
    h.warp(h.now + 86400)
    before = h.storage()
    with pytest.raises(Exception, match="CYCLE_EXPIRED"):
        h.confirm(owner=2)
    assert h.storage() == before
    assert h.c.get_protocol_stats()["active_total"] == 0


def test_history_over_one_page_never_breaks_capacity(h):
    for i in range(60):
        h.create(0)
        h.c.cancel_intent(i + 1, 1)
    page = h.c.get_owner_records(str(h.accounts[0]), 0, 50)
    assert len(page["intents"]) == 50 and page["has_more"]
    next_page = h.c.get_owner_records(str(h.accounts[0]), page["next_offset"], 50)
    assert len(next_page["intents"]) == 10 and not next_page["has_more"]
    assert len(h.c.owner_slots[str(h.accounts[0]).lower()]) == 1
    assert next_page["unfinished_count"] == 0
    assert h.c.get_protocol_stats(0, 50)["effective_intent_counts_page"]["CANCELLED"] == 50


@pytest.mark.parametrize(
    "method",
    [
        "get_intent",
        "get_cycle",
        "get_intents_page",
        "get_cycles_page",
        "get_owner_records",
        "get_protocol_stats",
    ],
)
def test_view_calldata_roundtrip(h, method):
    from genlayer.py import calldata

    h.reserve()
    args = {
        "get_intent": [1],
        "get_cycle": [1],
        "get_owner_records": [str(h.accounts[0])],
        "get_intents_page": [],
        "get_cycles_page": [],
        "get_protocol_stats": [],
    }[method]
    result = getattr(h.c, method)(*args)
    assert calldata.decode(calldata.encode(result)) == result


@pytest.mark.parametrize("expires", [0, 1791720000 + 86399, 1791720000 + 30 * 86400 + 1])
def test_invalid_update_expiration_atomic(h, expires):
    h.create()
    before = h.storage()
    with pytest.raises(Exception, match="INVALID_VALIDITY|INVALID_INTEGER"):
        h.update(expires_at=expires)
    assert h.storage() == before
