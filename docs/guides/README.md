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

## Earlier guide links

The existing [setup-guide URL](../YouTube-Agent-Pro-Setup-Guide.pdf) remains available as a byte-for-byte copy of the current Claude guide. The default build refreshes that alias, so there is only one maintained source of Claude setup guidance. A custom `--output-dir` generates the two edition guides there without changing the repository's alias.

`python3 docs/build_guide.py` is a deprecated compatibility entry point for the same builder. It now emits PDFs directly instead of writing HTML for manual browser printing.

The previous 16-page design and all its source remain preserved at commit `3f08946ed3c03f127c32a4549b09936d0c7d17fc`:

- [Original HTML generator and visual design](https://github.com/ahmedsakri/youtube-agent-pro/blob/3f08946ed3c03f127c32a4549b09936d0c7d17fc/docs/build_guide.py)
- [Original 16-page PDF](https://github.com/ahmedsakri/youtube-agent-pro/blob/3f08946ed3c03f127c32a4549b09936d0c7d17fc/docs/YouTube-Agent-Pro-Setup-Guide.pdf)

Those historical files document the earlier release; their commands and behavior are superseded by the current edition guides.
