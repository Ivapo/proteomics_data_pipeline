"""
Analysis Module

Statistical analysis of proteomics data.
"""

from .differential_expression import DifferentialExpression
from .statistics import StatisticalTests

__all__ = ["DifferentialExpression", "StatisticalTests"]
