# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""SCA-3 V1 deterministic core. Semantic assessment is unavailable in Phase 1."""

from genlayer import Address, DynArray, TreeMap, allow_storage, gl, u64, u256
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json

DAY = 86400
MAX_PAGE = 50
MAX_U64 = (1 << 64) - 1
PROTOCOL = "SCA-3-V1"


def _fail(code: str) -> None:
    raise gl.vm.UserError(code)


def _uint(value: int, positive: bool = True) -> None:
    if type(value) is not int or value < (1 if positive else 0) or value > MAX_U64:
        _fail("INVALID_INTEGER")


def _now() -> int:
    # GenVM pins this clock to transaction context; Direct Mode warps it offline.
    return int(datetime.now(timezone.utc).timestamp())


def _owner() -> str:
    return str(gl.message.sender_address).lower()


def _fields(offer: str, limitations: str, need: str, requirements: str) -> None:
    for text in (offer, limitations, need, requirements):
        if not isinstance(text, str):
            _fail("INVALID_TEXT")
        # Check character count before UTF-8 allocation for oversized inputs.
        if len(text) > 512:
            _fail("TEXT_TOO_LONG")
        try:
            byte_length = len(text.encode("utf-8"))
        except UnicodeError:
            _fail("INVALID_TEXT")
            return
        if byte_length > 512:
            _fail("TEXT_TOO_LONG")
    if not offer.strip() or not need.strip():
        _fail("EMPTY_DESCRIPTION")


def _expiry(expires_at: int, now: int) -> None:
    _uint(expires_at)
    if not DAY <= expires_at - now <= 30 * DAY:
        _fail("INVALID_VALIDITY")


@allow_storage
@dataclass
class Intent:
    intent_id: u64
    owner: str
    offer_description: str
    offer_limitations: str
    need_description: str
    need_requirements: str
    version: u64
    expires_at: u64
    status: str
    cycle_id: u64


@allow_storage
@dataclass
class Terms:
    intent_id: u64
    owner: str
    offer_description: str
    offer_limitations: str
    need_description: str
    need_requirements: str
    version: u64
    expires_at: u64
    supplies_to: u64


def _terms(intent: Intent, target: int) -> Terms:
    return Terms(
        intent.intent_id,
        intent.owner,
        intent.offer_description,
        intent.offer_limitations,
        intent.need_description,
        intent.need_requirements,
        intent.version,
        intent.expires_at,
        u64(target),
    )


def _term_values(t: Terms) -> list:
    return [
        int(t.intent_id),
        t.owner,
        t.offer_description,
        t.offer_limitations,
        t.need_description,
        t.need_requirements,
        int(t.version),
        int(t.expires_at),
        int(t.supplies_to),
    ]


@allow_storage
@dataclass
class Cycle:
    cycle_id: u64
    snapshot_id: str
    canonical_snapshot: str
    terms: DynArray[Terms]
    confirmations: DynArray[bool]
    created_at: u64
    confirmation_deadline: u64
    status: str


