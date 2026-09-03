# Python Toolkit

A collection of practical Python utilities for file management, automation, and data processing.

> Built incrementally using software engineering principles such as modular design, single responsibility, code reviews, versioning, and Git best practices.

---

## Current Features

### CLI
- Command-line interface
- Help command
- Version command
- Organize command
- Analyze command
- Info command
- Dry-run mode
- Clean command
- Cleanup dry-run mode
- Duplicate file finder command

### File Organizer
- Analyze files in a directory
- Handle empty directories during analysis
- Categorize files by extension
- Detect required categories
- Create category folders automatically
- Move files into category folders
- Skip duplicate files safely
- Display organization summary
- Display skipped files with their category and reason

### File Cleaner

- Identify temporary files
- Identify backup files
- Identify system-generated files
- Scan directories for cleanup candidates
- Calculate cleanup candidate file sizes
- Format file sizes into human-readable units
- Display cleanup candidates with their categories and formatted sizes
- Display cleanup summary grouped by category
- Preview files that would be cleaned without modifying them
- Ask for confirmation before permanently deleting cleanup files
- Delete cleanup candidate files
- Display removed files and freed disk space
- Calculate total cleanup size
- Display total cleanup size in human-readable format
- Handle directories with no cleanup candidates
- Continue cleanup when an individual file cannot be deleted
- Display failed file removal reporting
- Calculate freed disk space using only successfully deleted files
- Clean files only directly inside the selected directory
- Do not scan subdirectories during cleanup
- Accept `y` or `Y` to confirm cleanup
- Accept `n` or `N` to cancel cleanup
- Reject invalid confirmation input and ask again

### Duplicate File Finder

- Generate SHA-256 hashes for files
- Read files safely in chunks for efficient hashing
- Scan files directly inside a selected directory
- Ignore subdirectories during duplicate scanning
- Compare file hashes to identify identical content
- Group files with identical content
- Exclude unique files from duplicate results
- Return duplicate file groups
- Calculate potentially recoverable disk space from duplicate files
- Keep one file from each duplicate group when calculating recoverable space
- Calculate recoverable space across multiple duplicate groups
- Handle duplicate groups with different file sizes
- Display duplicate groups in a readable report
- Show duplicate file names and full paths
- Display individual duplicate file sizes
- Show the total number of duplicate groups found
- Display potentially recoverable disk space
- Handle directories with no duplicate files
- Access duplicate file detection through the `duplicates` CLI command
- Display duplicate file reports directly from the command line
- Keep duplicate file analysis report-only
- Do not delete or modify files during duplicate scanning
- Duplicate Finder dry-run support
- Preview duplicate analysis without modifying files
- Explicit confirmation that no files are modified during dry-run

### PDF Merger

- PDF merging module foundation
- Merge multiple PDF files into a single PDF file
- Preserve pages from input PDF files
- Automated testing for PDF merging
- Accept multiple PDF input files
- Preserve the exact input file order during merging
- Automated testing for multiple PDF input order
- Validate that input file paths exist
- Reject directory paths as PDF inputs
- Validate PDF file extensions
- Clear handling for invalid merger inputs
- Automated testing for PDF input validation
- Merge PDFs in the selected input order
- Preserve page order within each input PDF
- Preserve combined page order in the merged PDF
- Automated testing for merged page ordering
- Create and save the merged PDF output
- Preserve original input PDF files
- Verify successful merged output creation
- Automated testing for output creation and source preservation
- PDF merger CLI command
- Merge multiple PDFs through the command line
- Specify the output PDF through the CLI
- PDF merger dry-run support
- Preview PDF merging without creating output
- CLI handling for invalid PDF inputs
- Practical CLI verification
- PDF Merger basic phase completed

### PDF Splitter

