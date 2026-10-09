---
name: yt
description: >-
  The hub for the YouTube agent. Routes a vague request to the right
  skill and develops a video production package - idea, script, package,
  thumbnail, SEO, chapters, then the after-publish loop. Use for "help
  me with my channel", "make my next video", "where do I start", or any
  YouTube request where the specific skill is not obvious yet.
---

# yt

Read the [shared operating guide](references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

The front door. Use this when the user does not know which skill they need, or wants the whole thing
done in order rather than one piece.

## Start from the request

Use the available channel, voice, audience, and format context. A profile is optional; read the
operating guide for lookup order. If the user wants profile setup, use [/youtube-agent-pro:yt-voice](../yt-voice/SKILL.md).
Otherwise continue with the task rather than requiring setup first.

## Route the request

Match the ask to the skill below, read its linked instructions, and perform that workflow.
These are local skill files, not tools or executable slash-commands.

| the user says | run |
| --- | --- |
| "what should I make", "I have no idea" | [/youtube-agent-pro:yt-idea](../yt-idea/SKILL.md) |
| "write the script", "what do I say" | [/youtube-agent-pro:yt-script](../yt-script/SKILL.md) |
| "title", "what do I call it", "my CTR is bad" | [/youtube-agent-pro:yt-package](../yt-package/SKILL.md) |
| "thumbnail", "design the thumbnail" | [/youtube-agent-pro:yt-thumbnail](../yt-thumbnail/SKILL.md) |
| "description", "tags", "nobody finds it" | [/youtube-agent-pro:yt-seo](../yt-seo/SKILL.md) |
| "chapters", "timestamps" | [/youtube-agent-pro:yt-chapters](../yt-chapters/SKILL.md) |
| "why do people stop watching" | [/youtube-agent-pro:yt-retention](../yt-retention/SKILL.md) |
| "my numbers", "which video worked", a Studio export | [/youtube-agent-pro:yt-analytics](../yt-analytics/SKILL.md) |
| "cut this into shorts", "clip this" | [/youtube-agent-pro:yt-shorts](../yt-shorts/SKILL.md) |
| "turn this into a thread / newsletter / post" | [/youtube-agent-pro:yt-repurpose](../yt-repurpose/SKILL.md) |
| "edit this", "I rambled" | [/youtube-agent-pro:yt-edit](../yt-edit/SKILL.md) |
| "reply to comments" | [/youtube-agent-pro:yt-comment](../yt-comment/SKILL.md) |
| "plan my week / month" | [/youtube-agent-pro:yt-plan](../yt-plan/SKILL.md) |
| "a series", "a playlist" | [/youtube-agent-pro:yt-series](../yt-series/SKILL.md) |
| "what's working in my niche" | [/youtube-agent-pro:yt-viral](../yt-viral/SKILL.md) |
| "sponsorship", "rate card", "a brand emailed me" | [/youtube-agent-pro:yt-sponsor](../yt-sponsor/SKILL.md) |
| "find a collab" | [/youtube-agent-pro:yt-collab](../yt-collab/SKILL.md) |
| "my channel page", "subscribers aren't converting" | [/youtube-agent-pro:yt-funnel](../yt-funnel/SKILL.md) |
| "what to post this season", "trending" | [/youtube-agent-pro:yt-trend](../yt-trend/SKILL.md) |
| "shot list", "production brief", "how do I film this" | [/youtube-agent-pro:yt-brief](../yt-brief/SKILL.md) |
| "end screen", "cards", "what plays next" | [/youtube-agent-pro:yt-endscreen](../yt-endscreen/SKILL.md) |
| "review my whole channel" | [/youtube-agent-pro:yt-audit](../yt-audit/SKILL.md) |

## The full run

When the user wants a whole production package, use this order and continue through the authorized
stages. Respect any explicit review point; ask only when a missing choice prevents useful progress.

1. [/youtube-agent-pro:yt-idea](../yt-idea/SKILL.md) - pick one, scored.
2. [/youtube-agent-pro:yt-script](../yt-script/SKILL.md) - hook options, then the spoken script.
3. [/youtube-agent-pro:yt-brief](../yt-brief/SKILL.md) - translate the script into a shot list and production plan.
4. [/youtube-agent-pro:yt-package](../yt-package/SKILL.md) + [/youtube-agent-pro:yt-thumbnail](../yt-thumbnail/SKILL.md) - the click surface, linted as one pairing.
5. [/youtube-agent-pro:yt-seo](../yt-seo/SKILL.md) + [/youtube-agent-pro:yt-chapters](../yt-chapters/SKILL.md) - the found-in-search surface.
6. After it is up: [/youtube-agent-pro:yt-retention](../yt-retention/SKILL.md) and [/youtube-agent-pro:yt-analytics](../yt-analytics/SKILL.md) to find the one fix for next time.


Deliver the requested drafts and files with any assumptions or unresolved inputs. Creating a
finished video requires separate recording, generation, or editing tools; this pack does not render
or upload it. For a Shorts-only channel, keep the workflow and analytics specific to Shorts.
