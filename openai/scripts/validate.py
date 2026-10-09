#!/usr/bin/env python3
"""Validate the complete OpenAI skill pack and its local resource links."""
import json
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    raise SystemExit("Development validation needs PyYAML: python -m pip install -r requirements-dev.txt")

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []


def require(condition, message):
    if not condition:
        ERRORS.append(message)


def load_yaml(path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        ERRORS.append("{}: {}".format(path.relative_to(ROOT), exc))
        return None


def main():
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    require(len(skills) == 24, "Expected 24 skills")
    helpers = sorted((ROOT / "skills").glob("*/*.py"))
    require(len(helpers) == 11, "Expected 11 runtime helpers")
    for path in skills:
        text = path.read_text(encoding="utf-8")
        label = str(path.relative_to(ROOT))
        parts = text.split("---", 2)
        require(text.startswith("---\n") and len(parts) == 3, label + ": missing frontmatter")
        if len(parts) != 3:
            continue
        try:
            meta = yaml.safe_load(parts[1])
        except yaml.YAMLError as exc:
            ERRORS.append(label + ": " + str(exc))
            continue
        if not isinstance(meta, dict):
            ERRORS.append(label + ": frontmatter must be a mapping")
            continue
        require(meta.get("name") == path.parent.name, label + ": name differs from directory")
        require(bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(meta.get("name", "")))), label + ": invalid name")
        desc = meta.get("description")
        require(isinstance(desc, str) and 0 < len(desc.strip()) <= 1024, label + ": invalid description")
        require("~/.claude" not in text and "/plugin install" not in text, label + ": Claude-only instruction")
        ui = load_yaml(path.parent / "agents" / "openai.yaml")
        if not isinstance(ui, dict):
            ERRORS.append(label + ": invalid OpenAI UI metadata")
            continue
        interface = ui.get("interface", {})
        require(isinstance(interface.get("display_name"), str), label + ": missing display name")
        summary = interface.get("short_description", "")
        require(isinstance(summary, str) and 25 <= len(summary) <= 64, label + ": UI summary must be 25-64 characters")
        require("$" + path.parent.name in interface.get("default_prompt", ""), label + ": prompt must mention skill")
        require(ui.get("policy", {}).get("allow_implicit_invocation", True) is True, label + ": unexpected explicit-only invocation")

    # Follow local Markdown resource links, including sibling skills, from the file's directory.
    pages = list((ROOT / "skills").rglob("*.md")) + [ROOT / "README.md"]
    pages += list((ROOT / "docs").glob("*.md")) + list((ROOT / "chatgpt").glob("*.md"))
    for path in pages:
        for link in re.findall(r"\]\(([^\s)]+)\)", path.read_text(encoding="utf-8")):
            if link.startswith(("https://", "http://", "#", "mailto:")):
                continue
            target = (path.parent / link.split("#")[0]).resolve()
            require(ROOT == target or ROOT in target.parents, str(path.relative_to(ROOT)) + ": link escapes package: " + link)
            require(target.exists(), str(path.relative_to(ROOT)) + ": missing resource: " + link)

    for path in list((ROOT / "skills").rglob("*.json")) + [ROOT / "plugin.json", ROOT / ".agents/plugins/marketplace.json"]:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            ERRORS.append(str(path.relative_to(ROOT)) + ": " + str(exc))
    try:
        plugin = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        require(plugin.get("name") == "youtube-agent-pro-openai", "Plugin identity mismatch")
        require(plugin.get("license") == "MIT", "Plugin license mismatch")
        require(bool(re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", ""))), "Plugin version must be semver")
        require(isinstance(plugin.get("extensions", {}).get("com.openai"), dict), "OpenAI extension missing")
    except (OSError, ValueError):
        pass
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    require("Copyright (c) 2026 Ahmed Sakri" in license_text, "Maintainer copyright missing")
    require("Copyright (c) 2026 Jake Schincariol" in license_text, "Required upstream copyright missing")
    require("The above copyright notice and this permission notice" in license_text, "MIT conditions missing")
    if ERRORS:
        print("\n".join(ERRORS), file=sys.stderr)
        return 1
    print("Validated 24 skills, 24 OpenAI metadata files, 11 helpers, manifests, licenses and local links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
