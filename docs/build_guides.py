#!/usr/bin/env python3
"""Build the two edition setup guides as tall phone-card PDFs (Chrome renders HTML -> PDF).

Restores the original interactive phone-card design (warm cream, Fraunces serif, rust accents,
clickable TOC + deep links, crimson progress footer) and produces one guide per edition:
  docs/guides/YouTube-Agent-Pro-Claude.pdf
  docs/guides/YouTube-Agent-Pro-OpenAI.pdf
The legacy alias docs/YouTube-Agent-Pro-Setup-Guide.pdf is kept byte-identical to the Claude guide.

Rebuilding the PDFs needs Google Chrome (for print-to-pdf) and network access for the webfont link.
The runtime skills and their Python helpers do NOT depend on this script.
"""
import html
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ROOT / "docs" / "guides"
LEGACY = ROOT / "docs" / "YouTube-Agent-Pro-Setup-Guide.pdf"
REPO = "https://github.com/ahmedsakri/youtube-agent-pro"
REPO_SHORT = "github.com/ahmedsakri/youtube-agent-pro"
BLOB = REPO + "/blob/main"


def esc(s):
    return html.escape(s, quote=True)


ICONS = {
    "monitor": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "terminal": '<path d="M4 17l6-6-6-6"/><path d="M12 19h8"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "mic": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0 0 14 0M12 19v3"/>',
    "ban": '<circle cx="12" cy="12" r="9"/><path d="M5 5l14 14"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "film": '<rect x="2" y="3" width="20" height="18" rx="2"/><path d="M7 3v18M17 3v18M2 8h5M2 16h5M17 8h5M17 16h5"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/>',
    "check": '<path d="M20 6L9 17l-5-5"/>',
    "box": '<path d="M21 8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><path d="M3.3 7L12 12l8.7-5M12 22V12"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "bulb": '<path d="M9 18h6M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1h6c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z"/>',
    "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="M21 15l-5-5L5 21"/>',
    "chart": '<path d="M3 3v18h18"/><rect x="7" y="12" width="3" height="6"/><rect x="12" y="8" width="3" height="10"/><rect x="17" y="5" width="3" height="13"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0 5 5l-9 9a2.8 2.8 0 0 1-4-4z"/>',
    "flag": '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><path d="M4 22V15"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22 22 0 0 1-4 2z"/><path d="M9 12H4s.5-2.8 2-4c1.7-1.3 5-1 5-1M12 15v5s2.8-.5 4-2c1.3-1.7 1-5 1-5"/>',
    "arrow": '<path d="M7 17L17 7M7 7h10v10"/>',
}


def icon(name, color="var(--accent)", size=22, sw=2.0):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


SPARK = ('<svg class="spark" viewBox="0 0 24 24" fill="#c75a33">'
         '<path d="M12 0c.5 6 5.5 11 12 11-6.5 0-11.5 5-12 13-.5-8-5.5-13-12-13 6.5 0 11.5-5 12-11z"/></svg>')
RAYS = ('<svg class="rays" viewBox="0 0 560 970" preserveAspectRatio="xMidYMin slice">'
        + ''.join(f'<polygon points="560,120 {560-280},{120+(k-4)*32} {560-280},{120+(k-3)*32}" '
                  f'fill="#f1dec9" opacity="0.55"/>' for k in range(9)) + '</svg>')

