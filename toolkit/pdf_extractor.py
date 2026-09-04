from pathlib import Path

from pypdf import PdfReader, PdfWriter


def parse_page_selection(selection):
    """
    Convert a user page selection into zero-based page indexes.
    """
    if "-" in selection:
        start, end = selection.split("-", 1)

        start = int(start)
        end = int(end)

        return list(range(start - 1, end))

    page = int(selection)

    return [page - 1]


def extract_pdf_pages(input_file, output_file, page_numbers):
    """
    Extract selected pages from a PDF into a new PDF.
    """
    input_file = Path(input_file)
    output_file = Path(output_file)

    reader = PdfReader(input_file)
    writer = PdfWriter()

    for page_number in page_numbers:
        writer.add_page(reader.pages[page_number])

    with output_file.open("wb") as file:
        writer.write(file)
