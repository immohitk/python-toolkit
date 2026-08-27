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
