# Contributing

Contributions are welcome. The `main` branch is protected: nobody pushes to it directly, including
collaborators. Everything lands through a pull request that the maintainer reviews and merges.

## How to contribute

1. **Fork** the repo (or, if you are a collaborator, branch from `main`).
2. **Branch** per change: `git checkout -b fix/clear-name`.
3. **Make the change.** Keep the house style:
   - No em-dashes or en-dashes anywhere. Use a plain ` - `.
   - Every skill ends in a gate: a copy block and the question "ship it, or change it?". Nothing in
     this pack publishes on the user's behalf.
   - Tools stay dependency-free: standard-library Python 3 only, a `--json` flag, read a file or a
     flag, never phone home.
   - Be honest about what a heuristic can and cannot tell you, in the tool's own docstring.
4. **Run the checks locally** before opening the PR:
   ```bash
   python3 -m compileall -q skills
   # then run any tool you touched, e.g.
   python3 skills/yt-idea/ideascore.py --idea "test" --json
   ```
5. **Open a PR** against `main`. CI runs the tool smoke tests, validates every JSON manifest, and
   checks that each skill has valid frontmatter, on Python 3.9 and 3.12. All checks must pass.

## What CI enforces

- every tool compiles and the standalone ones run under `--json`
- every `*.json` manifest parses
- every `skills/*/SKILL.md` has `name:` and `description:` frontmatter

## Review

The maintainer reviews and merges. Direct pushes to `main` are disabled by branch protection, so a
PR is the only way in - that is by design, not an obstacle.
