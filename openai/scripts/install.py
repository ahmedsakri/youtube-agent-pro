#!/usr/bin/env python3
"""Install the complete YouTube Agent Pro skill pack without third-party packages."""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAMES = (
    "yt", "yt-analytics", "yt-audit", "yt-brief", "yt-chapters", "yt-collab",
    "yt-comment", "yt-edit", "yt-endscreen", "yt-funnel", "yt-idea",
    "yt-package", "yt-plan", "yt-repurpose", "yt-retention", "yt-script",
    "yt-seo", "yt-series", "yt-shorts", "yt-sponsor", "yt-thumbnail",
    "yt-trend", "yt-viral", "yt-voice",
)
HELPERS = (
    "yt-analytics/funnel.py", "yt-chapters/chapters.py", "yt-edit/deadair.py",
    "yt-idea/ideascore.py", "yt-package/title.py", "yt-retention/retention.py",
    "yt-script/hookscore.py", "yt-sponsor/ratecard.py",
    "yt-thumbnail/thumblint.py", "yt-viral/swipe.py", "yt-voice/voiceprint.py",
)
RESOURCES = (
    "yt-script/hooks.json", "yt/references/operating-guide.md",
    "yt-voice/assets/voice.md", "yt-seo/references/youtube-metadata.md",
)


class DistributionError(Exception):
    """A safe, actionable distribution failure."""


def reject_symlink_components(path):
    """Check the lexical path before resolving it or creating directories."""
    path = Path(os.path.abspath(str(path)))
    for component in reversed((path,) + tuple(path.parents)):
        if component.is_symlink():
            raise DistributionError("Symlink paths are not supported: {}".format(component))
    return path


def read_source(root, relative):
    root = Path(root).resolve()
    path = root / relative
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != root and root in parent.parents):
        raise DistributionError("Source contains a symlink: {}".format(relative))
    if not path.is_file():
        raise DistributionError("Required source file is missing: {}".format(relative))
    return path.read_bytes()


def skill_payload(root=ROOT):
    """An explicit allowlist; never include caches, secrets, or user profiles."""
    payload = {}
    for name in SKILL_NAMES:
        for filename in ("SKILL.md", "agents/openai.yaml"):
            relative = "{}/{}".format(name, filename)
            payload[relative] = read_source(root, "skills/" + relative)
    for relative in HELPERS + RESOURCES:
        payload[relative] = read_source(root, "skills/" + relative)
    license_text = read_source(root, "LICENSE")
    for name in SKILL_NAMES:
        payload[name + "/LICENSE"] = license_text
    return payload


def reject_tree_symlinks(path):
    for current, directories, files in os.walk(str(path), followlinks=False):
        for name in directories + files:
            candidate = Path(current) / name
            if candidate.is_symlink():
                raise DistributionError("Existing skill contains a symlink: {}".format(candidate))


def install(destination, dry_run=False, force=False, root=ROOT):
    """Stage all skills first, then install; retain overwritten folders as backups."""
    payload = skill_payload(root)
    destination = reject_symlink_components(Path(destination).expanduser())
    source_skills = (Path(root).resolve() / "skills")
    if destination == source_skills or source_skills in destination.parents:
        raise DistributionError("Destination must not overlap the source skills directory.")
    if destination.exists() and not destination.is_dir():
        raise DistributionError("Destination must be a directory: {}".format(destination))
    conflicts = []
    for name in SKILL_NAMES:
        target = reject_symlink_components(destination / name)
        if target.exists():
            if not target.is_dir():
                raise DistributionError("Existing skill is not a directory: {}".format(target))
            reject_tree_symlinks(target)
            conflicts.append(name)
    if conflicts and not force:
        raise DistributionError(
            "Existing skills would be overwritten: {}. Choose another --dest, or use "
            "--force to preserve these folders in a timestamped backup.".format(", ".join(conflicts))
        )
    if conflicts:
        reject_symlink_components(destination / ".youtube-agent-backups")
    if dry_run:
        return {"destination": destination, "count": len(SKILL_NAMES), "conflicts": conflicts, "backup": None, "dry_run": True}

    destination.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".youtube-agent-install-", dir=str(destination)))
    backup = None
    installed = []
    moved = []
    try:
        for relative, contents in payload.items():
            output = stage / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(contents)
        if conflicts:
            backup_parent = destination / ".youtube-agent-backups"
            backup_parent.mkdir(exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ-")
            backup = Path(tempfile.mkdtemp(prefix=stamp, dir=str(backup_parent)))
        for name in SKILL_NAMES:
            target = reject_symlink_components(destination / name)
            # Detect a new conflict that appeared since the initial preflight.
            if name not in conflicts and target.exists():
                raise DistributionError("Destination changed during installation: {}".format(target))
            if name in conflicts:
                reject_tree_symlinks(target)
                target.rename(backup / name)
                moved.append(name)
            (stage / name).rename(target)
            installed.append(name)
    except Exception:
        for name in reversed(installed):
            shutil.rmtree(str(destination / name))
        for name in reversed(moved):
            (backup / name).rename(destination / name)
        if backup is not None and not any(backup.iterdir()):
            backup.rmdir()
        raise
    finally:
        shutil.rmtree(str(stage))
    return {"destination": destination, "count": len(SKILL_NAMES), "conflicts": conflicts, "backup": backup, "dry_run": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, default=Path.home() / ".agents" / "skills", help="Skill directory (default: ~/.agents/skills)")
    parser.add_argument("--dry-run", action="store_true", help="Validate and show the plan without writing files")
    parser.add_argument("--force", action="store_true", help="Back up existing skill folders before replacing them")
    args = parser.parse_args(argv)
    try:
        result = install(args.dest, dry_run=args.dry_run, force=args.force)
    except (DistributionError, OSError) as error:
        print("Installation stopped: {}".format(error), file=sys.stderr)
        return 1
    action = "Would install" if result["dry_run"] else "Installed"
    print("{} all {} skills in {}".format(action, result["count"], result["destination"]))
    if result["conflicts"]:
        print("Existing skill folders preserved {}.".format("in " + str(result["backup"]) if result["backup"] else "in a timestamped backup when installed"))
    print("No channel voice profile or global agent configuration was created or changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
