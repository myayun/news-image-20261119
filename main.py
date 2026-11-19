#!/usr/bin/env python3
"""news-image-20261119 entrypoint.

Writes one image to /output/entry.png by copying the bundled
front-page image. Deterministic, offline, stdlib only.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "entry.png")
OUT_DIR = "/output"
OUT = os.path.join(OUT_DIR, "entry.png")


def main() -> int:
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)
    with open(OUT, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"wrote {OUT} sha256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
