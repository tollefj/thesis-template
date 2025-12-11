"""
DMD Transpiler

Converts enhanced DMD syntax to standard markdown + LaTeX that can be processed
by the existing Pandoc + Lua filter + XeLaTeX pipeline.
"""

from pathlib import Path
from typing import Optional
from .parser import DMDParser, FigureElement, TableElement, CrossReference, CalloutElement


class DMDTranspiler:
    """
    Transpile .dmd enhanced syntax to standard markdown + LaTeX

    Maintains 100% backward compatibility - standard markdown passes through unchanged.
    """

    # Map callout types to LaTeX box styles
    CALLOUT_STYLES = {
        'note': 'bluebox',
        'info': 'bluebox',
        'warning': 'yellowbox',
        'caution': 'yellowbox',
        'error': 'redbox',
        'danger': 'redbox',
        'success': 'greenbox',
        'tip': 'graybox',
    }

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.stats = {
            'figures': 0,
            'tables': 0,
            'cross_refs': 0,
            'callouts': 0,
        }

    def transpile_file(self, input_file: Path, output_file: Optional[Path] = None) -> str:
        """
        Transpile a file from enhanced syntax to standard markdown.

        Args:
            input_file: Path to input .dmd or .md file
            output_file: Optional path to write output (if None, returns string)

        Returns:
            Transpiled markdown content
        """
        content = input_file.read_text(encoding='utf-8')

        # Parse the content
        parser = DMDParser(content)

        # Check if it has enhanced syntax - if not, pass through unchanged
        if not parser.has_enhanced_syntax():
            if self.verbose:
                print(f"No enhanced syntax found in {input_file}, passing through unchanged")
            if output_file:
                output_file.write_text(content, encoding='utf-8')
            return content

        # Transpile the content
        transpiled = self.transpile_content(content)

        # Write output if requested
        if output_file:
            output_file.write_text(transpiled, encoding='utf-8')
            if self.verbose:
                print(f"Transpiled {input_file} -> {output_file}")
                print(f"  Figures: {self.stats['figures']}")
                print(f"  Tables: {self.stats['tables']}")
                print(f"  Cross-refs: {self.stats['cross_refs']}")
                print(f"  Callouts: {self.stats['callouts']}")

        return transpiled

    def transpile_content(self, content: str) -> str:
        """
        Transpile content string from enhanced syntax to standard markdown.

        Processing order matters - some transforms depend on others.
        """
        # Reset stats
        self.stats = {k: 0 for k in self.stats}

        # Process in order
        content = self.process_figures(content)
        content = self.process_tables(content)
        content = self.process_callouts(content)
        content = self.process_cross_references(content)

        return content

    def process_figures(self, content: str) -> str:
        """
        Convert figure inline syntax to standard markdown.

        Input:  @fig[id](path.jpg){w=50% short="Short"} Caption text.
        Output: ![Caption text.](path.jpg){#fig:id width=50% short-caption="Short"}
        """
        parser = DMDParser(content)
        figures = parser.parse_figures()

        # Sort by position (reverse order to maintain positions during replacement)
        figures.sort(key=lambda f: content.find(f.original), reverse=True)

        for fig in figures:
            standard_md = self._figure_to_markdown(fig)
            content = content.replace(fig.original, standard_md, 1)
            self.stats['figures'] += 1

        return content

    def process_tables(self, content: str) -> str:
        """
        Convert table inline syntax to standard markdown.

        Input:  @tbl[id] Caption text
                | Col1 | Col2 |
                |------|------|
                | A    | B    |

        Output: | Col1 | Col2 |
                |------|------|
                | A    | B    |

                : Caption text {#tbl:id}
        """
        parser = DMDParser(content)
        tables = parser.parse_tables()

        # Sort by position (reverse order)
        tables.sort(key=lambda t: content.find(t.original), reverse=True)

        for tbl in tables:
            # For tables, we need to replace the @tbl[id] line with proper caption syntax
            # The table markdown should follow immediately after
            standard_caption = f": {tbl.caption} {{#tbl:{tbl.label}}}"

            # Replace just the @tbl[id] Caption line
            # The actual table markdown is already there
            content = content.replace(tbl.original, '', 1)

            # Find the table that follows and append caption
            # Look for the next table (starts with |)
            pos = content.find(tbl.original[:0])  # Position where we removed @tbl

            # Find end of table (blank line after table)
            lines = content[pos:].split('\n')
            table_end_idx = 0
            in_table = False
            for i, line in enumerate(lines):
                if line.strip().startswith('|'):
                    in_table = True
                elif in_table and line.strip() == '':
                    table_end_idx = i
                    break

            if table_end_idx > 0:
                # Insert caption after table
                before_table = '\n'.join(lines[:table_end_idx])
                after_table = '\n'.join(lines[table_end_idx:])
                content = content[:pos] + before_table + '\n\n' + standard_caption + after_table

            self.stats['tables'] += 1

        return content

    def process_cross_references(self, content: str) -> str:
        """
        Convert unified cross-reference syntax to appropriate format.

        Input:  @fig[label] or @fig[label](custom text)
                @tbl[label] or @tbl[label](custom text)
                @eq[label] or @eq[label](custom text)
                @sec[label]

        Output: @fig:label (pandoc native)
                @tbl:label (pandoc native)
                \\eqref{eq:label} (LaTeX)
                @sec:label (pandoc native)
        """
        parser = DMDParser(content)
        refs = parser.parse_cross_references()

        # Sort by position (reverse order)
        refs.sort(key=lambda r: content.find(r.original), reverse=True)

        for ref in refs:
            standard_ref = self._reference_to_standard(ref)
            content = content.replace(ref.original, standard_ref, 1)
            self.stats['cross_refs'] += 1

        return content

    def process_callouts(self, content: str) -> str:
        """
        Convert callout syntax to div boxes.

        Input:  @note{Important concept}
                @warning{Be careful}

        Output: ::: {.bluebox title="Note"}
                Important concept
                :::
        """
        parser = DMDParser(content)
        callouts = parser.parse_callouts()

        # Sort by position (reverse order)
        callouts.sort(key=lambda c: content.find(c.original), reverse=True)

        for callout in callouts:
            div_box = self._callout_to_div(callout)
            content = content.replace(callout.original, div_box, 1)
            self.stats['callouts'] += 1

        return content

    def _figure_to_markdown(self, fig: FigureElement) -> str:
        """Convert FigureElement to standard markdown with attributes"""
        # Build attribute string
        attrs = [f'#fig:{fig.label}']

        for key, value in fig.attributes.items():
            attrs.append(f'{key}={value}')

        # Handle short-caption with proper escaping
        if 'short-caption' in fig.attributes:
            # Already in attributes, format it properly
            short = fig.attributes['short-caption']
            # Remove from attrs list (we'll add it properly formatted)
            attrs = [a for a in attrs if not a.startswith('short-caption')]
            attrs.append(f'short-caption="{short}"')

        attr_str = ' '.join(attrs)

        return f'![{fig.caption}]({fig.image_path}){{{attr_str}}}'

    def _reference_to_standard(self, ref: CrossReference) -> str:
        """Convert CrossReference to standard syntax"""
        if ref.custom_text:
            # Custom text provided
            if ref.ref_type == 'eq':
                # Equations use LaTeX \eqref
                return f'{ref.custom_text} \\eqref{{eq:{ref.label}}}'
            else:
                # Figures, tables, sections use pandoc link syntax
                return f'[{ref.custom_text}](#{ref.ref_type}:{ref.label})'
        else:
            # Standard reference
            if ref.ref_type == 'eq':
                # Equations use LaTeX \eqref
                return f'\\eqref{{eq:{ref.label}}}'
            else:
                # Figures, tables, sections use pandoc @ syntax
                return f'@{ref.ref_type}:{ref.label}'

    def _callout_to_div(self, callout: CalloutElement) -> str:
        """Convert CalloutElement to div box"""
        box_style = self.CALLOUT_STYLES.get(callout.callout_type, 'graybox')
        title = callout.callout_type.capitalize()

        return f'::: {{.{box_style} title="{title}"}}\n{callout.content}\n:::'
