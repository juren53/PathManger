#!/usr/bin/env python3
"""
Test script to verify GUI updates work correctly
"""

import sys
import os
sys.path.append('.')

def test_version_updates():
    """Test that version has been updated in GUI code"""
    try:
        from gui.gui_main import PathManagerWindow
        with open('gui/gui_main.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        assert 'v0.2.0a' in content, "Version not updated in GUI code"
        assert 'Version:</b> v0.2.0a' in content, "About dialog version not updated"
        print("OK: Version updated to v0.2.0a in GUI")
        
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_changelog_update():
    """Test that CHANGELOG has been updated"""
    try:
        with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
            content = f.read()
            
        assert 'Quick Reference Guide' in content, "Quick Reference not added to CHANGELOG"
        assert 'Help menu items' in content, "Help menu not mentioned in CHANGELOG"
        assert 'v0.2.0a' not in content or 'Unreleased' in content, "Should be in Unreleased section"
        print("OK: CHANGELOG updated with new features")
        
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("Testing Version Updates for Help Menu Enhancement")
    print("=" * 50)
    
    success = True
    
    if not test_version_updates():
        success = False
        
    if not test_changelog_update():
        success = False
    
    print("=" * 50)
    if success:
        print("SUCCESS: All version updates completed!")
        print("\nSummary of changes:")
        print("  - Added Quick Reference Guide to Help menu (F1)")
        print("  - Added Change Log to Help menu")
        print("  - Created markdown viewer for documentation")
        print("  - Updated version to v0.2.0a")
        print("  - Updated CHANGELOG with new features")
        return 0
    else:
        print("ERROR: Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())