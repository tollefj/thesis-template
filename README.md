# PhD Thesis Template with DMD

Write your thesis in Markdown. Build to professional PDF using Pandoc and XeLaTeX.

**NEW**: DMD (Document Markdown) - Enhanced syntax for cleaner, more intuitive academic writing. See [DMD Documentation](docs/DMD-README.md).

## Prerequisites

- Pandoc 2.x or 3.x
- XeLaTeX (TeX Live or MiKTeX)
- Python 3 (optional, for TikZ figures)

## Quick Start

### 1. Add Required Images

Place these in `images/`:
- `part1-placeholder.jpg` (1200×800px)
- `part2-placeholder.jpg` (1200×800px)
- `signature.jpg` (800×200px)

### 2. Build and Learn

```bash
./build.sh              # Build thesis PDF
```

Open `thesis.pdf` and `chapters/intro.md` side-by-side. The intro chapter contains working examples of:
- Figures (markdown, LaTeX, TikZ)
- Tables (markdown, LaTeX)
- Citations and cross-references
- Math equations
- Code listings

See the source markdown alongside the compiled output.

### 3. Replace with Your Content

- `meta.yaml` - Title, author, abstract, acknowledgements
- `chapters/*.md` - Delete examples, write your thesis
- `references.bib` - Add your bibliography

## Structure

```
thesis-md-template/
├── build.sh           # Main build script
├── meta.yaml          # Thesis metadata
├── references.bib     # Bibliography
├── chapters/          # Your chapters (Markdown)
├── papers/            # Published papers
├── appendix/          # Appendix content
├── images/            # Images and graphics
├── config/            # Pandoc configuration
├── latex/             # LaTeX packages, commands, filters
├── templates/         # LaTeX templates
└── docs/              # Documentation
```

## Additional Scripts

```bash
scripts/papers.sh       # Compile individual papers to PDF
scripts/filterbib.sh    # Filter bibliography (for large .bib files)
scripts/dmd-transpile   # DMD transpiler (enhanced syntax)
```

## Documentation

**Start here:** `chapters/intro.md` - Working examples of all features

**DMD Enhanced Syntax:**
- `docs/DMD-README.md` - Getting started with DMD
- `docs/DMD-SYNTAX.md` - Complete syntax reference
- `chapters/example.dmd` - Working example with enhanced syntax

Also see:
- `images/README.md` - Creating required placeholder images
- `papers/README.md` - Including papers in Part 2

## Troubleshooting

**Missing dependencies**: Install Pandoc and XeLaTeX
**Missing images**: Add required images to `images/`
**Bibliography not updating**: Run `scripts/filterbib.sh`
