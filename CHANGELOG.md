# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- System information header displaying machine name, OS, hardware architecture, and timestamp
- README.md with comprehensive project documentation
- CHANGELOG.md to track version history
- Project_Rules.md defining project conventions (timezone, versioning)

### Changed
- Renamed `check-path.py` to `pathmanager.py` for better project alignment
- Enhanced output with formatted system information section

## [0.1.0] - 2026-01-08

### Added
- Initial release of PathManager
- `check-path.py`: Python script to display system PATH environment variable entries
  - Cross-platform support (Windows, Linux, macOS)
  - Formatted output with numbered entries
  - Path separator detection based on operating system
- `How-check-path-works.txt`: Documentation explaining the check-path.py functionality
