# Prepare to Win / Winnen begint in de voorbereiding
## Phase 1: Manuscript audit · Phase 2: Design system and 8-page print sample

Author: Harrie Kwinten · Platform: Amazon KDP · Trim: **6 × 9 in (confirmed)**
Status: **sample for approval. Final production has not started.**

---

## 1. What is in this folder

| File | What it is |
|---|---|
| `Prepare_to_Win_Sample_8pp.pdf` | English: 8 real pages taken from a full trial layout, 6 × 9 in, fonts embedded |
| `Winnen_Begint_Sample_8pp.pdf` | Dutch: the same 8 page types, typeset independently |
| `previews/*_sample_color.png` | Contact sheets of the 8 pages |
| `previews/*_sample_grayscale_bw_print.png` | The same pages in grayscale, to show how a black-and-white print run will look |
| `../SOURCE_FILES/` | Editable production sources: DOCX parser, layout builder, stylesheet, QC scripts, fonts with their licences |

The 8 pages in each sample, with their positions in the trial layout:

| # | Page type | Book page (folio) |
|---|---|---|
| 1 | Full title page (recto) | 3 |
| 2 | Copyright page (verso), built from the manuscript's own Colophon | 4 |
| 3 | Contents (page numbers generated from the layout) | 5 (v) |
| 4 | Image page: *The 4 playing fields* / *De 4 speelvelden* infographic | 11 (5) |
| 5 | Part opening: Part I / Deel I | 13 (7) |
| 6 | Chapter opening with Statement / Stelling | 15 (9) |
| 7 | Body page with Reflection questions / Reflectievragen | 22 (16) |
| 8 | Body page with Practical example / Praktijkvoorbeeld and chapter end | 23 (17) |

The sample pages come from a full layout of both books, not from mock-ups. That trial layout is used only to produce real page numbers and an early page-count estimate. It is **not** the final production.

---

## 2. Manuscript audit

### 2.1 Structure found (both languages are structurally parallel)

| Element | English | Dutch |
|---|---|---|
| Front matter | Foreword, Introduction | Voorwoord, Inleiding |
| Parts | 4 (Part I–IV) | 4 (Deel I–IV) |
| Chapters | 26 | 26 |
| Statement / Stelling blocks | in every chapter | in every chapter |
| Practical example labels | ✓ | ✓ (one is spelled "Praktijkbeeld", see 2.5) |
| Reflection questions | ✓ | ✓ |
| Numbered items "1/ …" | 91 | 91 |
| Bulleted items | 82 | 78 |
| Embedded images | 13 (one is the cover) | 12 (one is the cover) |
| Tables | 1 (empty, see 2.4) | 1 (real text table) |
| Back matter | Afterword, Next steps, **Back Cover Text**, **Colophon** | Nawoord, Volgende stappen, **Achterflaptekst**, **Colofon** |

**Formatting problems in the DOCX files (handled by the conversion, no words changed):**
- Most chapter headings, and Parts II–IV, are not Word headings. They are bold body text in five different paragraph styles. The parser recognises them by their "Chapter N —" / "Part X —" pattern.
- Blank paragraphs are used for spacing (324 in EN, 240 in NL, some of which carry images). All spacing now comes from the design system.
- Tab characters and runs of spaces inside paragraphs (e.g. `2/         evaluation`) are normalised.
- The manuscript's own table of contents uses Word page numbers. It is discarded and rebuilt from the layout.
- The cover artwork is embedded as the first item of each manuscript. It is **excluded** from the interior, as the brief asks.

### 2.2 Content integrity (trial layout vs. DOCX)

Every non-empty source paragraph after the original TOC was searched for, word for word (ignoring case, punctuation and print hyphenation), in the typeset PDF text. Running heads and folios were excluded from the search.

