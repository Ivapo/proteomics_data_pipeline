"""
Test Module for File Parser

Unit tests for proteomics file parsing functionality.
"""

import pytest
import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from data_acquisition.file_parser import FileParser


class TestFileParser:
    """Tests for proteomics file parser."""
    
    def test_parser_initialization(self):
        """Test that parser initializes correctly."""
        parser = FileParser()
        assert parser is not None
    
    def test_parse_mztab(self, tmp_path):
        """Test parsing mzTab format file."""
        # Create a minimal mzTab file
        mztab_content = """MTD	mzTab-version	1.0.0
MTD	mzTab-mode	Summary
MTD	description	Test mzTab file
PRH	accession	description	protein_coverage	protein_abundance_study_variable[1]	protein_abundance_study_variable[2]
PRT	P12345	Test protein 1	0.45	1234.56	2345.67
PRT	P67890	Test protein 2	0.78	3456.78	4567.89
PRT	Q11111	Test protein 3	0.23	5678.90	6789.01
"""
        # Write to temporary file
        mztab_file = tmp_path / "test.mztab"
        mztab_file.write_text(mztab_content)
        
        # Parse file
        parser = FileParser()
        df = parser.parse_mztab(str(mztab_file))
        
        # Verify DataFrame
        assert df is not None
        assert len(df) == 3
        assert "accession" in df.columns
        assert "description" in df.columns
        assert df.iloc[0]["accession"] == "P12345"
        assert df.iloc[1]["description"] == "Test protein 2"
    
    def test_parse_mztab_metadata(self, tmp_path):
        """Test extracting metadata from mzTab file."""
        mztab_content = """MTD	mzTab-version	1.0.0
MTD	mzTab-mode	Summary
MTD	title	Proteomics Study
MTD	description	Test dataset
PRH	accession	description
PRT	P12345	Test protein
"""
        mztab_file = tmp_path / "test.mztab"
        mztab_file.write_text(mztab_content)
        
        parser = FileParser()
        metadata = parser.get_mztab_metadata(str(mztab_file))
        
        assert metadata is not None
        assert "mzTab-version" in metadata
        assert metadata["mzTab-version"] == "1.0.0"
        assert metadata["title"] == "Proteomics Study"
    
    def test_parse_csv(self, tmp_path):
        """Test parsing CSV file."""
        csv_content = """Protein,Intensity_Sample1,Intensity_Sample2
P12345,1234.56,2345.67
P67890,3456.78,4567.89
Q11111,5678.90,6789.01
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        
        parser = FileParser()
        df = parser.parse_tabular(str(csv_file))
        
        assert df is not None
        assert len(df) == 3
        assert "Protein" in df.columns
        assert df.iloc[0]["Protein"] == "P12345"
    
    def test_parse_tsv(self, tmp_path):
        """Test parsing TSV file."""
        tsv_content = """Protein\tIntensity_Sample1\tIntensity_Sample2
P12345\t1234.56\t2345.67
P67890\t3456.78\t4567.89
Q11111\t5678.90\t6789.01
"""
        tsv_file = tmp_path / "test.tsv"
        tsv_file.write_text(tsv_content)
        
        parser = FileParser()
        df = parser.parse_tabular(str(tsv_file))
        
        assert df is not None
        assert len(df) == 3
        assert "Protein" in df.columns
        assert df.iloc[0]["Protein"] == "P12345"
    
    def test_auto_detect_file_type(self, tmp_path):
        """Test auto-detection of file format."""
        # Test CSV
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("A,B,C\n1,2,3\n")
        
        parser = FileParser()
        df = parser.parse_file(str(csv_file))
        assert df is not None
        assert len(df) == 1
        
        # Test mzTab
        mztab_file = tmp_path / "data.mztab"
        mztab_file.write_text("PRH\taccession\nPRT\tP12345\n")
        df = parser.parse_file(str(mztab_file))
        assert df is not None
    
    def test_invalid_file(self):
        """Test handling of non-existent file."""
        parser = FileParser()
        
        with pytest.raises(FileNotFoundError):
            parser.parse_mztab("/nonexistent/file.mztab")
        
        with pytest.raises(FileNotFoundError):
            parser.parse_tabular("/nonexistent/file.csv")
    
    def test_empty_mztab(self, tmp_path):
        """Test handling of mzTab without protein data."""
        # Only metadata, no protein section
        mztab_content = """MTD	mzTab-version	1.0.0
MTD	title	Empty dataset
"""
        mztab_file = tmp_path / "empty.mztab"
        mztab_file.write_text(mztab_content)
        
        parser = FileParser()
        df = parser.parse_mztab(str(mztab_file))
        
        # Should return empty DataFrame
        assert df is not None
        assert len(df) == 0
