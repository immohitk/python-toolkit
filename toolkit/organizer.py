"""
File Organizer Module

This module contains functionality for categorizing
and organizing files.
"""

from pathlib import Path
import shutil

from toolkit.config import FILE_CATEGORIES
from toolkit.logger import get_logger

logger = get_logger()


# ============================
# File Analysis
# ============================


# Determine the category of a file

def get_file_category(extension):
    
    """Return the category for a file extension."""
    
    extension = extension.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"

    """Return the category for a file extension."""


# Read all files from a directory

def get_files(directory):
    folder = Path(directory)

    if not folder.exists():
        raise FileNotFoundError(
            f"Directory '{directory}' does not exist."
        )

    files = []

    for item in folder.iterdir():
        if item.is_file():
            files.append(item)

    return files

    """Return all files in the specified directory."""
    

# Analyze files in a directory

def analyze_files(directory):
    """
    Display files and category summary for a directory.
    """
    files = get_files(directory)
    category_counts = {}

    logger.info(
        "Analyzing directory '%s'",
        directory,
    )

    for file in files:
        category = get_file_category(file.suffix)

        print(f"{file.name:<30} -> {category}")

        category_counts[category] = category_counts.get(category, 0) + 1

    print("\nAnalysis Complete")
    print("-" * 17)

    for category, count in category_counts.items():
        print(f"{category:<10}: {count}")

    logger.info(
        "Analysis completed for '%s'",
        directory,
    )

# Get directory information

def get_directory_info(directory):
    """Display a quick summary of files in a directory."""
    files = get_files(directory)
    category_counts = {}

    for file in files:
        category = get_file_category(file.suffix)
        category_counts[category] = category_counts.get(category, 0) + 1

    print(f"Directory: {directory}")
    print()
    print(f"Total files: {len(files)}")

    for category, count in category_counts.items():
        print(f"{category:<10}: {count}")

# ============================
# Folder Management
# ============================


# Get required categories

def get_required_categories(directory):
    categories = set()
    files = get_files(directory)

    for file in files:
        extension = file.suffix
        category = get_file_category(extension)
        categories.add(category)

    return categories

    """Return the unique categories found in a directory."""

# Create category folders

def create_category_folders(directory):
    folder = Path(directory)
    categories = get_required_categories(directory)

    for category in categories:
        (folder / category).mkdir(exist_ok=True)

        """Create category folders if they do not exist."""

# ============================
# File Operations
# ============================


# Move files safely

def move_files(directory, dry_run=False):
    """Move files into their category folders safely."""

    folder = Path(directory)
    files = get_files(directory)

    moved = 0
    skipped = 0

    if dry_run:
        print("Dry Run - No files will be moved")
        print("-" * 35)

    for file in files:
        category = get_file_category(file.suffix)
        destination = folder / category / file.name

        if destination.exists():
            print(f"Skipped: {file.name} (already exists)")
            skipped += 1

            logger.info(
                "Skipped '%s' because destination already exists",
                file.name,
            )

            continue

        if dry_run:
            print(f"{file.name:<30} -> {category}")
            continue

        shutil.move(file, destination)
        moved += 1

        logger.info(
            "Moved '%s' to '%s'",
            file.name,
            category,
        )

    if dry_run:
        print("\nNo files were moved.")
        return

    print("\nOrganization Complete")
    print("-" * 25)
    print(f"Moved   : {moved}")
    print(f"Skipped : {skipped}")