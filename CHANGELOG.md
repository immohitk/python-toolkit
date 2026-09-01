# Changelog

All notable changes to this project will be documented in this file.

This project follows semantic versioning for incremental development.

---

## [v0.18.2] - 2026-09-01

### Added

- Added the PDF Splitter module foundation
- Added PDF splitting into individual page files
- Added predictable output file generation
- Added preservation of the original PDF file
- Added automated tests for PDF splitting

### Tested

- Individual PDF page splitting
- Multiple-page PDF splitting
- Generated PDF output validation
- Original PDF preservation
- Generated output path handling
- Full test suite: **69 tests passed**

---

## [v0.18.1] - 2026-09-01

### Added

- Added Duplicate Finder CLI dry-run support
- Added explicit dry-run confirmation that no files are modified
- Added automated testing for Duplicate Finder dry-run behavior
- Completed practical Duplicate Finder dry-run verification

### Tested

- Duplicate Finder dry-run CLI behavior
- Duplicate report generation during dry-run
- Dry-run file preservation
- Invalid directory handling
- Full test suite: **65 tests passed**

---

## [v0.18.0] - 2026-09-01

### Completed

- Completed the PDF Merger basic phase
- Added PDF merger CLI command
- Added PDF merger CLI dry-run support
- Added CLI validation error handling
- Verified multiple PDF input handling
- Verified selected input order preservation
- Verified page order preservation
- Verified merged output creation
- Verified original input PDF preservation
- Completed practical CLI verification

### Tested

- PDF merger unit tests
- PDF merger CLI tests
- Multiple PDF merging
- Input validation
- Selected input ordering
- Page ordering
- Output creation
- Source file preservation
- CLI dry-run behavior
- CLI validation error handling
- Practical merging using real PDF files
- Full test suite: **64 tests passed**

---

## [v0.17.5] - 2026-08-30

### Added

- Added verification for merged PDF output creation
- Verified that merged results are saved to the requested output path
- Verified that original input PDFs remain unchanged

### Tested

- Merged PDF output creation
- Output file existence verification
- Source PDF preservation
- Full test suite: **60 tests passed**

---

## [v0.17.4] - 2026-08-30

### Completed

- Implemented PDF merging in the selected input order
- Preserved page order within each input PDF
- Verified merged PDF page ordering
- Verified multiple PDF input ordering

### Tested

- PDF merging with multiple input files
- Selected input order preservation
- Page order preservation within individual PDFs
- Combined merged page ordering
- Full test suite: **59 tests passed**

---

## [v0.17.3] - 2026-08-30

### Added

- Added PDF merger input file validation
- Added validation for missing input file paths
- Added validation to reject directory inputs
- Added validation to reject non-PDF files
- Added clear error handling for invalid PDF merger inputs

### Tested

- Missing input file handling
- Directory input rejection
- Non-PDF file rejection
- Valid PDF merging after input validation
- Full test suite: **58 tests passed**

---

## [v0.17.2] - 2026-08-30

### Added

- Added automated verification for merging multiple PDF input files
- Added input order preservation testing
- Verified that PDF files are processed in the exact order provided

### Tested

- Merging multiple PDF files
- Preserving the exact input file order
- Creating merged PDFs from multiple input files
- Full test suite: **55 tests passed**

---

## [v0.17.1] - 2026-08-30

### Added

- Added the PDF Merger module foundation
- Added the `merge_pdf_files()` function
- Added support for merging multiple PDF files into a single output PDF
- Added the `pypdf` dependency
- Added an initial automated test for PDF merging

### Tested

- Merging multiple PDF files
- Preserving pages from all input PDF files
- Creating the merged output PDF
- Full test suite: **54 tests passed**

---

## [v0.17.0] - 2026-08-29

### Completed

