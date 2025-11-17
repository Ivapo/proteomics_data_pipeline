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

## 2025-11-17: Exploring the PRIDE REST API

**Related Task**: Epic 2, Task 2.1 - Research PRIDE REST API endpoints and authentication

### Topic: Working with REST APIs for Data Retrieval

**REST API Basics**:
- **REST** = Representational State Transfer
- Uses HTTP methods (GET, POST, PUT, DELETE)
- Returns data in JSON format
- No authentication needed for PRIDE public data

**PRIDE API Structure**:
- Base URL: `https://www.ebi.ac.uk/pride/ws/archive/v2/`
- Version 3 available for some endpoints: `v3/`
- Well-documented at: https://www.ebi.ac.uk/pride/markdownpage/prideapi

**Key Endpoints Discovered**:

1. **Get Project Metadata**: `GET /projects/{accession}`
   - Example: `/projects/PXD000001`
   - Returns: title, description, submitters, organisms, instruments, publication date, DOI
   - Use case: Verify dataset exists and get context before downloading

2. **List Project Files**: `GET /projects/{accession}/files` (v3)
   - Returns array of file objects with:
     - `fileName`: Name of file
     - `fileSizeBytes`: Size for download progress tracking
     - `fileCategory`: Type (PEAK, RAW, RESULT, OTHER)
     - `publicFileLocations`: Array with FTP URLs
   - Use case: See what files are available before downloading

3. **Search Projects**: `GET /search/projects?keyword={term}`
   - Example: `?keyword=cancer&pageSize=100&sortDirection=DESC`
   - Use case: Find relevant datasets programmatically

**Testing the API**:
Used `curl` in PowerShell to test endpoints:
```powershell
curl "https://www.ebi.ac.uk/pride/ws/archive/v2/projects/PXD000001"
curl "https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD000001/files"
```

**JSON Response Structure**:
- Nested objects and arrays
- Need to parse carefully
- Example file object has `publicFileLocations` as array of CV params with `value` field containing actual URL

**Key Insights**:
- API returns A LOT of metadata - need to extract what we need
- File URLs are FTP links, will need FTP download capability
- No rate limiting observed on public endpoints
- Some data fields use controlled vocabularies (CV terms) like "MS:1001742" for instrument types

**Challenges:**
- Deeply nested JSON requires careful parsing
- PowerShell JSON conversion can truncate at depth limit
- Need to handle various file categories (might only want specific types)

**Next Steps:**
- Implement Python class to wrap these API calls
- Add error handling for missing projects
- Create methods: `get_metadata()`, `list_files()`, `search_datasets()`

