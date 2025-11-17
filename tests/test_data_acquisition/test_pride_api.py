"""
Test Module for PRIDE API Client

Unit tests for PRIDE API client functionality.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from data_acquisition.pride_api import PRIDEClient


class TestPRIDEClient:
    """Tests for PRIDE API client."""
    
    def test_client_initialization(self):
        """Test that client initializes correctly."""
        client = PRIDEClient()
        assert client.base_url == "https://www.ebi.ac.uk/pride/ws/archive/v2"
        assert client.session is not None
    
    def test_get_project_metadata(self):
        """Test fetching project metadata for a known dataset."""
        client = PRIDEClient()
        metadata = client.get_dataset_metadata("PXD000001")
        
        assert metadata is not None
        assert metadata["accession"] == "PXD000001"
        assert "title" in metadata
        assert "submitters" in metadata
    
    def test_list_project_files(self):
        """Test listing files for a known project."""
        client = PRIDEClient()
        files = client.get_dataset_files("PXD000001")
        
        assert files is not None
        assert len(files) > 0
        assert "fileName" in files[0]
        assert "fileSizeBytes" in files[0]
    
    def test_search_projects(self):
        """Test searching for projects by keyword."""
        client = PRIDEClient()
        results = client.search_datasets("Erwinia", page_size=5)
        
        assert results is not None
        assert len(results) > 0
        assert "accession" in results[0]
    
    def test_invalid_project(self):
        """Test handling of invalid project accession."""
        client = PRIDEClient()
        
        # Should raise ValueError for non-existent project
        with pytest.raises(ValueError, match="not found"):
            client.get_dataset_metadata("PXD999999999")
    
    def test_download_file(self, tmp_path):
        """Test downloading a small file with progress tracking."""
        client = PRIDEClient()
        
        # Get a small file from PXD000001 for testing
        files = client.get_dataset_files("PXD000001")
        
        # Find a small file (less than 1MB) for quick test
        small_file = None
        for f in files:
            if f["fileSizeBytes"] and f["fileSizeBytes"] < 1_000_000:
                small_file = f
                break
        
        # Skip test if no small files found
        if not small_file or not small_file["downloadUrl"]:
            pytest.skip("No suitable small file found for download test")
        
        # Download to temporary directory
        output_path = tmp_path / small_file["fileName"]
        client.download_file(small_file["downloadUrl"], str(output_path))
        
        # Verify file was downloaded
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        # Note: Compressed files may differ in size from API metadata
        # Just verify file is within reasonable size range (not empty, not huge)
        assert output_path.stat().st_size < 10_000_000  # Less than 10MB

