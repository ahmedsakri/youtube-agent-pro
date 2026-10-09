#!/usr/bin/env python3
"""Compatibility entry point for the maintained two-edition PDF builder.

The original 16-page HTML design is preserved in Git at commit
3f08946ed3c03f127c32a4549b09936d0c7d17fc; see guides/README.md for links.
This entry point now emits current PDFs directly and does not write guide.html.
ReportLab is required only for rebuilding documentation.
"""

import sys

from build_guides import main


if __name__ == "__main__":
    print("docs/build_guide.py is deprecated; use docs/build_guides.py. "
          "Building current PDF guides directly.", file=sys.stderr)
    main()
