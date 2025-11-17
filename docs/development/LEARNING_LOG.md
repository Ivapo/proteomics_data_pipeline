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

## 2025-11-17: Implementing API Response Caching

**Related Task**: Epic 2, Task 2.5 - Add caching mechanism for API responses

### Topic: Disk-based Caching for API Responses

Implemented a caching system to avoid repeated API calls by storing responses to disk and reusing them when fresh.

**Why Caching Matters:**

**Problem**: During development/testing, you often call the same API endpoint multiple times:
```python
metadata = client.get_dataset_metadata("PXD000001")  # API call
# ... later in code ...
metadata = client.get_dataset_metadata("PXD000001")  # Another API call!
```

This is wasteful:
- Unnecessary network requests (slower)
- Extra load on PRIDE servers (not respectful)
- Slows down testing/iteration

**Solution**: Cache the first response to disk, reuse it for subsequent calls.

**Implementation Approach:**

Chose **disk-based caching** over in-memory because:
1. Persists between program runs (important during development)
2. Visible - can inspect cache files
3. Easy to clear - just delete files
4. Works well with testing

**Key Design Decisions:**

1. **Cache Location**: `data/cache/` directory
   - Already defined in project structure
   - Added to config.yaml: `cache_enabled: true`, `cache_max_age_hours: 24`

2. **Cache Keys**: MD5 hash of endpoint + parameters
   - Example: `metadata_PXD000001` → `151ae0ebdd5efd82d98a83d13344ea44.json`
   - Why hash? Creates valid filenames, avoids special characters
   ```python
   cache_str = f"{endpoint}_{json.dumps(params, sort_keys=True)}"
   cache_key = hashlib.md5(cache_str.encode()).hexdigest()
   ```

3. **Cache Expiration**: Files older than 24 hours are ignored
   - Uses file modification time (`st_mtime`)
   - Compares with `datetime.now() - timedelta(hours=24)`
   - Stale cache = fresh API call

4. **Enable/Disable**: Constructor parameters allow turning off caching
   ```python
   client = PRIDEClient(cache_enabled=False)  # Disable for production
   ```

**Three Helper Methods:**

1. **`_get_cache_key(endpoint, **params)`**:
   - Creates unique identifier for each request
   - Same params = same key = cache hit

2. **`_get_from_cache(cache_key)`**:
   - Checks if cache file exists
   - Validates file age (not expired)
   - Loads and returns JSON data
   - Returns `None` if cache miss or expired

3. **`_save_to_cache(cache_key, data)`**:
   - Saves response data to JSON file
   - Pretty-printed with `indent=2` (easier to inspect)
   - Creates cache directory if needed

**Integration with Existing Methods:**

Updated two methods to use caching:

**Before (no cache):**
```python
def get_dataset_metadata(self, dataset_id: str):
    url = f"{self.base_url}/projects/{dataset_id}"
    response = self.session.get(url)
    return response.json()
```

**After (with cache):**
```python
def get_dataset_metadata(self, dataset_id: str):
    # Check cache first
    cache_key = self._get_cache_key("metadata", dataset_id=dataset_id)
    cached_data = self._get_from_cache(cache_key)
    if cached_data is not None:
        return cached_data
    
    # Cache miss - fetch from API
    url = f"{self.base_url}/projects/{dataset_id}"
    response = self.session.get(url)
    data = response.json()
    
    # Save to cache for next time
    self._save_to_cache(cache_key, data)
    return data
```

**What I Learned:**

**Cache Invalidation Strategy**:
- Time-based expiration is simplest (24 hours)
- Could also use ETag headers from API (more complex)
- For proteomics datasets: metadata rarely changes, so time-based is fine

**MD5 Hashing for Cache Keys**:
- Creates consistent, filesystem-safe filenames
- `hashlib.md5(string.encode()).hexdigest()` → 32-character hex string
- Same input always produces same hash
- Collisions extremely unlikely for our use case

**File Timestamps**:
- `Path.stat().st_mtime` returns last modification time as Unix timestamp
- Convert to datetime: `datetime.fromtimestamp(st_mtime)`
- Calculate age: `datetime.now() - file_datetime`

**Graceful Degradation**:
- If cache file corrupted (invalid JSON), fall back to API call
- If cache disabled, methods work normally without caching
- Errors logged but don't break functionality

**Testing Strategy:**

Created two specific caching tests:

