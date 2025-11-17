# Installation Guide

## Prerequisites

- **Python 3.10 or higher**
- **UV package manager** (recommended) or pip
- **Docker** (optional, for containerized execution)

## Installation Steps

### 1. Install UV Package Manager

UV is a fast Python package manager that we recommend for this project.

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone the Repository

```bash
git clone <repository-url>
cd proteomics_data_pipeline
```

### 3. Create Virtual Environment

**Using UV:**
```bash
uv venv
```

**Using Python:**
```bash
python -m venv venv
```

### 4. Install Dependencies

```bash
uv sync --extra dev
```

### 5. Verify Installation

UV automatically manages the virtual environment - no activation needed!

```bash
uv run python -c "import pandas; import numpy; print('Installation successful!')"
```

**Note:** Use `uv run <command>` to run any command in the virtual environment.

## Docker Installation (Optional)

### Build Docker Image

```bash
docker build -t proteomics-pipeline .
```

### Run with Docker

```bash
docker run -v ${PWD}/data:/app/data -v ${PWD}/outputs:/app/outputs proteomics-pipeline
```

## Next Steps

See [Quick Start Guide](quickstart.md) to run your first analysis.
