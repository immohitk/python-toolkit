from pypdf import PdfReader, PdfWriter

from toolkit.pdf_splitter import get_page_numbers, split_pdf


def create_test_pdf(file_path, page_count):
    writer = PdfWriter()

    for _ in range(page_count):
        writer.add_blank_page(width=612, height=792)

    with file_path.open("wb") as file:
        writer.write(file)


def test_get_page_numbers_single_page():
    assert get_page_numbers("3", 5) == [2]


def test_get_page_numbers_page_range():
    assert get_page_numbers("2-5", 5) == [1, 2, 3, 4]


def test_get_page_numbers_full_document_range():
    assert get_page_numbers("1-5", 5) == [0, 1, 2, 3, 4]


def test_get_page_numbers_rejects_zero():
    try:
        get_page_numbers("0", 5)
    except ValueError as error:
        assert str(error) == "Page numbers must be greater than zero."
    else:
        raise AssertionError("Expected ValueError")


def test_get_page_numbers_rejects_out_of_range():
    try:
        get_page_numbers("6", 5)
    except ValueError as error:
        assert str(error) == "Page number exceeds PDF page count: 5"
    else:
        raise AssertionError("Expected ValueError")


def test_get_page_numbers_rejects_reversed_range():
    try:
        get_page_numbers("5-2", 5)
    except ValueError as error:
        assert str(error) == "Page range start cannot be greater than end."
    else:
        raise AssertionError("Expected ValueError")


def test_get_page_numbers_rejects_invalid_selection():
    try:
        get_page_numbers("abc", 5)
    except ValueError as error:
        assert str(error) == "Invalid page selection."
    else:
        raise AssertionError("Expected ValueError")


def test_get_page_numbers_rejects_invalid_range():
    try:
        get_page_numbers("2-", 5)
    except ValueError as error:
        assert str(error) == "Invalid page range."
    else:
        raise AssertionError("Expected ValueError")


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


def test_split_pdf_selected_single_page(tmp_path):
    input_file = tmp_path / "sample.pdf"
    output_directory = tmp_path / "split"

    create_test_pdf(input_file, 3)

    generated_files = split_pdf(
        input_file,
        output_directory,
        "2",
    )

    assert generated_files == [
        output_directory / "sample_page_2.pdf",
    ]

    assert generated_files[0].exists()

    reader = PdfReader(generated_files[0])

    assert len(reader.pages) == 1


def test_split_pdf_selected_page_range(tmp_path):
    input_file = tmp_path / "sample.pdf"
    output_directory = tmp_path / "split"

    create_test_pdf(input_file, 5)

    generated_files = split_pdf(
        input_file,
        output_directory,
        "2-4",
    )

    assert generated_files == [
        output_directory / "sample_page_2.pdf",
        output_directory / "sample_page_3.pdf",
        output_directory / "sample_page_4.pdf",
    ]

    assert all(file.exists() for file in generated_files)


def test_split_pdf_selected_range_preserves_page_order(tmp_path):
    input_file = tmp_path / "sample.pdf"
    output_directory = tmp_path / "split"

    create_test_pdf(input_file, 5)

    generated_files = split_pdf(
        input_file,
        output_directory,
        "3-5",
    )

    assert [
        file.name for file in generated_files
    ] == [
        "sample_page_3.pdf",
        "sample_page_4.pdf",
        "sample_page_5.pdf",
    ]


def test_split_pdf_invalid_selection_creates_no_output(
    tmp_path,
):
    input_file = tmp_path / "sample.pdf"
    output_directory = tmp_path / "split"

    create_test_pdf(input_file, 3)

    try:
        split_pdf(
            input_file,
            output_directory,
            "2-5",
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")

    assert not output_directory.exists()
