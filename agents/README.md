# Agents

Claude Code subagents for YouTube Agent Pro. Each agent is a focused specialist that the main
assistant can delegate a whole workflow to, orchestrating the plugin's [`yt-*` skills](../skills)
rather than duplicating them.

Skills are the instructions; agents decide *which* skills to run, in what order, and carry the
work end to end inside their own context.

## File convention

One Markdown file per agent, named after the agent (`agents/<name>.md`). YAML frontmatter:

```yaml
---
name: yt-producer          # must match the filename stem
description: >-            # when the main assistant should delegate here
  One or two sentences describing the agent's job and trigger phrases.
tools: Read, Write, Edit, Bash, Glob, Grep   # optional; omit to inherit all tools
model: opus               # optional; opus | sonnet | haiku | inherit
---
```

The body tells the agent how to route: it links to the [`SKILL.md`](../skills) files it owns and
describes the order to apply them. Keep links relative so they resolve inside the repository.

## Validation

`python scripts/validate_repo.py` checks every `agents/*.md` (except this README): frontmatter is
present, `name` matches the filename, and all relative links resolve inside the repository.

## Available agents

The specialist agents are listed in the [project README](../README.md#agents).
