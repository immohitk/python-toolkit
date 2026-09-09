from pathlib import Path


def convert_image(input_file, output_file):
    """Convert an image from its source format to the target format."""
    input_file = Path(input_file)
    output_file = Path(output_file)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if not input_file.is_file():
        raise ValueError(f"Input path is not a file: {input_file}")

    return output_file