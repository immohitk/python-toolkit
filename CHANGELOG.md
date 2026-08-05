# Changelog

All notable changes to this project will be documented in this file.

This project follows semantic versioning for incremental development.

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