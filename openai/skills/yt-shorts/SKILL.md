---
name: yt-shorts
description: >-
  Find the Shorts hiding inside a long video and write them, using the
  transcript to pick self-contained moments. Use for "cut this into shorts",
  "clip this", "repurpose this video", "what should I clip".
---

# yt-shorts

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

A Short cut out of a long video is not a clip of the best moment. It is a moment that **survives
without the video around it**, which is a much smaller set.

## Picking

Read the timestamped transcript and inspect footage when available. Select self-contained spans
for the requested duration (20–55 seconds is a useful starting range, not a platform limit). Verify
current Shorts eligibility if the requested length or aspect ratio depends on it. All three should be true:

1. It opens on a complete thought. If the first sentence needs the previous minute, it is not a Short.
2. There is a turn in it - a claim, then something that complicates or proves it.
3. It ends on a line, not a trail-off.

Rank the candidates and show the user the top five with their timecodes and first line, so they can
reject one without reading the whole transcript.

## Writing each one

- **A self-contained first line.** Prefer a usable existing line for a footage-only edit. If a new
  hook helps, label it as a proposed voiceover or rerecording, not a quote from the footage. Run
  candidates through the sibling `../yt-script/hookscore.py` using its resolved absolute path.
- **On-screen text for the first two seconds**, different words from the spoken line.
- **A loop point**: what the last line sets up so the first line answers it.
- Vertical framing note - what gets cropped out of a 16:9 frame and whether that matters.


## Deliverable

Return start/end timecodes, original source lines, proposed recording changes, captions, and crop
notes. Without timestamped source material, mark timings as estimates. These are clip plans;
claim a finished Short only after a separate media tool has exported and verified it. Keep text
clear of the platform's interface overlays and check the portrait composition on an actual frame.
