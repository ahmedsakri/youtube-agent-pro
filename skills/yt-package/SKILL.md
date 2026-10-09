---
name: yt-package
description: >-
  Write and lint the title and thumbnail for a YouTube video as one pairing,
  checking truncation, duplication and vagueness before publish. Use for
  "title ideas", "what should I call this", "thumbnail text", "my CTR is
  bad", packaging, or any request to rename or repackage an existing video.
---

# yt-package

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

The title and the thumbnail are ONE unit. Writing them separately is why most packaging fails: the
thumbnail repeats the title, and half the click surface says the same thing twice.

```bash
python3 "$YT_SKILL_DIR/title.py" --title "..." --thumb "AI RAN IT"
python3 "$YT_SKILL_DIR/title.py" titles.txt            # one per line, ranked
```

## Before you write

1. Use the creator's supplied voice profile or context, then a local `~/.claude/youtube/voice.md`
   if available, following the operating guide. If absent, draft in a clear voice using the stated
   audience and format; do not make voice-profile setup a prerequisite.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## Rules the tool enforces, and why

- **60 and 40 characters** are the helper's conservative truncation checks, not fixed YouTube
  limits. Display varies by surface and device; keep the subject early and preview when possible.
- **The thumbnail must not repeat the title.** Different words, same promise.
- **Aim for 0–3 thumbnail words.** Treat this as a readability heuristic, not a platform rule.
- **A number, a name or a date** beats every adjective available to you.
- **Two all-caps words is the ceiling** before a title reads as spam.

## Write ten, keep two

Generate ten titles, run them all through `title.py`, show the user the top three with their scores
and the specific issue on each. For the winner, write the thumbnail brief: the expression, the
framing, the three words, and what the background has to do to hold contrast at feed size.
