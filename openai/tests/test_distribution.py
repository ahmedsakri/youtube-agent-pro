"""Safety and completeness checks for the installable and portable distributions."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import install  # noqa: E402
import build_release  # noqa: E402


def snapshot(directory):
    return {
        path.relative_to(directory).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in directory.rglob("*") if path.is_file() and not path.is_symlink()
    }


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="youtube distribution ")
        self.base = Path(self.temporary.name).resolve()
        self.source = self.base / "source repo with spaces"
        self.destination = self.base / "project with spaces" / ".agents" / "skills"
        self.source.mkdir()
        for name in install.SKILL_NAMES:
            self.write("skills/" + name + "/SKILL.md", "---\nname: {}\ndescription: Test\n---\n[Guide](../yt/references/operating-guide.md)\n".format(name))
            self.write("skills/" + name + "/agents/openai.yaml", "interface:\n  display_name: {}\n".format(name))
        for helper in install.HELPERS:
            self.write("skills/" + helper, "print('helper')\n")
        self.write("skills/yt-script/hooks.json", "[]\n")
        self.write("skills/yt/references/operating-guide.md", "# Shared guide\n")
        self.write("skills/yt-voice/assets/voice.md", "# Blank voice template\n")
        self.write("skills/yt-seo/references/youtube-metadata.md", "# Official metadata reference\n")
        for relative in build_release.METADATA:
            self.write(relative, "Public document: " + relative + "\n")
        self.write("plugin.json", json.dumps({"name": build_release.PLUGIN_NAME}))
        self.write("LICENSE", "MIT License\nCopyright original contributor\n")
        self.write(".env", "PRIVATE_TOKEN=do-not-package")
        self.write(".git/config", "private repository setting")
        self.write(".youtube-agent/voice.md", "private creator voice")
        self.write("skills/yt/private.md", "private working note")
        self.write("skills/yt-script/__pycache__/secret.pyc", "private cache")
        self.write("skills/yt-script/.env", "private secret")
        self.before = snapshot(self.source)

    def tearDown(self):
        self.temporary.cleanup()

    def write(self, relative, text):
        path = self.source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_install_complete_pack_with_spaces_and_licenses(self):
        result = install.install(self.destination, root=self.source)
        self.assertEqual(result["count"], 24)
        self.assertEqual(set(path.name for path in self.destination.iterdir()), set(install.SKILL_NAMES))
        payload = install.skill_payload(self.source)
        for relative, data in payload.items():
            self.assertEqual((self.destination / relative).read_bytes(), data)
        for name in install.SKILL_NAMES:
            self.assertEqual((self.destination / name / "LICENSE").read_bytes(), (self.source / "LICENSE").read_bytes())
        self.assertEqual(snapshot(self.source), self.before)
        self.assertFalse((self.destination.parent.parent / ".youtube-agent").exists())
        self.assertFalse((self.destination / "yt" / "private.md").exists())

    def test_dry_run_has_no_side_effects(self):
        result = install.install(self.destination, dry_run=True, root=self.source)
        self.assertTrue(result["dry_run"])
        self.assertFalse(self.destination.parent.exists())
        self.assertEqual(snapshot(self.source), self.before)

    def test_conflict_refuses_before_installing_anything(self):
        old = self.destination / "yt-script"
        old.mkdir(parents=True)
        (old / "custom.md").write_text("keep")
        original = snapshot(self.destination)
        with self.assertRaisesRegex(install.DistributionError, "would be overwritten"):
            install.install(self.destination, root=self.source)
        self.assertEqual(snapshot(self.destination), original)
        self.assertEqual(list(self.destination.iterdir()), [old])

    def test_force_preserves_complete_existing_folders(self):
        old = self.destination / "yt-script" / "custom"
        old.mkdir(parents=True)
        (old / "user.txt").write_text("keep this exact personal file")
        unrelated = self.destination / "my-unrelated-skill"
        unrelated.mkdir()
        (unrelated / "SKILL.md").write_text("unrelated")
        result = install.install(self.destination, force=True, root=self.source)
        self.assertRegex(result["backup"].name, r"^\d{8}T\d{6}\.\d{6}Z-")
        self.assertEqual((result["backup"] / "yt-script" / "custom" / "user.txt").read_text(), "keep this exact personal file")
        self.assertEqual((unrelated / "SKILL.md").read_text(), "unrelated")
        self.assertFalse((self.destination / "yt-script" / "custom").exists())
        self.assertEqual(snapshot(self.source), self.before)

    def test_force_dry_run_preserves_existing_folder(self):
        (self.destination / "yt").mkdir(parents=True)
        before = snapshot(self.destination)
        result = install.install(self.destination, force=True, dry_run=True, root=self.source)
        self.assertEqual(result["conflicts"], ["yt"])
        self.assertEqual(snapshot(self.destination), before)
        self.assertFalse((self.destination / ".youtube-agent-backups").exists())

    def test_symlink_destination_is_rejected_even_with_force(self):
        victim = self.base / "untouched"
        victim.mkdir()
        self.destination.parent.mkdir(parents=True)
        self.destination.symlink_to(victim, target_is_directory=True)
        with self.assertRaisesRegex(install.DistributionError, "Symlink"):
            install.install(self.destination, force=True, root=self.source)
        self.assertEqual(list(victim.iterdir()), [])

    def test_symlink_ancestor_is_rejected(self):
        victim = self.base / "untouched"
        victim.mkdir()
        parent = self.base / "linked parent"
        parent.symlink_to(victim, target_is_directory=True)
        with self.assertRaisesRegex(install.DistributionError, "Symlink"):
            install.install(parent / "skills", root=self.source)
        self.assertEqual(list(victim.iterdir()), [])

    def test_symlink_existing_skill_is_rejected(self):
        self.destination.mkdir(parents=True)
        (self.destination / "yt").symlink_to(self.source / "skills" / "yt", target_is_directory=True)
        with self.assertRaisesRegex(install.DistributionError, "Symlink"):
            install.install(self.destination, force=True, root=self.source)
        self.assertEqual(snapshot(self.source), self.before)

    def test_symlink_inside_existing_skill_is_rejected(self):
        old = self.destination / "yt"
        old.mkdir(parents=True)
        (old / "private-link").symlink_to(self.source / ".env")
        with self.assertRaisesRegex(install.DistributionError, "contains a symlink"):
            install.install(self.destination, force=True, root=self.source)
        self.assertTrue((old / "private-link").is_symlink())

    def test_symlink_backup_folder_is_rejected(self):
        (self.destination / "yt").mkdir(parents=True)
        (self.destination / ".youtube-agent-backups").symlink_to(self.source, target_is_directory=True)
        with self.assertRaisesRegex(install.DistributionError, "Symlink"):
            install.install(self.destination, force=True, root=self.source)

    def test_source_symlink_is_rejected(self):
        helper = self.source / "skills" / install.HELPERS[0]
        helper.unlink()
        helper.symlink_to(self.source / ".env")
        with self.assertRaisesRegex(install.DistributionError, "Source contains a symlink"):
            install.install(self.destination, root=self.source)
        self.assertFalse(self.destination.exists())

    def test_missing_dependency_fails_before_writes(self):
        (self.source / "skills/yt/references/operating-guide.md").unlink()
        with self.assertRaisesRegex(install.DistributionError, "Required source file is missing"):
            install.install(self.destination, root=self.source)
        self.assertFalse(self.destination.exists())

    def test_install_failure_restores_previous_skills(self):
        original_rename = Path.rename
        for name in ("yt", "yt-analytics", "yt-audit"):
            (self.destination / name).mkdir(parents=True)
            (self.destination / name / "custom.txt").write_text(name)
        before = snapshot(self.destination)

        def fail_third_install(path, target):
            if path.name == "yt-audit" and path.parent.name.startswith(".youtube-agent-install-"):
                raise OSError("Simulated disk failure")
            return original_rename(path, target)

        with mock.patch.object(Path, "rename", fail_third_install):
            with self.assertRaisesRegex(OSError, "Simulated disk failure"):
                install.install(self.destination, force=True, root=self.source)
        self.assertEqual(snapshot(self.destination), before)
        self.assertFalse(any(path.name.startswith(".youtube-agent-install-") for path in self.destination.iterdir()))

    def test_source_skills_cannot_be_overwritten(self):
        with self.assertRaisesRegex(install.DistributionError, "overlap"):
            install.install(self.source / "skills", force=True, root=self.source)
        self.assertEqual(snapshot(self.source), self.before)

    def test_release_allowlist_completeness_and_determinism(self):
        one, two = self.base / "release one", self.base / "release two"
        paths = build_release.build(one, root=self.source)
        build_release.build(two, root=self.source)
        self.assertEqual(snapshot(one), snapshot(two))
        self.assertEqual(snapshot(self.source), self.before)
        self.assertEqual(len(paths), 5)
        payload = install.skill_payload(self.source)
        for flavor in ("plugin", "chatgpt"):
            prefix = build_release.PLUGIN_NAME + ("-chatgpt" if flavor == "chatgpt" else "") + "/"
            with zipfile.ZipFile(one / (build_release.PLUGIN_NAME + "-" + flavor + ".zip")) as archive:
                names = archive.namelist()
                self.assertEqual(names, sorted(names))
                self.assertEqual(len(names), len(set(names)))
                for name in names:
                    self.assertTrue(name.startswith(prefix))
                    self.assertNotIn("..", Path(name).parts)
                    self.assertFalse(any(part in (".git", ".env", "__pycache__", ".youtube-agent") for part in Path(name).parts))
                    self.assertNotIn("private.md", name)
                    self.assertEqual(archive.getinfo(name).date_time, build_release.FIXED_DATE)
                for relative, contents in payload.items():
                    self.assertEqual(archive.read(prefix + "skills/" + relative), contents)
                if flavor == "plugin":
                    self.assertEqual(set(names), {prefix + name for name in build_release.METADATA} | {prefix + "skills/" + name for name in payload})
                else:
                    self.assertEqual(archive.read(prefix + "INSTRUCTIONS.md"), (one / "ChatGPT-INSTRUCTIONS.md").read_bytes())
                    self.assertEqual(archive.read(prefix + "WORKFLOWS.md"), (one / "ChatGPT-WORKFLOWS.md").read_bytes())
        for line in (one / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ", 1)
            self.assertEqual(digest, hashlib.sha256((one / name).read_bytes()).hexdigest())
        consolidated = (one / "ChatGPT-WORKFLOWS.md").read_text()
        self.assertIn("ChatGPT-INSTRUCTIONS.md (standalone release file)", consolidated)
        self.assertIn("INSTRUCTIONS.md inside the extracted ChatGPT bundle", consolidated)
        self.assertEqual(consolidated.count("## Workflow: "), 24)
        self.assertIn("[Guide](skills/yt/references/operating-guide.md)", consolidated)
        self.assertIn("# Shared guide", consolidated)
        self.assertIn("# Blank voice template", consolidated)
        self.assertIn("## Hook formula library", consolidated)
        self.assertIn("# Official metadata reference", consolidated)

    def test_release_refuses_output_symlink(self):
        output = self.base / "release"
        output.mkdir()
        (output / "ChatGPT-INSTRUCTIONS.md").symlink_to(self.source / ".env")
        with self.assertRaisesRegex(install.DistributionError, "Symlink"):
            build_release.build(output, root=self.source)
        self.assertEqual(snapshot(self.source), self.before)
        self.assertEqual(len(list(output.iterdir())), 1)

    def test_release_does_not_write_through_output_hardlinks(self):
        output = self.base / "release"
        output.mkdir()
        os.link(self.source / ".env", output / "ChatGPT-INSTRUCTIONS.md")
        build_release.build(output, root=self.source)
        self.assertEqual(snapshot(self.source), self.before)
        self.assertNotEqual((output / "ChatGPT-INSTRUCTIONS.md").read_bytes(), (self.source / ".env").read_bytes())


class ActualPackTests(unittest.TestCase):
    def test_real_pack_is_complete_and_links_resolve(self):
        payload = install.skill_payload(REPO)
        self.assertEqual(len(install.SKILL_NAMES), 24)
        self.assertEqual(len(install.HELPERS), 11)
        for relative, content in payload.items():
            if not relative.endswith(".md"):
                continue
            for target in re.findall(r"!?\[[^\]\n]*\]\(([^\s)]+)\)", content.decode("utf-8")):
                if target.startswith(("#", "/", "~")) or ":" in target:
                    continue
                clean = target.split("#", 1)[0]
                path = (REPO / "skills" / relative).parent / clean
                self.assertTrue(path.is_file(), "Broken relative link in {}: {}".format(relative, target))
                packaged_path = path.resolve().relative_to(REPO / "skills").as_posix()
                self.assertIn(packaged_path, payload, "Linked resource omitted from distribution: " + packaged_path)
        consolidated = build_release.workflows(payload).decode("utf-8")
        for target in re.findall(r"!?\[[^\]\n]*\]\(([^\s)]+)\)", consolidated):
            if target.startswith(("#", "/", "~")) or ":" in target:
                continue
            clean = target.split("#", 1)[0]
            self.assertTrue(clean.startswith("skills/"), "Invalid consolidated workflow link: " + target)
            self.assertIn(clean[len("skills/"):], payload, "Consolidated link missing from distribution: " + target)

    def test_cli_help_is_available_without_dependencies(self):
        for name in ("install.py", "build_release.py"):
            result = subprocess.run([sys.executable, str(REPO / "scripts" / name), "--help"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("usage:", result.stdout)


if __name__ == "__main__":
    unittest.main()
