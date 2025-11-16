# Learning Log

A personal journal documenting key learnings, theory, and insights throughout the project development.

---

## 2025-11-16: Project Initialization

### Topic: Project Architecture & Modular Design

**What I Learned:**
- The importance of **modular architecture** in scientific pipelines
- Each module should have a **single responsibility** (data acquisition, processing, analysis, etc.)
- Separation of concerns makes code more maintainable and testable
- Configuration files (YAML) allow changing behavior without modifying code

**Key Concepts:**
- **Modularity**: Breaking complex systems into independent, reusable components
- **Separation of Concerns**: Different aspects of the application should be handled by different modules
- **DRY Principle**: Don't Repeat Yourself - write reusable functions

**Why This Matters:**
In proteomics, pipelines can become very complex. A modular design allows:
- Easy debugging (isolate issues to specific modules)
- Reusability (use same QC module for different analyses)
- Scalability (add new analysis types without rewriting everything)
- Collaboration (different people can work on different modules)

---

## 2025-11-16: Technology Stack Selection

### Topic: Choosing the Right Tools

**What I Learned:**

1. **UV Package Manager**
   - Modern alternative to pip/poetry
   - Much faster dependency resolution
   - Creates lock files for reproducibility
   - Built-in virtual environment management

2. **Snakemake for Workflow Management**
   - Declarative syntax (define what, not how)
   - Automatic dependency resolution
   - Parallelization out of the box
   - Industry standard in bioinformatics
   
   **Key Insight**: Snakemake is like Make but for data pipelines. It tracks:
   - Which files need to be created
   - Dependencies between steps
   - What needs to be rerun when inputs change

3. **Docker for Reproducibility**
   - Packages entire environment (OS, Python, libraries)
   - "It works on my machine" → "It works everywhere"
   - Critical for scientific reproducibility
   - Makes sharing pipelines trivial

**Challenges:**
- Initial learning curve for Snakemake syntax
- Docker adds complexity but worth it for reproducibility

**Resources:**
- [Snakemake Tutorial](https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html)
- [UV Documentation](https://github.com/astral-sh/uv)

---

## 2025-11-16: Understanding PRIDE Repository

### Topic: Proteomics Data Sources

**What I Learned:**

**PRIDE (PRoteomics IDEntifications Database)**:
- Largest public proteomics repository
- Part of ProteomeXchange Consortium
- Datasets identified by **PXD accessions** (e.g., PXD005011)
- Provides REST API for programmatic access

**ProteomeXchange Consortium**:
- Global network of proteomics repositories
- Includes: PRIDE (Europe), MassIVE (USA), jPOST (Japan), iProx (China)
- Standardized data submission and sharing

**Key File Formats**:
- **mzML**: Raw mass spectrometry data (large, XML-based)
- **mzTab**: Standardized table format for MS results
- **mzIdentML**: Peptide/protein identifications
- **CSV/TSV**: Simple tabular formats

**Why This Matters**:
Understanding data sources and formats is crucial for:
- Knowing what data is available
- Choosing appropriate parsers
- Understanding data limitations

**Resources:**
- [PRIDE Archive](https://www.ebi.ac.uk/pride/)
- [mzTab Specification](https://github.com/HUPO-PSI/mzTab)

---

## 2025-11-16: Differential Expression Analysis Concept

### Topic: Core Analysis Strategy

**What I Learned:**

**Differential Expression (DE) Analysis** compares protein abundance between conditions:
- Example: Healthy vs. Diseased tissue
- Goal: Find proteins that are significantly different

**Key Steps**:
1. **Data Preprocessing**:
   - Handle missing values
   - Log transformation (makes data more normal)
   - Normalization (remove technical variation)

2. **Statistical Testing**:
   - T-test for two groups
   - Calculate fold-change (how much protein changed)
   - P-value (is difference statistically significant?)

3. **Multiple Testing Correction**:
   - When testing thousands of proteins, some will appear significant by chance
   - **FDR (False Discovery Rate)**: Controls proportion of false positives
   - **Bonferroni**: More conservative, controls family-wise error rate

4. **Visualization**:
   - **Volcano Plot**: Shows fold-change vs. significance
   - **Heatmap**: Shows expression patterns across samples
   - **PCA**: Shows how samples cluster

**Key Terms**:
- **Log2 Fold-Change**: log2(Treatment/Control)
  - +1 means 2x higher in treatment
  - -1 means 2x lower in treatment
- **P-value**: Probability result is due to chance
- **FDR**: Expected proportion of false discoveries
- **Alpha**: Significance threshold (typically 0.05)

**Why Log Transform?**
- Makes data distribution more normal
- Makes fold-changes symmetric (2x up = -2x down)
- Stabilizes variance

**Resources:**
- [Statistics for Proteomics](https://www.nature.com/articles/nmeth.3901)

---

## Template for Future Entries

```markdown
## YYYY-MM-DD: [Topic Title]

### Topic: [Brief Description]

**What I Learned:**
- Key point 1
- Key point 2

**Key Concepts:**
- Concept and definition

**Challenges:**
- What was difficult
- How I overcame it

**Code Example** (if applicable):
```python
# Example code
```

**Resources:**
- [Link to documentation]

**Next Steps:**
- What to explore next
```

---

## Notes

This log is meant to be personal and informal. Focus on:
- **Understanding WHY**, not just HOW
- Capturing "aha!" moments
- Documenting dead ends and mistakes (they're valuable!)
- Connecting theory to practice
- Building intuition about proteomics and data science
