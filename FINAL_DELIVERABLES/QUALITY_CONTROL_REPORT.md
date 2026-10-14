# Quality Control Report: final files (version 2)
**Prepare to Win** (EN) · **Winnen begint in de voorbereiding** (NL) · Harrie Kwinten
Prepared by Elite Publishing · 14 October 2026

Sources:
- **English:** updated manuscript received 14 Oct 2026, with about 290 author revisions compared with v1.
- **Dutch:** manuscript unchanged (byte-for-byte identical to the version already checked).

---

## 1. Deliverables

| File | Format | Interior | Pages | ISBN printed |
|---|---|---|---|---|
| `ENGLISH_PREPARE_TO_WIN/Prepare_to_Win_Paperback.pdf` | 6 × 9 in print PDF | **black & white**, white paper | **165** | 9789090435213 |
| `ENGLISH_PREPARE_TO_WIN/Prepare_to_Win_Hardcover.pdf` | 6 × 9 in print PDF | **colour**, white paper | **169** | 9789090435008 |
| `ENGLISH_PREPARE_TO_WIN/Prepare_to_Win_Kindle.epub` | EPUB 3, reflowable | colour | — | lists both print ISBNs |
| `ENGLISH_PREPARE_TO_WIN/Prepare_to_Win_Kindle_Cover.jpg` | eBook cover, 1801 × 2700 px | — | — | — |
| `DUTCH_…/Winnen_Begint_Paperback.pdf` | 6 × 9 in print PDF | **black & white**, white paper | **163** | 9789090435015 |
| `DUTCH_…/Winnen_Begint_Hardcover.pdf` | 6 × 9 in print PDF | **colour**, white paper | **165** | 9789090434995 |
| `DUTCH_…/Winnen_Begint_Kindle.epub` | EPUB 3, reflowable | colour | — | lists both print ISBNs |

All four ISBNs were validated (ISBN-13 check digit correct).

## 2. Client decisions applied (message of 14 Oct)

