---
name: yt-seo
description: >-
  Write accurate YouTube titles, descriptions, tags, and optional hashtags
  in the creator's language, grounded in the actual video and search intent.
  Use for video SEO, description drafts, metadata revisions, keyword choices,
  or search discovery for Shorts and long-form videos.
---

# yt-seo

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow. Read
[YouTube's verified metadata guidance](references/youtube-metadata.md) for limits and surface-specific rules.

Help the right viewer recognize the actual video. Deliver the requested metadata without promising
ranking, virality, or additional views. Metadata relevance matters in Search; Shorts-feed performance
also depends on viewer response and personalization. Use the [analytics skill](../yt-analytics/SKILL.md)
when the request asks why reach is low, rather than diagnosing an SEO problem from views alone.

## Ground the metadata

- Read the supplied video, transcript, or reliable summary. Identify the actual topic, names,
  episode/version, key moment, and payoff. A filename alone is not evidence of what happens.
- Use the available creator profile or context. Preserve the requested language and tone, including
  intentional code-switching. Do not require a profile to write useful metadata.
- Choose one or two central topics/search phrases from the content. Use actual channel search-term
  data or verified research if supplied; otherwise label keyword choices as relevance judgments,
  not measured search demand. Never invent search volumes, quotes, identities, dates, or results.
- When adapting a batch, write a distinct description for each video from its own content. Reuse
  verified channel links and credits only where appropriate; do not copy an unrelated episode's facts.

## Title and description

1. **Title:** name the topic or moment early, with an accurate reason to watch. Use relevant wording
   naturally. No unrelated celebrity, trend, or outcome claims. Respect a request to keep the current
   title; otherwise use the [packaging skill](../yt-package/SKILL.md) for paired title/thumbnail options.
2. **Opening description:** write a clear, video-specific summary with the main phrase where it fits.
   The first lines should explain the content before channel boilerplate; no repeated keyword lists.
3. **Useful context:** add only relevant details, verified credits, resources, or a concise call to
   action. Do not pad the text to fill the field. Add chapters through the
   [chapters skill](../yt-chapters/SKILL.md) only when meaningful and supported by actual timestamps.
4. **Length:** validate the final title at no more than 100 characters and description at no more
   than 5,000 characters, including links and hashtags. These are platform limits; shorter preview
   targets are readability heuristics. Preview the opening lines when the relevant UI is available.

## Tags and hashtags

Tags have a limited discovery role. Use a small, relevant set for common misspellings, alternate
spellings, names, or abbreviations that need disambiguation; no fixed quota is required. Keep tags
in the tag field rather than appending a keyword dump to the description.

Hashtags are optional, topic-specific discovery links. Do not claim they are ineffective or required
for Shorts. If the user wants none, omit them. Otherwise prefer a few directly relevant hashtags;
never add unrelated trending terms. More than 60 causes YouTube to ignore all hashtags on that
content, but that limit is not a target. Distinguish hashtags from the separate tags field.

## Format, language, and links

- **Shorts:** URLs in Shorts descriptions and comments are not clickable. Do not write "click the
  link in this description." Refer to a verified channel profile link or an available related-video
  link only if that destination is actually configured. A URL may remain as a reference without a
  false click instruction.
- **Long-form:** include verified useful links when requested; external clickable links depend on
  the channel's advanced-feature access. Do not assume access or manufacture destinations.
- **Translations:** provide separate localized title/description drafts when requested. Preserve names
  and meaning, and use natural search wording in each language. Do not concatenate several full
  translations into one title. YouTube supports localized title/description fields; English-oriented
  text heuristics are not a validated multilingual SEO score.

## Deliver and check

Return the requested final title, description, tags, and optional hashtags as clearly separated
fields, with a short explanation of the chosen topic terms if useful. Verify factual consistency,
unique description, field lengths, language, links, and absence of stuffing. Flag missing source
facts outside the publishable copy; do not slip placeholders into a supposedly finished description.
This workflow drafts metadata. A Studio update requires the user's request and a separate available
account tool under its own controls; verify the saved result before reporting a change.
