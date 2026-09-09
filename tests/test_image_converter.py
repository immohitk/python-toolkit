from pathlib import Path

import pytest

from toolkit.image_converter import convert_image


def test_convert_image_accepts_valid_input(tmp_path):
    input_file = tmp_path / "sample.png"
    output_file = tmp_path / "sample.jpg"

    input_file.write_bytes(b"test image")

    result = convert_image(input_file, output_file)

    assert result == output_file
    assert input_file.exists()


def test_convert_image_rejects_missing_input(tmp_path):
    input_file = tmp_path / "missing.png"
    output_file = tmp_path / "output.jpg"

    with pytest.raises(FileNotFoundError, match="Input file not found"):
        convert_image(input_file, output_file)


def test_convert_image_rejects_directory_input(tmp_path):
    input_directory = tmp_path / "images"
    output_file = tmp_path / "output.jpg"

    input_directory.mkdir()

    with pytest.raises(ValueError, match="Input path is not a file"):
        convert_image(input_directory, output_file)