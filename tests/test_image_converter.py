import sys
from pathlib import Path

import pytest

from PIL import Image

from toolkit.cli import run
from toolkit.image_converter import convert_image
from toolkit.image_converter import convert_images
from toolkit.image_converter import get_image_format


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


def test_convert_image_creates_missing_output_directory(tmp_path):
    input_file = tmp_path / "sample.png"
    output_file = tmp_path / "missing" / "output.jpg"

    image = Image.new("RGB", (100, 100))
    image.save(input_file, format="PNG")

    result = convert_image(input_file, output_file)

    assert result == output_file
    assert output_file.exists()
    assert output_file.parent.exists()


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


def test_convert_images_processes_multiple_pngs(tmp_path):
    input_files = []

    for name in ("first.png", "second.png", "third.png"):
        image_path = tmp_path / name
        Image.new("RGB", (100, 100), "red").save(image_path)
        input_files.append(image_path)

    output_directory = tmp_path / "output"
    output_directory.mkdir()

    results = convert_images(
        input_files,
        output_directory,
        ".jpg",
    )

    assert len(results) == 3
    assert all(isinstance(result, Path) for result in results)

    for result in results:
        assert result.exists()


def test_convert_images_processes_multiple_jpgs(tmp_path):
    input_files = []

    for name in ("first.jpg", "second.jpg"):
        image_path = tmp_path / name
        Image.new("RGB", (100, 100), "blue").save(image_path)
        input_files.append(image_path)

    output_directory = tmp_path / "output"
    output_directory.mkdir()

    results = convert_images(
        input_files,
        output_directory,
        ".png",
    )

    assert len(results) == 2
    assert all(result.exists() for result in results)


def test_convert_images_preserves_originals(tmp_path):
    input_files = []

    for name in ("first.png", "second.png"):
        image_path = tmp_path / name
        Image.new("RGB", (100, 100), "green").save(image_path)
        input_files.append(image_path)

    original_contents = {
        path: path.read_bytes()
        for path in input_files
    }

    output_directory = tmp_path / "output"
    output_directory.mkdir()

    convert_images(input_files, output_directory, ".jpg")

    for path in input_files:
        assert path.exists()
        assert path.read_bytes() == original_contents[path]


def test_convert_images_reports_failed_input_and_continues(tmp_path):
    valid_file = tmp_path / "valid.png"
    Image.new("RGB", (100, 100), "red").save(valid_file)

    invalid_file = tmp_path / "missing.png"

    output_directory = tmp_path / "output"
    output_directory.mkdir()

    results = convert_images(
        [valid_file, invalid_file],
        output_directory,
        ".jpg",
    )

    assert len(results) == 2
    assert isinstance(results[0], Path)
    assert results[0].exists()

    assert results[1][0] == invalid_file
    assert isinstance(results[1][1], FileNotFoundError)


def test_convert_images_processes_mixed_formats_to_jpg(tmp_path):
    input_files = []

    for name, image_format in (
        ("first.png", "PNG"),
        ("second.jpg", "JPEG"),
        ("third.webp", "WEBP"),
    ):
        image_path = tmp_path / name
        Image.new("RGB", (100, 100), "red").save(
            image_path,
            format=image_format,
        )
        input_files.append(image_path)

    output_directory = tmp_path / "output"
    output_directory.mkdir()

    results = convert_images(
        input_files,
        output_directory,
        ".jpg",
    )

    assert len(results) == 3
    assert all(isinstance(result, Path) for result in results)

    for result in results:
        assert result.exists()
        with Image.open(result) as image:
            assert image.format == "JPEG"


def test_convert_images_processes_mixed_formats_to_png(tmp_path):
    input_files = []

    for name, image_format in (
        ("first.png", "PNG"),
        ("second.jpg", "JPEG"),
        ("third.webp", "WEBP"),
        ("fourth.bmp", "BMP"),
    ):
        image_path = tmp_path / name
        Image.new("RGB", (100, 100), "blue").save(
            image_path,
            format=image_format,
        )
        input_files.append(image_path)

    output_directory = tmp_path / "output"
    output_directory.mkdir()

    results = convert_images(
        input_files,
        output_directory,
        ".png",
    )

    assert len(results) == 4
    assert all(isinstance(result, Path) for result in results)

    for result in results:
        assert result.exists()
        with Image.open(result) as image:
            assert image.format == "PNG"


