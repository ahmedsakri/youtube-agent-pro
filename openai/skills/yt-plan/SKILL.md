---
name: yt-plan
description: >-
  Plan a week or a month of YouTube uploads - what to post, when, and in
  what order, sized to the creator's actual capacity. Use for "plan my
  week", "content calendar", "what should I post", "I have no idea what to
  make next".
---

# yt-plan

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

Build around the user's requested cadence, format, timezone, available hours, and material already
made. Use known context; ask only for missing constraints that change the plan.

## Before you write

1. Use the creator's supplied voice profile or context, then a workspace `.youtube-agent/voice.md`
   if available, following the operating guide. If absent, draft in a clear voice using the stated
   audience and format; do not make voice-profile setup a prerequisite.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## Size the plan to the creator

For a mixed-format channel, an anchor video, a lower-effort follow-up, and selected Shorts from
existing footage can be a useful starting mix. Use [$yt-shorts](../yt-shorts/SKILL.md) for clip
plans. For a Shorts-only channel, plan standalone Shorts without requiring a long-form anchor.
Honor a requested daily or other cadence when capacity supports it; if it does not, name the
tradeoff instead of silently changing the user's schedule.

Use the channel's own audience and performance evidence for timing. If none is available, label a
proposed time as a test, not a universal best time. Keep dates and timezones explicit. This is a
calendar draft unless the user separately requests scheduling through an available account tool.

## What to hand back

A table: day, format, working title, the one sentence it promises, and what already exists for it.
Then the honest line at the bottom - how many hours this costs, and what to drop first if the week
goes wrong.
