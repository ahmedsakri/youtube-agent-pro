---
name: yt-voice
description: >-
  Build or refresh the voice.md that every other skill in this pack reads -
  from the creator's own transcripts, measured not guessed. Use for "set up
  my voice", "write my voice.md", "make the scripts sound like me", "my
  scripts don't sound like me", or first-time setup of the YouTube pack.
---

# yt-voice

Every skill in this pack reads one file: `~/.claude/youtube/voice.md`. It is the highest-leverage ten
minutes in the whole pack, because on YouTube the words are said out loud and a script in the wrong
voice is unreadable on camera. This builds that file from how the creator actually talks, not how they
wish they did.

A tool lives here and it runs. It measures the things you cannot hear about yourself.

```bash
python3 voiceprint.py best-video.txt second.srt third.txt
```

## The move

1. **Get three transcripts** of the creator's own best-performing videos - the words they actually
   said, not their scripts. Pasted, `.srt`, `.vtt`, or ask them to export captions from Studio. If
   they have none (new channel), fall back to the interview below.
2. **Run `voiceprint.py`** across all of them. It returns mean sentence length, filler rate, the
   signature words they lean on, and the hype words they already use. These are measurements, not
   grades - a long sentence is not worse than a short one, it is just a thing the scripts must respect.
3. **Fill the six sections** of `templates/voice.md` from the measurements plus a short interview:
   - *Who I am talking to* - one named person, not "creators".
   - *How I actually talk* - from the mean sentence length and signature words.
   - *Words I never use* - the hype words to ban (the creator chooses from the ones voiceprint found).
   - *Words I do use* - the signature words. Keep them; they are what makes a script sound like them.
   - *What I will not claim* - numbers, results, tools they have not got. The skills refuse these.
   - *My format* - length, on-camera or not, intro or not, whether they swear.
4. **Write the file** to `~/.claude/youtube/voice.md`. Show it to the creator and have them correct
   the "who I am talking to" line in particular - that one they must own.

## New channel, no transcripts

Interview instead: who is the one viewer, three phrases that are theirs, three words that are not,
their format. Thinner than a voiceprint, but enough to start - and refresh it from real transcripts
after three uploads.

## What to hand back

- the written `~/.claude/youtube/voice.md`
- the voiceprint measurements that informed it
- one line: the one section to tighten after their next three videos

## The gate

This writes a local config file and nothing else - no publishing, no account access. The last line is
the question: **save this as your voice.md, or correct the audience line first?**