def test_convert_images_mixed_formats_preserves_originals(tmp_path):
    input_files = []

    for name, image_format in (
        ("first.png", "PNG"),
        ("second.jpg", "JPEG"),
        ("third.webp", "WEBP"),
    ):
        image_path = tmp_path / name
        Image.new("RGB", (100, 100), "green").save(
            image_path,
            format=image_format,
        )
        input_files.append(image_path)

    original_contents = {
        path: path.read_bytes()
        for path in input_files
    }

    output_directory = tmp_path / "output"
    output_directory.mkdir()

    convert_images(input_files, output_directory, ".jpg")

    for path in input_files:
        assert path.exists()
        assert path.read_bytes() == original_contents[path]


def test_convert_images_avoids_output_collision(tmp_path):
    input_file = tmp_path / "photo.png"
    Image.new("RGB", (100, 100), "red").save(input_file)

    output_directory = tmp_path / "output"
    output_directory.mkdir()

    existing_output = output_directory / "photo.jpg"
    existing_output.write_bytes(b"existing")

    results = convert_images(
        [input_file],
        output_directory,
        ".jpg",
    )

    assert results == [output_directory / "photo_1.jpg"]
    assert existing_output.read_bytes() == b"existing"
    assert results[0].exists()


def test_convert_images_avoids_multiple_output_collisions(tmp_path):
    input_file = tmp_path / "photo.png"
    Image.new("RGB", (100, 100), "blue").save(input_file)

    output_directory = tmp_path / "output"
    output_directory.mkdir()

    (output_directory / "photo.jpg").write_bytes(b"original")
    (output_directory / "photo_1.jpg").write_bytes(b"original")
    (output_directory / "photo_2.jpg").write_bytes(b"original")

    results = convert_images(
        [input_file],
        output_directory,
        ".jpg",
    )

    assert results == [output_directory / "photo_3.jpg"]
    assert results[0].exists()

    assert (output_directory / "photo.jpg").read_bytes() == b"original"
    assert (output_directory / "photo_1.jpg").read_bytes() == b"original"
    assert (output_directory / "photo_2.jpg").read_bytes() == b"original"


def test_convert_images_reports_multiple_failed_inputs(tmp_path):
    valid_file = tmp_path / "valid.png"
    Image.new("RGB", (100, 100), "red").save(valid_file)

    missing_file = tmp_path / "missing.png"
    corrupt_file = tmp_path / "corrupt.png"
    corrupt_file.write_bytes(b"corrupt image data")

    output_directory = tmp_path / "output"
    output_directory.mkdir()

    results = convert_images(
        [valid_file, missing_file, corrupt_file],
        output_directory,
        ".jpg",
    )

    assert len(results) == 3

    assert isinstance(results[0], Path)
    assert results[0].exists()

    assert results[1][0] == missing_file
    assert isinstance(results[1][1], FileNotFoundError)

    assert results[2][0] == corrupt_file
    assert isinstance(results[2][1], ValueError)


def test_convert_images_identifies_failed_input_among_valid_inputs(tmp_path):
    first_valid = tmp_path / "first.png"
    invalid_file = tmp_path / "invalid.png"
    second_valid = tmp_path / "second.jpg"

    Image.new("RGB", (100, 100), "red").save(first_valid)
    invalid_file.write_text("not an image")
    Image.new("RGB", (100, 100), "blue").save(second_valid)

    output_directory = tmp_path / "output"
    output_directory.mkdir()

    results = convert_images(
        [first_valid, invalid_file, second_valid],
        output_directory,
        ".png",
    )

    assert len(results) == 3

    assert isinstance(results[0], Path)
    assert results[0].exists()

    assert results[1][0] == invalid_file
    assert isinstance(results[1][1], ValueError)

    assert isinstance(results[2], Path)
    assert results[2].exists()


