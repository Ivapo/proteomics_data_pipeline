"""
Test utilities module.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from utils import setup_logger, ensure_dir, validate_dataframe
import pandas as pd


def test_setup_logger():
    """Test logger setup."""
    logger = setup_logger(name="test_logger", level="INFO")
    assert logger is not None
    assert logger.name == "test_logger"


def test_ensure_dir(tmp_path):
    """Test directory creation."""
    test_dir = tmp_path / "test_folder"
    result = ensure_dir(str(test_dir))
    assert result.exists()
    assert result.is_dir()


def test_validate_dataframe():
    """Test DataFrame validation."""
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    
    # Should not raise
    validate_dataframe(df, required_columns=["col1", "col2"])
    
    # Should raise for missing columns
    with pytest.raises(ValueError):
        validate_dataframe(df, required_columns=["col1", "col3"])
