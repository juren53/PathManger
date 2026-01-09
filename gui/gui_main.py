"""
PathManager GUI - Graphical User Interface

PyQt6-based GUI for viewing and managing PATH.
"""

import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QStatusBar, QHeaderView, QLabel, QHBoxLayout,
    QMenuBar, QMessageBox, QLineEdit, QPushButton, QFrame, QDialog, QTextEdit
)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QColor, QFont, QAction, QKeySequence, QShortcut
from core.path_analyzer import PathAnalyzer


class PathManagerWindow(QMainWindow):
    """Main window for PathManager GUI"""

    def __init__(self):
        super().__init__()
        self.analyzer = PathAnalyzer()
        self.search_matches = []  # List of matching row indices
        self.current_match_index = -1  # Current position in search results
        self.settings = QSettings("PathManager", "PathManager")
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("PathManager - PATH Environment Manager")

        # Restore window geometry from settings, or use default
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.setGeometry(100, 100, 1000, 600)

        # Create menu bar
        self.create_menu_bar()

        # Add Q hotkey to quit (with smart context handling)
        quit_shortcut = QShortcut(QKeySequence("Q"), self)
        quit_shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        quit_shortcut.activated.connect(self.handle_quit_shortcut)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add system information header
        header_layout = self.create_header()
        layout.addLayout(header_layout)

        # Create search bar (initially hidden)
        self.search_bar = self.create_search_bar()
        layout.addWidget(self.search_bar)
        self.search_bar.hide()

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

    def create_search_bar(self) -> QFrame:
        """Create the search bar widget"""
        search_frame = QFrame()
        search_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        search_frame.setStyleSheet("""
            QFrame {
                background-color: #e8e8e8;
                padding: 5px;
            }
            QLabel {
                color: #000000;
            }
        """)

        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(5, 5, 5, 5)

        # Search label
        search_label = QLabel("Find:")
        search_label.setStyleSheet("color: #000000; font-weight: bold;")
        search_layout.addWidget(search_label)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search PATH entries...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #cccccc;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        self.search_input.returnPressed.connect(self.find_next)
        self.search_input.textChanged.connect(self.perform_search)
        search_layout.addWidget(self.search_input)

        # Match counter label
        self.match_label = QLabel("No matches")
        self.match_label.setStyleSheet("color: #666666; margin-left: 10px;")
        search_layout.addWidget(self.match_label)

        # Previous button
        prev_button = QPushButton("Previous")
        prev_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        prev_button.clicked.connect(self.find_previous)
        search_layout.addWidget(prev_button)

        # Next button
        next_button = QPushButton("Next")
        next_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        next_button.clicked.connect(self.find_next)
        search_layout.addWidget(next_button)

        # Close button
        close_button = QPushButton("✕")
        close_button.setFixedWidth(30)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c41408;
            }
        """)
        close_button.clicked.connect(self.hide_search_bar)
        search_layout.addWidget(close_button)

        return search_frame

    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("&File")

        # Add Find action to File menu
        find_action = QAction("&Find...", self)
        find_action.setShortcut("Ctrl+F")
        find_action.setStatusTip("Search PATH entries")
        find_action.triggered.connect(self.show_search_bar)
        file_menu.addAction(find_action)

        file_menu.addSeparator()

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

        quick_ref_action = QAction("&Quick Reference Guide", self)
        quick_ref_action.setStatusTip("Open Quick Reference Guide")
        quick_ref_action.setShortcut("F1")
        quick_ref_action.triggered.connect(self.show_quick_reference)
        help_menu.addAction(quick_ref_action)

        changelog_action = QAction("&Change Log", self)
        changelog_action.setStatusTip("View version history and changes")
        changelog_action.triggered.connect(self.show_changelog)
        help_menu.addAction(changelog_action)

        help_menu.addSeparator()

        about_action = QAction("&About PathManager", self)
        about_action.setStatusTip("About PathManager")
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        """Display the About dialog"""
        about_text = """<h2>PathManager</h2>
        <p><b>Version:</b> v0.2.0d</p>
        <p><b>Date:</b> 2026-01-09 2:00 PM CST</p>
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

    def show_quick_reference(self):
        """Display the Quick Reference Guide in a dialog"""
        dialog = self.create_markdown_dialog("Quick Reference Guide", "QUICK_REFERENCE.md")
        dialog.exec()

    def show_changelog(self):
        """Display the Change Log in a dialog"""
        dialog = self.create_markdown_dialog("Change Log", "CHANGELOG.md")
        dialog.exec()

    def create_markdown_dialog(self, title: str, filename: str) -> QDialog:
        """Create a dialog to display markdown files"""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setGeometry(100, 100, 900, 700)
        
        layout = QVBoxLayout(dialog)
        
        # Create text widget for content
        text_widget = QTextEdit()
        text_widget.setReadOnly(True)
        
        # Try to load the markdown file
        try:
            # Get the project root directory (where pathmanager.py is)
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(current_dir, filename)
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    text_widget.setMarkdown(content)
            else:
                text_widget.setPlainText(f"Error: Could not find {filename}\n\nExpected location: {file_path}")
        except Exception as e:
            text_widget.setPlainText(f"Error reading {filename}: {str(e)}")
        
        # Configure text widget appearance
        text_widget.setStyleSheet("""
            QTextEdit {
                font-family: 'Segoe UI', 'Microsoft YaHei', Arial, sans-serif;
                font-size: 10pt;
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
                padding: 8px;
            }
        """)
        
        layout.addWidget(text_widget)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        close_button.clicked.connect(dialog.accept)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        return dialog

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

                # Color code by source with strong contrast
                if entry.source == "system":
                    source_item.setBackground(QColor(0, 60, 120))     # Dark blue background
                    source_item.setForeground(QColor(245, 245, 250))  # Off-white text
                elif entry.source == "user":
                    source_item.setBackground(QColor(0, 100, 0))      # Dark green background
                    source_item.setForeground(QColor(245, 245, 250))  # Off-white text
                else:
                    # Environment (fallback)
                    source_item.setForeground(QColor(160, 160, 160))  # Light gray text

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
        version_label = QLabel("v0.2.0d 2026-01-09 1400 CST")
        version_label.setStyleSheet("color: #888888; font-size: 9pt;")
        self.statusBar.addPermanentWidget(version_label)

    def show_search_bar(self):
        """Show the search bar and focus the input"""
        self.search_bar.show()
        self.search_input.setFocus()
        self.search_input.selectAll()

    def hide_search_bar(self):
        """Hide the search bar and clear highlights"""
        self.search_bar.hide()
        self.clear_search_highlights()
        self.search_matches = []
        self.current_match_index = -1
        self.match_label.setText("No matches")

    def clear_search_highlights(self):
        """Clear search highlighting from the Path column only"""
        path_column = 1
        for row in range(self.table.rowCount()):
            item = self.table.item(row, path_column)
            if item:
                # Clear background and foreground from Path column (use Qt default)
                item.setData(Qt.ItemDataRole.BackgroundRole, None)
                item.setData(Qt.ItemDataRole.ForegroundRole, None)

    def perform_search(self):
        """Perform search as text is typed"""
        search_text = self.search_input.text().strip()

        # Clear previous highlights and current match indicator
        self.clear_search_highlights()
        self.clear_current_match_indicator()
        self.search_matches = []
        self.current_match_index = -1

        if not search_text:
            self.match_label.setText("No matches")
            return

        # Search only in Path column (column 1) - case-insensitive
        search_lower = search_text.lower()
        path_column = 1

        for row in range(self.table.rowCount()):
            item = self.table.item(row, path_column)
            if item and search_lower in item.text().lower():
                # Highlight matching path cell with medium grey background and white text
                item.setBackground(QColor(128, 128, 128))  # Medium grey background
                item.setForeground(QColor(255, 255, 255))  # White text
                self.search_matches.append(row)

        # Update match counter
        if self.search_matches:
            self.match_label.setText(f"{len(self.search_matches)} matches")
            self.current_match_index = 0
            self.highlight_current_match()
        else:
            self.match_label.setText("No matches")

    def clear_current_match_indicator(self):
        """Remove the bright highlight from the current match"""
        if not self.search_matches or self.current_match_index < 0:
            return

        path_column = 1
        row = self.search_matches[self.current_match_index]
        item = self.table.item(row, path_column)
        if item:
            # Return to regular medium grey highlight with white text
            item.setBackground(QColor(128, 128, 128))  # Medium grey background
            item.setForeground(QColor(255, 255, 255))  # White text

    def highlight_current_match(self):
        """Highlight the current match and scroll to it"""
        if not self.search_matches or self.current_match_index < 0:
            return

        path_column = 1
        row = self.search_matches[self.current_match_index]

        # Clear any existing row selection
        self.table.clearSelection()

        # Make the current match stand out with a darker grey background
        item = self.table.item(row, path_column)
        if item:
            item.setBackground(QColor(80, 80, 80))    # Dark grey background for current match
            item.setForeground(QColor(255, 255, 255))  # White text

        # Scroll to the row
        self.table.scrollToItem(item)

        # Update match label with position
        self.match_label.setText(
            f"Match {self.current_match_index + 1} of {len(self.search_matches)}"
        )

    def find_next(self):
        """Navigate to the next search match"""
        if not self.search_matches:
            return

        # Clear current match indicator before moving
        self.clear_current_match_indicator()

        self.current_match_index = (self.current_match_index + 1) % len(self.search_matches)
        self.highlight_current_match()

    def find_previous(self):
        """Navigate to the previous search match"""
        if not self.search_matches:
            return

        # Clear current match indicator before moving
        self.clear_current_match_indicator()

        self.current_match_index = (self.current_match_index - 1) % len(self.search_matches)
        self.highlight_current_match()

    def handle_quit_shortcut(self):
        """Handle Q key press to quit - but not when typing in search"""
        # Don't quit if the search input field has focus (user is typing)
        if self.search_input.hasFocus():
            # Let the Q key go through to the search field
            return
        # Otherwise, close the application
        self.close()

    def closeEvent(self, event):
        """Save window geometry when closing"""
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


def run_gui():
    """Run the GUI version of PathManager"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look across platforms

    window = PathManagerWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(run_gui())
