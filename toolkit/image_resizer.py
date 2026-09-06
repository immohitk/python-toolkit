from pathlib import Path

from PIL import Image


def _validate_dimension(value, name):
    """
    Validate an optional image dimension.
    """
    if value is None:
        return

    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{name} must be a positive integer.")

    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def _calculate_dimensions(original_width, original_height, width, height):
    """
    Calculate target dimensions while preserving aspect ratio when needed.
    """
    _validate_dimension(width, "Width")
    _validate_dimension(height, "Height")

    if width is None and height is None:
        raise ValueError("Width or height must be provided.")

    if width is not None and height is not None:
        return width, height

    if width is not None:
        calculated_height = max(
            1,
            round(original_height * width / original_width),
        )
        return width, calculated_height

    calculated_width = max(
        1,
        round(original_width * height / original_height),
    )
    return calculated_width, height


def resize_image(input_file, output_file, width=None, height=None):
    """
    Resize an image while preserving aspect ratio when one dimension is omitted.
    """
    input_file = Path(input_file)
    output_file = Path(output_file)

    with Image.open(input_file) as image:
        target_width, target_height = _calculate_dimensions(
            image.width,
            image.height,
            width,
            height,
        )

        resized_image = image.resize(
            (target_width, target_height)
        )
        resized_image.save(output_file)


def resize_images(input_files, output_directory, width=None, height=None):
    """
    Resize multiple images independently and save them to an output directory.
    """
    input_files = [Path(input_file) for input_file in input_files]
    output_directory = Path(output_directory)

    output_directory.mkdir(parents=True, exist_ok=True)

    results = []
    failures = []

    for input_file in input_files:
        output_file = (
            output_directory
            / f"{input_file.stem}_resized{input_file.suffix}"
        )

        try:
            resize_image(
                input_file,
                output_file,
                width=width,
                height=height,
            )
            results.append(output_file)
        except Exception as error:
            failures.append((input_file, str(error)))

    if failures:
        failure_details = "; ".join(
            f"{input_file}: {error}"
            for input_file, error in failures
        )
        raise RuntimeError(
            f"Failed to resize {len(failures)} image(s): {failure_details}"
        )

    return results
