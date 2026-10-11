import ast
import hashlib
import json
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "field,value",
    [
        ("offer_description", "Substituted offer"),
        ("need_description", "Substituted need"),
        ("offer_limitations", "Unlimited"),
        ("need_requirements", "None"),
        ("version", 2),
        ("owner", "0x" + "f" * 40),
        ("expires_at", 1999999999),
        ("status", "OPEN"),
        ("cycle_id", 2),
    ],
)
@pytest.mark.parametrize("stage", [0, 2])
def test_authoritative_intent_substitution_rejected_atomic(h, field, value, stage):
    h.reserve()
    if stage == 2:
        h.confirm(owner=0)
        h.confirm(owner=1)
    setattr(h.c.intents[1], field, value)  # Offline hostile-storage fixture only.
    before = h.storage()
    with pytest.raises(Exception, match="SNAPSHOT_MISMATCH|RESERVATION_MISMATCH"):
        h.confirm(owner=2)
    assert h.storage() == before
    assert h.c.get_cycle(1)["status"] == "PENDING"


@pytest.mark.parametrize(
    "field,value",
    [
        ("snapshot_id", "0" * 64),
        ("canonical_snapshot", "[]"),
        ("confirmation_deadline", 1999999999),
        ("created_at", 1999999999),
    ],
)
def test_corrupt_cycle_metadata_rejected(h, field, value):
    h.reserve()
    setattr(h.c.cycles[1], field, value)
    before = h.storage()
    with pytest.raises(Exception, match="SNAPSHOT_MISMATCH"):
        h.confirm()
    assert h.storage() == before


def test_supplied_digest_cannot_authorize_substituted_snapshot(h):
    h.reserve()
    cycle = h.c.cycles[1]
    cycle.terms[0].offer_description = "Substitute"
    cycle.canonical_snapshot = h.c._canonical(list(cycle.terms))
    cycle.snapshot_id = hashlib.sha256(cycle.canonical_snapshot.encode()).hexdigest()
    before = h.storage()
    with pytest.raises(Exception, match="SNAPSHOT_MISMATCH"):
        h.confirm()
    assert h.storage() == before


def test_snapshot_direction_substitution_rejected(h):
    h.reserve()
    h.c.cycles[1].terms[0].supplies_to = 3
    with pytest.raises(Exception, match="SNAPSHOT_MISMATCH"):
        h.confirm()


def test_duplicate_proposal_and_rotation_no_new_cycle(h):
    h.reserve()
    before = h.storage()
    for ids in ([1, 2, 3], [2, 3, 1]):
        with pytest.raises(Exception, match="INTENT_UNAVAILABLE|DUPLICATE_PROPOSAL"):
            h.reserve(ids)
    assert h.storage() == before
    h.sender(0)
    h.c.cancel_intent(1, 1)
    assert h.c.get_protocol_stats()["cycle_total"] == 1


def test_declined_snapshot_blocked_across_callers_until_version_change(h):
    h.reserve()
    h.sender(0)
    h.c.decline_cycle(1, h.c.get_cycle(1)["snapshot_id"])
    before = h.storage()
    for owner in (0, 1, 2, 9):
        h.sender(owner)
        with pytest.raises(Exception, match="DECLINED_SNAPSHOT"):
            h.reserve([2, 3, 1])
    assert h.storage() == before
    h.sender(1)
    h.update(2, offer_limitations="Updated revision allowance")
    assert h.reserve([1, 2, 3]) == 2


def test_expired_identical_proposal_not_replayed(h):
    h.reserve()
    h.warp(h.now + 3 * 86400)
    h.c.expire_cycle(1)
    with pytest.raises(Exception, match="DUPLICATE_PROPOSAL"):
        h.reserve([1, 2, 3])


def test_second_cycle_cannot_reserve_or_consume_shared_intent(h):
    ids = h.ring()
    h.reserve(ids)
    x, y = h.create(3), h.create(4)
    before = h.storage()
    with pytest.raises(Exception, match="INTENT_UNAVAILABLE"):
        h.reserve([1, x, y])
    assert h.storage() == before
    for owner in (0, 1, 2):
        h.confirm(owner=owner)
    before = h.storage()
    with pytest.raises(Exception, match="INTENT_UNAVAILABLE"):
        h.reserve([1, x, y])
    assert h.storage() == before
    assert h.c.get_protocol_stats()["active_total"] == 1


@pytest.mark.parametrize("protected_state", ["CANCELLED", "EXPIRED", "CONSUMED"])
def test_cleanup_never_reopens_terminal_intent(h, protected_state):
    h.reserve()
    h.c.intents[1].status = protected_state
    h.warp(h.now + 3 * 86400)
    h.c.expire_cycle(1)
    assert h.c.get_intent(1)["stored_status"] == protected_state


def test_cleanup_releases_only_its_reservation(h):
    h.reserve()
    h.c.intents[1].cycle_id = 999  # Another-cycle reservation fixture.
    h.warp(h.now + 3 * 86400)
    h.c.expire_cycle(1)
    assert h.c.get_intent(1)["stored_status"] == "RESERVED"
    assert h.c.get_intent(1)["cycle_id"] == 999
    assert h.c.get_intent(2)["status"] == "OPEN"


def test_cleanup_missing_record_preflight_is_atomic(h):
    h.reserve()
    h.c.cycles[1].terms[2].intent_id = 999
    h.warp(h.now + 3 * 86400)
    before = h.storage()
    with pytest.raises(Exception, match="INTENT_NOT_FOUND"):
        h.c.expire_cycle(1)
    assert h.storage() == before


def test_only_authorized_public_surface_and_no_bypass(h):
    source = Path("contracts/semantic_cycle_accord.py").read_text()
    tree = ast.parse(source)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "SemanticCycleAccord")
    surface = {m.name for m in cls.body if isinstance(m, ast.FunctionDef) and m.decorator_list}
    assert surface == {
        "create_intent",
        "update_intent",
        "cancel_intent",
        "confirm_cycle",
        "decline_cycle",
        "expire_cycle",
        "assess_cycle",
        "get_assessment",
        "get_intent",
        "get_cycle",
        "get_intents_page",
        "get_cycles_page",
        "get_owner_records",
        "get_protocol_stats",
    }
    for forbidden in (
        "eq_principle",
        "strict_eq",
        "prompt_comparative",
        "prompt_non_comparative",
        "mock_llm",
        "private_key",
    ):
        assert forbidden not in source
    imports = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imports |= {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }
    assert not imports & {"requests", "urllib", "httpx", "aiohttp"}


def test_snapshot_canonical_unicode_roundtrip(h):
    ids = [h.create(0, offer="图像🙂"), h.create(1), h.create(2)]
    h.reserve(ids)
    snapshot = h.c.get_cycle(1)["canonical_snapshot"]
    assert "图像🙂" in snapshot
    assert json.dumps(json.loads(snapshot), ensure_ascii=False, separators=(",", ":")) == snapshot
