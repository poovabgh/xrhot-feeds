# xrhot-feeds

Public RSS feeds for xrhot, generated from X posts (login-browser collection).
Station should poll these feeds and **enable “short posts count as body”** so posts under 280 chars are treated as full body, not summary.

## Active feeds (public raw URLs)

| Feed | Handle / topic | Items | Public URL |
|---|---|---:|---|
| `x-metavr_official` | MetaVR_Official | 1 | https://raw.githubusercontent.com/poovabgh/xrhot-feeds/main/feeds/x-metavrofficial.xml |
| `x-nathie` | nathie | 6 | https://raw.githubusercontent.com/poovabgh/xrhot-feeds/main/feeds/x-nathie.xml |
| `x-dilmerv` | Dilmerv | 10 | https://raw.githubusercontent.com/poovabgh/xrhot-feeds/main/feeds/x-dilmerv.xml |
| `x-arealityevent` | ARealityEvent | 2 | https://raw.githubusercontent.com/poovabgh/xrhot-feeds/main/feeds/x-arealityevent.xml |
| `x-keyword` | keyword mix | 15 | https://raw.githubusercontent.com/poovabgh/xrhot-feeds/main/feeds/x-keyword.xml |

## Skipped (already have site RSS)

- UploadVR
- Road to VR (RtoVR)

## Planned (0 posts in last 48h window — no feed file yet)

- kentbye
- PICOXR
- htcvive
- BigscreenVR

## RSS field rules

- `link`: `https://x.com/{handle}/status/{id}`
- `guid`: tweet id only, `isPermaLink="false"`
- `pubDate`: RFC822 with timezone (GMT)
- `content:encoded`: verbatim post text; `t.co` expanded to final URL when possible
- Newest first; keep up to 50 items
- Do not rewrite post text after publish

## Source snapshot

- Collection file: `xrhot-48h-collect.json` (46 posts, this batch uses 34 after skipping UploadVR/RtoVR)
- Generated: 2026-10-09 10:18 UTC

