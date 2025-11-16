"""
Validators

Input validation functions.
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional


def validate_dataframe(df: pd.DataFrame, 
                      required_columns: Optional[List[str]] = None,
                      min_rows: int = 1) -> None:
    """
    Validate DataFrame structure.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        min_rows: Minimum number of rows required
        
    Raises:
        ValueError: If validation fails
    """
    if df is None:
        raise ValueError("DataFrame cannot be None")
    
    if len(df) < min_rows:
        raise ValueError(f"DataFrame must have at least {min_rows} rows, got {len(df)}")
    
    if required_columns:
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")


def validate_file_path(file_path: str, must_exist: bool = True) -> Path:
    """
    Validate file path.
    
    Args:
        file_path: Path to file
        must_exist: Whether file must already exist
        
    Returns:
        Path object
        
    Raises:
        FileNotFoundError: If file doesn't exist and must_exist=True
        ValueError: If path is invalid
    """
    path = Path(file_path)
    
    if must_exist and not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return path


def validate_sample_groups(control: List[str], 
                          treatment: List[str],
                          all_samples: List[str]) -> None:
    """
    Validate sample group definitions.
    
    Args:
        control: Control sample names
        treatment: Treatment sample names
        all_samples: All available sample names
        
    Raises:
        ValueError: If validation fails
    """
    if not control:
        raise ValueError("Control group cannot be empty")
    
    if not treatment:
        raise ValueError("Treatment group cannot be empty")
    
    # Check for overlap
    overlap = set(control) & set(treatment)
    if overlap:
        raise ValueError(f"Samples appear in both groups: {overlap}")
    
    # Check all samples exist
    all_specified = set(control) | set(treatment)
    missing = all_specified - set(all_samples)
    if missing:
        raise ValueError(f"Samples not found in data: {missing}")
