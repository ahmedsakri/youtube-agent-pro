#!/usr/bin/env python3
"""Build the two edition guides. Requires reportlab for documentation only.

Run from any directory: python3 docs/build_guides.py
The runtime skills and their helpers do not depend on ReportLab.
"""

from pathlib import Path
import argparse

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/ahmedsakri/youtube-agent-pro"
W, H = 612, 792
M, CW = 48, 516
INK = colors.HexColor("#172322")
MUTED = colors.HexColor("#596864")
PAPER = colors.HexColor("#FAFAF7")
RULE = colors.HexColor("#DDE3DD")


class Guide:
    def __init__(self, path, edition, accent, tint):
        self.path, self.edition = path, edition
        self.accent, self.tint = colors.HexColor(accent), colors.HexColor(tint)
        self.c = canvas.Canvas(str(path), pagesize=(W, H), pageCompression=1,
                               invariant=1)
        self.c.setTitle("YouTube Agent Pro | " + edition + " Guide")
        self.c.setAuthor("Ahmed Sakri")
        self.c.setSubject("Installation, workflows and capability boundaries")
        self.page = 0
        self.y = 0

    def new(self, eyebrow, title, subtitle):
        if self.page:
            self.finish_page()
            self.c.showPage()
        self.page += 1
        c = self.c
        c.setFillColor(PAPER)
        c.rect(0, 0, W, H, stroke=0, fill=1)
        c.setFillColor(self.accent)
        c.rect(M, H-45, 28, 5, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(M+38, H-46, "YOUTUBE AGENT PRO")
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 9)
        c.drawRightString(W-M, H-46, self.edition.upper())
        self.y = 704
        self.p(eyebrow.upper(), 9, 12, bold=True, color=self.accent, after=8)
        self.p(title, 30, 33, bold=True, after=12)
        self.p(subtitle, 11, 16, color=MUTED, after=22)

    def p(self, text, size=10.5, leading=15, bold=False, color=INK, after=8,
          x=M, width=CW):
        style = ParagraphStyle("p", fontName="Helvetica-Bold" if bold else "Helvetica",
                               fontSize=size, leading=leading, textColor=color,
                               splitLongWords=False)
        para = Paragraph(text, style)
        _, h = para.wrap(width, H)
        if self.y-h < 64:
            raise ValueError("Page overflow: {} page {}: {}".format(self.edition, self.page, text[:70]))
        para.drawOn(self.c, x, self.y-h)
        self.y -= h+after

    def section(self, number, title):
        self.y -= 5
        self.p(number + "  /  " + title, 13, 17, True, self.accent, after=9)

    def code(self, lines, after=14):
        rows = lines.splitlines()
        size, leading, pad = 8.9, 13.5, 12
        for row in rows:
            if self.c.stringWidth(row, "Courier", size) > CW-2*pad:
                raise ValueError("Code line too long: " + row)
        h = leading*len(rows)+2*pad
        if self.y-h < 64:
            raise ValueError("Code overflows page")
        self.c.setFillColor(self.tint)
        self.c.roundRect(M, self.y-h, CW, h, 7, stroke=0, fill=1)
        self.c.setFillColor(INK)
        self.c.setFont("Courier", size)
        baseline = self.y-pad-9
        for row in rows:
            self.c.drawString(M+pad, baseline, row)
            baseline -= leading
        self.y -= h+after

    def note(self, title, text):
        style = ParagraphStyle("note", fontName="Helvetica", fontSize=10.2,
                               leading=14.5, textColor=INK)
        para = Paragraph("<b>" + title + "</b><br/>" + text, style)
        _, h = para.wrap(CW-28, H)
        if self.y-h-24 < 64:
            raise ValueError("Note overflows page")
        self.c.setFillColor(self.tint)
        self.c.roundRect(M, self.y-h-24, CW, h+24, 7, stroke=0, fill=1)
        self.c.setFillColor(self.accent)
        self.c.rect(M, self.y-h-24, 3, h+24, stroke=0, fill=1)
        para.drawOn(self.c, M+14, self.y-h-12)
        self.y -= h+38

    def rows(self, items):
        for label, body in items:
            self.p(label, 10.7, 14, True, after=2)
            self.p(body, 10.1, 14.1, color=MUTED, after=11)

    def finish_page(self):
        c = self.c
        c.setStrokeColor(RULE)
        c.setLineWidth(.7)
        c.line(M, 49, W-M, 49)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(M, 32, "One repository. Two editions.  |  October 2026")
        c.drawRightString(W-M, 32, "{:02d} / 04".format(self.page))

    def save(self):
        self.finish_page()
        if self.page != 4:
            raise ValueError("Each guide must contain exactly four pages")
        self.c.save()


