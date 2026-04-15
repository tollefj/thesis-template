# thesis template

write your thesis in markdown, build to pdf via pandoc and xelatex. extended syntax for figures, tables, and callouts transpiles automatically on build.

[getting started](#getting-started) · [structure](#structure) · [writing](#writing) · [building](#building) · [papers](#papers) · [troubleshooting](#troubleshooting)

---

## getting started

### prerequisites

- pandoc 2.x or 3.x
- xelatex (tex live or miktex)
- python 3.8+

### setup

1. add required images to `images/`:
   - `part1-placeholder.jpg` (1200×800px) — part 1 divider
   - `part2-placeholder.jpg` (1200×800px) — part 2 divider
   - `signature.jpg` (800×200px) — preface signature

   create with imagemagick:
   ```bash
   convert -size 1200x800 xc:lightblue images/part1-placeholder.jpg
   convert -size 1200x800 xc:lightgray images/part2-placeholder.jpg
   convert -size 800x200 xc:white images/signature.jpg
   ```

2. fill in `meta.yaml` — title, author, abstract, supervisors, acknowledgements.

3. build:
   ```bash
   ./build.sh
   ```

open `thesis.pdf` alongside `chapters/intro.md`. the intro chapter has working examples of all features.

---

## structure

```
├── build.sh           # main build script
├── meta.yaml          # thesis metadata
├── references.bib     # bibliography
├── chapters/          # thesis chapters
├── papers/            # published papers (part 2)
├── appendix/          # appendix content
├── images/            # figures and graphics
├── config/            # pandoc config, citation style
├── latex/             # packages, commands, lua filters
└── templates/         # frontmatter/backmatter latex templates
```

add your chapters to `chapters/` and list them in `build.sh` under `THESIS_CONTENT_FILES`.

---

## writing

standard markdown works throughout. the build also supports extended syntax for figures, tables, cross-references, and callouts.

### figures

extended syntax:
```markdown
@fig[label](images/plot.png){w=60% short="short caption"} full caption text.
```

attributes:
- `w=50%` / `h=50%` — width / height
- `short="text"` — short caption for the list of figures

standard pandoc syntax also works:
```markdown
![full caption](images/plot.png){#fig:label width=60% short-caption="short caption"}
```

### tables

```markdown
@tbl[label] caption text

| col a | col b |
|-------|-------|
| data  | data  |
```

### cross-references

```markdown
@fig[label]      # figure
@tbl[label]      # table
@eq[label]       # equation
@sec[label]      # section
```

standard pandoc cross-reference syntax (`@fig:label`) also works.

### callouts

```markdown
@note{important observation.}
@warning{be careful here.}
@tip{pro tip: always validate.}
```

available types: `note` (blue), `warning` (yellow), `tip` (gray), `error` (red), `success` (green).

---

## building

```bash
./build.sh          # compile to thesis.pdf
./build.sh --tex    # generate latex only (debugging)
```

the build script:
1. generates frontmatter/backmatter from `meta.yaml`
2. transpiles extended syntax in chapter files (automatic)
3. runs pandoc with lua filters
4. compiles with xelatex

output: `thesis.pdf`

### bibliography

put citations in `references.bib`. for large bibliography files, filter to only cited references:

```bash
scripts/filterbib.sh
```

---

## papers

part 2 supports including published papers as pdfs or writing them in markdown.

**option 1: include existing pdf**

add to `chapters/papers.md`:
```latex
\paperheader{paper i}{title}{authors}{conference 2024}
\addcontentsline{toc}{section}{paper i: title}
\includepdfclean{papers/your-paper.pdf}
```

**option 2: write in markdown**

create a `.md` file in `papers/`, then compile:
```bash
scripts/papers.sh    # compiles all .md files in papers/ to pdf
```

then include the generated pdf using `\includepdfclean`.

---

## troubleshooting

**missing dependencies** — install pandoc and xelatex

**missing images** — add required images to `images/` (see [getting started](#getting-started))

**bibliography not updating** — run `scripts/filterbib.sh`

**xelatex font errors** — ensure libertine fonts are installed (tex live: `texlive-fonts-extra`)
