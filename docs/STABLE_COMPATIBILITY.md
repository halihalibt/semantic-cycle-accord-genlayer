# Stable Compatibility — Phase 1

## Authoritative target and verification level

The sole target is Stable Studionet, chain ID 61999, RPC
`https://studio.genlayer.com/api`. One read-only `eth_chainId` request returned
`0xf22f` (61999). No deployment, write RPC, faucet action, wallet signature,
private key, or network-backed contract integration test was performed.

Compatibility evidence consists of the exact official v0.2.16 Python runner,
offline SDK-backed storage execution, SDK semantic validation, and schema
generation. It is not full GenVM WASM execution, real onchain execution, or
Validator consensus. Those checks belong to separately authorized later phases.

## Validated versions and identities

| Component | Version / identity | Actual check |
| --- | --- | --- |
| Python | 3.12.14 | Interpreter, compile/import and complete test execution |
| GenVM release bundle | v0.2.16 | Downloaded official archive; SHA-256 recorded and pinned |
| py-genlayer runner | 1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6 | Contract header; Direct Mode and semantic validation |
| py-lib-genlayer-std | 11rhn002yfajawsz7fai6mykznbxkxs6l91iskj5cm82c92qhy3v | Exact dependency from official runner manifest |
| py-lib-cloudpickle | 1dlk6mnfabi0z7r39635amyfzw8xb6rm8bv4pmgv6ji1bfx9hghd | Exact dependency; SDK storage root serialized, restored and read |
| SDK-bundled cloudpickle | 3.1.0.dev0 | Version label of the library bundled with frozen stable runner, not an independently selected release candidate |
| genlayer-test | 0.29.2 | Direct Mode, calldata checks, storage-manager byte snapshots |
| genvm-linter | 0.11.0 | AST check, SDK semantic validation, 12-method schema export |
| pytest | 9.1.1 | 176 executed tests, none skipped |
| Ruff | 0.14.0 | Source/tests/scripts lint and formatting |
| genlayer-py | 0.16.3 | Transitive dependency only; no RPC client used for tests or transactions |
| genlayer-js | 1.1.8 reference | JavaScript package identity identified in preflight; NOT installed/executed and not required here |

Official archive:
`https://github.com/genlayerlabs/genvm/releases/download/v0.2.16/genvm-universal.tar.xz`

Archive SHA-256:
`4f0b358ec98ec148be9b95cdfb0f0e1a6cbe64da0194fdfac3fffc6f5d1d93e2`

The checksum records the actual downloaded artifact; it is not represented as
an independently signed publisher checksum. `bootstrap_sdk.py` checks it on
every run. The Python dependencies are locked in `uv.lock` and reproduced with
`uv sync --frozen`. Neither latest SDK resolution nor any newer network/tooling
line is selected.

## APIs exercised from the fixed artifact

- `gl.Contract`, `@gl.public.write` and `@gl.public.view`.
- `@allow_storage` dataclasses, typed `TreeMap` and nested `DynArray` values.
- `u64` stored counters/versions/timestamps and supported `u256` numeric map keys.
- `gl.message.sender_address`, `contract_address` and `chain_id`.
- `datetime.now(timezone.utc)` transaction clock, dynamically warped in Direct Mode.
- `gl.vm.UserError`, canonical JSON, UTF-8 and `hashlib.sha256`.
- Calldata argument roundtrip and explicit return-value roundtrip checks.
- SDK storage-root cloudpickle roundtrip, persisted byte serialization, fresh
  root reconstruction, and independent confirmation/activation after restoration.

Ordinary Python pickle cannot serialize this SDK's dynamically generated
storage descriptors. The official runtime's bundled cloudpickle handles them;
the original storage-root check was retained with that serializer. Ordinary
pickle still roundtrips the underlying serialized byte-storage map. This does
not weaken or bypass the storage-schema test.

The linter's supported key list does not include `u64`, even though direct
storage could execute it. Record map annotations therefore use documented
`u256`; actual IDs remain restricted to unsigned 64 bits. The final linter has
no warning or suppression. No SDK monkeypatch changes protocol behavior.

## Documentation reviewed

- https://docs.genlayer.com/developers/networks
- https://docs.genlayer.com/developers/intelligent-contracts/storage
- https://docs.genlayer.com/developers/intelligent-contracts/types/dataclasses
- https://docs.genlayer.com/developers/intelligent-contracts/features/transaction-context
- https://docs.genlayer.com/developers/intelligent-contracts/testing
- https://docs.genlayer.com/api-references/genlayer-test/direct

Current documentation can cover newer APIs. This implementation additionally
verified its used APIs against the frozen v0.2.16 artifact. Offline fixtures
set the chain context to 61999; invalid-chain rejection is an offline negative
test, not a connection to any other network.

## Limitations and decisions

No critical deterministic API blocker remains. Real semantic matching,
production invocation of the accepted-result seam, full VM execution and live
consensus remain untested/unimplemented as required by the phase boundary.
The SDK probe and Direct Mode fixture addresses are artificial and must never
be advertised as deployments. Python compatibility is validated on 3.12.14,
not across every Python release or operating system.
