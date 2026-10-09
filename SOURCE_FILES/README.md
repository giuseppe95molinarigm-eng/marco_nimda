# Production sources

Pipeline: DOCX → `tools/parse.py` (semantic blocks, JSON) → `tools/build_print.py` (HTML) + `tools/print.css` → WeasyPrint (`tools/render.py`) → print PDF.

```
python3 tools/parse.py <manuscript.docx> en.json build/en/media   # needs the DOCX unzipped next to it in ./x/
python3 tools/build_print.py en en.json build/en/book.html         # copy print.css + fonts/ next to book.html
python3 tools/render.py build/en/book.html build/en/book.pdf
python3 tools/integrity.py en build/en/book.pdf <manuscript.docx> en.json   # paragraph coverage check
python3 tools/sample.py en build/en/book.pdf sample.pdf                     # extract the 8 review pages
```

Requires: weasyprint (70), python-docx, pymupdf, pillow. Fonts: Source Serif 4 (Adobe, OFL) and Barlow / Barlow Condensed (OFL); licences in `fonts/`.
The source manuscripts are not stored in this repository.