def test_convert_images_preserves_existing_output_when_batch_input_fails(
    tmp_path,
):
    valid_file = tmp_path / "photo.png"
    invalid_file = tmp_path / "broken.png"

    Image.new("RGB", (100, 100), "green").save(valid_file)
    invalid_file.write_bytes(b"invalid image")

    output_directory = tmp_path / "output"
    output_directory.mkdir()

    existing_output = output_directory / "photo.jpg"
    existing_output.write_bytes(b"existing output")

    results = convert_images(
        [valid_file, invalid_file],
        output_directory,
        ".jpg",
    )

    assert len(results) == 2
    assert results[0] == output_directory / "photo_1.jpg"

    assert results[1][0] == invalid_file
    assert isinstance(results[1][1], ValueError)

    assert existing_output.read_bytes() == b"existing output"
    assert results[0].exists()


def test_convert_images_handles_same_filename_from_different_directories(
    tmp_path,
):
    first_directory = tmp_path / "folder_a"
    second_directory = tmp_path / "folder_b"
    output_directory = tmp_path / "output"

    first_directory.mkdir()
    second_directory.mkdir()
    output_directory.mkdir()

    first_file = first_directory / "photo.png"
    second_file = second_directory / "photo.png"

    Image.new("RGB", (100, 100), "red").save(first_file, format="PNG")
    Image.new("RGB", (100, 100), "blue").save(second_file, format="PNG")

    first_original = first_file.read_bytes()
    second_original = second_file.read_bytes()

    results = convert_images(
        [first_file, second_file],
        output_directory,
        ".jpg",
    )

    assert len(results) == 2
    assert results[0] == output_directory / "photo.jpg"
    assert results[1] == output_directory / "photo_1.jpg"
    assert results[0] != results[1]

    assert results[0].exists()
    assert results[1].exists()

    assert first_file.read_bytes() == first_original
    assert second_file.read_bytes() == second_original


def test_image_converter_cli_converts_single_image(
    tmp_path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "sample.jpg"
    output_directory = tmp_path / "output"

    Image.new("RGB", (100, 100), "red").save(
        input_file,
        format="JPEG",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "python-toolkit",
            "image-converter",
            str(input_file),
            "--format",
            "png",
            "--output-dir",
            str(output_directory),
        ],
    )

    run()

    output_file = output_directory / "sample.png"

    assert output_file.exists()
    assert input_file.exists()

    captured = capsys.readouterr()

    assert "Image Conversion Complete" in captured.out
    assert str(output_file) in captured.out


def test_image_converter_cli_processes_batch(
    tmp_path,
    monkeypatch,
    capsys,
):
    first_file = tmp_path / "first.jpg"
    second_file = tmp_path / "second.jpg"
    output_directory = tmp_path / "output"

    Image.new("RGB", (100, 100), "red").save(
        first_file,
        format="JPEG",
    )
    Image.new("RGB", (100, 100), "blue").save(
        second_file,
        format="JPEG",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "python-toolkit",
            "image-converter",
            str(first_file),
            str(second_file),
            "--format",
            "png",
            "--output-dir",
            str(output_directory),
        ],
    )

    run()

    assert (output_directory / "first.png").exists()
    assert (output_directory / "second.png").exists()

    captured = capsys.readouterr()

    assert str(output_directory / "first.png") in captured.out
    assert str(output_directory / "second.png") in captured.out


def test_image_converter_cli_reports_missing_input(
    tmp_path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "missing.jpg"
    output_directory = tmp_path / "output"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "python-toolkit",
            "image-converter",
            str(input_file),
            "--format",
            "png",
            "--output-dir",
            str(output_directory),
        ],
    )

    run()

    captured = capsys.readouterr()

    assert "Input file not found" in captured.out
    assert not output_directory.exists()


def test_image_converter_cli_rejects_unsupported_target(
    tmp_path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "sample.jpg"
    output_directory = tmp_path / "output"

    Image.new("RGB", (100, 100), "red").save(
        input_file,
        format="JPEG",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "python-toolkit",
            "image-converter",
            str(input_file),
            "--format",
            "gif",
            "--output-dir",
            str(output_directory),
        ],
    )

    run()

    captured = capsys.readouterr()

    assert "Unsupported image format" in captured.out
    assert not output_directory.exists()