| | Checked | Found | Not found |
|---|---|---|---|
| English | 1,518 | 1,508 | 10: **all intentional** (the "Back Cover Text" section and the "Colophon" heading; the colophon's content is on the copyright page) |
| Dutch | 1,517 | 1,509 | 8: **all intentional** (the "Achterflaptekst" section and the "Colofon" heading) |

All images except the cover appear in their original positions.

### 2.3 Images: quality report

| Image | Pixels | Placed at | Effective resolution | Assessment |
|---|---|---|---|---|
| 8 portrait infographics per language (4 playing fields, preparation circle, performance culture, customer→fan, scouting, coaching on the job, 90 days) | ≈ 960–1,055 px wide | full text width, 4.52 in | **206–233 ppi** | Sharp and readable on screen. Below the 300 ppi KDP recommends for print. The smallest labels inside the graphics are about 5 pt at this size. |
| IQ/EQ/FQ/SQ/AQ rings | 932 px (EN) / 866 px (NL) | 4.52 in | 206 / 191 ppi | Acceptable for a simple graphic; a higher-resolution file is still preferred |
| Retention-curve illustration | 981 × 479 | 4.52 in | 217 ppi | OK |
| Team photo (trophy) | 982 × 658 | 4.52 in | 217 ppi | Acceptable for a photo |
| Coaching vs. training table (EN only, as an image) | 997 × 739 | 4.52 in | 220 ppi | See 2.4 |
| **"Harrie and Marella, 1965" photo** | **323 × 392 (EN) / 392 × 434 (NL)** | ≈ 3.4–4 in | **≈ 96 ppi** | **Not suitable for print at this size.** At 300 ppi it could only be printed about 1.1–1.3 in wide. |

All infographics are in **full colour** (orange accents). In a black-and-white print run the orange becomes mid-grey and every label stays legible (see the grayscale previews). The orange "Winning starts in preparation" lines become noticeably lighter. No image has been stretched: all are scaled proportionally.

**Requests:** (a) the original infographic files, as vector PDF/SVG or PNG at least 1,400 px wide; (b) a higher-resolution scan of the 1965 photo, at least 1,000 px wide.

### 2.4 Tables
- **English, chapter 7:** the "Traditional training vs. Coaching on the job" comparison exists only as a **picture of a table**. It is followed by an **empty** 7-row Word table (no text in any cell), which has been removed.
- **Dutch, hoofdstuk 7:** the same comparison is a **real text table**, and it is typeset as one.
- **Recommendation:** typeset the English table as text from the image's wording, so both editions match and the EPUB stays readable and accessible. This needs your approval, because the text would be transcribed from the image.

### 2.5 Possible editorial issues: reported, NOT changed
| # | Edition | Location | Issue |
|---|---|---|---|
| 1 | EN | Ch. 1, Reflection questions, item 1 | "1/ **/** Where in our organisation…": stray slash (visible in the sample on page 7) |
| 2 | NL | Hoofdstuk 1, first example | Label reads **"Praktijkbeeld"**; everywhere else it is "Praktijkvoorbeeld" |
| 3 | EN | TOC vs. body headings | 8 headings are worded differently in the manuscript's TOC and in the body text, e.g. Ch. 10 "…your company's commercial strength" vs. "…the commercial strength of your company?"; Ch. 13 "Scouting:" vs. "Scout:"; Part III "…of **the** business athlete" vs. "…of business athlete"; Ch. 15, 17, 19, 21, 26. **The sample uses the body headings.** Please confirm which wording is final. |
| 4 | EN | Chapter titles | Capitalisation is inconsistent: sentence case (Ch. 1–13; Ch. 3 even starts lowercase, "performance culture…") vs. Title Case (Ch. 14+). In print this is hidden because titles are set in capitals; in the TOC and EPUB it shows. Should all titles be in sentence case? |
| 5 | NL | Hoofdstuk 17 title | "Frontale & Flankerende verkoop strategie: … (Frontal & Flanking)": the closed compound "verkoopstrategie" is standard Dutch; capitals mid-title |
| 6 | NL | Hoofdstuk 26 title | Hyphen "feiten - doen" where the English uses a dash (—) |
| 7 | NL | Hoofdstuk 26, last section | One sentence is split over two paragraphs: "…Zo wordt verbetering" / "beheersbaar." (formatting accident; will be joined unless you object) |
| 8 | EN | Next steps | Items "1/preparation", "3/coaching" have no space after the slash and start lowercase (the Dutch is consistent) |

### 2.6 Missing or unconfirmed publishing information
1. **ISBNs.** The colophon has "ISBN: [number]" (EN) and "ISBN" (NL). KDP requires a **separate ISBN for each paperback and each hardcover**: 4 in total. The eBook ISBN is optional.
2. **Imprint / publisher line.** The colophon says "© 2026 Harrie Kwinten / Amazon" and "Printing: Amazon". If KDP's free ISBNs are used, the imprint will read "Independently published". Please confirm the wording you want.
3. **Subtitle for the title page.** The cover says *"How a world champion thinks, leads and builds winning teams"*, but the colophon says *"Doing Is the Best Way of Thinking / The Practical Method for Leadership, Performance Culture and Commercial Effectiveness"* (NL equivalents). **The sample title page uses the cover subtitle. Please choose one.**
4. **Back-cover text.** The "Back Cover Text" / "Achterflaptekst" sections are cover copy and are **left out** of the interior. Please confirm.
5. **Colophon credits.** "Cover design and layout: Harrie Kwinten". Please confirm or update now that a typesetter is involved.
6. A **half-title page** (book title only) is included on page 1 of the layout. It is standard for premium editions and costs no content.

---

## 3. Design system

### 3.1 Page geometry (6 × 9 in, no bleed)

| | Value | KDP minimum |
|---|---|---|
| Inside (gutter) margin | **0.875 in** | 0.5 in for 151–300 pages |
| Outside margin | 0.60 in | 0.25 in |
| Top / bottom margin | 0.80 in / 0.80 in (running head and folio sit inside these) | 0.25 in |
| Text block | 4.525 × 7.40 in (≈ 62–66 characters per line) | — |
| Margins | Mirrored (gutter always on the binding side) | — |

**Estimated page count** (trial layout): **English ≈ 167 pp · Dutch ≈ 165 pp**, which falls in KDP's 151–300 page band. Both editions are typeset separately; their pagination already differs.
**Hardcover:** KDP applies the same gutter table to hardcovers, and 6 × 9 is an available hardcover trim. Because case binding swallows more of the gutter, I propose giving the hardcover an extra +0.125 in inside margin (1.0 in) and re-flowing it as its own file; its copyright page will carry the hardcover ISBN. The two print files will therefore **not** be assumed identical. *(KDP figures to be re-checked against KDP's own help pages at final export.)*

### 3.2 Typography (all fonts under the SIL Open Font License: commercial use and PDF embedding allowed, full Dutch character support)

| Role | Font | Setting |
|---|---|---|
| Body text | **Source Serif 4 (Small Text optical size)** | 10.4 / 14.6 pt, justified, 1.2 em first-line indent, no indent after headings/blocks |
| Chapter / part titles | **Barlow Condensed SemiBold**, capitals (echoes the cover's condensed headline type) | Chapter 21 pt; Part 25 pt; balanced line breaks |
| Chapter number | Barlow Condensed, **orange** "01" 40 pt + letter-spaced label "CHAPTER" | |
| Part numeral | Source Serif 4 Display SemiBold, 84 pt Roman numeral, orange "PART" label | |
| Subheadings | **Barlow SemiBold** 10.6 pt | |
| Labels (Statement, Practical example, Reflection questions) | Barlow SemiBold 7.2 pt, capitals, wide letter-spacing, orange | |
| Statement text | Source Serif 4 Display Italic 12.6 / 17 pt, 2.2 pt orange vertical rule | |
| Running heads / folios | Barlow Medium 6.6 pt capitals / 8.5 pt | |

Hyphenation: **en-GB** rules for English (the manuscript uses British spelling: organisation, behaviour), **nl-NL** rules for Dutch; minimum word length 6, at least 3 letters before and after a break. Headings and titles are never hyphenated. Widows and orphans: at least 2 lines.

### 3.3 Colour
Black and dark grey (#1a1a1a) for all text. Orange (#e5531a, matched to the cover) is used only for chapter numbers, part labels, the title-page accent, the short heading rules, labels, the statement rule and list numerals. Orange never carries information on its own: every orange element is also distinguished by position, size or label text. The grayscale previews show the black-and-white result.

### 3.4 Page furniture
- **Running heads:** verso pages show the book title; recto pages show the current chapter (or Foreword/Introduction). There are none on title, copyright, contents, part, chapter-opening or blank pages.
- **Folios:** bottom outside corner. Front matter uses lower-case Roman numerals; the main text restarts at **1 on the Foreword**. Blank pages and part pages have no folio.
- **Part openings:** always recto, followed by a blank verso, and the first chapter of each part opens recto.
- **Chapter openings:** a new page each time, with a dropped opening. *Option:* force every chapter onto a recto page (more premium; adds about 12 pages per book).
- **Practical example:** a thin black rule above, an orange label, unindented paragraphs, and a short closing rule.
- **Reflection questions:** a rule, a label, and a hanging list with orange numerals. No shaded boxes anywhere.
- **Images:** full text width, proportional scaling, never split across pages.

---

## 4. Decisions needed before Phase 3 (full production)

1. **Interior ink: black & white or colour?** The infographics are in colour. KDP prints an entire book in one ink type. The sample is built so that both options work; the PDF shows colour.
   - **B&W (recommended for cost):** orange accents are converted to a calibrated dark grey, and the infographics are converted to grayscale with a contrast check.
   - **Premium colour:** the colours shown in the sample.
2. **Paper:** white or cream (only relevant for B&W).
3. **Subtitle** for the title page (see 2.6-3).
4. **Chapter title wording** (2.5-3) and **capitalisation** (2.5-4).
5. **ISBNs × 4**, plus the imprint and colophon wording (2.6-1, 2, 5).
6. **Images:** high-resolution infographics and the 1965 photo (2.3); approval to typeset the English chapter 7 table (2.4).
7. **Chapters on recto pages only?** (3.4)
8. Approval of the typography and layout direction shown in the sample.

## 5. Production workflow after approval
1. Apply all decisions to the parser and stylesheet (a single source drives both languages).
2. Full typesetting of 4 print files: EN/NL × paperback/hardcover. The hardcover gets its own gutter and ISBN.
3. Page-by-page visual QC: fix short or unbalanced pages, isolated headings and stranded lines; check every part and chapter opening and every image page.
4. EPUB 3 production from the same structured content (semantic XHTML, nav + NCX TOC, `lang` metadata, alt text, no fixed sizes), validated with **EPUBCheck**. Kindle Previewer cannot run in this Linux environment, so that check will be reported as not completed unless it can be done elsewhere.
5. Automated checks: page size, embedded fonts (no substitutions), 100% paragraph coverage against the DOCX, link and TOC check. Then `FINAL_DELIVERABLES/` and `QUALITY_CONTROL_REPORT.md`.
