# YouTube Agent Pro for ChatGPT and Codex

**24 skills. 11 local Python tools. From video idea to performance review.**

Draft scripts, improve titles and thumbnail concepts, plan Shorts, read retention exports and build
content calendars from your own material. This OpenAI edition adapts
[YouTube Agent Pro](https://github.com/ahmedsakri/youtube-agent-pro) with native skill metadata,
portable packaging, and fixes to analytics edge cases.

Free, MIT-licensed code. No API key or runtime Python dependencies. Your ChatGPT/Codex plan and tool
availability still apply. The pack produces drafts, plans and analysis; it includes no YouTube login,
uploader, scheduling service or video renderer. It does not promise virality.

## Start with Codex

Requires Python 3.9+ for installation and analysis tools:

```bash
git clone https://github.com/ahmedsakri/youtube-agent-pro.git
cd youtube-agent-pro/openai
python3 scripts/install.py --dry-run
python3 scripts/install.py
```

The installer copies all 24 sibling skills to `~/.agents/skills`, with shared resources and license
notices. It refuses conflicting existing skills. To update intentionally, `--force` backs up existing
folders before replacement. Keep the backups until you verify the update.

For a single project, choose its skill directory:

```bash
python3 scripts/install.py --dest /absolute/path/to/your-project/.agents/skills
```

Use one installation route to avoid duplicate skill names. Start a new Codex conversation; restart
your client if the skills do not appear. Try:

```text
Use $yt to plan my next video about beginner photography. My audience uses phones.
Use $yt-script to turn this outline into a 45-second English Short.
Use $yt-analytics to review this export. Tell me what the data cannot establish.
```

Natural-language requests can also select a relevant skill automatically. See
[OpenAI's skill guide](https://learn.chatgpt.com/docs/build-skills) for invocation and discovery.

## Install as a plugin

Current compatible hosts can use `plugin.json` and `.agents/plugins/marketplace.json`. On a Codex
CLI that provides the plugin commands:

```bash
codex plugin marketplace add ahmedsakri/youtube-agent-pro
codex plugin add youtube-agent-pro-openai@youtube-agent-pro
```

The local marketplace is also available to supported desktop clients when the repository is opened
as a project. Select the plugin from its local source. If unavailable, use the standalone installer.
This does not publish a plugin to OpenAI's public directory or to a ChatGPT workspace. See
[plugin packaging](https://developers.openai.com/plugins/build/plugins).

## Start with ChatGPT

From the [latest release](https://github.com/ahmedsakri/youtube-agent-pro/releases/latest),
download `ChatGPT-INSTRUCTIONS.md`, `ChatGPT-WORKFLOWS.md` and the optional ChatGPT ZIP.
Paste the instructions into a conversation or project, attach the workflows and your source
material, and ask for a concrete result. For computed scores, a Python-capable mode must extract
and run the ZIP's tools. Otherwise request a qualitative review. Native installed plugins and
skills can be selected with `@` where available.

See [ChatGPT setup](chatgpt/README.md) for both routes and their capabilities. Build the same files
locally with:

```bash
python3 scripts/build_release.py
```

## Workflows

| Stage | Skills | Useful output |
| --- | --- | --- |
| Direction | `yt`, `yt-voice`, `yt-idea`, `yt-trend` | Routing, optional voice profile, scored ideas, calendar |
| Production | `yt-script`, `yt-brief`, `yt-edit`, `yt-chapters` | Hooks, scripts, shot lists, edit plans, chapters |
| Packaging | `yt-package`, `yt-thumbnail`, `yt-seo` | Title pairings, visual concepts, descriptions |
| Performance | `yt-analytics`, `yt-retention`, `yt-audit`, `yt-funnel` | Export analysis, retention review, next experiments |
| Reuse and planning | `yt-shorts`, `yt-repurpose`, `yt-series`, `yt-plan`, `yt-endscreen` | Clip plans, platform drafts, series, calendars |
| Research and business | `yt-viral`, `yt-collab`, `yt-sponsor`, `yt-comment` | Sourced comparisons, pitches, rate scenarios, replies |

The eleven helpers are `ideascore.py`, `hookscore.py`, `title.py`, `thumblint.py`, `funnel.py`,
`retention.py`, `deadair.py`, `chapters.py`, `swipe.py`, `ratecard.py` and `voiceprint.py`.
They run locally, use no model API and make no network requests. Examples from the `openai/` directory:

```bash
python3 skills/yt-script/hookscore.py --hook "I tested three phone cameras in the same dark room" --json
python3 skills/yt-package/title.py --title "Three Phone Cameras, One Dark Room" --thumb "WHICH WINS?" --json
python3 skills/yt-analytics/funnel.py --impressions 42000 --ctr 3.1 --avd 2:10 --length 9:40 --json
python3 skills/yt-voice/voiceprint.py /absolute/path/to/transcript.txt --json
```

Installed skills resolve helpers from their own location. Keep all siblings installed because some
share the hook library and operating guide.

## Your channel context

Use a supplied voice profile or the conversation. The optional local default is
`.youtube-agent/voice.md`; start from [the template](skills/yt-voice/assets/voice.md), or ask `$yt-voice`.
A missing profile does not block other tasks. Private profiles and exports do not belong in this
public repository; `.youtube-agent/` is ignored by Git.

Heuristic scores are editing aids, not forecasts. Research claims need sources. Shorts-feed
performance must not be diagnosed using long-form thumbnail CTR alone. Sponsorship figures are
illustrative USD assumptions unless replaced with supported deal data. Clip selection does not
establish copyright permission for source footage.

## Development and verification

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build_release.py
```

On Windows, use `.venv\Scripts\python.exe` instead. Runtime tools and installers use only Python's
standard library; PyYAML is solely for development-time metadata validation.
See the [port analysis](docs/PORTING_NOTES.md) and [verification report](docs/VALIDATION.md).
CI validates, tests and builds on Python 3.9 and 3.12.

## License

[MIT](LICENSE). Preserve copyright and permission notices in redistributions. Maintained by Ahmed
Sakri. This is an independent community project, not an official OpenAI product.
