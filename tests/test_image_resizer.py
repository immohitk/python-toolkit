from PIL import Image
import pytest

from toolkit.image_resizer import resize_image


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
