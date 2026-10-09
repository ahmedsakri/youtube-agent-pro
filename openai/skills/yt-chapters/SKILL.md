---
name: yt-chapters
description: >-
  Draft YouTube chapters from a timestamped transcript and check basic
  timestamp constraints before the creator uses them. Use for "add chapters", "timestamps",
  "break this video into sections".
---

# yt-chapters

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

```bash
python3 "$YT_SKILL_DIR/chapters.py" transcript.srt --target 8
```

## Basic chapter checks

The helper checks these common YouTube chapter constraints. Verify current platform guidance and
video eligibility when troubleshooting display; passing these checks alone does not guarantee
chapters will render:

- The first entry must be **00:00**.
- There must be **at least three**.
- Each must be **at least 10 seconds** long.

The tool checks these constraints. Verify the final chapter against the actual video end too.

## Retitle every line

`chapters.py` finds the BOUNDARIES well - it scores the pauses you actually took by how much the
vocabulary shifts across them. The titles it emits are the topic words, and they are a draft. A
chapter called "Thumbnails Titles Packaging" is a placeholder. Rewrite each one as the promise of
that section, in the user's voice, three to five words.

Chapters are also a retention diagnostic: if a section cannot be named in five words, it is two
sections or it is filler.
