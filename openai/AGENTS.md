# Maintaining the OpenAI edition

This is a public, reusable YouTube workflow pack. Keep channel-specific profiles, exports,
credentials and personal data out of the repository and release bundles.

- `skills/` is the canonical source for all 24 workflows and 11 Python helpers. The ChatGPT
  workflow document is generated from these files; do not maintain a second divergent copy.
- Keep runtime helpers and distribution scripts compatible with Python 3.9+ and standard-library
  only. PyYAML is a development-only dependency for validation.
- Resolve helper paths from the installed skill directory. Install and package all sibling skills
  because some share resources. Preserve the MIT notice in every distribution.
- Skills produce drafts, plans and analysis. They do not supply YouTube authentication, an uploader,
  video rendering, or access to private analytics. State what actually ran.
- Preserve user intent and existing authorization. Missing voice profiles must not block tasks that
  can proceed from available context. Treat heuristic scores as suggestions, not forecasts.
- For changes, run `python3 scripts/validate.py`, `python3 -m unittest discover -s tests -v`, and
  `python3 scripts/build_release.py`. Check the relevant workflow with a realistic request when its
  behavior changes. Run `git diff --check` before committing.
