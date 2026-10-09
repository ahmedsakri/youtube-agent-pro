# Edition guides

- [Claude guide](YouTube-Agent-Pro-Claude.pdf): Claude Code installation, plugin versus manual commands, creator voice setup, all 24 workflows and practical examples.
- [OpenAI guide](YouTube-Agent-Pro-OpenAI.pdf): Codex installation, portable ChatGPT setup, all 24 workflows, creator context and verification limits.

Both guides are four pages and describe the same public repository. They explain which capabilities the pack supplies and which require tools from the host.

## Rebuild

From the repository root, with ReportLab installed in your documentation environment:

```bash
python3 -m pip install reportlab
python3 docs/build_guides.py
```

ReportLab is a documentation build dependency only. The skill helpers and installers do not require it. You can select a different output location with `--output-dir`.

The generator uses built-in PDF fonts, fixed metadata and vector text for portable, reproducible output. After changing it, render every page with Poppler (`pdftoppm -png`) and check the latest images for clipping, overlaps, incorrect commands and stale platform claims. Compare installation guidance with the root README, `openai/README.md` and `openai/chatgpt/README.md`.
