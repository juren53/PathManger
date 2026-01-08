#!/usr/bin/env python3
"""
Simple test to verify documentation files are accessible
"""

def test_file_access():
    """Test if documentation files are accessible"""
    try:
        # Test QUICK_REFERENCE.md
        with open('QUICK_REFERENCE.md', 'r', encoding='utf-8') as f:
            content = f.read()
            assert len(content) > 100, "QUICK_REFERENCE.md seems too short"
            assert "PathManager" in content, "QUICK_REFERENCE.md doesn't contain PathManager"
        print("OK: QUICK_REFERENCE.md is accessible and contains content")
        
        # Test CHANGELOG.md
        with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
            content = f.read()
            assert len(content) > 100, "CHANGELOG.md seems too short"
            assert "0.2.0a" in content, "CHANGELOG.md doesn't contain version 0.2.0a"
        print("OK: CHANGELOG.md is accessible and contains content")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Error accessing documentation files: {e}")
        return False

def test_gui_code():
    """Test if GUI code has been new methods without creating widgets"""
    try:
        import sys
        import os
        sys.path.append('.')
        
        # Just import module to check for syntax errors
        from gui import gui_main
        print("OK: GUI module imports successfully")
        
        # Check if methods exist in class definition
        import inspect
        methods = [name for name, method in inspect.getmembers(gui_main.PathManagerWindow, predicate=inspect.isfunction)]
        
        assert 'show_quick_reference' in methods, "show_quick_reference method not found"
        assert 'show_changelog' in methods, "show_changelog method not found" 
        assert 'create_markdown_dialog' in methods, "create_markdown_dialog method not found"
        
        print("OK: All Help menu methods are defined in PathManagerWindow class")
        return True
        
    except Exception as e:
        print(f"ERROR: Error testing GUI code: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing PathManager Help Menu Components")
    print("=" * 50)
    
    success = True
    
    # Test file access
    if not test_file_access():
        success = False
    
    # Test GUI code
    if not test_gui_code():
        success = False
    
    print("=" * 50)
    if success:
        print("SUCCESS: All tests passed!")
        print("The Help menu should now include:")
        print("  - Quick Reference Guide (F1)")
        print("  - Change Log")
        print("  - About PathManager")
        return 0
    else:
        print("ERROR: Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())