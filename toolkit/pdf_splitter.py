from pathlib import Path

from pypdf import PdfReader, PdfWriter


def split_pdf(input_file, output_directory):
    """
    Split a PDF into individual one-page PDF files.

    The original PDF is preserved.
    """
    input_file = Path(input_file)
    output_directory = Path(output_directory)

    reader = PdfReader(input_file)
    output_directory.mkdir(parents=True, exist_ok=True)

    generated_files = []

    for page_number, page in enumerate(reader.pages, start=1):
        output_file = (
            output_directory
            / f"{input_file.stem}_page_{page_number}.pdf"
        )

        writer = PdfWriter()
        writer.add_page(page)

        with output_file.open("wb") as file:
            writer.write(file)

        generated_files.append(output_file)

    return generated_files