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
        h0, plain0, allb0 = runs_html(el)
        style = par.style.name
        pieces = split_soft_breaks(h0, plain0, allb0) if mode == 'main' and '\n' in plain0 and not in_toc else [(h0, plain0, allb0)]
        for h, plain, allb in pieces:
          text = norm(plain)
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
          lab = next((k for k, v in LABELS.items() if key.lower() in {x.lower() for x in v}), None)
          if lab:
              blocks.append({'t': 'label', 'kind': lab, 'text': key, 'raw': text, 'src': idx}); continue
          nm = RE_NUM.match(text)
          if nm:
              body = h.split('/', 1)[1].lstrip() if '/' in h else h
              kind = 'numsub' if (bold and len(text) < 100 and not text.endswith('.')) else 'num'
              blocks.append({'t': kind, 'n': int(nm.group(1)), 'html': norm_html(strip_strong(body) if kind == 'numsub' else body),
                             'text': norm(nm.group(2)), 'bold': bold, 'src': idx}); continue
          if re.match(r'^[•·▪]\s', text):   # bullets typed by hand: marker becomes list formatting
              blocks.append({'t': 'bullet', 'html': norm_html(re.sub(r'^((?:<[^>]+>)*)\s*[•·▪]\s*', r'\1', h.lstrip())),
                             'text': text[1:].strip(), 'src': idx}); continue
          if el.find('.//' + qn('w:numPr')) is not None:
              blocks.append({'t': 'bullet', 'html': norm_html(h), 'text': text, 'src': idx}); continue
          if style.startswith('Heading') or (bold and len(text) < 90 and not text.endswith(('.', '?', '!'))):
              blocks.append({'t': 'sub', 'html': norm_html(strip_strong(h)), 'text': text, 'src': idx}); continue
          blocks.append({'t': 'p', 'html': norm_html(h), 'text': text, 'bold': bold, 'src': idx})
    return postprocess(blocks)


# Hard returns typed in the middle of a sentence (Word line-wrap accidents), by source paragraph index.
# Each listed paragraph is joined with the one that follows it. Reviewed by hand; see the QC report.
JOIN_WITH_NEXT = {'en': {1684, 1816, 1818}, 'nl': {1732, 1734, 1780}}
RE_SIGN = re.compile(r'^Harrie Kwinten, \d{4}$')


def postprocess(blocks):
    lang = LANG
    out = []
    for b in blocks:
        prev = out[-1] if out else None
        if prev and prev.get('_join') and b['t'] in ('p', 'bullet'):
            prev['html'] += ' ' + b['html']; prev['text'] += ' ' + b['text']; prev['joined'] = b['src']
            del prev['_join']; continue
        if b['t'] in ('p', 'bullet') and b['src'] in JOIN_WITH_NEXT[lang]:
            b['_join'] = True
        if b['t'] in ('sub', 'p') and RE_SIGN.match(b['text']):
            b = dict(b, t='signature', html=strip_strong(b['html']))
        elif prev and prev['t'] == 'img' and b['t'] == 'p' and len(b['text']) < 70:
            b = dict(b, t='caption')
        out.append(b)
    for b in out: b.pop('_join', None)
    return out


def split_soft_breaks(h, plain, allb):
    """Soft line breaks (Shift+Enter) inside a body paragraph become separate paragraphs.
    Open <strong>/<em> tags are closed at the break and reopened on the next piece."""
    hs, ps = h.split('\n'), plain.split('\n')
    out, carry = [], ''
    for hp, pp in zip(hs, ps):
        hp = carry + hp
        opened = []
        for tag in re.findall(r'<(/?)(strong|em)>', hp):
            if tag[0]: opened.remove(tag[1]) if tag[1] in opened else None
            else: opened.append(tag[1])
        closing = ''.join(f'</{t}>' for t in reversed(opened))
        carry = ''.join(f'<{t}>' for t in opened)
        inner = re.sub(r'</?(?:strong|em)>', '', hp).strip()
        pb = allb or (hp.strip().startswith('<strong>') and inner and
                      re.sub(r'<strong>.*?</strong>', '', hp + closing).strip() == '')
        out.append((hp + closing, pp, bool(pb)))
    return out


def strip_strong(h):
    return h.replace('<strong>', '').replace('</strong>', '')


def norm_html(h):
    h = h.replace(' ', ' ').replace('\t', ' ')
    h = re.sub(r' {2,}', ' ', h).strip()
    h = h.replace('\n', '<br/>')
    return h


LANG = 'en'

if __name__ == '__main__':
    LANG = sys.argv[4] if len(sys.argv) > 4 else ('nl' if 'nl' in sys.argv[2] else 'en')
    b = parse(sys.argv[1], sys.argv[3])
    json.dump(b, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter(x['t'] for x in b))
