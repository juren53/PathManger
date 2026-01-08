"""
PathManager GUI - Graphical User Interface

PyQt6-based GUI for viewing and managing PATH.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QStatusBar, QHeaderView, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
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

                # Color code by source
                if entry.source == "system":
                    source_item.setBackground(QColor(173, 216, 230))  # Light blue
                elif entry.source == "user":
                    source_item.setBackground(QColor(144, 238, 144))  # Light green

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


def run_gui():
    """Run the GUI version of PathManager"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look across platforms

    window = PathManagerWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(run_gui())
