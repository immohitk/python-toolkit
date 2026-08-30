from toolkit.cli import run


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
