# Architecture Decision Records (ADRs)

This document records important architectural and technical decisions made during the project, along with the context and rationale.

---

## ADR-001: Use Modular Pipeline Architecture

**Date**: 2025-11-16

**Status**: Accepted

**Context**:
We needed to decide between a monolithic script-based pipeline vs. a modular architecture with separate components.

**Decision**: 
Use a **modular architecture** with six independent modules:
- data_acquisition
- data_processing  
- quality_control
- analysis
- visualization
- reporting

**Rationale**:
- **Maintainability**: Easier to debug and update individual components
- **Testability**: Each module can be tested independently
- **Reusability**: Modules can be used in different analysis contexts
- **Learning**: Better demonstrates software engineering principles
- **Scalability**: Easy to add new analysis types without major refactoring

**Consequences**:
- ✅ More organized codebase
- ✅ Better separation of concerns
- ✅ Easier to understand and modify
- ⚠️ Slightly more initial setup time
- ⚠️ Need to manage inter-module dependencies

**Alternatives Considered**:
- **Monolithic script**: Simpler initially, but harder to maintain as complexity grows
- **Package-based**: Similar to chosen approach, but more heavyweight

---

## ADR-002: Use Snakemake for Workflow Orchestration

**Date**: 2025-11-16

**Status**: Accepted

**Context**:
Needed a way to manage multi-step pipeline execution, handle dependencies, and enable reproducibility.

**Decision**: 
Use **Snakemake** as the workflow management system.

**Rationale**:
- **Industry Standard**: Widely used in bioinformatics
- **Declarative Syntax**: Define what to create, not how
- **Automatic Parallelization**: Runs independent steps simultaneously
- **Dependency Tracking**: Automatically determines what needs to run
- **Resume Capability**: Can restart from failures without re-running completed steps
- **Scalability**: Works from laptop to HPC clusters
- **Python-based**: Integrates well with our Python codebase

**Consequences**:
- ✅ Professional workflow management
- ✅ Easy to visualize pipeline
- ✅ Automatic re-running when inputs change
- ⚠️ Learning curve for Snakemake syntax
- ⚠️ Additional dependency to manage

**Alternatives Considered**:
- **Nextflow**: More complex, overkill for this project
- **Airflow**: Designed for task scheduling, not bioinformatics pipelines
- **Luigi**: Less popular in bioinformatics community
- **Plain Python scripts**: Harder to manage dependencies and parallelization
- **Make**: Not Python-native, less suited for data pipelines

---

## ADR-003: Use UV for Package Management

**Date**: 2025-11-16

**Status**: Accepted

**Context**:
Needed to choose a Python package manager for dependency management.

**Decision**: 
Use **UV** as the primary package manager (with pip as fallback).

**Rationale**:
- **Speed**: 10-100x faster than pip for resolving dependencies
- **Modern**: Written in Rust, actively developed
- **Lock Files**: Generates lock files for exact reproducibility
- **Compatibility**: Drop-in replacement for pip
- **Virtual Environment Management**: Built-in venv handling
- **Future-proof**: Likely to become standard

**Consequences**:
- ✅ Faster dependency installation
- ✅ Better reproducibility
- ✅ Modern tooling
- ⚠️ Users must install UV (though pip still works)
- ⚠️ Relatively new tool (less mature than pip/poetry)

**Alternatives Considered**:
- **pip**: Standard but slower, no built-in lock files
- **poetry**: Good but slower than UV
- **conda**: Heavy, slower, package availability issues

---

## ADR-004: Use Docker for Environment Reproducibility

**Date**: 2025-11-16

**Status**: Accepted

**Context**:
Scientific reproducibility requires exact environment replication across different machines and operating systems.

**Decision**: 
Provide a **Dockerfile** for containerized execution.

**Rationale**:
- **Perfect Reproducibility**: Exact same environment everywhere
- **System Dependencies**: Handles OS-level dependencies
- **Sharing**: Easy to share with collaborators
- **Scientific Standard**: Expected in computational biology
- **Cross-platform**: Works on Windows, Mac, Linux

**Consequences**:
- ✅ Guaranteed reproducibility
- ✅ Easy deployment
- ✅ Professional standard
- ⚠️ Requires Docker installation
- ⚠️ Slight performance overhead
- ⚠️ Larger learning curve for beginners

