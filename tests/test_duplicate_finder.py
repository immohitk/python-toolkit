from hashlib import sha256

from toolkit.duplicate_finder import (
    display_duplicate_report,
    find_duplicate_files,
    get_duplicate_space,
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


def test_find_duplicate_files_handles_empty_directory(tmp_path):
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


def test_get_duplicate_space(tmp_path):
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"
    third_file = tmp_path / "third.txt"

    first_file.write_text("Same content")
    second_file.write_text("Same content")
    third_file.write_text("Same content")

    duplicate_groups = [
        [first_file, second_file, third_file],
    ]

    expected_space = first_file.stat().st_size * 2

    assert get_duplicate_space(duplicate_groups) == expected_space


def test_get_duplicate_space_with_multiple_groups(tmp_path):
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"

    third_file = tmp_path / "third.txt"
    fourth_file = tmp_path / "fourth.txt"
    fifth_file = tmp_path / "fifth.txt"

    first_file.write_text("Short")
    second_file.write_text("Short")

    third_file.write_text("Different content")
    fourth_file.write_text("Different content")
    fifth_file.write_text("Different content")

    duplicate_groups = [
        [first_file, second_file],
        [third_file, fourth_file, fifth_file],
    ]

    expected_space = (
        first_file.stat().st_size
        + third_file.stat().st_size * 2
    )

    assert get_duplicate_space(duplicate_groups) == expected_space


def test_display_duplicate_report(tmp_path, capsys):
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"

    first_file.write_text("Same content")
    second_file.write_text("Same content")

    duplicate_groups = [
        [first_file, second_file],
    ]

    display_duplicate_report(duplicate_groups)

    output = capsys.readouterr().out

    assert "Duplicate File Report" in output
    assert "Duplicate Group 1" in output
    assert first_file.name in output
    assert second_file.name in output
    assert str(first_file) in output
    assert str(second_file) in output
    assert f"{first_file.stat().st_size} bytes" in output
    assert "Duplicate groups found: 1" in output


def test_display_duplicate_report_shows_space_savings(tmp_path, capsys):
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"

    first_file.write_text("Same content")
    second_file.write_text("Same content")

    duplicate_groups = [
        [first_file, second_file],
    ]

    expected_space = first_file.stat().st_size

    display_duplicate_report(duplicate_groups)

    output = capsys.readouterr().out

    assert f"Potential space savings: {expected_space} bytes" in output


def test_display_duplicate_report_handles_no_duplicates(capsys):
    display_duplicate_report([])

    output = capsys.readouterr().out

    assert output == "No duplicate files found.\n"