def workflow_map(g, prefix):
    def names(*items):
        return "  |  ".join(prefix + i for i in items)
    g.rows([
        ("Start and find direction", names("yt", "yt-voice", "yt-idea", "yt-trend") +
         "<br/>Route a request, define creator voice, evaluate ideas and plan a calendar."),
        ("Write and prepare production", names("yt-script", "yt-brief", "yt-edit", "yt-chapters") +
         "<br/>Hooks, spoken scripts, shot lists, transcript edit decisions and chapters."),
        ("Package the video", names("yt-package", "yt-thumbnail", "yt-seo") +
         "<br/>Title/thumbnail pairings, visual concepts, descriptions and search intent."),
        ("Read performance", names("yt-analytics", "yt-retention", "yt-audit", "yt-funnel") +
         "<br/>Interpret exports and retention, prioritize fixes and review channel conversion."),
        ("Plan and reuse", names("yt-shorts", "yt-repurpose", "yt-series", "yt-plan", "yt-endscreen") +
         "<br/>Clip plans, platform drafts, series structure, capacity and next-video routing."),
        ("Research and business", names("yt-viral", "yt-collab", "yt-sponsor", "yt-comment") +
         "<br/>Outlier comparisons, outreach drafts, sponsorship scenarios and comment replies."),
    ])


def claude(output):
    g = Guide(output, "Claude", "#A64B30", "#F4E7DE")
    g.new("01 / Start here", "A creator workflow\nfor Claude".replace("\n", "<br/>"),
          "Install the Claude edition from the shared repository. Use 24 workflows and 11 local helpers to turn source material into useful drafts and analysis.")
    g.section("1", "Install in Claude Code")
    g.p("Use a Claude Code client with plugin support. The plugin code is MIT-licensed; your Claude access, usage limits and available tools still apply.")
    g.code("/plugin marketplace add ahmedsakri/youtube-agent-pro\n/plugin install youtube-agent-pro")
    g.p("Plugin skills use namespaced commands: <b>/youtube-agent-pro:yt</b> and <b>/youtube-agent-pro:yt-script</b>. The shorter <b>/yt</b> form is for skills copied manually into Claude's skill directory.", after=10)
    g.section("2", "Add your creator voice, if useful")
    g.p("Your supplied context comes first. Optionally run <b>/youtube-agent-pro:yt-voice</b> with your own transcripts or a short interview. The default local profile is <b>~/.claude/youtube/voice.md</b>. A missing profile does not block scripts, analytics or other work that can proceed from your request.")
    g.section("3", "Ask for a concrete deliverable")
    g.code('/youtube-agent-pro:yt-script Write a 45-second English Short\nfrom this outline. Give me three opening-line options.')
    g.note("What you receive", "Scripts, plans, copy and analysis. The pack itself does not upload, schedule, edit footage or render video. Review its output before you use it.")
    g.new("02 / Choose the workflow", "The 24-command map", "These are the manual-install command names. For the plugin, add its namespace: /yt becomes /youtube-agent-pro:yt. Start with the hub when the next step is unclear.")
    workflow_map(g, "/")
    g.note("Metadata should follow the content", "Use yt-seo for a natural title and description that match the video and viewer's likely search. Tags have a limited role; include relevant spelling variants when useful. Hashtags are optional. No keyword list guarantees distribution or trending status.")
    g.new("03 / Put it to work", "Work from your evidence", "Give the workflow your audience, format, language and constraints. A timestamped transcript is more useful than a video URL alone. These examples use the plugin commands.")
    g.section("1", "Extract Shorts from an existing video")
    g.code('/youtube-agent-pro:yt-shorts Find three 30-45 second clips.\nPreserve transcript timecodes. Label any new opening line\nas a suggested recording, not words already in the video.')
    g.section("2", "Write relevant search metadata")
    g.code('/youtube-agent-pro:yt-seo Draft a title and description for\nthis phone-camera test. Use accurate search phrases naturally.\nPut the main topic early. Add only relevant tags; no hashtags\nare needed. Do not claim a result the script does not show.')
    g.section("3", "Diagnose with data")
    g.code('/youtube-agent-pro:yt-analytics Compare these exports with\nsimilar videos at the same age. Separate Shorts-feed metrics\nfrom long-form CTR. Give one experiment and the uncertainty.')
    g.section("4", "Run a helper yourself")
    g.p("From the cloned repository root, with Python 3 available:")
    g.code('python3 skills/yt-script/hookscore.py --hook "I tried three cameras" --json')
    g.p("All eleven helpers use the Python standard library and make no network requests. Scores are editing heuristics, not measurements of future views.", 10, 14, color=MUTED)
    g.new("04 / Use with confidence", "Setup checks<br/>and honest limits", "Keep the source files, protect your channel data and separate a useful recommendation from a verified result.")
    g.section("1", "Manual installation alternative")
    g.p("If plugin installation is unavailable, clone the shared repository and copy its root <b>skills/yt*</b> folders into <b>~/.claude/skills/</b>, or into a project's <b>.claude/skills/</b>. Keep all sibling folders together. Check existing names before copying; do not overwrite your own skills blindly.")
    g.section("2", "Troubleshoot the common failures")
    g.rows([
        ("The command is missing", "Reopen Claude Code and inspect the installed plugin. Use /youtube-agent-pro:yt for the plugin or /yt for a manually copied skill."),
        ("The writing does not sound like you", "Supply audience, language and style examples in your request, or ask yt-voice to create an optional profile at ~/.claude/youtube/voice.md. You can continue without that file."),
        ("A helper cannot find its inputs", "Run it from its skill directory, or pass its full path and an absolute input-file path. Keep hooks.json and the sibling skill folders in place."),
        ("Using a plain Claude chat instead", "Paste the relevant SKILL.md plus your source material and voice context. A plain chat does not automatically gain local file access or Python execution. Ask for qualitative analysis if the helper cannot run."),
    ])
    g.note("The boundaries", "Thumbnail output is a concept until a separate image tool creates an asset. Edit decisions need checking against footage. Sponsorship bands are assumptions, not quotes. Public research needs verifiable sources. Publishing needs your request and a separate authorized tool; the pack has no built-in account connection.")
    g.p('Source and updates: <link href="' + REPO + '" color="#A64B30">github.com/ahmedsakri/youtube-agent-pro</link><br/>Read the root README and the selected skills for detailed behavior. MIT license notices must remain with redistributed code.', 9.5, 13, color=MUTED)
    g.save()


