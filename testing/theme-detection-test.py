#!/usr/bin/env python3
"""
Test script to verify theme detection works for PathManager GUI dialogs
"""

import platform
import sys
import os

def is_dark_theme_fallback():
    """Fallback theme detection using Windows registry"""
    if platform.system() == "Windows":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                              r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as key:
                # 0 = light, 1 = dark
                apps_use_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return apps_use_light_theme == 0
        except Exception as e:
            print(f"Registry check failed: {e}")
            pass
    return False  # Default to light theme if detection fails

def test_qt_theme_detection():
    """Test Qt-based theme detection"""
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QPalette
        
        app = QApplication([])
        palette = app.palette()
        window_color = palette.color(QPalette.ColorRole.Window)
        window_text_color = palette.color(QPalette.ColorRole.WindowText)
        print(f'Window color RGB: ({window_color.red()}, {window_color.green()}, {window_color.blue()})')
        print(f'Window text color RGB: ({window_text_color.red()}, {window_text_color.green()}, {window_text_color.blue()})')
        
        # Calculate luminance
        def get_luminance(color):
            return (0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()) / 255
        
        bg_luminance = get_luminance(window_color)
        text_luminance = get_luminance(window_text_color)
        print(f'Background luminance: {bg_luminance:.2f}')
        print(f'Text luminance: {text_luminance:.2f}')
        print(f'Dark theme detected: {bg_luminance < text_luminance}')
        return bg_luminance < text_luminance
    except ImportError:
        print('PyQt6 not available - using fallback detection')
        return None
    except Exception as e:
        print(f'Qt theme detection failed: {e}')
        return None

if __name__ == "__main__":
    print("=== PathManager Theme Detection Test ===")
    print(f"Operating System: {platform.system()}")
    print(f"Platform: {platform.platform()}")
    print()
    
    # Test Qt-based detection (if available)
    qt_result = test_qt_theme_detection()
    print()
    
    # Test Windows registry detection
    if platform.system() == "Windows":
        dark_theme_registry = is_dark_theme_fallback()
        print(f"Windows registry dark theme detected: {dark_theme_registry}")
        
        # Also check system theme via registry if available
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                              r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as key:
                apps_use_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                system_use_light_theme, _ = winreg.QueryValueEx(key, "SystemUsesLightTheme")
                print(f"Apps use light theme: {apps_use_light_theme == 1}")
                print(f"System uses light theme: {system_use_light_theme == 1}")
                
                # Compare methods
                if qt_result is not None:
                    print(f"\nDetection method comparison:")
                    print(f"  Qt palette method: {'DARK' if qt_result else 'LIGHT'}")
                    print(f"  Registry method:   {'DARK' if dark_theme_registry else 'LIGHT'}")
                    print(f"  Methods agree: {qt_result == dark_theme_registry}")
        except Exception as e:
            print(f"Could not read theme registry: {e}")
    else:
        print("Non-Windows system - PyQt6 palette detection would be used")
    
    print("\n=== Test Completed ===")