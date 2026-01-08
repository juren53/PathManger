"""
PathManager GUI - Graphical User Interface

PyQt6-based GUI for viewing and managing PATH.
"""

import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QStatusBar, QHeaderView, QLabel, QHBoxLayout,
    QMenuBar, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QAction
from core.path_analyzer import PathAnalyzer


class PathManagerWindow(QMainWindow):
    """Main window for PathManager GUI"""

    def __init__(self):
        super().__init__()
        self.analyzer = PathAnalyzer()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("PathManager - PATH Environment Manager")
        self.setGeometry(100, 100, 1000, 600)

        # Create menu bar
        self.create_menu_bar()

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add system information header
        header_layout = self.create_header()
        layout.addLayout(header_layout)

        # Create table widget
        self.table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.table)

        # Populate table with PATH data
        self.populate_table()

        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.update_status_bar()

    def create_header(self) -> QHBoxLayout:
        """Create system information header"""
        header_layout = QHBoxLayout()

        info = self.analyzer.get_system_info()

        # Create labels for system info
        title_label = QLabel("PathManager")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)

        info_text = f"{info['machine_name']} | {info['os_name']} {info['os_version']} | {info['hardware']}"
        info_label = QLabel(info_text)
        info_label.setStyleSheet("color: gray;")

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(info_label)

        return header_layout

    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("&File")

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit PathManager")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")
        edit_menu.setEnabled(False)  # Disabled for Phase 1
        edit_menu.setStatusTip("Edit features coming in Phase 4")

        # Config Menu
        config_menu = menubar.addMenu("&Config")
        config_menu.setEnabled(False)  # Disabled for Phase 1
        config_menu.setStatusTip("Configuration features coming soon")

        # Help Menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About PathManager", self)
        about_action.setStatusTip("About PathManager")
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        """Display the About dialog"""
        about_text = """<h2>PathManager</h2>
        <p><b>Version:</b> 0.2.0</p>
        <p><b>Date:</b> 2026-01-08</p>
        <p><b>Status:</b> Phase 1 Complete - Foundation & Basic GUI</p>
        <br>
        <p>A Python utility for viewing and managing system PATH environment variables.</p>
        <br>
        <p><b>Current Features:</b></p>
        <ul>
        <li>Cross-platform PATH viewing (Windows, Linux, macOS)</li>
        <li>Windows registry integration (User & System PATH)</li>
        <li>Directory existence checking</li>
        <li>Dual CLI and GUI interfaces</li>
        </ul>
        <br>
        <p><b>Coming Soon:</b></p>
        <ul>
        <li>Phase 2: Problem Detection (duplicates, ordering issues)</li>
        <li>Phase 3: Backup System</li>
        <li>Phase 4: PATH Modification</li>
        <li>Phase 5: Polish & Distribution</li>
        </ul>
        <br>
        <p><b>Author:</b> Jim U'Ren</p>
        <p><b>License:</b> Personal and educational use</p>
        <p><b>Repository:</b> <a href="https://github.com/juren53/PathManger">github.com/juren53/PathManger</a></p>
        """

        QMessageBox.about(self, "About PathManager", about_text)

    def setup_table(self):
        """Set up the table widget structure"""
        # Define columns
        if self.analyzer.is_windows():
            columns = ["#", "Path", "Source", "Status"]
        else:
            columns = ["#", "Path", "Status"]

        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        # Set table properties
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # #
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Path
        if self.analyzer.is_windows():
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Source
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Status
        else:
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Status

    def populate_table(self):
        """Populate table with PATH entries"""
        entries = self.analyzer.get_path_entries()
        self.table.setRowCount(len(entries))

        for row, entry in enumerate(entries):
            # Column 0: Index
            index_item = QTableWidgetItem(str(entry.index + 1))
            index_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, index_item)

            # Column 1: Path
            path_item = QTableWidgetItem(entry.path)
            self.table.setItem(row, 1, path_item)

            # Column 2: Source (Windows) or Status (Unix)
            if self.analyzer.is_windows():
                source_item = QTableWidgetItem(entry.source.capitalize())
                source_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Color code by source with better contrast
                if entry.source == "system":
                    source_item.setBackground(QColor(220, 240, 255))  # Very light blue
                    source_item.setForeground(QColor(0, 80, 140))     # Dark blue text
                elif entry.source == "user":
                    source_item.setBackground(QColor(230, 255, 230))  # Very light green
                    source_item.setForeground(QColor(0, 100, 0))      # Dark green text
                else:
                    # Environment (fallback)
                    source_item.setForeground(QColor(100, 100, 100))  # Gray text

                self.table.setItem(row, 2, source_item)

                # Column 3: Status
                status_item = self.create_status_item(entry)
                self.table.setItem(row, 3, status_item)
            else:
                # Column 2: Status
                status_item = self.create_status_item(entry)
                self.table.setItem(row, 2, status_item)

    def create_status_item(self, entry) -> QTableWidgetItem:
        """Create a status table item for a PATH entry"""
        if entry.exists:
            status_item = QTableWidgetItem("✓ OK")
            status_item.setForeground(QColor(0, 128, 0))  # Green
        else:
            status_item = QTableWidgetItem("✗ Not Found")
            status_item.setForeground(QColor(255, 0, 0))  # Red

        status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return status_item

    def update_status_bar(self):
        """Update status bar with summary information"""
        total = self.analyzer.get_entry_count()
        missing = sum(1 for entry in self.analyzer.get_path_entries() if not entry.exists)

        status_text = f"Total entries: {total}"

        if self.analyzer.is_windows():
            user_count = len(self.analyzer.get_user_path())
            system_count = len(self.analyzer.get_system_path())
            status_text += f" | User: {user_count} | System: {system_count}"

        if missing > 0:
            status_text += f" | Missing directories: {missing}"

        self.statusBar.showMessage(status_text)

        # Add subdued version datestamp on the right
        version_label = QLabel("v0.2.0 | 2026-01-08")
        version_label.setStyleSheet("color: #888888; font-size: 9pt;")
        self.statusBar.addPermanentWidget(version_label)


def run_gui():
    """Run the GUI version of PathManager"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look across platforms

    window = PathManagerWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(run_gui())
