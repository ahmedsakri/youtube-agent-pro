# Contributing

Contributions are welcome. The `main` branch is protected: nobody pushes to it directly, including
collaborators. Everything lands through a pull request that the maintainer reviews and merges.

## How to contribute

1. **Fork** the repo (or, if you are a collaborator, branch from `main`).
2. **Branch** per change: `git checkout -b fix/clear-name`.
3. **Make the change.** Keep the house style:
   - No em-dashes or en-dashes anywhere. Use a plain ` - `.
   - Deliver the requested drafts and analyses. Respect explicit review points and the host's
     authorization rules; do not force a new approval question after every already-authorized draft.
     This pack bundles no uploader or account connection.
   - Tools stay dependency-free: standard-library Python 3 only, a `--json` flag, read a file or a
     flag, never phone home.
   - Be honest about what a heuristic can and cannot tell you, in the tool's own docstring.
4. **Run the checks locally** before opening the PR:
   ```bash
   python3 -m pip install -r openai/requirements-dev.txt
   python3 scripts/validate_repo.py
   python3 openai/scripts/validate.py
   python3 -m compileall -q skills openai/skills scripts openai/scripts
   python3 -m unittest discover -s openai/tests -v
   python3 openai/scripts/build_release.py
   ```
5. **Open a PR** against `main`. CI runs the validators, helper and distribution tests, and release
   build on Python 3.9 and 3.12. All checks must pass.

## What CI enforces

- Both editions' 24 skills have valid frontmatter and resolvable local resource links.
- The 24 OpenAI UI metadata files, plugin manifests and marketplace catalogs validate.
- Both editions share identical helpers, hook data, metadata guidance and MIT notices.
- The 47 tests cover helper correctness, installation, packaging and resource completeness.
- Release archives rebuild without changing tracked files.

Claude uses root `skills/`; the OpenAI edition lives in `openai/`. Keep common numerical tools
identical and adapt host-specific instructions explicitly. Update both PDF guides when setup changes.
The `openai/` README documents development dependencies; ReportLab is only needed to rebuild PDFs.

## Review

The maintainer reviews and merges. Direct pushes to `main` are disabled by branch protection, so a
PR is the only way in - that is by design, not an obstacle.
