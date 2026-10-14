"""Every source paragraph of the DOCX must appear in the EPUB text (same rules as integrity.py)."""
import sys, re, zipfile, json, docx, html
lang, epub, src, js = sys.argv[1:5]
z = zipfile.ZipFile(epub)
txt = ' '.join(re.sub(r'<[^>]+>', ' ', z.read(n).decode()) for n in z.namelist() if n.endswith('.xhtml'))
k = lambda t: re.sub(r'[\W_]+', '', html.unescape(t).lower())
body = k(txt)
skip = {b['src'] for b in json.load(open(js)) if b['t'] == 'toc_src'}
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
miss, tot = [], 0
for i, el in enumerate(docx.Document(src).element.body.iterchildren()):
    if i in skip or not el.tag.endswith('}p'): continue
    t = ''.join(x.text or '' for x in el.iter(W + 't'))
    t = re.sub(r'^\s*\d+\s*[/.]\s*', '', t)
    t = re.sub(r'^(Part|Deel|Chapter|Hoofdstuk)\s+[\dIVX]+\s*[—–-]\s*', '', t)
    if t.strip() in ('Contents', 'Inhoud') or len(k(t)) < 3: continue
    tot += 1
    if k(t) not in body: miss.append((i, t[:90]))
print(f'{lang} EPUB: source paragraphs {tot}, found {tot - len(miss)}, not found {len(miss)}')
for m in miss: print('   ', m)
