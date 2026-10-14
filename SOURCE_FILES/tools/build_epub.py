"""Build a reflowable EPUB 3 (Kindle-compatible) from the parsed manuscript blocks.

Semantic XHTML per part/chapter, nav.xhtml + toc.ncx, landmarks, language metadata,
alt text on every image, relative (em) sizing only, no print furniture.
Usage: build_epub.py <lang> <blocks.json> <media dir> <out.epub> [cover.jpg]
"""
import sys, os, json, html, re, uuid, zipfile, io, datetime
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_print import CFG, SKIP_IMG, FACING_PHOTO, ISBN

lang, src, media_dir, out = sys.argv[1:5]
cover = sys.argv[5] if len(sys.argv) > 5 else None
blocks = json.load(open(src))
c = CFG[lang]
e = lambda t: html.escape(t, quote=True)

ALT = {
    'en': {'image2': 'Infographic: The 4 playing fields of business performance: the Field, the Captain, the Fans and the Scout',
           'image3': 'Infographic: The preparation circle: prepare, execute, evaluate, adjust, repeat',
           'image4': 'Infographic: Performance culture is no coincidence: standards, role modelling, feedback, rhythm and ownership',
           'image5': 'Graph of the forgetting curve: retention falls sharply in the days after learning',
           'image6': 'Table comparing traditional training with coaching on the job',
           'image7': 'The Dutch team celebrating with the trophy after winning the 1990 field hockey world championship',
           'image8': 'Infographic: From customer to fan: understand, deliver reliably, manage expectations, deepen value',
           'image9': 'Infographic: Scouting: where are the real growth opportunities? Market, customer, competition, network and timing',
           'image10': 'Diagram of five linked rings: IQ, EQ, AQ, FQ and SQ',
           'image11': 'Infographic: Coaching on the job: from training to coaching on the job to results',
           'image12': 'Infographic: Build your performance culture in 90 days: diagnosis, focus, training and coaching, rhythm, embedding',
           'image13': 'Childhood photo of Harrie and his sister Marella, 1965'},
    'nl': {'image2': 'Infographic: De 4 speelvelden van zakelijk presteren: het Veld, de Captain, de Fans en de Scout',
           'image3': 'Infographic: De voorbereidingscirkel: voorbereiden, uitvoeren, evalueren, bijsturen, herhalen',
           'image4': 'Infographic: Prestatiecultuur is geen toeval: standaarden, voorbeeldgedrag, feedback, ritme en eigenaarschap',
           'image5': 'Grafiek van de vergeetcurve: wat je leert, vergeet je in de dagen erna snel',
           'image6': 'Het Nederlandse team viert met de trofee na het winnen van het wereldkampioenschap veldhockey in 1990',
           'image7': 'Infographic: Van klant naar fan: begrijpen, betrouwbaar leveren, verwachtingen managen, waarde verdiepen',
           'image8': 'Infographic: Scouten: waar liggen de echte groeikansen? Markt, klant, concurrentie, netwerk en timing',
           'image9': 'Diagram met vijf verbonden ringen: IQ, EQ, AQ, FQ en SQ',
           'image10': 'Infographic: Coaching on the job: van training via coaching on the job naar resultaat',
           'image11': 'Infographic: Bouw je prestatiecultuur in 90 dagen: diagnose, focus, training en coaching, ritme, verankering',
           'image12': 'Jeugdfoto van Harrie en zijn zus Marella, 1965'},
}
UI = {'en': dict(contents='Contents', cover='Cover', title='Title page', copyright='Copyright', start='Start reading',
                 photo='Harrie Kwinten as captain', pb='paperback', hc='hardcover'),
      'nl': dict(contents='Inhoud', cover='Omslag', title='Titelpagina', copyright='Colofon', start='Begin met lezen',
                 photo='Harrie Kwinten als aanvoerder', pb='paperback', hc='gebonden editie')}[lang]

files = []        # (id, href, title, xhtml, nav_level)  nav_level None = not in TOC
images = {}       # media name -> (href, bytes, mime)


def add_image(fname, src_dir=media_dir):
    """Re-encode for e-readers: JPEG (photos and infographics on light backgrounds), max 1600 px."""
    if fname in images: return images[fname][0]
    im = Image.open(os.path.join(src_dir, fname))
    im = im.convert('RGB')
    if max(im.size) > 1600: im.thumbnail((1600, 1600), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=86, optimize=True, progressive=False)
    href = 'images/' + os.path.splitext(fname)[0] + '.jpg'
    images[fname] = (href, buf.getvalue(), 'image/jpeg')
    return href


