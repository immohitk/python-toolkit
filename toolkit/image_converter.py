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

    source_format = get_image_format(input_file)
    target_format = get_image_format(output_file)

    if output_file == input_file:
        raise ValueError("Output file must be different from input file")

    if output_file.exists() and not output_file.is_file():
        raise ValueError(f"Output path is not a file: {output_file}")

    if not output_file.parent.exists():
        raise FileNotFoundError(
            f"Output directory not found: {output_file.parent}"
        )

    try:
        image = Image.open(input_file)
        image.verify()
    except (OSError, SyntaxError) as exc:
        raise ValueError(f"Input file is not a valid image: {input_file}") from exc

    try:
        with Image.open(input_file) as image:
            if target_format == "JPEG" and image.mode in ("RGBA", "LA"):
                image = image.convert("RGB")

            image.save(output_file, format=target_format)
    except OSError as exc:
        raise ValueError(
            f"Failed to convert image: {input_file} -> {output_file}"
        ) from exc

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
