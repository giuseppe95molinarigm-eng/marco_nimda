"""Build the print-interior HTML (WeasyPrint) from parsed manuscript blocks."""
import json, sys, html, os

CFG = {
    'en': dict(lang='en-GB', title='Prepare to Win', title_lines=['PREPARE', 'TO <span class="acc">WIN</span>'],
               subtitle='How a World Champion Thinks, Leads and Builds Winning Teams',  # wording/casing confirmed by client 14 Oct
               author='Harrie Kwinten', contents='Contents', part='Part', chapter='Chapter',
               labels={'statement': 'Statement', 'example': 'Practical example', 'reflection': 'Reflection questions'}),
    'nl': dict(lang='nl-NL', title='Winnen begint in de voorbereiding',
               title_lines=['WINNEN', 'BEGINT IN DE', '<span class="acc">VOORBEREIDING</span>'],
               subtitle='Hoe een wereldkampioen denkt, leidt en bouwt aan winnende teams',
               author='Harrie Kwinten', contents='Inhoud', part='Deel', chapter='Hoofdstuk',
               labels={'statement': 'Stelling', 'example': 'Praktijkvoorbeeld', 'reflection': 'Reflectievragen'}),
}
ALT = {
    'en': {'image2.png': 'Infographic: The 4 playing fields of business performance'},
    'nl': {'image2.png': 'Infographic: De 4 speelvelden van zakelijk presteren'},
}
# client request (requirements form): author photo as player/captain, full page facing the Chapter 6 opener
FACING_PHOTO = {6: ('author_captain.png', {
    'en': 'Harrie Kwinten as a field hockey player, wearing number 10 and the captain\'s armband',
    'nl': 'Harrie Kwinten als hockeyspeler met rugnummer 10 en de aanvoerdersband'})}
# ISBNs supplied by the client (14 Oct 2026); each print edition carries its own
ISBN = {('en', 'paperback'): '9789090435213', ('en', 'hardcover'): '9789090435008',
        ('nl', 'paperback'): '9789090435015', ('nl', 'hardcover'): '9789090434995'}
SKIP_IMG = {'en': {'image1.jpeg'}, 'nl': {'image1.jpg'}}  # cover artwork embedded at top of manuscript


def e(t): return html.escape(t)


def isbn_line(h, lang, edition):
    """Fill the manuscript's ISBN placeholder ("ISBN: [number]" / "ISBN") with this edition's number."""
    import re
    return re.sub(r'ISBN(?::\s*\[number\])?', f'ISBN {ISBN[(lang, edition)]}', h, count=1)


def runhead(t, limit=46):
    """Running heads must fit on one line: long chapter titles use the words before the colon."""
    return t if len(t) <= limit or ':' not in t else t.split(':')[0].strip()


def balance(t, per_line):
    """Break a display title into visually balanced lines (print only)."""
    import math
    words = t.split()
    nlines = max(1, math.ceil(len(t) / per_line))
    if nlines == 1 or len(words) < 2: return e(t)
    best = None
    def splits(ws, k):
        if k == 1: yield [ws]; return
        for i in range(1, len(ws) - k + 2):
            for rest in splits(ws[i:], k - 1): yield [ws[:i]] + rest
    for cand in splits(words, nlines):
        lens = [len(' '.join(x)) for x in cand]
        if max(lens) > per_line * 1.08: continue
        score = (max(lens) - min(lens)) + (3 if len(cand[-1]) == 1 else 0)
        if best is None or score < best[0]: best = (score, cand)
    if best is None: return e(t)
    return ' <br/>'.join(e(' '.join(x)) for x in best[1])