def page(title, body, epub_type='bodymatter', cls=''):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n'
            f'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{c["lang"]}" xml:lang="{c["lang"]}">'
            f'<head><meta charset="UTF-8"/><title>{e(title)}</title><link rel="stylesheet" type="text/css" href="css/book.css"/></head>'
            f'<body epub:type="{epub_type}"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>{body}</body></html>')


def fig(b, cap_html=''):
    key = os.path.splitext(b['src_file'])[0]
    href = add_image(b['src_file'])
    alt = ALT[lang].get(key, '')
    w, h = Image.open(os.path.join(media_dir, b['src_file'])).size
    small = ' class="small"' if w < 700 else ''
    cap = f'<figcaption>{cap_html}</figcaption>' if cap_html else ''
    return f'<figure{small}><img src="{href}" alt="{e(alt)}"/>{cap}</figure>'


def flow(bl, i, out):
    b = bl[i]; t = b['t']
    if t == 'p':
        out.append(f'<p{" class=\"em\"" if b.get("bold") else ""}>{b["html"]}</p>'); return i + 1
    if t == 'num':
        out.append('<ol class="nl">')
        while i < len(bl) and bl[i]['t'] == 'num':
            out.append(f'<li value="{bl[i]["n"]}">{bl[i]["html"]}</li>'); i += 1
        out.append('</ol>'); return i
    if t == 'bullet':
        out.append('<ul>')
        while i < len(bl) and bl[i]['t'] == 'bullet':
            out.append(f'<li>{bl[i]["html"]}</li>'); i += 1
        out.append('</ul>'); return i
    out.append(f'<p>{b.get("html", "")}</p>'); return i + 1


def render(bl):
    """Body content of one section (blocks after its heading)."""
    out = []; i = 0; n = len(bl)
    while i < n:
        b = bl[i]; t = b['t']
        if t == 'label':
            lab = e(b['text'])
            if b['kind'] == 'statement':
                nxt = bl[i + 1] if i + 1 < n and bl[i + 1]['t'] == 'p' else None
                out.append(f'<aside class="statement" epub:type="pullquote"><p class="lab">{lab}</p>'
                           f'<p class="st">{nxt["html"] if nxt else ""}</p></aside>')
                i += 2 if nxt else 1; continue
            if b['kind'] == 'reflection':
                out.append(f'<section class="reflection"><p class="lab">{lab}</p><ol class="nl">'); i += 1
                while i < n and bl[i]['t'] == 'num':
                    out.append(f'<li value="{bl[i]["n"]}">{bl[i]["html"]}</li>'); i += 1
                out.append('</ol></section>'); continue
            if b['kind'] == 'example':
                out.append(f'<section class="example"><p class="lab">{lab}</p>'); i += 1
                while i < n and bl[i]['t'] in ('p', 'num', 'bullet'): i = flow(bl, i, out)
                out.append('</section>'); continue
        if t == 'sub': out.append(f'<h2>{b["html"]}</h2>'); i += 1; continue
        if t == 'numsub': out.append(f'<h2><span class="sn">{b["n"]}</span> {b["html"]}</h2>'); i += 1; continue
        if t == 'signature': out.append(f'<p class="signature">{b["html"]}</p>'); i += 1; continue
        if t == 'img':
            cap = ''
            if i + 1 < n and bl[i + 1]['t'] == 'caption': cap = bl[i + 1]['html']; i += 1
            out.append(fig(b, cap)); i += 1; continue
        if t == 'caption': out.append(f'<p class="caption">{b["html"]}</p>'); i += 1; continue
        if t == 'table':
            rows = b['rows']
            out.append('<table><thead><tr>' + ''.join(f'<th>{e(x)}</th>' for x in rows[0]) + '</tr></thead><tbody>' +
                       ''.join('<tr>' + ''.join(f'<td>{e(x)}</td>' for x in r) + '</tr>' for r in rows[1:]) + '</tbody></table>')
            i += 1; continue
        i = flow(bl, i, out)
    return ''.join(out)


# ---------- split blocks into sections
skip = ('toc_src', 'empty_table', 'covercopy_head', 'covercopy', 'colophon_head', 'colophon')
body = [b for b in blocks if b['t'] not in skip and not (b['t'] == 'img' and b['src_file'] in SKIP_IMG[lang])]
sections = []
for b in body:
    if b['t'] in ('front', 'back', 'part', 'chapter'): sections.append([b, []])
    elif sections: sections[-1][1].append(b)

