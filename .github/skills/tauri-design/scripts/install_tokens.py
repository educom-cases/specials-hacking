#!/usr/bin/env python3
"""Install or verify the mandatory Tauri React design-token file."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


DESTINATION = Path("src/resources/design/tokens.json")
SOURCE = Path(__file__).resolve().parents[1] / "assets" / "tokens.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Tauri application root; defaults to the current directory",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify exact token bytes without writing",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace a different existing token file",
    )
    args = parser.parse_args()

    source_bytes = SOURCE.read_bytes()
    json.loads(source_bytes)

    destination = args.project_root.resolve() / DESTINATION
    if args.check:
        if not destination.is_file():
            print(f"error: mandatory token file is missing: {destination}", file=sys.stderr)
            return 1
        if destination.read_bytes() != source_bytes:
            print(f"error: mandatory token file differs: {destination}", file=sys.stderr)
            return 1
        print(f"Verified mandatory tokens: {destination}")
        return 0

    if destination.exists() and destination.read_bytes() != source_bytes and not args.force:
        print(
            f"error: token file differs; inspect it and rerun with --force: {destination}",
            file=sys.stderr,
        )
        return 1

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, destination)
    print(f"Installed mandatory tokens: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
