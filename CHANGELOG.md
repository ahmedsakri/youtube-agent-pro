# Changelog

## Unreleased

- Add Claude Code **agents** support: a top-level `agents/` directory, with the convention documented
  and `scripts/validate_repo.py` extended to validate agent files (frontmatter, name, links).
- Ship 5 specialist subagents that orchestrate the existing skills: `yt-producer`, `yt-strategist`,
  `yt-packager`, `yt-analyst` and `yt-editor`.
- Surface the agents across discovery surfaces: README headline, edition table and install steps,
  the marketplace and plugin manifests (description and keywords), and the GitHub description and
  topics, so the subagents are findable from search.
- Enrich the README for readability and SEO: an SVG hero banner (`assets/og-banner.svg`), badges,
  a table of contents, two Mermaid architecture diagrams, and an FAQ.
- Add a root `llms.txt` so AI search engines (ChatGPT, Perplexity, Gemini, Claude) can index and
  cite the project.

## 2.1.0 — 2026-10-09

- Keep Claude and OpenAI editions in one repository, with explicit commands for each host.
- Add 24 Codex skills with native metadata, a portable OpenAI plugin, a safe local installer,
  and reproducible ChatGPT instructions, workflow reference and ZIP packages.
- Publish separate four-page PDF guides for Claude and ChatGPT/Codex.
- Update both editions' YouTube SEO guidance using official sources: accurate natural keywords,
  distinct descriptions, limited tag value, optional hashtags and Shorts link behavior.
- Make creator profiles optional; honor requested formats, cadence and time zones; distinguish
  drafts and plans from completed media and account actions.
- Fix CSV metric selection, missing data, retention axes, overlapping edits and invalid input handling.
- Add 47 tests, repository consistency checks and Python 3.9/3.12 CI.

The OpenAI plugin has its own initial version, `1.0.0`, within this repository release.