- Completed the basic development phase of the Duplicate File Finder
- Reviewed meaningful duplicate detection edge cases
- Added missing empty directory coverage
- Verified directories with no duplicate files
- Verified duplicate file group detection
- Verified non-recursive duplicate scanning behavior
- Performed practical testing through the `duplicates` CLI command
- Confirmed duplicate analysis remains report-only and does not modify files

### Tested

- Empty directory handling
- Directories with no duplicate files
- Duplicate group detection
- Duplicate report generation
- Non-recursive directory scanning
- Duplicate File Finder CLI behavior
- Practical CLI testing
- Full test suite: **53 tests passed**

---

## [v0.16.5] - 2026-08-29

### Added

- Added the `duplicates` command for finding duplicate files from the command line
- Added CLI integration for duplicate file detection and report display
- Added automated tests for the Duplicate File Finder CLI command

### Improved

- Duplicate file analysis can now be accessed directly through the command line
- Duplicate detection remains report-only and does not delete or modify files
- Directories with no duplicate files display a clear user-friendly message

### Tested

- Duplicate file detection through the CLI
- Duplicate report display through the CLI
- Directories with no duplicate files
- Report-only behavior with files remaining unchanged
- Full test suite: **51 tests passed**

---

## [v0.16.4] - 2026-08-29

### Added

- Added a readable duplicate file report
- Added duplicate group display with clear group numbering
- Added duplicate file name and path display
- Added individual duplicate file size display
- Added duplicate group count reporting
- Added potential disk space savings reporting
- Added handling for directories with no duplicate files
- Added automated tests for duplicate report display

### Improved

- Duplicate detection results can now be reviewed in a clear, structured format
- Potentially recoverable space is displayed as part of the final report
- Empty duplicate results provide a simple user-friendly message

### Tested

- Duplicate report formatting
- Duplicate group numbering
- File name and path display
- Duplicate file size display
- Potential space savings reporting
- No-duplicate report handling
- Full test suite: 49 tests passed

---

## [v0.16.3] - 2026-08-29

### Added

- Added duplicate file size analysis
- Added calculation of potentially recoverable disk space
- Added support for calculating recoverable space across multiple duplicate groups
- Added automated tests for duplicate size analysis

### Improved

- Duplicate space calculation keeps one file from each duplicate group
- Only additional duplicate copies are counted as recoverable space
- Duplicate groups with different file sizes are handled correctly

### Tested

- Recoverable space calculation for a duplicate group
- Recoverable space calculation for multiple duplicate groups
- Duplicate groups containing different file sizes
- Full test suite: 46 tests passed

---

## [v0.16.2] - 2026-08-29

### Added

- Added duplicate file detection using SHA-256 file hashes
- Added scanning for files directly inside the selected directory
- Added grouping of files with identical content
- Added automated tests for duplicate file detection

### Improved

- Unique files are excluded from duplicate detection results
- Subdirectories are ignored during duplicate file scanning
- Reused the existing chunk-based file hashing functionality

### Tested

- Duplicate file grouping
- Unique file exclusion
- Subdirectory exclusion
- Practical duplicate detection with files containing identical content
- Full test suite: 44 tests passed

---

## [v0.16.1] - 2026-08-28

### Added

- Added the Duplicate File Finder module foundation
- Added SHA-256 file hashing for duplicate detection
- Files are read in chunks to avoid loading entire files into memory
- Added automated unit tests for file hashing

### Tested

- SHA-256 hash generation for files
- Hash comparison against expected SHA-256 values
- Identical files producing identical hash values
- Full test suite: 41 tests passed

---

## [v0.16.0] - 2026-08-28

### Added

- Completed the File Cleaner basic feature phase
- Added validated cleanup confirmation input
- Cleanup now accepts `y` or `Y` to proceed
- Cleanup now accepts `n` or `N` to cancel
- Invalid confirmation input now asks the user again until a valid choice is entered

### Improved

