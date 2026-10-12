#!/bin/bash
# Build all four print PDFs with figure optimisation, run QC, copy to the repository.
# Usage: finalize.sh <scratch dir> <repo dir>
set -e
S=$1; R=$2
cd "$S"
build() {  # lang edition css outname
  L=$1; ED=$2; CSS=$3; OUT=$4
  python3 -I tools/optimize_figures.py $L $L.json build/$L/book_$ED.html build/$L/book_$ED.pdf $CSS ${L}_layout_$ED.json 2>&1 | grep -v "Ignored\|WARNING" > qc_${L}_${ED}_opt.log
  python3 -I -c "
import pymupdf
d=pymupdf.open('build/$L/book_$ED.pdf')
d.set_metadata({'title': {'en':'Prepare to Win','nl':'Winnen begint in de voorbereiding'}['$L'], 'author':'Harrie Kwinten',
                'subject': 'Print interior, 6 x 9 in, $ED', 'creator':'Elite Publishing', 'producer':'WeasyPrint'})
d.save('$R/FINAL_DELIVERABLES/$OUT', garbage=4, deflate=True)"
  INS=$([ $ED = hardcover ] && echo 1.0 || echo 0.875)
  python3 -I tools/layout_qc.py "$R/FINAL_DELIVERABLES/$OUT" $INS > qc_${L}_${ED}_layout.log
  python3 -I tools/integrity.py $L "$R/FINAL_DELIVERABLES/$OUT" src_$L/$L.docx $L.json > qc_${L}_${ED}_integrity.log
}
LANGS=${3:-"en nl"}
mkdir -p "$R/FINAL_DELIVERABLES/ENGLISH_PREPARE_TO_WIN" "$R/FINAL_DELIVERABLES/DUTCH_WINNEN_BEGINT_IN_DE_VOORBEREIDING"
for L in $LANGS; do
  if [ $L = en ]; then D=ENGLISH_PREPARE_TO_WIN/Prepare_to_Win; else D=DUTCH_WINNEN_BEGINT_IN_DE_VOORBEREIDING/Winnen_Begint; fi
  build $L paperback print.css ${D}_Paperback.pdf &
  build $L hardcover hardcover.css ${D}_Hardcover.pdf &
done
wait
echo FINALIZE_DONE