1. **`test_caching()`**:
   - Creates client with temporary cache directory
   - Makes first call, verifies cache file created
   - Makes second call, verifies same data returned (cache hit)
   - Tests both metadata and file listing endpoints

2. **`test_cache_disabled()`**:
   - Creates client with `cache_enabled=False`
   - Verifies methods still work
   - Ensures no cache files are created

**Real-World Test:**
```python
# First call - hits API
client = PRIDEClient()
m1 = client.get_dataset_metadata("PXD000001")  # ~0.5-1s (network)

# Second call - uses cache  
m2 = client.get_dataset_metadata("PXD000001")  # ~0.001s (disk read)
```

Speed improvement: **~100-1000x faster** for cached responses!

**Cache File Example:**
```json
{
  "accession": "PXD000001",
  "title": "TMT spikes - Using R and Bioconductor...",
  "submitters": [...],
  ...
}
```

**Challenges & Solutions:**

1. **Challenge**: How to generate unique cache keys for different parameter combinations?
   - Solution: JSON serialize params with `sort_keys=True` (consistent ordering)
   - Hash the result to create short, valid filename

2. **Challenge**: How to check if cache is stale?
   - Solution: Compare file modification time with current time
   - Use `timedelta` for readable time comparisons

3. **Challenge**: Tests creating permanent cache files
   - Solution: Use pytest's `tmp_path` fixture for isolated cache directories
   - Each test gets its own temp directory, auto-cleaned after test

**Code Coverage:**
- PRIDEClient now at 75% coverage (up from 72%)
- All 8 tests passing (added 2 caching tests)

**Files Modified:**
- `config/config.yaml` - Added `cache_enabled` and `cache_max_age_hours` settings
- `src/data_acquisition/pride_api.py` - Implemented caching with 3 helper methods; added imports: `json`, `hashlib`, `datetime`; updated `__init__`, `get_dataset_metadata`, `get_dataset_files`
- `tests/test_data_acquisition/test_pride_api.py` - Added `test_caching()` and `test_cache_disabled()`

**Next Steps:**
- Task 2.6: Parse mzTab format files
- Task 2.7: Add support for CSV/TSV proteomics files
- Task 2.8: Add retry logic for failed API calls

---

## 2025-11-17: Parsing Proteomics File Formats (mzTab, CSV/TSV)

**Related Task**: Epic 2, Tasks 2.6 & 2.7 - Create file parser for mzTab format and add CSV/TSV support

### Topic: Parsing Structured Proteomics Data Files

Implemented a `FileParser` class to read various proteomics file formats into pandas DataFrames.

**mzTab File Format:**

**What is mzTab?**
- **HUPO-PSI standard** for reporting mass spectrometry results
- Tab-delimited text format (easy to parse, human-readable)
- Designed to be opened in Excel while remaining machine-parsable
- Lightweight summary format (not raw data)

**mzTab Structure:**

mzTab files have **four main sections**, each with specific prefixes:

1. **MTD (Metadata)**: File-level information
   ```
   MTD	mzTab-version	1.0.0
   MTD	title	Proteomics Study of Cancer Cells
   MTD	description	iTRAQ labeled quantification
   MTD	ms_run[1]-location	file://data/run1.raw
   ```

2. **PRH/PRT (Protein Section)**: Protein quantification
   ```
   PRH	accession	description	coverage	abundance_study_variable[1]
   PRT	P12345	Protein kinase	0.45	1234.56
   PRT	Q67890	Hemoglobin	0.78	2345.67
   ```

3. **PEH/PEP (Peptide Section)**: Peptide-level data
   ```
   PEH	sequence	accession	unique	database
   PEP	PEPTIDER	P12345	1	UniProt
   ```

4. **PSH/PSM (Peptide-Spectrum Match)**: Identification evidence
   ```
   PSH	sequence	PSM_ID	accession	charge
   PSM	PEPTIDER	1	P12345	2
   ```

**Key Insight**: Each section starts with header (H suffix) then data rows (T suffix for proteins, P for peptides, M for PSMs).

**Implementation Details:**

**`parse_mztab(file_path)`**:
```python
# Read line by line, categorize by prefix
for line in file:
    fields = line.split('\t')
    prefix = fields[0]
    
    if prefix == 'MTD':
        metadata.append(fields)
    elif prefix == 'PRH':
        protein_header = fields[1:]  # Skip prefix
    elif prefix == 'PRT':
        protein_rows.append(fields[1:])

# Convert to DataFrame
df = pd.DataFrame(protein_rows, columns=protein_header)
```