| Decision | How it was applied |
|---|---|
| Hardcover colour / paperback black-and-white, white paper | **Paperback:** every image is converted to grayscale and the orange accent becomes a dark grey (#4d4d4d), so the file contains no colour at all (checked). **Hardcover:** colour images and orange accents. |
| ISBNs | Each print edition carries its own ISBN on the copyright page. The eBook copyright page lists the paperback and hardcover ISBNs. |
| Title and subtitle | Title page: **Prepare to Win**, with the subtitle **"How a World Champion Thinks, Leads and Builds Winning Teams"** exactly as supplied. |
| Chapter 13 → "Scouting" | Applied in the chapter heading, table of contents, running heads and eBook navigation. |
| Typo corrections | See §3. |
| Final formats: hardcover, paperback and Kindle | All three formats delivered for both languages. |
| New front cover | Used for the English Kindle eBook (front panel cut from `Harrie_Cover_UK.pdf`). See §7 for cover remarks. |

## 3. Text corrections (approved by the client; nothing else in the author's text was changed)

| Edition | Correction |
|---|---|
| EN | Ch. 13 title "Scout:" → "Scouting:" |
| EN | Ch. 3 title "performance culture…" → "Performance culture…" |
| EN | Ch. 21: "…a sign you were too late" + "if you find yourself…" → full stop added, "If" capitalised |
| EN | Ch. 1 "1/ / Where…": **already corrected by the author** in the 14 Oct manuscript |
| NL | Hoofdstuk 1: "Praktijkbeeld" → "Praktijkvoorbeeld" |
| NL | Hoofdstuk 26, Stelling: "uitspraak van Mark Twain…" → "De uitspraak van Mark Twain…" |

## 4. Print PDFs: page geometry and checks

| | Paperback | Hardcover | KDP minimum (151–300 pages) |
|---|---|---|---|
| Inside margin (gutter) | 0.875 in | 1.0 in | 0.5 in |
| Outside / top / bottom | 0.60 / 0.80 / 0.80 in | 0.60 / 0.80 / 0.80 in | 0.25 in |
| Bleed | none | none | — |

| Automated check (all 4 PDFs) | Result |
|---|---|
| Page size 6.000 × 9.000 in on every page | ✅ |
| Text outside the text block / within 0.25 in of the trim edge | ✅ none |
| Fonts | ✅ 10 faces (Source Serif 4, Barlow, Barlow Condensed; SIL OFL), all embedded and subset; no substitutions |
| Headings stranded at the bottom of a page | ✅ none |
| Table of contents | ✅ page numbers generated from the final layout |
| Author photo (captain) on the left page facing the Chapter 6 opener | ✅ |
| Paperback contains only grayscale images and grey text | ✅ (images DeviceGray, no coloured text) |
| **Content integrity:** every DOCX paragraph found in the PDF text | ✅ EN 1,548 / 1,548 · NL 1,507 / 1,507 |

What is intentionally not in the interiors:
- the "Back Cover Text" / "Achterflaptekst" section (cover copy);
- the "Colophon" / "Colofon" heading, whose content is printed on the copyright page;
- the "ISBN: [number]" placeholder, replaced by the real ISBN;
- the two headings corrected in §3.

**Layout:** large infographics float within their own chapter to avoid half-empty pages, and captioned photos stay exactly where the author placed them. A few pages still have 1–2 in of space before an infographic that closes a chapter; this is intended.

## 5. Kindle eBooks (EPUB 3)

| Check | EN | NL |
|---|---|---|
| **EPUBCheck 5.1.0** | ✅ 0 fatal / 0 errors / 0 warnings | ✅ 0 fatal / 0 errors / 0 warnings |
| Reflowable (no fixed layout, no page numbers or running heads) | ✅ | ✅ |
| Navigation: nav.xhtml with Parts and nested Chapters, NCX for older Kindles, landmarks | ✅ | ✅ |
| Language metadata | en-GB | nl-NL |
| Alt text on every image | ✅ | ✅ |
| Embedded cover | ✅ new UK cover | — (see §7) |
| Content integrity (every DOCX paragraph present) | ✅ | ✅ |
| File size | 2.6 MB | 1.8 MB |

The text was also checked in a phone-width reading view at 160 % font size: headings, statements, lists and images reflow correctly.
**Not done here:** Amazon Kindle Previewer is a desktop application and cannot run in this environment. Please open both EPUBs in Kindle Previewer, or check them in KDP's online previewer after uploading.

## 6. Images

| Image | Effective resolution | Status |
|---|---|---|
| Infographics and diagrams | ≈ 190–235 ppi | Acceptable for print; 300 ppi originals would be sharper |
| Author photo, captain (Ch. 6) | 248 ppi | Good |
| "Harrie and Marella, 1965" | ≈ 150 ppi at a reduced size | ⚠️ Low resolution; a better scan is still recommended |

## 7. Points for the client

1. **⚠️ Cover file `Harrie_Cover_UK.pdf` will not pass KDP as it is.** Cover design is outside our scope, but:
   - it measures 13.181 × 9.0 in, which is **without bleed** (KDP needs 9.25 in tall);
   - its spine (about 1.18 in) does not match these interiors. A 165-page paperback on white paper has a spine of about 0.37 in.
   - The designer must rebuild the wraps with KDP's cover calculator using the **final page counts**:

     | Edition | Pages |
     |---|---|
     | EN paperback | 165 |
     | EN hardcover | 169 |
     | NL paperback | 163 |
     | NL hardcover | 165 |
2. **Subtitle punctuation.** The cover reads "Thinks, Leads**,** and Builds"; the subtitle supplied (and used on the title page) has no comma after "Leads". KDP compares the title and subtitle on the cover with the book details, so please use one spelling everywhere.
3. **Dutch eBook cover.** The new Dutch cover was not supplied as a file. Upload it as the eBook cover in KDP, or send it so it can be embedded in the EPUB.
4. **Colophon subtitle.** The copyright page keeps the author's own line, "Prepare to Win – Doing Is the Best Way of Thinking / The Practical Method for Leadership, Performance Culture and Commercial Effectiveness". Change it if it should match the new subtitle.
5. **English table of contents.** The other English chapter titles follow the headings in the text (e.g. Part III "The 15 strategies of business athlete"). Only Chapter 13 was changed, as requested.
