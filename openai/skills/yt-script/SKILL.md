---
name: yt-script
description: >-
  Write a YouTube video script from a raw idea - hook options off 21
  formulas, scored, then the full spoken script with the retention beats
  marked. Use whenever the user wants a video script, a hook, an opening
  line, "what should I say", "write my next video", or is about to record
  and does not have the first fifteen seconds yet.
---

# yt-script

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

One idea into a script somebody finishes.

`hookscore.py` scores candidate hooks against the accompanying formula library. Use it when
execution is available; its scores are writing heuristics, not predictions of viewer retention.

```bash
python3 "$YT_SKILL_DIR/hookscore.py" hooks.txt              # rank your hook options
python3 "$YT_SKILL_DIR/hookscore.py" --hook "one line"      # score a single one
```

## Before you write

1. Use the creator's supplied voice profile or context, then a workspace `.youtube-agent/voice.md`
   if available, following the operating guide. If absent, draft in a clear voice using the stated
   audience and format; do not make voice-profile setup a prerequisite.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## The shape

**The opening must earn attention.** Confirm the title's promise, open a meaningful question,
and show a reason to expect the payoff. The times below suit a longer video; for Shorts, establish
context in the first seconds and scale every beat to the requested runtime.

1. **Hook.** Write FIVE against [the 21 formulas](hooks.json), run them through `hookscore.py`,
   keep the strongest options, and report actual scores if run. If the user requests one final hook,
   select it and continue into the full script.
2. **The turn** (0:15-0:45). Say what the video is going to do, in one sentence, and start doing it.
   Keep setup brief and avoid delaying the promised content with an unrelated intro or subscribe pitch.
3. **The body.** One idea per beat. Mark each beat with what is ON SCREEN, not just what is said -
   a talking head with nothing to look at is a podcast.
4. **The payoff.** Deliver the thing the hook promised, explicitly, and say that you are delivering
   it: "that is the prompt, it is in the description".
5. **The close.** One ask. Not three.

## What to hand back

- the two best hooks with their scored panels
- the script, beat by beat, with `[ON SCREEN: ...]` on every beat
- a runtime estimate from the spoken words (150 words/minute is a starting assumption), with
  pauses, visual beats, and the creator's actual delivery speed accounted for
- one line naming which formula the winning hook used and why it fits this idea
