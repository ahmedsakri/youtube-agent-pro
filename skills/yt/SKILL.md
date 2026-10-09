---
name: yt
description: >-
  The hub for the YouTube agent. Routes a vague request to the right
  skill and runs a whole video end to end - idea, script, package,
  thumbnail, SEO, chapters, then the after-publish loop. Use for "help
  me with my channel", "make my next video", "where do I start", or any
  YouTube request where the specific skill is not obvious yet.
---

# yt

The front door. Use this when the user does not know which skill they need, or wants the whole thing
done in order rather than one piece.

## First, always

Read `~/.claude/youtube/voice.md`. If it is missing, stop and run **/yt-voice** before anything
else - every other skill is worse without it. One file, read by all of them.

## Route the request

Match the ask to the skill. Do not do the work here; hand off.

| the user says | run |
| --- | --- |
| "what should I make", "I have no idea" | **/yt-idea** |
| "write the script", "what do I say" | **/yt-script** |
| "title", "what do I call it", "my CTR is bad" | **/yt-package** |
| "thumbnail", "design the thumbnail" | **/yt-thumbnail** |
| "description", "tags", "nobody finds it" | **/yt-seo** |
| "chapters", "timestamps" | **/yt-chapters** |
| "why do people stop watching" | **/yt-retention** |
| "my numbers", "which video worked", a Studio export | **/yt-analytics** |
| "cut this into shorts", "clip this" | **/yt-shorts** |
| "turn this into a thread / newsletter / post" | **/yt-repurpose** |
| "edit this", "I rambled" | **/yt-edit** |
| "reply to comments" | **/yt-comment** |
| "plan my week / month" | **/yt-plan** |
| "a series", "a playlist" | **/yt-series** |
| "what's working in my niche" | **/yt-viral** |
| "sponsorship", "rate card", "a brand emailed me" | **/yt-sponsor** |
| "find a collab" | **/yt-collab** |
| "my channel page", "subscribers aren't converting" | **/yt-funnel** |
| "what to post this season", "trending" | **/yt-trend** |
| "shot list", "production brief", "how do I film this" | **/yt-brief** |
| "end screen", "cards", "what plays next" | **/yt-endscreen** |
| "review my whole channel" | **/yt-audit** |

## The full run

When the user wants a whole video from nothing, go in this order and stop at each gate:

1. **/yt-idea** - pick one, scored.
2. **/yt-brief** - turn it into a shot list before a word is written.
3. **/yt-script** - hook panel, then the spoken script.
4. **/yt-package** + **/yt-thumbnail** - the click surface, linted as one pairing.
5. **/yt-seo** + **/yt-chapters** - the found-in-search surface.
6. After it is up: **/yt-retention** and **/yt-analytics** to find the one fix for next time.

## The gate

Nothing in this pack publishes. Every skill ends in a block the user copies and the same question:
**ship it, or change it?** The hub does not change that - it just gets them to the right gate faster.