CSS = r"""
:root{
  --ink:#1b1a18; --body:#3b352f; --muted:#938577; --accent:#b4481f; --accent2:#c2552b;
  --card:#fffdf9; --pill-bg:#f7e0d3; --pill-ink:#b4481f; --code-bg:#f9f2e8; --code-ink:#2b2723;
  --on:#ec1f3a; --off:#ddd4c8; --divider:rgba(40,25,10,.09); --star:#c75a33; --yt:#ff0033;
}
*{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
@page{ size:560px 1052px; margin:0; }
html,body{background:#f3e6d4;}
body{font-family:'Inter',-apple-system,'Segoe UI',Roboto,sans-serif;color:var(--body);}
.page{position:relative;width:560px;height:1052px;overflow:hidden;
  background:linear-gradient(170deg,#fcf2e8 0%,#faeedf 42%,#f5e6d3 100%);
  padding:40px 44px 0;page-break-after:always;}
.page:last-child{page-break-after:auto;}
.rays{position:absolute;inset:0;pointer-events:none;opacity:.5;}
.hdr{display:flex;align-items:center;justify-content:space-between;}
.brand{display:flex;align-items:center;gap:11px;font-weight:700;color:var(--ink);font-size:19px;}
.spark{width:22px;height:22px;}
.yt{width:31px;height:22px;background:var(--yt);border-radius:7px;display:inline-flex;align-items:center;justify-content:center;}
.yt svg{margin-left:1px;}
.tag{font-family:'JetBrains Mono',Menlo,monospace;font-size:13px;color:var(--pill-ink);
  border:1px solid #eccdb9;border-radius:999px;padding:8px 16px;display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.4);}
.tag::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--accent);}
.rule{height:1px;background:var(--divider);margin:18px 0 0;}
.eyebrow{font-family:'JetBrains Mono',Menlo,monospace;font-size:13px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--muted);margin-top:34px;font-weight:600;}
h1{font-family:'Fraunces','Source Serif 4',Georgia,serif;color:var(--ink);font-weight:600;
  font-size:58px;line-height:.98;letter-spacing:-.015em;margin-top:8px;}
h1 em{font-style:italic;color:var(--accent);}
.lede{font-size:21px;line-height:1.4;color:#5a524a;margin-top:18px;max-width:34ch;}
.card{background:var(--card);border-radius:22px;padding:22px 24px;margin-top:16px;
  box-shadow:0 2px 10px rgba(90,60,25,.05),0 10px 30px rgba(90,60,25,.04);}
.card.tight{padding:18px 20px;}
.card.ic{display:flex;gap:16px;align-items:flex-start;}
.card h3{font-family:'Fraunces',Georgia,serif;font-size:26px;color:var(--ink);font-weight:600;}
.card p{font-size:17px;line-height:1.45;color:#5a524a;margin-top:6px;}
.soft{background:#f7ddd0;border-radius:20px;padding:22px 24px;margin-top:16px;}
.soft h3{color:var(--accent);font-family:'Fraunces',Georgia,serif;font-size:27px;font-weight:600;}
.soft p{font-size:17px;line-height:1.45;color:#6b4a3c;margin-top:7px;}
.dash{border:1.5px dashed #e3cdb9;border-radius:18px;padding:18px 22px;margin-top:16px;
  font-size:16px;line-height:1.45;color:#6a5e53;}
.isq{width:50px;height:50px;border-radius:14px;background:#f7e0d3;display:flex;align-items:center;justify-content:center;flex:none;}
.isq.sm{width:34px;height:34px;border-radius:10px;}
.pill{font-size:14px;font-weight:600;color:var(--pill-ink);background:var(--pill-bg);border-radius:999px;padding:6px 14px;display:inline-block;}
.pill.gray{background:#efe7db;color:#6a5e53;}
.pill.ok{background:#f7e0d3;color:var(--accent);}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center;}
code,.mono{font-family:'JetBrains Mono',Menlo,Consolas,monospace;}
.ichip{font-family:'JetBrains Mono',Menlo,monospace;background:#efe7db;border-radius:7px;padding:2px 8px;font-size:.92em;color:var(--code-ink);}
.code{background:var(--code-bg);border-radius:14px;padding:16px 18px;margin-top:12px;}
.code .lbl{font-family:'JetBrains Mono',Menlo,monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);font-weight:600;}
.code pre{font-family:'JetBrains Mono',Menlo,monospace;font-size:15px;line-height:1.55;color:var(--code-ink);margin-top:8px;white-space:pre-wrap;word-break:break-word;}
.code pre .c{color:var(--accent);}
a{color:inherit;text-decoration:none;}
.skill{background:var(--card);border-radius:20px;padding:16px 20px;margin-top:13px;box-shadow:0 2px 10px rgba(90,60,25,.05);display:block;}
.skill.cmp{padding:14px 18px;margin-top:11px;}
.skill.cmp p{margin-top:7px;font-size:16px;}
.skill .top{display:flex;align-items:center;justify-content:space-between;gap:10px;}
.cmd{font-family:'JetBrains Mono',Menlo,monospace;font-size:18px;background:#efe7db;border-radius:9px;padding:6px 12px;color:var(--code-ink);font-weight:600;}
.cmd b{color:var(--accent);font-weight:600;}
.skill p{font-size:16px;line-height:1.4;color:#5a524a;margin-top:9px;}
.try{font-family:'JetBrains Mono',Menlo,monospace;font-size:14px;color:#6a5e53;margin-top:8px;display:flex;align-items:center;}
.try b{color:var(--muted);letter-spacing:.1em;margin-right:8px;font-weight:600;}
.ext{margin-left:auto;opacity:.5;display:flex;}
.step{display:flex;gap:16px;margin-top:17px;align-items:flex-start;}
.num{flex:none;width:34px;height:34px;border-radius:50%;background:var(--accent);color:#fff;font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:18px;display:flex;align-items:center;justify-content:center;}
.step h4{font-family:'Fraunces',Georgia,serif;font-size:23px;color:var(--ink);font-weight:600;}
.step p{font-size:16px;line-height:1.4;color:#5a524a;margin-top:2px;}
.check{display:flex;gap:12px;align-items:flex-start;margin-top:12px;font-size:17px;color:#4a443e;line-height:1.35;}
.check .tick{flex:none;width:24px;height:24px;border-radius:50%;background:#f7e0d3;color:var(--accent);display:flex;align-items:center;justify-content:center;}
.check b{color:var(--ink);}
.flow{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:16px;}
.flow .c{background:var(--card);border-radius:12px;padding:10px 16px;font-family:'JetBrains Mono',Menlo,monospace;font-size:16px;color:var(--ink);box-shadow:0 2px 8px rgba(90,60,25,.06);}
.flow .a{color:var(--accent);display:flex;}
.link{background:var(--card);border-radius:18px;padding:18px 22px;margin-top:16px;display:flex;align-items:center;gap:14px;box-shadow:0 2px 10px rgba(90,60,25,.05);}
.link .ic{width:44px;height:44px;border-radius:12px;background:#f7e0d3;color:var(--accent);display:flex;align-items:center;justify-content:center;flex:none;}
.link .u{font-family:'JetBrains Mono',Menlo,monospace;font-size:16px;color:var(--ink);word-break:break-all;}
.link .go{margin-left:auto;color:var(--muted);display:flex;}
.stat{background:var(--card);border-radius:18px;padding:13px 20px;margin-top:11px;display:flex;align-items:center;gap:18px;box-shadow:0 2px 10px rgba(90,60,25,.05);}
.stat .n{font-family:'Fraunces',Georgia,serif;font-size:36px;color:var(--accent);font-weight:600;line-height:1;min-width:60px;}
.stat .l{font-size:19px;color:var(--ink);}
.price{background:var(--card);border-radius:18px;padding:18px 20px;box-shadow:0 2px 10px rgba(90,60,25,.05);}
.price .k{font-family:'JetBrains Mono',Menlo,monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);}
.price .v{font-family:'Fraunces',Georgia,serif;font-size:56px;color:var(--ink);font-weight:600;line-height:1;margin-top:2px;}
.price .s{font-family:'Fraunces',Georgia,serif;font-style:italic;color:var(--accent);font-size:22px;margin-top:6px;}
.price .n{font-size:14px;color:var(--muted);margin-top:2px;}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px;}
.mini{background:var(--card);border-radius:16px;padding:14px 16px;box-shadow:0 2px 8px rgba(90,60,25,.05);}
.mini .mh{display:flex;align-items:center;gap:9px;}
.mini h5{font-size:16px;color:var(--ink);}
.mini p{font-size:14px;color:#6a5e53;line-height:1.35;margin-top:5px;}
.repocard{background:var(--card);border-radius:20px;padding:22px 24px;margin-top:16px;box-shadow:0 2px 10px rgba(90,60,25,.05);}
.repocard .t{display:flex;align-items:center;gap:12px;font-family:'JetBrains Mono',Menlo,monospace;font-size:22px;color:var(--ink);font-weight:600;}
.repocard p{font-size:17px;color:#5a524a;margin-top:10px;line-height:1.4;}
.toc a{display:flex;align-items:center;gap:16px;background:var(--card);border-radius:16px;padding:14px 18px;margin-top:12px;box-shadow:0 2px 8px rgba(90,60,25,.05);}
.toc .tt{font-family:'Fraunces',Georgia,serif;font-size:21px;color:var(--ink);font-weight:600;}
.toc .pg{margin-left:auto;font-family:'JetBrains Mono',Menlo,monospace;font-size:15px;color:var(--muted);}
.closer{position:absolute;left:44px;right:44px;bottom:92px;}
.closer .q{font-family:'Fraunces',Georgia,serif;font-style:italic;color:var(--accent);font-size:34px;font-weight:600;margin-top:4px;}
.closer .p{color:var(--muted);font-size:19px;}
.ftr{position:absolute;left:44px;right:44px;bottom:30px;}
.prog{display:flex;align-items:center;gap:6px;height:10px;margin-bottom:18px;}
.seg{height:5px;border-radius:999px;background:var(--off);flex:1;}
.seg.on{background:var(--on);}
.dot{width:13px;height:13px;border-radius:50%;background:var(--on);box-shadow:0 0 0 4px #fbe7d9;flex:none;}
.fbar{display:flex;align-items:center;justify-content:space-between;}
.fbar .pg{font-size:16px;color:#7a6e62;min-width:52px;}
.fbar .nm{font-size:17px;color:var(--ink);font-weight:500;}
.fbar .ic{display:flex;gap:12px;align-items:center;color:#9a8c7d;}
.cc{border:1.5px solid #c9bba9;border-radius:6px;padding:1px 6px;font-size:12px;font-weight:700;color:#8c7e6f;font-family:'JetBrains Mono',monospace;}
"""

