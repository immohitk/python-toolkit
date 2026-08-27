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

def get_cleanup_summary(directory):
    """
    Return a summary of cleanup candidates grouped by category.
    """
    summary = {}

    candidates = find_cleanup_candidates(directory)

    for _, category, size in candidates:
        if category not in summary:
            summary[category] = {
                "count": 0,
                "size": 0,
            }

        summary[category]["count"] += 1
        summary[category]["size"] += size

    return summary

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

    summary = get_cleanup_summary(directory)

    print()
    print("Cleanup Summary")
    print("-" * 25)

    for category, details in summary.items():
        count = details["count"]
        size = details["size"]
        formatted_size = format_file_size(size)

        file_word = "file" if count == 1 else "files"

        print(
            f"{category}: {count} {file_word} ({formatted_size})"
        )

    total_size = get_total_cleanup_size(directory)
    formatted_total_size = format_file_size(total_size)

    print()
    print(f"Total cleanup size: {formatted_total_size}")

def preview_cleanup(directory):
    """
    Display a preview of files that would be cleaned.

    This function does not modify or delete any files.
    """
    candidates = find_cleanup_candidates(directory)

    if not candidates:
        print("No cleanup candidates found.")
        return

    print("Cleanup Preview")
    print("-" * 25)

    for file, category, size in candidates:
        formatted_size = format_file_size(size)
        print(f"{file.name:<30} -> {category} ({formatted_size})")

    total_size = get_total_cleanup_size(directory)
    formatted_total_size = format_file_size(total_size)

    print()
    print(f"Total cleanup size: {formatted_total_size}")

def confirm_cleanup():
    """
    Ask the user to confirm cleanup.

    Returns True if cleanup is confirmed.
    """
    response = input("Proceed with cleanup? [y/N]: ")

    return response.lower() == "y"

def clean_files(directory):
    """
    Delete all cleanup candidate files in a directory.
    """
    candidates = find_cleanup_candidates(directory)

    if not candidates:
        print("No cleanup candidates found.")
        return

    preview_cleanup(directory)

    print()

    if not confirm_cleanup():
        print("Cleanup cancelled.")
        return

    print()
    print("Cleanup Complete")
    print("-" * 25)

    total_size = 0

    for file, _, size in candidates:
        file.unlink()

        formatted_size = format_file_size(size)
        print(f"Removed: {file.name} ({formatted_size})")

        total_size += size

    formatted_total_size = format_file_size(total_size)

    print()
    print(f"Files removed: {len(candidates)}")
    print(f"Space freed: {formatted_total_size}")
