# YouTube Agent Pro

**Twenty-four Claude skills and eleven tools that run a YouTube channel end to end.** Free, MIT, no
signup, no API key, nothing to connect.

This is the advanced build of the [YouTube agent skill](https://github.com/Jakeschincariol/youtube-agent-skill)
by Jake Schincariol. It keeps all eleven of the originals and adds thirteen more: an idea engine that
scores a topic before you film it, a thumbnail concept linter, a funnel diagnoser that finds the one
number holding a video back, a cross-platform repurposer, series architecture, a sponsorship rate
card built from your own view numbers, collab outreach, channel-page conversion, a seasonal trend
calendar, a voiceprint that writes your `voice.md` from your own transcripts, production briefs, and
end-screen routing - plus a hub skill that routes a vague request to the right one.

**Nothing gets published until you do it.** These skills write. You upload. Every single one ends in
a block you copy and the same question: **ship it, or change it?**

## Install

In Claude Code, as a plugin:

```
/plugin marketplace add ahmedsakri/youtube-agent-pro
/plugin install youtube-agent-pro
```

Or copy the skills in by hand (global, every project):

```bash
git clone https://github.com/ahmedsakri/youtube-agent-pro.git
cp -r youtube-agent-pro/skills/yt* ~/.claude/skills/
```

Project-local instead: copy the same folders into your repo's `.claude/skills/`. No Claude Code at
all? Paste any single `SKILL.md` at the top of a chat and it runs as a mode - you lose the Python
tools, which is most of the point of the scored ones, but the reasoning still works.

Then **run `/yt-voice` first.** It builds `~/.claude/youtube/voice.md` from three of your own
transcripts - the one file every other skill reads. Ten minutes there beats any prompt you will ever
write, because on YouTube you say the words out loud and a script in the wrong voice is unreadable on
camera.

## The twenty-four skills

**Start here**

| command | what it does |
| --- | --- |
| `/yt` | The hub. Routes a vague request to the right skill, or runs a whole video in order. |
| `/yt-voice` | Builds your `voice.md` from your own transcripts, measured not guessed. Run this first. |

**Make the video**

| command | what it does |
| --- | --- |
| `/yt-idea` | A niche into scored ideas - searchable, specific, bigger than the channel - before you film the wrong one. |
| `/yt-script` | One idea into a script. Five hooks off [21 formulas](skills/yt-script/hooks.json), scored, then the spoken script with the retention beats marked. |
| `/yt-brief` | A script into a shot list: framing, b-roll, on-screen graphics, gear, runtime budget. |
| `/yt-chapters` | Chapters from a transcript, validated against YouTube's own rules so they render. |

**Package it**

| command | what it does |
| --- | --- |
| `/yt-package` | Title and thumbnail text as one pairing, linted for truncation, duplication and vagueness. |
| `/yt-thumbnail` | The thumbnail as a concept - one focal idea, three elements, three words - linted and A/B'd before you open an editor. |
| `/yt-seo` | The description, the tags worth having, and the three queries this should win. |

**Read the numbers**

| command | what it does |
| --- | --- |
| `/yt-analytics` | A Studio export read as a funnel - impressions, CTR, retention - to name the one number to fix. |
| `/yt-retention` | Your retention curve read properly: the hook leak, the cliffs, the slide, and what to change. |
| `/yt-funnel` | The channel page and subscriber conversion - trailer, above-the-fold, sections, the video that converts. |
| `/yt-audit` | The whole channel, ending in ONE fix rather than twenty. |

**Grow it**

| command | what it does |
| --- | --- |
| `/yt-viral` | What is working in your niche, ranked by multiple over each channel's own median - not by channel size. |
| `/yt-trend` | A 90-day calendar: seasonal demand, the evergreen/timely mix, the reserved reaction slot. |
| `/yt-series` | A multi-video series or playlist as an architecture - a binge order, each video earning the next click. |
| `/yt-collab` | The right channels to collaborate with, by audience overlap and size band, plus the pitch that gets a reply. |
| `/yt-endscreen` | End screens and cards placed to keep the session going, read off the retention curve. |

**Multiply it**

| command | what it does |
| --- | --- |
| `/yt-shorts` | The Shorts already inside a long video, with a new first line written for each. |
| `/yt-repurpose` | One long video into a thread, a LinkedIn post, a newsletter section and a blog outline - rewritten, not pasted. |
| `/yt-plan` | A week that fits the hours you actually have. One anchor, one cheap one, three Shorts. |

**Run it like a business**

| command | what it does |
| --- | --- |
| `/yt-sponsor` | A defensible rate card from your own views, the reply to the brand, and an integration that does not tank retention. |
| `/yt-comment` | The comment section triaged into piles, then replies in your voice. Says which one to pin. |

## The eleven tools

Every one runs on a clean Python 3 with no dependencies. They are the reason these are skills and not
just prompts.

```bash
python3 skills/yt-idea/ideascore.py --idea "..."                  # score an idea on 4 axes
python3 skills/yt-script/hookscore.py --hook "one line"           # 5-property hook panel
python3 skills/yt-package/title.py --title "..." --thumb "..."    # title + thumbnail linter
python3 skills/yt-thumbnail/thumblint.py --concept "..." --title "..."  # thumbnail concept linter
python3 skills/yt-analytics/funnel.py --impressions 42000 --ctr 3.1 --avd 2:10 --length 9:40  # the binding constraint
python3 skills/yt-retention/retention.py retention.csv            # where they left, and why
python3 skills/yt-edit/deadair.py transcript.srt                  # edit decision list
python3 skills/yt-chapters/chapters.py transcript.srt            # validated chapters
python3 skills/yt-viral/swipe.py collected.json --min 2.0        # outliers by own-channel multiple
python3 skills/yt-sponsor/ratecard.py --views 12000 --niche tech # sponsorship rate band
python3 skills/yt-voice/voiceprint.py best-video.txt            # measure how you actually talk
```

Every tool takes `--json` for piping, reads a file or a flag, and never phones home.

## The fine print

The part most packs leave out.

**It does not publish.** YouTube's Data API would allow it with your own OAuth. It is deliberately not
built here: every skill ends in a block you copy and a question - ship it, or change it? Anything that
claims to run your channel unattended should be read with that distinction in mind.

**The scorers are heuristics, not predictors.** `hookscore.py`, `ideascore.py`, `thumblint.py` and
`funnel.py` read the *words and the structure* of what you give them, not the market and not the
result. A low score is a reason to look again; a high score is not a promise. `hookscore.py` in
particular was calibrated against 74 real short-form hooks and separates deliberately bad hooks from
real ones well - and a creator's own hits from their own misses barely at all.

**`ratecard.py` gives negotiation anchors, not a quote.** The CPM bands are widely cited industry
ranges. Real deals move on geography, engagement, exclusivity and usage rights.

**`/yt-viral` and `/yt-collab` read, they do not scrape.** Public listings only. They never log in as
you and never touch your credentials.

**Nothing invents a number.** If a skill wants a figure it does not have, it asks you for it or writes
the line without it.

## Built on

The original [`youtube-agent-skill`](https://github.com/Jakeschincariol/youtube-agent-skill) by
**Jake Schincariol** (MIT). This pack extends it; the original hook formulas, the scored-hook idea,
the "nothing publishes" discipline and six of the eleven tools are his. Advanced skills and tools, and
this build, by **Ahmed Sakri**.

## Licence

MIT. Use it, change it, ship it. See [LICENSE](LICENSE).
