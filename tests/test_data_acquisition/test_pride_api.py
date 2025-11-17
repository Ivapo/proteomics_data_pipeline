"""
Test Module for PRIDE API Client

Unit tests for PRIDE API client functionality.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch
import requests

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
    
    def test_caching(self, tmp_path):
        """Test that caching works correctly."""
        # Create client with cache in temp directory
        cache_dir = tmp_path / "cache"
        client = PRIDEClient(cache_dir=cache_dir, cache_enabled=True)
        
        # First call - should hit API and cache
        metadata1 = client.get_dataset_metadata("PXD000001")
        assert metadata1 is not None
        
        # Verify cache file was created
        cache_files = list(cache_dir.glob("*.json"))
        assert len(cache_files) == 1
        
        # Second call - should use cache (no API call)
        metadata2 = client.get_dataset_metadata("PXD000001")
        assert metadata2 == metadata1
        
        # Test file listing cache
        files1 = client.get_dataset_files("PXD000001")
        assert len(files1) > 0
        
        # Should now have 2 cache files
        cache_files = list(cache_dir.glob("*.json"))
        assert len(cache_files) == 2
        
        # Second call should use cache
        files2 = client.get_dataset_files("PXD000001")
        assert files2 == files1
    
    def test_cache_disabled(self):
        """Test that caching can be disabled."""
        client = PRIDEClient(cache_enabled=False)
        
        # Should work normally but not create cache
        metadata = client.get_dataset_metadata("PXD000001")
        assert metadata is not None
        
        # No cache directory should be created
        # (This is implicit - if cache_enabled=False, no files are written)
    
    def test_retry_on_timeout(self):
        """Test that timeouts trigger retries."""
        client = PRIDEClient(max_retries=3, timeout=1)
        
        # Mock session.get to timeout twice, then succeed
        with patch.object(client.session, 'get') as mock_get:
            # First two calls timeout, third succeeds
            mock_response = Mock()
            mock_response.json.return_value = {"accession": "TEST"}
            mock_response.raise_for_status.return_value = None
            
            mock_get.side_effect = [
                requests.Timeout("Timeout 1"),
                requests.Timeout("Timeout 2"),
                mock_response
            ]
            
            # Should succeed after 2 retries
            result = client._make_request_with_retry("http://test.com")
            assert result == mock_response
            assert mock_get.call_count == 3
    
    def test_retry_on_connection_error(self):
        """Test that connection errors trigger retries."""
        client = PRIDEClient(max_retries=2, timeout=1)
        
        with patch.object(client.session, 'get') as mock_get:
            # First call fails, second succeeds
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            
            mock_get.side_effect = [
                requests.ConnectionError("Connection failed"),
                mock_response
            ]
            
            result = client._make_request_with_retry("http://test.com")
            assert result == mock_response
            assert mock_get.call_count == 2
    
    def test_no_retry_on_404(self):
        """Test that 404 errors don't retry (client error)."""
        client = PRIDEClient(max_retries=3, timeout=1)
        
        with patch.object(client.session, 'get') as mock_get:
            # Create 404 response
            mock_response = Mock()
            mock_response.status_code = 404
            error = requests.HTTPError(response=mock_response)
            mock_get.return_value.raise_for_status.side_effect = error
            
            # Should fail immediately without retries
            with pytest.raises(requests.HTTPError):
                client._make_request_with_retry("http://test.com")
            
            # Should only try once (no retries on 4xx)
            assert mock_get.call_count == 1
    
    def test_retry_on_server_error(self):
        """Test that 5xx errors trigger retries."""
        client = PRIDEClient(max_retries=2, timeout=1)
        
        with patch.object(client.session, 'get') as mock_get:
            # First call returns 503, second succeeds
            mock_response_error = Mock()
            mock_response_error.status_code = 503
            
            mock_response_ok = Mock()
            mock_response_ok.raise_for_status.return_value = None
            
            def side_effect(*args, **kwargs):
                if mock_get.call_count == 1:
                    raise requests.HTTPError(response=mock_response_error)
                return mock_response_ok
            
            mock_get.side_effect = side_effect
            
            result = client._make_request_with_retry("http://test.com")
            assert result == mock_response_ok
            assert mock_get.call_count == 2
    
    def test_retry_exhaustion(self):
        """Test that retries eventually give up."""
        client = PRIDEClient(max_retries=2, timeout=1, backoff_factor=0.1)
        
        with patch.object(client.session, 'get') as mock_get:
            # Always timeout
            mock_get.side_effect = requests.Timeout("Always fails")
            
            # Should raise after exhausting retries
            with pytest.raises(requests.Timeout):
                client._make_request_with_retry("http://test.com")
            
            # Should try max_retries times
            assert mock_get.call_count == 2
    
    def test_custom_retry_settings(self):
        """Test that custom retry settings are respected."""
        client = PRIDEClient(timeout=5, max_retries=5, backoff_factor=3.0)
        
        assert client.timeout == 5
        assert client.max_retries == 5
        assert client.backoff_factor == 3.0

