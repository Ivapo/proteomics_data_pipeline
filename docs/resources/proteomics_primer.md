# Proteomics Primer

A beginner-friendly introduction to proteomics concepts.

## What is Proteomics?

**Proteomics** is the large-scale study of proteins - their structure, function, and abundance in biological systems.

## Key Concepts

### 1. Mass Spectrometry (MS)
The primary technology for proteomics:
- **Ionization**: Convert proteins/peptides to charged particles
- **Mass Analysis**: Measure mass-to-charge ratio (m/z)
- **Detection**: Record abundance at each m/z

### 2. Bottom-Up Proteomics
The most common approach:
1. Digest proteins into peptides (usually with trypsin)
2. Analyze peptides by MS
3. Identify proteins from peptide sequences
4. Quantify protein abundance

### 3. Protein Quantification Methods

**Label-Free Quantification (LFQ)**:
- Compare peptide intensities across samples
- No chemical labeling required
- Most common in PRIDE datasets

**Labeled Quantification**:
- TMT (Tandem Mass Tags)
- SILAC (Stable Isotope Labeling)
- iTRAQ (Isobaric Tags)

### 4. Differential Expression
Comparing protein abundance between conditions:
- **Healthy vs. Disease**
- **Treated vs. Untreated**
- **Time points**

## Important Terms

- **Peptide**: Small protein fragment (amino acid chain)
- **Protein Intensity**: Measure of protein abundance
- **Missing Values**: Proteins not detected in some samples
- **PSM**: Peptide Spectrum Match - confident peptide identification
- **FDR**: False Discovery Rate - expected proportion of false positives

## Data Formats

### mzML
Raw mass spectrometry data (large files, ~GB)

### mzTab
Standardized tabular format for MS results
- Contains protein/peptide identifications
- Includes quantification values
- Human-readable

### CSV/TSV
Simple spreadsheet formats
- Protein ID
- Sample intensities
- Metadata

## Analysis Workflow

```
Sample → Protein Extraction → Digestion → MS Analysis → 
Raw Data → Identification → Quantification → 
Statistical Analysis → Biological Interpretation
```

## Resources

- [PRIDE Database](https://www.ebi.ac.uk/pride/)
- [Proteomics Tutorial](https://www.nature.com/articles/nprot.2016.136)
- [Mass Spectrometry Basics](https://www.nature.com/articles/nmeth.1692)
