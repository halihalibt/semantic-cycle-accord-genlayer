import ast
from pathlib import Path

import pytest

EDGES = [[1, 2], [2, 3], [3, 1]]


def call(h, ids=None, versions=None, edges=None):
    return h.c.assess_cycle(ids or [1, 2, 3], versions or [1] * 3, edges or EDGES)


@pytest.mark.parametrize(
    "fault,error",
    [
        ("duplicate_owner", "DUPLICATE_OWNER"),
        ("duplicate_intent", "DUPLICATE_INTENT"),
        ("bad_ring", "INVALID_RING"),
        ("stale", "STALE_VERSION"),
        ("expired", "INTENT_EXPIRED"),
        ("reserved", "INTENT_UNAVAILABLE"),
        ("outsider", "UNAUTHORIZED"),
        ("assessment_counter", "COUNTER_OVERFLOW"),
        ("cycle_counter", "COUNTER_OVERFLOW"),
    ],
)
def test_pre_ai_faults_never_call_llm_or_write(h, fault, error):
    h.ring((0, 1, 0) if fault == "duplicate_owner" else (0, 1, 2))
    h.sender(0)
    kwargs = {}
    if fault == "duplicate_intent":
        kwargs = {"ids": [1, 1, 3]}
    if fault == "bad_ring":
        kwargs = {"edges": [[1, 3], [2, 3], [3, 1]]}
    if fault == "stale":
        kwargs = {"versions": [2, 1, 1]}
    if fault == "expired":
        h.warp(h.now + 10 * 86400)
    if fault == "reserved":
        h.reserve([1, 2, 3])
    if fault == "outsider":
        h.sender(9)
    if fault == "assessment_counter":
        h.c.assessment_count = 2**64 - 1
    if fault == "cycle_counter":
        h.c.cycle_count = 2**64 - 1
    before = h.storage()
    with pytest.raises(Exception, match=error):
        call(h, **kwargs)
    assert h.storage() == before and not h.vm._captured_validators
    assert h.c.get_assessment(1) == {"found": False}


@pytest.mark.parametrize(
    "output",
    [
        "invalid json",
        "{",
        "{}",
        '{"decisions":["FIT","FIT"]}',
        '{"decisions":["FIT","FIT","FIT"],"admin":true}',
        '{"decisions":["FIT",null,"FIT"]}',
    ],
)
def test_actual_native_malformed_leader_no_mutation(h, output):
    h.ring()
    h.sender(0)
    h.vm.mock_llm("semantic compatibility classifier", output)
    before = h.storage()
    with pytest.raises(Exception, match="INVALID_CLASSIFICATION"):
        call(h)
    assert h.storage() == before and not h.vm._captured_validators
    assert h.c.get_assessment(1) == {"found": False}


def test_native_leader_error_no_mutation(h):
    h.ring()
    h.sender(0)
    before = h.storage()
    with pytest.raises(Exception, match="No LLM mock"):
        call(h)
    assert h.storage() == before


def test_vm_consensus_execution_failure_boundary_no_mutation(h, contract_module, monkeypatch):
    h.ring()
    h.sender(0)
    before = h.storage()

    def failed(leader, validator):
        raise contract_module.gl.vm.UserError("CONSENSUS_EXECUTION_FAILED")

    # Fault injection at the VM API boundary, not a fake network voting procedure.
    monkeypatch.setattr(contract_module.gl.vm, "run_nondet_unsafe", failed)
    with pytest.raises(Exception, match="CONSENSUS_EXECUTION_FAILED"):
        call(h)
    assert h.storage() == before


@pytest.mark.parametrize("bad", [None, {"decisions": ["FIT"] * 3}, ["FIT"] * 2, ["FIT", "FIT", "ACCEPT"]])
def test_unexpected_vm_result_rejected_after_block(h, contract_module, monkeypatch, bad):
    h.ring()
    h.sender(0)
    before = h.storage()
    monkeypatch.setattr(contract_module.gl.vm, "run_nondet_unsafe", lambda *args: bad)
    with pytest.raises(Exception, match="INVALID_CLASSIFICATION"):
        call(h)
    assert h.storage() == before


