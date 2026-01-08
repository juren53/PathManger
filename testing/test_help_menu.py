#!/usr/bin/env python3
"""
Test script to verify Help menu functionality in PathManager GUI
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_help_menu_methods():
    """Test if the Help menu methods are properly defined"""
    try:
        from gui.gui_main import PathManagerWindow
        window = PathManagerWindow()
        
        # Check if methods exist
        methods = dir(window)
        assert 'show_quick_reference' in methods, "show_quick_reference method not found"
        assert 'show_changelog' in methods, "show_changelog method not found"
        assert 'create_markdown_dialog' in methods, "create_markdown_dialog method not found"
        
        print("✓ All Help menu methods are properly defined")
        
        # Test markdown dialog creation (without showing)
        dialog = window.create_markdown_dialog("Test", "QUICK_REFERENCE.md")
        assert dialog is not None, "create_markdown_dialog returned None"
        
        print("✓ Markdown dialog creation works")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing Help menu methods: {e}")
        return False

def test_file_access():
    """Test if documentation files are accessible"""
    try:
        # Test QUICK_REFERENCE.md
        with open('QUICK_REFERENCE.md', 'r', encoding='utf-8') as f:
            content = f.read()
            assert len(content) > 100, "QUICK_REFERENCE.md seems too short"
            assert "PathManager" in content, "QUICK_REFERENCE.md doesn't contain PathManager"
        print("✓ QUICK_REFERENCE.md is accessible and contains content")
        
        # Test CHANGELOG.md
        with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
            content = f.read()
            assert len(content) > 100, "CHANGELOG.md seems too short"
            assert "0.2.0a" in content, "CHANGELOG.md doesn't contain version 0.2.0a"
        print("✓ CHANGELOG.md is accessible and contains content")
        
        return True
        
    except Exception as e:
        print(f"✗ Error accessing documentation files: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing PathManager Help Menu Functionality")
    print("=" * 50)
    
    success = True
    
    # Test file access
    if not test_file_access():
        success = False
    
    # Test Help menu methods (this might fail if PyQt6 is not available)
    try:
        if not test_help_menu_methods():
            success = False
    except ImportError as e:
        print(f"⚠ PyQt6 not available for GUI testing: {e}")
        print("  This is expected in environments without GUI support")
    
    print("=" * 50)
    if success:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())