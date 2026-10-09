# Port analysis

Source: [ahmedsakri/youtube-agent-pro](https://github.com/ahmedsakri/youtube-agent-pro), commit
`54512045264b9d0d88d82d48d081dfdd62204b46`. This edition lives in `openai/` in the same repository, preserving the project history and MIT
notices. The Claude edition at the root receives the same corrected workflows and numerical helpers,
with its own invocation and profile conventions.

## What the source does well

- Twenty-four focused workflows cover idea selection through post-publication analysis.
- Eleven small, local Python tools make parts of the workflow measurable and reproducible.
- The hook library and transcript-based voice profile provide useful reusable context.
- There is no hidden API dependency or account-writing code in the pack.

## Adaptation decisions

| Source behavior | OpenAI edition |
| --- | --- |
| Claude plugin manifest and slash-command installation | Portable `plugin.json`, local marketplace and native Codex skill metadata |
| `~/.claude/youtube/voice.md` | Supplied profile/context first; optional workspace `.youtube-agent/voice.md` |
| Missing profile can stop every workflow | Continue useful work; ask only for missing task-critical input |
| Relative helper examples assume current directory | Resolve from the actual installed skill directory |
| Sibling helper and hook-library references | Install and package all 24 skills together |
| Forced "ship it" gate after every stage | Finish authorized drafting workflows without repetitive approval gates |
| Hub requests brief before the script it needs | Script before production brief |
| Fixed weekly cadence and long-form assumptions | Honor the user's formats, time zone, capacity and Shorts-only scope |
| Generic funnel rules can sound causal | Separate observations, heuristic suggestions and missing evidence |
| ChatGPT filesystem and execution assumptions | Separate native-plugin and prompt/file routes; disclose missing capabilities |

The packaging includes a ChatGPT workflow document generated from the canonical skills, preventing
a separately maintained prompt from drifting. No OAuth app, MCP server, model-specific API client,
upload bot or video renderer has been added.

## Numerical correctness

The source audit found issues in CSV column selection, missing-value handling, retention-axis
inference and overlapping edit intervals. Regression coverage and final results are recorded in
[VALIDATION.md](VALIDATION.md). Heuristic outputs remain suggestions; even correct calculations
cannot promise views or prove a causal reason for a video's performance.

## Compatibility references

Checked against the official documentation on 2026-10-09:

- [Build skills](https://learn.chatgpt.com/docs/build-skills): discovery, invocation and local scope.
- [Package a plugin](https://developers.openai.com/plugins/build/plugins): portable manifest,
  marketplace and distribution boundaries.
- [Build plugins in ChatGPT](https://learn.chatgpt.com/docs/build-plugins): workspace creation and testing.

The native plugin needs a host that supports the current portable manifest. Standalone skill
installation is the fallback for Codex. The ChatGPT file route is the fallback when plugin creation
or installation is unavailable. This is an independent community project, not an OpenAI product.
