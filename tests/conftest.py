"""
Test Configuration

pytest configuration file.
"""

import sys
from pathlib import Path

# Add src to path for all tests
sys.path.insert(0, str(Path(__file__).parent / "src"))
