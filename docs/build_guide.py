#!/usr/bin/env python3
"""Generate the YouTube Agent Pro setup guide as a tall phone-card HTML, for Chrome -> PDF.

Design mirrors the reference setup guide: warm cream gradient, Fraunces serif headings with a rust
italic accent word, rounded cream cards, pill badges, mono code blocks, and a crimson progress bar
footer. Links are real <a> tags so they stay clickable in the PDF.
"""
import html

REPO = "https://github.com/ahmedsakri/youtube-agent-pro"
REPO_SHORT = "github.com/ahmedsakri/youtube-agent-pro"

PAGES = []  # filled by page() calls, each a full <section>

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
.page{
  position:relative; width:560px; height:1052px; overflow:hidden;
  background:linear-gradient(170deg,#fcf2e8 0%,#faeedf 42%,#f5e6d3 100%);
  padding:40px 44px 0; page-break-after:always;
}
.page:last-child{page-break-after:auto;}
.rays{position:absolute;inset:0;pointer-events:none;opacity:.5;}
/* header */
.hdr{display:flex;align-items:center;justify-content:space-between;}
.brand{display:flex;align-items:center;gap:11px;font-weight:700;color:var(--ink);font-size:19px;}
.spark{width:22px;height:22px;}
.yt{width:31px;height:22px;background:var(--yt);border-radius:7px;display:inline-flex;align-items:center;justify-content:center;}
.yt::after{content:"";border-left:10px solid #fff;border-top:6px solid transparent;border-bottom:6px solid transparent;margin-left:2px;}
.tag{font-family:'JetBrains Mono',Menlo,monospace;font-size:13px;color:var(--pill-ink);
  border:1px solid #eccdb9;border-radius:999px;padding:8px 16px;display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.4);}
.tag::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--accent);}
.rule{height:1px;background:var(--divider);margin:18px 0 0;}
/* titles */
.eyebrow{font-family:'JetBrains Mono',Menlo,monospace;font-size:13px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--muted);margin-top:34px;font-weight:600;}
h1{font-family:'Fraunces','Source Serif 4',Georgia,serif;color:var(--ink);font-weight:600;
  font-size:58px;line-height:.98;letter-spacing:-.015em;margin-top:8px;}