def test_image_converter_cli_rejects_invalid_image(
    tmp_path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "corrupt.jpg"
    output_directory = tmp_path / "output"

    input_file.write_bytes(b"corrupt image data")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "python-toolkit",
            "image-converter",
            str(input_file),
            "--format",
            "png",
            "--output-dir",
            str(output_directory),
        ],
    )

    run()

    captured = capsys.readouterr()

    assert "not a valid image" in captured.out


def test_image_converter_cli_dry_run_creates_no_files(
    tmp_path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "sample.jpg"
    output_directory = tmp_path / "dry-run"

    Image.new("RGB", (100, 100), "red").save(
        input_file,
        format="JPEG",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "python-toolkit",
            "image-converter",
            str(input_file),
            "--format",
            "png",
            "--output-dir",
            str(output_directory),
            "--dry-run",
        ],
    )

    run()

    captured = capsys.readouterr()

    expected_output = output_directory / "sample.png"

    assert "Image Conversion Dry Run" in captured.out
    assert str(expected_output) in captured.out
    assert "No files were created." in captured.out

    assert not output_directory.exists()


def test_image_converter_cli_dry_run_batch_creates_no_files(
    tmp_path,
    monkeypatch,
    capsys,
):
    first_file = tmp_path / "first.jpg"
    second_file = tmp_path / "second.jpg"
    output_directory = tmp_path / "dry-run-batch"

    Image.new("RGB", (100, 100), "red").save(
        first_file,
        format="JPEG",
    )
    Image.new("RGB", (100, 100), "blue").save(
        second_file,
        format="JPEG",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "python-toolkit",
            "image-converter",
            str(first_file),
            str(second_file),
            "--format",
            "png",
            "--output-dir",
            str(output_directory),
            "--dry-run",
        ],
    )

    run()

    captured = capsys.readouterr()

    assert str(output_directory / "first.png") in captured.out
    assert str(output_directory / "second.png") in captured.out
    assert "No files were created." in captured.out

    assert not output_directory.exists()


def test_image_converter_cli_dry_run_handles_existing_output_collision(
    tmp_path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "photo.jpg"
    output_directory = tmp_path / "output"

    Image.new("RGB", (100, 100), "red").save(
        input_file,
        format="JPEG",
    )

    output_directory.mkdir()

    existing_output = output_directory / "photo.png"
    existing_output.write_bytes(b"existing output")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "python-toolkit",
            "image-converter",
            str(input_file),
            "--format",
            "png",
            "--output-dir",
            str(output_directory),
            "--dry-run",
        ],
    )

    run()

    captured = capsys.readouterr()

    expected_output = output_directory / "photo_1.png"

    assert str(expected_output) in captured.out
    assert "No files were created." in captured.out

    assert existing_output.read_bytes() == b"existing output"
    assert not expected_output.exists()


def test_image_converter_cli_dry_run_handles_batch_output_collision(
    tmp_path,
    monkeypatch,
    capsys,
):
    first_directory = tmp_path / "folder_a"
    second_directory = tmp_path / "folder_b"
    output_directory = tmp_path / "output"

    first_directory.mkdir()
    second_directory.mkdir()
    output_directory.mkdir()

    first_file = first_directory / "photo.jpg"
    second_file = second_directory / "photo.jpg"

    Image.new("RGB", (100, 100), "red").save(
        first_file,
        format="JPEG",
    )
    Image.new("RGB", (100, 100), "blue").save(
        second_file,
        format="JPEG",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "python-toolkit",
            "image-converter",
            str(first_file),
            str(second_file),
            "--format",
            "png",
            "--output-dir",
            str(output_directory),
            "--dry-run",
        ],
    )

    run()

    captured = capsys.readouterr()

    assert str(output_directory / "photo.png") in captured.out
    assert str(output_directory / "photo_1.png") in captured.out
    assert "No files were created." in captured.out
