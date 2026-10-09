# xrhot-feeds

Public RSS for xrhot: one aggregated X feed for XR (VR / MR / AR / AI glasses) posts collected via login browser.

Station should poll this feed and **enable “short posts count as body”** so posts under 280 chars are treated as full body, not summary.

## Primary feed (use this)

| Feed | Description | Items | Public URL |
|---|---|---:|---|
| `xrhot-x` | X · XR 聚合（多账号 + 主题检索） | 34 | https://raw.githubusercontent.com/poovabgh/xrhot-feeds/main/feeds/xrhot-x.xml |

Channel: title `X · XR 聚合`, link `https://github.com/poovabgh/xrhot-feeds`.  
Includes: MetaVR_Official, nathie, Dilmerv, ARealityEvent, and keyword extras.  
**Skipped** (they already have site RSS): UploadVR, Road to VR (RtoVR).

## Deprecated: per-account feeds

Older split files under `feeds/x-*.xml` may still exist for reference. **Do not subscribe to them** — use only `feeds/xrhot-x.xml`.

## RSS field rules

- `link`: `https://x.com/{handle}/status/{id}`
- `guid`: tweet id only, `isPermaLink="false"`
- `pubDate`: RFC822 with timezone (GMT)
- `dc:creator`: author handle
- `content:encoded`: verbatim post text; `t.co` expanded to final URL when possible
- Newest first; keep up to 50 items
- Do not rewrite post text after publish

## Source snapshot

- Collection file: `xrhot-48h-collect.json`
- Aggregate generated from previously published per-account bodies (verbatim merge)
