# Routine prompt

Source of truth for the instructions the daily cloud routine runs. The routine
itself stores a copy in its trigger config — edit here first, then push the
change to the trigger.

- Routine: **Daily AI and design news digest** (`trig_01GFyqyBqQLCLfGyvE6rMKHi`)
- Schedule: `30 0 * * *` UTC = 06:00 IST daily
- Console: https://claude.ai/code/routines/trig_01GFyqyBqQLCLfGyvE6rMKHi
- Environment: Brisingr · model: claude-sonnet-5
- Tools: Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch

To apply an edit, paste the block below into the routine's instructions in the
console, or POST it to `/v1/code/triggers/{id}` as
`job_config.ccr.events[0].data.message.content`.

---

Build today's AI digest and push it to the akilxasp/ai-digest repo you have checked out.

STEP 1 — GATHER THE NEWS
Use web search to find the 6 best news articles from the last 24 hours, in English, across three domains: AI, AI tools, and Design. Check the date of the underlying news, not just the article's publish date — if the story it covers is more than 1 week old, skip it. Rank by relevance and recency, and try to cover all three domains rather than six of the same kind. Six slots means each one has to earn its place: prefer the story that changes what someone would do over the story that is merely loud. For each article record: headline, source name, one-sentence summary, canonical URL, and which of the three domains it belongs to.

STEP 2 — SCAN THE COMMUNITIES
Separately, find 4 genuinely interesting things from AI practitioner communities in the last 7 days: Reddit (r/LocalLLaMA, r/ClaudeAI, r/OpenAI, r/ChatGPTCoding, r/MachineLearning, r/StableDiffusion and similar), X/Twitter, Hacker News, and practitioner forums or Discords that get written up publicly.

What qualifies: things people BUILT (side projects, tools, agents, pipelines, self-hosted setups) and SKILLS or WORKFLOWS people are actually using — prompting patterns, agent-harness tricks, evaluation habits, model-routing setups, hard-won lessons. Prefer concrete and reproducible over speculation.

Only include items with a clearly positive community response: strong upvotes or points relative to that forum's norms, and comment threads that are appreciative or constructively engaged. Exclude anything ratioed, controversial, drama, doom-posting, culture-war, or thinly veiled marketing. If a thread's top comments are mostly criticism or argument, leave it out. Record for each: title, where it was posted (e.g. 'r/LocalLLaMA' or 'Hacker News'), the engagement signal in plain terms (e.g. '3.1k upvotes · 240 comments' or '780 points'), a one-to-two sentence summary of what it is and why people liked it, and the URL. Verify each URL resolves before using it. Aim for exactly 4; if fewer clear the bar, include only the ones that do — never pad this section. Keep these summaries tight: they sit in a narrow two-column layout, so aim for about 25 words.

STEP 3 — PICK 3 TOOLS FOR THE TOOLBOX
Find 3 pieces of software that put AI to work inside an existing workflow — the Cotypist and Granola end of the spectrum, not chatbots and not model releases. Think: an app that quietly drafts, transcribes, autocompletes, organises, or automates something a person already does daily. Small indie tools are very welcome; so are mature apps that recently added a genuinely useful AI feature.

For each: the tool name, a short kind-and-platform label (e.g. 'Meeting notes · macOS' or 'Email · Web'), one sentence on what it actually does for the user — concrete, no marketing language — and its official URL. Verify each URL returns HTTP 200. Keep summaries to about 20 words, since these sit in a narrow three-column layout.

Before choosing, grep the recent files in digests/ for any tool name you are considering. Do not feature a tool that appeared in the last 7 digests — pick something new.

STEP 4 — SYNTHESIZE
Identify emerging trends, innovations, new tools, or noteworthy insights that cut across the three domains. Then write a daily tip (2-3 sentences) on using AI tools effectively, grounded in today's news or a common use case.

STEP 5 — PICK AND CROP THREE ARTWORKS
The artwork must already be black and white in the original, because email clients ignore CSS filters. Query the Wikimedia Commons API with curl, for example:

curl -s -H 'User-Agent: ai-digest/1.0' 'https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrsearch=filetype:bitmap%20panorama%20engraving&gsrlimit=30&gsrnamespace=6&prop=imageinfo&iiprop=url|size|extmetadata&iiurlwidth=1400'

Vary the search terms each day so the art changes — engraving, etching, lithograph, woodcut, panorama, black and white photograph, astronomical chart, architectural drawing, botanical illustration, map. Keep only results where extmetadata LicenseShortName says public domain AND width/height >= 1.5. Pick three different ones at random: hero, deep dive, community.

Then crop each to the digest's 21:9 ratio using the script in the repo:

  python3 tools/crop.py '<thumburl>' YYYY-MM-DD-hero
  python3 tools/crop.py '<thumburl>' YYYY-MM-DD-feature
  python3 tools/crop.py '<thumburl>' YYYY-MM-DD-community

