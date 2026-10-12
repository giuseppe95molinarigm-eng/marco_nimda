# Quality Control Report: print interiors
**Prepare to Win** (EN) · **Winnen begint in de voorbereiding** (NL) · Harrie Kwinten
Prepared by Elite Publishing · 12 October 2026

---

## 1. Deliverables

| File | Edition | Pages | Trim | Size |
|---|---|---|---|---|
| `ENGLISH_PREPARE_TO_WIN/Prepare_to_Win_Paperback.pdf` | EN paperback | **165** | 6 × 9 in | 10.4 MB |
| `ENGLISH_PREPARE_TO_WIN/Prepare_to_Win_Hardcover.pdf` | EN hardcover | **169** | 6 × 9 in | 10.5 MB |
| `DUTCH_WINNEN_BEGINT_IN_DE_VOORBEREIDING/Winnen_Begint_Paperback.pdf` | NL paperback | **163** | 6 × 9 in | 9.9 MB |
| `DUTCH_WINNEN_BEGINT_IN_DE_VOORBEREIDING/Winnen_Begint_Hardcover.pdf` | NL hardcover | **165** | 6 × 9 in | 9.9 MB |

The paperback and hardcover files are typeset separately because they use different gutters, so their page counts differ.
**Kindle EPUB files are not included.** The order requirements ask for "the print-ready PDF file" only. They can be produced on request.

## 2. Page geometry

| | Paperback | Hardcover | KDP minimum (151–300 pages) |
|---|---|---|---|
| Inside margin (gutter) | 0.875 in | 1.0 in | 0.5 in |
| Outside margin | 0.60 in | 0.60 in | 0.25 in |
| Top / bottom | 0.80 / 0.80 in | 0.80 / 0.80 in | 0.25 in |
| Bleed | none | none | — |

- Margins are mirrored, with the gutter always on the binding side.
- Folios: Roman numerals in the front matter; the main text starts at page 1 with the Foreword.
- Running heads: verso pages show the book title; recto pages show the chapter title. Long titles are shortened to the words before the colon (e.g. Ch. 26 "Getting Started").
- Parts open on a right-hand page; chapters open on a new page.

## 3. Fonts (all embedded and subset; licensed under the SIL Open Font License for commercial use)
Source Serif 4 (body text, statements), Barlow and Barlow Condensed (headings, labels, running heads).
**Check result:** all 4 PDFs contain only these 10 font faces, and every face is embedded. No fallback fonts were substituted.

## 4. Automated checks (all 4 PDFs)

| Check | Result |
|---|---|
| Page size 6.000 × 9.000 in on every page | ✅ |
| Text outside the text block | ✅ none |
| Text within 0.25 in of the trim edge | ✅ none |
| Headings stranded at the bottom of a page | ✅ none (headings are kept with their text) |
| Table of contents page numbers | ✅ generated from the final layout; 0 mismatches on the 20 chapter entries checked automatically in each file |
| Author photo (player/captain) on its own left page facing the Chapter 6 opener | ✅ all 4 files |
| **Content integrity:** every source paragraph of the DOCX found in the PDF text | ✅ EN 1,508 / 1,508 · NL 1,509 / 1,509 |

The only DOCX text not in the interiors, left out on purpose:
- the "Back Cover Text" / "Achterflaptekst" section, which is cover copy;
- the "Colophon" / "Colofon" heading, whose content is printed on the copyright page.

## 5. Images

**Figure placement:** large infographics float a few paragraphs within their own chapter so the page before them is not left half empty. One image ("From customer to fan") is set slightly smaller, 6.0 in tall. Captioned personal photos always stay exactly where the author put them.

**Remaining white space:** a few pages still have 1–2 in of white space before an infographic that closes a chapter. This is normal and intended.

| Image | Effective resolution | Status |
|---|---|---|
| 8 infographics + IQ/EQ rings + diagrams | ≈ 190–235 ppi | Acceptable, below the ideal 300 ppi. Higher-resolution originals are recommended |
| Author photo, player/captain (Ch. 6) | 248 ppi (web copy received) | Acceptable; replace with the original `aangepastefoto.png` when available |
| **"Harrie and Marella, 1965"** | 323 × 392 px (EN) / 392 × 434 px (NL), printed ≈ 2.2–2.6 in wide at ≈ 150 ppi | ⚠️ Low resolution; set smaller to limit blur. **A better scan is strongly recommended** |

Images are in colour (RGB). If the book is printed with a black-and-white interior, KDP converts them to grayscale; every label stays readable (checked on grayscale previews).

## 6. Formatting corrections applied (no wording changed)

- Headings that were typed as bold body text were rebuilt as true headings: Parts II–IV and most chapter titles.
- Spacing: about 560 empty paragraphs and all tab/space runs were removed.
- **Soft line breaks:** 19 paragraphs per language used soft line breaks (Shift+Enter) instead of real paragraphs. They were split into proper paragraphs; this also fixed the EN Chapter 4 "Statement".
- **Sentences split across paragraphs** by a stray Enter were joined:
  - EN, Ch. 26: the bullet "…independence among / professionals" and two score lines;
  - NL, Ch. 26: two score lines and "…Zo wordt verbetering / beheersbaar."
- **Hand-typed bullets** ("•", "·") were turned into real lists.
- **Removed elements:**
  - the cover image embedded at the start of each manuscript;
  - the empty 7-row Word table in EN Ch. 7, which had no text in any cell (the comparison is shown as an image).
- **Table of contents** rebuilt from the chapter headings in the text.

## 7. Open points: the client should confirm (defaults used are in bold)

1. **ISBN.** The copyright page still reads "ISBN: [number]" (EN) and "ISBN" (NL), exactly as in the manuscript. Add the ISBNs, or remove the line if KDP's free ISBN is used. Each paperback and each hardcover needs its own ISBN.
2. **Subtitle on the title page:** **cover subtitle used** ("How a world champion thinks, leads and builds winning teams" / NL equivalent). The colophon uses a different subtitle.
3. **English chapter titles:** **headings from the body text used.** 8 of them differ slightly from the manuscript's own table of contents (e.g. Ch. 13 "Scout:" vs "Scouting:").
4. **Interior ink:** the files work for both black-and-white and colour printing (see §5).
5. **Colophon wording:** "© 2026 Harrie Kwinten / Amazon", "Printing: Amazon", "Cover design and layout: Harrie Kwinten". Kept exactly as written.
6. **Possible typos, reported and not changed:**
   - EN Ch. 1: "1/ **/** Where…" (stray slash).
   - NL Hoofdstuk 1: "Praktijkbeeld" (elsewhere "Praktijkvoorbeeld").
   - NL Hoofdstuk 26 Stelling begins in lowercase: "uitspraak van Mark Twain…". A word may be missing.
   - EN Ch. 21: "Price negotiations are usually a sign you were too late / if you find yourself…". Punctuation seems to be missing between the two lines.
   - EN Ch. 3 title starts in lowercase ("performance culture…"). It prints in capitals, but shows in lowercase in the contents.
7. **Manuscript status:** the client said content may still change. Any new DOCX can be re-typeset quickly with the same design.

## 8. Checks not performed here
- **Upload preview:** the files have not been through KDP's online previewer. Uploading them to KDP runs the definitive automated check.
- **Kindle EPUB:** not produced and not validated with EPUBCheck, because it is out of the requested scope.
