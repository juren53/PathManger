#!/usr/bin/env python3
"""
PathManager - PATH Environment Variable Manager

A cross-platform tool for viewing and managing system PATH variables.
Supports both CLI and GUI modes.

Usage:
    python pathmanager.py           # Run in CLI mode (default)
    python pathmanager.py --gui     # Run in GUI mode
    python pathmanager.py --help    # Show help message

Version: 0.2.0
Author: Jim U'Ren
License: Personal and educational use
"""

import sys
import argparse


def main():
    """Main entry point for PathManager"""
    parser = argparse.ArgumentParser(
        description="PathManager - View and manage your system PATH environment variable",
        epilog="For more information, see README.md"
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the graphical user interface (requires PyQt6)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="PathManager 0.2.0"
    )

    args = parser.parse_args()

    # Launch appropriate interface
    if args.gui:
        try:
            from gui.gui_main import run_gui
            return run_gui()
        except ImportError as e:
            print("Error: PyQt6 is required for GUI mode.", file=sys.stderr)
            print("Install it with: pip install PyQt6", file=sys.stderr)
            print(f"Details: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error launching GUI: {e}", file=sys.stderr)
            return 1
    else:
        # Default: CLI mode
        try:
            from cli.cli_main import run_cli
            return run_cli()
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1


if __name__ == "__main__":
    sys.exit(main())
