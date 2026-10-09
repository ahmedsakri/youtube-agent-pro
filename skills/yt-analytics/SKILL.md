---
name: yt-analytics
description: >-
  Read a YouTube Studio export and find the single number holding a video
  or a channel back - impressions, click-through, or retention - then say
  what to fix first. Use for "read my analytics", "which video worked",
  "my views dropped", "what's my CTR telling me", or a pasted Studio
  overview export.
---

# yt-analytics

Reach is a chain: impressions, then click-through, then retention. One link is always the binding
constraint, and fixing any other link is wasted work. This finds the one that matters.

A tool lives here and it runs. Feed it the numbers or the export.

```bash
python3 funnel.py --impressions 42000 --ctr 3.1 --avd 2:10 --length 9:40
python3 funnel.py stats.csv        # a Studio Overview export, one video or many
```

For *where in a video* people leave, that is a different file and a different skill: **/yt-retention**
reads the audience-retention curve. This skill reads the funnel; that one reads the drop-offs.

## Where the numbers live

Studio -> Content -> a video -> Analytics. Impressions and click-through are on the **Reach** tab;
average view duration is on **Engagement**; runtime is the video length. For a channel view, export
the **Overview** table so the tool can rank many videos at once.

## The move

1. Get impressions, CTR, average view duration and runtime - or the exported CSV.
2. Run `funnel.py`. It computes average-percentage-viewed, finds the binding constraint, and names it.
3. Act on **only** the binding constraint:
   - **IMPRESSIONS low** -> topic/packaging problem upstream. The video is not being offered. Rethink
     the idea's reach with **/yt-idea**, not the title.
   - **CTR low** -> the title/thumbnail pairing is the leak. Run **/yt-package** and **/yt-thumbnail**.
   - **RETENTION low** -> the video itself leaks. Run **/yt-retention** on the curve.
4. If nothing is below its band, the job is not to fix - it is to make more of this one. Say that.

## The honest part

The bands (CTR ~4-6%, ~50%+ average viewed) are rules of thumb, not your channel. They move hard by
niche, length and traffic source. Read the binding constraint as "look here first", never as a grade,
and never invent a benchmark the user did not give you.

## What to hand back

- the funnel, link by link, with the binding constraint named
- the one skill to run next, not five
- if many videos: the two that beat the channel and the one axis they share

## The gate

This diagnoses; it does not change your channel and it does not publish. The last line is the
question: **fix the one link, or make more of what already works?**
