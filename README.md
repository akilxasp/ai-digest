# AI Digest

Single-file HTML template for the recurring AI digest. Monospace / high-contrast
technical-brief style: black hero, hairline rules, uppercase small-caps labels.

## Usage

The routine copies `template.html` to `digests/YYYY-MM-DD.html` and replaces the
placeholders below. No build step, no dependencies — open the file in a browser.

| Placeholder | Meaning |
|---|---|
| `{{DIGEST_TITLE}}` | Headline, 2–4 words, uppercase reads best |
| `{{EDITION_LABEL}}` | e.g. `DAILY AI DIGEST` |
| `{{DATE}}` | Edition date |
| `{{ISSUE_NO}}` / `{{SOURCE_COUNT}}` / `{{READ_TIME}}` | Hero meta column |
| `{{DIGEST_LEDE}}` | 2–3 sentence hook |
| `{{HERO_IMAGE}}` | Path or data URI; auto-desaturated by CSS |
| `{{EXECUTIVE_SUMMARY}}` | One paragraph, what matters today |
| `{{ITEM_*}}` | One story: title, source, tag, summary, url |
| `{{FEATURE_*}}` | Deep-dive title, body, corner stamp |
| `{{ARCHIVE_URL}}`, `{{FOOTER_LEFT}}`, `{{FOOTER_RIGHT}}` | Footer bits |

Repeat the block between `<!-- ITEM_TEMPLATE_START -->` and `ITEM_TEMPLATE_END`
once per story. The grid auto-fits; 3–5 items per row-width looks right.

Any unreplaced `{{...}}` renders literally — grep for `{{` before publishing.
