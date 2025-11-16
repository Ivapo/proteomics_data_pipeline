# Proteomics Data Pipeline

A modular, reproducible pipeline for proteomics data analysis using the PRIDE repository as a data source. This project focuses on differential protein expression analysis with a learning-oriented approach.

## Project Overview

This pipeline enables:
- **Data Acquisition**: Download proteomics datasets from PRIDE repository
- **Quality Control**: Assess data quality and identify issues
- **Data Processing**: Clean, normalize, and transform proteomics data
- **Statistical Analysis**: Perform differential expression analysis
- **Visualization**: Generate volcano plots, heatmaps, and PCA plots
- **Reporting**: Create comprehensive HTML reports

## 🏗️ Architecture

The project follows a **modular architecture** with six core modules:

```
src/
├── data_acquisition/    # PRIDE API client and data download
├── data_processing/     # Data cleaning and normalization
├── quality_control/     # QC metrics and validation
├── analysis/           # Statistical analysis (DE, enrichment)
├── visualization/      # Plotting and figure generation
└── reporting/          # Report generation
```

## Quick Start

### Prerequisites

- Python 3.10+
- UV package manager (recommended) or pip
- Docker (optional, for containerized execution)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd proteomics_data_pipeline
   ```

2. **Set up environment with UV** (recommended)
   ```bash
   # Install UV if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Create virtual environment and install dependencies
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   uv pip install -r requirements-dev.txt  # For development
   ```

3. **Or use pip**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Running the Pipeline

**Option 1: Using Snakemake** (Recommended)
```bash
# Run entire pipeline
snakemake --cores 4

# Run specific step
snakemake analyze --cores 1

# Dry run to see what will execute
snakemake -n
```

**Option 2: Using Python scripts**
```bash
# Download a dataset
python scripts/download_dataset.py --dataset-id PXD005011

# Run full pipeline
python scripts/run_full_pipeline.py --dataset-id PXD005011
```

**Option 3: Using Docker**
```bash
# Build the image
docker build -t proteomics-pipeline .

# Run the pipeline
docker run -v $(pwd)/data:/app/data -v $(pwd)/outputs:/app/outputs \
    proteomics-pipeline python scripts/run_full_pipeline.py --dataset-id PXD005011
```

## 📁 Project Structure

```
proteomics_data_pipeline/
├── config/              # Configuration files
├── data/               # Data directory (gitignored)
│   ├── raw/           # Raw PRIDE downloads
│   ├── processed/     # Processed data
│   ├── results/       # Analysis results
│   └── cache/         # Cached API responses
├── docs/              # Documentation
│   ├── development/   # Developer docs (roadmap, decisions, learning log)
│   ├── user_guide/    # User documentation
│   └── resources/     # Reference materials
├── notebooks/         # Jupyter notebooks for exploration
├── outputs/           # Generated outputs
│   ├── figures/       # Plots and visualizations
│   ├── reports/       # HTML/PDF reports
│   └── logs/          # Execution logs
├── scripts/           # Executable scripts
├── src/               # Source code (modular)
└── tests/             # Unit tests
```

## 📊 Example Workflow

1. **Download dataset from PRIDE**
   ```python
   from src.data_acquisition.pride_api import PRIDEClient
   
   client = PRIDEClient()
   dataset = client.download_dataset("PXD005011")
   ```

2. **Process and normalize data**
   ```python
   from src.data_processing.normalizer import Normalizer
   
   normalizer = Normalizer(method="median", log_transform=True)
   normalized_data = normalizer.normalize(raw_data)
   ```

3. **Run differential expression analysis**
   ```python
   from src.analysis.differential_expression import DifferentialExpression
   
   de = DifferentialExpression(alpha=0.05, log2fc_threshold=1.0)
   results = de.analyze(normalized_data, groups=["control", "treatment"])
   ```

4. **Visualize results**
   ```python
   from src.visualization.volcano_plot import create_volcano_plot
   
   create_volcano_plot(results, output="outputs/figures/volcano.png")
   ```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test module
pytest tests/test_data_acquisition/
```

## Documentation

- **[Project Roadmap](docs/development/PROJECT_ROADMAP.md)**: Epics and task tracking
- **[Learning Log](docs/development/LEARNING_LOG.md)**: Learning notes and theory
- **[Architecture Decisions](docs/development/DECISIONS.md)**: Why we made certain choices
- **[User Guide](docs/user_guide/)**: Detailed usage instructions

## Technology Stack

- **Python 3.11**: Core language
- **Pandas/NumPy**: Data manipulation
- **Matplotlib/Seaborn/Plotly**: Visualization
- **Snakemake**: Workflow orchestration
- **Docker**: Containerization
- **UV**: Package management
- **Pytest**: Testing framework

## Contributing

This is a learning project, but contributions are welcome! See development documentation for guidelines.

## License

MIT License - See LICENSE file for details

## Resources

- [PRIDE Database](https://www.ebi.ac.uk/pride/)
- [ProteomeXchange Consortium](https://www.proteomexchange.org/)
- [Snakemake Documentation](https://snakemake.readthedocs.io/)

## Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This is a learning-focused project designed to teach proteomics data analysis and bioinformatics pipeline development.
