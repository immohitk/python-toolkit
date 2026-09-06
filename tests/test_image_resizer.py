from PIL import Image
import pytest

from toolkit.image_resizer import resize_image, resize_images


def test_resize_image_creates_resized_output(tmp_path):
    input_file = tmp_path / "input.png"
    output_file = tmp_path / "output.png"

    image = Image.new("RGB", (800, 600), "blue")
    image.save(input_file)

    resize_image(input_file, output_file, 400, 300)

    with Image.open(output_file) as resized_image:
        assert resized_image.size == (400, 300)


def test_resize_image_preserves_original(tmp_path):
    input_file = tmp_path / "input.png"
    output_file = tmp_path / "output.png"

    image = Image.new("RGB", (800, 600), "blue")
    image.save(input_file)

    resize_image(input_file, output_file, 400, 300)

    with Image.open(input_file) as original_image:
        assert original_image.size == (800, 600)


def test_resize_image_width_only_preserves_aspect_ratio(tmp_path):
    input_file = tmp_path / "input.png"
    output_file = tmp_path / "output.png"

    Image.new("RGB", (800, 600), "blue").save(input_file)

    resize_image(input_file, output_file, width=400)

    with Image.open(output_file) as resized_image:
        assert resized_image.size == (400, 300)


def test_resize_image_height_only_preserves_aspect_ratio(tmp_path):
    input_file = tmp_path / "input.png"
    output_file = tmp_path / "output.png"

    Image.new("RGB", (800, 600), "blue").save(input_file)

    resize_image(input_file, output_file, height=300)

    with Image.open(output_file) as resized_image:
        assert resized_image.size == (400, 300)


def test_resize_image_landscape(tmp_path):
    input_file = tmp_path / "landscape.png"
    output_file = tmp_path / "output.png"

    Image.new("RGB", (1200, 800), "blue").save(input_file)

    resize_image(input_file, output_file, width=600)

    with Image.open(output_file) as resized_image:
        assert resized_image.size == (600, 400)


def test_resize_image_portrait(tmp_path):
    input_file = tmp_path / "portrait.png"
    output_file = tmp_path / "output.png"

    Image.new("RGB", (600, 900), "blue").save(input_file)

    resize_image(input_file, output_file, width=300)

    with Image.open(output_file) as resized_image:
        assert resized_image.size == (300, 450)


def test_resize_image_square(tmp_path):
    input_file = tmp_path / "square.png"
    output_file = tmp_path / "output.png"

    Image.new("RGB", (800, 800), "blue").save(input_file)

    resize_image(input_file, output_file, width=400)

    with Image.open(output_file) as resized_image:
        assert resized_image.size == (400, 400)


def test_resize_image_supports_different_target_dimensions(tmp_path):
    input_file = tmp_path / "input.png"
    output_file = tmp_path / "output.png"

    Image.new("RGB", (1000, 700), "blue").save(input_file)

    resize_image(input_file, output_file, width=250, height=180)

    with Image.open(output_file) as resized_image:
        assert resized_image.size == (250, 180)


@pytest.mark.parametrize(
    "width,height",
    [
        (0, 300),
        (-100, 300),
        (400, 0),
        (400, -100),
        (None, None),
        (400.5, 300),
        (400, 300.5),
        ("400", 300),
        (400, "300"),
        (True, 300),
    ],
)
def test_resize_image_rejects_invalid_dimensions(
    tmp_path,
    width,
    height,
):
    input_file = tmp_path / "input.png"
    output_file = tmp_path / "output.png"

    Image.new("RGB", (800, 600), "blue").save(input_file)

    with pytest.raises(ValueError):
        resize_image(
            input_file,
            output_file,
            width=width,
            height=height,
        )

    assert not output_file.exists()


def test_resize_image_width_only_rounds_calculated_height(tmp_path):
    input_file = tmp_path / "input.png"
    output_file = tmp_path / "output.png"

    Image.new("RGB", (1000, 667), "blue").save(input_file)

    resize_image(input_file, output_file, width=500)

    with Image.open(output_file) as resized_image:
        assert resized_image.size == (500, 334)


def test_resize_image_height_only_rounds_calculated_width(tmp_path):
    input_file = tmp_path / "input.png"
    output_file = tmp_path / "output.png"

    Image.new("RGB", (667, 1000), "blue").save(input_file)

    resize_image(input_file, output_file, height=500)

    with Image.open(output_file) as resized_image:
        assert resized_image.size == (334, 500)


def test_resize_image_width_only_preserves_source_orientation(tmp_path):
    input_file = tmp_path / "input.png"
    output_file = tmp_path / "output.png"

    Image.new("RGB", (1200, 800), "blue").save(input_file)

    resize_image(input_file, output_file, width=300)

    with Image.open(output_file) as resized_image:
        assert resized_image.width > resized_image.height


def test_resize_image_height_only_preserves_source_orientation(tmp_path):
    input_file = tmp_path / "input.png"
    output_file = tmp_path / "output.png"

    Image.new("RGB", (800, 1200), "blue").save(input_file)

    resize_image(input_file, output_file, height=300)

    with Image.open(output_file) as resized_image:
        assert resized_image.height > resized_image.width