h1 em{font-style:italic;color:var(--accent);}
.lede{font-size:21px;line-height:1.4;color:#5a524a;margin-top:20px;max-width:30ch;}
/* cards */
.card{background:var(--card);border-radius:22px;padding:22px 24px;margin-top:16px;
  box-shadow:0 2px 10px rgba(90,60,25,.05),0 10px 30px rgba(90,60,25,.04);}
.card.tight{padding:18px 20px;}
.card h3{font-family:'Fraunces',Georgia,serif;font-size:26px;color:var(--ink);font-weight:600;}
.card p{font-size:17px;line-height:1.45;color:#5a524a;margin-top:6px;}
.soft{background:#f7ddd0;border-radius:20px;padding:22px 24px;margin-top:16px;}
.soft h3{color:var(--accent);font-family:'Fraunces',Georgia,serif;font-size:27px;font-weight:600;}
.soft p{font-size:17px;line-height:1.45;color:#6b4a3c;margin-top:7px;}
.dash{border:1.5px dashed #e3cdb9;border-radius:18px;padding:18px 22px;margin-top:16px;
  font-size:16px;line-height:1.45;color:#6a5e53;}
/* pills + code */
.pill{font-size:14px;font-weight:600;color:var(--pill-ink);background:var(--pill-bg);
  border-radius:999px;padding:6px 14px;display:inline-block;}
.pill.gray{background:#efe7db;color:#6a5e53;}
.pill.ok{background:#f7e0d3;color:var(--accent);}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center;}
code,.mono{font-family:'JetBrains Mono',Menlo,Consolas,monospace;}
. chip,.ichip{font-family:'JetBrains Mono',Menlo,monospace;background:#efe7db;border-radius:7px;
  padding:2px 8px;font-size:.92em;color:var(--code-ink);}
.code{background:var(--code-bg);border-radius:14px;padding:16px 18px;margin-top:12px;}
.code .lbl{font-family:'JetBrains Mono',Menlo,monospace;font-size:12px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted);font-weight:600;}
.code pre{font-family:'JetBrains Mono',Menlo,monospace;font-size:15px;line-height:1.55;
  color:var(--code-ink);margin-top:8px;white-space:pre-wrap;word-break:break-word;}
.code pre .c{color:var(--accent);}
/* skill card */
.skill{background:var(--card);border-radius:20px;padding:16px 20px;margin-top:13px;
  box-shadow:0 2px 10px rgba(90,60,25,.05);}
.skill.cmp{padding:14px 18px;margin-top:11px;}
.skill.cmp p{margin-top:7px;font-size:16px;}
.skill .top{display:flex;align-items:center;justify-content:space-between;gap:10px;}
.cmd{font-family:'JetBrains Mono',Menlo,monospace;font-size:18px;background:#efe7db;border-radius:9px;
  padding:6px 12px;color:var(--code-ink);font-weight:600;}
.cmd b{color:var(--accent);font-weight:600;}
.skill p{font-size:16px;line-height:1.4;color:#5a524a;margin-top:9px;}
.try{font-family:'JetBrains Mono',Menlo,monospace;font-size:14px;color:#6a5e53;margin-top:8px;}
.try b{color:var(--muted);letter-spacing:.1em;margin-right:8px;font-weight:600;}
/* numbered steps */
.step{display:flex;gap:16px;margin-top:18px;}
.num{flex:none;width:34px;height:34px;border-radius:50%;background:var(--accent);color:#fff;
  font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:18px;display:flex;align-items:center;justify-content:center;}
.step h4{font-family:'Fraunces',Georgia,serif;font-size:23px;color:var(--ink);font-weight:600;}
.step p{font-size:16px;line-height:1.4;color:#5a524a;margin-top:2px;}
/* list */
.check{display:flex;gap:12px;align-items:flex-start;margin-top:12px;font-size:17px;color:#4a443e;line-height:1.35;}
.check .tick{flex:none;width:24px;height:24px;border-radius:50%;background:#f7e0d3;color:var(--accent);
  display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;}
.check b{color:var(--ink);}
/* flow chips */
.flow{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:16px;}
.flow .c{background:var(--card);border-radius:12px;padding:10px 16px;font-family:'JetBrains Mono',Menlo,monospace;
  font-size:16px;color:var(--ink);box-shadow:0 2px 8px rgba(90,60,25,.06);}
.flow .a{color:var(--accent);font-size:20px;}
a{color:inherit;text-decoration:none;}
.link{background:var(--card);border-radius:18px;padding:18px 22px;margin-top:16px;display:flex;
  align-items:center;gap:14px;box-shadow:0 2px 10px rgba(90,60,25,.05);}
.link .ic{width:40px;height:40px;border-radius:11px;background:#f7e0d3;color:var(--accent);
  display:flex;align-items:center;justify-content:center;font-size:19px;flex:none;}
.link .u{font-family:'JetBrains Mono',Menlo,monospace;font-size:16px;color:var(--ink);word-break:break-all;}
.link .ext{margin-left:auto;color:var(--muted);font-size:18px;}
/* stat tiles */
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
.mini h5{font-size:16px;color:var(--ink);}
.mini p{font-size:14px;color:#6a5e53;line-height:1.35;margin-top:3px;}
.repocard{background:var(--card);border-radius:20px;padding:22px 24px;margin-top:16px;box-shadow:0 2px 10px rgba(90,60,25,.05);}
.repocard .t{display:flex;align-items:center;gap:12px;font-family:'JetBrains Mono',Menlo,monospace;font-size:22px;color:var(--ink);font-weight:600;}
.repocard p{font-size:17px;color:#5a524a;margin-top:10px;line-height:1.4;}
.closer{position:absolute;left:44px;right:44px;bottom:92px;}
.closer .q{font-family:'Fraunces',Georgia,serif;font-style:italic;color:var(--accent);font-size:34px;font-weight:600;margin-top:4px;}
.closer .p{color:var(--muted);font-size:19px;}
/* footer */
.ftr{position:absolute;left:44px;right:44px;bottom:30px;}
.prog{display:flex;align-items:center;gap:7px;height:10px;margin-bottom:18px;}
.seg{height:5px;border-radius:999px;background:var(--off);flex:1;}
.seg.on{background:var(--on);height:5px;}
.seg.cur{position:relative;}
.dot{width:13px;height:13px;border-radius:50%;background:var(--on);box-shadow:0 0 0 4px #fbe7d9;}
.fbar{display:flex;align-items:center;justify-content:space-between;}
.fbar .pg{font-size:16px;color:#7a6e62;min-width:52px;}
.fbar .nm{font-size:17px;color:var(--ink);font-weight:500;}
.fbar .ic{display:flex;gap:12px;align-items:center;color:#9a8c7d;}
.cc{border:1.5px solid #c9bba9;border-radius:6px;padding:1px 6px;font-size:12px;font-weight:700;color:#8c7e6f;font-family:'JetBrains Mono',monospace;}
"""

SPARK = ('<svg class="spark" viewBox="0 0 24 24" fill="none">'
         '<path d="M12 0c.5 6 5.5 11 12 11-6.5 0-11.5 5-12 13-.5-8-5.5-13-12-13 6.5 0 11.5-5 12-11z"'
         ' fill="#c75a33"/></svg>')

RAYS = ('<svg class="rays" viewBox="0 0 560 970" preserveAspectRatio="xMidYMin slice">'
        + "".join(f'<path d="M560 150 L{560-220} {150} L560 {150+i*55} Z" fill="#f0dcc6" opacity="0.5"/>'
                  for i in range(0))  # placeholder; real rays below
        + ''.join(
            f'<polygon points="560,120 {560-260},{120+(k-4)*34} {560-260},{120+(k-3)*34}" fill="#f1dec9" opacity="0.55"/>'
            for k in range(9))
        + '</svg>')


def esc(s):
    return html.escape(s, quote=True)


def header(tag):
    return (f'<div class="hdr"><div class="brand">{SPARK}<span class="yt"></span>'
            f'<span>YouTube Agent Pro</span></div>'
            f'<span class="tag">{esc(tag)}</span></div><div class="rule"></div>')


def footer(n, total, name):
    segs = []
    for i in range(1, total + 1):
        if i < n:
            segs.append('<div class="seg on"></div>')
        elif i == n:
            segs.append('<div class="seg on cur"></div><div class="dot"></div>')
        else:
            segs.append('<div class="seg"></div>')
    prog = '<div class="prog">' + "".join(segs) + '</div>'
    return (f'<div class="ftr">{prog}<div class="fbar">'
            f'<span class="pg">{n} / {total}</span>'
            f'<span class="nm">{esc(name)}</span>'
            f'<span class="ic"><span class="cc">CC</span>'
            f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#9a8c7d" stroke-width="2">'
            f'<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/></svg>'
            f'</span></div></div>')


def title(eyebrow, main_html):
    return f'<div class="eyebrow">{esc(eyebrow)}</div><h1>{main_html}</h1>'


def skill(cmd, needs, desc, try_cmd=None, compact=False):
    cmd_html = f'<span class="cmd"><b>/</b>{esc(cmd[1:]) if cmd.startswith("/") else esc(cmd)}</span>'
    needs_html = f'<span class="pill">{esc(needs)}</span>' if needs else ''
    t = '' if compact else (f'<div class="try"><b>TRY</b>{esc(try_cmd)}</div>' if try_cmd else '')
    cls = "skill cmp" if compact else "skill"
    return (f'<div class="{cls}"><div class="top">{cmd_html}{needs_html}</div>'
            f'<p>{desc}</p>{t}</div>')


def page(tag, n, total, section, body):
    PAGES.append(f'<section class="page">{header(tag)}{body}{footer(n, total, section)}</section>')


TOTAL = 15

# 1 COVER ------------------------------------------------------------------
page("setup guide", 1, TOTAL, "Start", f"""{RAYS}
<div class="eyebrow" style="margin-top:40px;">24 SKILLS &middot; 11 TOOLS &middot; FREE &middot; MIT</div>
<h1 style="font-size:60px;margin-top:10px;">YouTube<br>Agent Pro<br><em>Setup guide.</em></h1>
<p class="lede" style="margin-top:16px;">An AI agent for YouTube in Claude Code: ideas, scripts,
hooks, titles, thumbnails, SEO and sponsorship.</p>
<div class="repocard" style="margin-top:22px;">
  <div class="t"><span style="font-size:18px;">&#128230;</span> youtube-agent-pro <span class="pill ok" style="font-size:13px;">Public</span></div>
  <p>Twenty-four Claude skills that run a YouTube channel, end to end.</p>
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
<a href="{REPO}"><div class="link" style="margin-top:14px;"><span class="ic">&#128279;</span>
  <span class="u">{REPO_SHORT}</span><span class="ext">&#8599;</span></div></a>
""")

# 2 WHAT YOU NEED ----------------------------------------------------------
page("before you start", 2, TOTAL, "What you need", """
""" + title("BEFORE YOU START", 'What you <em>need.</em>') + """
<div class="card"><h3>Claude Code</h3><p>The terminal app, the desktop app or an IDE. Skills install
and run here.</p></div>
<div class="card"><h3>Python 3</h3><p>Only for the 11 tools. Nothing to pip install. Check it:
<span class="ichip">python3 --version</span></p></div>
<div class="card"><h3>Ten minutes</h3><p>To write your voice file with /yt-voice. Skip it and the
scripts will not sound like you.</p></div>
<div class="eyebrow" style="margin-top:24px;">NOTHING ELSE</div>
<div class="row" style="margin-top:12px;">
  <span class="pill ok">&#10003; No signup</span>
  <span class="pill ok">&#10003; No API key</span>
  <span class="pill ok">&#10003; Nothing to connect</span></div>
<div class="soft"><h3>It writes. You upload.</h3><p>Nothing is published to YouTube for you.
<span class="ichip">/yt-viral</span> and <span class="ichip">/yt-collab</span> read public listings
only and never log in as you.</p></div>
""")

# 3 INSTALL A (marketplace) -----------------------------------------------
page("install · marketplace", 3, TOTAL, "Install", """
""" + title("THE EASY WAY", 'Add the <em>marketplace.</em>') + """
<div class="flow"><span class="c">1 add</span><span class="a">&#8594;</span>
  <span class="c">2 install</span><span class="a">&#8594;</span><span class="c">3 ready</span></div>
<div class="code"><div class="lbl">Claude Code</div><pre><span class="c">/plugin</span> marketplace add ahmedsakri/youtube-agent-pro
<span class="c">/plugin</span> install youtube-agent-pro</pre></div>
<div class="card" style="margin-top:18px;"><h3>What those two lines do</h3>
<p>The first registers this repo as a plugin marketplace. The second installs the plugin from it.
A marketplace in Claude Code is just a git repo with a <span class="ichip">marketplace.json</span>,
so there is nothing central to sign up for.</p></div>
<div class="card tight"><div class="row"><span class="pill ok">&#10003; installed</span>
<span style="font-size:17px;color:#5a524a;">all 24 /yt- skills are now ready</span></div></div>
<div class="dash"><b>Update later:</b> <span class="ichip">/plugin marketplace update youtube-agent-pro</span></div>
""")

# 4 INSTALL B/C/D ----------------------------------------------------------
page("install · B, C, D", 4, TOTAL, "Install", """
""" + title("OTHER WAYS", 'Prefer to do it <em>yourself?</em>') + """
<div class="skill"><div class="top"><span class="cmd">B &nbsp;Clone and copy</span>
  <span class="pill">global</span></div>
  <div class="code" style="margin-top:12px;"><div class="lbl">Terminal</div><pre>git clone https://github.com/ahmedsakri/youtube-agent-pro
cp -r youtube-agent-pro/skills/yt* ~/.claude/skills/</pre></div></div>
<div class="skill"><div class="top"><span class="cmd">C &nbsp;Project only</span>
  <span class="pill">one repo</span></div>
  <p>Copy the same <span class="ichip">yt*</span> folders into your project's
  <span class="ichip">.claude/skills/</span> instead. They then work in that project only.</p></div>
<div class="skill"><div class="top"><span class="cmd">D &nbsp;No Claude Code</span>
  <span class="pill">fallback</span></div>
  <p>Paste any single <span class="ichip">SKILL.md</span> at the top of a chat and it runs as a mode.
  You lose the Python tools, but the reasoning still works.</p></div>
<div class="dash" style="margin-top:14px;"><b style="color:var(--accent);">Not sure?</b> Use the
marketplace method (page 3). Two lines, it does the rest.</div>
""")

# 5 VOICE ------------------------------------------------------------------
page("voice.md", 5, TOTAL, "Voice file", """
""" + title("STEP 1 · TEN MINUTES", 'Teach it <em>your voice.</em>') + """
<p class="lede" style="max-width:34ch;">Every skill reads one file. You say the words out loud, so it
has to sound like you.</p>
<div class="card"><div class="row"><span class="pill ok">FASTEST</span>
  <h3 style="font-size:23px;">Let /yt-voice write it</h3></div>
  <p>Send three of your own videos or transcripts, then run <span class="ichip">/yt-voice</span>. It
  runs <span class="ichip">voiceprint.py</span> to measure how you actually talk and writes
  <span class="ichip">~/.claude/youtube/voice.md</span>.</p></div>
<div class="eyebrow" style="margin-top:22px;">WHAT THE FILE CAPTURES</div>
<div class="grid2">
  <div class="mini"><h5>Who I talk to</h5><p>One real person, not "creators".</p></div>
  <div class="mini"><h5>How I talk</h5><p>Your real transcripts, measured.</p></div>
  <div class="mini"><h5>Words I never use</h5><p>Unlock. Game-changer. Be specific.</p></div>
  <div class="mini"><h5>Words I do use</h5><p>Your tics. Keep them.</p></div>
  <div class="mini"><h5>What I won't claim</h5><p>Numbers and tools you can't show.</p></div>
  <div class="mini"><h5>My format</h5><p>Length, on camera or not.</p></div>
</div>
<div class="dash">No voice.md yet? Every skill asks for three of your videos first.</div>
""")

# 6 FULL RUN ---------------------------------------------------------------
page("the full run", 6, TOTAL, "The full run", """
""" + title("ONE VIDEO, START TO FINISH", 'The <em>full run.</em>') + """
<p class="lede" style="max-width:34ch;">Ask <span class="ichip">/yt</span>, the hub, and it routes
you. Or run the pipeline yourself, stopping at each gate.</p>
<div class="step"><div class="num">1</div><div><h4>Idea</h4><p>/yt-idea scores it before you film.</p></div></div>
<div class="step"><div class="num">2</div><div><h4>Brief</h4><p>/yt-brief turns it into a shot list.</p></div></div>
<div class="step"><div class="num">3</div><div><h4>Script</h4><p>/yt-script: hook panel, then the spoken script.</p></div></div>
<div class="step"><div class="num">4</div><div><h4>Package</h4><p>/yt-package + /yt-thumbnail, linted as one pairing.</p></div></div>
<div class="step"><div class="num">5</div><div><h4>Find it</h4><p>/yt-seo + /yt-chapters for the search surface.</p></div></div>
<div class="step"><div class="num">6</div><div><h4>Learn</h4><p>/yt-retention + /yt-analytics find the one fix.</p></div></div>
""")

# 7 MAKE THE VIDEO ---------------------------------------------------------
page("skills · 1 of 5", 7, TOTAL, "Make the video",
     title("THE 24 SKILLS · 1 OF 5", 'Make the <em>video.</em>')
     + skill("/yt-idea", "needs: a niche", 'A niche into scored ideas, before you film the wrong one.', '/yt-idea ideas for my channel')
     + skill("/yt-script", "needs: an idea", 'One idea in, a full script out. Five hooks off 21 formulas, scored.', '/yt-script why my videos get no views')
     + skill("/yt-brief", "needs: a script", 'A script into a shot list: framing, b-roll, gear, runtime.', '/yt-brief for the script above')
     + skill("/yt-chapters", "needs: a transcript", "Chapters checked against YouTube's rules, so they render.", '/yt-chapters transcript.srt'))

# 8 PACKAGE IT -------------------------------------------------------------
page("skills · 2 of 5", 8, TOTAL, "Package it",
     title("THE 24 SKILLS · 2 OF 5", 'Package <em>it.</em>')
     + skill("/yt-package", "needs: a draft title", 'Title and thumbnail text as one pairing. Checks truncation, repeats, vague words.', '/yt-package for this video')
     + skill("/yt-thumbnail", "needs: a title", 'The thumbnail as a concept: one idea, three elements, three words. Linted and A/B’d.', '/yt-thumbnail concepts for this')
     + skill("/yt-seo", "needs: a topic", 'The description, the tags worth keeping, and three queries to win.', '/yt-seo write my description')
     + '<div class="dash">The pairing is the unit. A thumbnail that repeats the title wastes half the click surface, so these are linted together.</div>')

# 9 READ THE NUMBERS -------------------------------------------------------
page("skills · 3 of 5", 9, TOTAL, "Read the numbers",
     title("THE 24 SKILLS · 3 OF 5", 'Read the <em>numbers.</em>')
     + skill("/yt-analytics", "needs: a Studio export", 'The funnel read for the one number holding a video back: impressions, CTR, retention.', '/yt-analytics read my stats')
     + skill("/yt-retention", "needs: retention CSV", 'The retention curve read properly: the hook leak, the cliffs, the slide.', '/yt-retention retention.csv')
     + skill("/yt-funnel", "needs: channel page", 'The trailer, above-the-fold and sections that turn browsers into subscribers.', '/yt-funnel fix my channel page')
     + skill("/yt-audit", "needs: channel link", 'The whole channel, ending in ONE fix, not twenty.', '/yt-audit youtube.com/@you'))

# 10 GROW IT ---------------------------------------------------------------
page("skills · 4 of 5", 10, TOTAL, "Grow it",
     title("THE 24 SKILLS · 4 OF 5", 'Grow <em>it.</em>')
     + skill("/yt-viral", "needs: your niche", 'What works in your niche, ranked by multiple over each channel’s own median.', compact=True)
     + skill("/yt-trend", "needs: your niche", 'A 90-day calendar: seasonal demand and the evergreen-to-timely mix.', compact=True)
     + skill("/yt-series", "needs: a big topic", 'A series or playlist as a binge: each video earns the next click.', compact=True)
     + skill("/yt-collab", "needs: your niche", 'Channels to collaborate with, by audience overlap, plus the pitch.', compact=True)
     + skill("/yt-endscreen", "needs: retention", 'End screens and cards placed to keep the session going.', compact=True))

# 11 MULTIPLY / BUSINESS ---------------------------------------------------
page("skills · 5 of 5", 11, TOTAL, "Multiply + business",
     title("THE 24 SKILLS · 5 OF 5", 'Multiply, then <em>earn.</em>')
     + skill("/yt-shorts", "needs: a transcript", 'The Shorts hiding inside a long video, each with a new first line.', compact=True)
     + skill("/yt-repurpose", "needs: a transcript", 'One video into a thread, a LinkedIn post, a newsletter and a blog outline.', compact=True)
     + skill("/yt-plan", "needs: your hours", 'A week that fits your hours: one anchor, one cheap one, three Shorts.', compact=True)
     + skill("/yt-sponsor", "needs: your views", 'A defensible rate card, the reply to the brand, and the integration.', compact=True)
     + skill("/yt-comment", "needs: pasted comments", 'Comments triaged into piles, replies in your voice, which to pin.', compact=True))

# 12 TOOLS -----------------------------------------------------------------
TOOLS = [
    ("ideascore.py", "Scores a video idea on four axes.", "yt-idea/ideascore.py --idea \"...\""),
    ("hookscore.py", "Scores a hook on five properties.", "yt-script/hookscore.py --hook \"...\""),
    ("title.py", "Lints a title and thumbnail as one pair.", "yt-package/title.py --title \"...\""),
    ("thumblint.py", "Lints a thumbnail concept.", "yt-thumbnail/thumblint.py --concept \"...\""),
    ("funnel.py", "Finds the binding constraint.", "yt-analytics/funnel.py --impressions ..."),
    ("retention.py", "Where viewers left, and what was said.", "yt-retention/retention.py file.csv"),
    ("ratecard.py", "A sponsorship rate from your views.", "yt-sponsor/ratecard.py --views 12000"),
    ("voiceprint.py", "Measures how you actually talk.", "yt-voice/voiceprint.py best.txt"),
    ("deadair.py", "Edit decision list from a transcript.", "yt-edit/deadair.py file.srt"),
    ("chapters.py", "Chapters that pass YouTube's rules.", "yt-chapters/chapters.py file.srt"),
    ("swipe.py", "Outliers by own-channel multiple.", "yt-viral/swipe.py file.json --min 2.0"),
]
tool_cards = "".join(
    f'<div class="skill" style="padding:9px 18px;margin-top:8px;"><div class="top">'
    f'<span class="cmd" style="font-size:15px;color:var(--accent);">{esc(t[0])}</span>'
    f'<span style="font-size:15px;color:#6a5e53;">{esc(t[1])}</span></div></div>'
    for t in TOOLS)
page("11 tools", 12, TOTAL, "The 11 tools",
     title("UNDER THE HOOD", 'Eleven <em>tools.</em>')
     + '<p class="lede" style="max-width:44ch;margin-top:12px;">Plain Python 3. No installs. Claude '
       'runs them for you. They are heuristics, not predictors, and they are why the skills are more '
       'than prompts.</p>'
     + tool_cards)

# 13 THE GATE --------------------------------------------------------------
page("the gate", 13, TOTAL, "The gate",
     title("THE ONE RULE", 'Nothing <em>publishes.</em>')
     + '<p class="lede" style="max-width:34ch;">Every skill writes. You upload. That is the whole '
       'difference between this and a bot that runs your channel into the ground.</p>'
     + '<div class="card"><h3>Every run ends the same way</h3><p>A block you copy, and one question. '
       'You decide, every time, with the words in front of you.</p></div>'
     + '<div class="soft" style="text-align:center;padding:30px 24px;">'
       '<h3 style="font-size:34px;">Ship it, or change it?</h3></div>'
     + '<div class="grid2" style="margin-top:20px;">'
       '<div class="mini"><h5>Reads, never scrapes</h5><p>/yt-viral and /yt-collab use public '
       'listings only. Never your login.</p></div>'
       '<div class="mini"><h5>Invents no numbers</h5><p>If a skill wants a figure it does not have, '
       'it asks you or writes without it.</p></div></div>')

# 14 QUICK FIXES -----------------------------------------------------------
def fix(q, a):
    return f'<div class="card tight"><h3 style="font-style:italic;color:var(--accent);font-size:23px;">{q}</h3><p>{a}</p></div>'
page("fixes", 14, TOTAL, "Fixes",
     title("IF IT BREAKS", 'Quick <em>fixes.</em>')
     + fix("/yt- commands not found", 'Close and reopen Claude Code once. Then run '
           '<span class="ichip">ls ~/.claude/skills | grep yt-</span> and you should see 24 folders.')
     + fix("python3: command not found", "Install Python 3 from python.org. The tools need nothing else.")
     + fix("/yt-viral skipped a channel", "It needs about four videos per channel to find a median. Add more videos or another channel.")
     + fix("A score looks wrong", "The scorers are heuristics. A low score means look again, not a verdict.")
     + fix("Update to the latest", 'Run <span class="ichip">/plugin marketplace update youtube-agent-pro</span>, or git pull your clone and copy the folders again.'))

# 15 GET IT ----------------------------------------------------------------
page("get the skill", 15, TOTAL, "Get it", f"""{RAYS}
""" + title("THE LINK", 'Get the <em>skill.</em>') + f"""
<div class="repocard"><div class="t"><span style="font-size:18px;">&#128230;</span>
  youtube-agent-pro <span class="pill ok" style="font-size:13px;">Public</span></div>
  <p>Twenty-four Claude skills that run a YouTube channel. Use it, change it, ship it.</p>
  <div class="row" style="margin-top:12px;"><span class="pill gray">MIT License</span>
  <span class="pill ok">Open source</span><span class="pill gray">24 skills</span></div></div>
<a href="{REPO}"><div class="link"><span class="ic">&#128279;</span>
  <span class="u">{REPO_SHORT}</span><span class="ext">&#8599;</span></div></a>
<div class="card"><h3>Your first ten minutes</h3>
  <div class="check"><span class="tick">&#10003;</span><span>Add the marketplace and <b>install</b> in Claude Code</span></div>
  <div class="check"><span class="tick">&#10003;</span><span>Run <b>/yt-voice</b> to write your voice.md from three videos</span></div>
  <div class="check"><span class="tick">&#10003;</span><span>Run <b>/yt-idea</b>, then <b>/yt-script</b> on the winner</span></div></div>
<div class="dash" style="margin-top:16px;">Built by <b>Ahmed Sakri</b>. Based on the open-source
<b>youtube-agent-skill</b> by Jake Schincariol (MIT).</div>
<div class="closer"><div class="p">Every skill ends with one question.</div>
  <div class="q">Ship it, or change it?</div></div>
""")

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500;1,9..144,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
{''.join(PAGES)}
</body></html>"""

with open("guide.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"wrote guide.html with {len(PAGES)} pages")
