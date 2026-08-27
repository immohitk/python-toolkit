from hashlib import sha256

from toolkit.duplicate_finder import get_file_hash


def test_get_file_hash(tmp_path):
    test_file = tmp_path / "test.txt"
    content = b"Hello, duplicate file finder!"

    test_file.write_bytes(content)

    expected_hash = sha256(content).hexdigest()

    assert get_file_hash(test_file) == expected_hash
