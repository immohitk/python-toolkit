from pathlib import Path

import pytest

from toolkit.image_converter import convert_image

from toolkit.image_converter import get_image_format

from PIL import Image


def test_convert_image_accepts_valid_input(tmp_path):
    input_file = tmp_path / "sample.png"
    output_file = tmp_path / "sample.jpg"

    image = Image.new("RGB", (100, 100))
    image.save(input_file, format="PNG")

    result = convert_image(input_file, output_file)

    assert result == output_file
    assert input_file.exists()
    assert output_file.exists()


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


@pytest.mark.parametrize(
    ("extension", "expected_format"),
    [
        (".jpg", "JPEG"),
        (".jpeg", "JPEG"),
        (".png", "PNG"),
        (".webp", "WEBP"),
        (".bmp", "BMP"),
        (".tif", "TIFF"),
        (".tiff", "TIFF"),
        (".JPG", "JPEG"),
        (".PNG", "PNG"),
        (".WEBP", "WEBP"),
        (".BMP", "BMP"),
        (".TIFF", "TIFF"),
    ],
)
def test_get_image_format_supports_common_formats(
    extension, expected_format
):
    assert get_image_format(Path(f"sample{extension}")) == expected_format


def test_get_image_format_rejects_unsupported_format():
    with pytest.raises(ValueError, match="Unsupported image format"):
        get_image_format(Path("sample.gif"))


@pytest.mark.parametrize(
    ("source_format", "target_extension", "expected_format"),
    [
        ("PNG", ".jpg", "JPEG"),
        ("JPEG", ".png", "PNG"),
        ("PNG", ".webp", "WEBP"),
        ("JPEG", ".webp", "WEBP"),
        ("WEBP", ".png", "PNG"),
        ("BMP", ".png", "PNG"),
        ("TIFF", ".jpg", "JPEG"),
    ],
)
def test_convert_image_converts_between_formats(
    tmp_path,
    source_format,
    target_extension,
    expected_format,
):
    input_file = tmp_path / f"sample.{source_format.lower()}"
    output_file = tmp_path / f"converted{target_extension}"
    image = Image.new("RGB", (100, 100))
    image.save(input_file, format=source_format)

    original_data = input_file.read_bytes()

    result = convert_image(input_file, output_file)

    assert result == output_file
    assert output_file.exists()
    assert input_file.exists()
    assert input_file.read_bytes() == original_data

    with Image.open(output_file) as converted_image:
        assert converted_image.format == expected_format


def test_convert_rgba_png_to_jpeg(tmp_path):
    input_file = tmp_path / "transparent.png"
    output_file = tmp_path / "converted.jpg"

    image = Image.new("RGBA", (100, 100), (255, 0, 0, 128))
    image.save(input_file, format="PNG")

    original_data = input_file.read_bytes()

    convert_image(input_file, output_file)

    assert output_file.exists()
    assert input_file.read_bytes() == original_data

    with Image.open(output_file) as converted_image:
        assert converted_image.format == "JPEG"
        assert converted_image.mode == "RGB"


def test_convert_image_rejects_non_image_file(tmp_path):
    input_file = tmp_path / "input.png"
    output_file = tmp_path / "output.jpg"

    input_file.write_text("This is not an image.")

    with pytest.raises(ValueError, match="not a valid image"):
        convert_image(input_file, output_file)


def test_convert_image_rejects_corrupt_image(tmp_path):
    input_file = tmp_path / "input.png"
    output_file = tmp_path / "output.jpg"

    input_file.write_bytes(b"corrupt image data")

    with pytest.raises(ValueError, match="not a valid image"):
        convert_image(input_file, output_file)


def test_convert_image_rejects_unsupported_source_format(tmp_path):
    input_file = tmp_path / "sample.gif"
    output_file = tmp_path / "output.png"

    input_file.write_bytes(b"fake image data")

    with pytest.raises(ValueError, match="Unsupported image format"):
        convert_image(input_file, output_file)


def test_convert_image_rejects_unsupported_target_format(tmp_path):
    input_file = tmp_path / "sample.png"
    output_file = tmp_path / "output.gif"

    image = Image.new("RGB", (100, 100))
    image.save(input_file, format="PNG")

    with pytest.raises(ValueError, match="Unsupported image format"):
        convert_image(input_file, output_file)


def test_convert_image_rejects_same_input_and_output(tmp_path):
    input_file = tmp_path / "sample.png"

    image = Image.new("RGB", (100, 100))
    image.save(input_file, format="PNG")

    with pytest.raises(
        ValueError, match="Output file must be different from input file"
    ):
        convert_image(input_file, input_file)


def test_convert_image_rejects_missing_output_directory(tmp_path):
    input_file = tmp_path / "sample.png"
    output_file = tmp_path / "missing" / "output.jpg"

    image = Image.new("RGB", (100, 100))
    image.save(input_file, format="PNG")

    with pytest.raises(FileNotFoundError, match="Output directory not found"):
        convert_image(input_file, output_file)


def test_convert_image_rejects_output_directory(tmp_path):
    input_file = tmp_path / "sample.png"
    output_directory = tmp_path / "output.jpg"

    image = Image.new("RGB", (100, 100))
    image.save(input_file, format="PNG")
    output_directory.mkdir()

    with pytest.raises(ValueError, match="Output path is not a file"):
        convert_image(input_file, output_directory)


def test_convert_image_reports_conversion_failure(tmp_path, monkeypatch):
    input_file = tmp_path / "sample.png"
    output_file = tmp_path / "output.jpg"

    image = Image.new("RGB", (100, 100))
    image.save(input_file, format="PNG")

    original_save = Image.Image.save

    def failing_save(self, *args, **kwargs):
        raise OSError("simulated save failure")

    monkeypatch.setattr(Image.Image, "save", failing_save)

    with pytest.raises(ValueError, match="Failed to convert image"):
        convert_image(input_file, output_file)

    monkeypatch.setattr(Image.Image, "save", original_save)
