import pytest

DAY = 86400


def test_valid_creation_and_owner_index(h):
    assert h.create() == 1
    item = h.c.get_intent(1)
    assert item["version"] == 1 and item["status"] == "OPEN" and item["cycle_id"] == 0
    assert item["owner"] == str(h.accounts[0]).lower()
    records = h.c.get_owner_records(str(h.accounts[0]))
    assert records["intent_total"] == records["unfinished_count"] == 1


@pytest.mark.parametrize("field", ["offer", "need"])
@pytest.mark.parametrize("value", ["", " ", "\t\n", "\u3000"])
def test_mandatory_empty(h, field, value):
    before = h.storage()
    with pytest.raises(Exception, match="EMPTY_DESCRIPTION"):
        h.create(**{field: value})
    assert h.storage() == before


@pytest.mark.parametrize("field", ["offer", "limitations", "need", "requirements"])
@pytest.mark.parametrize("value", ["a" * 512, "é" * 256, "禹" * 170 + "ab"])
def test_512_byte_boundary(h, field, value):
    assert h.create(**{field: value}) == 1


@pytest.mark.parametrize("field", ["offer", "limitations", "need", "requirements"])
@pytest.mark.parametrize("value", ["a" * 513, "é" * 257, "禹" * 171, "x" * 10000])
def test_oversized_text(h, field, value):
    with pytest.raises(Exception, match="TEXT_TOO_LONG"):
        h.create(**{field: value})
    assert h.c.get_protocol_stats()["intent_total"] == 0


def test_optional_empty_and_preserve_unicode(h):
    h.create(offer=" 大禹🙂 ", limitations="", need="日本語", requirements="")
    assert h.c.get_intent(1)["offer_description"] == " 大禹🙂 "


@pytest.mark.parametrize("delta", [DAY, 30 * DAY])
def test_expiry_inclusive_bounds(h, delta):
    h.create(expires=h.now + delta)


@pytest.mark.parametrize("delta", [-1, 0, DAY - 1, 30 * DAY + 1])
def test_invalid_validity(h, delta):
    with pytest.raises(Exception, match="INVALID_VALIDITY"):
        h.create(expires=h.now + delta)


def test_owner_capacity_and_terminal_slot_reuse(h):
    for _ in range(5):
        h.create()
    before = h.storage()
    with pytest.raises(Exception, match="OWNER_CAPACITY"):
        h.create()
    assert h.storage() == before
    h.c.cancel_intent(2, 1)
    assert h.create() == 6
    assert h.c.get_owner_records(str(h.accounts[0]))["unfinished_count"] == 5
    assert len(h.c.owner_slots[str(h.accounts[0]).lower()]) == 5


def test_logical_expiration_excluded_without_cleanup(h):
    for _ in range(5):
        h.create(expires=h.now + DAY)
    h.warp(h.now + DAY)
    assert h.c.get_intent(1)["status"] == "EXPIRED"
    assert h.c.get_intent(1)["stored_status"] == "OPEN"
    assert h.c.get_owner_records(str(h.accounts[0]))["unfinished_count"] == 0
    assert h.create() == 6
    assert h.c.get_protocol_stats()["effective_intent_counts_page"]["EXPIRED"] == 5


@pytest.mark.parametrize("operation", ["update", "cancel"])
def test_non_owner_rejected(h, operation):
    h.create()
    h.sender(1)
    before = h.storage()
    with pytest.raises(Exception, match="UNAUTHORIZED"):
        h.update() if operation == "update" else h.c.cancel_intent(1, 1)
    assert h.storage() == before


def test_update_increments_and_stale_update_cancel_rejected(h):
    h.create()
    assert h.update(offer_description="New offer") == 2
    assert h.c.get_intent(1)["offer_description"] == "New offer"
    for action in (lambda: h.update(version=1), lambda: h.c.cancel_intent(1, 1)):
        before = h.storage()
        with pytest.raises(Exception, match="STALE_VERSION"):
            action()
        assert h.storage() == before


@pytest.mark.parametrize("state", ["CANCELLED", "EXPIRED", "RESERVED", "CONSUMED"])
def test_unavailable_intent_mutation(h, state):
    ids = h.ring()
    h.sender(0)
    if state == "CANCELLED":
        h.c.cancel_intent(1, 1)
    elif state == "EXPIRED":
        h.warp(h.c.get_intent(1)["expires_at"])
    else:
        h.reserve(ids)
        if state == "CONSUMED":
            for owner in range(3):
                h.confirm(owner=owner)
    h.sender(0)
    before = h.storage()
    with pytest.raises(Exception, match="INTENT_EXPIRED|INTENT_NOT_OPEN"):
        h.update()
    assert h.storage() == before
    if state in ("CANCELLED", "EXPIRED", "CONSUMED"):
        with pytest.raises(Exception, match="INTENT_EXPIRED|INTENT_NOT_CANCELLABLE"):
            h.c.cancel_intent(1, 1)
        assert h.storage() == before


@pytest.mark.parametrize("value", [-1, 0, 2**64])
def test_invalid_ids(h, value):
    with pytest.raises(Exception, match="INVALID_INTEGER"):
        h.c.get_intent(value)


def test_update_validation_atomicity(h):
    h.create()
    before = h.storage()
    with pytest.raises(Exception, match="TEXT_TOO_LONG"):
        h.update(need_requirements="界" * 512)
    assert h.storage() == before
