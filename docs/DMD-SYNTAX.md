# DMD (Document Markdown) - Enhanced Syntax Reference

DMD is a transpiled language for academic document authoring that provides clean, intuitive syntax while maintaining 100% backward compatibility with standard markdown.

## Philosophy

DMD enhances markdown with inline shorthand syntax that transpiles to standard markdown + LaTeX, which then flows through the existing Pandoc + Lua filter + XeLaTeX pipeline.

**Key principles:**
- Clean, readable syntax
- Backward compatible (all standard markdown works)
- Mixed mode (use both syntaxes in same document)
- Transpiles to standard formats (no custom parsers in build)

## Enhanced Syntax Elements

### 1. Figures

**DMD Syntax:**
```markdown
@fig[label](path/to/image.jpg){w=50% short="Short caption"} Full detailed caption text.
```

**Transpiles to:**
```markdown
![Full detailed caption text.](path/to/image.jpg){#fig:label width=50% short-caption="Short caption"}
```

**Attributes:**
- `w=50%` → `width=50%` (also `h` for height)
- `short="text"` → `short-caption="text"`
- Any other attribute passes through as-is

**Examples:**
```markdown
@fig[architecture](images/system.png){w=80%} The system architecture diagram.

@fig[plot](images/results.pdf){w=60% short="Results"} Experimental results showing performance improvements across all test cases.
```

### 2. Tables

**DMD Syntax:**
```markdown
@tbl[label] Caption text

| Column 1 | Column 2 |
|----------|----------|
| Data     | Data     |
```

**Transpiles to:**
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Data     | Data     |

: Caption text {#tbl:label}
```

**Example:**
```markdown
@tbl[results] Performance comparison of different methods

| Method   | Accuracy | F1-Score |
|----------|----------|----------|
| Baseline | 85.2%    | 0.83     |
| Proposed | 92.1%    | 0.91     |
```

### 3. Cross-References

**DMD Syntax:**
```markdown
@fig[label]     # Reference a figure
@tbl[label]     # Reference a table
@eq[label]      # Reference an equation
@sec[label]     # Reference a section
```

**Transpiles to:**
```markdown
@fig:label              # Pandoc native (figures, tables, sections)
\eqref{eq:label}        # LaTeX (equations)
```

**Examples:**
```markdown
As shown in @fig[architecture], the system consists of three layers.

Results in @tbl[results] demonstrate improvements.

According to @eq[maxwell], electromagnetic waves propagate at...

See @sec[background] for detailed discussion.
```

**With custom text** (for figures, tables, sections):
```markdown
@fig[arch](as shown in the diagram)
# Transpiles to: [as shown in the diagram](#fig:arch)
```

### 4. Semantic Callouts

**DMD Syntax:**
```markdown
@note{Content here}
@warning{Content here}
@tip{Content here}
@error{Content here}
@success{Content here}
```

**Transpiles to:**
```markdown
::: {.bluebox title="Note"}
Content here
:::
```

**Mapping:**
- `@note` → bluebox
- `@warning` → yellowbox
- `@tip` → graybox
- `@error` → redbox
- `@success` → greenbox

**Examples:**
```markdown
@note{This is an important concept to remember.}

@warning{Be careful when applying this technique in production.}

@tip{Pro tip: Always validate your results with multiple test cases.}
```

## Backward Compatibility

DMD maintains 100% backward compatibility with standard markdown:

```markdown
# This is standard markdown

![Standard figure](image.jpg){#fig:std width=50%}

See @fig:std for details.
```

**Everything works unchanged!**

## Mixed Mode

You can freely mix DMD and standard syntax in the same document:

```markdown
# Chapter

Standard figure: ![Caption](img1.jpg){#fig:std width=50%}

DMD figure: @fig[new](img2.jpg){w=50%} Enhanced caption.

Reference both: @fig[std] and @fig[new].
```

## File Extensions

- `.dmd` - DMD enhanced markdown (transpiled before build)
- `.md` - Standard markdown (passed through, but DMD syntax still works)

## Usage

### Command Line

```bash
# Transpile a single file
./scripts/dmd-transpile chapters/intro.dmd

# Transpile with validation
./scripts/dmd-transpile chapters/intro.dmd --validate --verbose

# Dry run (show output without writing)
./scripts/dmd-transpile chapters/intro.dmd --dry-run
```

### In Build Pipeline

DMD transpilation will be integrated into the build system automatically when `dmd.yaml` is detected.

## Benefits

1. **More Readable**: `@fig[id](path) Caption` is clearer than `![Caption](path){#fig:id}`
2. **Less Typing**: Short attribute names (`w=50%` vs `width=50%`)
3. **Unified Syntax**: Always use `@type[label]` pattern for references
4. **Semantic Clarity**: `@note{text}` is self-documenting
5. **No Lock-in**: Transpiles to standard formats, can always fall back

## Comparison

### Standard Markdown
```markdown
![Long detailed caption about experimental methodology and setup procedures used in this comprehensive study.](images/experiment.jpg){#fig:exp width=60% short-caption="Experimental setup"}

See Figure @fig:exp for the experimental setup.
```

### DMD Enhanced
```markdown
@fig[exp](images/experiment.jpg){w=60% short="Experimental setup"} Long detailed caption about experimental methodology and setup procedures used in this comprehensive study.

See @fig[exp] for the experimental setup.
```

**Result: Cleaner, more maintainable, easier to write.**

## Validation

DMD validates your documents before building:

- **Duplicate labels**: Catches fig/tbl/eq labels used multiple times
- **Undefined references**: Warns about @fig[missing] with no definition
- **Missing files**: Checks that image/paper PDF files exist
- **Helpful suggestions**: "Did you mean @fig:example?"

## Editor Support

For syntax highlighting:

- `.dmd` files are markdown with extensions
- Configure your editor to treat `.dmd` as markdown
- Highlighting for `@fig[`, `@tbl[`, etc. works out of the box in most editors

## Next Steps

- See `chapters/example.dmd` for a complete working example
- See `dmd.yaml.example` for document structure configuration
- Check `tests/test_transpile.py` for more syntax examples
