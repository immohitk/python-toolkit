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
- Calculate total cleanup size
- Display total cleanup size in human-readable format
- Handle directories with no cleanup candidates

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

**v0.14.0**

---

## License

This project is licensed under the MIT License.