#!/usr/bin/env python3
"""Quick test to verify GUI version updates"""

def test_gui_imports():
    try:
        import sys
        sys.path.append('.')
        import core
        import gui.gui_main
        
        print(f"Core version: {core.__version__}")
        print("OK: GUI and core modules import successfully")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    test_gui_imports()