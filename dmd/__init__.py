"""
DMD (Document Markdown) - Transpiled language for academic document authoring

A transpiler that converts enhanced inline syntax to standard markdown + LaTeX,
designed for complex PDF rendering with Pandoc, Lua filters, and XeLaTeX.
"""

__version__ = "0.1.0"
__author__ = "DMD Project"

from .transpile import DMDTranspiler
from .parser import DMDParser
from .validator import DMDValidator

__all__ = ["DMDTranspiler", "DMDParser", "DMDValidator"]