YT_PLAY = '<svg width="11" height="11" viewBox="0 0 24 24" fill="#fff"><path d="M6 4l14 8-14 8z"/></svg>'


def header(tag):
    return (f'<div class="hdr"><div class="brand">{SPARK}<span class="yt">{YT_PLAY}</span>'
            f'<span>YouTube Agent Pro</span></div><span class="tag">{esc(tag)}</span></div>'
            f'<div class="rule"></div>')


def footer(n, total, name):
    segs = []
    for i in range(1, total + 1):
        if i < n:
            segs.append('<div class="seg on"></div>')
        elif i == n:
            segs.append('<div class="seg on"></div><div class="dot"></div>')
        else:
            segs.append('<div class="seg"></div>')
    prog = '<div class="prog">' + "".join(segs) + '</div>'
    sun = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#9a8c7d" '
           'stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/>'
           '<path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/></svg>')
    return (f'<div class="ftr">{prog}<div class="fbar"><span class="pg">{n} / {total}</span>'
            f'<span class="nm">{esc(name)}</span>'
            f'<span class="ic"><span class="cc">CC</span>{sun}</span></div></div>')


def title(eyebrow, main_html):
    return f'<div class="eyebrow">{esc(eyebrow)}</div><h1>{main_html}</h1>'


def skill(cmd, needs, desc, try_cmd=None, compact=False):
    name = cmd.lstrip("/")
    href = f"{BLOB}/skills/{name}/SKILL.md"
    cmd_html = f'<span class="cmd"><b>/</b>{esc(name)}</span>'
    needs_html = f'<span class="pill">{esc(needs)}</span>' if needs else ''
    arrow = f'<span class="ext">{icon("arrow", "#b4481f", 15, 2)}</span>'
    if compact:
        inner = f'<div class="top">{cmd_html}{needs_html}{arrow}</div><p>{esc(desc)}</p>'
        return f'<a class="skill cmp" href="{href}">{inner}</a>'
    t = f'<div class="try"><b>TRY</b>{esc(try_cmd)}{arrow}</div>' if try_cmd else ''
    inner = f'<div class="top">{cmd_html}{needs_html}</div><p>{esc(desc)}</p>{t}'
    return f'<a class="skill" href="{href}">{inner}</a>'


