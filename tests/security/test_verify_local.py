import importlib.util
import json
from pathlib import Path
import subprocess

import pytest

spec = importlib.util.spec_from_file_location("sca3_verify_local", Path("scripts/verify_local.py"))
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


def approved_schema():
    return {
        "ok": True,
        "schema": {
            "methods": {name: {"readonly": name in verify.VIEWS} for name in verify.WRITES | verify.VIEWS}
        },
    }


def test_schema_accepts_exact_approved_surface():
    result = approved_schema()
    assert verify.validate_schema(json.dumps(result)) == result


@pytest.mark.parametrize("name", sorted(verify.WRITES | verify.VIEWS))
def test_schema_rejects_missing_public_method(name):
    result = approved_schema()
    del result["schema"]["methods"][name]
    with pytest.raises(ValueError):
        verify.validate_schema(json.dumps(result))


@pytest.mark.parametrize(
    "name", ["_reserve_accepted_cycle", "assess_cycle", "inject_ai_verdict", "extra_view"]
)
def test_schema_rejects_extra_public_method(name):
    result = approved_schema()
    result["schema"]["methods"][name] = {"readonly": False}
    with pytest.raises(ValueError):
        verify.validate_schema(json.dumps(result))


@pytest.mark.parametrize("name", sorted(verify.WRITES | verify.VIEWS))
def test_schema_rejects_wrong_readonly_classification(name):
    result = approved_schema()
    result["schema"]["methods"][name]["readonly"] = name not in verify.VIEWS
    with pytest.raises(ValueError):
        verify.validate_schema(json.dumps(result))


@pytest.mark.parametrize("value", [None, 0, 1, "false"])
def test_schema_rejects_nonboolean_readonly(value):
    result = approved_schema()
    result["schema"]["methods"]["create_intent"]["readonly"] = value
    with pytest.raises(ValueError):
        verify.validate_schema(json.dumps(result))


@pytest.mark.parametrize("output", ["{", "[]", "null", "{}", '{"ok": false}', '{"ok": true}', '{"ok": 1}'])
def test_schema_rejects_malformed_or_unsuccessful_output(output):
    with pytest.raises(ValueError):
        verify.validate_schema(output)


def test_schema_command_failure_propagates(monkeypatch):
    def failed(*args, **kwargs):
        raise subprocess.CalledProcessError(1, args[0])

    monkeypatch.setattr(verify.subprocess, "run", failed)
    with pytest.raises(subprocess.CalledProcessError):
        verify.verify_schema("genvm-lint", {})


@pytest.mark.parametrize("output", ["{", '{"ok": false}', '{"ok": true, "schema": {"methods": {}}}'])
def test_verification_main_rejects_zero_exit_invalid_schema(monkeypatch, output):
    commands = []

    def fake_run(command, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, stdout=output)

    monkeypatch.setattr(verify.subprocess, "run", fake_run)
    with pytest.raises(ValueError):
        verify.main()
    assert commands[-1][1:] == ["schema", "contracts/semantic_cycle_accord.py", "--json"]
