from pathlib import Path

from PIL import Image


def resize_image(input_file, output_file, width, height):
    """
    Resize an image and save the result to a new output file.
    """
    input_file = Path(input_file)
    output_file = Path(output_file)

    with Image.open(input_file) as image:
        resized_image = image.resize((width, height))
        resized_image.save(output_file)