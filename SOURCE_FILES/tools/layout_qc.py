"""Automated layout checks on a typeset print PDF."""
import sys, pymupdf
pdf, inside_in = sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 0.875
d = pymupdf.open(pdf)
W, H = d[0].rect.width, d[0].rect.height
issues = {'orphan_heading': [], 'short_page': [], 'outside_textblock': [], 'unsafe_edge': [], 'font': set()}
def is_heading(span):
    f = span['font']
    return ('Barlow' in f and span['size'] > 9.5) or ('Barlow' in f and 6.9 < span['size'] < 7.6)  # subheads, labels
for i, p in enumerate(d):
    no = i + 1
    left = inside_in * 72 if no % 2 else 0.60 * 72          # recto: gutter on the left
    right = W - (0.60 * 72 if no % 2 else inside_in * 72)
    lines = []
    for b in p.get_text('dict', sort=True)['blocks']:
        for l in b.get('lines', []):
            sp = [s for s in l['spans'] if s['text'].strip()]
            if not sp: continue
            for s in sp:
                if not s['font'].startswith('PTW-'): issues['font'].add(s['font'])
            lines.append((l['bbox'], sp))
    for (x0, y0, x1, y1), sp in lines:
        if x0 < 18 or y0 < 18 or x1 > W - 18 or y1 > H - 18: issues['unsafe_edge'].append(no)
        if 0.8 * 72 - 2 < y0 < H - 0.8 * 72 + 2 and (x0 < left - 2 or x1 > right + 2): issues['outside_textblock'].append((no, round(x0), round(x1), sp[0]['text'][:30]))
    body = [l for l in lines if 0.8 * 72 - 2 < l[0][1] < H - 0.8 * 72 + 2]
    if body:
        last = body[-1]
        if all(is_heading(s) for s in last[1]): issues['orphan_heading'].append((no, last[1][0]['text'][:40]))
        gap = (H - 0.8 * 72) - last[0][3]
        nxt = d[i + 1] if i + 1 < len(d) else None
        nxt_txt = nxt.get_text().replace(' ', '')[:12].upper() if nxt else ''
        chapter_end = (not nxt) or nxt_txt.startswith(('CHAPTER', 'HOOFDSTUK', 'PART', 'DEEL')) or nxt.get_text().strip() == '' \
            or any(k in nxt_txt for k in ('AFTERWORD', 'NAWOORD', 'NEXTSTEPS', 'VOLGENDE', 'INTRODUC', 'INLEIDING'))
        if gap > 72 and not chapter_end:
            img_next = bool(nxt and nxt.get_image_info() and nxt.get_image_info()[0]['bbox'][1] < 2 * 72)
            issues['short_page'].append((no, round(gap / 72, 2), 'image on next page' if img_next else ''))
print(pdf.split('/')[-2], 'pages', len(d), 'size', round(W / 72, 3), 'x', round(H / 72, 3))
for k, v in issues.items(): print(' ', k, len(v), sorted(v)[:40] if not isinstance(v, set) else v)
