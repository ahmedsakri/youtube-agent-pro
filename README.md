# YouTube Agent Pro - Claude, ChatGPT & Codex

[![CI](https://github.com/ahmedsakri/youtube-agent-pro/actions/workflows/ci.yml/badge.svg)](https://github.com/ahmedsakri/youtube-agent-pro/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**One repository. 24 YouTube creator workflows per edition. 11 local Python tools.**

Plan YouTube Shorts and long-form videos, write scripts and hooks, improve titles and thumbnail
concepts, draft accurate SEO descriptions, and analyze your own YouTube Analytics exports.
Choose the Claude or OpenAI edition below; each has instructions written for its host.

Free, MIT-licensed code. The Python tools need no API key or runtime packages. Your AI provider's
plan and available tools still apply. This pack creates drafts, plans and analysis; it does not
include a YouTube uploader, scheduling service, account connection or video renderer.

[Claude PDF guide](docs/guides/YouTube-Agent-Pro-Claude.pdf) ·
[ChatGPT & Codex PDF guide](docs/guides/YouTube-Agent-Pro-OpenAI.pdf) ·
[Download release files](https://github.com/ahmedsakri/youtube-agent-pro/releases/latest)

## Choose your edition

| Use it in | Location | How to ask |
| --- | --- | --- |
| Claude Code plugin | Root `skills/` and `.claude-plugin/` | `/youtube-agent-pro:yt` or `/youtube-agent-pro:yt-seo` |
| Claude Code, manually installed skills | Root `skills/` | `/yt` or `/yt-seo` |
| OpenAI Codex | [`openai/`](openai/README.md) | `$yt` or `$yt-seo` |
| ChatGPT | [OpenAI instructions and workflow files](openai/chatgpt/README.md) | Ask naturally; use `@` for installed skills where supported |

### Claude Code

In Claude Code:

```text
/plugin marketplace add ahmedsakri/youtube-agent-pro
/plugin install youtube-agent-pro@youtube-agent-pro
/youtube-agent-pro:yt
```

Update the registered marketplace with `/plugin marketplace update youtube-agent-pro`.
Plugin skills use the plugin namespace. If you prefer manual installation, copy **all** root
`skills/yt*` folders into `~/.claude/skills/` or a project's `.claude/skills/`; those use `/yt`,
`/yt-script`, and so on. Check for existing names before copying. Use one route to avoid duplicates.

### OpenAI Codex

With Python 3.9 or later:

```bash
git clone https://github.com/ahmedsakri/youtube-agent-pro.git
cd youtube-agent-pro/openai
python3 scripts/install.py --dry-run
python3 scripts/install.py
```

Start a new Codex conversation and try:

```text
Use $yt-script to turn this outline into a 45-second English Short.
Use $yt-seo to write accurate title options and a unique description for this transcript.
Use $yt-analytics to review this export and explain what the numbers cannot establish.
```

The installer keeps all 24 skills together in `~/.agents/skills`, including their shared resources.
It refuses conflicts; an intentional update with `--force` first makes backups. A project-specific
destination and an alternative native plugin route are documented in the [OpenAI edition](openai/README.md).

### ChatGPT

Download `ChatGPT-INSTRUCTIONS.md` and `ChatGPT-WORKFLOWS.md` from the
[latest release](https://github.com/ahmedsakri/youtube-agent-pro/releases/latest). Add the instructions
to a conversation or project, attach the workflows and your source material, then ask for a result.
For computed scores, use the optional ChatGPT ZIP with a mode that can extract and execute Python.
Without execution, request a qualitative review. See [complete setup and capability limits](openai/chatgpt/README.md).

## The 24 workflows

Use the name below with your edition's invocation syntax, such as `/youtube-agent-pro:yt-script`
in the Claude plugin or `$yt-script` in Codex.

| Workflow | What you get |
| --- | --- |
| `yt` | Route a request or develop a complete video production package |
| `yt-voice` | An optional creator voice profile based on supplied transcripts |
| `yt-idea` | Relevant ideas and transparent heuristic comparisons |
| `yt-script` | Hooks, spoken scripts and retention beats |
| `yt-brief` | Shot lists, framing, graphics and production notes |
| `yt-edit` | Transcript-based edit decisions and dead-air suggestions |
| `yt-chapters` | Chapters checked for timestamp and formatting rules |
| `yt-package` | Accurate title and thumbnail-text pairings |
| `yt-thumbnail` | Visual concepts and a concept-level checklist |
| `yt-seo` | Video-specific descriptions, natural keywords and relevant tags |
| `yt-analytics` | Export analysis with missing evidence clearly identified |
| `yt-retention` | Retention curves, timecoded drops and testable editing ideas |
| `yt-funnel` | Channel page and subscriber-conversion review |
| `yt-audit` | A prioritized channel review grounded in supplied evidence |
| `yt-viral` | Public examples compared with each channel's own baseline |
| `yt-trend` | Sourced trend research and seasonal planning |
| `yt-series` | Series structure, playlist order and next-video connections |
| `yt-collab` | Audience-fit research and draft collaboration pitches |
| `yt-endscreen` | End-screen and card plans for eligible formats |
| `yt-shorts` | Standalone clip plans and new openings from supplied material |
| `yt-repurpose` | Platform-specific drafts from one source video |
| `yt-plan` | A calendar matched to your cadence, capacity and time zone |
| `yt-sponsor` | Illustrative rate scenarios, pitches and integration drafts |
| `yt-comment` | Comment triage, reply drafts and pin suggestions |

## YouTube SEO, with realistic expectations

Both editions ground titles and descriptions in the actual video, use one or two main topic terms
naturally, and write distinct descriptions for each upload. Tags have a limited role, especially for
misspellings; relevant hashtags remain optional. Shorts description URLs are not clickable, so
calls to action must match the destination available to viewers. These rules are based on
[YouTube's current metadata guidance](skills/yt-seo/references/youtube-metadata.md).

Search relevance and Shorts-feed recommendations are different. Low views alone cannot identify an
SEO problem, and no keyword list, thumbnail or posting time guarantees reach. The analytics workflow
distinguishes evidence from hypotheses and avoids applying long-form CTR rules to Shorts-feed views.

## Local tools and creator context

The 11 Python helpers cover idea and hook scoring, title and thumbnail-concept checks, funnel and
retention analysis, edit intervals, chapters, public-video comparisons, sponsorship scenarios and
transcript voice measurements. They operate on supplied data and make no network requests.

From the repository root, for example:

```bash
python3 skills/yt-package/title.py --title "Three Phone Cameras, One Dark Room" --thumb "WHICH WINS?" --json
python3 skills/yt-analytics/funnel.py --format shorts --avd 12 --length 30 --json
python3 skills/yt-retention/retention.py --help
```

Scores are editing aids, not predictions. Text heuristics are English-oriented; sponsorship bands
are illustrative USD assumptions. Use your language, audience data and verified deal terms to guide
decisions. A thumbnail concept is not a rendered image, and clip selection does not establish
permission to reuse the source footage.

Voice setup is optional. Supplied context comes first; Claude's default profile is
`~/.claude/youtube/voice.md`, while Codex uses a workspace `.youtube-agent/voice.md` when present.
ChatGPT uses attached profiles or conversation context. Keep private exports, credentials and
profiles out of this public repository.

## Verification and maintenance

The editions share byte-identical Python helpers, checked by the repository validator. Regression
tests cover installation, packaging, missing data, CSV columns, retention axes, overlapping edits,
and execution from unrelated folders with spaces. See the [verification report](openai/docs/VALIDATION.md)
and [adaptation notes](openai/docs/PORTING_NOTES.md) for evidence and limits.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r openai/requirements-dev.txt
.venv/bin/python scripts/validate_repo.py
.venv/bin/python openai/scripts/validate.py
.venv/bin/python -m unittest discover -s openai/tests -v
.venv/bin/python openai/scripts/build_release.py
```

CI runs on Python 3.9 and 3.12. PDF sources and rebuild instructions are in
[`docs/guides/`](docs/guides/README.md). This repository distributes community skills; publishing it
does not register a plugin in OpenAI's public directory or grant access to a YouTube account.

Contributions go through a pull request; see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE). Maintained by Ahmed Sakri. Preserve the included copyright and permission notices
when redistributing. This is an independent project, not affiliated with YouTube, Anthropic or OpenAI.
