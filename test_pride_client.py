"""
Quick test script for PRIDEClient implementation
"""
from src.data_acquisition.pride_api import PRIDEClient
from src.utils.logger import setup_logger

# Set up logging
logger = setup_logger("test_pride", log_file="outputs/logs/test_pride.log")

# Initialize client
client = PRIDEClient()

# Test 1: Get metadata for a known dataset
print("\n=== Test 1: Get Dataset Metadata ===")
try:
    metadata = client.get_dataset_metadata("PXD000001")
    print(f"✓ Dataset: {metadata['title']}")
    print(f"✓ Accession: {metadata['accession']}")
    print(f"✓ Submission Date: {metadata['submissionDate']}")
    print(f"✓ Organisms: {[org['name'] for org in metadata.get('organisms', [])]}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 2: List files for a dataset
print("\n=== Test 2: List Dataset Files ===")
try:
    files = client.get_dataset_files("PXD000001")
    print(f"✓ Found {len(files)} files")
    for i, file in enumerate(files[:3], 1):
        size_mb = file['fileSizeBytes'] / (1024 * 1024)
        print(f"  {i}. {file['fileName']} ({size_mb:.2f} MB) - {file['fileCategory']}")
    if len(files) > 3:
        print(f"  ... and {len(files) - 3} more files")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 3: Search for datasets
print("\n=== Test 3: Search Datasets ===")
try:
    results = client.search_datasets("cancer", page_size=5)
    print(f"✓ Found {len(results)} datasets")
    for i, dataset in enumerate(results, 1):
        print(f"  {i}. {dataset['accession']}: {dataset['title'][:60]}...")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n=== All Tests Complete ===")
