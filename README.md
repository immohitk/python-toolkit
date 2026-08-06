# Python Toolkit

A collection of practical Python utilities for file management, automation, and data processing.

> Built incrementally using software engineering principles such as modular design, single responsibility, code reviews, versioning, and Git best practices.

---

## Current Features

### CLI Foundation
- Command-line interface
- Help and version commands

### File Organizer
- Analyze files in a directory
- Categorize files by extension
- Detect required categories
- Create category folders automatically
- Uses `pathlib` for file operations

---

## Project Structure

```text
python-toolkit/
│
├── main.py
├── toolkit/
│   ├── __init__.py
│   ├── cli.py
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

---

## Current Development Status

### Completed

- CLI foundation
- File categorization
- Directory analysis
- Modular project architecture

### In Progress

- Folder creation
- File moving
- Duplicate filename handling

### Planned

- Dry-run mode
- Summary report
- Automated tests with pytest
- Logging
- Configuration module
- GitHub Actions CI/CD

---

## Version

Current Version:

**v0.2.1**

---

## License

This project is licensed under the MIT License.