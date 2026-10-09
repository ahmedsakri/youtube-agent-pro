"""Behavioral integration tests: stdlib only; execute the shipped CLIs out of tree."""
import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = {
    "analytics": "yt-analytics/funnel.py", "chapters": "yt-chapters/chapters.py",
    "edit": "yt-edit/deadair.py", "idea": "yt-idea/ideascore.py",
    "package": "yt-package/title.py", "retention": "yt-retention/retention.py",
    "script": "yt-script/hookscore.py", "sponsor": "yt-sponsor/ratecard.py",
    "thumbnail": "yt-thumbnail/thumblint.py", "viral": "yt-viral/swipe.py",
    "voice": "yt-voice/voiceprint.py",
}


class ToolIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="YouTube tools test ")
        cls.home = Path(cls.temp.name)
        cls.skills = cls.home / "installed skills with spaces"
        shutil.copytree(ROOT / "skills", cls.skills)
        cls.cwd = cls.home / "unrelated working directory"
        cls.cwd.mkdir()
        cls.inputs = cls.home / "input media with spaces"
        cls.inputs.mkdir()

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def write(self, name, data):
        path = self.inputs / name
        path.write_text(data, encoding="utf-8")
        return path

    def csv(self, name, rows):
        path = self.inputs / name
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            csv.writer(handle).writerows(rows)
        return path

    def invoke(self, tool, *args, success=True, as_json=True):
        command = [sys.executable, str(self.skills / TOOLS[tool]), *map(str, args)]
        if as_json:
            command.append("--json")
        result = subprocess.run(command, cwd=self.cwd, capture_output=True, text=True, timeout=15)
        if not success:
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertNotIn("Traceback", result.stderr)
            return result
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        return json.loads(result.stdout) if as_json else result.stdout

    def transcript(self, extension="srt"):
        texts = ["Camera lenses control focal distance.", "Compare primes and zoom lenses.",
                 "Lighting changes facial contrast.", "Bounce light from a reflector.",
                 "Microphone placement reduces room noise.", "Record quiet audio before editing.",
                 "Editing connects each camera shot.", "Export the finished video for review."]
        segments = [{"start": index * 15, "end": index * 15 + 12, "text": text} for index, text in enumerate(texts)]
        if extension == "json":
            return self.write("spoken segments.json", json.dumps({"segments": segments}))
        body = "WEBVTT\n\n" if extension == "vtt" else ""
        for index, segment in enumerate(segments):
            def ts(seconds):
                return f"00:{seconds // 60:02d}:{seconds % 60:02d}" + (".000" if extension == "vtt" else ",000")
            body += f"{index+1}\n{ts(segment['start'])} --> {ts(segment['end'])}\n{segment['text']}\n\n"
        return self.write("camera transcript." + extension, body)

    def test_every_tool_help_and_missing_arguments(self):
        for tool in TOOLS:
            with self.subTest(tool=tool):
                self.assertIn("usage:", self.invoke(tool, "--help", as_json=False).lower())
                self.invoke(tool, success=False)

    def test_hooks_rank_and_resolve_adjacent_formula_data(self):
        path = self.write("hook choices.txt", "Hey guys welcome to another amazing video\nYou waste 3 hours every week because of this one mistake\n")
        rows = self.invoke("script", path)
        self.assertEqual(len(rows), 2)
        self.assertGreater(rows[0]["verdict"], rows[1]["verdict"])
        self.assertEqual(set(rows[0]["properties"]), {"SPECIFICITY", "ADDRESS", "STAKES", "CURIOSITY", "BREVITY"})
        one = self.invoke("script", "--hook", rows[0]["hook"])
        self.assertEqual(one[0]["verdict"], rows[0]["verdict"])

    def test_ideas_rank_specific_queries(self):
        path = self.write("idea choices.txt", "Amazing stuff for everyone\nHow to fix 3 camera lighting mistakes for beginners\n")
        rows = self.invoke("idea", path)
        self.assertEqual(len(rows), 2)
        self.assertGreater(rows[0]["axes"]["SEARCH"], rows[1]["axes"]["SEARCH"])
        self.assertGreater(rows[0]["verdict"], rows[1]["verdict"])
        self.assertEqual(self.invoke("idea", "--idea", rows[0]["idea"])[0], rows[0])

    def test_title_limit_and_actual_pairing_duplication(self):
        row = self.invoke("package", "--title", "3 Camera Mistakes Cost You Sharp Photos", "--thumb", "Camera Mistakes")[0]
        self.assertIn("duplicate", dict(row["issues"]))
        long = self.invoke("package", "--title", "Camera " * 20)[0]
        self.assertGreater(long["chars"], 100)
        self.assertIn("length", dict(long["issues"]))
        path = self.write("titles to rank.txt", row["title"] + "\n" + "Camera " * 20)
        self.assertEqual(len(self.invoke("package", path)), 2)

    def test_thumbnail_measures_concept_not_image(self):
        row = self.invoke("thumbnail", "--concept", 'shocked face, camera, lens, arrow, "FIX YOUR CAMERA TODAY"', "--title", "Fix Your Camera")[0]
        self.assertGreater(row["elements"], 3)
        self.assertTrue({"elements", "text", "duplicate"}.issubset(dict(row["issues"])))
        path = self.write("thumbnail ideas.txt", 'shocked face, "ONE CHANGE"\nface, arrow, camera, lens, text\n')
        rows = self.invoke("thumbnail", path)
        self.assertGreaterEqual(rows[0]["score"], rows[1]["score"])

    def test_text_clis_reject_missing_and_empty_inputs(self):
        for tool, flag in (("script", "--hook"), ("idea", "--idea"), ("package", "--title"), ("thumbnail", "--concept")):
            with self.subTest(tool=tool):
                self.invoke(tool, flag, "   ", success=False)
                self.invoke(tool, self.inputs / "missing input.txt", success=False)
                self.invoke(tool, flag, success=False)

    def test_funnel_csv_does_not_use_avd_as_video_length(self):
        path = self.csv("studio without runtime.csv", [["Video title", "Average view duration", "Impressions click-through rate (%)", "Impressions", "Views"], ["Camera tutorial", "0:30", "5.5", "12,000", "900"]])
        result = self.invoke("analytics", path)
        self.assertEqual(result["impressions"], 12000)
        self.assertEqual(result["ctr"], 5.5)
        self.assertIsNone(result["length_s"])
        self.assertIsNone(result["avg_pct_viewed"])
        self.assertEqual(result["status"], "partial_data")
        self.assertEqual(result["label"], "Camera tutorial")

    def test_funnel_zero_metrics_and_partial_missing(self):
        result = self.invoke("analytics", "--impressions", 0, "--ctr", 0, "--avd", 0, "--length", 30)
        self.assertEqual(result["avg_pct_viewed"], 0)
        self.assertEqual(result["estimated_views_from_impressions"], 0)
        self.assertEqual(result["status"], "review")
        result = self.invoke("analytics", "--views", 100)
        self.assertEqual(result["status"], "insufficient_data")
        self.assertIsNone(result["binding_constraint"])

    def test_funnel_shorts_avoid_long_form_thresholds(self):
        result = self.invoke("analytics", "--format", "shorts", "--impressions", 30, "--ctr", 1, "--avd", 36, "--length", 30, "--views", 1000)
        self.assertEqual(result["avg_pct_viewed"], 120)
        self.assertEqual(result["links"], [])
        self.assertIsNone(result["binding_constraint"])
        self.assertEqual(result["status"], "shorts_requires_context")
        self.assertEqual(result["views"], 1000)
        self.assertEqual(result["missing_metrics"], [])
        self.assertIn("engaged_views", result["context_required"])

    def test_funnel_valid_runtime_and_estimate_scope(self):
        result = self.invoke("analytics", "--impressions", 10000, "--ctr", "5%", "--avd", "2:30", "--length", "10:00")
        self.assertEqual(result["avg_pct_viewed"], 25)
        self.assertEqual(result["binding_constraint"], "RETENTION")
        self.assertEqual(result["estimated_views_from_impressions"], 500)
        self.assertIsNone(result["views"])
        self.assertGreaterEqual(len(result["warnings"]), 2)

    def test_funnel_empty_csv_errors_without_index_traceback(self):
        self.invoke("analytics", self.csv("empty.csv", [["Impressions", "Views"]]), success=False)
        result = self.invoke("analytics", self.csv("no metrics.csv", [["Video title"], ["Unknown"]]))
        self.assertEqual(result["status"], "insufficient_data")

    def test_funnel_rejects_invalid_numbers(self):
        for flag, value in (("--ctr", 101), ("--ctr", -1), ("--impressions", "NaN"), ("--avd", "inf"), ("--length", 0), ("--avd", "2:99")):
            with self.subTest(flag=flag, value=value):
                self.invoke("analytics", flag, value, success=False)

    def test_short_seconds_retention_not_misread_as_percent(self):
        path = self.csv("short retention seconds.csv", [["Elapsed seconds", "Audience retention (%)"], *[(i * 5, 100 - i * 5) for i in range(9)]])
        result = self.invoke("retention", path, "--hook-seconds", 10)
        self.assertEqual(result["axis"], "seconds")
        self.assertEqual(result["hook_leak"], 10)
        self.assertEqual(result["hook_window_seconds"], 10)
        self.assertTrue(all(c["at_seconds"] == c["from"] for c in result["cliffs"]))

    def test_retention_percent_axis_and_transcript_link(self):
        path = self.csv("retention percent.csv", [["Video position (%)", "Audience retention (%)"], *[(i * 10, 110 - i * 5) for i in range(11)]])
        result = self.invoke("retention", path, "--duration", 100, "--hook-seconds", 30, "--transcript", self.transcript())
        self.assertEqual(result["start"], 110)
        self.assertEqual(result["hook_leak"], 15)
        self.assertEqual(result["hook_window"], 30)
        self.assertTrue(result["said"])

    def test_retention_fraction_api_headers_are_normalized(self):
        path = self.csv("api retention ratios.csv", [["elapsedVideoTimeRatio", "audienceWatchRatio"], *[(i / 10, 1.1 - i * .05) for i in range(11)]])
        result = self.invoke("retention", path, "--duration", 100)
        self.assertEqual(result["axis"], "percent")
        self.assertAlmostEqual(result["start"], 110)
        self.assertAlmostEqual(result["end"], 60)

    def test_retention_units_must_be_known(self):
        path = self.csv("unitless retention.csv", [[i * 5, 100 - i] for i in range(9)])
        self.invoke("retention", path, success=False)
        result = self.invoke("retention", path, "--axis", "seconds")
        self.assertEqual(result["axis"], "seconds")

    def test_retention_invalid_data_and_zero_start(self):
        path = self.csv("zero retention.csv", [["Seconds", "Retention %"], *[(i, 0) for i in range(9)]])
        result = self.invoke("retention", path)
        self.assertEqual(result["start"], 0)
        self.assertEqual(result["hook_leak"], 0)
        for value in ("NaN", -1, "inf"):
            self.invoke("retention", path, "--duration", value, success=False)
        duplicate = self.csv("duplicate positions.csv", [["Seconds", "Retention %"], *[(0, 100) for _ in range(9)]])
        self.invoke("retention", duplicate, success=False)

    def test_edit_srt_vtt_whisper_parse_consistently(self):
        results = [self.invoke("edit", self.transcript(ext), "--floor", .4) for ext in ("srt", "vtt", "json")]
        for result in results:
            self.assertEqual(result["duration"], 117)
            self.assertEqual(len(result["cuts"]), 7)
            self.assertAlmostEqual(result["removed"], 18.2)
            self.assertEqual({c["kind"] for c in result["cuts"]}, {"DEAD"})
            self.assertAlmostEqual(result["out"], 98.8)

    def test_edit_whisper_list_and_overlap_removed_once(self):
        rows = [{"start": start, "end": start + 10, "text": "Here are the five camera settings to adjust."} for start in (0, 2, 4)]
        path = self.write("overlapping retakes.json", json.dumps(rows))
        result = self.invoke("edit", path)
        self.assertEqual(len(result["cuts"]), 2)
        self.assertEqual(result["removed"], 12)
        self.assertEqual(result["out"], 2)

    def test_edit_retakes_skip_filler_and_validate_timestamps(self):
        rows = [{"start": 0, "end": 2, "text": "This is how you change the camera settings."}, {"start": 2, "end": 3, "text": "um"}, {"start": 3, "end": 5, "text": "This is how you change the camera settings correctly."}]
        path = self.write("filler and retake.json", json.dumps(rows))
        result = self.invoke("edit", path)
        self.assertEqual({c["kind"] for c in result["cuts"]}, {"FILLER", "REPEAT"})
        self.assertEqual(result["removed"], 3)
        for floor in (-1, "NaN", "inf"):
            self.invoke("edit", path, "--floor", floor, success=False)
        bad = self.write("invalid timestamps.json", json.dumps([{"start": 3, "end": 2, "text": "Hi"}]))
        self.invoke("edit", bad, success=False)

    def test_overlapping_cues_do_not_invent_silence(self):
        rows = [{"start": 0, "end": 10, "text": "The long narrator sentence."},
                {"start": 2, "end": 3, "text": "Other voice."},
                {"start": 5, "end": 6, "text": "More overlap."}]
        path = self.write("overlapping voices.JSON", json.dumps(rows))
        result = self.invoke("edit", path)
        self.assertEqual(result["duration"], 10)
        self.assertEqual(result["removed"], 0)
        self.assertEqual(result["cuts"], [])

    def test_chapters_constraints_and_shared_parser(self):
        for ext in ("srt", "vtt", "json"):
            result = self.invoke("chapters", self.transcript(ext), "--target", 5)
            self.assertTrue(result["valid"])
            self.assertEqual(len(result["chapters"]), 5)
            self.assertEqual(result["chapters"][0]["start"], 0)
            self.assertTrue(all(c["seconds"] >= 10 for c in result["chapters"]))
        self.invoke("chapters", self.transcript(), "--target", -1, success=False)

    def test_chapters_too_short_has_invalid_result(self):
        path = self.write("short chapter transcript.json", json.dumps([{"start": i * 2, "end": i * 2 + 1, "text": "One short sentence"} for i in range(8)]))
        result = self.invoke("chapters", path)
        self.assertFalse(result["valid"])

    def test_swipe_own_channel_median_and_minimum_sample(self):
        rows = [{"channel": "Camera School", "views": views, "title": "I tested 5 cameras", "url": f"https://example.com/{views}"} for views in (100, 200, 300, 1000)]
        rows.append({"channel": "Thin channel", "views": 9999999, "title": "Big hit"})
        result = self.invoke("viral", self.write("collected videos.json", json.dumps(rows)), "--min", 2)
        self.assertEqual(len(result["outliers"]), 1)
        self.assertEqual(result["outliers"][0]["median"], 250)
        self.assertEqual(result["outliers"][0]["multiple"], 4)
        self.assertEqual(result["skipped_thin_channels"], [["Thin channel", 1]])

    def test_swipe_missing_views_do_not_become_zero(self):
        rows = [{"channel": "Camera School", "views": views, "title": "Camera"} for views in (100, 200, 300)] + [{"channel": "Camera School", "title": "Unknown"}]
        result = self.invoke("viral", self.write("missing views.json", json.dumps({"videos": rows})))
        self.assertEqual(result["skipped_invalid_rows"], [3])
        self.assertEqual(result["skipped_thin_channels"], [["Camera School", 3]])
        self.assertEqual(result["outliers"], [])

    def test_swipe_zero_median_and_nonfinite_views(self):
        rows = [{"channel": "Zero", "views": 0, "title": "Camera"} for _ in range(4)] + [{"channel": "Zero", "views": "NaN"}]
        path = self.write("zero views.json", json.dumps(rows))
        result = self.invoke("viral", path)
        self.assertEqual(result["skipped_zero_median_channels"], ["Zero"])
        self.assertEqual(result["skipped_invalid_rows"], [4])
        self.invoke("viral", path, "--min", -1, success=False)

    def test_sponsor_currency_and_placement_math(self):
        rows = self.invoke("sponsor", "--views", 12000, "--niche", "tech", "--placement", "all")
        self.assertEqual([row["mid"] for row in rows], [144, 360, 792])
        self.assertEqual({row["currency"] for row in rows}, {"USD"})
        self.assertTrue(all(row["low"] <= row["mid"] <= row["high"] for row in rows))
        for value in (-1, "NaN", "inf"):
            self.invoke("sponsor", "--views", value, success=False)
        self.invoke("sponsor", "--views", 100, "--placement", "unknown", success=False)

    def test_voice_counts_transcript_without_srt_timestamps(self):
        srt = self.transcript()
        result = self.invoke("voice", srt)
        self.assertGreater(result["words"], 35)
        self.assertEqual(result["sentences"], 8)
        self.assertIn("camera", result["signature_words"])
        text = self.write("voice sample.txt", "You know, cameras matter. Basically this camera is amazing!")
        merged = self.invoke("voice", srt, text)
        self.assertGreater(merged["words"], result["words"])
        self.assertGreater(merged["filler_rate_pct"], result["filler_rate_pct"])
        self.assertIn("amazing", merged["hype_words_you_already_use"])
        self.invoke("voice", self.write("blank voice.txt", "  \n"), success=False)
        self.invoke("voice", srt, self.inputs / "missing voice.txt", success=False)


if __name__ == "__main__":
    unittest.main()
