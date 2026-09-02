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

from toolkit.logger import get_logger

logger = get_logger()

APP_NAME = "python-toolkit"
APP_VERSION = "0.19.0"
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

    except FileNotFoundError as error:
        logger.error("%s", error)
        print(f"Error: {error}")

    except NotADirectoryError as error:
        logger.error("%s", error)
        print(f"Error: {error}")

    except ValueError as error:
        logger.error("%s", error)
        print(f"Error: {error}")
