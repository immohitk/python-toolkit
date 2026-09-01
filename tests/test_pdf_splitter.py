from pypdf import PdfReader, PdfWriter

from toolkit.pdf_splitter import split_pdf


def create_test_pdf(file_path, page_count):
    writer = PdfWriter()

    for _ in range(page_count):
        writer.add_blank_page(width=612, height=792)

    with file_path.open("wb") as file:
        writer.write(file)


def test_split_pdf_creates_one_file_per_page(tmp_path):
    input_file = tmp_path / "sample.pdf"
    output_directory = tmp_path / "split"

    create_test_pdf(input_file, 3)

    generated_files = split_pdf(
        input_file,
        output_directory,
    )

    assert len(generated_files) == 3

    for file_number, output_file in enumerate(
        generated_files,
        start=1,
    ):
        assert output_file.exists()
        assert output_file.name == f"sample_page_{file_number}.pdf"


def test_split_pdf_outputs_contain_one_page_each(tmp_path):
    input_file = tmp_path / "sample.pdf"
    output_directory = tmp_path / "split"

    create_test_pdf(input_file, 3)

    generated_files = split_pdf(
        input_file,
        output_directory,
    )

    for output_file in generated_files:
        reader = PdfReader(output_file)

        assert len(reader.pages) == 1


def test_split_pdf_preserves_original_file(tmp_path):
    input_file = tmp_path / "sample.pdf"
    output_directory = tmp_path / "split"

    create_test_pdf(input_file, 3)

    original_size = input_file.stat().st_size

    split_pdf(
        input_file,
        output_directory,
    )

    assert input_file.exists()
    assert input_file.stat().st_size == original_size


def test_split_pdf_returns_generated_paths(tmp_path):
    input_file = tmp_path / "sample.pdf"
    output_directory = tmp_path / "split"

    create_test_pdf(input_file, 2)

    generated_files = split_pdf(
        input_file,
        output_directory,
    )

    assert generated_files == [
        output_directory / "sample_page_1.pdf",
        output_directory / "sample_page_2.pdf",
    ]