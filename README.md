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