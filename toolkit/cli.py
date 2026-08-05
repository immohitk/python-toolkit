"""
Command Line Interface for Python Toolkit.

This module is responsible for parsing command-line arguments
and displaying help/version information.
"""

import argparse

APP_NAME = "python-toolkit"
APP_VERSION = "0.1.1"
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

    return parser


def run():
    """
    Run the command-line interface.
    """
    parser = create_parser()
    parser.parse_args()