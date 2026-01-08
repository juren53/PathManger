"""
PathManager CLI - Command Line Interface

Provides a text-based interface for viewing and analyzing PATH.
"""

import sys
from core.path_analyzer import PathAnalyzer


def run_cli():
    """Run the CLI version of PathManager"""
    try:
        # Create analyzer
        analyzer = PathAnalyzer()

        # Print system information header
        print(analyzer.format_system_info_header())

        # Print PATH entries
        print(analyzer.format_path_list())

        # Print summary for Windows
        if analyzer.is_windows():
            print(f"\nPath Summary:")
            print(f"  User PATH entries: {len(analyzer.get_user_path())}")
            print(f"  System PATH entries: {len(analyzer.get_system_path())}")
            print(f"  Combined PATH entries: {analyzer.get_entry_count()}")
            print(f"\nLegend: [U] = User PATH, [S] = System PATH")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(run_cli())
