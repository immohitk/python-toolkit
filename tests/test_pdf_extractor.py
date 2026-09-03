from pypdf import PdfReader, PdfWriter

from toolkit.pdf_extractor import extract_pdf_pages


def create_test_pdf(path, page_count):
    writer = PdfWriter()

    for _ in range(page_count):
        writer.add_blank_page(width=200, height=200)

    with path.open("wb") as file:
        writer.write(file)


def test_extract_pdf_pages(tmp_path):
    input_file = tmp_path / "input.pdf"
    output_file = tmp_path / "output.pdf"

    create_test_pdf(input_file, 5)

    extract_pdf_pages(
        input_file,
        output_file,
        [1, 3, 4],
    )

    assert output_file.exists()

    reader = PdfReader(output_file)

    assert len(reader.pages) == 3


def test_extract_pdf_pages_preserves_input(tmp_path):
    input_file = tmp_path / "input.pdf"
    output_file = tmp_path / "output.pdf"

    create_test_pdf(input_file, 5)

    original_size = input_file.stat().st_size

    extract_pdf_pages(
        input_file,
        output_file,
        [0, 2],
    )

    assert input_file.exists()
    assert input_file.stat().st_size == original_size


def test_extract_pdf_pages_preserves_selected_order(tmp_path):
    input_file = tmp_path / "input.pdf"
    output_file = tmp_path / "output.pdf"

    create_test_pdf(input_file, 5)

    extract_pdf_pages(
        input_file,
        output_file,
        [3, 1, 4],
    )

    reader = PdfReader(output_file)

    assert len(reader.pages) == 3