@pytest.mark.parametrize(
    "fault,error",
    [
        ("version", "STALE_VERSION"),
        ("content", "SNAPSHOT_MISMATCH"),
        ("expired", "INTENT_EXPIRED"),
        ("reserved", "INTENT_UNAVAILABLE"),
        ("owner", "SNAPSHOT_MISMATCH"),
        ("caller", "UNAUTHORIZED"),
        ("assessment_counter", "COUNTER_OVERFLOW"),
        ("cycle_counter", "COUNTER_OVERFLOW"),
        ("resolved", "DUPLICATE_ASSESSMENT"),
        ("declined", "DECLINED_SNAPSHOT"),
    ],
)
def test_post_consensus_hostile_state_rejected_without_additional_mutation(
    h, contract_module, monkeypatch, fault, error
):
    m = contract_module
    h.ring()
    h.sender(0)
    identity = h.c._prepare_cycle([1, 2, 3], [1] * 3, EDGES)[2]
    h.vm.mock_llm("semantic compatibility classifier", '{"decisions":["FIT","FIT","FIT"]}')
    native = m.gl.nondet.exec_prompt
    after = {}

    def changed(prompt, **kwargs):
        output = native(prompt, **kwargs)
        if fault == "version":
            h.c.intents[1].version = 2
        if fault == "content":
            h.c.intents[1].offer_description = "Substituted capability"
        if fault == "owner":
            h.c.intents[1].owner = str(h.accounts[9]).lower()
        if fault == "caller":
            h.sender(9)
        if fault == "expired":
            h.warp(h.now + 10 * 86400)
        if fault == "reserved":
            h.c.intents[1].status = "RESERVED"
            h.c.intents[1].cycle_id = 999
        if fault == "assessment_counter":
            h.c.assessment_count = 2**64 - 1
        if fault == "cycle_counter":
            h.c.cycle_count = 2**64 - 1
        if fault == "resolved":
            h.c.assessed_snapshots[identity] = 999
        if fault == "declined":
            h.c.declined[identity] = True
        after.update(h.storage())
        return output

    # Offline hostile mutation is only a test of deterministic rechecks, never
    # an allowed nondeterministic production storage operation.
    monkeypatch.setattr(m.gl.nondet, "exec_prompt", changed)
    with pytest.raises(Exception, match=error):
        call(h)
    assert h.storage() == after
    assert h.c.get_assessment(1) == {"found": False}
    assert h.c.get_cycle(1) == {"found": False}


def test_record_allocation_failure_before_reservations(h, contract_module, monkeypatch):
    h.ring()
    h.sender(0)
    h.vm.mock_llm("semantic compatibility classifier", '{"decisions":["FIT","FIT","FIT"]}')
    before = h.storage()

    def failed(*args):
        raise MemoryError("record allocation fault")

    monkeypatch.setattr(contract_module, "Assessment", failed)
    with pytest.raises(MemoryError, match="record allocation fault"):
        call(h)
    assert h.storage() == before and int(h.c.assessment_count) == 0
    assert all(h.c.get_intent(i)["status"] == "OPEN" for i in (1, 2, 3))


def test_reservation_preflight_failure_no_assessment_record(h, contract_module, monkeypatch):
    h.ring()
    h.sender(0)
    h.vm.mock_llm("semantic compatibility classifier", '{"decisions":["FIT","FIT","FIT"]}')
    before = h.storage()

    def failed(*args):
        raise contract_module.gl.vm.UserError("reservation fault")

    monkeypatch.setattr(contract_module.SemanticCycleAccord, "_reserve_accepted_cycle", failed)
    with pytest.raises(Exception, match="reservation fault"):
        call(h)
    assert h.storage() == before


@pytest.mark.parametrize("field", ["assessment_count", "cycle_count"])
def test_counter_last_increment(h, field):
    h.ring()
    h.sender(0)
    setattr(h.c, field, 2**64 - 2)
    h.vm.mock_llm("semantic compatibility classifier", '{"decisions":["FIT","FIT","FIT"]}')
    result = call(h)
    assert int(getattr(h.c, field)) == 2**64 - 1
    assert h.vm.run_validator() is True
    assert h.c.get_assessment(result["assessment_id"])["cycle_id"] == result["cycle_id"]


