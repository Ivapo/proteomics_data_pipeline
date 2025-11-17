"""
PRIDE API Client

Handles interaction with PRIDE REST API for querying and downloading proteomics datasets.
"""

import requests
from typing import Dict, List, Optional
import logging
from pathlib import Path
from tqdm import tqdm
from urllib.request import urlopen
import urllib.error

logger = logging.getLogger(__name__)


class PRIDEClient:
    """
    Client for interacting with PRIDE Archive REST API.
    
    The PRIDE Archive is the world's largest data repository of mass 
    spectrometry-based proteomics data.
    
    API Documentation: https://www.ebi.ac.uk/pride/ws/archive/v2
    """
    
    def __init__(self, base_url: str = "https://www.ebi.ac.uk/pride/ws/archive/v2"):
        """
        Initialize PRIDE API client.
        
        Args:
            base_url: Base URL for PRIDE API (default: production API)
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "ProteomicsPipeline/0.1.0"
        })
        logger.info(f"Initialized PRIDE client with base URL: {base_url}")
    
    def get_dataset_metadata(self, dataset_id: str) -> Dict:
        """
        Retrieve metadata for a specific PRIDE dataset.
        
        Args:
            dataset_id: PRIDE dataset accession (e.g., "PXD005011")
            
        Returns:
            Dictionary containing dataset metadata
            
        Raises:
            requests.HTTPError: If dataset not found or API error
        """
        logger.info(f"Fetching metadata for dataset: {dataset_id}")
        
        url = f"{self.base_url}/projects/{dataset_id}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            metadata = response.json()
            logger.info(f"Successfully retrieved metadata for {dataset_id}")
            return metadata
            
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                logger.error(f"Dataset {dataset_id} not found")
                raise ValueError(f"Dataset {dataset_id} not found in PRIDE")
            else:
                logger.error(f"HTTP error retrieving {dataset_id}: {e}")
                raise
        except requests.RequestException as e:
            logger.error(f"Request failed for {dataset_id}: {e}")
            raise
    
    def search_datasets(self, query: str, page_size: int = 10) -> List[Dict]:
        """
        Search for datasets in PRIDE.
        
        Args:
            query: Search query string
            page_size: Number of results per page
            
        Returns:
            List of dataset metadata dictionaries
        """
        logger.info(f"Searching for datasets with query: '{query}'")
        
        url = f"{self.base_url}/search/projects"
        params = {
            "keyword": query,
            "pageSize": page_size,
            "page": 0,
            "sortDirection": "DESC",
            "sortFields": "submissionDate"
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            # Check if API returns list directly or nested structure
            if isinstance(data, list):
                results = data
            else:
                # API returns nested structure with results in '_embedded' field
                results = data.get("_embedded", {}).get("projects", [])
            
            logger.info(f"Found {len(results)} datasets matching '{query}'")
            return results
            
        except requests.RequestException as e:
            logger.error(f"Search failed for query '{query}': {e}")
            raise
    
    def get_dataset_files(self, dataset_id: str) -> List[Dict]:
        """
        Get list of files available for a dataset.
        
        Args:
            dataset_id: PRIDE dataset accession
            
        Returns:
            List of file metadata (name, size, type, download URL)
        """
        logger.info(f"Fetching file list for dataset: {dataset_id}")
        
        # Use v3 API for files endpoint
        url = f"{self.base_url.replace('v2', 'v3')}/projects/{dataset_id}/files"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            files = response.json()
            
            # Extract useful information from each file
            file_list = []
            for file_data in files:
                # Extract FTP URL from publicFileLocations
                ftp_url = None
                for location in file_data.get("publicFileLocations", []):
                    if location.get("name") == "FTP Protocol":
                        ftp_url = location.get("value")
                        break
                
                file_info = {
                    "fileName": file_data.get("fileName"),
                    "fileSizeBytes": file_data.get("fileSizeBytes"),
                    "fileCategory": file_data.get("fileCategory", {}).get("value"),
                    "downloadUrl": ftp_url
                }
                file_list.append(file_info)
            
            logger.info(f"Found {len(file_list)} files for dataset {dataset_id}")
            return file_list
            
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                logger.error(f"Files not found for dataset {dataset_id}")
                raise ValueError(f"No files found for dataset {dataset_id}")
            else:
                logger.error(f"HTTP error retrieving files for {dataset_id}: {e}")
                raise
        except requests.RequestException as e:
            logger.error(f"Request failed for dataset files {dataset_id}: {e}")
            raise
    
    def download_file(self, file_url: str, output_path: str, 
                     chunk_size: int = 8192) -> None:
        """
        Download a file from PRIDE with progress tracking.
        
        Supports both HTTP/HTTPS and FTP protocols.
        
        Args:
            file_url: URL of file to download (HTTP, HTTPS, or FTP)
            output_path: Local path to save file
            chunk_size: Size of chunks for streaming download (default: 8KB)
            
        Raises:
            urllib.error.URLError: If download fails
            requests.RequestException: If HTTP download fails
        """
        logger.info(f"Downloading file from: {file_url}")
        logger.info(f"Saving to: {output_path}")
        
        # Create parent directory if it doesn't exist
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Handle FTP and HTTP/HTTPS differently
            if file_url.startswith('ftp://'):
                self._download_ftp(file_url, output_path, chunk_size)
            else:
                self._download_http(file_url, output_path, chunk_size)
            
            logger.info(f"Successfully downloaded file to {output_path}")
            
        except Exception as e:
            logger.error(f"Download failed for {file_url}: {e}")
            # Clean up partial download
            if output_file.exists():
                output_file.unlink()
                logger.info("Removed partial download")
            raise
    
    def _download_http(self, file_url: str, output_path: str, chunk_size: int) -> None:
        """Download file via HTTP/HTTPS."""
        response = self.session.get(file_url, stream=True)
        response.raise_for_status()
        
        # Get file size for progress bar
        total_size = int(response.headers.get('content-length', 0))
        
        # Download with progress bar
        output_file = Path(output_path)
        with open(output_path, 'wb') as f:
            with tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=output_file.name
            ) as pbar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
    
    def _download_ftp(self, file_url: str, output_path: str, chunk_size: int) -> None:
        """Download file via FTP."""
        output_file = Path(output_path)
        
        with urlopen(file_url) as response:
            # Try to get file size (not all FTP servers support this)
            total_size = int(response.headers.get('Content-Length', 0))
            
            with open(output_path, 'wb') as f:
                with tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=output_file.name,
                    disable=total_size == 0  # Disable if size unknown
                ) as pbar:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        pbar.update(len(chunk))
