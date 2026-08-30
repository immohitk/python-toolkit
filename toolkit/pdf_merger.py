from pathlib import Path

from pypdf import PdfReader, PdfWriter


def validate_pdf_files(
    input_files: list[Path],
) -> None:
    """Validate PDF files before merging."""

    for input_file in input_files:
        if not input_file.exists():
            raise FileNotFoundError(
                f"Input file does not exist: {input_file}"
            )

        if not input_file.is_file():
            raise ValueError(
                f"Input path is not a file: {input_file}"
            )

        if input_file.suffix.lower() != ".pdf":
            raise ValueError(
                f"Input file is not a PDF: {input_file}"
            )


def merge_pdf_files(
    input_files: list[Path],
    output_file: Path,
) -> None:
    """Merge multiple PDF files into a single PDF file."""

    validate_pdf_files(input_files)

    writer = PdfWriter()

    for input_file in input_files:
        reader = PdfReader(input_file)

        for page in reader.pages:
            writer.add_page(page)

    with output_file.open("wb") as file:
        writer.write(file)
