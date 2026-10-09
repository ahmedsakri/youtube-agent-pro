#!/usr/bin/env python3
"""Compatibility entry point for the maintained PDF guide builder.

The interactive phone-card design now lives in docs/build_guides.py, which
renders one guide per edition (Claude, OpenAI) and refreshes the legacy alias.
Rebuilding the PDFs needs Google Chrome; the runtime skills do not.
"""
import sys

from build_guides import main

if __name__ == "__main__":
    print("docs/build_guide.py is a thin alias; running docs/build_guides.py.", file=sys.stderr)
    main()
