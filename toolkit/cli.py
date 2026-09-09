"""
Command Line Interface for Python Toolkit.

This module is responsible for parsing command-line arguments
and displaying help/version information.
"""

import argparse
from pathlib import Path

from pypdf import PdfReader

from toolkit.organizer import (
    analyze_files,
    create_category_folders,
    get_directory_info,
    move_files,
)

from toolkit.cleaner import (
    clean_files,
    preview_cleanup,
)

from toolkit.duplicate_finder import (
    display_duplicate_report,
    find_duplicate_files,
)

from toolkit.pdf_merger import (
    merge_pdf_files,
    validate_pdf_files,
)

from toolkit.pdf_splitter import (
    get_page_numbers,
    split_pdf,
)

from toolkit.pdf_extractor import (
    extract_pdf_pages,
    parse_page_selection,
    validate_page_selection,
)

from toolkit.image_resizer import (
    calculate_resize_dimensions,
    get_output_path,
    resize_images,
)

from toolkit.logger import get_logger

logger = get_logger()

APP_NAME = "python-toolkit"
APP_VERSION = "0.21.3"
APP_DESCRIPTION = (
    "A collection of practical Python utilities for file management, "
    "automation, and data processing."
)


def create_parser():
    """
    Create and configure the command-line argument parser.
    """
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description=APP_DESCRIPTION,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {APP_VERSION}",
    )

    subparsers = parser.add_subparsers(dest="command")

    organize_parser = subparsers.add_parser(
        "organize",
        help="Organize files in a directory",
    )

    organize_parser.add_argument(
        "directory",
        help="Directory to organize",
    )

    organize_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview file organization without moving files",
    )
    
    clean_parser = subparsers.add_parser(
        "clean",
        help="Clean temporary, backup, and system files in a directory",
    )

    clean_parser.add_argument(
        "directory",
        help="Directory to clean",
    )

    clean_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview cleanup without deleting files",
    )

    duplicates_parser = subparsers.add_parser(
        "duplicates",
        help="Find duplicate files in a directory",
    )

    duplicates_parser.add_argument(
        "directory",
        help="Directory to scan for duplicate files",
    )

    duplicates_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview duplicate file analysis without modifying files",
    )

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze files in a directory",
    )

    info_parser = subparsers.add_parser(
        "info",
        help="Show directory information",
    )

    info_parser.add_argument(
        "directory",
        help="Directory to inspect",
    )

    analyze_parser.add_argument(
        "directory",
        help="Directory to analyze",
    )

    merge_parser = subparsers.add_parser(
        "merge",
        help="Merge multiple PDF files into a single PDF",
    )

    merge_parser.add_argument(
        "input_files",
        nargs="+",
        help="PDF files to merge",
    )

    merge_parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output PDF file",
    )

    merge_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview PDF merge without creating the output file",
    )

    split_parser = subparsers.add_parser(
        "split",
        help="Split a PDF into individual pages",
    )

    split_parser.add_argument(
        "input_file",
        help="PDF file to split",
    )

    split_parser.add_argument(
        "-o",
        "--output",
        default="split",
        help="Output directory for split PDF files",
    )

    split_parser.add_argument(
        "--pages",
        help="Pages to split, such as 2 or 2-4",
    )

    split_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview PDF split without creating output files",
    )

    extract_parser = subparsers.add_parser(
        "extract",
        help="Extract selected pages from a PDF",
    )

    extract_parser.add_argument(
        "input_file",
        help="PDF file to extract pages from",
    )

    extract_parser.add_argument(
        "--pages",
        required=True,
        help="Pages to extract, such as 2 or 2-4",
    )

    extract_parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output PDF file",
    )

    extract_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview extraction without creating the output file",
    )


    image_resizer_parser = subparsers.add_parser(
        "image-resizer",
        help="Resize one or more images",
    )

    image_resizer_parser.add_argument(
        "input_files",
        nargs="+",
        help="Image files to resize",
    )

    image_resizer_parser.add_argument(
        "--width",
        type=int,
        help="Target image width",
    )

    image_resizer_parser.add_argument(
        "--height",
        type=int,
        help="Target image height",
    )

    image_resizer_parser.add_argument(
        "-o",
        "--output-dir",
        required=True,
        help="Output directory for resized images",
    )

    image_resizer_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the resize operation without creating files",
    )

    return parser

