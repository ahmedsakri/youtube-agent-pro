---
name: yt-audit
description: >-
  Audit a YouTube channel end to end - packaging, consistency, the first
  fifteen seconds, and what to fix first. Use for "audit my channel", "why
  isn't my channel growing", "review my videos", or a pasted channel URL.
---

# yt-audit

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

An audit that lists twenty problems is a way of avoiding the one that matters. This ends in ONE fix.

## Before you write

1. Use the creator's supplied voice profile or context, then a local `~/.claude/youtube/voice.md`
   if available, following the operating guide. If absent, draft in a clear voice using the stated
   audience and format; do not make voice-profile setup a prerequisite.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## What to look at, in this order

1. **The last ten titles, as a set.** Read them as a list, the way the channel page shows them. Do
   they promise different things? Run them through `../yt-package/title.py`. A channel where every
   title is the same shape has a format problem, not a title problem.
2. **The thumbnails, at feed size.** Shrink them. What survives? If three of them are unreadable at
   that size, that is the fix and nothing else matters yet.
3. **The first fifteen seconds of the three most recent.** Transcribe them and score with
   `../yt-script/hookscore.py`. This is where most channels lose.
4. **Upload rhythm and capacity.** Compare formats, publication age, and performance before
   attributing a result to frequency. A sustainable cadence helps planning, but consistency alone
   does not establish how YouTube will distribute a video.
5. **The retention shape**, if they can export it. `/youtube-agent-pro:yt-retention`.

## What to hand back

- The single biggest fix, named, with what to do this week.
- Three things that are already working, so they do not break them. Be specific; "your energy is
  good" is not an observation.
- What NOT to do yet, and why.

Never open an audit with praise you do not mean, and never end one with a list of twenty things.