(using today's date). Each run writes assets/<slug>.jpg and prints the URL to use in the template — use exactly that printed URL, not the Wikimedia one. The script installs Pillow itself if missing. Commit the three files in assets/ along with the digest.

Write a short credit for each: artwork title, artist, year if known, then 'public domain, Wikimedia Commons'.

STEP 6 — BUILD THE PAGE
Read template.html at the repo root. Copy it to digests/YYYY-MM-DD.html using today's date (UTC). Replace every {{PLACEHOLDER}} in that copy:
  {{DIGEST_TITLE}} - 2-4 words naming the day's dominant theme, uppercase reads best
  {{EDITION_LABEL}} - DAILY AI DIGEST
  {{DATE}} - today's date, e.g. 23 JULY 2026
  {{ISSUE_NO}} - number of files already in digests/ plus one
  {{SOURCE_COUNT}} - count of distinct sources used
  {{READ_TIME}} - estimate, e.g. 5 MIN
  {{DIGEST_LEDE}} - 2-3 sentence hook. This is the only overview in the digest, so make it carry the day.
  {{HERO_IMAGE}} / {{HERO_IMAGE_CREDIT}} - first cropped artwork
  {{FEATURE_IMAGE}} / {{FEATURE_IMAGE_CREDIT}} - second cropped artwork
  {{COMMUNITY_IMAGE}} / {{COMMUNITY_IMAGE_CREDIT}} - third cropped artwork
  {{FEATURE_TITLE}} / {{FEATURE_BODY}} - the cross-domain trends from step 4. Analysis only — the tip goes in its own section, do not repeat it here.
  {{DAILY_TIP}} - the daily tip from step 4, plain sentences with no 'Daily tip:' prefix (the section is already labelled)
  {{FEATURE_STAMP}} - today's date
  {{ARCHIVE_URL}} - https://github.com/akilxasp/ai-digest/tree/main/digests
  {{FOOTER_LEFT}} - AI DIGEST — AUTOMATED DAILY BRIEF
  {{FOOTER_RIGHT}} - today's date

Articles: the block between <!-- ITEM_TEMPLATE_START --> and <!-- ITEM_TEMPLATE_END --> is one article card, one per row. Duplicate it once per article from step 1 — 6 articles means 6 cards — and fill {{ITEM_TITLE}}, {{ITEM_SOURCE}}, {{ITEM_TAG}} (AI, AI TOOLS, or DESIGN), {{ITEM_SUMMARY}}, {{ITEM_URL}}, and {{ITEM_COLOR}}. For {{ITEM_COLOR}} give each article a different color picked at random from this palette, so no two adjacent cards match: #f4c046 #e94f37 #3f88c5 #44bba4 #d81e5b #8e6c8a #f26419 #2e933c #5762d5 #c05299.

Community items: the block between <!-- COMMUNITY_ROW_START --> and <!-- COMMUNITY_ROW_END --> is a TWO-COLUMN row holding two items — left cell uses the _A placeholders, right cell the _B ones. Duplicate this row once per PAIR, so 4 items means exactly 2 rows. Fill {{COMMUNITY_TITLE_A}}, {{COMMUNITY_SOURCE_A}}, {{COMMUNITY_SIGNAL_A}}, {{COMMUNITY_SUMMARY_A}}, {{COMMUNITY_URL_A}} and the matching _B set.

Toolbox: the block between <!-- TOOL_ROW_START --> and <!-- TOOL_ROW_END --> is a THREE-COLUMN row — _A, _B, _C left to right. Three tools means exactly one row, used as-is. Fill {{TOOL_NAME_A}}, {{TOOL_KIND_A}}, {{TOOL_SUMMARY_A}}, {{TOOL_URL_A}} and the matching _B and _C sets.

If any row ends up with unused cells (an odd community item, or fewer than 3 tools), keep those <td> elements so the filled columns keep their width, but delete everything inside them — every div and the anchor — leaving only &nbsp;. Do not merely blank the placeholders, or an empty cell ends up with a stray 'View thread' or 'Visit' link pointing nowhere.

Remove all six HTML comment markers from the finished file.

Do not restyle the template. It is written to survive Gmail: literal hex colors, table layout, inline styles. Fill the placeholders and change nothing else.

STEP 7 — VERIFY, THEN PUSH
Run: grep -o '{{[A-Z_]*}}' digests/YYYY-MM-DD.html
It must print nothing. If anything prints, fix it before continuing — the email workflow rejects files with leftover placeholders and no digest goes out.
Also confirm no 'View thread' or 'Visit' link is left in an empty cell, and that all three <img> tags point at raw.githubusercontent.com URLs rather than Wikimedia.
Then commit the digest and the three assets/ images to main and push.

The push triggers the 'Email digest' GitHub Action, which mails the styled HTML automatically. Do not create an artifact and do not try to send email yourself.

If fewer than 6 articles qualify, include the ones you found and say so plainly in the lede. Do not invent articles, sources, community threads, engagement numbers, tools, or URLs to fill space.
