import sys
import pytest
from pathlib import Path

from toolkit.config import FILE_CATEGORIES

sys.path.append(str(Path(__file__).resolve().parents[1]))

from toolkit.organizer import (
    analyze_files, 
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

def test_get_files_invalid_directory():
    with pytest.raises(FileNotFoundError):
        get_files("C:/does/not/exist")

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