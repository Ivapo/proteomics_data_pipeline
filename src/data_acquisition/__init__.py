"""
Data Acquisition Module

Handles downloading and parsing proteomics data from PRIDE repository.
"""

from .pride_api import PRIDEClient
from .dataset_downloader import DatasetDownloader
from .file_parser import FileParser

__all__ = ["PRIDEClient", "DatasetDownloader", "FileParser"]
