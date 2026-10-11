import pytest

DAY = 86400


def test_three_separate_confirmations_and_terminal_consumption(h):
    h.reserve()
    assert h.confirm(owner=0)
    assert h.c.get_cycle(1)["confirmation_count"] == 1
    assert h.confirm(owner=1)
    assert h.c.get_cycle(1)["confirmation_count"] == 2
    assert h.c.get_cycle(1)["status"] == "PENDING"
    assert h.confirm(owner=2)
    assert h.c.get_cycle(1)["status"] == "ACTIVE"
    assert h.c.get_protocol_stats()["active_total"] == 1
    assert all(h.c.get_intent(i)["status"] == "CONSUMED" for i in (1, 2, 3))
    assert all(h.c.get_intent(i)["cycle_id"] == 1 for i in (1, 2, 3))


@pytest.mark.parametrize("owner", [0, 1, 2])
def test_duplicate_confirmation_noop(h, owner):
    h.reserve()
    assert h.confirm(owner=owner)
    before = h.storage()
    assert h.confirm(owner=owner) is False
    assert h.storage() == before
    assert h.c.get_cycle(1)["confirmation_count"] == 1


def test_unrelated_wallet_and_wrong_digest(h):
    h.reserve()
    for owner, digest, code in [(9, None, "UNAUTHORIZED"), (0, "bad", "SNAPSHOT_MISMATCH")]:
        before = h.storage()
        with pytest.raises(Exception, match=code):
            h.confirm(owner=owner, digest=digest)
        assert h.storage() == before


@pytest.mark.parametrize("owner", [0, 1, 2])
def test_decline_releases_and_rejects_repetition(h, owner):
    h.reserve()
    h.confirm(owner=0)
    h.sender(owner)
    digest = h.c.get_cycle(1)["snapshot_id"]
    h.c.decline_cycle(1, digest)
    assert h.c.get_cycle(1)["status"] == "ABORTED"
    assert h.c.get_protocol_stats()["aborted_total"] == 1
    for i in range(1, 4):
        assert h.c.get_intent(i)["status"] == "OPEN"
        assert h.c.get_intent(i)["cycle_id"] == 0
    before = h.storage()
    with pytest.raises(Exception, match="CYCLE_NOT_PENDING"):
        h.c.decline_cycle(1, digest)
    assert h.storage() == before


@pytest.mark.parametrize("intent_id", [1, 2, 3])
def test_cancel_reserved_safely_aborts(h, intent_id):
    h.reserve()
    h.sender(intent_id - 1)
    h.c.cancel_intent(intent_id, 1)
    assert h.c.get_cycle(1)["status"] == "ABORTED"
    for i in (1, 2, 3):
        assert h.c.get_intent(i)["status"] == ("CANCELLED" if i == intent_id else "OPEN")
        assert h.c.get_intent(i)["cycle_id"] == 0


def test_decline_unauthorized_and_mismatched_digest_atomic(h):
    h.reserve()
    digest = h.c.get_cycle(1)["snapshot_id"]
    for owner, supplied, code in [(9, digest, "UNAUTHORIZED"), (0, "bad", "SNAPSHOT_MISMATCH")]:
        h.sender(owner)
        before = h.storage()
        with pytest.raises(Exception, match=code):
            h.c.decline_cycle(1, supplied)
        assert h.storage() == before


def test_72_hour_deadline_and_permissionless_cleanup(h):
    h.reserve()
    cycle = h.c.get_cycle(1)
    assert cycle["confirmation_deadline"] == h.now + 3 * DAY
    before = h.storage()
    with pytest.raises(Exception, match="DEADLINE_NOT_REACHED"):
        h.c.expire_cycle(1)
    assert h.storage() == before
    h.warp(cycle["confirmation_deadline"] - 1)
    h.confirm(owner=0)
    h.warp(h.now + 1)
    before = h.storage()
    with pytest.raises(Exception, match="CYCLE_EXPIRED"):
        h.confirm(owner=1)
    assert h.storage() == before
    assert h.c.get_cycle(1)["status"] == "EXPIRED"
    assert h.c.get_cycle(1)["stored_status"] == "PENDING"
    h.sender(9)
    assert h.c.expire_cycle(1)
    assert all(h.c.get_intent(i)["status"] == "OPEN" for i in (1, 2, 3))
    before = h.storage()
    assert h.c.expire_cycle(1) is False
    assert h.storage() == before
    assert h.c.get_protocol_stats()["expired_cycles_cleaned"] == 1


def test_earliest_intent_deadline_and_no_reopen_expired(h):
    ids = [h.create(0, expires=h.now + DAY), h.create(1), h.create(2)]
    h.reserve(ids)
    assert h.c.get_cycle(1)["confirmation_deadline"] == h.now + DAY
    h.warp(h.now + DAY)
    h.c.expire_cycle(1)
    assert h.c.get_intent(1)["status"] == h.c.get_intent(1)["stored_status"] == "EXPIRED"
    assert h.c.get_intent(2)["status"] == h.c.get_intent(3)["status"] == "OPEN"


@pytest.mark.parametrize("terminal", ["ACTIVE", "ABORTED", "EXPIRED"])
@pytest.mark.parametrize("action", ["confirm", "decline", "expire"])
def test_terminal_cycle_immutable(h, terminal, action):
    h.reserve()
    digest = h.c.get_cycle(1)["snapshot_id"]
    if terminal == "ACTIVE":
        for owner in range(3):
            h.confirm(owner=owner)
    elif terminal == "ABORTED":
        h.sender(0)
        h.c.decline_cycle(1, digest)
    else:
        h.warp(h.now + 3 * DAY)
        h.c.expire_cycle(1)
    h.sender(0)
    before = h.storage()
    if terminal == "EXPIRED" and action == "expire":
        assert h.c.expire_cycle(1) is False
    else:
        with pytest.raises(Exception, match="CYCLE_NOT_PENDING"):
            {
                "confirm": lambda: h.c.confirm_cycle(1, digest),
                "decline": lambda: h.c.decline_cycle(1, digest),
                "expire": lambda: h.c.expire_cycle(1),
            }[action]()
    assert h.storage() == before


def test_unrelated_cycle_isolation(h):
    a = h.reserve(h.ring((0, 1, 2)))
    b = h.reserve(h.ring((3, 4, 5)))
    other = h.c.get_cycle(b)
    other_intents = [h.c.get_intent(i) for i in (4, 5, 6)]
    h.confirm(a, 0)
    h.sender(1)
    h.c.decline_cycle(a, h.c.get_cycle(a)["snapshot_id"])
    assert h.c.get_cycle(b) == other
    assert [h.c.get_intent(i) for i in (4, 5, 6)] == other_intents
    for owner in (3, 4, 5):
        h.confirm(b, owner)
    assert h.c.get_cycle(b)["status"] == "ACTIVE"


def test_consumed_slots_reused_without_reopening(h):
    h.reserve()
    for owner in range(3):
        h.confirm(owner=owner)
    for _ in range(5):
        h.create(0)
    assert h.c.get_intent(1)["status"] == "CONSUMED"
    assert h.c.get_owner_records(str(h.accounts[0]))["unfinished_count"] == 5
