"""
Command Line Interface for Python Toolkit.

This module is responsible for parsing command-line arguments
and displaying help/version information.
"""

import argparse

from toolkit.organizer import (
    create_category_folders,
    move_files,
)

APP_NAME = "python-toolkit"
APP_VERSION = "0.4.0"
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

    if args.command == "organize":
        create_category_folders(args.directory)
        move_files(args.directory)