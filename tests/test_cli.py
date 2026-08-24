from toolkit.cli import run


def test_clean_dry_run(tmp_path, monkeypatch, capsys):
    temporary_file = tmp_path / "file.tmp"
    backup_file = tmp_path / "backup.bak"
    normal_file = tmp_path / "photo.jpg"

    temporary_file.touch()
    backup_file.touch()
    normal_file.touch()

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