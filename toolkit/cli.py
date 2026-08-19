"""
Command Line Interface for Python Toolkit.

This module is responsible for parsing command-line arguments
and displaying help/version information.
"""

import argparse

from toolkit.organizer import (
    analyze_files,
    create_category_folders,
    get_directory_info,
    move_files,
)

from toolkit.logger import get_logger

logger = get_logger()

APP_NAME = "python-toolkit"
APP_VERSION = "0.13.0"
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

    except FileNotFoundError as error:
        logger.error("%s", error)
        print(f"Error: {error}")

    except NotADirectoryError as error:
        logger.error("%s", error)
        print(f"Error: {error}")