def build(lang, blocks, media_rel, css='print.css', shrink=(), edition='paperback'):
    c = CFG[lang]
    out = []
    toc = []
    # --- front matter
    out.append(f'<section class="halftitle"><p>{e(c["title"])}</p></section>')
    out.append('<section class="blankpage"></section>')
    out.append('<section class="titlepage"><div class="tp-title">' +
               ''.join(f'<span class="tl">{l}</span>' for l in c['title_lines']) +
               f'</div><div class="tp-rule"></div><p class="tp-sub">{e(c["subtitle"])}</p>'
               f'<p class="tp-author">{e(c["author"].upper())}</p></section>')
    colo = [b for b in blocks if b['t'] == 'colophon']
    out.append('<section class="copyright">' + ''.join(f'<p>{isbn_line(b["html"], lang, edition)}</p>' for b in colo) + '</section>')
    out.append('@@TOC@@')

    i = 0; n = len(blocks); sec = None; first = True
    def close():
        nonlocal sec
        if sec: out.append('</section>'); sec = None
    while i < n:
        b = blocks[i]; t = b['t']
        if t in ('toc_src', 'empty_table', 'covercopy_head', 'covercopy', 'colophon_head', 'colophon') or (t == 'img' and b['src_file'] in SKIP_IMG[lang]):
            i += 1; continue
        if t == 'front' or t == 'back':
            close(); aid = f's{b["src"]}'
            cls = 'front' + (' firstmain' if first else '')
            first = False
            out.append(f'<section class="{cls}"><h1 class="fm-title" id="{aid}">{e(b["title"])}</h1><div class="h-rule"></div>')
            sec = 'f'; toc.append(('fm', aid, b['title'])); i += 1; continue
        if t == 'part':
            close(); aid = f's{b["src"]}'
            out.append(f'<section class="part" id="{aid}"><p class="part-label">{e(c["part"]).upper()}</p>'
                       f'<p class="part-num">{b["num"]}</p><div class="part-rule"></div>'
                       f'<h1 class="part-title">{balance(b["title"], 22)}</h1></section>')
            toc.append(('part', aid, f'{c["part"]} {b["num"]}', b['title'])); i += 1; continue
        if t == 'chapter':
            close(); aid = f's{b["src"]}'
            after_part = i > 0 and blocks[i - 1]['t'] == 'part'
            if b['num'] in FACING_PHOTO:
                f, alts = FACING_PHOTO[b['num']]
                out.append(f'<section class="photopage"><img src="{media_rel}/{f}" alt="{e(alts[lang])}"/></section>')
            out.append(f'<section class="chapter{" afterpart" if after_part else ""}">'
                       f'<header class="ch-head" id="{aid}"><p class="ch-label">{e(c["chapter"]).upper()}</p>'
                       f'<p class="ch-num">{b["num"]:02d}</p>'
                       f'<h1 class="ch-title" data-rh="{e(runhead(b["title"]))}">{balance(b["title"], 30)}</h1><div class="h-rule"></div></header>')
            sec = 'c'; toc.append(('ch', aid, f'{b["num"]}', b['title'])); i += 1; continue
        if t == 'label':
            kind = b['kind']
            lab = e(b['text'])
            if kind == 'statement':
                nxt = blocks[i + 1] if i + 1 < n else None
                body = nxt['html'] if nxt and nxt['t'] == 'p' else ''
                out.append(f'<aside class="statement"><p class="lab">{lab}</p><p class="st-text">{body}</p></aside>')
                i += 2 if body else 1; continue
            if kind == 'reflection':
                out.append(f'<div class="reflection"><p class="lab">{lab}</p><ol class="nl">')
                i += 1
                while i < n and blocks[i]['t'] == 'num':
                    out.append(f'<li><span class="n">{blocks[i]["n"]}</span>{blocks[i]["html"]}</li>'); i += 1
                out.append('</ol></div>'); continue
            if kind == 'example':
                start = len(out)
                out.append(f'<div class="example"><p class="lab">{lab}</p>')
                i += 1
                while i < n and blocks[i]['t'] in ('p', 'num', 'bullet'):
                    i = emit_flow(blocks, i, out)
                if i < n and blocks[i]['t'] == 'label' and blocks[i]['kind'] == 'reflection':
                    out[start] = out[start].replace('class="example"', 'class="example tight"')
                out.append('</div>'); continue
        if t == 'sub':
            out.append(f'<h2 class="sub">{b["html"]}</h2>'); i += 1; continue
        if t == 'img':
            alt = ALT[lang].get(b['src_file'], '')
            from PIL import Image
            px = Image.open(os.path.join(MEDIA_DIR, b['src_file'])).size[0]
            # never print a raster below ~150 ppi: small originals are set narrower than the text block
            style = f' style="width:{px / 150:.2f}in"' if px / 150 < 4.5 else ''
            cap = ''
            if i + 1 < n and blocks[i + 1]['t'] == 'caption':
                cap = f'<figcaption>{blocks[i + 1]["html"]}</figcaption>'; i += 1
            if b['src'] in shrink and not style: style = ' style="max-height:6.0in"'
            out.append(f'<figure class="fig" id="fig{b["src"]}"><img src="{media_rel}/{b["src_file"]}" alt="{e(alt)}"{style}/>{cap}</figure>')
            i += 1; continue
        if t == 'numsub':
            out.append(f'<h2 class="sub numsub"><span class="sn">{b["n"]}</span>{b["html"]}</h2>'); i += 1; continue
        if t == 'signature':
            out.append(f'<p class="signature">{b["html"]}</p>'); i += 1; continue
        if t == 'caption':
            out.append(f'<p class="caption">{b["html"]}</p>'); i += 1; continue
        if t == 'table':
            rows = b['rows']
            out.append('<table class="tbl"><thead><tr>' + ''.join(f'<th>{e(x)}</th>' for x in rows[0]) + '</tr></thead><tbody>' +
                       ''.join('<tr>' + ''.join(f'<td>{e(x)}</td>' for x in r) + '</tr>' for r in rows[1:]) + '</tbody></table>')
            i += 1; continue
        i = emit_flow(blocks, i, out)
    close()

    # --- table of contents, page numbers resolved by the layout engine (target-counter)
    rows = []
    for item in toc:
        if item[0] == 'fm':
            rows.append(f'<li class="t-fm"><span class="tt">{e(item[2])}</span><a class="pg" href="#{item[1]}"></a></li>')
        elif item[0] == 'part':
            rows.append(f'<li class="t-part"><span class="tn">{e(item[2])}</span>'
                        f'<span class="tt">{e(item[3])}</span><a class="pg" href="#{item[1]}"></a></li>')
        else:
            rows.append(f'<li class="t-ch"><span class="tn">{item[2]}</span>'
                        f'<span class="tt">{e(item[3])}</span><a class="pg" href="#{item[1]}"></a></li>')
    tochtml = (f'<section class="toc"><h1 class="fm-title">{e(c["contents"])}</h1><div class="h-rule"></div>'
               f'<ol class="toc-list">{"".join(rows)}</ol></section>')
    body = '\n'.join(out).replace('@@TOC@@', tochtml)
    return (f'<!doctype html><html lang="{c["lang"]}"><head><meta charset="utf-8"/><title>{e(c["title"])}</title>'
            f'<link rel="stylesheet" href="{css}"/><style>.front .fm-title {{ string-set: runhead content(text), versohead "{e(c["title"])}"; }} .ch-title {{ string-set: runhead attr(data-rh), versohead "{e(c["title"])}"; }}</style></head>'
            f'<body data-title="{e(c["title"])}">{body}</body></html>')


def emit_flow(blocks, i, out):
    b = blocks[i]; t = b['t']
    if t == 'p':
        cls = ' class="em"' if b.get('bold') else ''
        out.append(f'<p{cls}>{b["html"]}</p>'); return i + 1
    if t == 'num':
        out.append('<ol class="nl">')
        while i < len(blocks) and blocks[i]['t'] == 'num':
            out.append(f'<li><span class="n">{blocks[i]["n"]}</span>{blocks[i]["html"]}</li>'); i += 1
        out.append('</ol>'); return i
    if t == 'bullet':
        out.append('<ul class="bl">')
        while i < len(blocks) and blocks[i]['t'] == 'bullet':
            out.append(f'<li>{blocks[i]["html"]}</li>'); i += 1
        out.append('</ul>'); return i
    out.append(f'<p>{b.get("html", "")}</p>'); return i + 1


MEDIA_DIR = 'media'

if __name__ == '__main__':
    lang, src, dst = sys.argv[1:4]
    MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(dst)), 'media')
    blocks = json.load(open(src))
    open(dst, 'w').write(build(lang, blocks, 'media'))
