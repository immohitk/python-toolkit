"""
File Organizer Module

This module contains functionality for categorizing
and organizing files.
"""

from pathlib import Path
import shutil


FILE_CATEGORIES = {
    "Images": {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".svg",
        ".webp",
        ".tiff",
        ".ico",
    },
    "Documents": {
        ".pdf",
        ".docx",
        ".doc",
        ".txt",
        ".xlsx",
        ".xls",
        ".pptx",
        ".ppt",
        ".csv",
        ".odt",
        ".rtf",
    },
    "Videos": {
        ".mp4",
        ".mkv",
        ".avi",
        ".mov",
        ".wmv",
        ".flv",
        ".webm",
        ".m4v",
    },
    "Audio": {
        ".mp3",
        ".wav",
        ".aac",
        ".flac",
        ".ogg",
        ".m4a",
        ".wma",
    },
    "Archives": {
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
        ".bz2",
    },
}


def get_file_category(extension):
    extension = extension.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


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


def analyze_files(directory):
    files = get_files(directory)

    for file in files:
        extension = file.suffix
        category = get_file_category(extension)

        print(f"{file.name:<30} -> {category}")
        
        
def get_required_categories(directory):
    categories = set()
    files = get_files(directory)

    for file in files:
        extension = file.suffix
        category = get_file_category(extension)
        categories.add(category)

    return categories


def create_category_folders(directory):
    folder = Path(directory)
    categories = get_required_categories(directory)

    for category in categories:
        (folder / category).mkdir(exist_ok=True)


def move_files(directory):
    folder = Path(directory)
    files = get_files(directory)

    moved = 0
    skipped = 0

    for file in files:
        category = get_file_category(file.suffix)
        destination = folder / category / file.name

        if destination.exists():
            print(f"Skipped: {file.name} (already exists)")
            skipped += 1
            continue

        shutil.move(file, destination)
        moved += 1

    
    print("\nOrganization Complete")
    print("-" * 25)
    print(f"Moved   : {moved}")
    print(f"Skipped : {skipped}")