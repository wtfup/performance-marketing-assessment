# Platform notes (the facts the stations are built on)

Verified 2026-09-12 against the platform documentation and current practice. These are the limits and
mechanics the Ads Lab enforces; they are what a competent operator should already know by heart.

## Meta

| Fact | Value / rule | Why it matters |
|---|---|---|
| Primary text | 125 characters recommended (truncates behind "See More"); API accepts ~63,206 | Front-load the hook — ~99% never tap "See More" |
| Headline | 40 characters recommended (Feed 27); API accepts 255 | Truncated mid-word otherwise |
| Description | 25 characters recommended | Only reliably shown in Marketplace / Audience Network / Search Results |
| Text variations | Up to 5 per text field | Cheapest test lever there is |
| Hierarchy | Campaign → Ad set → Ad | Objective lives at campaign; audience, budget, placements, attribution at ad set |
| Objectives | Awareness · Traffic · Engagement · Leads · App promotion · Sales | Lead-gen for the ₹24k pass and walk-ins; Sales/app flow for the ₹100 pass |
| Budget | Campaign level (Advantage campaign budget / CBO) or ad set level — never both | Mixing them is a classic account error |
| Bid strategies | Highest volume, Cost per result goal, ROAS goal, Bid cap | Cost per result goal needs a value |
| Attribution | Set at ad set level; 7-day click / 1-day view is the default | Anything shorter under-credits the human close on high-ticket |
| Placements | Advantage+ placements vs manual; Audience Network can be excluded | Junk placements spend without converting |
| URL parameters | ad-level field; dynamic tokens like `{{campaign.name}}`, `{{ad.name}}` | Attribution dies without them; the ₹24k funnel needs the campaign name in the CRM |

## Google

| Fact | Value / rule | Why it matters |
|---|---|---|
| Responsive search ad | Up to 15 headlines (30 characters each), up to 4 descriptions (90 characters each); minimum 3 headlines / 2 descriptions to serve | The single most common build error |
| Pinning | Pin for control, costs flexibility | Pin only what must always show |
| Match types | Broad, phrase, exact; close variants apply; negatives take the same forms | Broad without negatives is how budgets die |
| Negatives | Brand terms as negatives inside non-brand campaigns | Otherwise you pay brand CPCs for traffic you'd get free |
| Sitelinks | ≤25 characters each; 4+ for a healthy ad | Free real estate |
| Bidding | Target CPA / Target ROAS / Maximize conversions / Maximize clicks / Manual CPC — note the June 2026 relabel: "Maximise conversions with a Target CPA" is now "Target CPA" | Strategy must match conversion volume; tCPA with no conversions is a trap |
| Targeting | Geo + language + networks (Search / Search Partners / Display) | Search campaigns should not silently include Display |
| Conversions | Conversion actions carry a "primary for goal" flag; only primary actions drive bidding | A non-primary lead action = bidding blind |
| Performance Max | Asset groups: headlines, long headlines, descriptions, images, logos, videos, audience signals, search themes | Different beast; build it only with assets to feed it |

## Sources verified

- Meta business help — attribution settings: https://www.facebook.com/business/help/460276478298895
- Meta creative text guidance + per-placement limits (2026 spec roundup): https://adsuploader.com/blog/meta-ad-copy-specs
- Meta dynamic URL parameters for UTM tracking: https://metricfixer.com/publications/online-advertising/meta-ads-dynamic-url-parameters-utm-tracking
- Google Ads Help — responsive search ads: https://support.google.com/google-ads/answer/7684791
- Google Ads Help — Target CPA bidding (June 2026 relabel): https://support.google.com/google-ads/answer/6268632
- Google Ads Help — Performance Max text asset best practices: https://support.google.com/google-ads/answer/15996555

Re-check before each hiring round: platform limits move (character counts, bidding labels, asset
specs), and this file is the reference the stations and the reviewer rubric both use.
