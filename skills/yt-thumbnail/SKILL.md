---
name: yt-thumbnail
description: >-
  Design the thumbnail as a concept before you open an editor - the one
  focal idea, three elements at most, three words at most, and nothing
  that repeats the title. Lints the plan and writes A/B variants. Use for
  "thumbnail idea", "design my thumbnail", "my CTR is low", "what should
  the thumbnail be", or thumbnail A/B testing.
---

# yt-thumbnail

The thumbnail is half the click surface and it is the half most people design last, tired, in the
wrong tool. This designs it first, as a concept, and lints it before any pixels exist.

A tool lives here and it runs. Describe the concept in words; it checks the structure.

```bash
python3 thumblint.py --concept "my shocked face, red arrow, phone showing \"4 SUBS\"" --title "..."
python3 thumblint.py concepts.txt --title "..."    # rank several concepts
```

## Before you design

1. Read `~/.claude/youtube/voice.md` and, more importantly, the title - the thumbnail is linted
   *against the title*. The single most expensive mistake is the thumbnail repeating the title's
   words, because it wastes half the surface saying one thing twice. This skill refuses that.
2. Design for feed size, about 210x118 px on a phone. If it does not read at a thumbnail of a
   thumbnail, it does not read.

## The rules this enforces

- **One focal idea.** The viewer decides in well under a second. Three elements is the ceiling.
- **Three words, maximum.** Zero is allowed. Four is not readable on a phone.
- **A signal.** A face with a real expression, or one unmistakable subject, or a contrast cue
  (arrow, circle, before/after). A screenshot with no focal point is a slide, not a thumbnail.
- **Complement, do not echo.** The thumbnail says what the title does not. Title carries the
  specifics; thumbnail carries the emotion or the artifact.

## The move

1. Write **three distinct concepts** - not three colours of one idea. One face-led, one
   artifact-led (show the thing), one contrast-led (before/after, vs).
2. Run all three through `thumblint.py` with the title.
3. Keep the top two and hand them over as an A/B pair - YouTube lets you test thumbnails now, so
   give the user two that are genuinely different, not two fonts.

## What to hand back

- two linted concepts, described tightly enough to hand to a designer or build in Canva
- for each: the focal element, the 0-3 words of overlay, the emotion it is going for
- one line: which to lead with, and what the A/B is actually testing

## The gate

This designs and lints; it does not render an image and it does not publish. The last line is the
question: **which of the two do you want to build first?**
