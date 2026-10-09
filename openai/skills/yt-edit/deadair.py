#!/usr/bin/env python3
"""deadair.py - an edit decision list from a timestamped transcript.

    python3 deadair.py transcript.srt            # or .vtt, or whisper .json
    python3 deadair.py transcript.srt --floor 0.35 --json

Finds three things and prints the cuts as a list you can act on, newest problem first:
  DEAD    gaps between spoken cues longer than the floor
  FILLER  cues that are only filler ("um", "so yeah", "basically")
  REPEAT  a sentence restarted - the second take of the same opening

WHAT IT DOES NOT DO. It does not cut the file. It prints an EDL, the total it would remove, and the
runtime you would land on, and you apply it in whatever editor you use. Nothing here touches media.
"""
import argparse, json, math, os, re, sys

FILLER_ONLY = re.compile(r"^[\s,.-]*((um+|uh+|er+|ah+|so|okay|ok|right|yeah|like|anyway|basically|"
                         r"actually|you know|i mean|let me see|hold on)[\s,.-]*)+$", re.I)

def parse_ts(s):
    s = s.strip().replace(",", ".")
    p = s.split(":")
    return int(p[0]) * 3600 + int(p[1]) * 60 + float(p[2]) if len(p) == 3 else int(p[0]) * 60 + float(p[1])

def load(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    if path.lower().endswith(".json"):
        d = json.loads(raw)
        if not isinstance(d, (list, dict)):
            raise ValueError("Whisper JSON must contain a segment list or an object with segments")
        segs = d if isinstance(d, list) else d.get("segments", [])
        if not isinstance(segs, list) or any(not isinstance(s, dict) for s in segs):
            raise ValueError("segments must be a list of objects with start, end and text")
        cues = [(float(s["start"]), float(s["end"]), (s.get("text") or "").strip()) for s in segs]
        return validate(cues)
    cues, cur = [], None
    for line in raw.splitlines():
        m = re.match(r"\s*(\d[\d:.,]+)\s*-->\s*(\d[\d:.,]+)", line)
        if m:
            cur = [parse_ts(m.group(1)), parse_ts(m.group(2)), []]
            cues.append(cur)
        elif not line.strip():
            cur = None
        elif cur is not None and not line.strip().isdigit():
            cur[2].append(line.strip())
    return validate([(a, b, " ".join(t)) for a, b, t in cues if t])

def validate(cues):
    if any(not math.isfinite(a) or not math.isfinite(b) or a < 0 or b <= a for a, b, _ in cues):
        raise ValueError("cue timestamps must be finite, nonnegative and end after start")
    return sorted(cues, key=lambda cue: (cue[0], cue[1]))

def union_seconds(cuts):
    """Overlapping suggestions remove a shared interval only once."""
    total, end = 0.0, 0.0
    for c in sorted(cuts, key=lambda c: c["start"]):
        total += max(0.0, c["end"] - max(end, c["start"]))
        end = max(end, c["end"])
    return total

def norm(t): return re.sub(r"[^a-z ]", "", t.lower()).split()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcript")
    parser.add_argument("--floor", type=float, default=0.45)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    floor, as_json = args.floor, args.json
    a = [args.transcript]
    if not math.isfinite(floor) or floor < 0:
        parser.error("--floor must be a finite nonnegative number")
    try:
        cues = load(a[0])
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    if not cues: parser.error("no cues found - use SRT, VTT or Whisper JSON")
    dur = max(c[1] for c in cues)
    cuts = []
    for i, (s, e, t) in enumerate(cues):
        if FILLER_ONLY.match(t):
            cuts.append({"kind": "FILLER", "start": s, "end": e, "why": t.strip()[:48]})
        if i:
            # Subtitle tracks can contain overlapping cues: silence only begins
            # after every earlier active cue has finished.
            previous_end = max(c[1] for c in cues[:i])
            gap = s - previous_end
            if gap > floor:
                keep = floor / 2
                cuts.append({"kind": "DEAD", "start": round(previous_end + keep, 3),
                             "end": round(s - keep, 3), "why": f"{gap:.2f}s gap"})
        # A restart is compared against the last cue that was actually SPEECH. Comparing against
        # the literal previous cue misses every retake with an "um" between the two attempts, which
        # is most of them.
        if t.strip() and not FILLER_ONLY.match(t):
            j = i - 1
            while j >= 0 and (FILLER_ONLY.match(cues[j][2]) or not cues[j][2].strip()): j -= 1
            if j >= 0:
                a1, b1 = norm(cues[j][2])[:5], norm(t)[:5]
                if len(a1) >= 3 and a1 == b1:
                    cuts.append({"kind": "REPEAT", "start": cues[j][0], "end": cues[j][1],
                                 "why": f'restart of "{" ".join(a1)}"'})
    cuts = [c for c in cuts if c["end"] > c["start"]]
    cuts.sort(key=lambda c: c["start"])
    removed = union_seconds(cuts)
    if as_json:
        print(json.dumps({"source": a[0], "duration": dur, "cuts": cuts,
                          "removed": round(removed, 3), "out": round(dur - removed, 3)}, indent=1)); return
    print(f"\n  {a[0]}   {dur:.2f}s in, {len(cues)} cues, dead-air floor {floor}s\n")
    for c in cuts:
        print(f"    {c['kind']:<7} {c['start']:8.2f} -> {c['end']:8.2f}   {c['end']-c['start']:5.2f}s   {c['why']}")
    print(f"\n  {len(cuts)} cuts, {removed:.2f}s removed, {dur - removed:.2f}s out "
          f"({removed / dur * 100:.1f}% shorter)\n")

if __name__ == "__main__":
    main()
