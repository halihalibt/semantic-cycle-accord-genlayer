"""Isolated pinned executor smoke via its published host ABI; no blockchain or LLM.

Requires the checksum-verified official v0.2.16 distributions extracted together.
Only AF_UNIX host communication and disposable state are used. Native VM deltas
are applied by this test host on Return only, not advertised as network rollback.
"""

import argparse
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import tempfile

from gltest.direct.sdk_loader import setup_sdk_paths

setup_sdk_paths(version="v0.2.16")
from genlayer.py import calldata  # noqa: E402
from genlayer.py.types import Address  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def exact(sock, size):
    data = bytearray()
    while len(data) < size:
        part = sock.recv(size - len(data))
        if not part:
            raise EOFError("Executor closed its host socket")
        data.extend(part)
    return bytes(data)


def invoke(bundle, config, state, method, args, init=False, code=None):
    parent, child = socket.socketpair()
    parent.settimeout(45)
    message = {
        "contract_address": Address("0x" + "a1" * 20),
        "sender_address": Address("0x" + "b2" * 20),
        "origin_address": Address("0x" + "b2" * 20),
        "chain_id": 61999,
        "value": 0,
        "is_init": init,
        "datetime": "2026-10-11T12:00:00Z",
    }
    call = {"args": args}
    if method:
        call["method"] = method
    execution = {
        "calldata": calldata.encode(call),
        "message": message,
        "host_data": json.dumps(
            {"node_address": "offline-test", "tx_id": "offline-smoke", "signerUrl": "http://127.0.0.1:1"}
        ),
        "code": code,
        "leader_nondet_results": None,
        "method_hosts": [],
        "data_fees_limit": 10000000,
        "storage_page_cost": 1,
        "receipt_word_cost": 1,
    }
    command = [
        str(bundle / "lib/libc.so"),
        str(bundle / "executor/v0.2.16/bin/genvm"),
        "--config",
        str(config),
        "run",
        "--host",
        f"fd://{child.fileno()}",
        "--permissions",
        "rw" if init or method == "create_intent" else "r",
    ]
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        proc = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, pass_fds=(child.fileno(),)
        )
        child.close()
        reads = 0
        result = None
        try:
            proc.stdin.write(calldata.encode(execution))
            proc.stdin.close()
            while True:
                opcode = exact(parent, 1)[0]
                if opcode == 0:
                    mode = exact(parent, 1)[0]
                    address = exact(parent, 20)
                    slot = exact(parent, 32)
                    offset = int.from_bytes(exact(parent, 4), "little")
                    size = int.from_bytes(exact(parent, 4), "little")
                    reads += 1
                    assert address == message["contract_address"].as_bytes and mode in (0, 1, 2)
                    assert size <= 16 * 1024 * 1024
                    data = state.get(slot, b"")[offset : offset + size].ljust(size, b"\0")
                    parent.sendall(b"\0" + data)
                elif opcode == 2:
                    exact(parent, 8)  # Local fuel notification; not network gas evidence.
                elif opcode == 5:
                    parent.sendall(b"\0" + (2**32).to_bytes(8, "little"))
                elif opcode == 7:
                    size = int.from_bytes(exact(parent, 4), "little")
                    encoded = exact(parent, size)
                    result = calldata.decode(encoded[1:])
                    parent.sendall(b"\0")
                elif opcode == 8:
                    parent.sendall(b"\0")
                    break
                else:
                    raise AssertionError(f"Unexpected host opcode {opcode}")
            proc.wait(timeout=10)
        finally:
            parent.close()
            if proc.poll() is None:
                proc.kill()
                proc.wait()
            stdout.seek(0)
            stderr.seek(0)
            out = stdout.read().decode(errors="replace")
            err = stderr.read().decode(errors="replace")
            if result is None:
                print(f"Executor exit={proc.returncode}; stdout={out}; stderr={err}")
        if result is None:
            raise RuntimeError(f"No native result; exit={proc.returncode}; stderr={err}")
        if result["kind"] == "Return":
            for key, value in result["storage_changes"]:
                slot, offset = key[:32], 32 * int.from_bytes(key[32:], "big")
                current = bytearray(state.get(slot, b""))
                current.extend(b"\0" * max(0, offset + len(value) - len(current)))
                current[offset : offset + len(value)] = value
                state[slot] = bytes(current)
        print(json.dumps({"method": method, "kind": result["kind"], "data": result["data"], "stderr": err}))
        return {
            "method": method or "constructor",
            "command": command,
            "exit_code": proc.returncode,
            "kind": result["kind"],
            "data": result["data"],
            "storage_delta_count": len(result["storage_changes"]),
            "host_reads": reads,
            "stdout": out,
            "stderr": err,
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args()
    bundle = options.bundle.resolve()
    for name, digest in {
        "genvm-linux-amd64.tar.xz": "0e16aa26a4f70a5198eeca819a62516775a793ec96bcab4eb3f8544b55e7e75c",
        "genvm-linux-amd64-executor.tar.xz": "0d060cf4cceba4adf6a0dd886225be7a500ebbc2eb474c462a98a9743aa641ab",
    }.items():
        assert hashlib.sha256((bundle / name).read_bytes()).hexdigest() == digest
    # All paths explicit because musl loader invocation changes current_exe.
    config = bundle / "offline-config.yaml"
    config.write_text(
        "modules:\n  llm:\n    address: ws://127.0.0.1:3031\n  web:\n    address: ws://127.0.0.1:3032\n"
        f"threads: 2\nblocking_threads: 4\nlog_disable: genvm::rt::memlimiter\ncache_dir: {bundle}/cache\n"
        f"runners_dir: {bundle}/runners\nregistry_dir: {bundle}/executor/v0.2.16/data\n"
    )
    state = {}
    results = []
    code = (ROOT / "contracts/semantic_cycle_accord.py").read_bytes()
    results.append(invoke(bundle, config, state, None, [], init=True, code=code))
    assert results[-1]["kind"] == "Return", results[-1]
    results.append(invoke(bundle, config, state, "get_protocol_stats", [0, 50]))
    assert results[-1]["kind"] == "Return" and results[-1]["data"]["network_id"] == 61999
    results.append(
        invoke(
            bundle,
            config,
            state,
            "create_intent",
            ["Logo design", "One revision", "Translation", "English", 1792584000],
        )
    )
    assert results[-1]["kind"] == "Return" and results[-1]["data"] == 1
    results.append(invoke(bundle, config, state, "get_intent", [1]))
    assert results[-1]["kind"] == "Return" and results[-1]["data"]["status"] == "OPEN"
    options.output.write_text(
        json.dumps(
            {
                "execution_level": "isolated official GenVM v0.2.16 WASM; disposable host state; no blockchain",
                "source_sha256": hashlib.sha256(code).hexdigest(),
                "results": results,
                "rollback": "NOT TESTED; host applies successful Return deltas only",
                "real_consensus": "NOT RUN",
                "native_llm_calls": 0,
            },
            indent=2,
        )
        + "\n"
    )
    print("Offline WASM constructor/read/write/read smoke PASS")


if __name__ == "__main__":
    main()