# ---------- front matter
if cover:
    cimg = Image.open(cover).convert('RGB'); buf = io.BytesIO(); cimg.save(buf, 'JPEG', quality=90)
    images['__cover'] = ('images/cover.jpg', buf.getvalue(), 'image/jpeg')
    files.append(('cover', 'cover.xhtml', UI['cover'],
                  page(UI['cover'], f'<div class="cover"><img src="images/cover.jpg" alt="{e(c["title"])}, {e(c["author"])}"/></div>', 'cover', 'coverpage'), None))
files.append(('titlepage', 'title.xhtml', UI['title'],
              page(c['title'], f'<section class="titlepage" epub:type="titlepage"><h1 class="booktitle">{e(c["title"])}</h1>'
                               f'<p class="subtitle">{e(c["subtitle"])}</p><p class="author">{e(c["author"])}</p></section>', 'frontmatter'), None))
colo = [b['html'] for b in blocks if b['t'] == 'colophon']
isbn_print = (f'ISBN {ISBN[(lang, "paperback")]} ({UI["pb"]})<br/>ISBN {ISBN[(lang, "hardcover")]} ({UI["hc"]})')
colo = [re.sub(r'ISBN(?::\s*\[number\])?', isbn_print, h, count=1) if 'ISBN' in h else h for h in colo]
files.append(('copyright', 'copyright.xhtml', UI['copyright'],
              page(UI['copyright'], '<section class="copyright" epub:type="copyright-page">' + ''.join(f'<p>{h}</p>' for h in colo) + '</section>', 'frontmatter'), None))

# ---------- body sections
first_body = None
for head, bl in sections:
    t = head['t']
    if t == 'part':
        fid = f'part{head["num"]}'
        x = (f'<section class="part" epub:type="part"><p class="part-label">{e(c["part"])} {head["num"]}</p>'
             f'<h1 class="part-title">{e(head["title"])}</h1></section>')
        files.append((fid, fid + '.xhtml', f'{c["part"]} {head["num"]} — {head["title"]}', page(head['title'], x), 1))
    elif t == 'chapter':
        if head['num'] in FACING_PHOTO:
            f, alts = FACING_PHOTO[head['num']]
            href = add_image(f)
            files.append((f'photo{head["num"]}', f'photo-ch{head["num"]:02d}.xhtml', UI['photo'],
                          page(UI['photo'], f'<figure class="fullpage"><img src="{href}" alt="{e(alts[lang])}"/></figure>'), None))
        fid = f'ch{head["num"]:02d}'
        x = (f'<section epub:type="chapter" aria-labelledby="h-{fid}"><p class="ch-num">{e(c["chapter"])} {head["num"]}</p>'
             f'<h1 id="h-{fid}" class="ch-title">{e(head["title"])}</h1>{render(bl)}</section>')
        files.append((fid, fid + '.xhtml', f'{head["num"]}. {head["title"]}', page(head['title'], x), 2))
    else:
        fid = re.sub(r'\W+', '-', head['title'].lower()).strip('-')[:30]
        ty = 'foreword' if head['title'] in ('Foreword', 'Voorwoord') else ('introduction' if head['title'] in ('Introduction', 'Inleiding')
             else ('afterword' if head['title'] in ('Afterword', 'Nawoord') else 'chapter'))
        x = f'<section epub:type="{ty}"><h1 class="fm-title">{e(head["title"])}</h1>{render(bl)}</section>'
        files.append((fid, fid + '.xhtml', head['title'], page(head['title'], x, 'frontmatter' if ty in ('foreword', 'introduction') else 'backmatter' if ty == 'afterword' else 'bodymatter'), 1))
    if first_body is None and t in ('front', 'part', 'chapter'): first_body = files[-1][1]

# ---------- navigation (nav.xhtml + NCX for older Kindle readers)
nav_items, open_part = [], False
for fid, href, title, _, lvl in files:
    if lvl is None: continue
    if lvl == 1:
        if open_part: nav_items.append('</ol></li>'); open_part = False
        if fid.startswith('part'):
            nav_items.append(f'<li><a href="{href}">{e(title)}</a><ol>'); open_part = True
        else:
            nav_items.append(f'<li><a href="{href}">{e(title)}</a></li>')
    else:
        nav_items.append(f'<li><a href="{href}">{e(title)}</a></li>')
if open_part: nav_items.append('</ol></li>')
nav = (f'<nav epub:type="toc" id="toc"><h1 class="fm-title">{e(c["contents"])}</h1><ol class="toc">{"".join(nav_items)}</ol></nav>'
       f'<nav epub:type="landmarks" hidden="hidden"><ol>'
       + (f'<li><a epub:type="cover" href="cover.xhtml">{e(UI["cover"])}</a></li>' if cover else '')
       + f'<li><a epub:type="toc" href="nav.xhtml">{e(c["contents"])}</a></li>'
         f'<li><a epub:type="bodymatter" href="{first_body}">{e(UI["start"])}</a></li></ol></nav>')
