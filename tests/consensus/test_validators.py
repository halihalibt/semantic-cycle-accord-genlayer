import json

import pytest

from .test_prompt_parser import BAD_OUTPUTS


def prime(h, m, decisions=None):
    h.vm.mock_llm("SCA3 offline", json.dumps({"decisions": decisions or ["FIT"] * 3}))
    before = h.storage()
    result = m._consensus_decisions("SCA3 offline")
    assert h.storage() == before
    return result


@pytest.mark.parametrize(
    "leader,validator,expected",
    [
        (["FIT"] * 3, ["FIT"] * 3, True),
        (["FIT"] * 3, ["NO_FIT", "FIT", "FIT"], False),
        (["FIT"] * 3, ["FIT", "UNSURE", "FIT"], False),
        (["FIT"] * 3, ["FIT", "FIT", "NO_FIT"], False),
        (["FIT"] * 3, ["UNSURE", "NO_FIT", "FIT"], False),
        (["FIT", "NO_FIT", "FIT"], ["FIT", "NO_FIT", "FIT"], True),
        (["UNSURE"] * 3, ["UNSURE"] * 3, True),
        (["FIT", "NO_FIT", "UNSURE"], ["UNSURE", "NO_FIT", "FIT"], False),
    ],
)
def test_actual_captured_validator_independent_full_vector(
    h, contract_module, monkeypatch, leader, validator, expected
):
    m = contract_module
    calls = []
    native = m.gl.nondet.exec_prompt

    def spy(prompt, **kwargs):
        calls.append((prompt, kwargs))
        assert h.storage() == before
        return native(prompt, **kwargs)

    before = h.storage()
    monkeypatch.setattr(m.gl.nondet, "exec_prompt", spy)
    assert prime(h, m, leader) == leader
    h.vm.clear_mocks()
    h.vm.mock_llm("SCA3 offline", json.dumps({"decisions": validator}, indent=2))
    assert h.vm.run_validator() is expected
    assert calls == [("SCA3 offline", {"response_format": "json"})] * 2
    assert h.storage() == before


@pytest.mark.parametrize("bad", BAD_OUTPUTS)
def test_leader_return_shape_checked_before_independent_call(h, contract_module, monkeypatch, bad):
    m = contract_module
    prime(h, m)

    calls = []
    native = m.gl.nondet.exec_prompt
    valid = bad == ["FIT"] * 3

    def checked(*args, **kwargs):
        assert valid, "Invalid Leader result must be rejected before LLM"
        calls.append(args)
        return native(*args, **kwargs)

    monkeypatch.setattr(m.gl.nondet, "exec_prompt", checked)
    # The actual captured callback receives Return via the supported API.
    assert h.vm.run_validator(leader_result=bad) is valid
    assert len(calls) == (1 if valid else 0)


@pytest.mark.parametrize("bad", BAD_OUTPUTS)
def test_validator_native_wire_forms_strictly_checked(h, contract_module, bad):
    prime(h, contract_module)
    h.vm.clear_mocks()
    h.vm.mock_llm("SCA3 offline", bad if isinstance(bad, str) else json.dumps(bad))
    # Valid JSON strings and tuple fixtures become valid dict/list wire values.
    # This verifies the pinned mock boundary rather than assuming raw Python types.
    wire = bad if isinstance(bad, str) else json.dumps(bad)
    try:
        expected = json.loads(wire) == {"decisions": ["FIT"] * 3}
    except ValueError:
        expected = False
    assert h.vm.run_validator() is expected


def test_return_error_forms_and_validator_exception(h, contract_module):
    m = contract_module
    prime(h, m)
    before = h.storage()
    assert h.vm.run_validator(leader_error=ValueError("leader error")) is False
    callback = h.vm._captured_validators[-1][2]
    for value in (
        m.gl.vm.VMError("failure"),
        m.gl.vm.UserError("failure"),
        ["FIT"] * 3,
        None,
        m.gl.vm.Return(m.gl.vm.Return(["FIT"] * 3)),
    ):
        assert callback(value) is False
    h.vm.clear_mocks()  # Missing native LLM mock raises the actual mock error.
    assert h.vm.run_validator() is False
    assert h.storage() == before


def test_actual_leader_exception_propagates_without_capture(h, contract_module):
    before = h.storage()
    with pytest.raises(Exception, match="No LLM mock"):
        contract_module._consensus_decisions("SCA3 offline")
    assert not h.vm._captured_validators
    assert h.storage() == before


def test_closure_serialization_pinned_cloudpickle(h, contract_module):
    import cloudpickle

    prime(h, contract_module)
    _, leader, validator = h.vm._captured_validators[-1]
    assert leader.__code__.co_freevars == validator.__code__.co_freevars == ("prompt",)
    assert all(cell.cell_contents == "SCA3 offline" for cell in leader.__closure__ + validator.__closure__)
    before = h.storage()
    assert cloudpickle.loads(cloudpickle.dumps(leader))() == ["FIT"] * 3
    assert cloudpickle.loads(cloudpickle.dumps(validator))(contract_module.gl.vm.Return(["FIT"] * 3)) is True
    assert h.storage() == before
