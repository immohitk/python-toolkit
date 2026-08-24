"""
File Cleaner Module.

This module contains functionality for identifying
files that may be suitable for cleanup.
"""

from toolkit.config import CLEANUP_EXTENSIONS, CLEANUP_FILENAMES

def get_cleanup_category(filename):
    """
    Return the cleanup category for a filename.

    Returns None if the file is not a cleanup candidate.
    """
    for category, extensions in CLEANUP_EXTENSIONS.items():
        if any(filename.endswith(extension) for extension in extensions):
            return category

    for category, filenames in CLEANUP_FILENAMES.items():
        if filename in filenames:
            return category

    return None

def get_file_size(file):
    """
    Return the size of a file in bytes.
    """
    return file.stat().st_size

def format_file_size(size):
    """
    Return a human-readable file size.
    """
    if size < 1024:
        return f"{size} bytes"

    if size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"

    return f"{size / (1024 * 1024):.2f} MB"

def get_total_cleanup_size(directory):
    """
    Return the total size of all cleanup candidates in bytes.
    """
    candidates = find_cleanup_candidates(directory)

    return sum(size for _, _, size in candidates)

def find_cleanup_candidates(directory):
    """
    Find files in a directory that are cleanup candidates.
    """
    candidates = []

    for file in sorted(directory.iterdir()):
        if not file.is_file():
            continue

        category = get_cleanup_category(file.name)

        if category is not None:
            size = get_file_size(file)
            candidates.append((file, category, size))

    return candidates

def show_cleanup_candidates(directory):
    """
    Display cleanup candidates found in a directory.
    """
    candidates = find_cleanup_candidates(directory)

    if not candidates:
        print("No cleanup candidates found.")
        return

    print("Cleanup Candidates")
    print("-" * 25)

    for file, category, size in candidates:
        formatted_size = format_file_size(size)
        print(f"{file.name:<30} -> {category} ({formatted_size})")

    total_size = get_total_cleanup_size(directory)
    formatted_total_size = format_file_size(total_size)

    print()
    print(f"Total cleanup size: {formatted_total_size}")
