import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from toolkit.organizer import get_file_category


def test_get_file_category_pdf():
    assert get_file_category(".pdf") == "Documents"


def test_get_file_category_jpg():
    assert get_file_category(".jpg") == "Images"


def test_get_file_category_mp4():
    assert get_file_category(".mp4") == "Videos"


def test_get_file_category_unknown():
    assert get_file_category(".xyz") == "Others"