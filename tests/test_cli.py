from toolkit.cli import run

from pypdf import PdfReader, PdfWriter


def create_pdf(file_path, page_count, width, height):
    """Create a PDF with blank pages of the requested size."""

    writer = PdfWriter()

    for _ in range(page_count):
        writer.add_blank_page(
            width=width,
            height=height,
        )

    with file_path.open("wb") as file:
        writer.write(file)


def test_clean_dry_run(tmp_path, monkeypatch, capsys):
    temporary_file = tmp_path / "file.tmp"
    backup_file = tmp_path / "backup.bak"
    normal_file = tmp_path / "photo.jpg"

    temporary_file.touch()
    backup_file.touch()
    normal_file.touch()

    monkeypatch.setattr("builtins.input", lambda _: "y")

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "clean",
            str(tmp_path),
            "--dry-run",
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "Cleanup Preview" in output
    assert "file.tmp" in output
    assert "backup.bak" in output
    assert "photo.jpg" not in output

    assert temporary_file.exists()
    assert backup_file.exists()
    assert normal_file.exists()


def test_clean_command(tmp_path, monkeypatch, capsys):
    temporary_file = tmp_path / "file.tmp"
    backup_file = tmp_path / "backup.bak"
    normal_file = tmp_path / "photo.jpg"

    temporary_file.touch()
    backup_file.touch()
    normal_file.touch()

    monkeypatch.setattr("builtins.input", lambda _: "y")

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "clean",
            str(tmp_path),
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "Cleanup Complete" in output
    assert "file.tmp" in output
    assert "backup.bak" in output
    assert "photo.jpg" not in output

    assert not temporary_file.exists()
    assert not backup_file.exists()
    assert normal_file.exists()


def test_duplicates_command(tmp_path, monkeypatch, capsys):
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"
    unique_file = tmp_path / "unique.txt"

    first_file.write_text("Same content")
    second_file.write_text("Same content")
    unique_file.write_text("Different content")

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "duplicates",
            str(tmp_path),
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "Duplicate File Report" in output
    assert "Duplicate Group 1" in output
    assert first_file.name in output
    assert second_file.name in output
    assert unique_file.name not in output

    assert first_file.exists()
    assert second_file.exists()
    assert unique_file.exists()


def test_duplicates_command_handles_no_duplicates(
    tmp_path,
    monkeypatch,
    capsys,
):
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"

    first_file.write_text("First content")
    second_file.write_text("Second content")

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "duplicates",
            str(tmp_path),
        ],
    )

    run()

    output = capsys.readouterr().out

    assert output == "No duplicate files found.\n"

    assert first_file.exists()
    assert second_file.exists()


def test_duplicates_command_handles_empty_directory(
    tmp_path,
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "duplicates",
            str(tmp_path),
        ],
    )

    run()

    output = capsys.readouterr().out

    assert output == "No duplicate files found.\n"

def test_duplicates_command_dry_run(
    tmp_path,
    monkeypatch,
    capsys,
):
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"

    first_file.write_text("Same content")
    second_file.write_text("Same content")

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "duplicates",
            str(tmp_path),
            "--dry-run",
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "Duplicate File Report" in output
    assert first_file.name in output
    assert second_file.name in output
    assert "No files were modified." in output

    assert first_file.exists()
    assert second_file.exists()

def test_merge_command(tmp_path, monkeypatch):
    first_file = tmp_path / "first.pdf"
    second_file = tmp_path / "second.pdf"
    output_file = tmp_path / "merged.pdf"

    create_pdf(first_file, 2, 100, 100)
    create_pdf(second_file, 3, 200, 200)

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "merge",
            str(first_file),
            str(second_file),
            "-o",
            str(output_file),
        ],
    )

    run()

    reader = PdfReader(output_file)

    assert output_file.exists()
    assert len(reader.pages) == 5

def test_merge_command_dry_run(tmp_path, monkeypatch, capsys):
    first_file = tmp_path / "first.pdf"
    second_file = tmp_path / "second.pdf"
    output_file = tmp_path / "merged.pdf"

    create_pdf(first_file, 2, 100, 100)
    create_pdf(second_file, 3, 200, 200)

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "merge",
            str(first_file),
            str(second_file),
            "-o",
            str(output_file),
            "--dry-run",
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "PDF Merge Preview" in output
    assert str(first_file) in output
    assert str(second_file) in output
    assert str(output_file) in output
    assert "No files were modified." in output

    assert not output_file.exists()
    assert first_file.exists()
    assert second_file.exists()

def test_merge_command_handles_missing_file(
    tmp_path,
    monkeypatch,
    capsys,
):
    missing_file = tmp_path / "missing.pdf"
    output_file = tmp_path / "merged.pdf"

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "merge",
            str(missing_file),
            "-o",
            str(output_file),
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "Error: Input file does not exist:" in output
    assert str(missing_file) in output
    assert not output_file.exists()

