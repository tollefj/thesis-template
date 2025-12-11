"""
DMD Syntax Parser

Parses enhanced inline syntax for figures, tables, cross-references, and callouts.
"""

import re
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple


@dataclass
class FigureElement:
    """Parsed figure element"""
    label: str
    image_path: str
    caption: str
    attributes: Dict[str, str]
    line_number: int
    original: str


@dataclass
class TableElement:
    """Parsed table element"""
    label: str
    caption: str
    line_number: int
    original: str


@dataclass
class CrossReference:
    """Parsed cross-reference"""
    ref_type: str  # 'fig', 'tbl', 'eq', 'sec'
    label: str
    custom_text: Optional[str]
    line_number: int
    original: str


@dataclass
class CalloutElement:
    """Parsed callout element"""
    callout_type: str  # 'note', 'warning', 'tip', etc.
    content: str
    line_number: int
    original: str


class DMDParser:
    """Parser for DMD enhanced syntax"""

    # Figure syntax: @fig[id](path.jpg){w=50% short="Short"} Caption text.
    FIGURE_PATTERN = re.compile(
        r'@fig\[([a-zA-Z0-9_-]+)\]\(([^)]+)\)(?:\{([^}]*)\})?\s*([^\n@]+?)(?=\n|@|\Z)',
        re.MULTILINE
    )

    # Table syntax: @tbl[id] Caption
    TABLE_PATTERN = re.compile(
        r'@tbl\[([a-zA-Z0-9_-]+)\]\s+([^\n]+)',
        re.MULTILINE
    )

    # Cross-reference: @fig[label] or @fig[label](custom text)
    CROSS_REF_PATTERN = re.compile(
        r'@(fig|tbl|eq|sec)\[([a-zA-Z0-9_-]+)\](?:\(([^)]+)\))?'
    )

    # Callout: @note{content}, @warning{content}, @tip{content}
    CALLOUT_PATTERN = re.compile(
        r'@(note|warning|tip|error|success)\{([^}]+)\}'
    )

    def __init__(self, content: str):
        self.content = content
        self.lines = content.split('\n')

    def get_line_number(self, match_start: int) -> int:
        """Get line number for a match position"""
        return self.content[:match_start].count('\n') + 1

    def parse_figures(self) -> List[FigureElement]:
        """Parse all figure elements"""
        figures = []
        for match in self.FIGURE_PATTERN.finditer(self.content):
            label = match.group(1)
            image_path = match.group(2)
            attr_str = match.group(3) or ""
            caption = match.group(4).strip()

            # Parse attributes
            attributes = self._parse_attributes(attr_str)

            figures.append(FigureElement(
                label=label,
                image_path=image_path,
                caption=caption,
                attributes=attributes,
                line_number=self.get_line_number(match.start()),
                original=match.group(0)
            ))

        return figures

    def parse_tables(self) -> List[TableElement]:
        """Parse all table elements"""
        tables = []
        for match in self.TABLE_PATTERN.finditer(self.content):
            label = match.group(1)
            caption = match.group(2).strip()

            tables.append(TableElement(
                label=label,
                caption=caption,
                line_number=self.get_line_number(match.start()),
                original=match.group(0)
            ))

        return tables

    def parse_cross_references(self) -> List[CrossReference]:
        """Parse all cross-references"""
        refs = []
        for match in self.CROSS_REF_PATTERN.finditer(self.content):
            ref_type = match.group(1)
            label = match.group(2)
            custom_text = match.group(3)

            refs.append(CrossReference(
                ref_type=ref_type,
                label=label,
                custom_text=custom_text,
                line_number=self.get_line_number(match.start()),
                original=match.group(0)
            ))

        return refs

    def parse_callouts(self) -> List[CalloutElement]:
        """Parse all callout elements"""
        callouts = []
        for match in self.CALLOUT_PATTERN.finditer(self.content):
            callout_type = match.group(1)
            content = match.group(2)

            callouts.append(CalloutElement(
                callout_type=callout_type,
                content=content,
                line_number=self.get_line_number(match.start()),
                original=match.group(0)
            ))

        return callouts

    def _parse_attributes(self, attr_str: str) -> Dict[str, str]:
        """
        Parse attribute string like 'w=50% short="Short caption"'
        Returns dict like {'width': '50%', 'short-caption': 'Short caption'}
        """
        attributes = {}

        if not attr_str:
            return attributes

        # Handle quoted values: key="value with spaces"
        quoted_pattern = r'(\w+)="([^"]*)"'
        for match in re.finditer(quoted_pattern, attr_str):
            key = match.group(1)
            value = match.group(2)
            # Normalize attribute names
            if key == 'w':
                key = 'width'
            elif key == 'h':
                key = 'height'
            elif key == 'short':
                key = 'short-caption'
            attributes[key] = value

        # Handle unquoted values: key=value
        unquoted_pattern = r'(\w+)=([^\s"]+)'
        for match in re.finditer(unquoted_pattern, attr_str):
            key = match.group(1)
            value = match.group(2)
            # Skip if already processed as quoted
            if key not in attributes:
                if key == 'w':
                    key = 'width'
                elif key == 'h':
                    key = 'height'
                attributes[key] = value

        return attributes

    def has_enhanced_syntax(self) -> bool:
        """Check if content contains any DMD enhanced syntax"""
        patterns = [
            self.FIGURE_PATTERN,
            self.TABLE_PATTERN,
            self.CROSS_REF_PATTERN,
            self.CALLOUT_PATTERN
        ]

        for pattern in patterns:
            if pattern.search(self.content):
                return True

        return False
