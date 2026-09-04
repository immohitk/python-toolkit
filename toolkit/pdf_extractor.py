from pathlib import Path

from pypdf import PdfReader, PdfWriter


def parse_page_selection(selection):
    """
    Convert a user page selection into zero-based page indexes.
    """
    if not selection or not selection.strip():
        raise ValueError("Page selection cannot be empty.")

    selection = selection.strip()

    if "-" in selection:
        parts = selection.split("-")

        if len(parts) != 2:
            raise ValueError("Invalid page range.")

        start, end = parts

        if not start.isdigit() or not end.isdigit():
            raise ValueError("Page selection must contain numbers.")

        start = int(start)
        end = int(end)

        if start < 1 or end < 1:
            raise ValueError("Page numbers must be at least 1.")

        if start > end:
            raise ValueError("Page range cannot be reversed.")

        return list(range(start - 1, end))

    if not selection.isdigit():
        raise ValueError("Page selection must contain a number.")

    page = int(selection)

    if page < 1:
        raise ValueError("Page numbers must be at least 1.")

    return [page - 1]


def validate_page_selection(page_numbers, page_count):
    """
    Validate zero-based page indexes against the PDF page count.
    """
    if not page_numbers:
        raise ValueError("Page selection cannot be empty.")

    for page_number in page_numbers:
        if page_number < 0:
            raise ValueError("Page numbers must be at least 1.")

        if page_number >= page_count:
            raise ValueError("Page selection is out of range.")


def extract_pdf_pages(input_file, output_file, page_numbers):
    """
    Extract selected pages from a PDF into a new PDF.
    """
    input_file = Path(input_file)
    output_file = Path(output_file)

    reader = PdfReader(input_file)

    validate_page_selection(page_numbers, len(reader.pages))

    writer = PdfWriter()

    for page_number in page_numbers:
        writer.add_page(reader.pages[page_number])

    with output_file.open("wb") as file:
        writer.write(file)
