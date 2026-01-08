# PathManager

A Python utility for viewing and managing system PATH environment variables across different operating systems.

## Overview

PathManager provides tools to help you understand and manage your system's PATH environment variable. The PATH variable is crucial for determining where your system looks for executable programs, and this tool makes it easy to view and analyze these entries.

Available in both **CLI** (command-line) and **GUI** (graphical) modes.

## Features

- **Dual Interface**: Choose between CLI or GUI mode
- **Cross-platform compatibility**: Works on Windows, Linux, and macOS
- **Windows-specific features**:
  - Reads User and System PATH separately from Windows registry
  - Distinguishes between User and System PATH entries
  - Detects missing directories
- **Clean, formatted output**: Displays PATH entries in a numbered, easy-to-read format
- **Automatic OS detection**: Handles different path separators (`;` for Windows, `:` for Unix-like systems)
- **Entry counting**: Shows the total number of PATH entries

## Requirements

- Python 3.7+
- **For CLI mode**: No external dependencies (uses only Python standard library)
- **For GUI mode**: PyQt6 (install via pip)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/juren53/PathManger.git
   cd PathManger
   ```

2. (Optional) Install GUI dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or install PyQt6 directly:
   ```bash
   pip install PyQt6
   ```

## Usage

### CLI Mode (Default)

Display all entries in your system's PATH environment variable:

```bash
python pathmanager.py
```

**Output example (Windows):**
```
============================================================
PathManager - System Information
============================================================
Machine Name: YOUR-PC
Operating System: Windows 11
Hardware: AMD64
Date: 2026-01-08 10:34:02
============================================================

####################
System PATH Entries (45 total)
####################

01 | C:\Windows\system32 [S]
02 | C:\Users\YourName\AppData\Local\Programs\Python [U]
03 | C:\Program Files\Git\cmd [S]
...

Path Summary:
  User PATH entries: 12
  System PATH entries: 33
  Combined PATH entries: 45

Legend: [U] = User PATH, [S] = System PATH, [NOT FOUND] = Directory missing
```

### GUI Mode

Launch the graphical interface:

```bash
python pathmanager.py --gui
```

The GUI displays:
- System information header
- Table view of all PATH entries
- Color-coded source (User/System on Windows)
- Status indicators (✓ OK or ✗ Not Found)
- Summary statistics in status bar

### Other Options

```bash
python pathmanager.py --help      # Show help message
python pathmanager.py --version   # Show version
```

## How It Works

PathManager uses a modular architecture:

1. **Core Module** (`core/`): Business logic
   - `PathAnalyzer`: Reads PATH from environment or Windows registry
   - Detects OS and uses appropriate path separator (`;` for Windows, `:` for Unix)
   - On Windows, reads User PATH and System PATH separately from registry
   - Checks if directories exist on disk

2. **CLI Module** (`cli/`): Command-line interface
   - Formats output for terminal display
   - Shows system information and PATH entries

3. **GUI Module** (`gui/`): Graphical interface (PyQt6)
   - Table view with sortable columns
   - Color-coded entries (blue=System, green=User)
   - Status indicators for missing directories

## Project Structure

```
PathManager/
├── core/
│   ├── __init__.py
│   └── path_analyzer.py           # Core PATH analysis logic
├── cli/
│   ├── __init__.py
│   └── cli_main.py                # CLI interface
├── gui/
│   ├── __init__.py
│   ├── gui_main.py                # GUI main window
│   ├── widgets/                   # Custom widgets (future)
│   └── dialogs/                   # Dialog windows (future)
├── pathmanager.py                 # Main entry point
├── requirements.txt               # Python dependencies
├── CHANGELOG.md                   # Version history
├── PLAN_PathManager-project.md    # Development roadmap
├── CLAUDE.md                      # AI assistant guidance
└── README.md                      # This file
```

## Contributing

This is a personal project, but suggestions and improvements are welcome. Feel free to open an issue or submit a pull request.

## Roadmap

See `PLAN_PathManager-project.md` for the full development plan. Upcoming features:

**Phase 1 (Current)**: Foundation & Basic GUI ✓
- Modular architecture
- CLI and GUI working in parallel
- Windows registry integration

**Phase 2**: Problem Detection
- Duplicate detection
- Non-existent directory detection
- Ordering issues (shadowed executables)
- Windows-specific issues (path length, invalid characters)

**Phase 3**: Backup System
- Automatic backup before modifications
- Backup browser and restore functionality

**Phase 4**: PATH Modification
- Add/remove/reorder PATH entries
- Smart cleanup operations
- Safe modification with preview and confirmation

**Phase 5**: Polish & Windows 11 Integration
- Modern Windows 11 UI
- Installer/distribution
- System tray integration

## License

This project is available for personal and educational use.

## Author

Jim U'Ren - [GitHub](https://github.com/juren53)
