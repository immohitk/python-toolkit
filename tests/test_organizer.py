import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from toolkit.organizer import (
    analyze_files, 
    get_file_category
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