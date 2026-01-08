# PathManager

A Python utility for viewing and managing system PATH environment variables across different operating systems.

## Overview

PathManager provides tools to help you understand and manage your system's PATH environment variable. The PATH variable is crucial for determining where your system looks for executable programs, and this tool makes it easy to view and analyze these entries.

## Features

- **Cross-platform compatibility**: Works on Windows, Linux, and macOS
- **Clean, formatted output**: Displays PATH entries in a numbered, easy-to-read format
- **Automatic OS detection**: Handles different path separators (`;` for Windows, `:` for Unix-like systems)
- **Entry counting**: Shows the total number of PATH entries

## Requirements

- Python 3.x
- No external dependencies (uses only Python standard library)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/juren53/PathManger.git
   cd PathManger
   ```

2. The scripts are ready to use without any additional installation.

## Usage

### check-path.py

Display all entries in your system's PATH environment variable:

```bash
python3 check-path.py
```

**Output example:**
```
####################
System PATH Entries (15 total)
####################

01 | /usr/local/bin
02 | /usr/bin
03 | /bin
...
```

## How It Works

The `check-path.py` script uses Python's built-in modules to:

1. **Extract PATH**: Uses `os.environ.get('PATH')` to retrieve the PATH environment variable
2. **Detect separator**: Uses `os.pathsep` to automatically determine the correct separator:
   - Windows: `;` (semicolon)
   - Linux/macOS: `:` (colon)
3. **Parse entries**: Splits the PATH string into individual directory entries
4. **Format output**: Uses `enumerate()` to create numbered, aligned output

## Project Structure

```
PathManager/
├── check-path.py              # Main script to display PATH entries
├── How-check-path-works.txt   # Technical documentation
├── CHANGELOG.md               # Version history and changes
└── README.md                  # This file
```

## Contributing

This is a personal project, but suggestions and improvements are welcome. Feel free to open an issue or submit a pull request.

## Future Enhancements

Potential features under consideration:
- Validate whether PATH directories actually exist on disk
- Add/remove PATH entries programmatically
- Detect duplicate entries
- Export PATH configuration to file
- Compare PATH across different environments

## License

This project is available for personal and educational use.

## Author

Jim U'Ren - [GitHub](https://github.com/juren53)
