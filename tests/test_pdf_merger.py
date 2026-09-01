import pytest

from pypdf import PdfReader, PdfWriter

from toolkit.pdf_merger import merge_pdf_files


def create_pdf(file_path, page_count, width, height):
    """Create a PDF with blank pages of the requested size."""

    writer = PdfWriter()

    for _ in range(page_count):
        writer.add_blank_page(
            width=width,
            height=height,
        )

    with file_path.open("wb") as file:
        writer.write(file)


def test_merge_pdf_files(tmp_path):
    first_file = tmp_path / "first.pdf"
    second_file = tmp_path / "second.pdf"
    output_file = tmp_path / "merged.pdf"

    create_pdf(first_file, 2, 200, 200)
    create_pdf(second_file, 3, 300, 300)

    merge_pdf_files(
        [first_file, second_file],
        output_file,
    )

    reader = PdfReader(output_file)

    assert output_file.exists()
    assert len(reader.pages) == 5


def test_merge_pdf_files_preserves_input_order(tmp_path):
    first_file = tmp_path / "first.pdf"
    second_file = tmp_path / "second.pdf"
    third_file = tmp_path / "third.pdf"
    output_file = tmp_path / "merged.pdf"

    create_pdf(first_file, 1, 100, 100)
    create_pdf(second_file, 1, 200, 200)
    create_pdf(third_file, 1, 300, 300)

    merge_pdf_files(
        [
            first_file,
            second_file,
            third_file,
        ],
        output_file,
    )

    reader = PdfReader(output_file)

    assert len(reader.pages) == 3

    assert reader.pages[0].mediabox.width == 100
    assert reader.pages[1].mediabox.width == 200
    assert reader.pages[2].mediabox.width == 300

def test_merge_pdf_files_preserves_page_order(tmp_path):
    first_file = tmp_path / "first.pdf"
    second_file = tmp_path / "second.pdf"
    output_file = tmp_path / "merged.pdf"

    create_pdf(first_file, 2, 100, 100)
    create_pdf(second_file, 3, 200, 200)

    merge_pdf_files(
        [first_file, second_file],
        output_file,
    )

    reader = PdfReader(output_file)

    assert len(reader.pages) == 5

    assert reader.pages[0].mediabox.width == 100
    assert reader.pages[1].mediabox.width == 100
    assert reader.pages[2].mediabox.width == 200
    assert reader.pages[3].mediabox.width == 200
    assert reader.pages[4].mediabox.width == 200

def test_merge_pdf_files_rejects_missing_file(tmp_path):
    missing_file = tmp_path / "missing.pdf"
    output_file = tmp_path / "merged.pdf"

    with pytest.raises(FileNotFoundError):
        merge_pdf_files(
            [missing_file],
            output_file,
        )

def test_merge_pdf_files_rejects_directory(tmp_path):
    input_directory = tmp_path / "pdfs"
    input_directory.mkdir()

    output_file = tmp_path / "merged.pdf"

    with pytest.raises(ValueError):
        merge_pdf_files(
            [input_directory],
            output_file,
        )

def test_merge_pdf_files_rejects_non_pdf_file(tmp_path):
    input_file = tmp_path / "document.txt"
    output_file = tmp_path / "merged.pdf"

    input_file.write_text("Not a PDF file")

    with pytest.raises(ValueError):
        merge_pdf_files(
            [input_file],
            output_file,
        )

