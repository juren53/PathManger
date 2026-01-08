"""
PathManager CLI - Command Line Interface

Provides a text-based interface for viewing and analyzing PATH.
"""

import sys
from core.path_analyzer import PathAnalyzer


def run_cli(show_all: bool = False):
    """
    Run the CLI version of PathManager

    Args:
        show_all: If True, show all PATH entries. If False, show first 20.
    """
    try:
        # Create analyzer
        analyzer = PathAnalyzer()

        # Print system information header
        print(analyzer.format_system_info_header())

        # Print PATH entries (limit to 20 unless show_all is True)
        limit = None if show_all else 20
        print(analyzer.format_path_list(limit=limit))

        # Print summary for Windows
        if analyzer.is_windows():
            print(f"\nPath Summary:")
            user_count = len(analyzer.get_user_path())
            system_count = len(analyzer.get_system_path())
            combined_count = analyzer.get_entry_count()
            print(f"  User PATH entries: {user_count:<8}System PATH entries: {system_count:<8}Combined PATH entries: {combined_count}")
            print(f"\nLegend: [U] = User PATH, [S] = System PATH")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(run_cli())
