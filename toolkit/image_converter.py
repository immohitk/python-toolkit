from pathlib import Path

from PIL import Image


SUPPORTED_FORMATS = {
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".png": "PNG",
    ".webp": "WEBP",
    ".bmp": "BMP",
    ".tif": "TIFF",
    ".tiff": "TIFF",
}


def convert_image(input_file, output_file):
    """Convert an image to the format specified by the output file."""
    input_file = Path(input_file)
    output_file = Path(output_file)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if not input_file.is_file():
        raise ValueError(f"Input path is not a file: {input_file}")

    target_format = get_image_format(output_file)

    with Image.open(input_file) as image:
        image.save(output_file, format=target_format)

    return output_file


def get_image_format(file_path):
    """Return the normalized image format for a supported file extension."""
    file_path = Path(file_path)

    image_format = SUPPORTED_FORMATS.get(file_path.suffix.lower())

    if image_format is None:
        raise ValueError(
            f"Unsupported image format: {file_path.suffix}"
        )

    return image_format
