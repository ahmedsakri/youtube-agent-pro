#!/usr/bin/env python3
"""funnel.py - find the one number holding a video back, from its Studio stats.

A video's reach is a chain: impressions -> click-through -> average view duration -> session.
One link is always the binding constraint. Fixing any other link is wasted work. This finds it.

    python3 funnel.py --impressions 42000 --ctr 3.1 --avd 2:10 --length 9:40
    python3 funnel.py --impressions 42000 --ctr 3.1 --avd 130 --length 580 --views 1300
    python3 funnel.py stats.csv            # a Studio "Overview" export, one video or many
    python3 funnel.py --impressions ... --json

Where the numbers live in Studio: Content -> a video -> Analytics -> Overview and Reach.
  impressions          Reach tab, "Impressions"
  ctr                  Reach tab, "Impressions click-through rate" (a percentage)
  avd                  Engagement tab, "Average view duration" (mm:ss or seconds)
  length               the video's runtime (mm:ss or seconds)

THE BANDS ARE RULES OF THUMB, NOT YOUR CHANNEL. CTR of 4-6% and 50%+ average-percentage-viewed are
the commonly cited "healthy" bands, but they move hard by niche, length and traffic source. A 2%
CTR on a video fed mostly to non-subscribers is not the same failure as 2% to your own subs. Read
the binding constraint as "look here first", never as a grade.
"""
import csv, json, os, re, sys


def dur(x):
    """accept 130, '2:10', '1:02:10' -> seconds."""
    if x is None:
        return None
    x = str(x).strip()
    if ":" in x:
        p = [float(n) for n in x.split(":")]
        s = 0
        for n in p:
            s = s * 60 + n
        return s
    try:
        return float(x)
    except ValueError:
        return None


def diagnose(impr, ctr, avd, length, views=None):
    out = {"impressions": impr, "ctr": ctr, "avd_s": avd, "length_s": length}
    pct = (avd / length * 100) if (avd and length) else None
    out["avg_pct_viewed"] = round(pct, 1) if pct is not None else None
    if views is None and impr and ctr:
        views = round(impr * ctr / 100)
    out["views_est"] = views

    links = []
    # each link: (name, healthy?, severity 0-1 where 1 = worst, message)
    if impr is not None:
        weak = impr < 1000
        links.append(("IMPRESSIONS", not weak, 1 - min(1, impr / 1000),
                      f"{impr:,} impressions - YouTube is barely showing this. "
                      "That is a packaging or a topic problem upstream of everything else."
                      if weak else f"{impr:,} impressions - YouTube is distributing it."))
    if ctr is not None:
        sev = max(0, min(1, (4.0 - ctr) / 4.0))
        links.append(("CTR", ctr >= 4, sev,
                      f"{ctr:.1f}% click-through - under 4% the title/thumbnail pairing is the leak. "
                      "Run /yt-package and /yt-thumbnail." if ctr < 4
                      else f"{ctr:.1f}% click-through - the pairing is earning its impressions."))
    if pct is not None:
        sev = max(0, min(1, (50.0 - pct) / 50.0))
        links.append(("RETENTION", pct >= 50, sev,
                      f"{pct:.0f}% average viewed - under 50% the video itself leaks. "
                      "Run /yt-retention on the export." if pct < 50
                      else f"{pct:.0f}% average viewed - the content holds."))

    out["links"] = [{"name": n, "ok": ok, "note": m} for n, ok, _, m in links]
    broken = [l for l in links if not l[1]]
    if broken:
        worst = max(broken, key=lambda l: l[2])
        out["binding_constraint"] = worst[0]
        out["verdict"] = worst[3]
    else:
        out["binding_constraint"] = None
        out["verdict"] = "no link is below its band - scale what works, make more of this one."
    return out


def show(r, label=None):
    if label:
        print(f"\n  == {label} ==")
    if r.get("views_est") is not None:
        print(f"  ~{r['views_est']:,} views"
              + (f"   {r['avg_pct_viewed']}% avg viewed" if r.get("avg_pct_viewed") is not None else ""))
    for l in r["links"]:
        print(f"    {'ok' if l['ok'] else 'x ':<3} {l['name']:<12} {l['note']}")
    bc = r["binding_constraint"]
    print(f"\n  FIX FIRST   {bc if bc else 'nothing - this one works, make more like it'}")


def from_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
        rdr = csv.DictReader(fh)
        hdr = {h.lower(): h for h in (rdr.fieldnames or [])}

        def pick(*names):
            for n in names:
                for k, orig in hdr.items():
                    if n in k:
                        return orig
            return None
        ci, cc, ca, cl, cv, ct = (pick("impression"), pick("click-through", "click through", "ctr"),
                                  pick("average view duration", "avg view"), pick("duration", "length"),
                                  pick("views"), pick("content", "title", "video"))
        for row in rdr:
            def g(c):
                return row.get(c) if c else None
            impr = g(ci)
            try:
                impr = float(str(impr).replace(",", "")) if impr else None
            except ValueError:
                impr = None
            ctr = g(cc)
            try:
                ctr = float(str(ctr).replace("%", "")) if ctr else None
            except ValueError:
                ctr = None
            views = g(cv)
            try:
                views = float(str(views).replace(",", "")) if views else None
            except ValueError:
                views = None
            rows.append((g(ct) or path, impr, ctr, dur(g(ca)), dur(g(cl)), views))
    return rows


def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]

    def flag(name):
        return a[a.index(name) + 1] if name in a else None

    files = [x for x in a if not x.startswith("--") and os.path.exists(x)]
    results = []
    if files:
        for label, impr, ctr, avd, length, views in from_csv(files[0]):
            results.append((label, diagnose(impr, ctr, avd, length, views)))
    elif "--impressions" in a or "--ctr" in a:
        r = diagnose(
            float(flag("--impressions")) if flag("--impressions") else None,
            float(flag("--ctr").replace("%", "")) if flag("--ctr") else None,
            dur(flag("--avd")), dur(flag("--length")),
            float(flag("--views")) if flag("--views") else None,
        )
        results.append((None, r))
    else:
        print(__doc__)
        sys.exit(1)

    if as_json:
        print(json.dumps([r for _, r in results] if len(results) > 1 else results[0][1], indent=1))
        return
    for label, r in results:
        show(r, label)
    print()


if __name__ == "__main__":
    main()