ORDER = ["cover", "contents", "what-you-need", "install", "install-more", "voice", "full-run",
         "skills", "skills-2", "skills-3", "skills-4", "skills-5", "tools", "gate", "fixes", "get-it"]
TOTAL = len(ORDER)


def pg(anchor):
    return ORDER.index(anchor) + 1


# ---- per-edition configuration -----------------------------------------
EDITIONS = {
    "Claude": {
        "host": "Claude Code",
        "cover_desc": "Twenty-four Claude skills that run a YouTube channel, end to end.",
        "need_host_body": "The terminal app, the desktop app or an IDE. Skills install and run here.",
        "install_tag": "install · marketplace",
        "install_lbl": "Claude Code",
        "install_code": ('<span class="c">/plugin</span> marketplace add ahmedsakri/youtube-agent-pro\n'
                         '<span class="c">/plugin</span> install youtube-agent-pro'),
        "install_what": ("The first registers this repo as a plugin marketplace. The second installs the "
                         "plugin from it. A marketplace in Claude Code is just a git repo with a "
                         '<span class="ichip">marketplace.json</span>, so there is nothing central to sign up for.'),
        "install_update": '<b>Update later:</b> <span class="ichip">/plugin marketplace update youtube-agent-pro</span>',
        "skill_dir": "~/.claude/skills",
        "getit_first": "Add the marketplace and <b>install</b> in Claude Code",
        "fixes_dir": "~/.claude/skills",
        "fixes_update": '<span class="ichip">/plugin marketplace update youtube-agent-pro</span>, or git pull your clone and copy the folders again.',
    },
    "OpenAI": {
        "host": "ChatGPT & Codex",
        "cover_desc": "Twenty-four skills that run a YouTube channel, for ChatGPT and Codex.",
        "need_host_body": "The Codex CLI, or ChatGPT with skill upload. Skills install and run here.",
        "install_tag": "install · codex",
        "install_lbl": "Terminal (Codex)",
        "install_code": ('git clone https://github.com/ahmedsakri/youtube-agent-pro\n'
                         '<span class="c">cd</span> youtube-agent-pro\n'
                         'python3 scripts/install.py'),
        "install_what": ("The installer copies all 24 skills to "
                         '<span class="ichip">~/.agents/skills</span> with shared resources and license '
                         "notices. It refuses conflicting skills; use "
                         '<span class="ichip">--force</span> to back up and replace. For ChatGPT, upload '
                         "the skill folders instead."),
        "install_update": '<b>Update later:</b> <span class="ichip">git pull</span> then <span class="ichip">python3 scripts/install.py --force</span>',
        "skill_dir": "~/.agents/skills",
        "getit_first": "Clone the repo and run <b>python3 scripts/install.py</b> for Codex",
        "fixes_dir": "~/.agents/skills",
        "fixes_update": '<span class="ichip">git pull</span> then <span class="ichip">python3 scripts/install.py --force</span>.',
    },
}


