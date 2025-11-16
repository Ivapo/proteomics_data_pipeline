"""
Download Dataset Script

Downloads a proteomics dataset from PRIDE repository.

Usage:
    python scripts/download_dataset.py --dataset-id PXD005011
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_acquisition import PRIDEClient, DatasetDownloader
from utils import setup_logger


def main():
    """Main entry point for dataset download script."""
    parser = argparse.ArgumentParser(
        description="Download proteomics dataset from PRIDE"
    )
    parser.add_argument(
        "--dataset-id",
        required=True,
        help="PRIDE dataset accession (e.g., PXD005011)"
    )
    parser.add_argument(
        "--output-dir",
        default="data/raw",
        help="Output directory for downloaded files"
    )
    parser.add_argument(
        "--file-types",
        nargs="+",
        help="File types to download (e.g., mzTab csv)"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger(
        level=args.log_level,
        log_file=f"outputs/logs/{args.dataset_id}_download.log"
    )
    
    logger.info(f"Starting download for dataset: {args.dataset_id}")
    
    try:
        # Initialize downloader
        downloader = DatasetDownloader(output_dir=args.output_dir)
        
        # Download dataset
        output_path = downloader.download_dataset(
            dataset_id=args.dataset_id,
            file_types=args.file_types
        )
        
        logger.info(f"Download completed successfully: {output_path}")
        print(f"\n✅ Dataset {args.dataset_id} downloaded to: {output_path}")
        
    except Exception as e:
        logger.error(f"Download failed: {e}", exc_info=True)
        print(f"\n❌ Download failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
