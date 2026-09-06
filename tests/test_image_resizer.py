from PIL import Image

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