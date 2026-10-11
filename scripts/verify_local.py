"""Reproduce offline checks without pytest's network-capable plugin autoload."""

import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
WRITES = frozenset(
    {
        "create_intent",
        "update_intent",
        "cancel_intent",
        "confirm_cycle",
        "decline_cycle",
        "expire_cycle",
        "assess_cycle",
    }
)
VIEWS = frozenset(
    {
        "get_assessment",
        "get_intent",
        "get_cycle",
        "get_intents_page",
        "get_cycles_page",
        "get_owner_records",
        "get_protocol_stats",
    }
)


def validate_schema(output: str) -> dict:
    result = json.loads(output)
    if not isinstance(result, dict) or result.get("ok") is not True:
        raise ValueError("Schema generation did not report success")
    schema = result.get("schema")
    methods = schema.get("methods") if isinstance(schema, dict) else None
    if not isinstance(methods, dict) or set(methods) != WRITES | VIEWS:
        raise ValueError("Schema must export exactly the approved 14 public methods")
    for name, method in methods.items():
        if not isinstance(method, dict) or method.get("readonly") is not (name in VIEWS):
            raise ValueError(f"Incorrect readonly classification: {name}")
    return result


def verify_schema(linter: str, env: dict) -> dict:
    completed = subprocess.run(
        [linter, "schema", "contracts/semantic_cycle_accord.py", "--json"],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    result = validate_schema(completed.stdout)
    print("Schema verification PASS: exactly 14 public methods, 7 writes / 7 views")
    return result


def main():
    env = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", GENVM_VERSION="v0.2.16")
    linter = str(Path(sys.executable).parent / ("genvm-lint.exe" if os.name == "nt" else "genvm-lint"))
    commands = [
        [sys.executable, "-m", "pytest", "-q"],
        [sys.executable, "-m", "ruff", "check", "contracts", "tests", "scripts"],
        [sys.executable, "-m", "ruff", "format", "--check", "contracts", "tests", "scripts"],
        [
            linter,
            "check",
            "contracts/semantic_cycle_accord.py",
            "--json",
        ],
    ]
    for command in commands:
        subprocess.run(command, cwd=ROOT, env=env, check=True)
    verify_schema(linter, env)


if __name__ == "__main__":
    main()
