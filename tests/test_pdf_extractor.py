from pypdf import PdfReader, PdfWriter

from toolkit.pdf_extractor import extract_pdf_pages, parse_page_selection


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


def test_parse_page_selection_single_page():
    assert parse_page_selection("2") == [1]


def test_parse_page_selection_page_range():
    assert parse_page_selection("2-4") == [1, 2, 3]


def test_parse_page_selection_converts_single_page_to_zero_based():
    assert parse_page_selection("4") == [3]
