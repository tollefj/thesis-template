# DMD (Document Markdown) - Getting Started

DMD is a transpiled language that makes writing academic documents cleaner and more intuitive while maintaining 100% compatibility with your existing markdown files.

## What is DMD?

DMD provides enhanced inline syntax for common academic writing patterns:

**Before (Standard Markdown):**
```markdown
![Long caption with experimental details...](images/plot.jpg){#fig:results width=50% short-caption="Results"}
```

**After (DMD):**
```markdown
@fig[results](images/plot.jpg){w=50% short="Results"} Long caption with experimental details...
```

**It transpiles to standard markdown** that works with your existing Pandoc + LaTeX pipeline.

## Quick Start

### 1. Try the Example

```bash
# Transpile the example file
./scripts/dmd-transpile chapters/example.dmd

# View the output
cat chapters/example.md
```

### 2. Create Your First .dmd File

```markdown
# My Chapter

@fig[myplot](images/data.png){w=60%} This figure shows interesting results.

As we can see in @fig[myplot], the trend is clear.

@note{This is an important observation.}
```

### 3. Transpile and Build

```bash
# Transpile
./scripts/dmd-transpile chapters/mychapter.dmd

# Build (using existing build.sh)
./build.sh
```

## Installation

DMD is already set up in this project. The transpiler is in the `dmd/` directory.

**Dependencies:**
- Python 3.8+
- No additional packages required (uses stdlib only)

## Features

### Enhanced Figures
```markdown
@fig[label](path){w=50% short="Short"} Full caption.
```

### Enhanced Tables
```markdown
@tbl[label] Caption
| A | B |
|---|---|
| 1 | 2 |
```

### Unified Cross-References
```markdown
See @fig[label], @tbl[label], @eq[label], @sec[label]
```

### Semantic Callouts
```markdown
@note{Important concept}
@warning{Be careful}
@tip{Pro tip here}
```

## Document Structure with dmd.yaml

Create a `dmd.yaml` file to define your document structure with flexible N-part organization:

```yaml
document:
  type: thesis
  title: "My Thesis"
  author: "Your Name"

structure:
  parts:
    - id: research
      number: 1
      title: "Research"
      image: "images/part1.jpg"
      chapters:
        - chapters/intro.md
        - chapters/background.md

    - id: publications
      number: 2
      title: "Publications"
      image: "images/part2.jpg"
      papers:
        - number: I
          title: "Paper Title"
          file: papers/paper1.pdf
```

**Benefits:**
- Support any number of parts (not just 2)
- Easy to reorder chapters
- Auto-generate part headers
- Clear structure definition

## Backward Compatibility

**100% of your existing markdown works unchanged.**

```markdown
# This still works fine

![Standard syntax](image.jpg){#fig:old width=50%}

Reference with @fig:old or @fig[old] - both work!
```

You can mix both syntaxes in the same document.

## Validation

DMD validates your documents before building:

```bash
./scripts/dmd-transpile chapters/intro.dmd --validate --verbose
```

**Checks for:**
- Duplicate labels (fig:test defined twice)
- Undefined references (@fig[missing] not found)
- Missing image files
- Provides helpful suggestions

## CLI Reference

```bash
# Basic transpile
./scripts/dmd-transpile input.dmd

# Specify output
./scripts/dmd-transpile input.dmd output.md

# Validate before transpiling
./scripts/dmd-transpile input.dmd --validate

# Verbose mode
./scripts/dmd-transpile input.dmd --verbose

# Dry run (show without writing)
./scripts/dmd-transpile input.dmd --dry-run

# Strict mode (fail on warnings)
./scripts/dmd-transpile input.dmd --validate --strict
```

## Project Structure

```
thesis-md-template/
├── dmd/                     # Transpiler package
│   ├── __init__.py
│   ├── transpile.py        # Core transpiler
│   ├── parser.py           # Syntax parser
│   └── validator.py        # Validation
├── scripts/
│   └── dmd-transpile       # CLI script
├── chapters/
│   ├── intro.dmd           # Enhanced syntax
│   └── background.md       # Standard markdown (both work!)
├── dmd.yaml.example        # Structure config example
└── docs/
    ├── DMD-SYNTAX.md       # Complete syntax reference
    └── DMD-README.md       # This file
```

## Examples

See `chapters/example.dmd` for a complete working example demonstrating all features.

## Why DMD?

1. **Cleaner**: Less verbose, more readable
2. **Faster**: Quick shorthand for common patterns
3. **Safer**: Validation catches errors early
4. **Flexible**: N-part document structure
5. **Compatible**: 100% backward compatible, no lock-in

## Limitations

Current phase implements:
- ✅ Figure inline syntax
- ✅ Table inline syntax
- ✅ Unified cross-references
- ✅ Semantic callouts
- ✅ Validation
- ⏳ Structure generator (dmd.yaml) - Phase 2
- ⏳ Build system integration - Phase 3
- ⏳ Watch mode - Phase 6

## Next Steps

1. Read the [Complete Syntax Reference](DMD-SYNTAX.md)
2. Try the example: `./scripts/dmd-transpile chapters/example.dmd --dry-run`
3. Convert a chapter to use DMD syntax
4. Configure `dmd.yaml` for your document structure (Phase 2)

## Support

- Documentation: `docs/DMD-SYNTAX.md`
- Examples: `chapters/example.dmd`
- Tests: `tests/test_transpile.py`

## License

Same as the thesis template project.
