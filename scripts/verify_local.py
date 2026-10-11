"""Reproduce offline checks without pytest's network-capable plugin autoload."""

import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    env = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", GENVM_VERSION="v0.2.16")
    commands = [
        [sys.executable, "-m", "pytest", "-q"],
        [sys.executable, "-m", "ruff", "check", "contracts", "tests", "scripts"],
        [sys.executable, "-m", "ruff", "format", "--check", "contracts", "tests", "scripts"],
        [
            str(Path(sys.executable).parent / ("genvm-lint.exe" if os.name == "nt" else "genvm-lint")),
            "check",
            "contracts/semantic_cycle_accord.py",
            "--json",
        ],
    ]
    for command in commands:
        subprocess.run(command, cwd=ROOT, env=env, check=True)


if __name__ == "__main__":
    main()