- Improved overall File Cleaner reliability and safety
- Continued cleanup when individual files cannot be deleted
- Added clear reporting for successful and failed file removals
- Freed disk space is calculated using only successfully deleted files
- Defined cleanup as non-recursive to avoid modifying files inside subdirectories
- Improved edge-case test coverage and final File Cleaner behavior review

### Tested

- Cleanup confirmation and cancellation behavior
- Uppercase and lowercase confirmation input
- Invalid input retry behavior
- Cleanup deletion failure handling
- Continued cleanup after individual failures
- Non-recursive cleanup behavior
- Full test suite: 40 tests passed

---

## [v0.15.2] - 2026-08-28

### Improved

- Improved cleanup error handling during file deletion
- Cleanup continues when individual files cannot be deleted
- Added reporting for successfully removed and failed files
- Improved freed disk space reporting to count only successfully deleted files
- Clarified that cleanup only scans files directly inside the selected directory
- Added explicit non-recursive cleanup behavior documentation

### Tested

- Successful cleanup operations
- Cleanup deletion failure handling
- Continued cleanup after individual file deletion failures
- Removed and failed file reporting
- Freed disk space reporting after deletion failures
- Subdirectory cleanup exclusion
- Full test suite: 34 tests passed

---

## [v0.15.1] - 2026-08-28

### Added

- Cleanup confirmation prompt before file deletion

### Improved

- Added an extra safety step before cleanup operations permanently remove files

### Tested

- Cleanup confirmation behavior
- Full test suite: 32 tests passed

---

## [v0.15.0] - 2026-08-24

### Added

- New `clean` CLI command
- Cleanup preview support using `--dry-run`
- Automatic deletion of temporary, backup, and system-generated files
- Cleanup completion summary
- Freed disk space reporting
- Automated CLI tests for cleanup operations

### Improved

- Integrated the File Cleaner with the command-line interface
- Added safe cleanup preview without modifying files
- Improved access to cleanup functionality through the CLI

### Tested

- Cleanup command execution
- Cleanup dry-run behavior
- File deletion behavior
- Preservation of non-cleanup files
- CLI integration for cleanup commands
- Full test suite: 32 tests passed

### Next

- Additional CLI commands
- More comprehensive error handling

---

## [v0.14.0] - 2026-08-19

### Improved

- Improved empty directory analysis
- Added a clear message when no files are found during analysis

### Tested

- Empty directory analysis
- Unknown file type handling
- Already-organized directory behavior
- Dry-run conflict handling
- Full test suite: 18 tests passed

### Next

- Additional CLI commands
- More comprehensive error handling

---

## [v0.13.0] - 2026-08-19

### Improved

- Improved skipped file reporting during organization
- Added skipped file details to the organization summary
- Displayed skipped filenames, categories, and reasons

### Tested

- Skipped file reporting
- Multiple skipped files
- CLI organization output
- Full test suite: 17 tests passed

### Next

- Additional CLI commands
- More comprehensive error handling

---

## [v0.12.0] - 2026-08-19

### Improved

- Improved directory validation
- Added detection for paths that exist but are not directories
- Added user-friendly error handling for invalid directory paths
- Added CLI logging for directory validation errors

### Tested

- Nonexistent directory handling
- File path passed where a directory is expected
- CLI error handling for invalid directory paths
- Full test suite: 16 tests passed

### Next

- Additional CLI commands
- More comprehensive error handling

---

## [v0.11.0] - 2026-08-10

### Added

- New `info` CLI command
- Directory information summary
- Total file count and category counts

### Tested

- `info` command with valid directories
- CLI integration for the `info` command
- Full test suite: 14 tests passed

### Next

- Additional CLI commands
- More comprehensive error handling

---

## [v0.10.0] - 2026-08-10

### Added

- GitHub Actions CI/CD workflow
- Automated test execution on pushes to `main`
- Automated test execution for pull requests targeting `main`

### Improved

