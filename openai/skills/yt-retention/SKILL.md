---
name: yt-retention
description: >-
  Read a YouTube Studio audience-retention export and find where viewers
  actually leave, then say what to change. Use for "why do people stop
  watching", "my retention is bad", a pasted retention chart or CSV, or "fix
  my pacing".
---

# yt-retention

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

Read an audience-retention export alongside the video length and, when available, a timestamped
transcript. A drop suggests a place to inspect; it does not establish why viewers left.

```bash
python3 "$YT_SKILL_DIR/retention.py" retention.csv --duration 600 --axis percent
python3 "$YT_SKILL_DIR/retention.py" retention.csv --axis seconds --transcript transcript.srt
python3 "$YT_SKILL_DIR/retention.py" shorts-retention.csv --axis seconds --duration 30 --hook-seconds 3
```

`--axis auto` uses column labels to identify seconds, percent, or elapsed-time ratios. For an
ambiguous unit-less axis, specify `--axis seconds`, `--axis percent`, or `--axis fraction`; percent
and fraction axes need the actual runtime. Do not guess units from whether the largest value
happens to be below 100. The helper also recognizes an `audienceWatchRatio` column for retention
fractions; inspect its diagnostics and make other source units explicit before analysis.

Get the audience-retention data from Studio's video Analytics/Engagement export when available;
if the UI does not offer that export, work from supplied chart data or a clearly labeled manual
reading. Never fabricate samples from a chart you cannot read.

## Patterns to inspect

- **Opening loss:** compare the opening window with videos of similar length and format. The
  helper uses the first 10% of runtime, capped at 30 seconds, when duration is supplied. Set
  `--hook-seconds` for a different window; for a Short, inspect the first seconds alongside
  stayed-to-watch data and the opening footage.
- **Cliffs:** inspect the exact transcript/footage at a sharp drop for topic changes, sponsor reads,
  slow setup, or an unmet promise. An edit or transition may matter as much as the script.
- **Gradual decline:** look for repeated material or delayed payoff. Compare against the channel's
  own curves before calling normal attrition a failure.
- **Peaks and loops:** a replay or confusing segment can both make a peak. Shorts can exceed 100%
  viewed; distinguish replay behavior from a causal claim about satisfaction.

## What to hand back

Name the most consequential supported observation, its timecode, and one proposed change.
Separate measured changes from interpretations. If the curve is healthy, use
[$yt-analytics](../yt-analytics/SKILL.md) for other evidence instead of declaring packaging at fault
from retention alone. Respect requests for a full audit rather than withholding other findings.
