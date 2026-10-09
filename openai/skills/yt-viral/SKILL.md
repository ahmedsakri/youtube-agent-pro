---
name: yt-viral
description: >-
  Find what is actually working in the user's niche on YouTube and rank it
  by how far each video beat its own channel, then name the formula. Use for
  "what's working right now", "find viral videos in my niche", "why did this
  blow up", competitor research, or a swipe file.
---

# yt-viral

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

Compare videos by **multiple over each channel's own median** as one useful outlier measure.
Account for age, format, and topic before interpreting the multiple; public counts cannot establish
why a video worked or predict whether copying its structure will succeed.

```bash
python3 "$YT_SKILL_DIR/swipe.py" collected.json --min 2.0
```

## Collecting the input

The helper requires at least **four videos per channel**, but a small sample still gives an unstable
baseline. Collect verified public listings through available browsing, user-provided exports, or
an available public-data tool. Record collection date, publication dates, format, and comparable
video age; avoid mixing long-form and Shorts in one baseline. Inspect missing counts before scoring.

```json
[{"channel":"...","title":"...","views":412000,"url":"...","duration":613}]
```

**Read, do not scrape.** Public listings only, never a logged-in session, never the user's own
account credentials.

## Reading the output

The multiple is the signal. The formula line is a judgement about the TITLE, matched against
[the 21 formulas](../yt-script/hooks.json) - it is not a claim about why the video worked, and you
should say so when you present it.

What to hand back: the top five with their multiples, the formula each used, and the ONE structural
thing they share. Then the harder line - which of those the user could actually make this week, in
their voice, with what they have.
