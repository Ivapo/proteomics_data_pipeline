# Getting Started

Welcome to the Proteomics Data Pipeline project! This guide will help you get started.

## What Was Just Created

Your project now has:

### Complete Folder Structure
- `src/` - 6 modular Python packages (data_acquisition, processing, analysis, etc.)
- `data/` - Directories for raw, processed, and results data
- `docs/` - Comprehensive documentation including roadmap and learning log
- `config/` - Configuration files
- `scripts/` - Executable Python scripts
- `tests/` - Unit test framework
- `outputs/` - For figures, reports, and logs

### Key Documentation Files
- `README.md` - Project overview
- `docs/development/PROJECT_ROADMAP.md` - **Track your progress here!**
- `docs/development/LEARNING_LOG.md` - **Document what you learn!**
- `docs/development/DECISIONS.md` - Architecture decisions explained
- `docs/user_guide/installation.md` - Installation instructions
- `docs/resources/proteomics_primer.md` - Learn proteomics basics

### Configuration Files
- `pyproject.toml` - Project metadata and dependencies
- `requirements.txt` - Python dependencies
- `Dockerfile` - For containerization
- `Snakefile` - Workflow orchestration
- `config/config.yaml` - Pipeline configuration
- `.gitignore` - Git ignore rules

## Next Steps

### 1. Install UV Package Manager

Open a PowerShell terminal and run:

```powershell
# Install UV package manager
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Install Dependencies

```powershell
# Create virtual environment
uv venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
```

### 3. Initialize Git Repository

```powershell
git init
git add .
git commit -m "Initial project structure"
```

### 4. Review the Project Roadmap

Open `docs/development/PROJECT_ROADMAP.md` to see:
- 9 major epics (project phases)
- ~70 individual tasks
- Clear learning progression

### 5. Start Learning & Building

#### Option A: Follow the Roadmap
Start with **Epic 2: Data Acquisition Module**
- Read about PRIDE API
- Implement the PRIDEClient class
- Document learnings in `LEARNING_LOG.md`

#### Option B: Explore with Jupyter
```powershell
# Create a notebook
jupyter notebook
```

Create a notebook in `notebooks/` to experiment with:
- Pandas DataFrames
- Making HTTP requests
- Basic data visualization

## Important Files to Know

### For Tracking Progress
- `docs/development/PROJECT_ROADMAP.md` - Your task tracker
- `docs/development/LEARNING_LOG.md` - Your learning journal

### For Configuration
- `config/config.yaml` - Change analysis parameters here

### For Running Code
- `scripts/download_dataset.py` - Download PRIDE datasets
- `scripts/run_full_pipeline.py` - Run full analysis
- `Snakefile` - Workflow definition

### For Documentation
- `docs/user_guide/` - User documentation
- `docs/resources/` - Learning resources

## Verify Installation

Test that everything is set up correctly:

```powershell
# Run basic tests
pytest tests/test_utils.py -v

# Check imports work
python -c "from src.utils import setup_logger; print('Imports working!')"
```

## Learning Path Suggestion

### Week 1-2: Data Acquisition
1. Learn about PRIDE API and REST APIs
2. Implement `PRIDEClient` class
3. Add file download functionality
4. Write tests

### Week 3-4: Data Processing
1. Learn about pandas DataFrames
2. Implement data cleaning
3. Add normalization methods
4. Practice with real datasets

### Week 5-6: Analysis
1. Learn statistics basics (t-tests, p-values)
2. Implement differential expression
3. Understand multiple testing correction

### Week 7-8: Visualization & Reporting
1. Create volcano plots
2. Generate heatmaps
3. Build HTML reports

## Tips

1. **Document as You Go**: Update `LEARNING_LOG.md` after each task
2. **Test Everything**: Write tests before marking tasks complete
3. **Use Notebooks**: Jupyter notebooks are great for experimentation
4. **Ask Questions**: Add questions to `docs/development/QUESTIONS.md`
5. **Commit Often**: Small, frequent commits are better than big ones

## Need Help?

- Check `docs/resources/useful_links.md` for learning resources
- Review `docs/resources/proteomics_primer.md` for domain knowledge
- Look at the `tests/` directory for code examples

## Current Status

- Project structure created  
- Documentation framework in place  
- Configuration files ready  
- Ready to start Epic 2: Data Acquisition Module  

**You're all set! Start coding and learning!**

---

**Remember**: This is a learning project. The goal isn't just to build a pipeline, but to understand:
- How to structure Python projects
- How to work with APIs
- How to process scientific data
- How to apply statistical methods
- How to create reproducible analyses

Good luck!