def test_merge_command_rejects_non_pdf_file(
    tmp_path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "document.txt"
    output_file = tmp_path / "merged.pdf"

    input_file.write_text("Not a PDF file")

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "merge",
            str(input_file),
            "-o",
            str(output_file),
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "Error: Input file is not a PDF:" in output
    assert str(input_file) in output
    assert not output_file.exists()


def test_split_command(tmp_path, monkeypatch, capsys):
    input_file = tmp_path / "sample.pdf"
    output_directory = tmp_path / "split"

    create_pdf(input_file, 3, 100, 100)

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "split",
            str(input_file),
            "-o",
            str(output_directory),
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "PDF Split Complete" in output
    assert "sample_page_1.pdf" in output
    assert "sample_page_2.pdf" in output
    assert "sample_page_3.pdf" in output

    assert (output_directory / "sample_page_1.pdf").exists()
    assert (output_directory / "sample_page_2.pdf").exists()
    assert (output_directory / "sample_page_3.pdf").exists()


def test_split_command_with_page_range(
    tmp_path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "sample.pdf"
    output_directory = tmp_path / "split"

    create_pdf(input_file, 5, 100, 100)

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "split",
            str(input_file),
            "-o",
            str(output_directory),
            "--pages",
            "2-4",
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "PDF Split Complete" in output
    assert "sample_page_2.pdf" in output
    assert "sample_page_3.pdf" in output
    assert "sample_page_4.pdf" in output

    assert not (output_directory / "sample_page_1.pdf").exists()
    assert not (output_directory / "sample_page_5.pdf").exists()


def test_split_command_handles_missing_file(
    tmp_path,
    monkeypatch,
    capsys,
):
    missing_file = tmp_path / "missing.pdf"
    output_directory = tmp_path / "split"

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "split",
            str(missing_file),
            "-o",
            str(output_directory),
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "Error:" in output
    assert "No such file or directory" in output
    assert "missing.pdf" in output
    assert not output_directory.exists()


def test_split_command_rejects_invalid_page_selection(
    tmp_path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "sample.pdf"
    output_directory = tmp_path / "split"

    create_pdf(input_file, 3, 100, 100)

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "split",
            str(input_file),
            "-o",
            str(output_directory),
            "--pages",
            "2-10",
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "Error: Page number exceeds PDF page count: 3" in output
    assert not output_directory.exists()


def test_split_command_dry_run(
    tmp_path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "sample.pdf"
    output_directory = tmp_path / "split"

    create_pdf(input_file, 4, 100, 100)

    original_size = input_file.stat().st_size
    original_mtime = input_file.stat().st_mtime

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "split",
            str(input_file),
            "-o",
            str(output_directory),
            "--pages",
            "2-3",
            "--dry-run",
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "PDF Split Preview" in output
    assert str(input_file) in output
    assert "Selected pages:" in output
    assert "- 2" in output
    assert "- 3" in output
    assert "Files that would be generated:" in output
    assert "sample_page_2.pdf" in output
    assert "sample_page_3.pdf" in output
    assert "No files were modified." in output

    assert not output_directory.exists()
    assert input_file.exists()
    assert input_file.stat().st_size == original_size
    assert input_file.stat().st_mtime == original_mtime


def test_extract_command(tmp_path, monkeypatch, capsys):
    input_file = tmp_path / "sample.pdf"
    output_file = tmp_path / "extracted.pdf"

    create_pdf(input_file, 3, 100, 100)

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "extract",
            str(input_file),
            "--pages",
            "2",
            "-o",
            str(output_file),
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "PDF Extract Complete" in output
    assert str(output_file) in output

    assert output_file.exists()
    assert input_file.exists()

    reader = PdfReader(output_file)

    assert len(reader.pages) == 1


def test_extract_command_with_page_range(
    tmp_path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "sample.pdf"
    output_file = tmp_path / "extracted.pdf"

    create_pdf(input_file, 5, 100, 100)

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "extract",
            str(input_file),
            "--pages",
            "2-4",
            "-o",
            str(output_file),
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "PDF Extract Complete" in output
    assert str(output_file) in output

    assert output_file.exists()
    assert input_file.exists()

    reader = PdfReader(output_file)

    assert len(reader.pages) == 3


def test_extract_command_handles_missing_file(
    tmp_path,
    monkeypatch,
    capsys,
):
    missing_file = tmp_path / "missing.pdf"
    output_file = tmp_path / "extracted.pdf"

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "extract",
            str(missing_file),
            "--pages",
            "2",
            "-o",
            str(output_file),
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "Error:" in output
    assert "No such file or directory" in output
    assert "missing.pdf" in output
    assert not output_file.exists()


def test_extract_command_rejects_invalid_page_selection(
    tmp_path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "sample.pdf"
    output_file = tmp_path / "extracted.pdf"

    create_pdf(input_file, 3, 100, 100)

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "extract",
            str(input_file),
            "--pages",
            "2-10",
            "-o",
            str(output_file),
        ],
    )

    run()

    output = capsys.readouterr().out

    assert "Error: Page selection is out of range." in output
    assert not output_file.exists()

def test_extract_command_requires_pages_and_output(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "extract",
            "sample.pdf",
        ],
    )

    try:
        run()
    except SystemExit as error:
        assert error.code == 2

    output = capsys.readouterr().err

    assert "the following arguments are required:" in output
    assert "--pages" in output
    assert "-o/--output" in output


def test_extract_command_preserves_source_pdf(
    tmp_path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "sample.pdf"
    output_file = tmp_path / "extracted.pdf"

    create_pdf(input_file, 4, 100, 100)

    original_size = input_file.stat().st_size
    original_mtime = input_file.stat().st_mtime

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "extract",
            str(input_file),
            "--pages",
            "2-3",
            "-o",
            str(output_file),
        ],
    )

    run()

    capsys.readouterr()

    assert output_file.exists()
    assert input_file.exists()

    assert input_file.stat().st_size == original_size
    assert input_file.stat().st_mtime == original_mtime

    reader = PdfReader(output_file)

    assert len(reader.pages) == 2
