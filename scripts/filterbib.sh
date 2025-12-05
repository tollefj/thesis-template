#!/bin/bash

# Bibliography Filtering Script
# Extracts only cited references from references.bib to create filtered.bib
# This reduces file size when working with large bibliography databases

set -e

BIB_FILE="references.bib"
DEFAULTS_FILE="config/config.yaml"

# Define all files that contain citations
ALL_FILES=(
  "chapters/intro.md"
  "chapters/background.md"
  "chapters/discussion.md"
  "chapters/conclusion.md"
  "appendix/appendix.md"
  # Add paper files here if they contain citations
  # "papers/paper1.md"
  # "papers/paper2.md"
)

echo "=== Filtering Bibliography ==="
echo "Source: ${BIB_FILE}"

# Fix URL-encoded underscores in BibTeX file (common in some export formats)
sed 's/\\%5F/_/g' "${BIB_FILE}" > "${BIB_FILE}.tmp" && mv "${BIB_FILE}.tmp" "${BIB_FILE}"

# Run pandoc with filterbib.lua to extract cited references
# Output to /dev/null since we only need the filtered.bib side effect
pandoc --bibliography ${BIB_FILE} \
       --csl=config/acl.csl \
       --defaults=${DEFAULTS_FILE} \
       --lua-filter=latex/filters/filterbib.lua \
       ${ALL_FILES[*]} \
       -o /dev/null

echo "Generated: filtered.bib"
echo "=== Bibliography Filtering Complete ==="
