#!/usr/bin/env python3
"""retention.py - find candidate drop-offs in an audience-retention CSV.

    python3 retention.py retention.csv --axis seconds --json
    python3 retention.py retention.csv --axis percent --duration 180 --transcript transcript.srt

The first two columns must be position and retention percentage. --axis auto
recognizes explicit seconds, percentage or elapsedVideoTimeRatio headers; it never
infers units from the largest value. Unitless CSVs need --axis. Ratio-style API
headers (elapsedVideoTimeRatio and audienceWatchRatio) are also recognized.
Retention can exceed 100% because of replays. Drops are observations, not proof
of why viewers left. The default opening window is the first 10% capped at 30s
when duration is known. Use --hook-seconds to inspect a specific opening window.
"""
import argparse
import csv
import json
import math
import os
import re
import sys


def load_csv(path, axis="auto"):
    rows, header = [], []
    with open(path, newline="", encoding="utf-8-sig") as handle:
        for line, row in enumerate(csv.reader(handle), 1):
            if not row or all(not cell.strip() for cell in row):
                continue
            if len(row) < 2:
                raise ValueError(f"CSV row {line}: two columns are required")
            try:
                x, y = [float(cell.strip().replace("%", "").replace(",", "")) for cell in row[:2]]
            except ValueError:
                if not rows and not header:
                    header = row
                    continue
                raise ValueError(f"CSV row {line}: position and retention must be numeric")
            if not all(math.isfinite(v) and v >= 0 for v in (x, y)):
                raise ValueError(f"CSV row {line}: values must be finite and nonnegative")
            rows.append((x, y))
    first = header[0].strip().lower() if header else ""
    second = header[1].strip().lower() if header else ""
    if axis == "auto":
        if "elapsedvideotimeratio" in first or "fraction" in first or "ratio" in first:
            axis = "fraction"
        elif "%" in first or "percent" in first:
            axis = "percent"
        elif "second" in first or re.search(r"\(s\)|\bs\b", first):
            axis = "seconds"
        else:
            raise ValueError("ambiguous position units; supply --axis seconds, percent or fraction")
    if axis == "fraction":
        if any(x > 1 for x, _ in rows):
            raise ValueError("fraction positions must be between 0 and 1")
        rows = [(x * 100, y) for x, y in rows]
        axis = "percent"
    if "audiencewatchratio" in second or "fraction" in second or "ratio" in second:
        rows = [(x, y * 100) for x, y in rows]
    if axis == "percent" and any(x > 100 for x, _ in rows):
        raise ValueError("percent positions must be between 0 and 100")
    rows.sort()
    if any(rows[i][0] == rows[i - 1][0] for i in range(1, len(rows))):
        raise ValueError("duplicate positions cannot define a retention slope")
    return rows, axis


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv")
    parser.add_argument("--axis", choices=("auto", "seconds", "percent", "fraction"), default="auto")
    parser.add_argument("--duration", type=float)
    parser.add_argument("--hook-seconds", type=float)
    parser.add_argument("--transcript")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    for name in ("duration", "hook_seconds"):
        value = getattr(args, name)
        if value is not None and (not math.isfinite(value) or value <= 0):
            parser.error("--" + name.replace("_", "-") + " must be finite and positive")
    try:
        rows, axis = load_csv(args.csv, args.axis)
        if len(rows) < 8:
            parser.error("could not read at least 8 data points from that CSV")
        xs, ys = zip(*rows)
        pct_axis = axis == "percent"
        duration = args.duration if args.duration is not None else (None if pct_axis else xs[-1])
        if duration is not None and not pct_axis and xs[-1] > duration:
            parser.error("position exceeds --duration")
        if args.hook_seconds is not None and pct_axis and duration is None:
            parser.error("--hook-seconds with percentage positions requires --duration")
        window = args.hook_seconds if args.hook_seconds is not None else (min(30.0, duration * 0.1) if duration else None)
        cutoff = min(100, window / duration * 100) if pct_axis and duration else (10.0 if pct_axis else window)
        start = ys[0]
        hook_end = min((y for x, y in rows if x <= cutoff), default=start)
        drops = [( (ys[i-1] - ys[i]) / (xs[i] - xs[i-1]), xs[i-1], xs[i], ys[i-1] - ys[i]) for i in range(1, len(rows))]
        cliffs = [{"from": round(a, 2), "to": round(b, 2), "lost": round(drop, 2),
                   "at_seconds": round(a / 100 * duration if pct_axis else a, 1) if duration is not None else None}
                  for _, a, b, drop in sorted(drops, reverse=True)[:5] if drop > 0.8]
        middle = [(drop, b-a) for _, a, b, drop in drops if a >= cutoff]
        slide = sum(drop for drop, _ in middle) / sum(span for _, span in middle) if middle else 0
        said = {}
        if args.transcript:
            sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "yt-edit"))
            from deadair import load
            cues = load(args.transcript)
            for cliff in cliffs:
                time = cliff["at_seconds"]
                if time is not None:
                    said[str(cliff["from"])] = " ".join(c[2] for c in cues if c[0] <= time + 4 and c[1] >= time - 4)[:140]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    out = {"points": len(rows), "axis": axis, "retention_unit": "percentage_points",
           "start": start, "hook_leak": round(start - hook_end, 2), "hook_window": cutoff,
           "hook_window_seconds": window, "end": ys[-1], "cliffs": cliffs,
           "slide_per_unit": round(slide, 3), "said": said,
           "warning": "Descriptive drop-offs, not causal findings; compare similar formats and traffic sources."}
    if args.json:
        print(json.dumps(out, indent=1, allow_nan=False))
        return
    print(f"\n{args.csv}: {len(rows)} points, {ys[0]:.1f}% -> {ys[-1]:.1f}%")
    print(f"  OPENING: {out['hook_leak']:.1f} percentage points lost over {cutoff:g} {axis}")
    for cliff in cliffs:
        where = f"{cliff['at_seconds']:g}s" if cliff["at_seconds"] is not None else f"{cliff['from']}%"
        print(f"  DROP: {cliff['lost']:.1f} points at {where} {said.get(str(cliff['from']), '')}")
    print(f"  MIDDLE: {slide:.3f} percentage points per {axis} unit")
    print("  " + out["warning"])


if __name__ == "__main__":
    main()
