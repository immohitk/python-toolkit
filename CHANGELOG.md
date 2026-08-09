# Changelog

All notable changes to this project will be documented in this file.

This project follows semantic versioning for incremental development.

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