- Added continuous integration to automatically verify the test suite
- Added automated Python environment setup for CI

### Tested

- GitHub Actions workflow
- Automated execution of the pytest test suite
- Existing organizer and CLI functionality

### Next

- Additional CLI commands
- More comprehensive error handling

---

## [v0.9.0] - 2026-08-09

### Added

- Application logging module
- Logging for file movements
- Logging for skipped duplicate files
- Logging for directory analysis
- CLI error logging
- Automated tests for logging behavior

### Improved

- Added structured logging for important application events
- Improved CLI error diagnostics
- Kept generated log files out of version control

### Tested

- Successful file movement logging
- Skipped-file logging
- Analysis logging
- Invalid-directory CLI logging
- Existing organizer functionality

---

## [v0.8.0] - 2026-08-08

### Added

- Centralized configuration module
- Moved file category definitions into `toolkit/config.py`
- Automated test for configuration categories

### Improved

- Separated configuration from file-organizing logic
- Improved project modularity and maintainability

### Tested

- File category configuration
- File categorization
- Existing organizer functionality
- Automated tests with pytest

---

## [v0.7.0] - 2026-08-08

### Added

- `--dry-run` option for the `organize` command
- Automated test for dry-run behavior

### Improved

- Added a safe preview mode that shows planned file movements
- Dry-run mode prevents file movement and category folder creation

---

## [v0.6.0] - 2026-08-08

### Added

- CLI error handling for invalid directories
- Automated test for invalid directory handling

### Improved

- Replaced the full Python traceback with a user-friendly error message
- Improved CLI behavior for invalid directory paths

---

## [v0.5.0] - 2026-08-08

### Added

- `analyze` CLI command
- File analysis summary
- Automated test for file analysis

### Improved

- Extended CLI with directory analysis
- Reused existing file categorization logic

---

## [v0.4.0] - 2026-08-06

### Added

- CLI `organize` command
- Directory argument support
- Automatic help display when no command is provided

### Improved

- Integrated the CLI with the File Organizer
- Removed the need for temporary test scripts
- Improved command-line user experience

### Tested

- CLI command execution
- File organization workflow
- Duplicate file protection
- Automated unit tests with pytest

---

## [v0.3.0] - 2026-08-06

### Added

- Automated unit tests with pytest
- Type hints for all public functions
- Function docstrings

### Improved

- Better code organization
- Cleaner project structure
- Improved code readability and maintainability

### Tested

- File category detection
- Unknown file handling
- Multiple file type validation

---

## [v0.2.3] - 2026-08-06

### Added

- Automatic file movement into category folders
- Duplicate file protection
- Organization summary after completion

### Implemented

- `move_files()`

### Improved

- Prevents overwriting existing files
- Safe file organization workflow
- Better execution feedback with moved/skipped counters

---

## [v0.2.1] - 2026-08-06

### Added

- Automatic detection of required file categories
- Automatic creation of category folders

### Implemented

- `get_required_categories()`
- `create_category_folders()`

### Improved

- Reused existing helper functions to reduce duplicate code
- Folder creation now uses `exist_ok=True` to safely handle existing folders

---

## [v0.2.0] - 2026-08-05

### Added

- File Organizer module
- File extension categorization
- Directory file discovery using `pathlib`
- File analysis workflow
- Support for:
  - Images
  - Documents
  - Videos
  - Audio
  - Archives
  - Others

### Implemented

- `get_file_category()`
- `get_files()`
- `analyze_files()`

### Improved

- Refactored file retrieval to return `Path` objects
- Improved modular architecture
- Added directory validation
- Improved code readability

---

## [v0.1.1] - 2026-08-05

### Added

- CLI foundation using `argparse`
- Project entry point (`main.py`)
- `--help` command
- `--version` command

---

## [v0.1.0] - 2026-08-05

### Added

- Initial project structure
- Git repository
- MIT License
- README
- Project folders
- `.gitignore`