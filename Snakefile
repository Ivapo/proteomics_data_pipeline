# Proteomics Data Pipeline - Snakemake Workflow
# Main workflow orchestration file

import os
from pathlib import Path

# Configuration
configfile: "config/config.yaml"

# Global variables
DATASET_ID = config.get("dataset_id", "PXD005011")
OUTPUT_DIR = Path("outputs")
DATA_DIR = Path("data")

# Default target - runs the entire pipeline
rule all:
    input:
        f"{OUTPUT_DIR}/reports/{DATASET_ID}_final_report.html",
        f"{OUTPUT_DIR}/figures/{DATASET_ID}_volcano_plot.png",
        f"{OUTPUT_DIR}/figures/{DATASET_ID}_heatmap.png"

# Rule 1: Download dataset from PRIDE
rule download_data:
    output:
        raw_data = f"{DATA_DIR}/raw/{{dataset_id}}.mzTab"
    params:
        dataset_id = "{dataset_id}"
    log:
        f"{OUTPUT_DIR}/logs/{{dataset_id}}_download.log"
    shell:
        """
        python scripts/download_dataset.py \
            --dataset-id {params.dataset_id} \
            --output {output.raw_data} \
            > {log} 2>&1
        """

# Rule 2: Quality control checks
rule quality_control:
    input:
        raw_data = f"{DATA_DIR}/raw/{{dataset_id}}.mzTab"
    output:
        qc_report = f"{OUTPUT_DIR}/reports/{{dataset_id}}_qc_report.json",
        qc_plots = f"{OUTPUT_DIR}/figures/{{dataset_id}}_qc_plots.png"
    log:
        f"{OUTPUT_DIR}/logs/{{dataset_id}}_qc.log"
    script:
        "src/quality_control/qc_metrics.py"

# Rule 3: Data processing (cleaning and normalization)
rule process_data:
    input:
        raw_data = f"{DATA_DIR}/raw/{{dataset_id}}.mzTab",
        qc_report = f"{OUTPUT_DIR}/reports/{{dataset_id}}_qc_report.json"
    output:
        processed_data = f"{DATA_DIR}/processed/{{dataset_id}}_normalized.csv"
    log:
        f"{OUTPUT_DIR}/logs/{{dataset_id}}_processing.log"
    script:
        "src/data_processing/normalizer.py"

# Rule 4: Differential expression analysis
rule analyze:
    input:
        processed_data = f"{DATA_DIR}/processed/{{dataset_id}}_normalized.csv"
    output:
        results = f"{DATA_DIR}/results/{{dataset_id}}_de_results.csv"
    params:
        alpha = config.get("alpha", 0.05),
        log2fc_threshold = config.get("log2fc_threshold", 1.0)
    log:
        f"{OUTPUT_DIR}/logs/{{dataset_id}}_analysis.log"
    script:
        "src/analysis/differential_expression.py"

# Rule 5: Generate visualizations
rule visualize:
    input:
        results = f"{DATA_DIR}/results/{{dataset_id}}_de_results.csv"
    output:
        volcano_plot = f"{OUTPUT_DIR}/figures/{{dataset_id}}_volcano_plot.png",
        heatmap = f"{OUTPUT_DIR}/figures/{{dataset_id}}_heatmap.png"
    log:
        f"{OUTPUT_DIR}/logs/{{dataset_id}}_visualization.log"
    script:
        "src/visualization/volcano_plot.py"

# Rule 6: Generate final report
rule report:
    input:
        results = f"{DATA_DIR}/results/{{dataset_id}}_de_results.csv",
        qc_report = f"{OUTPUT_DIR}/reports/{{dataset_id}}_qc_report.json",
        figures = [
            f"{OUTPUT_DIR}/figures/{{dataset_id}}_volcano_plot.png",
            f"{OUTPUT_DIR}/figures/{{dataset_id}}_heatmap.png"
        ]
    output:
        report = f"{OUTPUT_DIR}/reports/{{dataset_id}}_final_report.html"
    log:
        f"{OUTPUT_DIR}/logs/{{dataset_id}}_report.log"
    script:
        "src/reporting/html_reporter.py"

# Clean intermediate files
rule clean:
    shell:
        """
        rm -rf data/processed/* data/results/* outputs/figures/* outputs/reports/*
        echo "Cleaned intermediate and output files"
        """

# Clean everything including raw data
rule clean_all:
    shell:
        """
        rm -rf data/raw/* data/processed/* data/results/* data/cache/* \
               outputs/figures/* outputs/reports/* outputs/logs/* \
               .snakemake/
        echo "Cleaned all data and outputs"
        """
