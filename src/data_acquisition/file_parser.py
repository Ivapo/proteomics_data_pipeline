"""
File Parser

Parses various proteomics file formats (mzTab, CSV, etc.).
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class FileParser:
    """
    Parses proteomics data files into pandas DataFrames.
    
    Supports:
    - mzTab (HUPO-PSI standard format)
    - CSV/TSV (generic tabular formats)
    - Excel files
    """
    
    def __init__(self):
        """Initialize file parser."""
        logger.info("Initialized file parser")
    
    def parse_file(self, file_path: str) -> pd.DataFrame:
        """
        Auto-detect format and parse file.
        
        Args:
            file_path: Path to proteomics data file
            
        Returns:
            DataFrame containing parsed data
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine file type and parse accordingly
        suffix = path.suffix.lower()
        
        if suffix == ".mztab":
            return self.parse_mztab(file_path)
        elif suffix in [".csv", ".tsv", ".txt"]:
            return self.parse_tabular(file_path)
        elif suffix in [".xlsx", ".xls"]:
            return self.parse_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
    
    def parse_mztab(self, file_path: str) -> pd.DataFrame:
        """
        Parse mzTab format file.
        
        mzTab is a tab-delimited format with sections:
        - MTD: Metadata lines (mzTab-version, description, etc.)
        - PRH/PRT: Protein section header and data rows
        - PEH/PEP: Peptide section header and data rows  
        - PSH/PSM: Peptide-spectrum match section header and data rows
        
        Args:
            file_path: Path to mzTab file
            
        Returns:
            DataFrame with protein quantification data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        logger.info(f"Parsing mzTab file: {file_path}")
        
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read file and separate sections
        metadata = []
        protein_header = None
        protein_rows = []
        peptide_header = None
        peptide_rows = []
        psm_header = None
        psm_rows = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Split by tab
                fields = line.split('\t')
                prefix = fields[0]
                
                # Metadata lines
                if prefix == 'MTD':
                    metadata.append(fields)
                
                # Protein section
                elif prefix == 'PRH':
                    protein_header = fields[1:]  # Skip 'PRH' prefix
                elif prefix == 'PRT':
                    protein_rows.append(fields[1:])  # Skip 'PRT' prefix
                
                # Peptide section
                elif prefix == 'PEH':
                    peptide_header = fields[1:]
                elif prefix == 'PEP':
                    peptide_rows.append(fields[1:])
                
                # PSM section
                elif prefix == 'PSH':
                    psm_header = fields[1:]
                elif prefix == 'PSM':
                    psm_rows.append(fields[1:])
        
        # Convert protein data to DataFrame
        if protein_rows and protein_header:
            df = pd.DataFrame(protein_rows, columns=protein_header)
            logger.info(f"Parsed {len(df)} proteins from mzTab")
            return df
        else:
            logger.warning("No protein data found in mzTab file")
            return pd.DataFrame()
    
    def get_mztab_metadata(self, file_path: str) -> dict:
        """
        Extract metadata from mzTab file.
        
        Args:
            file_path: Path to mzTab file
            
        Returns:
            Dictionary of metadata key-value pairs
        """
        logger.info(f"Extracting metadata from: {file_path}")
        
        metadata = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or not line.startswith('MTD'):
                    continue
                
                # MTD lines format: MTD	key	value
                fields = line.split('\t')
                if len(fields) >= 3:
                    key = fields[1]
                    value = fields[2] if len(fields) == 3 else '\t'.join(fields[2:])
                    metadata[key] = value
        
        logger.info(f"Extracted {len(metadata)} metadata fields")
        return metadata
    
    def parse_tabular(self, file_path: str, delimiter: Optional[str] = None) -> pd.DataFrame:
        """
        Parse CSV/TSV file.
        
        Args:
            file_path: Path to file
            delimiter: Column delimiter (auto-detected if None)
            
        Returns:
            DataFrame with proteomics data
        """
        logger.info(f"Parsing tabular file: {file_path}")
        
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Auto-detect delimiter if not specified
        if delimiter is None:
            suffix = path.suffix.lower()
            if suffix == '.csv':
                delimiter = ','
            elif suffix in ['.tsv', '.txt']:
                delimiter = '\t'
            else:
                # Try to detect from first line
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline()
                    if '\t' in first_line:
                        delimiter = '\t'
                    else:
                        delimiter = ','
        
        logger.info(f"Using delimiter: {repr(delimiter)}")
        
        # Read file with pandas
        df = pd.read_csv(file_path, delimiter=delimiter)
        logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        
        return df
    
    def parse_excel(self, file_path: str, sheet_name: str = 0) -> pd.DataFrame:
        """
        Parse Excel file.
        
        Args:
            file_path: Path to Excel file
            sheet_name: Sheet name or index
            
        Returns:
            DataFrame with proteomics data
        """
        # TODO: Implement Excel parsing
        logger.info(f"Parsing Excel file: {file_path}")
        raise NotImplementedError("Excel parsing not yet implemented")
