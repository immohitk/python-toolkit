from toolkit.cleaner import (
    find_cleanup_candidates,
    get_cleanup_category,
    show_cleanup_candidates,
)

def test_find_cleanup_candidates(tmp_path):
    (tmp_path / "file.tmp").touch()
    (tmp_path / "backup.bak").touch()
    (tmp_path / "photo.jpg").touch()

    candidates = find_cleanup_candidates(tmp_path)

    assert candidates == [
        (tmp_path / "backup.bak", "Backup"),
        (tmp_path / "file.tmp", "Temporary"),
    ]

def test_get_cleanup_category():
    assert get_cleanup_category("file.tmp") == "Temporary"
    assert get_cleanup_category("file.temp") == "Temporary"
    assert get_cleanup_category("backup.bak") == "Backup"
    assert get_cleanup_category("Thumbs.db") == "System"
    assert get_cleanup_category(".DS_Store") == "System"
    assert get_cleanup_category("photo.jpg") is None

def test_show_cleanup_candidates(tmp_path, capsys):
    (tmp_path / "file.tmp").touch()
    (tmp_path / "backup.bak").touch()
    (tmp_path / "photo.jpg").touch()

    show_cleanup_candidates(tmp_path)

    output = capsys.readouterr().out

    assert "Cleanup Candidates" in output
    assert "backup.bak" in output
    assert "Backup" in output
    assert "file.tmp" in output
    assert "Temporary" in output
    assert "photo.jpg" not in output

def test_show_cleanup_candidates_no_candidates(tmp_path, capsys):
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "document.pdf").touch()

    show_cleanup_candidates(tmp_path)

    output = capsys.readouterr().out

    assert "No cleanup candidates found." in output