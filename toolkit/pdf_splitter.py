from pathlib import Path

from pypdf import PdfReader, PdfWriter


def get_page_numbers(page_selection, total_pages):
    """
    Parse and validate a page selection.

    Page numbers are one-based for user input and converted
    to zero-based indexes for internal PDF processing.
    """
    if not isinstance(page_selection, str):
        raise ValueError("Page selection must be a string.")

    page_selection = page_selection.strip()

    if not page_selection:
        raise ValueError("Page selection cannot be empty.")

    if "-" in page_selection:
        parts = page_selection.split("-")

        if len(parts) != 2:
            raise ValueError("Invalid page range.")

        start, end = parts

        if not start or not end:
            raise ValueError("Invalid page range.")

        if not start.isdigit() or not end.isdigit():
            raise ValueError("Invalid page range.")

        start = int(start)
        end = int(end)

        if start < 1 or end < 1:
            raise ValueError("Page numbers must be greater than zero.")

        if start > end:
            raise ValueError("Page range start cannot be greater than end.")

        if end > total_pages:
            raise ValueError(
                f"Page number exceeds PDF page count: {total_pages}"
            )

        return list(range(start - 1, end))

    if not page_selection.isdigit():
        raise ValueError("Invalid page selection.")

    page_number = int(page_selection)

    if page_number < 1:
        raise ValueError("Page numbers must be greater than zero.")

    if page_number > total_pages:
        raise ValueError(
            f"Page number exceeds PDF page count: {total_pages}"
        )

    return [page_number - 1]


def split_pdf(input_file, output_directory, page_selection=None):
    """
    Split a PDF into individual one-page PDF files.

    The original PDF is preserved.
    """
    input_file = Path(input_file)
    output_directory = Path(output_directory)

    reader = PdfReader(input_file)

    if page_selection is None:
        page_numbers = list(range(len(reader.pages)))
    else:
        page_numbers = get_page_numbers(
            page_selection,
            len(reader.pages),
        )

    output_directory.mkdir(parents=True, exist_ok=True)

    generated_files = []

    for page_number in page_numbers:
        page = reader.pages[page_number]
        output_page_number = page_number + 1

        output_file = (
            output_directory
            / f"{input_file.stem}_page_{output_page_number}.pdf"
        )

        writer = PdfWriter()
        writer.add_page(page)

        with output_file.open("wb") as file:
            writer.write(file)

        generated_files.append(output_file)

    return generated_files