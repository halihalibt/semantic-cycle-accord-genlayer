import json
from pathlib import Path

import pytest

from .test_prompt_parser import INJECTIONS, input_data

CASES = json.loads(Path("tests/consensus/classification-fixtures.json").read_text())


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_documented_expectations_native_mock_orchestration(h, contract_module, monkeypatch, case):
    # These fixtures document intended semantics. Canned labels test the prompt,
    # native API, parsing, callback and state effects; they do not score a real LLM.
    ids = [
        h.create(
            i,
            offer=case["offer"],
            limitations=case["limitations"],
            need=case["need"],
            requirements=case["requirements"],
        )
        for i in range(3)
    ]
    h.sender(0)
    calls = []
    native = contract_module.gl.nondet.exec_prompt

    def spy(prompt, **kwargs):
        data = input_data(prompt)
        assert len(data["edges"]) == 3
        for edge in data["edges"]:
            assert edge["provider_offer_description"] == case["offer"]
            assert edge["provider_offer_limitations"] == case["limitations"]
            assert edge["recipient_need_description"] == case["need"]
            assert edge["recipient_need_requirements"] == case["requirements"]
        calls.append(prompt)
        return native(prompt, **kwargs)

    monkeypatch.setattr(contract_module.gl.nondet, "exec_prompt", spy)
    h.vm.mock_llm("semantic compatibility classifier", json.dumps({"decisions": [case["expected"]] * 3}))
    result = h.c.assess_cycle(ids, [1] * 3, [[1, 2], [2, 3], [3, 1]])
    assert h.vm.run_validator() is True
    assert len(calls) == 2 and calls[0] == calls[1]
    assert result["result"] == ("MATCHED" if case["expected"] == "FIT" else "NOT_MATCHED")
    assert h.c.get_assessment(1)["decisions"] == [case["expected"]] * 3
    assert case["basis"]


@pytest.mark.parametrize("injection", INJECTIONS)
def test_injection_still_requires_independent_validator_comparison(h, contract_module, injection):
    ids = [h.create(0, offer=injection), h.create(1), h.create(2)]
    prompt = contract_module._assessment_prompt(h.c._prepare_cycle(ids, [1] * 3, [[1, 2], [2, 3], [3, 1]])[1])
    before = h.storage()
    h.vm.mock_llm("semantic compatibility classifier", '{"decisions":["FIT","FIT","FIT"]}')
    assert contract_module._consensus_decisions(prompt) == ["FIT"] * 3
    h.vm.clear_mocks()
    h.vm.mock_llm("semantic compatibility classifier", '{"decisions":["FIT","UNSURE","FIT"]}')
    assert h.vm.run_validator() is False
    assert h.storage() == before