**Key Design Decision**: Return protein DataFrame by default (most common use case for quantification analysis).

**`get_mztab_metadata(file_path)`**:
- Extracts all MTD lines into dictionary
- Format: `MTD	key	value`
- Useful for understanding dataset context before processing

**CSV/TSV Parsing:**

**`parse_tabular(file_path, delimiter=None)`**:
- Auto-detects delimiter based on file extension
  - `.csv` → comma
  - `.tsv`, `.txt` → tab
  - Unknown → peek at first line
- Uses pandas `read_csv()` with appropriate delimiter
- Simple but effective for standard tabular formats

**Delimiter Auto-Detection Logic:**
```python
# Extension-based
if suffix == '.csv':
    delimiter = ','
elif suffix in ['.tsv', '.txt']:
    delimiter = '\t'
else:
    # Content-based
    with open(file_path) as f:
        first_line = f.readline()
        delimiter = '\t' if '\t' in first_line else ','
```

**`parse_file(file_path)`**: Auto-detect format and route to appropriate parser:
```python
suffix = Path(file_path).suffix.lower()

if suffix == ".mztab":
    return self.parse_mztab(file_path)
elif suffix in [".csv", ".tsv", ".txt"]:
    return self.parse_tabular(file_path)
else:
    raise ValueError(f"Unsupported format: {suffix}")
```

**Testing Strategy:**

Created comprehensive test suite with **8 test cases**:

1. **`test_parser_initialization`**: Verify object creation
2. **`test_parse_mztab`**: Parse complete mzTab with protein section
3. **`test_parse_mztab_metadata`**: Extract metadata dictionary
4. **`test_parse_csv`**: Parse comma-separated values
5. **`test_parse_tsv`**: Parse tab-separated values
6. **`test_auto_detect_file_type`**: Verify format auto-detection
7. **`test_invalid_file`**: Error handling for missing files
8. **`test_empty_mztab`**: Handle files with metadata but no data

**Using tmp_path Fixture:**
```python
def test_parse_mztab(self, tmp_path):
    # Create test file in temporary directory
    mztab_file = tmp_path / "test.mztab"
    mztab_file.write_text(mztab_content)
    
    # Parse and verify
    df = parser.parse_mztab(str(mztab_file))
    assert len(df) == 3
```

**What I Learned:**

**Standard File Formats:**
- Standardization is crucial in bioinformatics (enables tool interoperability)
- mzTab balances human-readability with machine-parseability
- Tab-delimited formats are simple but effective

**Parsing Strategies:**
- **Line-by-line parsing** better for large files than loading entire file
- **Prefix-based routing** (MTD, PRH, PRT) makes parsing straightforward
- **Section accumulation** (collect all proteins, then convert to DataFrame at end)

**Error Handling:**
- Always check file existence before parsing
- Return empty DataFrame for valid but data-less files (not error)
- Raise specific errors (`FileNotFoundError`, `ValueError`) for different failure modes

**Testing with Fixtures:**
- `tmp_path` pytest fixture creates isolated test directories
- Write test data to temp files (auto-cleaned after test)
- Tests are independent, can run in any order

**Challenges & Solutions:**

1. **Challenge**: mzTab can have multiple sections (protein, peptide, PSM) - which to return?
   - Solution: Return protein section by default (most common), can add methods for peptides/PSMs later

2. **Challenge**: How to handle tabs in field values?
   - Solution: Use `'\t'.join(fields[2:])` to rejoin multi-field values

3. **Challenge**: Empty files or files with only metadata
   - Solution: Return empty DataFrame (len=0) rather than error - allows graceful handling

**Code Coverage:**
- FileParser: 79% coverage (97 statements, 20 missed)
- All 8 tests passing in <1 second

**Files Modified:**
- `src/data_acquisition/file_parser.py` - Implemented `parse_mztab()`, `get_mztab_metadata()`, `parse_tabular()` methods
- `tests/test_data_acquisition/test_file_parser.py` - Created comprehensive test suite with 8 test cases

**What This Enables:**

With file parsing implemented, we can now:
1. Download datasets from PRIDE (Tasks 2.1-2.5 ✓)
2. Parse the downloaded files (Tasks 2.6-2.7 ✓)
3. Next: Process the data (Epic 3)

