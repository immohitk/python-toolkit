from pathlib import Path

from pypdf import PdfReader, PdfWriter


def merge_pdf_files(
    input_files: list[Path],
    output_file: Path,
) -> None:
    """Merge multiple PDF files into a single PDF file."""

    writer = PdfWriter()

    for input_file in input_files:
        reader = PdfReader(input_file)

        for page in reader.pages:
            writer.add_page(page)

    with output_file.open("wb") as file:
        writer.write(file)