**Resources:**
- [PRIDE API Documentation](https://www.ebi.ac.uk/pride/markdownpage/prideapi)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

---

## 2025-11-17: Implementing the PRIDE API Client

**Related Task**: Epic 2, Tasks 2.2 & 2.3 - Implement PRIDEClient class with basic API calls and metadata retrieval

### Topic: Building a Python REST API Client


Created the `PRIDEClient` class in `src/data_acquisition/pride_api.py` with three main methods:

1. **`get_dataset_metadata(dataset_id)`**
   - Fetches complete metadata for a PRIDE project (e.g., PXD000001)
   - Returns: title, description, submitters, organisms, instruments, publication info
   - Error handling: Raises `ValueError` if dataset not found (404 error)
   - Example: `client.get_dataset_metadata("PXD000001")`

2. **`search_datasets(query, page_size=10)`**
   - Searches PRIDE for datasets matching a keyword
   - Returns: List of matching projects sorted by submission date
   - Had to handle API inconsistency - sometimes returns list, sometimes nested object
   - Example: `client.search_datasets("cancer", page_size=5)`

3. **`get_dataset_files(dataset_id)`**
   - Lists all files available for a dataset
   - Extracts useful info: fileName, fileSizeBytes, fileCategory, downloadUrl
   - Uses v3 API endpoint (different from metadata which uses v2)
   - Parses nested `publicFileLocations` to extract FTP URLs
   - Example: `client.get_dataset_files("PXD000001")`

**Key Concepts Learned:**

**HTTP Session Management:**
- Used `requests.Session()` to reuse connections (faster for multiple requests)
- Set headers once: `Accept: application/json` and custom `User-Agent`
- Sessions automatically handle cookies and connection pooling

**Error Handling:**
- `response.raise_for_status()` - raises exception for HTTP errors (404, 500, etc.)
- Catch `requests.HTTPError` separately from general `RequestException`
- Return meaningful errors to users (e.g., "Dataset PXD999 not found")

**API Versioning:**
- PRIDE has v2 and v3 APIs with different endpoints
- v2: `/projects/{id}` for metadata
- v3: `/projects/{id}/files` for file listings
- Had to dynamically replace v2→v3 in URL: `self.base_url.replace('v2', 'v3')`

**JSON Parsing Challenges:**
- File locations deeply nested: `file_data["publicFileLocations"][0]["value"]`
- Had to iterate through locations array to find FTP URL
- Search API inconsistent: sometimes returns list, sometimes `{"_embedded": {"projects": [...]}}`
- Solution: Check data type with `isinstance(data, list)` before parsing

**Testing with pytest:**

Created comprehensive tests in `tests/test_data_acquisition/test_pride_api.py`:
- ✅ `test_client_initialization` - Verify client setup
- ✅ `test_get_project_metadata` - Test real API call to PXD000001
- ✅ `test_list_project_files` - Verify file listing works
- ✅ `test_search_projects` - Search for "Erwinia" datasets
- ✅ `test_invalid_project` - Verify error handling with `pytest.raises()`

**Command used:**
```powershell
pytest tests/test_data_acquisition/test_pride_api.py -v
```

**Challenges & Solutions:**

1. **Test naming mismatch**: Tests called `get_project_metadata()` but code had `get_dataset_metadata()`
   - Fixed: Updated test to match actual method name

2. **Search API structure**: Assumed nested `_embedded.projects` but API returned flat list
   - Fixed: Added type checking - handle both list and nested object formats

3. **File URL extraction**: URLs buried in CV param objects
   - Fixed: Loop through `publicFileLocations` to find "FTP Protocol" entry

**What I Learned:**

- **API clients should be defensive**: Handle multiple response formats
- **Logging is crucial**: Every method logs what it's doing (easier debugging later)
- **Test with real data**: Using PXD000001 (real dataset) caught actual API quirks
- **Type hints help**: `-> Dict` and `-> List[Dict]` make code clearer

**Code Coverage:**
- PRIDEClient now at 73% coverage (up from 19%)
- Still need to implement: `download_file()` method (Task 2.4)

**Files Modified:**
- `src/data_acquisition/pride_api.py` - Implemented PRIDEClient class with 3 methods
- `tests/test_data_acquisition/test_pride_api.py` - Created 5 comprehensive tests

**Next Steps:**
- Task 2.4: Implement file download with progress bar using `tqdm`
- Task 2.5: Add caching to avoid repeated API calls
- Task 2.8: Add retry logic for network failures

---

## 2025-11-17: Implementing File Downloads with Progress Tracking

**Related Task**: Epic 2, Task 2.4 - Implement file download with progress tracking

### Topic: Downloading Files from FTP and HTTP with Progress Bars

Implemented file download functionality in the `PRIDEClient` class to download proteomics datasets from PRIDE servers.

**Key Implementation Details:**

1. **Multi-Protocol Support**:
   - Created `download_file()` main method that detects protocol (FTP vs HTTP)
   - Implemented `_download_http()` for HTTP/HTTPS downloads using `requests`
   - Implemented `_download_ftp()` for FTP downloads using `urllib.request.urlopen()`

2. **Progress Tracking**:
   - Used `tqdm` library to show real-time download progress
   - Display format: `filename: 100%|█| 101k/101k [00:01<00:00, 89.5kB/s]`
   - Shows: filename, percentage, bytes downloaded/total, time elapsed/remaining, speed

3. **Streaming Downloads**:
   - Download in chunks (default 8KB) to handle large files efficiently
   - Prevents loading entire file into memory
   - Updates progress bar after each chunk

4. **Error Handling**:
   - Cleans up partial downloads if error occurs
   - Logs all download attempts and failures
   - Raises appropriate exceptions for caller to handle

**Why FTP Support Was Needed:**

Initially implemented only HTTP downloads using `requests.Session.get()`, but discovered PRIDE files are hosted on FTP servers:
```
ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001/...
```

The `requests` library doesn't support FTP protocol, causing error:
```
requests.exceptions.InvalidSchema: No connection adapters were found for 'ftp://...'
```

**Solution**: Use Python's built-in `urllib.request.urlopen()` which supports FTP.

**Key Concepts Learned:**

**Protocol Detection**:
```python
if file_url.startswith('ftp://'):
    self._download_ftp(file_url, output_path, chunk_size)
else:
    self._download_http(file_url, output_path, chunk_size)
```

**Streaming with tqdm**:
```python
with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
    for chunk in response.iter_content(chunk_size=chunk_size):
        f.write(chunk)
        pbar.update(len(chunk))
```
- `unit_scale=True`: Automatically converts B → KB → MB → GB
- `unit_divisor=1024`: Binary units (1KB = 1024 bytes, not 1000)

**FTP File Size Handling**:
- HTTP has `Content-Length` header for file size
- FTP may not always provide file size
- Solution: Disable progress bar if size unknown (`disable=total_size == 0`)

**Path Management**:
```python
output_file = Path(output_path)
output_file.parent.mkdir(parents=True, exist_ok=True)
```
- `parents=True`: Create all intermediate directories
- `exist_ok=True`: Don't error if directory already exists

**Challenges & Solutions:**

1. **FTP Protocol Not Supported by requests**:
   - Problem: `requests` library only handles HTTP/HTTPS
   - Solution: Split download logic - use `urllib.request` for FTP, `requests` for HTTP

2. **File Size Mismatch in Tests**:
   - Problem: API reported 497,985 bytes, downloaded 103,845 bytes
   - Reason: File is compressed (.gz), API may report uncompressed size
   - Solution: Changed test assertion to verify file exists and is reasonable size (not exact match)

3. **Cleaning Up Failed Downloads**:
   - Problem: Partial files left on disk if download fails
   - Solution: Added try/except that deletes partial file using `output_file.unlink()`

**Testing:**

Created `test_download_file()` in test suite:
- Finds small file (<1MB) from PXD000001 dataset
- Downloads to pytest's temporary directory (`tmp_path` fixture)
- Verifies: file exists, size > 0, size < 10MB (sanity check)
- Successfully downloaded 103KB test file in ~2 seconds

**Command used:**
```powershell
uv run pytest tests/test_data_acquisition/test_pride_api.py -v
```

**What I Learned:**

- **Different libraries for different protocols**: `requests` for HTTP, `urllib` for FTP
- **tqdm is powerful**: Automatically formats bytes, calculates speed, shows ETA
- **Streaming is essential**: Don't load multi-GB files into memory
- **Always clean up on failure**: Delete partial downloads to avoid confusion
- **Test with real data carefully**: Small files for tests, but verify protocol handling

**Code Coverage:**
- PRIDEClient now at 69% coverage
- All 6 tests passing (added 1 new download test)

**Files Modified:**
- `src/data_acquisition/pride_api.py` - Added `download_file()`, `_download_http()`, `_download_ftp()` methods; imported `tqdm`, `Path`, `urlopen`
- `tests/test_data_acquisition/test_pride_api.py` - Added `test_download_file()` with small file download test

**Next Steps:**
- Task 2.5: Add caching mechanism to avoid re-downloading files
- Task 2.6: Parse mzTab files after download
- Task 2.8: Add retry logic for network failures

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