@pytest.mark.parametrize("phase", ["cycle_write", "assessment_write", "replay_write"])
def test_unexpected_persistence_failure_transaction_boundary_simulation(
    h, contract_module, monkeypatch, phase
):
    # Direct Mode does not implement transactional exception rollback. Explicitly
    # simulate that boundary with its supported snapshot/revert API. This test
    # is NOT evidence of full GenVM WASM transaction rollback.
    h.ring()
    h.sender(0)
    h.vm.mock_llm("semantic compatibility classifier", '{"decisions":["FIT","FIT","FIT"]}')
    before = h.storage()
    checkpoint = h.vm.snapshot()
    map_type = type(h.c.assessments)
    original = map_type.__setitem__

    def failed(mapping, key, value):
        hit = phase == "assessment_write" and isinstance(value, contract_module.Assessment)
        hit = hit or (phase == "cycle_write" and isinstance(value, contract_module.Cycle))
        hit = hit or (phase == "replay_write" and isinstance(key, str) and isinstance(value, int))
        if hit:
            raise MemoryError("persistence fault")
        return original(mapping, key, value)

    monkeypatch.setattr(map_type, "__setitem__", failed)
    with pytest.raises(MemoryError, match="persistence fault"):
        try:
            call(h)
        except Exception:
            h.vm.revert(checkpoint)
            raise
    assert h.storage() == before
    assert h.c.get_assessment(1) == h.c.get_cycle(1) == {"found": False}
    assert all(h.c.get_intent(i)["status"] == "OPEN" for i in (1, 2, 3))


def test_public_signature_and_nondet_storage_boundary(contract_module):
    import inspect

    assert list(inspect.signature(contract_module.SemanticCycleAccord.assess_cycle).parameters) == [
        "self",
        "intent_ids",
        "versions",
        "edges",
    ]
    tree = ast.parse(Path("contracts/semantic_cycle_accord.py").read_text())
    function = next(
        n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_consensus_decisions"
    )
    for node in ast.walk(function):
        assert not isinstance(node, ast.Attribute) or node.attr not in (
            "intents",
            "cycles",
            "assessments",
            "assessed_snapshots",
        )
        assert not isinstance(node, ast.Name) or node.id != "self"
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "SemanticCycleAccord"]
    public = [n.name for n in classes[0].body if isinstance(n, ast.FunctionDef) and n.decorator_list]
    assert len(public) == 14 and all(not n.startswith("_") for n in public)
    assert not set(public) & {
        "inject_ai_verdict",
        "set_assessment_verdict",
        "reserve_cycle",
        "set_leader_output",
    }


def test_phase1_deterministic_methods_and_storage_fields_preserved():
    import subprocess

    baseline = subprocess.run(
        ["git", "show", "cc773e936cf6184d0b3f9447771ac804e597bfe7:contracts/semantic_cycle_accord.py"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    trees = [ast.parse(baseline), ast.parse(Path("contracts/semantic_cycle_accord.py").read_text())]
    classes = [
        next(n for n in t.body if isinstance(n, ast.ClassDef) and n.name == "SemanticCycleAccord")
        for t in trees
    ]
    fields = [[ast.dump(n) for n in c.body if isinstance(n, ast.AnnAssign)] for c in classes]
    assert fields[1][: len(fields[0])] == fields[0]
    assert len(fields[1]) == len(fields[0]) + 3
    methods = [{n.name: n for n in c.body if isinstance(n, ast.FunctionDef)} for c in classes]
    for name, old in methods[0].items():
        new = methods[1][name]
        assert ast.dump(old.args) == ast.dump(new.args)
        assert [ast.dump(d) for d in old.decorator_list] == [ast.dump(d) for d in new.decorator_list]
        if name == "get_protocol_stats":
            continue  # Authorized availability flag and assessment count additions.
        # A documentation change on the private seam does not change behavior.
        bodies = [
            n.body[1:]
            if isinstance(n.body[0], ast.Expr)
            and isinstance(n.body[0].value, ast.Constant)
            and isinstance(n.body[0].value.value, str)
            else n.body
            for n in (old, new)
        ]
        assert [ast.dump(n) for n in bodies[0]] == [ast.dump(n) for n in bodies[1]], name
