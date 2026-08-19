import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from toolkit.config import FILE_CATEGORIES
from toolkit.cli import run
from toolkit.organizer import (
    analyze_files,
    get_directory_info,
    get_file_category,
    get_files,
    move_files,
)

def test_get_file_category_pdf():
    assert get_file_category(".pdf") == "Documents"


def test_get_file_category_jpg():
    assert get_file_category(".jpg") == "Images"


def test_get_file_category_mp4():
    assert get_file_category(".mp4") == "Videos"


def test_get_file_category_unknown():
    assert get_file_category(".xyz") == "Others"
    
    
def test_analyze_files(tmp_path, capsys):
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "report.pdf").touch()

    analyze_files(tmp_path)

    output = capsys.readouterr().out

    assert "photo.jpg" in output
    assert "Images" in output
    assert "report.pdf" in output
    assert "Documents" in output

def test_get_directory_info(tmp_path, capsys):
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "report.pdf").touch()
    (tmp_path / "song.mp3").touch()

    get_directory_info(tmp_path)

    output = capsys.readouterr().out

    assert f"Directory: {tmp_path}" in output
    assert "Total files: 3" in output
    assert "Images    : 1" in output
    assert "Documents : 1" in output
    assert "Audio     : 1" in output

def test_get_files_invalid_directory():
    with pytest.raises(FileNotFoundError):
        get_files("C:/does/not/exist")

def test_get_files_file_path(tmp_path):
    file = tmp_path / "photo.jpg"
    file.touch()

    with pytest.raises(NotADirectoryError):
        get_files(file)

def test_move_files_dry_run(tmp_path, capsys):
    file = tmp_path / "photo.jpg"
    file.touch()

    move_files(tmp_path, dry_run=True)

    output = capsys.readouterr().out

    assert "Dry Run - No files will be moved" in output
    assert "photo.jpg" in output
    assert "Images" in output
    assert "No files were moved." in output
    assert file.exists()

def test_file_categories_configuration():
    assert ".jpg" in FILE_CATEGORIES["Images"]
    assert ".pdf" in FILE_CATEGORIES["Documents"]
    assert ".mp4" in FILE_CATEGORIES["Videos"]
    assert ".mp3" in FILE_CATEGORIES["Audio"]
    assert ".zip" in FILE_CATEGORIES["Archives"]

def test_move_files_logs_moved_file(tmp_path, caplog):
    file = tmp_path / "photo.jpg"
    file.touch()

    (tmp_path / "Images").mkdir()

    with caplog.at_level("INFO"):
        move_files(tmp_path)

    assert "Moved 'photo.jpg' to 'Images'" in caplog.text

def test_move_files_logs_skipped_file(tmp_path, caplog):
    file = tmp_path / "photo.jpg"
    file.touch()

    images_folder = tmp_path / "Images"
    images_folder.mkdir()

    existing_file = images_folder / "photo.jpg"
    existing_file.touch()

    with caplog.at_level("INFO"):
        move_files(tmp_path)

    assert "Skipped 'photo.jpg' because destination already exists" in caplog.text


def test_analyze_files_logs_activity(tmp_path, caplog):
    file = tmp_path / "photo.jpg"
    file.touch()

    with caplog.at_level("INFO"):
        analyze_files(tmp_path)

    assert f"Analyzing directory '{tmp_path}'" in caplog.text
    assert f"Analysis completed for '{tmp_path}'" in caplog.text

def test_cli_logs_invalid_directory(monkeypatch, caplog, capsys):
    directory = "C:/does/not/exist"

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "analyze", directory],
    )

    with caplog.at_level("ERROR"):
        run()

    output = capsys.readouterr().out

    assert f"Error: Directory '{directory}' does not exist." in output
    assert f"Directory '{directory}' does not exist." in caplog.text

def test_cli_logs_file_path(monkeypatch, tmp_path, caplog, capsys):
    file = tmp_path / "photo.jpg"
    file.touch()

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "info", str(file)],
    )

    with caplog.at_level("ERROR"):
        run()

    output = capsys.readouterr().out

    assert f"Error: Path '{file}' is not a directory." in output
    assert f"Path '{file}' is not a directory." in caplog.text

def test_cli_info(monkeypatch, tmp_path, capsys):
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "report.pdf").touch()

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "info", str(tmp_path)],
    )

    run()

    output = capsys.readouterr().out

    assert f"Directory: {tmp_path}" in output
    assert "Total files: 2" in output
    assert "Images    : 1" in output
    assert "Documents : 1" in output
