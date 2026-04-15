"""
tmd (thesis markdown) — extended markdown syntax for academic document authoring.
"""

__version__ = "0.1.0"
__author__ = "tmd"

from .transpile import Transpiler
from .parser import Parser
from .validator import Validator

__all__ = ["Transpiler", "Parser", "Validator"]