nav_doc = page(c['contents'], nav, 'frontmatter')

book_id = 'urn:uuid:' + str(uuid.uuid5(uuid.NAMESPACE_URL, f'harrie-kwinten/{lang}/kindle'))
points, order = [], 0
for fid, href, title, _, lvl in files:
    if lvl is None: continue
    order += 1
    points.append(f'<navPoint id="np{order}" playOrder="{order}"><navLabel><text>{e(title)}</text></navLabel><content src="{href}"/></navPoint>')
ncx = (f'<?xml version="1.0" encoding="UTF-8"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="{c["lang"]}">'
       f'<head><meta name="dtb:uid" content="{book_id}"/><meta name="dtb:depth" content="1"/></head>'
       f'<docTitle><text>{e(c["title"])}</text></docTitle><navMap>{"".join(points)}</navMap></ncx>')

css = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'epub.css')).read()

# insert the visible contents page after the copyright page
spine = [f for f in files if f[0] in ('cover', 'titlepage', 'copyright')] + [('nav', 'nav.xhtml', c['contents'], nav_doc, None)] + \
        [f for f in files if f[0] not in ('cover', 'titlepage', 'copyright')]
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
manifest = [f'<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
            '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
            '<item id="css" href="css/book.css" media-type="text/css"/>']
for fid, href, *_ in spine:
    if fid == 'nav': continue
    props = ' properties="svg"' if False else ''
    manifest.append(f'<item id="{fid}" href="{href}" media-type="application/xhtml+xml"{props}/>')
for k, (href, _, mime) in images.items():
    iid = 'cover-image' if k == '__cover' else 'img-' + re.sub(r'\W', '-', os.path.splitext(k)[0])
    manifest.append(f'<item id="{iid}" href="{href}" media-type="{mime}"{" properties=\"cover-image\"" if k == "__cover" else ""}/>')
spine_xml = ''.join(f'<itemref idref="{f[0]}"{" linear=\"yes\""}/>' for f in spine)
opf = (f'<?xml version="1.0" encoding="UTF-8"?>\n<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="{c["lang"]}">'
       f'<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
       f'<dc:identifier id="bookid">{book_id}</dc:identifier><dc:title id="t1">{e(c["title"])}</dc:title>'
       f'<meta refines="#t1" property="title-type">main</meta>'
       f'<dc:title id="t2">{e(c["subtitle"])}</dc:title><meta refines="#t2" property="title-type">subtitle</meta>'
       f'<dc:creator id="a1">{e(c["author"])}</dc:creator><meta refines="#a1" property="role" scheme="marc:relators">aut</meta>'
       f'<meta refines="#a1" property="file-as">Kwinten, Harrie</meta>'
       f'<dc:language>{c["lang"]}</dc:language><dc:rights>© 2026 Harrie Kwinten</dc:rights><dc:date>2026</dc:date>'
       f'<meta property="dcterms:modified">{now}</meta>'
       + ('<meta name="cover" content="cover-image"/>' if cover else '') +
       f'</metadata><manifest>{"".join(manifest)}</manifest><spine toc="ncx">{spine_xml}</spine></package>')

container = ('<?xml version="1.0" encoding="UTF-8"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
             '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
with zipfile.ZipFile(out, 'w') as z:
    z.writestr(zipfile.ZipInfo('mimetype'), 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
    z.writestr('META-INF/container.xml', container, zipfile.ZIP_DEFLATED)
    z.writestr('OEBPS/content.opf', opf, zipfile.ZIP_DEFLATED)
    z.writestr('OEBPS/toc.ncx', ncx, zipfile.ZIP_DEFLATED)
    z.writestr('OEBPS/nav.xhtml', nav_doc, zipfile.ZIP_DEFLATED)
    z.writestr('OEBPS/css/book.css', css, zipfile.ZIP_DEFLATED)
    for fid, href, _, x, _ in spine:
        if fid != 'nav': z.writestr('OEBPS/' + href, x, zipfile.ZIP_DEFLATED)
    for href, data, _ in images.values(): z.writestr('OEBPS/' + href, data, zipfile.ZIP_STORED)
print(out, 'files', len(spine), 'images', len(images), 'size', round(os.path.getsize(out) / 1e6, 2), 'MB')
