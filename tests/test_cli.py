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
