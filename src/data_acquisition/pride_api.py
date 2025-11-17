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
import json
import hashlib
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)


class PRIDEClient:
    """
    Client for interacting with PRIDE Archive REST API.
    
    The PRIDE Archive is the world's largest data repository of mass 
    spectrometry-based proteomics data.
    
    API Documentation: https://www.ebi.ac.uk/pride/ws/archive/v2
    """
    
    def __init__(self, base_url: str = "https://www.ebi.ac.uk/pride/ws/archive/v2",
                 cache_dir: Optional[Path] = None,
                 cache_enabled: bool = True,
                 cache_max_age_hours: int = 24,
                 timeout: int = 30,
                 max_retries: int = 3,
                 backoff_factor: float = 2.0):
        """
        Initialize PRIDE API client.
        
        Args:
            base_url: Base URL for PRIDE API (default: production API)
            cache_dir: Directory for caching API responses (default: data/cache)
            cache_enabled: Enable/disable caching (default: True)
            cache_max_age_hours: Maximum age of cache in hours (default: 24)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retry attempts (default: 3)
            backoff_factor: Exponential backoff multiplier (default: 2.0)
        """
        self.base_url = base_url
        self.cache_enabled = cache_enabled
        self.cache_max_age = timedelta(hours=cache_max_age_hours)
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        
        # Set up cache directory
        if cache_dir is None:
            self.cache_dir = Path("data/cache")
        else:
            self.cache_dir = Path(cache_dir)
        
        if self.cache_enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Cache enabled: {self.cache_dir} (max age: {cache_max_age_hours}h)")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "ProteomicsPipeline/0.1.0"
        })
        logger.info(f"Initialized PRIDE client with base URL: {base_url}")
    
    def _get_cache_key(self, endpoint: str, **params) -> str:
        """Generate a unique cache key for a request."""
        # Create a string from endpoint and params
        cache_str = f"{endpoint}_{json.dumps(params, sort_keys=True)}"
        # Hash it to create a valid filename
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict]:
        """Retrieve data from cache if valid."""
        if not self.cache_enabled:
            return None
        
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if not cache_file.exists():
            logger.debug(f"Cache miss: {cache_key}")
            return None
        
        # Check if cache is stale
        file_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        if file_age > self.cache_max_age:
            logger.debug(f"Cache expired: {cache_key} (age: {file_age})")
            return None
        
        # Load from cache
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
            logger.info(f"Cache hit: {cache_key} (age: {file_age})")
            return data
        except Exception as e:
            logger.warning(f"Failed to load cache {cache_key}: {e}")
            return None
    
    def _save_to_cache(self, cache_key: str, data: Dict) -> None:
        """Save data to cache."""
        if not self.cache_enabled:
            return
        
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug(f"Saved to cache: {cache_key}")
        except Exception as e:
            logger.warning(f"Failed to save cache {cache_key}: {e}")
    
    def _make_request_with_retry(self, url: str, params: Optional[Dict] = None) -> requests.Response:
        """
        Make HTTP request with exponential backoff retry logic.
        
        Retries on:
        - Timeouts
        - Connection errors
        - Server errors (5xx)
        
        Does NOT retry on:
        - Client errors (4xx) - indicates bad request, won't succeed on retry
        
        Args:
            url: URL to request
            params: Optional query parameters
            
        Returns:
            Response object
            
        Raises:
            requests.RequestException: If all retries exhausted
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                return response
                
            except requests.Timeout as e:
                last_exception = e
                logger.warning(f"Request timeout (attempt {attempt + 1}/{self.max_retries}): {url}")
                
            except requests.ConnectionError as e:
                last_exception = e
                logger.warning(f"Connection error (attempt {attempt + 1}/{self.max_retries}): {url}")
                
            except requests.HTTPError as e:
                # Don't retry client errors (4xx)
                if e.response.status_code < 500:
                    raise
                # Retry server errors (5xx)
                last_exception = e
                logger.warning(f"Server error {e.response.status_code} (attempt {attempt + 1}/{self.max_retries}): {url}")
            
            # If not last attempt, wait with exponential backoff
            if attempt < self.max_retries - 1:
                wait_time = self.backoff_factor ** attempt
                logger.info(f"Retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
        
        # All retries exhausted
        logger.error(f"All {self.max_retries} retry attempts failed for {url}")
        raise last_exception
    
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
        
        # Check cache first
        cache_key = self._get_cache_key("metadata", dataset_id=dataset_id)
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            return cached_data
        
        url = f"{self.base_url}/projects/{dataset_id}"
        
        try:
            response = self._make_request_with_retry(url)
            
            metadata = response.json()
            logger.info(f"Successfully retrieved metadata for {dataset_id}")
            
            # Save to cache
            self._save_to_cache(cache_key, metadata)
            
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
            response = self._make_request_with_retry(url, params=params)
            
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
        
        # Check cache first
        cache_key = self._get_cache_key("files", dataset_id=dataset_id)
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            return cached_data
        
        # Use v3 API for files endpoint
        url = f"{self.base_url.replace('v2', 'v3')}/projects/{dataset_id}/files"
        
        try:
            response = self._make_request_with_retry(url)
            
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
            
            # Save to cache
            self._save_to_cache(cache_key, file_list)
            
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
