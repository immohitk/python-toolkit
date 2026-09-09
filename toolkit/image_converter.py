from pathlib import Path


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
    """Convert an image from its source format to the target format."""
    input_file = Path(input_file)
    output_file = Path(output_file)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if not input_file.is_file():
        raise ValueError(f"Input path is not a file: {input_file}")

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
