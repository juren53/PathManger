#!/usr/bin/env python3
"""
Verify version updates comply with Project_Rules.md
"""

def test_changelog_format():
    """Test CHANGELOG follows correct format"""
    try:
        with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for proper version format
        assert '## [0.2.0a] - Thu 08 Jan 2026 11:32:00 AM CST' in content, "Version format incorrect in CHANGELOG"
        assert 'CST' in content, "Timezone indicator missing from CHANGELOG"
        
        print("OK: CHANGELOG version format follows Project_Rules.md")
        return True
    except Exception as e:
        print(f"ERROR: CHANGELOG format issue: {e}")
        return False

def test_gui_version_format():
    """Test GUI version format"""
    try:
        with open('gui/gui_main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check status bar version
        assert 'v0.2.0a 2026-01-08 1132 CST' in content, "Status bar version format incorrect"
        assert 'Version:</b> v0.2.0a' in content, "About dialog version format incorrect"
        
        print("OK: GUI version format follows Project_Rules.md")
        return True
    except Exception as e:
        print(f"ERROR: GUI version format issue: {e}")
        return False

def test_entry_point_version():
    """Test main entry point version"""
    try:
        with open('pathmanager.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check header comment and argument version
        assert 'Version: v0.2.0a 2026-01-08 1132 CST' in content, "Header version format incorrect"
        assert 'version="PathManager v0.2.0a 2026-01-08 1132 CST"' in content, "Argument version format incorrect"
        
        print("OK: Entry point version format follows Project_Rules.md")
        return True
    except Exception as e:
        print(f"ERROR: Entry point version format issue: {e}")
        return False

def test_core_version():
    """Test core module version"""
    try:
        with open('core/__init__.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert '__version__ = "0.2.0a"' in content, "Core version format incorrect"
        
        print("OK: Core module version updated")
        return True
    except Exception as e:
        print(f"ERROR: Core version issue: {e}")
        return False

def main():
    print("Verifying Version Updates Compliance with Project_Rules.md")
    print("=" * 60)
    
    success = True
    
    if not test_changelog_format():
        success = False
    if not test_gui_version_format():
        success = False
    if not test_entry_point_version():
        success = False
    if not test_core_version():
        success = False
    
    print("=" * 60)
    if success:
        print("SUCCESS: All version formats comply with Project_Rules.md!")
        print("\nVersion format requirements met:")
        print("  ✓ Version Number: v0.2.0a")
        print("  ✓ Date: 2026-01-08")
        print("  ✓ Time: 1132")
        print("  ✓ Timezone: CST")
        print("  ✓ CHANGELOG format: Thu 08 Jan 2026 11:32:00 AM CST")
        return 0
    else:
        print("ERROR: Some version formats don't comply with Project_Rules.md")
        return 1

if __name__ == "__main__":
    exit(main())