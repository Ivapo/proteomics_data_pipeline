# Quick Start Guide

This guide will walk you through running your first proteomics analysis.

## Prerequisites

Make sure you've completed the [installation](installation.md) steps.

## Running Your First Analysis

### Step 1: Download a Dataset

```bash
uv run python scripts/download_dataset.py --dataset-id PXD005011
```

This will download a sample dataset from PRIDE into `data/raw/`.

### Step 2: Run the Pipeline with Snakemake

```bash
# Dry run to see what will execute
uv run snakemake -n

# Run the full pipeline
uv run snakemake --cores 4
```

### Step 3: View Results

Results will be saved in:
- **Figures**: `outputs/figures/`
- **Reports**: `outputs/reports/`
- **Processed data**: `data/processed/`

## Using Python Scripts

Alternatively, you can run the pipeline using Python scripts:

```bash
uv run python scripts/run_full_pipeline.py \
    --dataset-id PXD005011 \
    --control sample1,sample2 \
    --treatment sample3,sample4
```

## Configuration

Edit `config/config.yaml` to customize:
- Analysis parameters (alpha, fold-change thresholds)
- Normalization methods
- Visualization settings

## Example Configuration

```yaml
analysis:
  alpha: 0.05
  log2fc_threshold: 1.0
  
visualization:
  dpi: 300
  figure_format: "png"
```

## Next Steps

- Explore Jupyter notebooks in `notebooks/`
- Read the [full documentation](../README.md)
- Check the [Project Roadmap](../development/PROJECT_ROADMAP.md) for upcoming features
