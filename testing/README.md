# Testing Directory

This directory contains test scripts used during PathManager development.

## Test Files

- `test_help_menu.py` - Tests Help menu functionality and file access
- `test_help_simple.py` - Simple tests for Help menu components
- `verify_version_compliance.py` - Verifies version format compliance with Project_Rules.md
- `quick_version_test.py` - Quick version verification test
- `test_version_update.py` - Tests version update functionality

## Usage

Run tests from project root:
```bash
python testing/test_help_simple.py
python testing/verify_version_compliance.py
```

## Notes

- These are development/testing scripts, not part of the main PathManager distribution
- Tests may require PyQt6 for GUI functionality
- Tests are designed to work with Windows Command Prompt (no special Unicode characters)
- All tests include proper error handling and clear output formatting