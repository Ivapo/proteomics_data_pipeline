"""
Test Module for Data Acquisition

Unit tests for data acquisition module.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from data_acquisition import PRIDEClient


class TestPRIDEClient:
    """Tests for PRIDE API client."""
    
    def test_client_initialization(self):
        """Test that client initializes correctly."""
        client = PRIDEClient()
        assert client.base_url == "https://www.ebi.ac.uk/pride/ws/archive/v2"
        assert client.session is not None
    
    # TODO: Add more tests as functionality is implemented
    # def test_get_dataset_metadata(self):
    # def test_search_datasets(self):
    # def test_download_file(self):
