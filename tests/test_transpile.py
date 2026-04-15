"""
Unit tests for tmd transpiler
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tmd.transpile import Transpiler
from tmd.parser import Parser


class TestFigureSyntax:
    """Test figure inline syntax transpilation"""

    def test_basic_figure(self):
        """Test basic figure without attributes"""
        input_md = '@fig[example](images/test.jpg) This is a figure caption.'
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert '![This is a figure caption.](images/test.jpg){#fig:example}' in result
        assert transpiler.stats['figures'] == 1

    def test_figure_with_width(self):
        """Test figure with width attribute"""
        input_md = '@fig[example](images/test.jpg){w=50%} This is a figure caption.'
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert '![This is a figure caption.](images/test.jpg){#fig:example width=50%}' in result

    def test_figure_with_short_caption(self):
        """Test figure with short caption attribute"""
        input_md = '@fig[example](images/test.jpg){short="Short caption"} This is a longer figure caption with details.'
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert '#fig:example' in result
        assert 'short-caption="Short caption"' in result
        assert 'This is a longer figure caption with details.' in result

    def test_figure_with_multiple_attributes(self):
        """Test figure with multiple attributes"""
        input_md = '@fig[example](images/test.jpg){w=50% short="Short"} Caption text.'
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert '#fig:example' in result
        assert 'width=50%' in result
        assert 'short-caption="Short"' in result

    def test_multiple_figures(self):
        """Test multiple figures in same document"""
        input_md = '''
@fig[fig1](img1.jpg) Caption 1.

Some text here.

@fig[fig2](img2.jpg){w=60%} Caption 2.
'''
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert '![Caption 1.](img1.jpg){#fig:fig1}' in result
        assert '![Caption 2.](img2.jpg){#fig:fig2 width=60%}' in result
        assert transpiler.stats['figures'] == 2


class TestTableSyntax:
    """Test table inline syntax transpilation"""

    def test_basic_table(self):
        """Test basic table with caption"""
        input_md = '''@tbl[results] Performance comparison
| Method | Accuracy |
|--------|----------|
| Ours   | 95.2%    |
'''
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert ': Performance comparison {#tbl:results}' in result
        assert '| Method | Accuracy |' in result
        assert transpiler.stats['tables'] == 1


class TestCrossReferences:
    """Test cross-reference syntax transpilation"""

    def test_figure_reference(self):
        """Test figure cross-reference"""
        input_md = 'See @fig[example] for details.'
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert '@fig:example' in result
        assert transpiler.stats['cross_refs'] == 1

    def test_table_reference(self):
        """Test table cross-reference"""
        input_md = 'Results in @tbl[results] show improvements.'
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert '@tbl:results' in result

    def test_equation_reference(self):
        """Test equation cross-reference"""
        input_md = 'According to @eq[maxwell], we can derive...'
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert '\\eqref{eq:maxwell}' in result

    def test_reference_with_custom_text(self):
        """Test cross-reference with custom text"""
        input_md = 'As @fig[example](shown in the figure) demonstrates...'
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert '[shown in the figure](#fig:example)' in result

    def test_equation_reference_with_custom_text(self):
        """Test equation reference with custom text"""
        input_md = 'Using @eq[maxwell](Maxwell\'s equation), we get...'
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert 'Maxwell\'s equation \\eqref{eq:maxwell}' in result


class TestCallouts:
    """Test callout syntax transpilation"""

    def test_note_callout(self):
        """Test note callout"""
        input_md = '@note{This is an important concept to remember.}'
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert '::: {.bluebox title="Note"}' in result
        assert 'This is an important concept to remember.' in result
        assert ':::' in result
        assert transpiler.stats['callouts'] == 1

    def test_warning_callout(self):
        """Test warning callout"""
        input_md = '@warning{Be careful with this approach.}'
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert '::: {.yellowbox title="Warning"}' in result
        assert 'Be careful with this approach.' in result

    def test_tip_callout(self):
        """Test tip callout"""
        input_md = '@tip{Pro tip: use this shortcut.}'
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        assert '::: {.graybox title="Tip"}' in result


class TestBackwardCompatibility:
    """Test backward compatibility with standard markdown"""

    def test_standard_markdown_passthrough(self):
        """Test that standard markdown passes through unchanged"""
        input_md = '''
# Introduction

This is standard markdown with **bold** and *italic* text.

![Standard figure](image.jpg){#fig:standard width=50%}

See Figure @fig:standard for details.
'''
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        # Should pass through unchanged (no enhanced syntax)
        assert result == input_md

    def test_mixed_syntax(self):
        """Test mixing standard and enhanced syntax"""
        input_md = '''
# Chapter

Standard figure: ![Caption](img1.jpg){#fig:std width=50%}

Enhanced figure: @fig[enhanced](img2.jpg) Enhanced caption.

Reference both: @fig[std] and @fig[enhanced].
'''
        transpiler = Transpiler()
        result = transpiler.transpile_content(input_md)

        # Standard figure unchanged
        assert '![Caption](img1.jpg){#fig:std width=50%}' in result

        # Enhanced figure transpiled
        assert '![Enhanced caption.](img2.jpg){#fig:enhanced}' in result

        # References updated
        assert '@fig:std' in result
        assert '@fig:enhanced' in result


class TestParser:
    """Test the tmd parser"""

    def test_parse_figures(self):
        """Test parsing figure elements"""
        content = '@fig[test](img.jpg){w=50%} Caption here.'
        parser = Parser(content)
        figures = parser.parse_figures()

        assert len(figures) == 1
        assert figures[0].label == 'test'
        assert figures[0].image_path == 'img.jpg'
        assert figures[0].caption == 'Caption here.'
        assert figures[0].attributes['width'] == '50%'

    def test_parse_cross_references(self):
        """Test parsing cross-references"""
        content = 'See @fig[test], @tbl[data], and @eq[formula].'
        parser = Parser(content)
        refs = parser.parse_cross_references()

        assert len(refs) == 3
        assert refs[0].ref_type == 'fig'
        assert refs[0].label == 'test'
        assert refs[1].ref_type == 'tbl'
        assert refs[2].ref_type == 'eq'

    def test_has_enhanced_syntax(self):
        """Test detection of enhanced syntax"""
        # Standard markdown
        standard = '# Title\n\nParagraph with text.'
        parser1 = Parser(standard)
        assert not parser1.has_enhanced_syntax()

        # Enhanced syntax
        enhanced = '@fig[test](img.jpg) Caption.'
        parser2 = Parser(enhanced)
        assert parser2.has_enhanced_syntax()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
