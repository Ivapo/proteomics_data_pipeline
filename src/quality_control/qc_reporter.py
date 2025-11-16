"""
QC Reporter

Generates quality control reports.
"""

import json
import logging
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)


class QCReporter:
    """
    Generates QC reports in various formats.
    """
    
    def __init__(self, output_dir: str = "outputs/reports"):
        """
        Initialize QC reporter.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized QC reporter with output dir: {output_dir}")
    
    def generate_report(self, metrics: Dict, dataset_id: str) -> Path:
        """
        Generate QC report.
        
        Args:
            metrics: Dictionary of QC metrics
            dataset_id: Dataset identifier
            
        Returns:
            Path to generated report
        """
        logger.info(f"Generating QC report for dataset: {dataset_id}")
        
        # Save as JSON
        report_path = self.output_dir / f"{dataset_id}_qc_report.json"
        
        with open(report_path, 'w') as f:
            json.dump(metrics, f, indent=2, default=str)
        
        logger.info(f"QC report saved to: {report_path}")
        return report_path
