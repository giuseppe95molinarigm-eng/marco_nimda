"""Parse a manuscript DOCX into a flat list of semantic blocks (JSON).

Only structure is inferred; text is carried over verbatim (whitespace runs
collapsed). Every source paragraph index is kept so content integrity can be
checked against the DOCX afterwards.
"""
import sys, re, json, html, os, shutil
import docx
from docx.oxml.ns import qn

LABELS = {
    'statement': {'Statement', 'Stelling'},
    'example': {'Practical example', 'Praktijkvoorbeeld', 'Praktijkbeeld'},
    'reflection': {'Reflection questions', 'Reflectievragen'},
}
RE_PART = re.compile(r'^(Part|Deel)\s+([IVX]+)\s*[—–-]\s*(.+)$')
RE_CHAP = re.compile(r'^(Chapter|Hoofdstuk)\s+(\d+)\s*[—–-]\s*(.+)$')
RE_NUM = re.compile(r'^(\d+)/\s*(.*)$', re.S)
FRONT = {'Foreword', 'Introduction', 'Voorwoord', 'Inleiding'}
BACK = {'Afterword', 'Nawoord'}
NEXT = re.compile(r'^(Next steps for you to win the game|Volgende stappen voor jou om de wedstrijd te winnen)', re.I)


def norm(t):
    t = t.replace(' ', ' ').replace('\t', ' ')
    return re.sub(r' {2,}', ' ', t).strip()


def runs_html(el):
    """Inline HTML from runs, keeping bold/italic. Returns (html, plain, all_bold)."""
    out, plain, boldchars, total = [], [], 0, 0
    for r in el.iter(qn('w:r')):
        rpr = r.find(qn('w:rPr'))
        def on(tag):
            if rpr is None: return False
            e = rpr.find(qn(tag))
            return e is not None and e.get(qn('w:val')) not in ('0', 'false')
        b, i = on('w:b'), on('w:i')
        txt = ''
        for c in r:
            if c.tag == qn('w:t'): txt += c.text or ''
            elif c.tag == qn('w:tab'): txt += '\t'
            elif c.tag == qn('w:br') and c.get(qn('w:type')) != 'page': txt += '\n'
        if not txt: continue
        plain.append(txt)
        n = len(txt.strip())
        total += n
        if b: boldchars += n
        h = html.escape(txt)
        if i: h = f'<em>{h}</em>'
        if b: h = f'<strong>{h}</strong>'
        out.append(h)
    p = ''.join(plain)
    h = ''.join(out).replace('</strong><strong>', '').replace('</em><em>', '')
    return h, p, (total > 0 and boldchars == total)


def style_bold(par, d):
    s = par.style
    while s is not None:
        if s.font is not None and s.font.bold: return True
        s = s.base_style
    return False


def parse(path, media_out):
    d = docx.Document(path)
    rels = {r.rId: r.target_ref for r in d.part.rels.values()}
    blocks = []
    in_toc = False
    mode = 'main'   # main -> covercopy (excluded from interior) -> colophon (copyright page)
    for idx, el in enumerate(d.element.body.iterchildren()):
        tag = el.tag.split('}')[1]
        if tag == 'tbl':
            rows = []
            for tr in el.iter(qn('w:tr')):
                rows.append([norm(''.join(t.text or '' for t in tc.iter(qn('w:t')))) for tc in tr.iter(qn('w:tc'))])
            if any(c for r in rows for c in r):
                blocks.append({'t': 'table', 'rows': rows, 'src': idx})
            else:
                blocks.append({'t': 'empty_table', 'src': idx})
            continue
        if tag != 'p': continue
        par = docx.text.paragraph.Paragraph(el, d)
        for blip in el.iter(qn('a:blip')):
            rid = blip.get(qn('r:embed'))
            tgt = rels[rid]
            os.makedirs(media_out, exist_ok=True)
            shutil.copy(os.path.join(os.path.dirname(path), 'x', 'word', tgt), media_out)
            blocks.append({'t': 'img', 'src_file': os.path.basename(tgt), 'src': idx})
        h, plain, allb = runs_html(el)
        text = norm(plain)
        style = par.style.name
        if not text:
            continue
        bold = allb or style_bold(par, d)
        if text in ('Back Cover Text', 'Achterflaptekst'):
            mode = 'covercopy'; blocks.append({'t': 'covercopy_head', 'text': text, 'src': idx}); continue
        if text in ('Colophon', 'Colofon'):
            mode = 'colophon'; blocks.append({'t': 'colophon_head', 'text': text, 'src': idx}); continue
        if mode != 'main':
            blocks.append({'t': mode, 'html': norm_html(h), 'text': text, 'src': idx}); continue
        if style == 'Heading 1' and text in ('Contents', 'Inhoud'):
            in_toc = True; continue
        if in_toc:
            if style.startswith('Heading'): in_toc = False
            else:
                blocks.append({'t': 'toc_src', 'text': text, 'src': idx}); continue
        key = text.rstrip(':').strip()
        m = RE_PART.match(text); c = RE_CHAP.match(text)
        if text in FRONT:
            blocks.append({'t': 'front', 'title': text, 'src': idx}); continue
        if m and (bold or style.startswith('Heading')):
            blocks.append({'t': 'part', 'num': m.group(2), 'title': m.group(3), 'raw': text, 'src': idx}); continue
        if c and (bold or style.startswith('Heading')):
            blocks.append({'t': 'chapter', 'num': int(c.group(2)), 'title': c.group(3), 'raw': text, 'src': idx}); continue
        if key in BACK:
            blocks.append({'t': 'back', 'title': key, 'src': idx}); continue
        if NEXT.match(text) and bold:
            blocks.append({'t': 'back', 'title': text, 'src': idx}); continue
        lab = next((k for k, v in LABELS.items() if key in v), None)
        if lab:
            blocks.append({'t': 'label', 'kind': lab, 'text': key, 'raw': text, 'src': idx}); continue
        nm = RE_NUM.match(text)
        if nm:
            body = h.split('/', 1)[1].lstrip() if '/' in h else h
            blocks.append({'t': 'num', 'n': int(nm.group(1)), 'html': norm_html(body), 'text': norm(nm.group(2)),
                           'bold': bold, 'src': idx}); continue
        if el.find('.//' + qn('w:numPr')) is not None:
            blocks.append({'t': 'bullet', 'html': norm_html(h), 'text': text, 'src': idx}); continue
        if style.startswith('Heading') or (bold and len(text) < 90 and not text.endswith(('.', '?', '!'))):
            blocks.append({'t': 'sub', 'html': norm_html(strip_strong(h)), 'text': text, 'src': idx}); continue
        blocks.append({'t': 'p', 'html': norm_html(h), 'text': text, 'bold': bold, 'src': idx})
    return blocks


def strip_strong(h):
    return h.replace('<strong>', '').replace('</strong>', '')


def norm_html(h):
    h = h.replace(' ', ' ').replace('\t', ' ')
    h = re.sub(r' {2,}', ' ', h).strip()
    h = h.replace('\n', '<br/>')
    return h


if __name__ == '__main__':
    b = parse(sys.argv[1], sys.argv[3])
    json.dump(b, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter(x['t'] for x in b))
