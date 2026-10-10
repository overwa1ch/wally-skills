#!/usr/bin/env python3
"""Print UTF-8 source files as one JavaScript data declaration for CUA."""
import argparse
import hashlib
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", nargs="+", required=True, type=Path)
    args = parser.parse_args()
    sources = []
    for source in args.source:
        path = source.resolve(strict=True)
        raw = path.read_bytes()
        # Decode bytes directly: preserve CRLF, whitespace, BOM and Unicode.
        sources.append({"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "text": raw.decode("utf-8")})
    # Keep Chinese readable; escape JS line separators without changing values.
    literal = json.dumps(sources, ensure_ascii=False).replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    declaration = f"var staticSources = Object.freeze({literal}.map(Object.freeze));\n"
    sys.stdout.buffer.write(declaration.encode("utf-8"))


if __name__ == "__main__":
    main()
