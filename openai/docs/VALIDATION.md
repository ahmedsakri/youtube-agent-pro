# Verification report

Verified on 2026-10-09. Results describe this release, not a guarantee of every future host or task.

## Automated checks

- **47 passing tests:** 28 helper integration tests and 19 installation/distribution tests.
- **48 skill entrypoints validated:** 24 Claude and 24 OpenAI skills pass the official Codex skill
  creator's frontmatter validator. The OpenAI edition also validates all 24 `agents/openai.yaml` files.
- **11 identical helper implementations:** the repository validator compares both editions byte for
  byte, along with their hook data, SEO references and license notices.
- **Paths and errors:** helpers run from an unrelated working directory using installed folders with
  spaces. Tests exercise JSON output, help, missing files, empty data, invalid numeric inputs and units.
- **Numerical regressions:** correct CSV metric selection; zero versus missing values; Shorts-specific
  interpretation; retention time versus percentage axes; overlapping edit intervals; missing view counts.
- **Installation:** complete sibling skill set, metadata and resources; conflict refusal; backup and
  rollback behavior; source preservation; rejection of unsafe symbolic-link paths.
- **Distribution:** deterministic archives, explicit public-file allowlists, checksum output, complete
  metadata and resources, license copies, and no private profiles or secrets included in fixtures.
- **Archive verification:** local Markdown links checked across both generated ZIP files with none
  broken. A real plugin ZIP was extracted into a fresh directory containing spaces; its own validator,
  all 47 tests and release rebuild passed in a clean environment with development requirements installed.

CI repeats the repository checks, compilation, 47 tests and packaging on Python 3.9 and 3.12. Refer
to the repository's Actions run for the status of a particular commit. Runtime helpers, the installer
and the release builder use the standard library; PyYAML is a validation-only dependency.

## Host and behavior checks

The installed Codex CLI discovered the original repository's local marketplace as
`youtube-agent-pro-openai@youtube-agent-pro`, version `1.0.0`, resolving to `openai/`. This was a
read-only discovery test using per-command configuration; no global plugin was installed or enabled.

An independent agent read the actual skill instructions and checked two realistic requests:

1. Seven finished Shorts, one per day at noon Asia/Kolkata beginning 10 October 2026: produced
   10–16 October at noon, without requiring a voice profile or adding long-form videos.
2. A 30-second Short with 200 views and 12-second average view duration: computed 40% average viewed,
   identified missing distribution/engagement evidence, and did not claim that SEO caused low reach.

Both four-page PDF guides were rendered and all eight pages inspected for clipping, layout and
command accuracy. Text checks and deterministic rebuilds also passed.

## What has not been established

- No end-to-end install was performed inside the user's Claude or ChatGPT account. Their UI, plan,
  permissions and available tools can differ. Claude command names were checked against its official
  plugin documentation; ChatGPT file-based instructions provide a fallback to native plugins.
- GitHub distribution does not register a plugin in OpenAI's public directory or a ChatGPT workspace.
- These are instruction workflows and local analytical helpers. No actual upload, scheduled publish,
  account edit, thumbnail render or video render was tested because the pack contains none of those services.
- Text scores and sponsorship bands remain illustrative heuristics, not validated performance forecasts
  or live market rates. The helper word lists are primarily English-oriented.
- Behavioral examples are useful smoke checks, not a statistically representative model evaluation.

See [PORTING_NOTES.md](PORTING_NOTES.md) for source provenance, design changes and official references.