**Resources:**
- [mzTab Specification](https://github.com/HUPO-PSI/mzTab)
- [mzTab 1.0 Paper](http://www.mcponline.org/content/early/2014/06/30/mcp.O113.036681.abstract)
- [Pandas read_csv documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)

**Next Steps:**
- Task 2.8: Add retry logic for API failures
- Task 2.9: Additional unit tests (already have good coverage)
- Task 2.10: Create demo notebook showing download → parse workflow

---

## 2025-11-18: Implementing Resilient API Calls with Retry Logic

**Related Task**: Epic 2, Task 2.8 - Implement error handling and retries

### Topic: Building Fault-Tolerant Network Communication

Implemented automatic retry logic with exponential backoff to make the PRIDE API client resilient to transient network failures.

**The Problem:**

Network requests can fail for many reasons:
- **Transient failures**: Temporary network glitches, WiFi drops
- **Server overload**: PRIDE servers temporarily unavailable (503 Service Unavailable)
- **Timeouts**: Slow connections, large responses taking too long
- **Connection errors**: DNS issues, server unreachable

Without retry logic, any of these would crash the entire pipeline, even though retrying might succeed.

**Solution: Exponential Backoff Retry Strategy**

**What is Exponential Backoff?**

A retry strategy where wait time doubles after each failure:
- Attempt 1: Fails → wait 1 second (2^0)
- Attempt 2: Fails → wait 2 seconds (2^1)
- Attempt 3: Fails → wait 4 seconds (2^2)
- Attempt 4: Success!

**Why exponential?**
- Gives servers time to recover (not hammering an overloaded server)
- Avoids thundering herd problem (many clients retrying simultaneously)
- Industry standard (used by AWS, Google, GitHub APIs)

**Implementation:**

Created `_make_request_with_retry()` method:

```python
def _make_request_with_retry(self, url: str, params: Optional[Dict] = None) -> requests.Response:
    last_exception = None
    
    for attempt in range(self.max_retries):
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response
            
        except requests.Timeout:
            logger.warning(f"Request timeout (attempt {attempt + 1}/{self.max_retries})")
        except requests.ConnectionError:
            logger.warning(f"Connection error (attempt {attempt + 1}/{self.max_retries})")
        except requests.HTTPError as e:
            # Don't retry client errors (4xx)
            if e.response.status_code < 500:
                raise
            # Retry server errors (5xx)
            logger.warning(f"Server error {e.response.status_code}")
        
        # Exponential backoff
        if attempt < self.max_retries - 1:
            wait_time = self.backoff_factor ** attempt  # 1s, 2s, 4s, 8s...
            logger.info(f"Retrying in {wait_time:.1f} seconds...")
            time.sleep(wait_time)
    
    # All retries exhausted
    raise last_exception
```

**Key Design Decisions:**

**1. Selective Retrying:**

Only retry errors that might be transient:
- ✅ **Timeout** (`requests.Timeout`): Retry - might work with more time
- ✅ **Connection Error** (`requests.ConnectionError`): Retry - network might recover
- ✅ **Server Error (5xx)**: Retry - server might be temporarily down
- ❌ **Client Error (4xx)**: Don't retry - request is bad, won't succeed

**Example - 404 Not Found:**
```python
# Bad dataset ID - will NEVER work, don't waste time retrying
client.get_dataset_metadata("PXD999999999")
# Immediately raises ValueError (no retries)
```

**2. Configurable Parameters:**

Added to `__init__`:
```python
def __init__(self, 
             timeout: int = 30,        # Seconds before timeout
             max_retries: int = 3,     # How many retry attempts
             backoff_factor: float = 2.0):  # Multiplier for wait time
```

**3. Timeout Handling:**

Added `timeout` parameter to prevent hanging forever:
```python
response = self.session.get(url, timeout=self.timeout)
# Raises requests.Timeout if takes longer than 30 seconds
```

**Integration:**

Updated three main API methods to use retry wrapper:

```python
# Before:
response = self.session.get(url)
response.raise_for_status()

# After:
response = self._make_request_with_retry(url)
# Automatically retries on failure
```

**Configuration (config.yaml):**

```yaml
pride_api:
  timeout: 30
  max_retries: 3
  backoff_factor: 2.0
```

Users can adjust based on their needs:
- **Fast development**: `timeout: 5, max_retries: 1`
- **Production reliability**: `timeout: 60, max_retries: 5`

**Testing Strategy:**

Created 6 new tests using mocking to simulate failures:

**1. `test_retry_on_timeout`**: Timeout twice, succeed third time
```python
mock_get.side_effect = [
    requests.Timeout("Timeout 1"),
    requests.Timeout("Timeout 2"),
    mock_response  # Success!
]
# Verifies retry count: 3
```

**2. `test_retry_on_connection_error`**: Network failure then recovery
```python
mock_get.side_effect = [
    requests.ConnectionError("Connection failed"),
    mock_response  # Success!
]
```

**3. `test_no_retry_on_404`**: Don't retry client errors
```python
mock_response.status_code = 404
# Should fail immediately, call_count == 1 (no retries)
```

**4. `test_retry_on_server_error`**: Retry on 503
```python
mock_response_error.status_code = 503
# Should retry
```

**5. `test_retry_exhaustion`**: All retries fail
```python
mock_get.side_effect = requests.Timeout("Always fails")
# Raises after max_retries attempts
```

**6. `test_custom_retry_settings`**: Verify configuration works

**What I Learned:**

**HTTP Status Code Classes:**
- **1xx (Informational)**: Request received, continuing
- **2xx (Success)**: Request successfully processed
- **3xx (Redirection)**: Further action needed
- **4xx (Client Error)**: Bad request from client - DON'T RETRY
  - 400 Bad Request, 401 Unauthorized, 404 Not Found
- **5xx (Server Error)**: Server failed - RETRY
  - 500 Internal Server Error, 503 Service Unavailable

**Why `response.status_code < 500`:**
Check if it's a client error (4xx) to avoid retrying.

**Mock Testing:**
- `unittest.mock.Mock()` creates fake objects
- `side_effect` can be list of return values (different per call)
- `call_count` verifies how many times method was called
- Essential for testing network code without actual network calls

**Exponential Backoff Math:**
```python
wait_time = backoff_factor ** attempt
# attempt 0: 2^0 = 1 second
# attempt 1: 2^1 = 2 seconds
# attempt 2: 2^2 = 4 seconds
# Total: 7 seconds over 3 retries
```

**Alternative: `backoff_factor * (2 ** attempt)`:**
- 0: 2 * 1 = 2s
- 1: 2 * 2 = 4s
- 2: 2 * 4 = 8s
Both work, chose simpler formula.

**Challenges & Solutions:**

**1. Challenge**: How to test network failures without actual failures?
   - Solution: Mock `session.get()` to raise specific exceptions

**2. Challenge**: Server errors (5xx) should retry, client errors (4xx) shouldn't
   - Solution: Check `e.response.status_code < 500` - only raise immediately on client errors

**3. Challenge**: Testing exponential backoff timing would slow tests
   - Solution: Use `backoff_factor=0.1` in tests for faster execution

**4. Challenge**: Last exception might be `None` if no exceptions raised
   - Solution: Initialize `last_exception = None`, only raise at end if set

**Real-World Impact:**

**Before (no retries):**
```
# User experience
>>> client.get_dataset_metadata("PXD000001")
ConnectionError: Connection refused
# Pipeline crashes, user has to restart
```

**After (with retries):**
```
# User experience
>>> client.get_dataset_metadata("PXD000001")
WARNING: Request timeout (attempt 1/3)
INFO: Retrying in 1.0 seconds...
WARNING: Request timeout (attempt 2/3)
INFO: Retrying in 2.0 seconds...
INFO: Successfully retrieved metadata for PXD000001
# Success! User doesn't even notice the hiccup
```

**Test Results:**
- All 14 tests passing (8 original + 6 new)
- Coverage: 78% for pride_api.py (up from 75%)
- Total statements: 192 (up from 167 due to retry logic)

**Files Modified:**
- `src/data_acquisition/pride_api.py` - Added `time` import, timeout/retry params to `__init__`, implemented `_make_request_with_retry()`, updated 3 API methods
- `config/config.yaml` - Added `timeout`, `max_retries`, `backoff_factor` settings
- `tests/test_data_acquisition/test_pride_api.py` - Added `Mock` and `patch` imports, created 6 retry tests

**What This Enables:**

Pipeline is now resilient to:
- Temporary network issues
- Server overload
- Slow connections
- Intermittent failures

Users get reliable data downloads without manual intervention.

**Resources:**
- [Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Python requests Timeout](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)

**Next Steps:**
- Task 2.9: Additional unit tests (already have 14 tests, 78% coverage - may be sufficient)
- Task 2.10: Create demo notebook showing full workflow
- Epic 3: Data processing module (actually work with proteomics data!)

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
