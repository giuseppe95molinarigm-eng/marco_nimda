"""Check every source paragraph of the DOCX (after the original TOC) appears in the typeset PDF body text."""
import sys, re, pymupdf, docx, json
lang, pdf, src, js = sys.argv[1:5]
d = pymupdf.open(pdf)
parts = []
for p in d:
    for b in p.get_text('dict', sort=True)['blocks']:
        for l in b.get('lines', []):
            y0, y1 = l['bbox'][1], l['bbox'][3]
            if y1 < 0.80 * 72 or y0 > p.rect.height - 0.80 * 72: continue  # running head / folio zones
            parts.append(''.join(s['text'] for s in l['spans']) + '\n')
def k(t):
    t = t.lower().replace('­', '')
    t = re.sub(r'-\s*\n', '', t)            # print hyphenation at line ends
    return re.sub(r'[\W_]+', '', t)
body = k(''.join(parts))
blocks = json.load(open(js))
skip = {b['src'] for b in blocks if b['t'] == 'toc_src'}
doc = docx.Document(src)
els = list(doc.element.body.iterchildren())
miss, tot = [], 0
for i, el in enumerate(els):
    if i in skip or not el.tag.endswith('}p'): continue
    t = ''.join(x.text or '' for x in el.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
    t = re.sub(r'^\s*\d+/\s*', '', t)
    t = re.sub(r'^(Part|Deel|Chapter|Hoofdstuk)\s+[\dIVX]+\s*[—–-]\s*', '', t)
    if t.strip() in ('Contents', 'Inhoud'): continue
    kk = k(t)
    if len(kk) < 3: continue
    tot += 1
    if kk not in body: miss.append((i, t[:100]))
print(f'{lang}: source paragraphs checked {tot}, found {tot-len(miss)}, not found {len(miss)}')
for m in miss: print('   ', m)
