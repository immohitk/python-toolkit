from pypdf import PdfReader, PdfWriter

from toolkit.pdf_merger import merge_pdf_files


def create_pdf(file_path, page_count):
    """Create a simple PDF with the requested number of blank pages."""

    writer = PdfWriter()

    for _ in range(page_count):
        writer.add_blank_page(width=200, height=200)

    with file_path.open("wb") as file:
        writer.write(file)


def test_merge_pdf_files(tmp_path):
    first_file = tmp_path / "first.pdf"
    second_file = tmp_path / "second.pdf"
    output_file = tmp_path / "merged.pdf"

    create_pdf(first_file, 2)
    create_pdf(second_file, 3)

    merge_pdf_files(
        [first_file, second_file],
        output_file,
    )

    reader = PdfReader(output_file)

    assert output_file.exists()
    assert len(reader.pages) == 5
