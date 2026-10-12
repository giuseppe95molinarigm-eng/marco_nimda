"""Float large figures to avoid half-empty pages before them.

For each figure that leaves a big gap at the bottom of the preceding page, try moving it
past (or before) up to 3 neighbouring body paragraphs of the same section, or shrinking it
slightly (max 6.0 in tall). Keeps the option with the smallest gap. Text is never changed;
only the figure's position in the flow. The chosen layout is saved as JSON for reproducibility.
Usage: optimize_figures.py <lang> <blocks.json> <out.html> <out.pdf> <css> <layout.json>
"""
import sys, os, json, copy, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_print, weasyprint, pymupdf

lang, src, out_html, out_pdf, css, layout_json = sys.argv[1:7]
base = json.load(open(src))
build_print.MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(out_html)), 'media')
FLOW = ('p', 'num', 'bullet', 'sub', 'numsub')   # blocks a figure may float past (never labels, chapters, parts)
HEAD = ('sub', 'numsub', 'label')
BOTTOM = 9 * 72 - 0.8 * 72


def arrange(blocks, shifts):
    bl = copy.deepcopy(blocks)
    for fsrc, k in shifts.items():
        if k == 0: continue
        j = next(i for i, b in enumerate(bl) if b['t'] == 'img' and b['src'] == fsrc)
        n = 2 if j + 1 < len(bl) and bl[j + 1]['t'] == 'caption' else 1
        fig = bl[j:j + n]
        if k > 0:
            nb = bl[j + n:j + n + k]
            if len(nb) < k or any(b['t'] not in FLOW for b in nb) or nb[-1]['t'] in HEAD: return None
            if j > 0 and bl[j - 1]['t'] == 'label': return None
            bl[j:j + n + k] = nb + fig
        else:
            pb = bl[j + k:j]
            if len(pb) < -k or any(b['t'] not in FLOW for b in pb) or bl[j + k - 1]['t'] in HEAD: return None
            bl[j + k:j + n] = fig + pb
    return bl


def render(shifts, shrink):
    bl = arrange(base, shifts)
    if bl is None: return None
    html = build_print.build(lang, bl, 'media', css, shrink)
    open(out_html, 'w').write(html)
    doc = weasyprint.HTML(out_html).render()
    figpage = {}
    for i, p in enumerate(doc.pages):
        for a in p.anchors:
            if a.startswith('fig'): figpage[int(a[3:])] = i
    pdf = doc.write_pdf()
    return pdf, figpage


def costs(pdf, figpage):
    d = pymupdf.open(stream=pdf, filetype='pdf')
    res = {}
    for f, pi in figpage.items():
        if pi == 0: continue
        prev = d[pi - 1]
        ys = [l['bbox'][3] for b in prev.get_text('dict')['blocks'] for l in b.get('lines', [])
              if 0.8 * 72 - 2 < l['bbox'][1] < BOTTOM + 2 and ''.join(s['text'] for s in l['spans']).strip()]
        if not ys: res[f] = 0; continue
        # a gap only matters when the text before the figure page continues the same section
        res[f] = max(0.0, (BOTTOM - max(ys)) / 72) if prev.get_text().strip() else 0
        # figure on a chapter's first page or after a section-ending page: no cost
        top = d[pi].get_text().replace(' ', '').upper()[:12]
        if top.startswith(('CHAPTER', 'HOOFDSTUK')): res[f] = 0
    return res, len(d)


figs = [b['src'] for b in base if b['t'] == 'img' and b['src_file'] not in build_print.SKIP_IMG[lang]]
shifts, shrink = {f: 0 for f in figs}, set()
pdf, fp = render(shifts, shrink); c, npages = costs(pdf, fp)
print(lang, 'initial gaps (in):', {f: round(v, 2) for f, v in c.items() if v > 0.9})
CANDS = [(1, False), (2, False), (-1, False), (3, False), (-2, False), (0, True), (4, False), (-3, False), (5, False), (1, True), (-1, True), (6, False)]
for f in figs:
    if c.get(f, 0) <= 0.9: continue
    best = (c[f], 0, False, pdf, fp)
    for k, sh in CANDS:
        s2 = {**shifts, f: k}; sh2 = shrink | {f} if sh else shrink - {f}
        r = render(s2, sh2)
        if r is None: continue
        c2, _ = costs(*r)
        if c2.get(f, 99) < best[0] - 0.05 and all(c2.get(g, 0) <= max(c.get(g, 0), 0.9) + 0.05 for g in figs if g != f):
            best = (c2[f], k, sh, r[0], r[1])
        if best[0] < 0.5: break
    shifts[f] = best[1]; shrink = shrink | {f} if best[2] else shrink - {f}
    pdf, fp = best[3], best[4]; c, npages = costs(pdf, fp)
    print(f'  fig {f}: shift {best[1]:+d} shrink {best[2]} -> gap {best[0]:.2f} in')
# final render with chosen layout
pdf, fp = render(shifts, shrink); c, npages = costs(pdf, fp)
open(out_pdf, 'wb').write(pdf)
json.dump({'shifts': shifts, 'shrink': sorted(shrink)}, open(layout_json, 'w'), indent=1)
print(lang, 'pages', npages, 'remaining gaps > 0.9in:', {f: round(v, 2) for f, v in c.items() if v > 0.9})
