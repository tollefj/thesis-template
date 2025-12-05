#!/bin/sh

# Compile individual papers from Markdown to PDF
# Processes all .md files in the papers/ directory

echo "=== Compiling Individual Papers ==="

# Remove old PDFs
rm -f papers/*.pdf

# Process each markdown file in papers/
for PAPER in papers/*.md; do
  echo "---------------------------------"
  echo "Processing $PAPER"

  # Extract basename without extension
  BASENAME=$(basename $PAPER .md)

  # Compile to PDF using paper configuration
  pandoc --bibliography=filtered.bib \
         --defaults=config/config_paper.yaml \
         --csl=config/csl-chicago-author-date.csl \
         $PAPER \
         -o papers/${BASENAME}.pdf \
         --top-level-division=chapter

  echo "Generated papers/${BASENAME}.pdf"
  echo "---------------------------------"
done

echo "=== Paper Compilation Complete ==="
