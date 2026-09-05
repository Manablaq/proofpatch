#!/usr/bin/env python3
from pathlib import Path
import argparse
import hashlib


def main() -> int:
    parser = argparse.ArgumentParser(description="Print exact SHA-256 for a source file.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    data = args.path.read_bytes()
    print(hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
