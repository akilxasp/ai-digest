# Notes

Decisions and traps behind this repo, written down so a fresh session does not
rediscover them the hard way.

## How it runs

```
06:00 IST — cloud routine (Brisingr) clones this repo
           → searches news + communities + tools
           → picks and crops 3 artworks into assets/
           → fills template.html into digests/YYYY-MM-DD.html
           → commits and pushes
push       → .github/workflows/email-digest.yml
           → sends the newest digest via Resend
also       → GitHub Pages serves the archive
```

Nothing depends on a local machine. The routine prompt lives in
[ROUTINE_PROMPT.md](ROUTINE_PROMPT.md); the trigger holds the live copy.

## Traps, each one paid for once

**Gmail strips CSS custom properties.** The first version used `var(--bg)`
throughout and arrived as unstyled black-on-white. Literal hex only.

**Gmail ignores flex and grid.** The card layout collapsed to a stacked column.
Multi-column sections are nested tables with percentage-width cells.

**Gmail drops most of `<style>`.** Every load-bearing rule is inline on the
element. The `<style>` block is browser-only polish.

**Email clients ignore `filter: grayscale()` and `object-fit`.** Artwork must be
monochrome at source (engravings, etchings, B/W photography) and is cropped to
21:9 by [tools/crop.py](tools/crop.py) before it ships.

**Cloudflare fronts the Resend API** and rejects the default `Python-urllib`
user agent with `error code: 1010`, which reads like an auth failure. The
workflow sets an explicit `User-Agent`.

**Nested-cell borders stop short.** A separator on the inner cells renders
inside the outer cell's 40px padding, 620px instead of 700px. Row separators go
on the outer cell; vertical rules go on the inner cells.

**Pages lags a push by about a minute** but the email fires immediately, so
images are served from `raw.githubusercontent.com`, not the Pages URL.

**Grid children default to `min-width: auto`** and refuse to shrink below their
longest unbreakable word — that is what pushed the hero title over the meta
column in the first web-only version.

## Conventions

- Digest file: `digests/YYYY-MM-DD.html`, UTC date
- Artwork: `assets/YYYY-MM-DD-{hero,feature,community}.jpg`, 1400×600
- A digest with any `{{PLACEHOLDER}}` left in it is rejected by the workflow
  before sending — fail closed, on purpose
- Sections in order: hero art, 6 articles, deep-dive art, analysis, daily tip,
  community art, 4 community items (2×2), 3 tools (1×3), archive

## Manual operations

Run the routine now (rebuilds and re-sends):
https://claude.ai/code/routines/trig_01GFyqyBqQLCLfGyvE6rMKHi

Re-send the existing digest without rebuilding:

```bash
gh workflow run "Email digest"
```
