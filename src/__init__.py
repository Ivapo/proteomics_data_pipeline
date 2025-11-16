"""
Proteomics Data Pipeline

A modular pipeline for proteomics data analysis using PRIDE repository.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Import main modules (will be populated as we build)
# from .data_acquisition import PRIDEClient
# from .data_processing import Normalizer
# from .analysis import DifferentialExpression
