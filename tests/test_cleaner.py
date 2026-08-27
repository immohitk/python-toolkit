from toolkit.cleaner import (
    find_cleanup_candidates,
    format_file_size,
    get_cleanup_category,
    get_cleanup_summary,
    get_file_size,
    get_total_cleanup_size,
    preview_cleanup,
    clean_files,
    show_cleanup_candidates,
)

def test_find_cleanup_candidates(tmp_path):
    (tmp_path / "file.tmp").touch()
    (tmp_path / "backup.bak").touch()
    (tmp_path / "photo.jpg").touch()

    candidates = find_cleanup_candidates(tmp_path)

    assert candidates == [
        (tmp_path / "backup.bak", "Backup", 0),
        (tmp_path / "file.tmp", "Temporary", 0),
    ]

def test_get_cleanup_category():
    assert get_cleanup_category("file.tmp") == "Temporary"
    assert get_cleanup_category("file.temp") == "Temporary"
    assert get_cleanup_category("backup.bak") == "Backup"
    assert get_cleanup_category("Thumbs.db") == "System"
    assert get_cleanup_category(".DS_Store") == "System"
    assert get_cleanup_category("photo.jpg") is None

def test_show_cleanup_candidates(tmp_path, capsys):
    (tmp_path / "file.tmp").write_bytes(b"a" * 1024)
    (tmp_path / "backup.bak").write_bytes(b"b" * 2048)
    (tmp_path / "photo.jpg").touch()

    show_cleanup_candidates(tmp_path)

    output = capsys.readouterr().out

    assert "Cleanup Candidates" in output
    assert "backup.bak" in output
    assert "Backup" in output
    assert "file.tmp" in output
    assert "Temporary" in output
    assert "photo.jpg" not in output
    assert "1.00 KB" in output
    assert "2.00 KB" in output
    assert "Total cleanup size: 3.00 KB" in output
    assert "Cleanup Summary" in output
    assert "Backup: 1 file (2.00 KB)" in output
    assert "Temporary: 1 file (1.00 KB)" in output

def test_show_cleanup_candidates_no_candidates(tmp_path, capsys):
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "document.pdf").touch()

    show_cleanup_candidates(tmp_path)

    output = capsys.readouterr().out

    assert "No cleanup candidates found." in output

def test_get_file_size(tmp_path):
    test_file = tmp_path / "file.tmp"
    test_file.write_bytes(b"1234567890")

    assert get_file_size(test_file) == 10

def test_get_total_cleanup_size(tmp_path):
    (tmp_path / "file.tmp").write_bytes(b"a" * 1024)
    (tmp_path / "backup.bak").write_bytes(b"b" * 2048)
    (tmp_path / "photo.jpg").write_bytes(b"12345678901234567890")

    total_size = get_total_cleanup_size(tmp_path)

    assert total_size == 3072

def test_format_file_size():
    assert format_file_size(0) == "0 bytes"
    assert format_file_size(500) == "500 bytes"
    assert format_file_size(1024) == "1.00 KB"
    assert format_file_size(1048576) == "1.00 MB"

def test_get_cleanup_summary(tmp_path):
    (tmp_path / "file.tmp").write_bytes(b"a" * 1024)
    (tmp_path / "another.tmp").write_bytes(b"b" * 2048)
    (tmp_path / "backup.bak").write_bytes(b"c" * 512)
    (tmp_path / "photo.jpg").write_bytes(b"d" * 100)

    summary = get_cleanup_summary(tmp_path)

    assert summary == {
        "Backup": {
            "count": 1,
            "size": 512,
        },
        "Temporary": {
            "count": 2,
            "size": 3072,
        },
    }

def test_preview_cleanup(tmp_path, capsys):
    temporary_file = tmp_path / "file.tmp"
    backup_file = tmp_path / "backup.bak"
    normal_file = tmp_path / "photo.jpg"

    temporary_file.write_bytes(b"a" * 1024)
    backup_file.write_bytes(b"b" * 2048)
    normal_file.write_bytes(b"c" * 100)

    preview_cleanup(tmp_path)

    output = capsys.readouterr().out

    assert "Cleanup Preview" in output
    assert "file.tmp" in output
    assert "backup.bak" in output
    assert "photo.jpg" not in output
    assert "Temporary" in output
    assert "Backup" in output
    assert "1.00 KB" in output
    assert "2.00 KB" in output
    assert "Total cleanup size: 3.00 KB" in output

    assert temporary_file.exists()
    assert backup_file.exists()
    assert normal_file.exists()

def test_preview_cleanup_no_candidates(tmp_path, capsys):
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "document.pdf").touch()

    preview_cleanup(tmp_path)

    output = capsys.readouterr().out

    assert "No cleanup candidates found." in output

def test_clean_files(tmp_path, monkeypatch, capsys):
    temporary_file = tmp_path / "file.tmp"
    backup_file = tmp_path / "backup.bak"
    normal_file = tmp_path / "photo.jpg"

    temporary_file.write_bytes(b"a" * 1024)
    backup_file.write_bytes(b"b" * 2048)
    normal_file.write_bytes(b"c" * 100)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    clean_files(tmp_path)

    output = capsys.readouterr().out

    assert "Cleanup Complete" in output
    assert "file.tmp" in output
    assert "backup.bak" in output
    assert "photo.jpg" not in output
    assert "Files removed: 2" in output
    assert "Space freed: 3.00 KB" in output

    assert not temporary_file.exists()
    assert not backup_file.exists()
    assert normal_file.exists()


def test_clean_files_no_candidates(tmp_path, capsys):
    normal_file = tmp_path / "photo.jpg"
    normal_file.touch()

    clean_files(tmp_path)

    output = capsys.readouterr().out

    assert "No cleanup candidates found." in output
    assert normal_file.exists()

def test_clean_files_handles_deletion_failure(
    tmp_path,
    monkeypatch,
    capsys,
):
    temporary_file = tmp_path / "file.tmp"
    backup_file = tmp_path / "backup.bak"

    temporary_file.write_bytes(b"a" * 1024)
    backup_file.write_bytes(b"b" * 2048)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    original_unlink = type(temporary_file).unlink

    def failing_unlink(file, *args, **kwargs):
        if file == temporary_file:
            raise PermissionError("Access denied")

        return original_unlink(file, *args, **kwargs)

    monkeypatch.setattr(
        type(temporary_file),
        "unlink",
        failing_unlink,
    )

    clean_files(tmp_path)

    output = capsys.readouterr().out

    assert "Failed to remove: file.tmp" in output
    assert "Removed: backup.bak" in output
    assert "Files removed: 1" in output
    assert "Files failed: 1" in output
    assert "Space freed: 2.00 KB" in output

    assert temporary_file.exists()
    assert not backup_file.exists()
