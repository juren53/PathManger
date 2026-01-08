# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