- PDF Splitter module foundation
- Split PDF files into individual pages
- Generate separate PDF files for each page
- Preserve original PDF files
- Predictable output file naming
- Automated testing for PDF splitting
- Select a single page to split
- Select a page range to split
- Validate page selections against the PDF page count
- PDF Splitter CLI command
- Specify a custom output directory
- Report generated output files
- PDF Splitter dry-run support
- Preview selected pages without creating output files
- Display files that would be generated during dry-run
- Explicit confirmation that no files are modified during dry-run

### PDF Page Extractor

- PDF Page Extractor module foundation
- Extract selected PDF pages into a new PDF file
- Preserve the original source PDF
- Preserve the selected page order
- Automated testing for PDF page extraction

### Code Quality

- Type hints
- Function docstrings
- Automated unit tests with pytest
- User-friendly CLI error handling
- Improved directory validation
- Application logging
- GitHub Actions CI/CD

---

## Project Structure

```text
python-toolkit/
│
├── main.py
├── toolkit/
│   ├── __init__.py
│   ├── cleaner.py
│   ├── cli.py
│   ├── config.py
│   ├── duplicate_finder.py
│   ├── logger.py
│   ├── organizer.py
│   ├── pdf_merger.py
│   ├── pdf_splitter.py
│   └── pdf_extractor.py
│
├── tests/
├── docs/
│
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

---

## Requirements

- Python 3.10+
- pypdf 6.16.2

---

## Usage

Display help

```bash
python main.py --help
```

Display version

```bash
python main.py --version
```

Organize a directory

```bash
python main.py organize "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder"
```

Analyze a directory

```bash
python main.py analyze "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder"
```

Get directory information

```bash
python main.py info "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder"
```

Preview organization without moving files

```bash
python main.py organize "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder" --dry-run
```

Clean a directory

```bash
python main.py clean "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder"
```

Preview cleanup without deleting files

```bash
python main.py clean "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder" --dry-run
```

Find duplicate files in a directory

```bash
python main.py duplicates "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder"
```

Preview duplicate file analysis without modifying files

```bash
python main.py duplicates "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder" --dry-run
```

Merge PDF files

```bash
python main.py merge "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder\first.pdf" "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder\second.pdf" -o "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder\merged.pdf"
```

Preview PDF merging without creating the output

```bash
python main.py merge "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder\first.pdf" "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder\second.pdf" -o "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder\merged.pdf" --dry-run
```

Split a PDF

```bash
python main.py split "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder\document.pdf"
```

Split selected pages

```bash
python main.py split "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder\document.pdf" --pages "2-4"
```

Split a single page

```bash
python main.py split "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder\document.pdf" --pages "2"
```

Specify a custom output directory

```bash
python main.py split "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder\document.pdf" -o "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder\split"
```

Preview a PDF split without creating output files

```bash
python main.py split "C:\Users\[YOUR SYSTEM NAME]\Desktop\TestFolder\document.pdf" --pages "2-4" --dry-run
```

---

## Current Development Status

### Completed

- CLI integration
- File categorization
- Directory analysis
- File cleanup category detection
- Cleanup candidate directory scanning
- Cleanup candidate display
- No-candidate handling
- Empty directory analysis handling
- Directory information command
- Category folder creation
- Safe file movement
- Duplicate protection
- Skipped file reporting
- Automated unit testing
- Modular project architecture
- CLI error handling for invalid directories
- Improved directory validation
- Dry-run file organization
- Centralized configuration module
- Application logging
- CLI error logging
- GitHub Actions CI/CD
- Cleanup candidate file size detection
- Cleanup candidate size display
- Total cleanup size calculation
- Total cleanup size display
- Human-readable file size formatting
- Human-readable total cleanup size display
- Cleanup summary grouped by category
- Cleanup candidate count and size summary
- Safe cleanup preview without file modification
- Cleanup candidate file deletion
- Cleanup file removal summary
- Freed disk space reporting
- CLI cleanup command
- Cleanup dry-run CLI support
- Cleanup confirmation before permanent file deletion
- Cleanup deletion failure handling
- Continued cleanup after individual file deletion failures
- Failed file removal reporting
- Accurate freed disk space reporting after deletion failures
- Non-recursive cleanup scope
- Subdirectory cleanup exclusion
- Cleanup confirmation input validation
- Uppercase and lowercase cleanup confirmation support
- Invalid confirmation input retry handling
- Final File Cleaner basic-phase testing and polish
- File Cleaner basic phase completion
- Duplicate File Finder module foundation
- SHA-256 file hashing
- Chunk-based file hashing
- Automated testing for file hashing
- Duplicate file detection
- Direct directory file scanning for duplicate detection
- SHA-256 hash comparison for duplicate detection
- Duplicate file grouping
- Unique file exclusion from duplicate results
- Non-recursive duplicate scanning
- Subdirectory exclusion during duplicate detection
- Automated duplicate detection testing
- Duplicate file size analysis
- Potentially recoverable duplicate space calculation
- Recoverable space calculation across multiple duplicate groups
- Duplicate groups with different file sizes handling
- Automated duplicate size analysis testing
- Duplicate file report display
- Duplicate group report formatting
- Duplicate file name and path display
- Duplicate file size display
- Duplicate group count display
- Potential duplicate space savings display
- No-duplicate report handling
- Automated duplicate report testing
- Duplicate File Finder CLI command
- CLI integration for duplicate file detection
- Duplicate report display through the command line
- Report-only duplicate file analysis
- Duplicate CLI testing
- Final Duplicate File Finder edge-case testing
- Empty directory handling verification
- Directories with no duplicate files verification
- Duplicate group detection verification
- Non-recursive duplicate scanning verification
- Practical Duplicate File Finder CLI testing
- Duplicate File Finder basic phase completion
- Duplicate Finder dry-run support
- Duplicate Finder CLI dry-run testing
- Practical Duplicate Finder dry-run verification
- PDF Merger module foundation
- PDF merging function structure
- PDF page merging using pypdf
- Automated PDF merging test
- Initial external dependency management with requirements.txt
- Multiple PDF input support
- PDF input order preservation
- Automated multiple PDF input testing
- PDF merger input file validation
- Missing PDF input file validation
- Directory input rejection for PDF merging
- Non-PDF input rejection
- Automated PDF merger input validation testing
- PDF merging in selected input order
- PDF page order preservation
- Automated merged page ordering testing
- Merged PDF output creation
- Source PDF preservation during merging
- Automated PDF output creation testing
- PDF merger CLI command
- PDF merger CLI integration
- PDF merger dry-run support
- PDF merger CLI testing
- PDF merger CLI validation error handling
- Practical PDF merger CLI verification
- PDF Merger basic phase completion
- PDF Splitter module foundation
- PDF splitting into individual pages
- PDF Splitter output generation
- PDF Splitter source PDF preservation
- Automated PDF Splitter testing
- PDF Splitter core phase completion
- PDF Splitter page selection
- PDF Splitter page selection validation
- PDF Splitter CLI command
- PDF Splitter custom output directory support
- PDF Splitter generated-file reporting
- PDF Splitter dry-run support
- PDF Splitter CLI testing
- PDF Splitter practical CLI verification
- PDF Splitter invalid page selection verification
- PDF Splitter dry-run source preservation verification
- PDF Splitter basic phase completion
- PDF Page Extractor module foundation
- PDF page extraction into a new PDF
- PDF Page Extractor source PDF preservation
- PDF Page Extractor selected page order preservation
- Automated PDF Page Extractor testing

### Future Improvements

- Additional CLI commands
- More comprehensive error handling

### Future Tools

- Additional independent utility tools
- Unified GUI application combining toolkit utilities
- Desktop application packaging and installation

---

## Version

Current Version:

**v0.19.1**

---

## License

This project is licensed under the MIT License.