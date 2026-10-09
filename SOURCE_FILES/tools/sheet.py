import sys, glob, subprocess, os, tempfile
from PIL import Image
pdf, first, last, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
res = sys.argv[5] if len(sys.argv) > 5 else '40'
d = tempfile.mkdtemp()
subprocess.run(['pdftoppm', '-r', res, '-png', '-f', first, '-l', last, pdf, os.path.join(d, 'p')], check=True)
fs = sorted(glob.glob(os.path.join(d, 'p-*.png')))
ims = [Image.open(f) for f in fs]; w, h = ims[0].size
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 8
rows = (len(ims) + cols - 1) // cols
sh = Image.new('RGB', (cols * (w + 6), rows * (h + 6)), '#888')
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * (w + 6), (i // cols) * (h + 6)))
sh.save(out)
