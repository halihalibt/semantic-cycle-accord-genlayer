import hashlib
import json

import pytest


def test_valid_ring_snapshot_and_rotation(h):
    ids = h.ring()
    a = h.c._prepare_cycle(ids, [1] * 3, [[1, 2], [2, 3], [3, 1]])
    b = h.c._prepare_cycle([2, 3, 1], [1] * 3, [[2, 3], [3, 1], [1, 2]])
    assert a[1:] == b[1:]
    data = json.loads(a[1])
    assert data[:3] == ["SCA-3-V1", 61999, h.c.contract_identity]
    assert data[3][0] == [
        1,
        str(h.accounts[0]).lower(),
        "Service 0",
        "One revision",
        "Translate a page",
        "English",
        1,
        h.now + 864000,
        2,
    ]
    assert a[2] == hashlib.sha256(a[1].encode()).hexdigest()
    assert h.reserve(ids) == 1
    cycle = h.c.get_cycle(1)
    assert cycle["edges"] == [[1, 2], [2, 3], [3, 1]]
    assert cycle["confirmation_count"] == 0 and cycle["status"] == "PENDING"
    for i in ids:
        assert h.c.get_intent(i)["status"] == "RESERVED"


def test_reversed_ring_and_contract_network_identity(h):
    ids = h.ring()
    a = h.c._prepare_cycle(ids, [1] * 3, [[1, 2], [2, 3], [3, 1]])[2]
    b = h.c._prepare_cycle([1, 3, 2], [1] * 3, [[1, 3], [3, 2], [2, 1]])[2]
    assert a != b
    h.c.contract_identity = "0x" + "b" * 40
    assert h.c._prepare_cycle(ids, [1] * 3, [[1, 2], [2, 3], [3, 1]])[2] != a
    h.c.network_id = 123
    assert h.c._prepare_cycle(ids, [1] * 3, [[1, 2], [2, 3], [3, 1]])[2] != a


@pytest.mark.parametrize(
    "ids,versions,edges,error",
    [
        ([1, 2], [1, 1], [[1, 2], [2, 1]], "EXACTLY_THREE_REQUIRED"),
        ([1, 2, 3, 4], [1] * 4, [[1, 2]] * 4, "EXACTLY_THREE_REQUIRED"),
        ([1, 1, 3], [1] * 3, [[1, 1], [1, 3], [3, 1]], "DUPLICATE_INTENT"),
        ([1, 2, 3], [1] * 3, [[1, 1], [2, 3], [3, 1]], "INVALID_RING"),
        ([1, 2, 3], [1] * 3, [[1, 2], [2, 3]], "EXACTLY_THREE_REQUIRED"),
        ([1, 2, 3], [1] * 3, [[1, 2], [1, 2], [3, 1]], "INVALID_RING"),
        ([1, 2, 3], [1] * 3, [[1, 2], [2, 4], [3, 1]], "INVALID_RING"),
        ([1, 2, 3], [1] * 3, [[1, 3], [3, 2], [2, 1]], "INVALID_RING"),
        ([1, 2, 3], [1] * 3, [[1], [2, 3], [3, 1]], "INVALID_RING"),
        ([1, 2, 3], [2, 1, 1], [[1, 2], [2, 3], [3, 1]], "STALE_VERSION"),
        ([1, 2, 999], [1] * 3, [[1, 2], [2, 999], [999, 1]], "INTENT_NOT_FOUND"),
    ],
)
def test_bad_topology_atomic(h, ids, versions, edges, error):
    h.ring()
    before = h.storage()
    with pytest.raises(Exception, match=error):
        h.reserve(ids, versions, edges)
    assert h.storage() == before
    assert h.c.get_protocol_stats()["cycle_total"] == 0


def test_duplicate_owner(h):
    ids = h.ring((0, 1, 0))
    with pytest.raises(Exception, match="DUPLICATE_OWNER"):
        h.reserve(ids)


def test_expired_matching_boundary(h):
    ids = h.ring(expires=h.now + 86400)
    h.warp(h.now + 86400)
    with pytest.raises(Exception, match="INTENT_EXPIRED"):
        h.reserve(ids)


@pytest.mark.parametrize(
    "field", ["offer_description", "need_description", "offer_limitations", "need_requirements", "expires_at"]
)
def test_changed_terms_change_identity_and_reject_old_version(h, field):
    ids = h.ring()
    old = h.c._prepare_cycle(ids, [1] * 3, [[1, 2], [2, 3], [3, 1]])[2]
    h.sender(0)
    h.update(**{field: h.now + 20 * 86400 if field == "expires_at" else "Changed"})
    with pytest.raises(Exception, match="STALE_VERSION"):
        h.reserve(ids, [1] * 3)
    new = h.c._prepare_cycle(ids, [2, 1, 1], [[1, 2], [2, 3], [3, 1]])[2]
    assert new != old


def test_reserved_capacity_counts(h):
    h.reserve()
    for _ in range(4):
        h.create(0)
    with pytest.raises(Exception, match="OWNER_CAPACITY"):
        h.create(0)
