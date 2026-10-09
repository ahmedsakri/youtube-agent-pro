---
name: yt-sponsor
description: >-
  Price a sponsorship, reply to a brand, and write the integration that
  does not tank retention. Builds a defensible rate card from your own view
  numbers. Use for "a brand emailed me", "how much do I charge", "rate
  card", "sponsorship", "sponsor integration script", or "is this offer
  fair".
---

# yt-sponsor

Most creators underprice the first deal and then read the sponsor segment like a hostage. This fixes
both: a rate you can defend, and an integration people do not skip.

A tool lives here and it runs.

```bash
python3 ratecard.py --views 12000 --niche tech --placement all
```

## Before you quote

1. Read `~/.claude/youtube/voice.md`. The integration is read out loud, in the creator's voice. A
   segment in ad-voice is the segment everyone scrubs past.
2. Use the **median of the last 10 videos**, not the best one and not the subscriber count. You are
   selling the views this video will realistically get.

## Pricing

Run `ratecard.py` with the median views and the niche. It returns low / mid / high for the three
placements advertisers actually buy: a mention, an integrated mid-roll (the default, 60-90s), and a
dedicated video. The CPM bands are industry ranges, not a quote - they are negotiation anchors.

- **Open at the mid.** Quote it without apologising.
- **The high** is the number for exclusivity, a tight deadline, or usage rights (they want to run it
  as an ad). Name those as the reason, not as a favour.
- **The low** is your walk-away floor - a floor you say out loud, not one you discover mid-call.

## The reply

Write the response to the brand: thank, confirm the median-views number plainly, quote the mid, and
ask the two questions that decide the real price - exclusivity, and whether they want usage rights.
Short. Brands trust a creator who answers like a business.

## The integration

Write the 60-90 second segment so it survives the retention graph:
- **Place it at a peak, not a cliff** - just after a payoff, never before the hook lands.
- **Make it relevant or make it honest** - "I use this / I do not, but here is the offer".
- **One claim, from the brief, that the creator will actually say** - never invent a product claim.
- **A clean hand-back** to the video so the retention curve recovers.

## What to hand back

- the rate card (three placements, three bands)
- the reply to the brand, ready to send
- the integration script in the creator's voice, with a placement note
- one line: the floor you will not go under

## The gate

This prices and drafts; it does not send email, sign anything, or publish. The last line is the
question: **send the reply, or hold for a better offer?**
