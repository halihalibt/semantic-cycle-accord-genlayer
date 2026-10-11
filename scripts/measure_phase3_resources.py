"""Reproducible local allocation/storage measurements; never network gas estimates."""

import hashlib
import json
from pathlib import Path
import socket
import time
import tracemalloc

from gltest.direct import VMContext, create_address, deploy_contract
from gltest.direct.sdk_loader import setup_sdk_paths

ROOT = Path(__file__).resolve().parents[1]


def main():
    setup_sdk_paths(version="v0.2.16")

    def blocked(*args, **kwargs):
        raise AssertionError("Resource probe must remain offline")

    socket.socket.connect = blocked
    socket.socket.connect_ex = blocked
    vm = VMContext()
    vm._chain_id = 61999
    vm.sender = create_address("phase3-resource-owner")
    vm.warp("2026-10-11T12:00:00Z")
    rows = []
    with vm.activate():
        c = deploy_contract(ROOT / "contracts/semantic_cycle_accord.py", vm, sdk_version="v0.2.16")
        owner = str(vm.sender)
        reads = 0
        writes = 0
        native_read, native_write = vm._storage.do_read, vm._storage.do_write

        def read(*args):
            nonlocal reads
            reads += 1
            return native_read(*args)

        def write(*args):
            nonlocal writes
            writes += 1
            return native_write(*args)

        vm._storage.do_read, vm._storage.do_write = read, write
        for i in range(200):
            cid = c.create_intent("O" * 512, "L" * 512, "N" * 512, "R" * 512, 1792584000)
            c.cancel_intent(cid, 1)
            if i + 1 in (1, 50, 200):
                reads = writes = 0
                start = time.perf_counter()
                page = c.get_owner_records(owner, 0, 50)
                rows.append(
                    {
                        "historical_intents": i + 1,
                        "returned": len(page["intents"]),
                        "sdk_reads": reads,
                        "sdk_writes": writes,
                        "seconds": time.perf_counter() - start,
                        "serialized_nonzero_bytes": sum(
                            len(v.rstrip(b"\0")) for v in vm._storage.snapshot().values()
                        ),
                        "working_slots": len(c.owner_slots[owner.lower()]),
                    }
                )
        import sys

        m = sys.modules["_contract_semantic_cycle_accord"]
        sizes = []
        for text in ("\x00" * 512, "<" * 512, "🙂" * 128):
            ids = []
            for i in range(3):
                vm.sender = create_address(f"phase3-resource-ring-{i}")
                ids.append(c.create_intent(text, text, text, text, 1792584000))
            edges = [[ids[i], ids[(i + 1) % 3]] for i in range(3)]
            tracemalloc.start()
            snap = c._prepare_cycle(ids, [1] * 3, edges)[1]
            prompt = m._assessment_prompt(snap)
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            sizes.append(
                {
                    "field_utf8_bytes": len(text.encode()),
                    "first_codepoint": ord(text[0]),
                    "snapshot_utf8_bytes": len(snap.encode()),
                    "prompt_utf8_bytes": len(prompt.encode()),
                    "python_peak_allocated_bytes": peak,
                }
            )
    result = {
        "level": "SDK Direct Mode; Python allocations and storage read/write counts only",
        "source_sha256": hashlib.sha256(
            (ROOT / "contracts/semantic_cycle_accord.py").read_bytes()
        ).hexdigest(),
        "history_pages": rows,
        "max_input_samples": sizes,
        "conservative_bounds": {"canonical_snapshot_utf8_bytes_lt": 38000, "prompt_utf8_bytes_lt": 45000},
        "network_gas": "NOT MEASURED",
        "cumulative_history": "grows; u32 SDK lengths and offsets are finite",
        "tcp_calls": 0,
    }
    (ROOT / "evidence/phase3/resource-measurements.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