def run():
    """
    Run the command-line interface.
    """
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    try:
        if args.command == "organize":
            if args.dry_run:
                move_files(args.directory, dry_run=True)
            else:
                create_category_folders(args.directory)
                move_files(args.directory)

        if args.command == "analyze":
            analyze_files(args.directory)

        if args.command == "info":
            get_directory_info(args.directory)

        if args.command == "clean":
            directory = Path(args.directory)

            if args.dry_run:
                preview_cleanup(directory)
            else:
                clean_files(directory)

        if args.command == "duplicates":
            directory = Path(args.directory)

            duplicate_groups = find_duplicate_files(directory)

            display_duplicate_report(duplicate_groups)

            if args.dry_run:
                print("\nNo files were modified.")

        if args.command == "merge":
            input_files = [Path(file) for file in args.input_files]
            output_file = Path(args.output)

            if args.dry_run:
                validate_pdf_files(input_files)

                print("PDF Merge Preview")
                print()
                print("Input files:")

                for index, input_file in enumerate(input_files, start=1):
                    print(f"{index}. {input_file}")

                print()
                print(f"Output: {output_file}")
                print()
                print("No files were modified.")
            else:
                merge_pdf_files(
                    input_files,
                    output_file,
                )

        if args.command == "split":
            input_file = Path(args.input_file)
            output_directory = Path(args.output)

            if args.dry_run:
                reader = PdfReader(input_file)

                if args.pages is None:
                    page_numbers = list(range(len(reader.pages)))
                else:
                    page_numbers = get_page_numbers(
                        args.pages,
                        len(reader.pages),
                    )

                print("PDF Split Preview")
                print()
                print(f"Input: {input_file}")
                print()

                print("Selected pages:")

                for page_number in page_numbers:
                    print(f"- {page_number + 1}")

                print()
                print("Files that would be generated:")

                for page_number in page_numbers:
                    output_file = (
                        output_directory
                        / f"{input_file.stem}_page_{page_number + 1}.pdf"
                    )
                    print(f"- {output_file}")

                print()
                print("No files were modified.")

            else:
                generated_files = split_pdf(
                    input_file,
                    output_directory,
                    args.pages,
                )

                print("PDF Split Complete")
                print()

                print("Generated files:")

                for generated_file in generated_files:
                    print(f"- {generated_file}")

        if args.command == "extract":
            input_file = Path(args.input_file)
            output_file = Path(args.output)

            page_numbers = parse_page_selection(args.pages)

            if args.dry_run:
                reader = PdfReader(input_file)

                validate_page_selection(
                    page_numbers,
                    len(reader.pages),
                )

                print("PDF Extract Preview")
                print()
                print(f"Input: {input_file}")
                print(f"Pages: {args.pages}")
                print(f"Output: {output_file}")
                print()
                print("No files were modified.")

            else:
                extract_pdf_pages(
                    input_file,
                    output_file,
                    page_numbers,
                )

                print("PDF Extract Complete")
                print()
                print(f"Input: {input_file}")
                print(f"Pages: {args.pages}")
                print(f"Output: {output_file}")

        if args.command == "image-resizer":
            input_files = [Path(file) for file in args.input_files]
            output_directory = Path(args.output_dir)

            if args.width is None and args.height is None:
                raise ValueError(
                    "Width or height must be provided."
                )

            if args.width is not None and args.width <= 0:
                raise ValueError(
                    "Width must be greater than zero."
                )

            if args.height is not None and args.height <= 0:
                raise ValueError(
                    "Height must be greater than zero."
                )

            for input_file in input_files:
                if not input_file.is_file():
                    raise FileNotFoundError(
                        f"Input file does not exist: {input_file}"
                    )

            if args.dry_run:
                print("Image Resize Dry Run")
                print()

                print("Input images:")

                for input_file in input_files:
                    print(f"- {input_file}")

                print()

                print("Resize settings:")

                if args.width is not None:
                    print(f"Width: {args.width}")
                else:
                    print("Width: Preserve aspect ratio")

                if args.height is not None:
                    print(f"Height: {args.height}")
                else:
                    print("Height: Preserve aspect ratio")

                print()

                print(f"Output directory: {output_directory}")
                print()

                print("Files that would be generated:")

                for input_file in input_files:
                    target_width, target_height = (
                        calculate_resize_dimensions(
                            input_file,
                            width=args.width,
                            height=args.height,
                        )
                    )

                    output_file = get_output_path(
                        output_directory,
                        input_file,
                    )

                    print(
                        f"- {output_file} "
                        f"({target_width}x{target_height})"
                    )

                print()
                print("No files were created.")
                return

            generated_files = resize_images(
                input_files,
                output_directory,
                width=args.width,
                height=args.height,
            )

            print("Image Resize Complete")
            print()

            print("Generated files:")

            for generated_file in generated_files:
                print(f"- {generated_file}")

    except FileNotFoundError as error:
        logger.error("%s", error)
        print(f"Error: {error}")

    except NotADirectoryError as error:
        logger.error("%s", error)
        print(f"Error: {error}")

    except ValueError as error:
        logger.error("%s", error)
        print(f"Error: {error}")

    except RuntimeError as error:
        logger.error("%s", error)
        print(f"Error: {error}")
