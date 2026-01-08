# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PathManager is a Python utility for viewing and managing system PATH environment variables across different operating systems (Windows, Linux, macOS). It features both CLI and GUI interfaces that share a common business logic core.

**Current Status**: Phase 1 complete (v0.2.0) - Foundation & Basic GUI
**Next Phase**: Phase 2 - Problem Detection (duplicates, missing dirs, ordering issues, Windows-specific problems)

## Development Commands

### Running the Application

**CLI Mode (default):**
```bash
python pathmanager.py
# or
python pathmanager.py --help
python pathmanager.py --version
```

**GUI Mode:**
```bash
python pathmanager.py --gui
```

Note: GUI requires PyQt6. Install with: `pip install -r requirements.txt`

### Installing Dependencies
```bash
pip install -r requirements.txt  # Installs PyQt6
```

### Testing
This project currently has no automated tests. Manual testing involves:

**CLI Testing:**
- Run `python pathmanager.py` and verify:
  - System information displays correctly
  - PATH entries are numbered and formatted
  - User/System distinction shown on Windows (e.g., [U], [S] indicators)
  - Missing directories flagged with [NOT FOUND]
  - Summary statistics displayed (Windows)

**GUI Testing:**
- Run `python pathmanager.py --gui` and verify:
  - Window launches without errors
  - Table displays all PATH entries
  - Source column shows User/System (Windows only)
  - Status column shows ✓ OK or ✗ Not Found
  - Color coding: System=light blue, User=light green
  - Status bar shows correct counts
  - Window resizing works properly

## Code Architecture

PathManager uses a **three-layer modular architecture** to support both CLI and GUI interfaces sharing the same business logic:

```
pathmanager/
├── core/                      # Business Logic Layer
│   ├── path_analyzer.py      # PathAnalyzer class - core PATH operations
│   └── __init__.py
├── cli/                       # CLI Presentation Layer
│   ├── cli_main.py           # Command-line interface
│   └── __init__.py
├── gui/                       # GUI Presentation Layer
│   ├── gui_main.py           # PyQt6 main window
│   ├── widgets/              # Custom widgets (future)
│   ├── dialogs/              # Dialog windows (future)
│   └── __init__.py
└── pathmanager.py            # Entry point with argument parsing
```

### Key Components

**`core/path_analyzer.py`** - Core business logic:
- `PathEntry` class: Represents a single PATH entry with metadata (path, index, source, exists)
- `PathAnalyzer` class: Main analyzer
  - `__init__()`: Auto-loads PATH based on OS
  - `_load_windows_path()`: Reads from Windows registry (User & System PATH)
  - `_load_unix_path()`: Reads from environment variable
  - `get_path_entries()`: Returns list of PathEntry objects
  - `get_system_info()`: Returns dict of system information
  - `is_windows()`: OS detection helper

**Windows Registry Access:**
- User PATH: `HKEY_CURRENT_USER\Environment`
- System PATH: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment`

**`cli/cli_main.py`** - CLI interface:
- `run_cli()`: Main CLI function
- Uses PathAnalyzer to get data
- Formats output for terminal display

**`gui/gui_main.py`** - GUI interface:
- `PathManagerWindow` class: Main QMainWindow
- `run_gui()`: Entry point for GUI mode
- Uses PathAnalyzer for data
- PyQt6 components: QTableWidget, QStatusBar

**`pathmanager.py`** - Entry point:
- Argument parsing with `argparse`
- Routes to CLI or GUI based on `--gui` flag
- Handles import errors gracefully

### Design Principles

1. **Separation of Concerns**: Business logic in `core/`, presentation in `cli/` and `gui/`
2. **Code Reuse**: Both interfaces use the same PathAnalyzer class
3. **No Duplication**: PATH reading logic exists only in core module
4. **Future-Ready**: Architecture supports Phase 2-5 enhancements

## Project Conventions

### Timezone
**CRITICAL**: All timestamps and dates MUST use Central Time USA (CST/CDT), never UTC.
- Changelog format: `Tue 03 Dec 2025 09:20:00 PM CST`
- Version label format: `v0.0.9b 2025-12-03`
- Always include timezone indicator (CST or CDT)

### Version Numbering
- Format: `v0.0.X` for releases
- Format: `v0.0.Xa`, `v0.0.Xb`, `v0.0.Xc` for point releases/patches
- Update version info in README.md, CHANGELOG.md, and code comments when making releases
- Version info must include version number, date, AND time (CST/CDT)

### Documentation
- CHANGELOG.md follows [Keep a Changelog](https://keepachangelog.com/) format
- Project adheres to [Semantic Versioning](https://semver.org/)
- See PLAN_PathManager-project.md for full development roadmap

## Development Roadmap

**Phase 1** ✓ Complete (v0.2.0)
- Modular architecture established
- CLI and GUI both functional
- Windows registry integration

**Phase 2** - Next (Problem Detection)
- Duplicate detection
- Non-existent directory detection
- Ordering issues (shadowed executables)
- Windows-specific issues (path length, invalid characters)

**Phase 3** - Backup System
- Auto-backup before modifications
- Backup browser and restore

**Phase 4** - PATH Modification
- Add/remove/reorder PATH entries
- Preview and confirmation system

**Phase 5** - Polish & Distribution
- Windows 11 UI styling
- Installer
- System tray integration

## Important Notes for Future Development

1. **Never break the CLI**: When adding features, ensure CLI mode continues to work
2. **Shared Logic**: New features should be implemented in `core/` modules, not in CLI or GUI
3. **Windows Focus**: This tool is optimized for Windows 11, but should remain cross-platform
4. **Safety First**: When implementing PATH modification (Phase 4), always backup first
5. **Python Path**: On this system, use `C:\Users\jimur\AppData\Local\Microsoft\WindowsApps\python.exe` for testing with PyQt6
