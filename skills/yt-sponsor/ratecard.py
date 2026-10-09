#!/usr/bin/env python3
"""ratecard.py - a defensible sponsorship rate from your own view numbers.

    python3 ratecard.py --views 12000 --niche tech
    python3 ratecard.py --views 12000 --niche finance --placement integrated --json

Sponsorship is priced on a CPM - a price per thousand views - that varies by niche because a
thousand finance viewers are worth more to an advertiser than a thousand gaming viewers. This takes
your realistic per-video views (use the median of your last 10, NOT your best) and a niche, and
returns a low/mid/high band plus the three placement tiers advertisers actually buy.

  niches:     finance, b2b, tech, education, health, marketing, general, lifestyle, gaming, entertainment
  placements: integrated (60-90s mid-roll, the default), dedicated (whole video), mention (shout-out)

THESE ARE NEGOTIATION ANCHORS, NOT A PRICE LIST. Real deals move on audience geography, how engaged
your comments are, whether it is exclusive, and how badly the brand wants your specific viewers.
The CPM bands are widely cited industry ranges, not a quote. Use the mid as your opening ask and
the high as the number you do not apologise for.
"""
import json, sys

# niche -> (low, mid, high) USD CPM for an integrated placement, commonly cited 2024-25 ranges
CPM = {
    "finance":       (25, 45, 70),
    "b2b":           (25, 40, 65),
    "tech":          (18, 30, 50),
    "education":     (15, 25, 40),
    "health":        (18, 30, 45),
    "marketing":     (20, 35, 55),
    "general":       (12, 20, 30),
    "lifestyle":     (10, 18, 28),
    "gaming":        (8, 14, 22),
    "entertainment": (6, 12, 20),
}
PLACEMENT = {
    "mention":    0.4,
    "integrated": 1.0,
    "dedicated":  2.2,
}


def card(views, niche, placement):
    niche = niche.lower()
    placement = placement.lower()
    if niche not in CPM:
        niche = "general"
    base = CPM[niche]
    mult = PLACEMENT.get(placement, 1.0)
    low, mid, high = (round(views / 1000 * c * mult) for c in base)
    return {"views": views, "niche": niche, "placement": placement,
            "low": low, "mid": mid, "high": high}


def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]

    def flag(name, default=None):
        return a[a.index(name) + 1] if name in a else default

    if "--views" not in a:
        print(__doc__)
        sys.exit(1)
    views = float(flag("--views"))
    niche = flag("--niche", "general")
    placement = flag("--placement", "integrated")

    if placement == "all":
        rows = [card(views, niche, p) for p in ("mention", "integrated", "dedicated")]
    else:
        rows = [card(views, niche, placement)]

    if as_json:
        print(json.dumps(rows if len(rows) > 1 else rows[0], indent=1))
        return

    print(f"\n  {int(views):,} views/video   niche: {rows[0]['niche']}\n")
    for r in rows:
        print(f"    {r['placement']:<12} ${r['low']:>6,}  -  ${r['mid']:>6,}  -  ${r['high']:>6,}")
    print("\n    open at the mid. do not apologise for the high. the low is your walk-away floor,")
    print("    and a floor you say out loud, not one you discover halfway through the call.\n")


if __name__ == "__main__":
    main()
