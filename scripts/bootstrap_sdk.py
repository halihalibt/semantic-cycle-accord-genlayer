"""Cache only the frozen official v0.2.16 tooling; never connects to a blockchain."""

import hashlib
from pathlib import Path
import shutil
import urllib.request

from gltest.direct.sdk_loader import CACHE_DIR, extract_runner, setup_sdk_paths

VERSION = "v0.2.16"
SHA256 = "4f0b358ec98ec148be9b95cdfb0f0e1a6cbe64da0194fdfac3fffc6f5d1d93e2"
URL = f"https://github.com/genlayerlabs/genvm/releases/download/{VERSION}/genvm-universal.tar.xz"


def main():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    target = CACHE_DIR / f"genvm-universal-{VERSION}.tar.xz"
    if not target.exists():
        temporary = target.with_suffix(".download")
        try:
            with urllib.request.urlopen(URL, timeout=60) as source, temporary.open("wb") as output:
                shutil.copyfileobj(source, output)
            if hashlib.sha256(temporary.read_bytes()).hexdigest() != SHA256:
                raise RuntimeError("Official artifact digest differs from the validated Phase 1 artifact")
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
    if hashlib.sha256(target.read_bytes()).hexdigest() != SHA256:
        raise RuntimeError("Pinned GenVM artifact checksum mismatch")
    setup_sdk_paths(version=VERSION)
    extract_runner(
        target, "py-lib-cloudpickle", "1dlk6mnfabi0z7r39635amyfzw8xb6rm8bv4pmgv6ji1bfx9hghd", VERSION
    )
    lint_cache = Path.home() / ".cache" / "genvm-linter"
    lint_cache.mkdir(parents=True, exist_ok=True)
    destination = lint_cache / target.name
    if not destination.exists():
        shutil.copyfile(target, destination)
    elif hashlib.sha256(destination.read_bytes()).hexdigest() != SHA256:
        raise RuntimeError("Linter artifact checksum mismatch")
    print(f"Validated {VERSION}; SDK and linter caches ready. SHA256={SHA256}")


if __name__ == "__main__":
    main()
