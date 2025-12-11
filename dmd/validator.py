"""
DMD Validator

Validates cross-references, checks for duplicate labels, and provides helpful
error messages with line numbers and suggestions.
"""

from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass
from difflib import get_close_matches
from .parser import DMDParser


@dataclass
class ValidationError:
    """Validation error or warning"""
    severity: str  # 'error' or 'warning'
    file: Path
    line: int
    column: Optional[int]
    message: str
    suggestion: Optional[str] = None


class DMDValidator:
    """Validate DMD documents for common issues"""

    def __init__(self, project_dir: Path, strict: bool = False):
        self.project_dir = project_dir
        self.strict = strict
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []

        # Track all labels by type
        self.labels: Dict[str, Set[str]] = {
            'fig': set(),
            'tbl': set(),
            'eq': set(),
            'sec': set(),
        }

        # Track where labels are defined
        self.label_locations: Dict[str, Tuple[Path, int]] = {}

        # Track all references
        self.references: List[Tuple[str, str, Path, int]] = []  # (type, label, file, line)

    def validate_file(self, file_path: Path) -> bool:
        """
        Validate a single file.

        Returns True if no errors found (warnings are OK).
        """
        content = file_path.read_text(encoding='utf-8')
        parser = DMDParser(content)

        # Collect labels from figures
        figures = parser.parse_figures()
        for fig in figures:
            label = fig.label
            if label in self.labels['fig']:
                # Duplicate label
                prev_file, prev_line = self.label_locations[f'fig:{label}']
                self.errors.append(ValidationError(
                    severity='error',
                    file=file_path,
                    line=fig.line_number,
                    column=None,
                    message=f"Duplicate figure label 'fig:{label}'",
                    suggestion=f"Previous definition at {prev_file}:{prev_line}"
                ))
            else:
                self.labels['fig'].add(label)
                self.label_locations[f'fig:{label}'] = (file_path, fig.line_number)

        # Collect labels from tables
        tables = parser.parse_tables()
        for tbl in tables:
            label = tbl.label
            if label in self.labels['tbl']:
                prev_file, prev_line = self.label_locations[f'tbl:{label}']
                self.errors.append(ValidationError(
                    severity='error',
                    file=file_path,
                    line=tbl.line_number,
                    column=None,
                    message=f"Duplicate table label 'tbl:{label}'",
                    suggestion=f"Previous definition at {prev_file}:{prev_line}"
                ))
            else:
                self.labels['tbl'].add(label)
                self.label_locations[f'tbl:{label}'] = (file_path, tbl.line_number)

        # Collect cross-references
        refs = parser.parse_cross_references()
        for ref in refs:
            self.references.append((ref.ref_type, ref.label, file_path, ref.line_number))

        # Check for images that don't exist
        for fig in figures:
            image_path = self.project_dir / fig.image_path
            if not image_path.exists():
                self.warnings.append(ValidationError(
                    severity='warning',
                    file=file_path,
                    line=fig.line_number,
                    column=None,
                    message=f"Image file not found: {fig.image_path}",
                    suggestion="Check the path or create the image"
                ))

        return len(self.errors) == 0

    def validate_references(self) -> bool:
        """
        Validate all cross-references after collecting all labels.

        Returns True if no undefined references found.
        """
        for ref_type, label, file_path, line_num in self.references:
            if label not in self.labels[ref_type]:
                # Undefined reference
                similar = self._find_similar_labels(label, ref_type)

                suggestion = None
                if similar:
                    suggestion = f"Did you mean: {', '.join(similar)}?"

                self.errors.append(ValidationError(
                    severity='error',
                    file=file_path,
                    line=line_num,
                    column=None,
                    message=f"Undefined reference @{ref_type}:{label}",
                    suggestion=suggestion
                ))

        return len(self.errors) == 0

    def validate_all(self, files: List[Path]) -> bool:
        """
        Validate all files in the project.

        Returns True if validation passes (no errors).
        """
        # Phase 1: Collect all labels and check for duplicates
        for file_path in files:
            if file_path.suffix in ['.md', '.dmd']:
                self.validate_file(file_path)

        # Phase 2: Validate all references
        self.validate_references()

        return len(self.errors) == 0

    def print_report(self, verbose: bool = False):
        """Print validation report"""
        if not self.errors and not self.warnings:
            print("✓ Validation passed")
            return

        if self.errors:
            print(f"\n{len(self.errors)} error(s) found:\n")
            for error in self.errors:
                self._print_error(error)

        if self.warnings and verbose:
            print(f"\n{len(self.warnings)} warning(s):\n")
            for warning in self.warnings:
                self._print_error(warning)

        if not verbose and self.warnings:
            print(f"\n{len(self.warnings)} warning(s) (use --verbose to see them)")

    def _print_error(self, error: ValidationError):
        """Print a single error in a nice format"""
        severity_symbol = "✗" if error.severity == 'error' else "⚠"
        print(f"{severity_symbol} {error.severity.upper()}: {error.message}")
        print(f"  --> {error.file}:{error.line}")

        if error.suggestion:
            print(f"  = help: {error.suggestion}")

        print()

    def _find_similar_labels(self, label: str, ref_type: str, max_suggestions: int = 3) -> List[str]:
        """Find similar label names using fuzzy matching"""
        defined_labels = list(self.labels[ref_type])

        if not defined_labels:
            return []

        similar = get_close_matches(label, defined_labels, n=max_suggestions, cutoff=0.6)
        return [f'@{ref_type}:{s}' for s in similar]

    def has_errors(self) -> bool:
        """Check if there are any errors"""
        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        """Check if there are any warnings"""
        return len(self.warnings) > 0
