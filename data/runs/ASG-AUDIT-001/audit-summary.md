# ASG-AUDIT-001 — Stock Audit Brief

- Source: real Google Search Console export (asgdropshipping.com), period 2026-02-15 .. 2026-05-16.
- Mode: **basic** (GSC has no AI-citation dimension — `ai_cited` is null, status `flagged`).
- All recommendations are AI judgment (`derived:true`); only clicks/impressions/CTR/position are verified facts.

## Totals

- **Total pages audited: 98** (every row of gsc_pages.csv; README said 97, file has 98 — real data used).
- Article-type content pages: **73** (README estimated ~90).
- Page-type breakdown: article=73, category=3, home=1, product=1, system=20

## Counts per recommendation

| Recommendation | Count |
|---|---|
| KEEP | 27 |
| UPGRADE | 26 |
| REWRITE | 31 |
| KILL | 14 |

Priority spread: P0=3, P1=8, P2=18, P3=69

## Top 10 highest-impression underperformers (priority UPGRADE targets)

High impressions but CTR <1% or position >10 — fastest wins are title/meta/snippet rewrites, not new articles.

| # | Page | Impr | Clicks | CTR | Pos | Rec | Pri |
|---|---|---|---|---|---|---|---|
| 1 | how-long-does-stockx-take-to-ship | 21925 | 13 | 0.0006 | 9.1 | UPGRADE | P0 |
| 2 | usps-vs-ups | 8502 | 1 | 0.0001 | 17.4 | UPGRADE | P0 |
| 3 | dropshipping-automation-software | 3278 | 4 | 0.0012 | 29.9 | UPGRADE | P1 |
| 4 | what-happened-to-pandabuy-is-pandabuy-legit | 3042 | 1 | 0.0003 | 12.5 | UPGRADE | P0 |
| 5 | why-does-is-dhgate-legit | 2304 | 0 | 0.0000 | 26.3 | UPGRADE | P1 |
| 6 | aliexpress-vs-dhgate-in-2025-a-detailed-comparison | 911 | 0 | 0.0000 | 10.6 | UPGRADE | P1 |
| 7 | how-long-how-long-does-customs-clearance-take-from-china-to-the-usa-2 | 638 | 0 | 0.0000 | 7.4 | UPGRADE | P1 |
| 8 | how-to-marketplace-research-tool | 602 | 0 | 0.0000 | 26.2 | UPGRADE | P1 |
| 9 | how-long-dropshipping-companies-shopify | 562 | 0 | 0.0000 | 9.4 | UPGRADE | P1 |
| 10 | hypersku-vs-private-dropshipping-agent-which-is-better-in-2026 | 510 | 1 | 0.0020 | 7.3 | KEEP | P2 |

## Topic gaps (demand with no strong page)

Queries with real impressions, position >10 and 0 clicks — either no dedicated page or the page is buried:

- 'how long does stockx take to ship' — 552 impr, pos 14.3, 0 clicks (demand un-served)
- 'pandabuy' — 372 impr, pos 28.0, 0 clicks (demand un-served)
- 'is pandabuy legit' — 351 impr, pos 10.7, 0 clicks (demand un-served)
- 'best dropshipping automation software' — 320 impr, pos 39.1, 0 clicks (demand un-served)
- 'dropshipping automation' — 296 impr, pos 71.4, 0 clicks (demand un-served)
- 'what happened to pandabuy' — 295 impr, pos 10.2, 0 clicks (demand un-served)
- 'dropshipping automation software' — 285 impr, pos 56.1, 0 clicks (demand un-served)
- 'how long does stockx take to deliver' — 229 impr, pos 12.2, 0 clicks (demand un-served)
- 'what is pandabuy' — 180 impr, pos 11.2, 0 clicks (demand un-served)
- 'is dhgate legit' — 136 impr, pos 40.1, 0 clicks (demand un-served)
- 'is dhgate reliable' — 128 impr, pos 39.5, 0 clicks (demand un-served)
- 'stockx shipping time' — 124 impr, pos 18.5, 0 clicks (demand un-served)

## Caveat — AI citation needs manual review

Google Search Console reports clicks/impressions/CTR/position only. It **cannot** see whether a page is cited by Perplexity, Google AI Overview, ChatGPT, etc. The GEO side of every KEEP/KILL decision here is therefore provisional: a human must run the manual AI-citation pass before any page is killed, because a zero-GSC-click page can still be an AI-cited authority. This is why the envelope status is `flagged`, not `ok`.
