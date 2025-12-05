#!/bin/bash

# PhD Thesis Build Script
# Compiles Markdown chapters to PDF via Pandoc and XeLaTeX

set -e  # Exit on any error

# Color codes for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== PhD Thesis Build Script ===${NC}\n"

# Check required dependencies
echo -e "${YELLOW}Checking dependencies...${NC}"

if ! command -v pandoc &> /dev/null; then
    echo -e "${RED}Error: pandoc not found${NC}"
    echo "Install from https://pandoc.org"
    exit 1
fi

if ! command -v xelatex &> /dev/null; then
    echo -e "${RED}Error: xelatex not found${NC}"
    echo "Install TeX Live (Linux/Mac) or MiKTeX (Windows)"
    exit 1
fi

echo -e "${GREEN}✓ Dependencies found${NC}\n"

# Configuration variables
META_FILE="meta.yaml"
DEFAULTS_FILE="config/config.yaml"
FRONTMATTER_TEX="__frontmatter.filled.tex"
BACKMATTER_TEX="__backmatter.filled.tex"

# Use filtered.bib if it exists, otherwise fall back to references.bib
if [ -f "filtered.bib" ]; then
    BIB_FILE="filtered.bib"
    echo -e "${GREEN}Using filtered.bib${NC}"
else
    BIB_FILE="references.bib"
    echo -e "${YELLOW}Using references.bib (run scripts/filterbib.sh to filter citations)${NC}"
fi

# Step 1: Generate frontmatter from template
echo -e "${YELLOW}Step 1/3: Generating frontmatter...${NC}"
pandoc --wrap=preserve --template="templates/frontmatter.tex" ${META_FILE} -o ${FRONTMATTER_TEX}
echo -e "${GREEN}✓ Frontmatter generated${NC}\n"

# Step 2: Generate backmatter from template
echo -e "${YELLOW}Step 2/3: Generating backmatter...${NC}"
pandoc --wrap=preserve --template="templates/backmatter.tex" ${META_FILE} -o ${BACKMATTER_TEX}
echo -e "${GREEN}✓ Backmatter generated${NC}\n"

# Define thesis content files in compilation order
THESIS_CONTENT_FILES=(
    "chapters/intro.md"
    "chapters/background.md"
    "chapters/discussion.md"
    "chapters/conclusion.md"
    "config/references.md"    # Bibliography placement
    "appendix/appendix.md"    # Appendix section
    "chapters/papers.md"      # Part 2: Publications
)

echo -e "${GREEN}Building from: ${THESIS_CONTENT_FILES[*]}${NC}\n"

# Step 3: Compile thesis
if [[ "$1" == "--tex" ]]; then
    # Generate LaTeX file only (for debugging)
    echo -e "${YELLOW}Step 3/3: Generating LaTeX file...${NC}"
    pandoc --bibliography ${BIB_FILE} \
           --csl=config/csl-chicago-author-date.csl \
           --defaults=${DEFAULTS_FILE} \
           ${THESIS_CONTENT_FILES[*]} \
           ${META_FILE} \
           -o thesis.tex
    echo -e "${GREEN}✓ LaTeX generated: thesis.tex${NC}"
else
    # Generate PDF (default)
    echo -e "${YELLOW}Step 3/3: Compiling to PDF (this may take 1-2 minutes)...${NC}"
    pandoc --bibliography ${BIB_FILE} \
           --csl=config/csl-chicago-author-date.csl \
           --defaults=${DEFAULTS_FILE} \
           ${THESIS_CONTENT_FILES[*]} \
           ${META_FILE} \
           -o thesis.pdf
    echo -e "${GREEN}✓ PDF generated: thesis.pdf${NC}"
fi

echo -e "\n${GREEN}=== Build Complete ===${NC}"
