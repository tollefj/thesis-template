\chapterheader{Part 1}{Research Overview}{images/part1-placeholder.jpg}

# Introduction {#sec:intro}

This chapter demonstrates how to use this thesis template. Replace this content with your own research.

## Citations

Cite papers with `@citekey` syntax [@Darwin1859]. Multiple citations: [@Darwin1859; @Einstein1905].

In-text citations: @Darwin1859 showed that... or as shown by previous work [@Darwin1859; @Einstein1905].

## Figures

### Basic Figure (Markdown)

Simple syntax for most cases:

![This is the figure caption. It appears below the figure and in the List of Figures.](images/part1-placeholder.jpg){#fig:example width=60%}

Reference: See Figure @fig:example for details.

### Figure with Short Caption

Long captions clutter the List of Figures. Use `short-caption` attribute:

![This is a very long and detailed caption that explains the experimental setup, methodology, data collection procedures, and analysis techniques used in this particular study.](images/part2-placeholder.jpg){#fig:short-example width=50% short-caption="Experimental setup"}

The List of Figures shows "Experimental setup" while the full caption appears below the figure. Reference with @fig:short-example.

### LaTeX Figure (More Control)

\begin{figure}[htbp]
\centering
\includegraphics[width=0.4\textwidth]{images/part1-placeholder.jpg}
\caption[Short caption for list]{Full detailed caption that appears below the figure.}
\label{fig:latex-example}
\end{figure}

Reference: See Figure \ref{fig:latex-example} or use `Figure~\ref{fig:latex-example}` for non-breaking space.

### TikZ Diagrams

Create standalone LaTeX files in `figures-generated/`, compile with `pdflatex`, then include:

```latex
% Create figures-generated/mydiagram.tex
\documentclass[tikz, border=3mm]{standalone}
\usetikzlibrary{arrows.meta, positioning, shapes}
\begin{document}
\begin{tikzpicture}
    \node[draw] (A) {Input};
    \node[draw, right=2cm of A] (B) {Output};
    \draw[-stealth] (A) -- (B);
\end{tikzpicture}
\end{document}
```

Then: `![Diagram.](figures-generated/mydiagram.pdf){#fig:diag width=40%}`

## Tables

### Markdown Table

| Method   | Accuracy | Speed  |
|----------|----------|--------|
| Baseline | 85.3%    | Fast   |
| Proposed | 92.1%    | Medium |
| Oracle   | 98.5%    | Slow   |

: Comparison of methods. Reference with @tbl:comparison. {#tbl:comparison short-caption="Comparison of methods."}

### LaTeX Table

\begin{table}[htbp]
\centering
\caption[Short table caption]{Full table caption with detailed explanation.}
\label{tbl:latex-example}
\begin{tabular}{lcc}
\toprule
Method & Precision & Recall \\
\midrule
Baseline & 0.82 & 0.79 \\
Proposed & 0.91 & 0.88 \\
\bottomrule
\end{tabular}
\end{table}

Reference: See Table \ref{tbl:latex-example}.

## Math

Inline math: $E = mc^2$ and $\alpha + \beta = \gamma$.

Display math:

$$
f(x) = \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

Numbered equations:

\begin{equation}
\label{eq:example}
\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}
\end{equation}

Reference Equation \ref{eq:example} or use `\eqref{eq:example}` for parentheses: \eqref{eq:example}.

## Lists

Bullet points:

- First item
- Second item
  - Nested item
  - Another nested
- Third item

Numbered lists:

1. First step
2. Second step
3. Third step

## Code Listings

Inline code: `variable_name` or `function()`.

Code blocks:

```python
def hello_world():
    """Example function."""
    print("Hello, World!")
    return 42
```

## Text Formatting

**Bold text** for emphasis, *italic text* for terms, and ***bold italic*** for strong emphasis.

## Cross-References

Reference chapters: Chapter @sec:intro (this chapter) or Chapter @sec:background.

Reference sections within chapters by adding `{#sec:label}` after headings.

## Special Characters

LaTeX special characters need escaping in markdown:
- Ampersand: \&
- Percent: \%
- Dollar: \$
- Underscore: \_

Or use them directly in LaTeX environments.

## Colored Text Boxes

The `filterboxes.lua` filter creates colored boxes from divs:

::: {.bluebox}
This is a blue information box. Useful for highlighting key concepts or important notes.
:::

Define more colors in `latex/packages.tex` using tcolorbox.

## Research Questions

After seeing these examples, delete this content and replace with your actual thesis:

1. What is your main research question?
2. What methodology will you use?
3. What are your expected contributions?

## Thesis Structure

Chapter @sec:background provides theoretical background. Chapter @sec:discussion presents findings. Chapter @sec:conclusion summarizes contributions and future work.
