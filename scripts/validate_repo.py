#!/usr/bin/env python3
"""Check the Claude edition and consistency of this two-edition repository."""
import json
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)

    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    check(len(skills) == 24, "Expected 24 Claude skills")
    for path in skills:
        text = path.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        check(text.startswith("---\n") and len(parts) == 3, "Missing frontmatter: " + str(path))
        if len(parts) != 3:
            continue
        meta = yaml.safe_load(parts[1])
        check(isinstance(meta, dict) and meta.get("name") == path.parent.name, "Skill name mismatch: " + str(path))
        check(isinstance(meta, dict) and isinstance(meta.get("description"), str), "Missing description: " + str(path))
        check("$yt" not in text and ".youtube-agent/voice.md" not in text, "OpenAI-only instructions in Claude skill: " + str(path))
    agents = sorted(p for p in (ROOT / "agents").glob("*.md") if p.name != "README.md")
    for path in agents:
        text = path.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        check(text.startswith("---\n") and len(parts) == 3, "Missing frontmatter: " + str(path))
        if len(parts) != 3:
            continue
        meta = yaml.safe_load(parts[1])
        check(isinstance(meta, dict) and meta.get("name") == path.stem, "Agent name mismatch: " + str(path))
        check(isinstance(meta, dict) and isinstance(meta.get("description"), str), "Missing description: " + str(path))
    helpers = sorted((ROOT / "skills").glob("*/*.py"))
    check(len(helpers) == 11, "Expected 11 Claude helpers")
    for path in helpers + [ROOT / "skills/yt-script/hooks.json", ROOT / "skills/yt-seo/references/youtube-metadata.md"]:
        check(path.read_bytes() == (ROOT / "openai" / path.relative_to(ROOT)).read_bytes(), "Edition data/helper drift: " + str(path))
    check((ROOT / "LICENSE").read_bytes() == (ROOT / "openai/LICENSE").read_bytes(), "License drift")
    check((ROOT / "templates/voice.md").read_bytes() == (ROOT / "skills/yt-voice/assets/voice.md").read_bytes(), "Legacy voice template drift")
    pages = list((ROOT / "skills").rglob("*.md")) + [ROOT / "README.md"] + list((ROOT / "docs").rglob("*.md")) + list((ROOT / "agents").glob("*.md"))
    for path in pages:
        for link in re.findall(r"\]\(([^\s)]+)\)", path.read_text(encoding="utf-8")):
            if link.startswith(("https://", "http://", "#", "mailto:")):
                continue
            target = (path.parent / link.split("#")[0]).resolve()
            check(ROOT == target or ROOT in target.parents, "Link escapes repository: " + link)
            check(target.exists(), "Missing link in {}: {}".format(path.relative_to(ROOT), link))
    for path in [ROOT / ".claude-plugin/plugin.json", ROOT / ".claude-plugin/marketplace.json", ROOT / ".agents/plugins/marketplace.json"]:
        json.loads(path.read_text(encoding="utf-8"))
    catalog = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    check(catalog["name"] == "youtube-agent-pro", "Wrong OpenAI marketplace name")
    check(catalog["plugins"][0]["source"]["path"] == "./openai", "Wrong OpenAI plugin source")
    for name in ["Claude", "OpenAI"]:
        pdf = ROOT / "docs/guides" / ("YouTube-Agent-Pro-" + name + ".pdf")
        check(pdf.read_bytes().startswith(b"%PDF-"), "Missing or invalid PDF: " + name)
    check((ROOT / "docs/YouTube-Agent-Pro-Setup-Guide.pdf").read_bytes() ==
          (ROOT / "docs/guides/YouTube-Agent-Pro-Claude.pdf").read_bytes(), "Legacy guide URL must serve the current Claude guide")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Validated Claude skills, {} agents, 11 identical helpers, shared resources, both catalogs, PDFs and repository links.".format(len(agents)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