**Alternatives Considered**:
- **Virtual environments only**: Less reproducible (doesn't capture system deps)
- **Conda**: Good but slower and less complete than Docker
- **Singularity**: Better for HPC but less common on personal machines

---

## ADR-005: Focus on Differential Expression Analysis

**Date**: 2025-11-16

**Status**: Accepted

**Context**:
Needed to choose an initial analysis type that would be educational and cover fundamental pipeline concepts.

**Decision**: 
Start with **Differential Protein Expression Analysis** (e.g., comparing disease vs. healthy).

**Rationale**:
- **Fundamental**: Core analysis type in proteomics
- **Well-documented**: Many examples and resources available
- **Covers Key Concepts**: Data processing, statistics, visualization
- **Clear Output**: Easy to interpret results (volcano plots, heatmaps)
- **Modular Foundation**: Other analyses can be added later
- **Real-world Application**: Used in actual research

**Consequences**:
- ✅ Learn statistical analysis fundamentals
- ✅ Understand data preprocessing pipeline
- ✅ Generate publication-quality visualizations
- ✅ Foundation for more advanced analyses
- ⚠️ Single analysis type initially (but expandable)

**Alternatives Considered**:
- **Pathway Enrichment**: More complex, better as second analysis
- **PTM Analysis**: More specialized, narrower application
- **Network Analysis**: Very complex, advanced topic
- **Quality Control Only**: Too limited, not a complete analysis

---

## ADR-006: Use PRIDE as Primary Data Source

**Date**: 2025-11-16

**Status**: Accepted

**Context**:
Needed to select a proteomics data repository for acquiring datasets.

**Decision**: 
Use **PRIDE (PRoteomics IDEntifications Database)** as the primary data source.

**Rationale**:
- **Largest Repository**: Most datasets available
- **REST API**: Programmatic access available
- **Well-documented**: Good documentation and examples
- **Part of ProteomeXchange**: Industry standard
- **Active Development**: Regularly updated
- **Free and Open**: No authentication required for public data

**Consequences**:
- ✅ Access to thousands of datasets
- ✅ Learn API interaction
- ✅ Industry-standard approach
- ⚠️ API rate limiting to consider
- ⚠️ Large file downloads

**Alternatives Considered**:
- **MassIVE**: Good but smaller than PRIDE
- **jPOST**: Excellent but fewer datasets
- **Local files only**: Limits learning and scalability

---

## ADR-007: Postpone Streamlit Dashboard to Phase 2

**Date**: 2025-11-16

**Status**: Accepted

**Context**:
Needed to decide whether to build an interactive web interface from the start.

**Decision**: 
Build **core pipeline first**, add **Streamlit dashboard later** (Phase 2).

**Rationale**:
- **Focus on Fundamentals**: Learn data science and pipeline concepts first
- **Complexity Management**: Don't overwhelm with too many technologies at once
- **Core Value**: Pipeline functionality is more important than UI initially
- **Easy to Add Later**: Streamlit can wrap existing functionality
- **Learning Path**: Better to understand the data processing before visualization

**Consequences**:
- ✅ Faster initial development
- ✅ Focus on learning core concepts
- ✅ Clearer learning progression
- ⚠️ No interactive UI initially (use notebooks instead)
- ⚠️ Will need to refactor slightly when adding UI

**Alternatives Considered**:
- **Build UI from start**: Would slow down core development
- **No UI ever**: Limits usability for non-programmers
- **Jupyter only**: Good for exploration but not for sharing

---

## Template for Future ADRs

```markdown
## ADR-XXX: [Decision Title]

**Date**: YYYY-MM-DD

**Status**: Proposed | Accepted | Deprecated | Superseded

**Context**:
What is the issue that we're seeing that is motivating this decision?

**Decision**: 
What is the change that we're proposing and/or doing?

**Rationale**:
Why did we choose this option?
- Reason 1
- Reason 2

**Consequences**:
What becomes easier or more difficult to do because of this change?
- ✅ Positive consequence
- ⚠️ Negative consequence

**Alternatives Considered**:
- Alternative 1: Why not chosen
- Alternative 2: Why not chosen
```

---

## Notes

- ADRs are **immutable** - don't change old decisions, create new ones that supersede them
- Focus on **WHY** not WHAT - code shows what, ADRs explain why
- Include enough context so you can understand the decision in 6 months
- It's okay to make wrong decisions - document them and learn
