"""
Run Full Pipeline Script

Executes the complete proteomics analysis pipeline.

Usage:
    python scripts/run_full_pipeline.py --dataset-id PXD005011 --control ctrl1,ctrl2 --treatment trt1,trt2
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import setup_logger, load_config


def main():
    """Main entry point for full pipeline execution."""
    parser = argparse.ArgumentParser(
        description="Run complete proteomics analysis pipeline"
    )
    parser.add_argument(
        "--dataset-id",
        required=True,
        help="PRIDE dataset accession (e.g., PXD005011)"
    )
    parser.add_argument(
        "--control",
        required=True,
        help="Control sample names (comma-separated)"
    )
    parser.add_argument(
        "--treatment",
        required=True,
        help="Treatment sample names (comma-separated)"
    )
    parser.add_argument(
        "--config",
        default="config/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip download step (use existing data)"
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
        log_file=f"outputs/logs/{args.dataset_id}_pipeline.log"
    )
    
    # Load configuration
    config = load_config(args.config)
    
    # Parse sample groups
    control_samples = [s.strip() for s in args.control.split(',')]
    treatment_samples = [s.strip() for s in args.treatment.split(',')]
    
    logger.info(f"Starting pipeline for dataset: {args.dataset_id}")
    logger.info(f"Control samples: {control_samples}")
    logger.info(f"Treatment samples: {treatment_samples}")
    
    try:
        # TODO: Implement pipeline steps
        # 1. Download data (if not skipped)
        # 2. Parse files
        # 3. Quality control
        # 4. Data processing
        # 5. Differential expression analysis
        # 6. Generate visualizations
        # 7. Create report
        
        print("\n" + "="*60)
        print("PROTEOMICS ANALYSIS PIPELINE")
        print("="*60)
        print(f"\nDataset: {args.dataset_id}")
        print(f"Control: {', '.join(control_samples)}")
        print(f"Treatment: {', '.join(treatment_samples)}")
        print("\n" + "-"*60)
        
        print("\n⚠️  Pipeline implementation in progress...")
        print("Individual modules need to be implemented first.")
        print("\nNext steps:")
        print("1. Implement data acquisition module")
        print("2. Implement data processing module")
        print("3. Implement analysis module")
        print("4. Connect modules in this script")
        
        logger.info("Pipeline execution completed")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        print(f"\n❌ Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
