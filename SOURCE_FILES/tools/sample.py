import sys, pymupdf
lang, src, dst = sys.argv[1:4]
d = pymupdf.open(src)
def flat(i): return d[i].get_text().replace(' ', '').replace('\n', '').upper()
K = {'en': ('THE4PLAYINGFIELDS', 'PART', 'CHAPTER01', 'REFLECTIONQUESTIONS', 'PRACTICALEXAMPLE'),
     'nl': ('DE4SPEELVELDEN', 'DEEL', 'HOOFDSTUK01', 'REFLECTIEVRAGEN', 'PRAKTIJKVOORBEELD')}[lang]
img = next(i for i in range(len(d)) if d[i].get_image_info() and i > 4)
part = next(i for i in range(len(d)) if flat(i).startswith(K[1] + 'I'))
ch = next(i for i in range(len(d)) if flat(i).startswith(K[2]))
refl = next(i for i in range(ch, len(d)) if K[3] in flat(i))
ex = next(i for i in range(refl + 1, len(d)) if K[4] in flat(i))
pages = [2, 3, 4, img, part, ch, refl, ex]
d.select(pages)
d.set_metadata({'title': {'en': 'Prepare to Win - interior sample (6 x 9 in)', 'nl': 'Winnen begint in de voorbereiding - binnenwerkproef (6 x 9 inch)'}[lang], 'author': 'Harrie Kwinten'})
d.save(dst, garbage=4, deflate=True)
print(lang, 'sample = book pages', [p + 1 for p in pages])
