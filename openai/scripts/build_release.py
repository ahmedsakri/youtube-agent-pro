#!/usr/bin/env python3
"""Build reproducible Codex plugin and ChatGPT bundles from an explicit allowlist."""

import argparse
import hashlib
import io
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
import zipfile

from install import DistributionError, ROOT, SKILL_NAMES, read_source, reject_symlink_components, skill_payload


PLUGIN_NAME = "youtube-agent-pro-openai"
METADATA = (
    "plugin.json", "README.md", "LICENSE", "chatgpt/INSTRUCTIONS.md",
    "chatgpt/README.md", "docs/PORTING_NOTES.md", "docs/VALIDATION.md",
    ".agents/plugins/marketplace.json", "scripts/install.py", "scripts/build_release.py",
    "scripts/validate.py", "requirements-dev.txt", "AGENTS.md",
    "tests/test_distribution.py", "tests/test_tools.py",
)
OPTIONAL_METADATA = ("NOTICE", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md")
FIXED_DATE = (1980, 1, 1, 0, 0, 0)


def zip_bytes(files, prefix):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(files):
            info = zipfile.ZipInfo(prefix + "/" + name, date_time=FIXED_DATE)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, files[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return buffer.getvalue()


def rebase_links(text, directory):
    """Keep ordinary relative Markdown links usable after consolidating documents."""
    pattern = re.compile(r"(!?\[[^\]\n]*\]\()([^\s)]+)(\))")

    def replace(match):
        target = match.group(2)
        if target.startswith(("#", "/", "~")) or ":" in target:
            return match.group(0)
        parts = []
        for part in (PurePosixPath(directory) / target).parts:
            if part == "..":
                if parts:
                    parts.pop()
            elif part != ".":
                parts.append(part)
        return match.group(1) + "/".join(parts) + match.group(3)

    return pattern.sub(replace, text)


def workflows(payload):
    intro = (
        "# YouTube Agent Pro — portable workflows\n\n"
        "Generated from the canonical skills and shared operating guide. "
        "Use ChatGPT-INSTRUCTIONS.md (standalone release file), or INSTRUCTIONS.md "
        "inside the extracted ChatGPT bundle, as the entry point. These workflows do not add tools, "
        "connect a YouTube account, or grant publishing access. Helper execution requires "
        "an available Python environment and the companion bundle.\n\n"
        "## Shared operating guide\n\n"
    )
    guide = payload["yt/references/operating-guide.md"].decode("utf-8")
    sections = [intro + rebase_links(guide, "skills/yt/references")]
    for name in SKILL_NAMES:
        skill = payload[name + "/SKILL.md"].decode("utf-8")
        sections.append(
            "\n\n---\n\n## Workflow: {}\n\nCanonical source: `skills/{}/SKILL.md`. "
            "Relative command paths in this workflow are resolved from that skill's folder.\n\n{}".format(
                name, name, rebase_links(skill, "skills/" + name)
            )
        )
    sections.append(
        "\n\n---\n\n## YouTube metadata reference\n\nCanonical source: "
        "`skills/yt-seo/references/youtube-metadata.md`.\n\n" +
        rebase_links(payload["yt-seo/references/youtube-metadata.md"].decode("utf-8"), "skills/yt-seo/references")
    )
    sections.append(
        "\n\n---\n\n## Voice profile template\n\nCanonical source: "
        "`skills/yt-voice/assets/voice.md`. Copy only when the user requests a profile.\n\n" +
        payload["yt-voice/assets/voice.md"].decode("utf-8")
    )
    sections.append(
        "\n\n---\n\n## Hook formula library\n\nCanonical source: "
        "`skills/yt-script/hooks.json`.\n\n```json\n" +
        payload["yt-script/hooks.json"].decode("utf-8").rstrip() + "\n```\n"
    )
    return ("".join(sections).rstrip() + "\n").encode("utf-8")


def build(output_dir, root=ROOT):
    root = Path(root).resolve()
    payload = skill_payload(root)
    metadata = {name: read_source(root, name) for name in METADATA}
    for name in OPTIONAL_METADATA:
        if (root / name).exists() or (root / name).is_symlink():
            metadata[name] = read_source(root, name)
    plugin = dict(metadata)
    plugin.update({"skills/" + name: data for name, data in payload.items()})
    workflow_text = workflows(payload)
    instructions = metadata["chatgpt/INSTRUCTIONS.md"]
    chatgpt = {
        "INSTRUCTIONS.md": instructions,
        "WORKFLOWS.md": workflow_text,
        "README.md": metadata["chatgpt/README.md"],
        "LICENSE": metadata["LICENSE"],
    }
    chatgpt.update({"skills/" + name: data for name, data in payload.items()})
    outputs = {
        PLUGIN_NAME + "-plugin.zip": zip_bytes(plugin, PLUGIN_NAME),
        PLUGIN_NAME + "-chatgpt.zip": zip_bytes(chatgpt, PLUGIN_NAME + "-chatgpt"),
        "ChatGPT-INSTRUCTIONS.md": instructions,
        "ChatGPT-WORKFLOWS.md": workflow_text,
    }
    sums = ["{}  {}\n".format(hashlib.sha256(outputs[name]).hexdigest(), name) for name in sorted(outputs)]
    outputs["SHA256SUMS"] = "".join(sums).encode("ascii")
    output_dir = reject_symlink_components(Path(output_dir).expanduser())
    source_skills = root / "skills"
    if output_dir == source_skills or source_skills in output_dir.parents:
        raise DistributionError("Output directory must not overlap the source skills directory.")
    if output_dir.exists() and not output_dir.is_dir():
        raise DistributionError("Output path is not a directory: {}".format(output_dir))
    for name in outputs:
        target = reject_symlink_components(output_dir / name)
        if target.exists() and not target.is_file():
            raise DistributionError("Output artifact is not a file: {}".format(target))
    output_dir.mkdir(parents=True, exist_ok=True)
    # Replacing completed files also avoids following hard links or leaving half-written ZIPs.
    with tempfile.TemporaryDirectory(prefix=".youtube-agent-release-", dir=str(output_dir)) as staged:
        for name, data in outputs.items():
            (Path(staged) / name).write_bytes(data)
        for name in outputs:
            (Path(staged) / name).replace(output_dir / name)
    return [output_dir / name for name in sorted(outputs)]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist", help="Artifact directory (default: repository dist/)")
    args = parser.parse_args(argv)
    try:
        paths = build(args.output_dir)
    except (DistributionError, OSError, UnicodeError) as error:
        print("Release build stopped: {}".format(error), file=sys.stderr)
        return 1
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