def make_html(ed):
    DEFS = []

    def add(tag, section, anchor, body):
        DEFS.append({"tag": tag, "section": section, "anchor": anchor, "body": body})

    label = ed["_label"]

    # 1 COVER
    add("setup guide", "Start", "cover", f"""{RAYS}
<div class="eyebrow" style="margin-top:40px;">{esc(label.upper())} EDITION &middot; 24 SKILLS &middot; 11 TOOLS &middot; MIT</div>
<h1 style="font-size:60px;margin-top:10px;">YouTube<br>Agent Pro<br><em>Setup guide.</em></h1>
<p class="lede" style="margin-top:16px;">An AI agent for YouTube in {esc(ed['host'])}: ideas, scripts,
hooks, titles, thumbnails, SEO and sponsorship.</p>
<div class="repocard" style="margin-top:22px;">
  <div class="t">{icon('box', '#b4481f', 22)} youtube-agent-pro
    <span class="pill ok" style="font-size:13px;">Public</span></div>
  <p>{esc(ed['cover_desc'])}</p>
  <div class="row" style="margin-top:14px;"><span class="pill gray">MIT License</span>
  <span class="pill ok">Open source</span><span class="pill gray">24 skills</span></div>
</div>
<div class="grid2" style="grid-template-columns:1fr 1.3fr;">
  <div class="price"><div class="k">Price</div><div class="v">&#8377;0</div>
    <div class="s">free to use</div><div class="n">No signup &middot; No API key</div></div>
  <div>
    <div class="stat"><span class="n">24</span><span class="l">skills</span></div>
    <div class="stat"><span class="n">21</span><span class="l">hook formulas</span></div>
    <div class="stat"><span class="n">11</span><span class="l">Python tools</span></div>
  </div>
</div>
<a href="{REPO}"><div class="link" style="margin-top:14px;"><span class="ic">{icon('link','#b4481f',22)}</span>
  <span class="u">{REPO_SHORT}</span><span class="go">{icon('arrow','#938577',20)}</span></div></a>
""")

    # 2 CONTENTS
    TOC = [("what-you-need", "monitor", "What you need"), ("install", "box", "Install"),
           ("voice", "mic", "Teach it your voice"), ("full-run", "rocket", "The full run"),
           ("skills", "list", "The 24 skills"), ("tools", "terminal", "The 11 tools"),
           ("gate", "flag", "Nothing publishes"), ("fixes", "wrench", "Quick fixes"),
           ("get-it", "link", "Get the skill")]
    toc_rows = "".join(
        f'<a href="#{a}"><span class="isq sm">{icon(ic, "#b4481f", 18)}</span>'
        f'<span class="tt">{esc(t)}</span><span class="pg">{pg(a):02d}</span></a>' for a, ic, t in TOC)
    add("contents", "Contents", "contents",
        title("TAP TO JUMP", 'The <em>contents.</em>')
        + '<p class="lede" style="margin-top:14px;">Every row is a link. The whole guide is clickable, '
          'including each skill and tool.</p>'
        + f'<div class="toc">{toc_rows}</div>')

    # 3 WHAT YOU NEED
    add("before you start", "What you need", "what-you-need",
        title("BEFORE YOU START", 'What you <em>need.</em>')
        + f'<div class="card ic"><span class="isq">{icon("monitor")}</span><div><h3>{esc(ed["host"])}</h3>'
          f'<p>{ed["need_host_body"]}</p></div></div>'
        + f'<div class="card ic"><span class="isq">{icon("terminal")}</span><div><h3>Python 3</h3>'
          '<p>Only for the 11 tools. Nothing to pip install. Check it: '
          '<span class="ichip">python3 --version</span></p></div></div>'
        + f'<div class="card ic"><span class="isq">{icon("clock")}</span><div><h3>Ten minutes</h3>'
          '<p>To write your optional voice file with /yt-voice. Skip it and the scripts are more '
          'generic.</p></div></div>'
        + '<div class="eyebrow" style="margin-top:22px;">NOTHING ELSE</div>'
        + '<div class="row" style="margin-top:12px;"><span class="pill ok">No signup</span>'
          '<span class="pill ok">No API key</span><span class="pill ok">Nothing to connect</span></div>'
        + '<div class="soft"><h3>It writes. You upload.</h3><p>Nothing is published to YouTube for you. '
          '<span class="ichip">/yt-viral</span> and <span class="ichip">/yt-collab</span> read public '
          'listings only and never log in as you.</p></div>')

    # 4 INSTALL
    add(ed["install_tag"], "Install", "install",
        title("THE EASY WAY", 'Install the <em>pack.</em>')
        + f'<div class="flow"><span class="c">1 add</span><span class="a">{icon("arrow","#b4481f",18)}</span>'
          f'<span class="c">2 install</span><span class="a">{icon("arrow","#b4481f",18)}</span>'
          '<span class="c">3 ready</span></div>'
        + f'<div class="code"><div class="lbl">{esc(ed["install_lbl"])}</div><pre>{ed["install_code"]}</pre></div>'
        + f'<div class="card" style="margin-top:18px;"><h3>What that does</h3><p>{ed["install_what"]}</p></div>'
        + f'<div class="card tight"><div class="row"><span class="pill ok">{icon("check","#b4481f",14,2.4)} '
          'installed</span><span style="font-size:17px;color:#5a524a;">all 24 skills are now '
          'ready</span></div></div>'
        + f'<div class="dash">{ed["install_update"]}</div>')

    # 5 INSTALL MORE
    add("install · other ways", "Install", "install-more",
        title("OTHER WAYS", 'Prefer to do it <em>yourself?</em>')
        + '<a class="skill" href="' + REPO + '"><div class="top"><span class="cmd">A &nbsp;Clone and copy'
          '</span><span class="pill">global</span></div>'
          '<div class="code" style="margin-top:12px;"><div class="lbl">Terminal</div><pre>'
          'git clone https://github.com/ahmedsakri/youtube-agent-pro\n'
          f'cp -r youtube-agent-pro/skills/yt* {esc(ed["skill_dir"])}/</pre></div></a>'
        + f'<div class="skill"><div class="top"><span class="cmd">B &nbsp;Project only</span>'
          '<span class="pill">one repo</span></div><p>Copy the same <span class="ichip">yt*</span> '
          'folders into your project’s skills directory instead. They then work in that project '
          'only.</p></div>'
        + '<div class="skill"><div class="top"><span class="cmd">C &nbsp;Paste a skill</span>'
          '<span class="pill">fallback</span></div><p>Paste any single <span class="ichip">SKILL.md</span> '
          'at the top of a chat and it runs as a mode. You lose the Python tools, but the reasoning still '
          'works.</p></div>'
        + '<div class="dash" style="margin-top:14px;"><b style="color:var(--accent);">Not sure?</b> Use '
          'the install method on page 4. It does the rest.</div>')

    # 6 VOICE
    tiles = [("users", "Who I talk to", "One real person, not “creators”."),
             ("mic", "How I talk", "Your real transcripts, measured."),
             ("ban", "Words I never use", "Unlock. Game-changer. Be specific."),
             ("message", "Words I do use", "Your tics. Keep them."),
             ("shield", "What I won’t claim", "Numbers and tools you can’t show."),
             ("film", "My format", "Length, on camera or not.")]
    tile_html = "".join(
        f'<div class="mini"><div class="mh">{icon(ic, "#b4481f", 18)}<h5>{esc(t)}</h5></div>'
        f'<p>{esc(d)}</p></div>' for ic, t, d in tiles)
    add("voice.md", "Voice file", "voice",
        title("STEP 1 · OPTIONAL", 'Teach it <em>your voice.</em>')
        + '<p class="lede">An optional profile every skill can read. You say the words out loud, so it '
          'helps to sound like you.</p>'
        + f'<div class="card"><div class="row"><span class="pill ok">FASTEST</span>'
          '<h3 style="font-size:23px;">Let /yt-voice write it</h3></div><p>Send three of your own videos '
          'or transcripts, then run <span class="ichip">/yt-voice</span>. It runs '
          '<span class="ichip">voiceprint.py</span> to measure how you talk and writes a voice profile.</p></div>'
        + '<div class="eyebrow" style="margin-top:20px;">WHAT THE FILE CAPTURES</div>'
        + f'<div class="grid2">{tile_html}</div>'
        + '<div class="dash">No voice profile yet? Skills still work; they just ask for samples when useful.</div>')

    # 7 FULL RUN
    steps = [("bulb", "Idea", "/yt-idea scores it before you film."),
             ("pen", "Brief", "/yt-brief turns it into a shot list."),
             ("film", "Script", "/yt-script: hook panel, then the spoken script."),
             ("image", "Package", "/yt-package + /yt-thumbnail, linted as one pairing."),
             ("list", "Find it", "/yt-seo + /yt-chapters for the search surface."),
             ("chart", "Learn", "/yt-retention + /yt-analytics find the one fix.")]
    step_html = "".join(
        f'<div class="step"><div class="num">{i}</div><div><h4>{esc(t)}</h4><p>{esc(d)}</p></div></div>'
        for i, (ic, t, d) in enumerate(steps, 1))
    add("the full run", "The full run", "full-run",
        title("ONE VIDEO, START TO FINISH", 'The <em>full run.</em>')
        + '<p class="lede">Ask <span class="ichip">/yt</span>, the hub, and it routes you. Or run the '
          'pipeline yourself, stopping at each gate.</p>' + step_html)

    # 8-12 SKILLS
    add("skills · 1 of 5", "Make the video", "skills",
        title("THE 24 SKILLS · 1 OF 5", 'Make the <em>video.</em>')
        + skill("/yt-idea", "needs: a niche", 'A niche into scored ideas, before you film the wrong one.', '/yt-idea ideas for my channel')
        + skill("/yt-script", "needs: an idea", 'One idea in, a full script out. Five hooks off 21 formulas, scored.', '/yt-script why no views')
        + skill("/yt-brief", "needs: a script", 'A script into a shot list: framing, b-roll, gear, runtime.', '/yt-brief for the script')
        + skill("/yt-chapters", "needs: a transcript", "Chapters checked against YouTube's rules, so they render.", '/yt-chapters file.srt'))
    add("skills · 2 of 5", "Package it", "skills-2",
        title("THE 24 SKILLS · 2 OF 5", 'Package <em>it.</em>')
        + skill("/yt-package", "needs: a draft title", 'Title and thumbnail text as one pairing. Checks truncation, repeats, vague words.', '/yt-package for this')
        + skill("/yt-thumbnail", "needs: a title", 'The thumbnail as a concept: one idea, three elements, three words. Linted and A/B’d.', '/yt-thumbnail concepts')
        + skill("/yt-seo", "needs: a topic", 'The description, the tags worth keeping, and three queries to win.', '/yt-seo write my description')
        + '<div class="dash">The pairing is the unit. A thumbnail that repeats the title wastes half the '
          'click surface, so these are linted together.</div>')
    add("skills · 3 of 5", "Read the numbers", "skills-3",
        title("THE 24 SKILLS · 3 OF 5", 'Read the <em>numbers.</em>')
        + skill("/yt-analytics", "needs: a Studio export", 'The funnel read for the one number holding a video back: impressions, CTR, retention.', '/yt-analytics my stats')
        + skill("/yt-retention", "needs: retention CSV", 'The retention curve read properly: the hook leak, the cliffs, the slide.', '/yt-retention file.csv')
        + skill("/yt-funnel", "needs: channel page", 'The trailer, above-the-fold and sections that turn browsers into subscribers.', '/yt-funnel my channel page')
        + skill("/yt-audit", "needs: channel link", 'The whole channel, ending in ONE fix, not twenty.', '/yt-audit youtube.com/@you'))
    add("skills · 4 of 5", "Grow it", "skills-4",
        title("THE 24 SKILLS · 4 OF 5", 'Grow <em>it.</em>')
        + skill("/yt-viral", "needs: your niche", 'What works in your niche, ranked by multiple over each channel’s own median.', compact=True)
        + skill("/yt-trend", "needs: your niche", 'A 90-day calendar: seasonal demand and the evergreen-to-timely mix.', compact=True)
        + skill("/yt-series", "needs: a big topic", 'A series or playlist as a binge: each video earns the next click.', compact=True)
        + skill("/yt-collab", "needs: your niche", 'Channels to collaborate with, by audience overlap, plus the pitch.', compact=True)
        + skill("/yt-endscreen", "needs: retention", 'End screens and cards placed to keep the session going.', compact=True))
    add("skills · 5 of 5", "Multiply + business", "skills-5",
        title("THE 24 SKILLS · 5 OF 5", 'Multiply, then <em>earn.</em>')
        + skill("/yt-shorts", "needs: a transcript", 'The Shorts hiding inside a long video, each with a new first line.', compact=True)
        + skill("/yt-repurpose", "needs: a transcript", 'One video into a thread, a LinkedIn post, a newsletter and a blog outline.', compact=True)
        + skill("/yt-plan", "needs: your hours", 'A week that fits your hours: one anchor, one cheap one, three Shorts.', compact=True)
        + skill("/yt-sponsor", "needs: your views", 'A defensible rate card, the reply to the brand, and the integration.', compact=True)
        + skill("/yt-comment", "needs: pasted comments", 'Comments triaged into piles, replies in your voice, which to pin.', compact=True))

    # 13 TOOLS
    TOOLS = [
        ("ideascore.py", "Scores a video idea on four axes.", "skills/yt-idea/ideascore.py"),
        ("hookscore.py", "Scores a hook on five properties.", "skills/yt-script/hookscore.py"),
        ("title.py", "Lints a title and thumbnail as one pair.", "skills/yt-package/title.py"),
        ("thumblint.py", "Lints a thumbnail concept.", "skills/yt-thumbnail/thumblint.py"),
        ("funnel.py", "Finds the binding constraint.", "skills/yt-analytics/funnel.py"),
        ("retention.py", "Where viewers left, and what was said.", "skills/yt-retention/retention.py"),
        ("ratecard.py", "A sponsorship rate from your views.", "skills/yt-sponsor/ratecard.py"),
        ("voiceprint.py", "Measures how you actually talk.", "skills/yt-voice/voiceprint.py"),
        ("deadair.py", "Edit decision list from a transcript.", "skills/yt-edit/deadair.py"),
        ("chapters.py", "Chapters that pass YouTube's rules.", "skills/yt-chapters/chapters.py"),
        ("swipe.py", "Outliers by own-channel multiple.", "skills/yt-viral/swipe.py"),
    ]
    tool_cards = "".join(
        f'<a class="skill" style="padding:9px 18px;margin-top:8px;" href="{BLOB}/{p}"><div class="top">'
        f'<span class="cmd" style="font-size:15px;color:var(--accent);">{esc(f)}</span>'
        f'<span style="font-size:15px;color:#6a5e53;">{esc(d)}</span>'
        f'<span class="ext">{icon("arrow","#938577",14,2)}</span></div></a>'
        for f, d, p in TOOLS)
    add("11 tools", "The 11 tools", "tools",
        title("UNDER THE HOOD", 'Eleven <em>tools.</em>')
        + '<p class="lede" style="max-width:44ch;margin-top:12px;">Plain Python 3. No installs. The agent '
          'runs them for you. They are heuristics, not predictors, and they are why the skills are more '
          'than prompts.</p>' + tool_cards)

    # 14 GATE
    add("the gate", "The gate", "gate",
        title("THE ONE RULE", 'Nothing <em>publishes.</em>')
        + '<p class="lede">Every skill writes. You upload. That is the whole difference between this and '
          'a bot that runs your channel into the ground.</p>'
        + '<div class="card"><h3>Every run ends the same way</h3><p>A block you copy, and one question. '
          'You decide, every time, with the words in front of you.</p></div>'
        + '<div class="soft" style="text-align:center;padding:30px 24px;">'
          '<h3 style="font-size:34px;">Ship it, or change it?</h3></div>'
        + f'<div class="grid2" style="margin-top:20px;">'
          f'<div class="mini"><div class="mh">{icon("ban","#b4481f",18)}<h5>Reads, never scrapes</h5></div>'
          '<p>/yt-viral and /yt-collab use public listings only. Never your login.</p></div>'
          f'<div class="mini"><div class="mh">{icon("shield","#b4481f",18)}<h5>Invents no numbers</h5></div>'
          '<p>If a skill wants a figure it does not have, it asks you or writes without it.</p></div></div>')

    # 15 FIXES
    def fix(q, a):
        return (f'<div class="card tight"><h3 style="font-style:italic;color:var(--accent);'
                f'font-size:23px;">{q}</h3><p>{a}</p></div>')
    add("fixes", "Fixes", "fixes",
        title("IF IT BREAKS", 'Quick <em>fixes.</em>')
        + fix("skills not found", f'Restart your client once. Then check '
              f'<span class="ichip">ls {esc(ed["fixes_dir"])} | grep yt-</span> and you should see 24 folders.')
        + fix("python3: command not found", "Install Python 3 from python.org. The tools need nothing else.")
        + fix("/yt-viral skipped a channel", "It needs about four videos per channel to find a median. Add more videos or another channel.")
        + fix("A score looks wrong", "The scorers are heuristics. A low score means look again, not a verdict.")
        + fix("Update to the latest", f'Run {ed["fixes_update"]}'))

    # 16 GET IT
    add("get the skill", "Get it", "get-it", f"""{RAYS}
""" + title("THE LINK", 'Get the <em>skill.</em>') + f"""
<div class="repocard"><div class="t">{icon('box','#b4481f',22)} youtube-agent-pro
  <span class="pill ok" style="font-size:13px;">Public</span></div>
  <p>{esc(ed['cover_desc'])} Use it, change it, ship it.</p>
  <div class="row" style="margin-top:12px;"><span class="pill gray">MIT License</span>
  <span class="pill ok">Open source</span><span class="pill gray">24 skills</span></div></div>
<a href="{REPO}"><div class="link"><span class="ic">{icon('link','#b4481f',22)}</span>
  <span class="u">{REPO_SHORT}</span><span class="go">{icon('arrow','#938577',20)}</span></div></a>
<div class="card"><h3>Your first ten minutes</h3>
  <div class="check"><span class="tick">{icon('check','#b4481f',14,2.4)}</span><span>{ed['getit_first']}</span></div>
  <div class="check"><span class="tick">{icon('check','#b4481f',14,2.4)}</span><span>Run <b>/yt-voice</b> to write your voice profile from three videos</span></div>
  <div class="check"><span class="tick">{icon('check','#b4481f',14,2.4)}</span><span>Run <b>/yt-idea</b>, then <b>/yt-script</b> on the winner</span></div></div>
<div class="closer"><div class="p">Every skill ends with one question.</div>
  <div class="q">Ship it, or change it?</div></div>
""")

    assert [d["anchor"] for d in DEFS] == ORDER, "page order mismatch"
    sections = "".join(
        f'<section id="{d["anchor"]}" class="page">{header(d["tag"])}{d["body"]}'
        f'{footer(i + 1, TOTAL, d["section"])}</section>'
        for i, d in enumerate(DEFS))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500;1,9..144,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
{sections}
</body></html>"""


def chrome_path():
    for p in [os.environ.get("CHROME_PATH"),
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              shutil.which("google-chrome"), shutil.which("chromium"),
              shutil.which("chromium-browser")]:
        if p and os.path.exists(p):
            return p
    raise SystemExit("Google Chrome not found. Set CHROME_PATH to rebuild the PDFs.")


def render(html_text, out_pdf):
    chrome = chrome_path()
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as fh:
        fh.write(html_text)
        tmp = fh.name
    try:
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={out_pdf}", "file://" + tmp],
                       check=True, capture_output=True)
    finally:
        os.unlink(tmp)


def main():
    GUIDES.mkdir(parents=True, exist_ok=True)
    claude_pdf = GUIDES / "YouTube-Agent-Pro-Claude.pdf"
    for label, ed in EDITIONS.items():
        ed = dict(ed, _label=label)
        out = GUIDES / ("YouTube-Agent-Pro-" + label + ".pdf")
        render(make_html(ed), str(out))
        print("wrote", out.relative_to(ROOT))
    # legacy alias must be byte-identical to the Claude guide
    shutil.copyfile(claude_pdf, LEGACY)
    print("wrote", LEGACY.relative_to(ROOT), "(alias of Claude guide)")


if __name__ == "__main__":
    main()
