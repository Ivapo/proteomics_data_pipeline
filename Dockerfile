# Proteomics Data Pipeline Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy dependency files
COPY requirements.txt requirements-dev.txt pyproject.toml ./

# Install Python dependencies
RUN uv pip install --system -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p data/raw data/processed data/results data/cache \
    outputs/figures outputs/reports outputs/logs

# Set Python path
ENV PYTHONPATH=/app/src:${PYTHONPATH}

# Default command
CMD ["python", "scripts/run_full_pipeline.py", "--help"]
