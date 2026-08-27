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
│   ├── logger.py
│   └── organizer.py
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
- No external dependencies

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

**v0.16.0**

---

## License

This project is licensed under the MIT License.