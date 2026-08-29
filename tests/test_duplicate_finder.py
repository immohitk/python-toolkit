from hashlib import sha256

from toolkit.duplicate_finder import (
    find_duplicate_files,
    get_file_hash,
)


def test_get_file_hash(tmp_path):
    test_file = tmp_path / "test.txt"
    content = b"Hello, duplicate file finder!"

    test_file.write_bytes(content)

    expected_hash = sha256(content).hexdigest()

    assert get_file_hash(test_file) == expected_hash

def test_find_duplicate_files(tmp_path):
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"
    unique_file = tmp_path / "unique.txt"

    first_file.write_text("Same content")
    second_file.write_text("Same content")
    unique_file.write_text("Different content")

    duplicates = find_duplicate_files(tmp_path)

    assert duplicates == [
        [first_file, second_file],
    ]


def test_find_duplicate_files_ignores_unique_files(tmp_path):
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"

    first_file.write_text("First file")
    second_file.write_text("Second file")

    duplicates = find_duplicate_files(tmp_path)

    assert duplicates == []


def test_find_duplicate_files_ignores_subdirectories(tmp_path):
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"

    first_file.write_text("Same content")
    second_file.write_text("Same content")

    subdirectory = tmp_path / "subfolder"
    subdirectory.mkdir()

    nested_file = subdirectory / "nested.txt"
    nested_file.write_text("Same content")

    duplicates = find_duplicate_files(tmp_path)

    assert duplicates == [
        [first_file, second_file],
    ]

    assert nested_file.exists()
