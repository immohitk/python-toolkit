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

    output_file.parent.mkdir(parents=True, exist_ok=True)

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


def convert_images(input_files, output_directory, target_extension):
    """Convert multiple images independently to the target format."""
    output_directory = Path(output_directory)
    input_files = [Path(input_file) for input_file in input_files]

    if not input_files:
        raise ValueError("At least one input image is required")

    results = []

    for input_file in input_files:
        output_file = get_unique_output_path(
            output_directory / f"{input_file.stem}{target_extension}"
        )

        try:
            converted_file = convert_image(input_file, output_file)
            results.append(converted_file)
        except (FileNotFoundError, ValueError) as exc:
            results.append((input_file, exc))

    return results


def get_image_format(file_path):
    """Return the normalized image format for a supported file extension."""
    file_path = Path(file_path)

    image_format = SUPPORTED_FORMATS.get(file_path.suffix.lower())

    if image_format is None:
        raise ValueError(
            f"Unsupported image format: {file_path.suffix}"
        )

    return image_format


def get_unique_output_path(output_file):
    """Return a collision-safe output path."""
    output_file = Path(output_file)

    if not output_file.exists():
        return output_file

    counter = 1

    while True:
        candidate = (
            output_file.parent
            / f"{output_file.stem}_{counter}{output_file.suffix}"
        )

        if not candidate.exists():
            return candidate

        counter += 1