def test_resize_image_width_only_never_creates_zero_height(tmp_path):
    input_file = tmp_path / "input.png"
    output_file = tmp_path / "output.png"

    Image.new("RGB", (1000, 1), "blue").save(input_file)

    resize_image(input_file, output_file, width=1)

    with Image.open(output_file) as resized_image:
        assert resized_image.size == (1, 1)


def test_resize_images_processes_single_image(tmp_path):
    input_file = tmp_path / "photo.jpg"
    output_directory = tmp_path / "resized"

    image = Image.new("RGB", (800, 600), "blue")
    image.save(input_file)

    results = resize_images(
        [input_file],
        output_directory,
        width=400,
    )

    output_file = output_directory / "photo_resized.jpg"

    assert results == [output_file]
    assert output_file.exists()

    with Image.open(output_file) as resized_image:
        assert resized_image.size == (400, 300)


def test_resize_images_processes_multiple_images(tmp_path):
    input_files = [
        tmp_path / "photo1.jpg",
        tmp_path / "photo2.png",
        tmp_path / "photo3.jpeg",
    ]
    output_directory = tmp_path / "resized"

    Image.new("RGB", (800, 600), "blue").save(input_files[0])
    Image.new("RGB", (600, 900), "red").save(input_files[1])
    Image.new("RGB", (700, 700), "green").save(input_files[2])

    results = resize_images(
        input_files,
        output_directory,
        width=400,
    )

    assert len(results) == 3

    expected_outputs = [
        output_directory / "photo1_resized.jpg",
        output_directory / "photo2_resized.png",
        output_directory / "photo3_resized.jpeg",
    ]

    assert results == expected_outputs

    for output_file in expected_outputs:
        assert output_file.exists()


def test_resize_images_handles_different_image_dimensions(tmp_path):
    input_files = [
        tmp_path / "landscape.jpg",
        tmp_path / "portrait.jpg",
        tmp_path / "square.jpg",
    ]
    output_directory = tmp_path / "resized"

    Image.new("RGB", (800, 600), "blue").save(input_files[0])
    Image.new("RGB", (600, 900), "red").save(input_files[1])
    Image.new("RGB", (700, 700), "green").save(input_files[2])

    resize_images(
        input_files,
        output_directory,
        width=400,
    )

    with Image.open(output_directory / "landscape_resized.jpg") as image:
        assert image.size == (400, 300)

    with Image.open(output_directory / "portrait_resized.jpg") as image:
        assert image.size == (400, 600)

    with Image.open(output_directory / "square_resized.jpg") as image:
        assert image.size == (400, 400)


def test_resize_images_preserves_originals(tmp_path):
    input_files = [
        tmp_path / "photo1.jpg",
        tmp_path / "photo2.jpg",
    ]
    output_directory = tmp_path / "resized"

    Image.new("RGB", (800, 600), "blue").save(input_files[0])
    Image.new("RGB", (600, 900), "red").save(input_files[1])

    resize_images(
        input_files,
        output_directory,
        width=400,
    )

    with Image.open(input_files[0]) as image:
        assert image.size == (800, 600)

    with Image.open(input_files[1]) as image:
        assert image.size == (600, 900)


def test_resize_images_reports_invalid_image_without_losing_valid_results(tmp_path):
    valid_file_1 = tmp_path / "photo1.jpg"
    invalid_file = tmp_path / "broken.jpg"
    valid_file_2 = tmp_path / "photo2.jpg"
    output_directory = tmp_path / "resized"

    Image.new("RGB", (800, 600), "blue").save(valid_file_1)
    invalid_file.write_text("not a valid image")
    Image.new("RGB", (600, 900), "red").save(valid_file_2)

    with pytest.raises(RuntimeError, match="broken.jpg"):
        resize_images(
            [valid_file_1, invalid_file, valid_file_2],
            output_directory,
            width=400,
        )

    assert (output_directory / "photo1_resized.jpg").exists()
    assert (output_directory / "photo2_resized.jpg").exists()


def test_resize_images_rejects_empty_input(tmp_path):
    output_directory = tmp_path / "resized"

    with pytest.raises(
        ValueError,
        match="Input files must contain at least one image",
    ):
        resize_images(
            [],
            output_directory,
            width=400,
        )


def test_resize_images_reports_missing_input_file(tmp_path):
    missing_file = tmp_path / "missing.jpg"
    output_directory = tmp_path / "resized"

    with pytest.raises(RuntimeError, match="missing.jpg"):
        resize_images(
            [missing_file],
            output_directory,
            width=400,
        )

    assert not (output_directory / "missing_resized.jpg").exists()


def test_resize_images_reports_invalid_dimensions(tmp_path):
    input_file = tmp_path / "photo.jpg"
    output_directory = tmp_path / "resized"

    Image.new("RGB", (800, 600), "blue").save(input_file)

    with pytest.raises(RuntimeError, match="Width must be greater than zero"):
        resize_images(
            [input_file],
            output_directory,
            width=0,
        )

    assert not (output_directory / "photo_resized.jpg").exists()
