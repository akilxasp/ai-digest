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
The email workflow hard-fails on leftover placeholders, so a half-filled digest
never reaches the inbox.

## Auto-send

`.github/workflows/email-digest.yml` fires on every push touching
`digests/**.html`, takes the newest file, and sends it as an HTML email through
the Resend API. `workflow_dispatch` re-sends manually (optional `file` input).

One-time setup:

1. Sign up at resend.com and create an API key (send access is enough).
2. Repo → Settings → Secrets and variables → Actions:
   - Secrets: `RESEND_API_KEY`, `MAIL_TO` (recipient)
   - Variables (optional): `MAIL_FROM` — defaults to
     `AI Digest <onboarding@resend.dev>`, which can only deliver to the address
     the Resend account was registered with. Verify a domain in Resend to send
     from your own address or to anyone else.
3. Repo → Settings → Pages → deploy from `main`, root. Gives each digest a
   stable URL that the email links to.

The routine only commits and pushes; CI owns the sending.

