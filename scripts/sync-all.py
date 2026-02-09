#!/usr/bin/env python3
"""
Sync navigation and footer across all public HTML pages.

Convenience wrapper around:
- scripts/sync-nav.py
- scripts/sync-footer.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    scripts_dir = Path(__file__).resolve().parent
    python = sys.executable

    commands = [
        [python, str(scripts_dir / "sync-nav.py")],
        [python, str(scripts_dir / "sync-footer.py")],
    ]

    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

