# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0b] - Thu 08 Jan 2026 02:00:00 PM CST

### Added
- Window geometry persistence: GUI now saves and restores window size and position between sessions

### Changed
- Improved Source column contrast in GUI table with bold dark backgrounds and off-white text
  - System entries: Dark blue background (#003C78) with off-white text
  - User entries: Dark green background (#006400) with off-white text
  - Environment entries: Light gray text for subtle appearance
- Improved search result highlighting with white text on grey backgrounds for better readability
  - Regular matches: Medium grey background with white text
  - Current match: Dark grey background with white text

## [0.2.0a] - Thu 08 Jan 2026 11:32:00 AM CST

### Added
- Quick Reference Guide (`QUICK_REFERENCE.md`) with comprehensive command and GUI documentation
- Help menu items in GUI for Quick Reference Guide (F1) and Change Log
- Markdown-based documentation viewer in GUI with proper formatting
- Updated version to v0.2.0a in GUI status bar and About dialog

### Changed
- Enhanced Help menu accessibility with keyboard shortcuts (F1 for Quick Reference)
- Improved user documentation accessibility through integrated GUI help system

## [0.2.0] - 2026-01-08

### Added
- **Phase 1: Foundation & Basic GUI - Complete**
- Modular architecture with three-layer design (core/cli/gui)
- `core/path_analyzer.py`: Core business logic module
  - `PathAnalyzer` class for reading and analyzing PATH
  - Windows registry integration (reads User and System PATH separately)
  - Cross-platform support with OS detection
  - Directory existence checking
  - `PathEntry` class for structured PATH data
- `cli/cli_main.py`: Refactored command-line interface
  - Uses PathAnalyzer for core logic
  - Displays User/System PATH distinction on Windows
  - Shows missing directory warnings with [NOT FOUND] indicator
  - Summary statistics (User, System, Combined counts)
- `gui/gui_main.py`: PyQt6 graphical user interface
  - Main window with table view (1000x600)
  - System information header
  - Color-coded PATH entries (blue=System, green=User)
  - Status indicators (✓ OK, ✗ Not Found)
  - Status bar with summary statistics
  - Sortable columns and alternating row colors
- `requirements.txt`: Python dependencies file
- `PLAN_PathManager-project.md`: Comprehensive 5-phase development roadmap
- `CLAUDE.md`: AI assistant guidance for future development
- Command-line arguments: `--gui`, `--help`, `--version`
- Package structure with `__init__.py` files for all modules

### Changed
- Renamed `check-path.py` to `pathmanager.py` (completed in previous version)
- `pathmanager.py` refactored as main entry point with argument parsing
  - Default: CLI mode
  - `--gui` flag: Launch GUI mode
  - `--version` flag: Show version number (0.2.0)
- README.md completely rewritten with:
  - New usage instructions for both CLI and GUI modes
  - Architecture documentation
  - Updated project structure
  - Development roadmap summary
  - Enhanced features list

### Technical Details
- Windows registry reading from:
  - User PATH: `HKEY_CURRENT_USER\Environment`
  - System PATH: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment`
- CLI and GUI both use shared PathAnalyzer for consistency
- PyQt6 Fusion style for modern cross-platform appearance

## [0.1.0] - 2026-01-08

### Added
- Initial release of PathManager
- `check-path.py`: Python script to display system PATH environment variable entries
  - Cross-platform support (Windows, Linux, macOS)
  - Formatted output with numbered entries
  - Path separator detection based on operating system
- `How-check-path-works.txt`: Documentation explaining the check-path.py functionality
