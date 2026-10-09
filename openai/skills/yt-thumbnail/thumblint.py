#!/usr/bin/env python3
"""thumblint.py - lint a thumbnail CONCEPT before you spend an hour designing it.

You describe the thumbnail in one line - what is in it - and this checks it against the rules that
decide whether it reads at feed size (about 210x118 px on a phone). It lints the plan, not a pixel.

    python3 thumblint.py --concept "my shocked face, red arrow, phone showing 4 subs" --title "..."
    python3 thumblint.py concepts.txt --title "..."    # one concept per line, ranked
    python3 thumblint.py --concept "..." --json

Four things sink a thumbnail at feed size and this looks for all four:
  ELEMENTS    more than three distinct focal things and the eye bounces off. Three is the ceiling.
  TEXT        more than three words is unreadable on a phone. Zero is allowed; four is not.
  DUPLICATE   text that repeats the title wastes half the click surface - the one mistake that
              costs the most and is the easiest to miss, because you wrote them in separate tabs.
  SIGNAL      a face with an emotion, or a single clear subject, or contrast. A screenshot of a
              dashboard with no focal point is not a thumbnail, it is a slide.

WHAT THIS IS NOT. It cannot see colour, contrast or composition - it reads your description of them.
If you write "high contrast, one big face" it believes you. It catches the structural mistakes
(too many elements, too much text, title duplication); it cannot tell you the red actually pops.
"""
import argparse, json, os, re, sys

STOP = {"the", "a", "an", "of", "for", "to", "in", "on", "and", "or", "my", "with", "showing",
        "a", "big", "huge", "giant", "small", "red", "green", "blue", "yellow", "bright"}
FACE = re.compile(r"\b(face|me|myself|shocked|surprised|pointing|reaction|crying|laughing|angry|"
                  r"smiling|expression|eyes|looking)\b", re.I)
CONTRAST = re.compile(r"\b(arrow|circle|highlight|glow|outline|contrast|bold|vs|versus|before|after|"
                      r"split|x|cross|tick|check)\b", re.I)
# a rough count of focal objects: nouns separated by commas / 'and' / 'with'
SPLIT = re.compile(r",|\band\b|\bwith\b|\bplus\b|\+", re.I)


def words(t):
    return re.findall(r"[a-z0-9']+", t.lower())


def quoted_text(concept):
    """pull the on-thumbnail text: anything in quotes, else nothing assumed."""
    q = re.findall(r'"([^"]+)"|“([^”]+)”', concept)
    return [a or b for a, b in q]


def check(concept, title=None):
    c = concept.strip()
    issues, good = [], []

    elements = [p.strip() for p in SPLIT.split(c) if p.strip()]
    n_el = len(elements)
    if n_el > 3:
        issues.append(("elements", f"{n_el} focal things - three is the ceiling before the eye bounces"))
    else:
        good.append(f"{n_el} focal element{'s' if n_el != 1 else ''}, reads at feed size")

    texts = quoted_text(c)
    thumb_words = [w for t in texts for w in words(t)]
    if len(thumb_words) > 3:
        issues.append(("text", f'{len(thumb_words)} words of text ("{" ".join(thumb_words)}") - '
                               "three is the ceiling on a phone"))
    elif texts:
        good.append(f"{len(thumb_words)}-word text overlay, readable")
    else:
        good.append("no text overlay quoted - fine if the image carries it")

    if FACE.search(c):
        good.append("a face or expression to anchor the eye")
    elif not CONTRAST.search(c):
        issues.append(("signal", "no face, no arrow, no contrast cue - name the one thing the eye lands on"))
    if CONTRAST.search(c):
        good.append("a contrast cue (arrow / circle / before-after)")

    if title and thumb_words:
        tw = set(words(title)) - STOP
        hw = set(thumb_words) - STOP
        shared = tw & hw
        if shared:
            issues.append(("duplicate", f"thumbnail text repeats the title on {', '.join(sorted(shared))} - "
                                        "say what the title does not"))
        else:
            good.append("thumbnail text and title carry different words")

    score = max(0, min(100, 100 - 16 * len(issues) + 4 * len(good)))
    return {"concept": c, "elements": n_el, "score": score, "issues": issues, "good": good}


def show(r):
    print(f'\n  {r["concept"]}')
    print(f"  {r['elements']} elements   score {r['score']}/100")
    for k, m in r["issues"]:
        print(f"    x  {k:<10} {m}")
    for m in r["good"]:
        print(f"    ok            {m}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?")
    parser.add_argument("--concept")
    parser.add_argument("--title")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    as_json, title = args.json, args.title
    if (args.file is None) == (args.concept is None):
        parser.error("provide a text file or --concept, not both")
    try:
        lines = [args.concept] if args.concept is not None else open(args.file, encoding="utf-8").read().splitlines()
    except OSError as exc:
        parser.error(str(exc))
    rows = [check(line, title) for line in lines if line.strip()]
    if not rows:
        parser.error("provide at least one nonempty concept")
    rows.sort(key=lambda r: -r["score"])
    if as_json:
        print(json.dumps(rows, indent=1))
        return
    for r in rows:
        show(r)
    print()


if __name__ == "__main__":
    main()
