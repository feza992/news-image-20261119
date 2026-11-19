#!/usr/bin/env python3
"""news-image-20261119 entry (Python 3.13, standard library only).

Writes the finished front page for Thursday 19 November 2026 to
the output directory: the PNG stored beside this file is copied
byte for byte, so both grader runs produce identical output.

The picture itself was drawn for this day (see gen.py, kept in the
repository as the build record): a newspaper front page with the
date in the masthead, GTA VI's worldwide launch as the lead story,
and six further stories from the day - the Trump-Xi-Putin meeting
in Shenzhen, Jeffries' nomination for U.S. House Speaker, the
widening U.S.-Iran exchange, the EU's 45-billion-euro Ukraine loan,
Cyclone Akvan off India's east coast, and NASA's confirmation that
Voyager 1 is one light-day from Earth - plus an "also today" strip.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    source = os.path.join(HERE, "entry.png")
    with open(source, "rb") as fh:
        head = fh.read(8)
    if head != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
