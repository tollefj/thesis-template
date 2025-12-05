# Papers (Part 2)

## Option 1: Include Published PDF

Place PDF here and add to `chapters/papers.md`:

```latex
\paperheader{Paper I}{Title}{Authors}{Conference 2024}
\addcontentsline{toc}{section}{Paper I: Title}
\includepdfclean{papers/your-paper.pdf}
```

## Option 2: Write in Markdown

Create `.md` file (see `example-paper.md`) and compile:

```bash
scripts/papers.sh    # Compiles all .md files
```

Then include the generated PDF in `chapters/papers.md` using `\includepdfclean`.

**Note:** `\includepdfclean` masks original page numbers so thesis page numbers appear.
