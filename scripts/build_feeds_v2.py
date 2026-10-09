#!/usr/bin/env python3
"""Build x-official.xml and x-media-kol.xml from raw/posts.json (XRHOT X feeds v2)."""
# See README.md for rules. Input: raw/posts.json produced by X MCP collection.
import json, re, os
from datetime import datetime, timezone
from collections import defaultdict, Counter

OFFICIAL = {"MetaVR_Official","PICOXR","htcvive","BigscreenVR","XREAL_Global","RokidGlobal","getVITURE","rayneo_global","pimaxofficial","Play_for_dream","PICOXR_Dev"}
MEDIA_KOL = {"ARealityEvent","nathie","Dilmerv","kentbye"}
ALL = OFFICIAL | MEDIA_KOL

def expand_text(text, urlmap):
    if not text: return text
    out = text.replace('&amp;', '&')
    for tco, real in (urlmap or {}).items():
        if tco in out: out = out.replace(tco, real)
    for tco in re.findall(r'https://t\.co/\w+', out):
        out = out.replace(tco, '')
    out = re.sub(r'[ \t]+\n', '\n', out)
    out = re.sub(r'\n{3,}', '\n\n', out)
    out = re.sub(r'  +', ' ', out)
    return out.strip()

XR_KEEP = re.compile(
    r'\b(VR|MR|AR|XR|Quest|Vision Pro|visionOS|SteamVR|Steam Frame|PICO|Pico|VIVE|Meta VR|passthrough|'
    r'hand tracking|hand.?grab|microgesture|locomotion|headset|head.?set|smart glasses|AR glasses|'
    r'VR glasses|AI glasses|XREAL|SPECS|Horizon|Mixed Reality|Augmented Reality|Virtual Reality|'
    r'Bigscreen|Halo Mount|ISDK|Interaction SDK|Meta Connect|Unity.*XR|XR rendering|XR Simulator|'
    r'eyetracking|eye.?tracking|waveguide|spatial)\b', re.I)

def is_xr(text, quoted_text=None):
    blob = (text or '') + '\n' + (quoted_text or '')
    if XR_KEEP.search(blob): return True
    low = blob.lower()
    if 'unity spark' in low and not re.search(r'\b(xr|vr|quest)\b', low): return False
    if 'three.js' in low and 'megacity' in low: return False
    if re.search(r"i.?ll be in los angeles", low) and 'hit me up' in low: return False
    return True

def first_line(text, limit=120):
    t = text.strip().split('\n')[0].strip()
    return t[:limit].rstrip() if len(t) > limit else t

def to_rfc822_gmt(iso):
    dt = datetime.fromisoformat(iso.replace('Z','+00:00')).astimezone(timezone.utc)
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def build(posts_path='raw/posts.json'):
    posts = [p for p in json.load(open(posts_path)) if p.get('handle') in ALL]
    threads = defaultdict(list)
    for p in posts: threads[(p['handle'], p['conversation_id'])].append(p)
    stats_seen = Counter(p['handle'] for p in posts)
    stats_kept = Counter()
    merged = []
    for (handle, conv), parts in threads.items():
        parts = sorted(parts, key=lambda x: x['created_at'])
        roots = [p for p in parts if p['id'] == conv or not p.get('reply_to_id')]
        if not roots:
            root, rest = parts[0], parts[1:]
        else:
            root = sorted(roots, key=lambda x: x['created_at'])[0]
            rest = [p for p in parts if p['id'] != root['id']]
        urlmap = dict(root.get('urls') or {})
        for p in rest: urlmap.update(p.get('urls') or {})
        body = expand_text(root['text'], root.get('urls') or {})
        for p in rest: body += '\n\n' + expand_text(p['text'], p.get('urls') or {})
        qh, qt = root.get('quoted_handle'), root.get('quoted_text')
        if not qh:
            for p in rest:
                if p.get('quoted_handle'):
                    qh, qt = p['quoted_handle'], p['quoted_text']; break
        if qh and qt: body += f"\n\n引用 @{qh}：{qt}"
        body = expand_text(body, urlmap)
        if not re.sub(r'https?://\S+', '', body).strip(): continue
        if not is_xr(body, qt): continue
        if 'Spark sounds super interesting' in body and 'Unity Spark' in body: continue
        if "Unity’s ease of use is hard to beat" in body and 'Three.js' in (qt or ''): continue
        if "I’ll be in Los Angeles" in body and 'hit me up' in body: continue
        merged.append({'id': root['id'], 'handle': handle, 'created_at': root['created_at'],
                       'body': body, 'url': f'https://x.com/{handle}/status/{root["id"]}'})
        stats_kept[handle] += 1
    merged.sort(key=lambda x: x['created_at'], reverse=True)

    def write_rss(title, description, items, path):
        items = items[:100]
        last = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
        lines = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">',
            '  <channel>', f'    <title>{esc(title)}</title>',
            '    <link>https://github.com/poovabgh/xrhot-feeds</link>',
            f'    <description>{esc(description)}</description>',
            f'    <lastBuildDate>{last}</lastBuildDate>']
        for it in items:
            lines += ['    <item>', f'      <title>{esc(first_line(it["body"]))}</title>',
                f'      <link>{esc(it["url"])}</link>', f'      <guid isPermaLink="false">{esc(it["id"])}</guid>',
                f'      <pubDate>{to_rfc822_gmt(it["created_at"])}</pubDate>',
                f'      <dc:creator>{esc(it["handle"])}</dc:creator>',
                f'      <content:encoded><![CDATA[{it["body"]}]]></content:encoded>', '    </item>']
        lines += ['  </channel>', '</rss>', '']
        open(path,'w',encoding='utf-8').write('\n'.join(lines))
        return last, len(items)

    os.makedirs('feeds', exist_ok=True)
    off = [i for i in merged if i['handle'] in OFFICIAL]
    kol = [i for i in merged if i['handle'] in MEDIA_KOL]
    off_lbd, off_n = write_rss('X · XR 官方账号','MetaVR_Official / PICOXR / htcvive / BigscreenVR / XREAL_Global / RokidGlobal / getVITURE / rayneo_global / pimaxofficial / Play_for_dream / PICOXR_Dev 的帖子', off, 'feeds/x-official.xml')
    kol_lbd, kol_n = write_rss('X · XR 媒体和 KOL','ARealityEvent / nathie / Dilmerv / kentbye 的帖子', kol, 'feeds/x-media-kol.xml')
    return {'lastBuildDate': off_lbd, 'official': off_n, 'media_kol': kol_n,
            'per_account': {h: {'seen': stats_seen.get(h,0), 'kept': stats_kept.get(h,0)} for h in sorted(ALL)}}

if __name__ == '__main__':
    print(json.dumps(build(), ensure_ascii=False, indent=2))