def openai(output):
    g = Guide(output, "OpenAI / ChatGPT + Codex", "#087B6C", "#E3F1EA")
    g.new("01 / Codex setup", "One pack.<br/>Native Codex skills.", "The OpenAI edition lives in openai/ inside the same repository. It adapts invocation, context handling and evidence rules for Codex and ChatGPT.")
    g.section("1", "Install all 24 sibling skills")
    g.p("Requires Python 3.9+ for the installer and local helpers. Review the dry run, then install into <b>~/.agents/skills</b>. No API key or third-party runtime Python package is required by this pack.")
    g.code("git clone https://github.com/ahmedsakri/youtube-agent-pro.git\ncd youtube-agent-pro/openai\npython3 scripts/install.py --dry-run\npython3 scripts/install.py")
    g.p("The installer refuses existing-name conflicts. For an intentional update, <b>--force</b> backs up old folders before replacement. For one project, use <b>--dest /absolute/project/path/.agents/skills</b>. Choose one route to avoid duplicate skill names.")
    g.section("2", "Start a new Codex conversation")
    g.code('Use $yt to plan my next video for beginner phone photographers.\nUse $yt-script to turn this outline into a 45-second Short.')
    g.p("Restart the client if the skills do not appear. These are references in your prompt, not terminal commands. Natural-language requests may also select a relevant installed skill.")
    g.section("3", "Plugin alternative, where supported")
    g.code("codex plugin marketplace add ahmedsakri/youtube-agent-pro\ncodex plugin add youtube-agent-pro-openai@youtube-agent-pro")
    g.p("Use a Codex CLI with these plugin commands, or a supported desktop client's local plugin source. The standalone installer above is the fallback. A GitHub repository does not automatically publish a plugin to OpenAI's public directory.", 9.8, 14, color=MUTED)
    g.new("02 / ChatGPT setup", "ChatGPT, with your files.", "Use portable instructions and files, or select an installed plugin where that capability is available in your ChatGPT account.")
    g.section("1", "Get the release files")
    g.p('From the <link href="' + REPO + '/releases/latest" color="#087B6C">shared repository\'s latest release</link>, download <b>ChatGPT-INSTRUCTIONS.md</b> and <b>ChatGPT-WORKFLOWS.md</b>. For computed scores, also download <b>youtube-agent-pro-openai-chatgpt.zip</b>.')
    g.section("2", "Supply instructions and your material")
    g.p("Paste the instructions into the conversation or project instructions where available. Attach the workflows and your transcript, export or outline. Add your voice profile if you have one. When file upload is unavailable, paste the relevant workflow and source text.")
    g.section("3", "Ask in plain language")
    g.code('Use yt-shorts to find three standalone clips in this transcript.\nPreserve timecodes and give each a new suggested opening line.\nAudience: English-speaking beginners. Target: 30-45 seconds.')
    g.p("In this portable route, <b>yt-shorts</b> is a workflow label, not an executable slash command. Select an actual installed plugin or skill with <b>@</b> only when it is available in your client.")
    g.note("Computed scores need execution", "To run helpers, use a mode that can access uploaded files, extract the optional ZIP and execute Python. Keep its skills/ directories together. Markdown alone does not run code. Without execution, request a qualitative review and no invented scores.")
    g.section("4", "Build the same files locally")
    g.p("From the shared repository's <b>openai/</b> directory:")
    g.code("python3 scripts/build_release.py")
    g.p("Build outputs go to openai/dist/. Account tools and limits still apply.", 9.8, 14, color=MUTED)
    g.new("03 / Choose the workflow", "The 24-skill map", "In Codex, use the $ form below. In portable ChatGPT conversations, ask to use the same workflow name without a command prefix.")
    workflow_map(g, "$")
    g.note("SEO without keyword stuffing", "Try: Use $yt-seo to write metadata for this phone-camera test. Put the real topic early, use relevant search phrases naturally and include only useful tags. No hashtags are needed. Do not invent results. Tags have a limited role; metadata cannot guarantee reach.")
    g.p("Eleven local helpers support scoring, linting and analysis. They use Python's standard library and make no network requests. Their scores are heuristics, not forecasts.", 10, 14, color=MUTED)
    g.new("04 / Verify the result", "Useful output,<br/>clear boundaries.", "Match the tool to the evidence. The OpenAI edition can proceed from your current context; a missing voice profile does not block useful work.")
    g.section("1", "Supply your channel context")
    g.p("Use an attached profile, your conversation, or the optional local file <b>.youtube-agent/voice.md</b>. Ask <b>$yt-voice</b> to create one; its template is <b>openai/skills/yt-voice/assets/voice.md</b>. Keep private exports, profiles and credentials outside this public repository.")
    g.section("2", "Check what actually happened")
    g.rows([
        ("Drafts and media", "A script is a draft, a thumbnail brief is a concept, and a clip plan is not an exported video. Rendering or image creation requires an appropriate, separately available tool."),
        ("Analytics and research", "Use real exports, comparable publication windows and traffic sources. Separate Shorts-feed metrics from long-form CTR. Do not infer causation from low views alone. Current claims need verified sources."),
        ("Publishing and accounts", "The pack contains no OAuth uploader, scheduling service or account client. External actions require your request and a separate authorized tool. A saved draft is not a verified upload."),
        ("Installation or execution problems", "Use one installation route, restart the client and keep sibling resources together. Resolve helper paths from their skill folder. If Python or file access is unavailable, use a qualitative workflow or provide local tool output."),
    ])
    g.note("Verification is scoped", "The repository's openai/docs/VALIDATION.md records the tested build and limits. A passing local test cannot guarantee every host, account or future platform version. There is no guarantee of views, revenue or virality.")
    g.p('Source and releases: <link href="' + REPO + '" color="#087B6C">github.com/ahmedsakri/youtube-agent-pro</link><br/>Setup: openai/README.md and openai/chatgpt/README.md.<br/>Independent community project. MIT license; preserve its notices.', 9.5, 13, color=MUTED)
    g.save()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "docs" / "guides")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for filename, build in (("YouTube-Agent-Pro-Claude.pdf", claude),
                            ("YouTube-Agent-Pro-OpenAI.pdf", openai)):
        path = args.output_dir / filename
        build(path)
        print(path)


if __name__ == "__main__":
    main()