class SemanticCycleAccord(gl.Contract):
    intents: TreeMap[u256, Intent]
    cycles: TreeMap[u256, Cycle]
    owner_intents: TreeMap[str, DynArray[u64]]
    owner_cycles: TreeMap[str, DynArray[u64]]
    owner_slots: TreeMap[str, DynArray[u64]]
    proposals: TreeMap[str, u64]
    declined: TreeMap[str, bool]
    intent_count: u64
    cycle_count: u64
    active_count: u64
    aborted_count: u64
    expired_cycle_count: u64
    network_id: u64
    contract_identity: str

    def __init__(self):
        if int(gl.message.chain_id) != 61999:
            _fail("UNSUPPORTED_NETWORK")
        self.network_id = u64(61999)
        self.contract_identity = str(gl.message.contract_address).lower()

    def _intent(self, intent_id: int) -> Intent:
        _uint(intent_id)
        if u64(intent_id) not in self.intents:
            _fail("INTENT_NOT_FOUND")
        return self.intents[u64(intent_id)]

    def _cycle(self, cycle_id: int) -> Cycle:
        _uint(cycle_id)
        if u64(cycle_id) not in self.cycles:
            _fail("CYCLE_NOT_FOUND")
        return self.cycles[u64(cycle_id)]

    def _effective(self, intent: Intent, now: int) -> str:
        if intent.status in ("OPEN", "RESERVED") and now >= intent.expires_at:
            return "EXPIRED"
        return intent.status

    def _owned(self, intent_id: int, version: int) -> Intent:
        item = self._intent(intent_id)
        if item.owner != _owner():
            _fail("UNAUTHORIZED")
        _uint(version)
        if item.version != version:
            _fail("STALE_VERSION")
        if self._effective(item, _now()) == "EXPIRED":
            _fail("INTENT_EXPIRED")
        return item

    @gl.public.write
    def create_intent(
        self,
        offer_description: str,
        offer_limitations: str,
        need_description: str,
        need_requirements: str,
        expires_at: int,
    ) -> int:
        now = _now()
        _fields(offer_description, offer_limitations, need_description, need_requirements)
        _expiry(expires_at, now)
        owner = _owner()
        slots = self.owner_slots.get(owner, [])
        live = [i for i in slots if self._effective(self.intents[i], now) in ("OPEN", "RESERVED")]
        if len(live) >= 5:
            _fail("OWNER_CAPACITY")
        if self.intent_count == MAX_U64:
            _fail("COUNTER_OVERFLOW")
        intent_id = u64(self.intent_count + 1)
        # All validations precede the write block.
        self.intents[intent_id] = Intent(
            intent_id,
            owner,
            offer_description,
            offer_limitations,
            need_description,
            need_requirements,
            u64(1),
            u64(expires_at),
            "OPEN",
            u64(0),
        )
        self.owner_slots[owner] = live + [intent_id]
        if owner not in self.owner_intents:
            self.owner_intents[owner] = []
        self.owner_intents[owner].append(intent_id)
        self.intent_count = intent_id
        return int(intent_id)

    @gl.public.write
    def update_intent(
        self,
        intent_id: int,
        expected_version: int,
        offer_description: str,
        offer_limitations: str,
        need_description: str,
        need_requirements: str,
        expires_at: int,
    ) -> int:
        item = self._owned(intent_id, expected_version)
        if item.status != "OPEN":
            _fail("INTENT_NOT_OPEN")
        _fields(offer_description, offer_limitations, need_description, need_requirements)
        _expiry(expires_at, _now())
        if item.version == MAX_U64:
            _fail("VERSION_OVERFLOW")
        self.intents[u64(intent_id)] = Intent(
            item.intent_id,
            item.owner,
            offer_description,
            offer_limitations,
            need_description,
            need_requirements,
            u64(item.version + 1),
            u64(expires_at),
            "OPEN",
            u64(0),
        )
        return int(expected_version + 1)

    @gl.public.write
    def cancel_intent(self, intent_id: int, expected_version: int) -> None:
        item = self._owned(intent_id, expected_version)
        if item.status == "RESERVED":
            cycle = self._pending(int(item.cycle_id))
            self._verify_snapshot(cycle)
            self._finish(cycle, "ABORTED")
        elif item.status != "OPEN":
            _fail("INTENT_NOT_CANCELLABLE")
        # Re-read: release above may have changed this record.
        item = self.intents[u64(intent_id)]
        item.status = "CANCELLED"
        item.cycle_id = u64(0)

    def _canonical(self, terms: list[Terms]) -> str:
        return json.dumps(
            [PROTOCOL, int(self.network_id), self.contract_identity, [_term_values(t) for t in terms]],
            ensure_ascii=False,
            separators=(",", ":"),
        )

    def _prepare_cycle(
        self, intent_ids: list[int], versions: list[int], edges: list[list[int]]
    ) -> tuple[list[Terms], str, str, int]:
        """Pure storage preflight; PHASE 2 must run it again after accepted consensus."""
        if len(intent_ids) != 3 or len(versions) != 3 or len(edges) != 3:
            _fail("EXACTLY_THREE_REQUIRED")
        for number in intent_ids + versions:
            _uint(number)
        if len(set(intent_ids)) != 3:
            _fail("DUPLICATE_INTENT")
        for i, edge in enumerate(edges):
            if len(edge) != 2:
                _fail("INVALID_RING")
            for number in edge:
                _uint(number)
            if edge != [intent_ids[i], intent_ids[(i + 1) % 3]]:
                _fail("INVALID_RING")
        now = _now()
        records = [self._intent(i) for i in intent_ids]
        if len({r.owner for r in records}) != 3:
            _fail("DUPLICATE_OWNER")
        for item, version in zip(records, versions):
            if item.version != version:
                _fail("STALE_VERSION")
            if self._effective(item, now) == "EXPIRED":
                _fail("INTENT_EXPIRED")
            if item.status != "OPEN" or item.cycle_id != 0:
                _fail("INTENT_UNAVAILABLE")
        terms = [_terms(records[i], intent_ids[(i + 1) % 3]) for i in range(3)]
        # Normalize cyclic rotation, preserving direction; reversal remains different.
        start = intent_ids.index(min(intent_ids))
        terms = terms[start:] + terms[:start]
        canonical = self._canonical(terms)
        identity = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        if self.declined.get(identity, False):
            _fail("DECLINED_SNAPSHOT")
        if identity in self.proposals:
            _fail("DUPLICATE_PROPOSAL")
        deadline = min(now + 3 * DAY, min(int(t.expires_at) for t in terms))
        return terms, canonical, identity, deadline

    def _reserve_accepted_cycle(
        self, intent_ids: list[int], versions: list[int], edges: list[list[int]]
    ) -> int:
        """Internal deterministic seam. No public entry point or verdict parameter.

        Only a future legitimate consensus method may call this after every edge
        is accepted. Phase 1 calls it solely from offline controlled test fixtures.
        This method creates no semantic assessment or Validator evidence.
        """
        terms, canonical, identity, deadline = self._prepare_cycle(intent_ids, versions, edges)
        if self.cycle_count == MAX_U64:
            _fail("COUNTER_OVERFLOW")
        cycle_id = u64(self.cycle_count + 1)
        self.cycles[cycle_id] = Cycle(
            cycle_id, identity, canonical, terms, [False] * 3, u64(_now()), u64(deadline), "PENDING"
        )
        for term in terms:
            item = self.intents[term.intent_id]
            item.status = "RESERVED"
            item.cycle_id = cycle_id
            if item.owner not in self.owner_cycles:
                self.owner_cycles[item.owner] = []
            self.owner_cycles[item.owner].append(cycle_id)
        self.proposals[identity] = cycle_id
        self.cycle_count = cycle_id
        return int(cycle_id)

    def _pending(self, cycle_id: int) -> Cycle:
        cycle = self._cycle(cycle_id)
        if cycle.status != "PENDING":
            _fail("CYCLE_NOT_PENDING")
        if _now() >= cycle.confirmation_deadline:
            _fail("CYCLE_EXPIRED")
        return cycle

    def _participant(self, cycle: Cycle) -> int:
        for i in range(3):
            if cycle.terms[i].owner == _owner():
                return i
        _fail("UNAUTHORIZED")
        return -1

    def _verify_snapshot(self, cycle: Cycle) -> None:
        if len(cycle.terms) != 3 or len(cycle.confirmations) != 3:
            _fail("SNAPSHOT_MISMATCH")
        terms = list(cycle.terms)
        ids = [int(t.intent_id) for t in terms]
        if len(set(ids)) != 3 or len({t.owner for t in terms}) != 3 or ids[0] != min(ids):
            _fail("SNAPSHOT_MISMATCH")
        for i, term in enumerate(terms):
            if term.supplies_to != terms[(i + 1) % 3].intent_id:
                _fail("SNAPSHOT_MISMATCH")
            item = self._intent(int(term.intent_id))
            if self._effective(item, _now()) == "EXPIRED":
                _fail("INTENT_EXPIRED")
            if item.status != "RESERVED" or item.cycle_id != cycle.cycle_id:
                _fail("RESERVATION_MISMATCH")
            if _term_values(_terms(item, int(term.supplies_to))) != _term_values(term):
                _fail("SNAPSHOT_MISMATCH")
        canonical = self._canonical(terms)
        if (
            canonical != cycle.canonical_snapshot
            or hashlib.sha256(canonical.encode("utf-8")).hexdigest() != cycle.snapshot_id
        ):
            _fail("SNAPSHOT_MISMATCH")
        expected_deadline = min(int(cycle.created_at) + 3 * DAY, min(int(t.expires_at) for t in terms))
        if cycle.confirmation_deadline != expected_deadline or cycle.created_at > _now():
            _fail("SNAPSHOT_MISMATCH")

    @gl.public.write
    def confirm_cycle(self, cycle_id: int, snapshot_id: str) -> bool:
        cycle = self._pending(cycle_id)
        index = self._participant(cycle)
        if snapshot_id != cycle.snapshot_id:
            _fail("SNAPSHOT_MISMATCH")
        self._verify_snapshot(cycle)
        if cycle.confirmations[index]:
            return False
        activates = all(cycle.confirmations[i] for i in range(3) if i != index)
        if activates and self.active_count == MAX_U64:
            _fail("COUNTER_OVERFLOW")
        # Preflight verifies all three even for confirmations one and two.
        cycle.confirmations[index] = True
        if all(cycle.confirmations):
            for term in cycle.terms:
                self.intents[term.intent_id].status = "CONSUMED"
            cycle.status = "ACTIVE"
            self.active_count = u64(self.active_count + 1)
        return True

    def _preflight_finish_counter(self, status: str) -> None:
        counter = self.aborted_count if status == "ABORTED" else self.expired_cycle_count
        if counter == MAX_U64:
            _fail("COUNTER_OVERFLOW")

    def _finish(self, cycle: Cycle, status: str) -> None:
        if len(cycle.terms) != 3:
            _fail("SNAPSHOT_MISMATCH")
        ids = [int(t.intent_id) for t in cycle.terms]
        if len(set(ids)) != 3:
            _fail("SNAPSHOT_MISMATCH")
        # Resolve every record before changing any, including during cleanup.
        records = [self._intent(i) for i in ids]
        self._preflight_finish_counter(status)
        # Fixed three-record loop; release only reservations owned by this cycle.
        for item in records:
            if item.status == "RESERVED" and item.cycle_id == cycle.cycle_id:
                item.status = "EXPIRED" if _now() >= item.expires_at else "OPEN"
                item.cycle_id = u64(0)
        cycle.status = status
        if status == "ABORTED":
            self.aborted_count = u64(self.aborted_count + 1)
        else:
            self.expired_cycle_count = u64(self.expired_cycle_count + 1)

    @gl.public.write
    def decline_cycle(self, cycle_id: int, snapshot_id: str) -> None:
        cycle = self._pending(cycle_id)
        self._participant(cycle)
        if snapshot_id != cycle.snapshot_id:
            _fail("SNAPSHOT_MISMATCH")
        self._verify_snapshot(cycle)
        self._preflight_finish_counter("ABORTED")
        self.declined[cycle.snapshot_id] = True
        self._finish(cycle, "ABORTED")

    @gl.public.write
    def expire_cycle(self, cycle_id: int) -> bool:
        cycle = self._cycle(cycle_id)
        if cycle.status == "EXPIRED":
            return False
        if cycle.status != "PENDING":
            _fail("CYCLE_NOT_PENDING")
        if _now() < cycle.confirmation_deadline:
            _fail("DEADLINE_NOT_REACHED")
        self._finish(cycle, "EXPIRED")
        return True

    def _intent_view(self, item: Intent) -> dict:
        return {
            "intent_id": int(item.intent_id),
            "owner": item.owner,
            "offer_description": item.offer_description,
            "offer_limitations": item.offer_limitations,
            "need_description": item.need_description,
            "need_requirements": item.need_requirements,
            "version": int(item.version),
            "expires_at": int(item.expires_at),
            "status": self._effective(item, _now()),
            "stored_status": item.status,
            "cycle_id": int(item.cycle_id),
        }

    def _cycle_view(self, cycle: Cycle) -> dict:
        terms = [_term_values(t) for t in cycle.terms]
        status = (
            "EXPIRED" if cycle.status == "PENDING" and _now() >= cycle.confirmation_deadline else cycle.status
        )
        return {
            "cycle_id": int(cycle.cycle_id),
            "snapshot_id": cycle.snapshot_id,
            "canonical_snapshot": cycle.canonical_snapshot,
            "terms": terms,
            "intent_ids": [t[0] for t in terms],
            "owners": [t[1] for t in terms],
            "edges": [[t[0], t[8]] for t in terms],
            "versions": [t[6] for t in terms],
            "confirmations": list(cycle.confirmations),
            "confirmation_count": sum(cycle.confirmations),
            "created_at": int(cycle.created_at),
            "confirmation_deadline": int(cycle.confirmation_deadline),
            "status": status,
            "stored_status": cycle.status,
        }

    @gl.public.view
    def get_intent(self, intent_id: int) -> dict:
        _uint(intent_id)
        return (
            {"found": False}
            if u64(intent_id) not in self.intents
            else {"found": True, **self._intent_view(self.intents[u64(intent_id)])}
        )

    @gl.public.view
    def get_cycle(self, cycle_id: int) -> dict:
        _uint(cycle_id)
        return (
            {"found": False}
            if u64(cycle_id) not in self.cycles
            else {"found": True, **self._cycle_view(self.cycles[u64(cycle_id)])}
        )

    def _page(self, offset: int, limit: int, total: int) -> tuple[int, int]:
        _uint(offset, False)
        _uint(limit)
        if limit > MAX_PAGE:
            _fail("PAGE_TOO_LARGE")
        start = min(offset, total)
        return start, min(start + limit, total)

    @gl.public.view
    def get_intents_page(self, offset: int = 0, limit: int = 20) -> dict:
        start, end = self._page(offset, limit, int(self.intent_count))
        return {
            "records": [self._intent_view(self.intents[u64(i + 1)]) for i in range(start, end)],
            "total": int(self.intent_count),
            "next_offset": end,
            "has_more": end < self.intent_count,
        }

    @gl.public.view
    def get_cycles_page(self, offset: int = 0, limit: int = 20) -> dict:
        start, end = self._page(offset, limit, int(self.cycle_count))
        return {
            "records": [self._cycle_view(self.cycles[u64(i + 1)]) for i in range(start, end)],
            "total": int(self.cycle_count),
            "next_offset": end,
            "has_more": end < self.cycle_count,
        }

    @gl.public.view
    def get_owner_records(self, owner: str, offset: int = 0, limit: int = 20) -> dict:
        try:
            owner = str(Address(owner)).lower()
        except Exception:
            _fail("INVALID_ADDRESS")
        intents = self.owner_intents.get(owner, [])
        cycles = self.owner_cycles.get(owner, [])
        start_i, end_i = self._page(offset, limit, len(intents))
        start_c, end_c = self._page(offset, limit, len(cycles))
        return {
            "owner": owner,
            "intents": [self._intent_view(self.intents[intents[i]]) for i in range(start_i, end_i)],
            "cycles": [self._cycle_view(self.cycles[cycles[i]]) for i in range(start_c, end_c)],
            "intent_total": len(intents),
            "cycle_total": len(cycles),
            "next_offset": max(end_i, end_c),
            "has_more": end_i < len(intents) or end_c < len(cycles),
            "unfinished_count": sum(
                self._effective(self.intents[i], _now()) in ("OPEN", "RESERVED")
                for i in self.owner_slots.get(owner, [])
            ),
        }

    @gl.public.view
    def get_protocol_stats(self, offset: int = 0, limit: int = 50) -> dict:
        # Expiration is time-dependent: bounded pages provide effective counts;
        # O(1) cumulative counters are global and never mislabeled as live counts.
        start, end = self._page(offset, limit, int(self.intent_count))
        counts = {s: 0 for s in ("OPEN", "RESERVED", "CONSUMED", "CANCELLED", "EXPIRED")}
        for i in range(start, end):
            counts[self._effective(self.intents[u64(i + 1)], _now())] += 1
        return {
            "protocol": PROTOCOL,
            "network_id": int(self.network_id),
            "intent_total": int(self.intent_count),
            "cycle_total": int(self.cycle_count),
            "active_total": int(self.active_count),
            "aborted_total": int(self.aborted_count),
            "expired_cycles_cleaned": int(self.expired_cycle_count),
            "effective_intent_counts_page": counts,
            "offset": start,
            "next_offset": end,
            "has_more": end < self.intent_count,
            "semantic_matching_available": False,
        }
