from datetime import datetime, timezone
from pathlib import Path
import sys
import socket

import pytest
from gltest.direct import VMContext, create_address, deploy_contract
from gltest.direct.sdk_loader import CACHE_DIR, extract_runner

ROOT = Path(__file__).resolve().parents[1]
BASE = 1791720000
DAY = 86400


@pytest.fixture(autouse=True)
def offline_only(monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError("Network calls are forbidden in the deterministic suite")

    monkeypatch.setattr(socket.socket, "connect", blocked)
    monkeypatch.setattr(socket.socket, "connect_ex", blocked)


class Harness:
    def __init__(self, vm, contract):
        self.vm = vm
        self.c = contract
        self.accounts = [create_address(f"sca3-test-{i}") for i in range(10)]
        self.now = BASE

    def sender(self, i):
        self.vm.sender = self.accounts[i]

    def warp(self, now):
        self.now = now
        self.vm.warp(datetime.fromtimestamp(now, timezone.utc).isoformat())

    def create(
        self,
        owner=0,
        offer="Design a logo",
        limitations="One revision",
        need="Translate a page",
        requirements="English",
        expires=None,
    ):
        self.sender(owner)
        return self.c.create_intent(
            offer, limitations, need, requirements, self.now + 10 * DAY if expires is None else expires
        )

    def ring(self, owners=(0, 1, 2), expires=None):
        return [self.create(owner, offer=f"Service {i}", expires=expires) for i, owner in enumerate(owners)]

    def reserve(self, ids=None, versions=None, edges=None):
        if ids is None:
            ids = self.ring()
        if versions is None:
            versions = [self.c.get_intent(i)["version"] for i in ids]
        if edges is None:
            edges = [[ids[i], ids[(i + 1) % 3]] for i in range(3)]
        return self.c._reserve_accepted_cycle(ids, versions, edges)

    def confirm(self, cycle=1, owner=0, digest=None):
        self.sender(owner)
        return self.c.confirm_cycle(
            cycle, self.c.get_cycle(cycle)["snapshot_id"] if digest is None else digest
        )

    def update(self, intent=1, version=None, **changes):
        item = self.c.get_intent(intent)
        fields = {
            name: item[name]
            for name in (
                "offer_description",
                "offer_limitations",
                "need_description",
                "need_requirements",
                "expires_at",
            )
        }
        fields.update(changes)
        return self.c.update_intent(intent, item["version"] if version is None else version, **fields)

    def storage(self):
        # InmemManager allocates zero-filled buffers on reads; compare actual
        # nonzero content rather than treating a read allocation as a write.
        return {
            key: value.rstrip(b"\0")
            for key, value in self.vm._storage.snapshot().items()
            if value.rstrip(b"\0")
        }


@pytest.fixture
def h():
    pickler = extract_runner(
        CACHE_DIR / "genvm-universal-v0.2.16.tar.xz",
        "py-lib-cloudpickle",
        "1dlk6mnfabi0z7r39635amyfzw8xb6rm8bv4pmgv6ji1bfx9hghd",
        "v0.2.16",
    )
    pickler_path = str(pickler / "src")
    if pickler_path not in sys.path:
        sys.path.insert(0, pickler_path)
    vm = VMContext()
    vm._chain_id = 61999
    vm.sender = create_address("sca3-initial-caller")
    vm.warp("2026-10-11T12:00:00+00:00")
    with vm.activate():
        contract = deploy_contract(ROOT / "contracts/semantic_cycle_accord.py", vm, sdk_version="v0.2.16")
        yield Harness(vm, contract)


@pytest.fixture
def contract_module(h):
    return sys.modules["_contract_semantic_cycle_accord"]
