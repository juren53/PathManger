"""
PathAnalyzer - Core PATH reading and analysis functionality

This module provides the PathAnalyzer class which handles reading PATH
from environment variables and Windows registry, parsing entries, and
providing structured data for both CLI and GUI interfaces.
"""

import os
import platform
import socket
from datetime import datetime
from typing import List, Dict, Tuple, Optional


class PathEntry:
    """Represents a single PATH entry with metadata"""

    def __init__(self, path: str, index: int, source: str = "environment"):
        self.path = path
        self.index = index
        self.source = source  # "user", "system", or "environment"
        self.exists = os.path.exists(path)

    def __repr__(self):
        return f"PathEntry(index={self.index}, path='{self.path}', source='{self.source}', exists={self.exists})"


class PathAnalyzer:
    """
    Analyzes system PATH configuration across different operating systems.

    On Windows, distinguishes between User and System PATH entries.
    On Unix-like systems, reads from the environment variable.
    """

    def __init__(self):
        self.os_name = platform.system()
        self.os_version = platform.release()
        self.hardware = platform.machine()
        self.machine_name = socket.gethostname()
        self.separator = os.pathsep  # ';' on Windows, ':' on Unix

        # Storage for PATH entries
        self.user_path: List[str] = []
        self.system_path: List[str] = []
        self.combined_path: List[str] = []
        self.entries: List[PathEntry] = []

        # Load PATH data
        self._load_path()

    def _load_path(self):
        """Load PATH from appropriate source based on OS"""
        if self.os_name == "Windows":
            self._load_windows_path()
        else:
            self._load_unix_path()

    def _load_windows_path(self):
        """
        Load PATH from Windows registry (User and System) and environment.

        On Windows, PATH can come from multiple sources:
        - User PATH: HKEY_CURRENT_USER\\Environment
        - System PATH: HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment
        - The environment variable combines both (System + User typically)
        """
        try:
            import winreg

            # Try to read User PATH from registry
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ) as key:
                    user_path_string, _ = winreg.QueryValueEx(key, "Path")
                    self.user_path = [p for p in user_path_string.split(self.separator) if p]
            except (WindowsError, FileNotFoundError):
                self.user_path = []

            # Try to read System PATH from registry (requires read access, not admin)
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                   r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                                   0, winreg.KEY_READ) as key:
                    system_path_string, _ = winreg.QueryValueEx(key, "Path")
                    self.system_path = [p for p in system_path_string.split(self.separator) if p]
            except (WindowsError, FileNotFoundError):
                self.system_path = []

            # Get the actual combined PATH from environment
            env_path = os.environ.get('PATH', '')
            self.combined_path = [p for p in env_path.split(self.separator) if p]

            # Create PathEntry objects
            # Mark entries as user or system based on registry data
            index = 0
            for path in self.combined_path:
                # Determine source (this is approximate since combined PATH may have been modified)
                source = "environment"
                if path in self.system_path:
                    source = "system"
                elif path in self.user_path:
                    source = "user"

                entry = PathEntry(path, index, source)
                self.entries.append(entry)
                index += 1

        except ImportError:
            # winreg not available (not on Windows), fall back to environment
            self._load_unix_path()

    def _load_unix_path(self):
        """Load PATH from environment variable (Unix-like systems)"""
        env_path = os.environ.get('PATH', '')
        self.combined_path = [p for p in env_path.split(self.separator) if p]

        # Create PathEntry objects
        for index, path in enumerate(self.combined_path):
            entry = PathEntry(path, index, "environment")
            self.entries.append(entry)

    def get_system_info(self) -> Dict[str, str]:
        """Get system information as a dictionary"""
        return {
            "machine_name": self.machine_name,
            "os_name": self.os_name,
            "os_version": self.os_version,
            "hardware": self.hardware,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def get_path_entries(self) -> List[PathEntry]:
        """Get all PATH entries as PathEntry objects"""
        return self.entries

    def get_path_list(self) -> List[str]:
        """Get PATH as a simple list of strings"""
        return self.combined_path

    def get_user_path(self) -> List[str]:
        """Get User PATH (Windows only)"""
        return self.user_path

    def get_system_path(self) -> List[str]:
        """Get System PATH (Windows only)"""
        return self.system_path

    def get_entry_count(self) -> int:
        """Get total number of PATH entries"""
        return len(self.entries)

    def is_windows(self) -> bool:
        """Check if running on Windows"""
        return self.os_name == "Windows"

    def format_system_info_header(self) -> str:
        """Format system information as a text header"""
        info = self.get_system_info()
        header = f"{'=' * 60}\n"
        header += f"PathManager - System Information\n"
        header += f"{'=' * 60}\n"
        header += f"Machine Name: {info['machine_name']}\n"
        header += f"Operating System: {info['os_name']} {info['os_version']}\n"
        header += f"Hardware: {info['hardware']}\n"
        header += f"Date: {info['timestamp']}\n"
        header += f"{'=' * 60}\n"
        return header

    def format_path_list(self) -> str:
        """Format PATH entries as numbered list"""
        output = f"{'#' * 20}\n"
        output += f"System PATH Entries ({self.get_entry_count()} total)\n"
        output += f"{'#' * 20}\n\n"

        for entry in self.entries:
            # Add source indicator for Windows
            source_indicator = ""
            if self.is_windows() and entry.source != "environment":
                source_indicator = f" [{entry.source[0].upper()}]"  # [U] or [S]

            # Add existence indicator
            exists_indicator = "" if entry.exists else " [NOT FOUND]"

            output += f"{entry.index + 1:02d} | {entry.path}{source_indicator}{exists_indicator}\n"

        return output
