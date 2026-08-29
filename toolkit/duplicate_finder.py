from hashlib import sha256
from pathlib import Path


def get_file_hash(file_path):
    """
    Generate a SHA-256 hash for a file.

    The file is read in chunks to avoid loading the entire
    file into memory.
    """
    file_hash = sha256()

    with Path(file_path).open("rb") as file:
        while chunk := file.read(8192):
            file_hash.update(chunk)

    return file_hash.hexdigest()


def find_duplicate_files(directory):
    """
    Find groups of files with identical content.

    Only files directly inside the selected directory
    are scanned. Subdirectories are ignored.
    """
    directory = Path(directory)
    file_hashes = {}

    for file_path in directory.iterdir():
        if not file_path.is_file():
            continue

        file_hash = get_file_hash(file_path)

        if file_hash not in file_hashes:
            file_hashes[file_hash] = []

        file_hashes[file_hash].append(file_path)

    return [
        files
        for files in file_hashes.values()
        if len(files) > 1
    ]


def get_duplicate_space(duplicate_groups):
    """
    Calculate the potentially recoverable space from duplicate files.

    One file from each duplicate group is kept, so only the
    remaining duplicate copies are counted as recoverable space.
    """
    recoverable_space = 0

    for group in duplicate_groups:
        if len(group) < 2:
            continue

        file_size = group[0].stat().st_size
        recoverable_space += (len(group) - 1) * file_size

    return recoverable_space
