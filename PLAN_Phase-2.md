# PathManager - Phase 2: Problem Detection

**Phase Duration:** 2-3 weeks
**Status:** Planning
**Started:** 2026-01-08

---

## Overview

Phase 2 transforms PathManager from a simple viewer into a diagnostic tool that can identify and report PATH problems. This phase focuses on **detection only** - no modifications yet (that's Phase 4).

### Four Detection Categories

1. **Duplicates** - Same path appearing multiple times
2. **Missing Directories** - Paths that don't exist on filesystem
3. **Executable Shadowing** - Multiple versions of same program in PATH
4. **Windows-Specific Issues** - Path length limits, invalid characters, etc.

---

## Architecture Design

### Core Layer: `core/path_detector.py`

Create a new `PathDetector` class that works alongside `PathAnalyzer`:

```python
class PathDetector:
    """Analyzes PATH entries for problems and issues"""

    def __init__(self, analyzer: PathAnalyzer):
        self.analyzer = analyzer
        self.problems = []

    # Individual detection methods
    def detect_duplicates(self) -> List[Problem]:
        """Find exact and case-insensitive duplicates"""

    def detect_missing_directories(self) -> List[Problem]:
        """Find paths that don't exist on filesystem"""

    def detect_shadowed_executables(self) -> List[Problem]:
        """Find multiple versions of common executables"""

    def detect_windows_issues(self) -> List[Problem]:
        """Find Windows-specific problems (length, characters, etc.)"""

    # Main entry point
    def detect_all_problems(self) -> DetectionReport:
        """Run all detectors and return comprehensive report"""
```

### Data Structures

**Problem Class:**
```python
@dataclass
class Problem:
    severity: str           # "error", "warning", "info"
    category: str          # "duplicate", "missing", "shadowing", "windows"
    title: str             # Short description
    description: str       # Detailed explanation
    affected_indices: List[int]  # Which PATH entry numbers
    affected_paths: List[str]    # The actual paths
    suggestion: str        # What user should do
    auto_fixable: bool     # Can be automatically fixed?
    fix_action: Optional[Callable]  # Function to fix (Phase 4)
```

**DetectionReport Class:**
```python
@dataclass
class DetectionReport:
    timestamp: datetime
    total_entries: int
    problems: List[Problem]
    error_count: int
    warning_count: int
    info_count: int

    def get_problems_by_category(self) -> Dict[str, List[Problem]]:
        """Group problems by category"""

    def get_problems_by_severity(self) -> Dict[str, List[Problem]]:
        """Group problems by severity"""

    def has_errors(self) -> bool:
        """Quick check if any errors exist"""

    def has_warnings(self) -> bool:
        """Quick check if any warnings exist"""
```

### Design Principles

1. **Separation of Concerns**: `PathAnalyzer` reads PATH, `PathDetector` finds problems
2. **Structured Results**: Problems are objects, not strings
3. **Lazy Evaluation**: Detection only runs when requested
4. **Extensible**: Easy to add new detectors later
5. **Non-Destructive**: Phase 2 only detects, doesn't modify

---

## Detection Algorithms

### 1. Duplicate Detection

**Algorithm:**
```python
def detect_duplicates(self) -> List[Problem]:
    seen = {}
    duplicates = []

    for entry in self.analyzer.get_path_entries():
        # Normalize: lowercase, resolve path, remove trailing slash
        normalized = os.path.normpath(entry.path).lower()

        if normalized in seen:
            # Found duplicate
            original = seen[normalized]
            problem = Problem(
                severity="warning",
                category="duplicate",
                title=f"Duplicate PATH entry",
                description=f"Path appears multiple times",
                affected_indices=[original.index, entry.index],
                affected_paths=[original.path, entry.path],
                suggestion="Remove duplicate entries (keep first occurrence)",
                auto_fixable=True
            )
            duplicates.append(problem)
        else:
            seen[normalized] = entry

    return duplicates
```

**Handles:**
- Exact duplicates: `C:\Foo` and `C:\Foo`
- Case differences: `C:\Foo` and `c:\foo`
- Trailing slashes: `C:\Foo` and `C:\Foo\`
- Path separators: `C:\Foo\Bar` and `C:/Foo/Bar`

### 2. Missing Directory Detection

**Algorithm:**
```python
def detect_missing_directories(self) -> List[Problem]:
    missing = []

    for entry in self.analyzer.get_path_entries():
        if not os.path.exists(entry.path):
            # Check if it's a network path or removable drive
            is_network = entry.path.startswith(r'\\')
            is_removable = self._is_removable_drive(entry.path)

            severity = "warning" if (is_network or is_removable) else "error"

            problem = Problem(
                severity=severity,
                category="missing",
                title=f"Directory not found",
                description=f"Path does not exist on filesystem",
                affected_indices=[entry.index],
                affected_paths=[entry.path],
                suggestion="Remove from PATH or create directory",
                auto_fixable=True if severity == "error" else False
            )
            missing.append(problem)

    return missing
```

**Handles:**
- Regular missing directories (ERROR)
- Network paths `\\server\share` (WARNING - may be offline)
- Removable drives `D:\`, `E:\` (WARNING - may be disconnected)

### 3. Executable Shadowing Detection

**Common Executables to Check:**
- `python.exe`, `python3.exe`
- `git.exe`
- `node.exe`, `npm.cmd`
- `java.exe`, `javac.exe`
- `code.cmd` (VS Code)
- `docker.exe`
- `rustc.exe`, `cargo.exe`

**Algorithm:**
```python
def detect_shadowed_executables(self) -> List[Problem]:
    executables = ['python.exe', 'git.exe', 'node.exe', 'java.exe', 'code.cmd']
    shadowing = []

    for exe in executables:
        # Find all locations of this executable in PATH
        locations = []
        for entry in self.analyzer.get_path_entries():
            exe_path = os.path.join(entry.path, exe)
            if os.path.exists(exe_path):
                locations.append((entry.index, entry.path, exe_path))

        if len(locations) > 1:
            # Multiple versions found - first one will be used
            active = locations[0]
            shadowed = locations[1:]

            problem = Problem(
                severity="warning",
                category="shadowing",
                title=f"Multiple versions of {exe}",
                description=f"Found {len(locations)} copies in PATH. "
                           f"Only first one ({active[2]}) will be used.",
                affected_indices=[loc[0] for loc in locations],
                affected_paths=[loc[1] for loc in locations],
                suggestion=f"Reorder PATH if different version needed, "
                          f"or remove unused versions",
                auto_fixable=False  # User must decide which to keep
            )
            shadowing.append(problem)

    return shadowing
```

### 4. Windows-Specific Issues

**Checks:**

**A. PATH Length Limits:**
```python
def _check_path_length(self) -> Optional[Problem]:
    # Windows 11 limits (relaxed from older versions)
    SYSTEM_LIMIT = 8191  # characters
    USER_LIMIT = 2047    # legacy limit (relaxed in Win 11)

    user_path_str = os.pathsep.join(self.analyzer.get_user_path())
    system_path_str = os.pathsep.join(self.analyzer.get_system_path())

    user_len = len(user_path_str)
    system_len = len(system_path_str)

    # Warn at 80% of limit
    if system_len > SYSTEM_LIMIT * 0.8:
        return Problem(
            severity="warning",
            category="windows",
            title="System PATH approaching length limit",
            description=f"System PATH is {system_len} of {SYSTEM_LIMIT} chars ({system_len/SYSTEM_LIMIT*100:.1f}%)",
            affected_indices=[],
            affected_paths=[],
            suggestion="Remove unused entries to reduce length",
            auto_fixable=False
        )

    return None
```

**B. Invalid Characters:**
```python
def _check_invalid_characters(self) -> List[Problem]:
    # Windows doesn't allow: < > " | ? *
    invalid_chars = '<>"|?*'
    problems = []

    for entry in self.analyzer.get_path_entries():
        has_invalid = any(c in entry.path for c in invalid_chars)
        if has_invalid:
            problems.append(Problem(
                severity="error",
                category="windows",
                title="Invalid characters in path",
                description=f"Path contains invalid characters: {invalid_chars}",
                affected_indices=[entry.index],
                affected_paths=[entry.path],
                suggestion="Remove or fix path with invalid characters",
                auto_fixable=False
            ))

    return problems
```

**C. Other Windows Checks:**
- UNC paths (`\\server\share`) - INFO/WARNING
- Trailing backslashes - WARNING
- Paths with spaces (check if properly handled) - INFO
- Mixed separators (`\` and `/`) - INFO

---

## CLI Implementation

### Command Structure

**New flags for Phase 2:**
```bash
python pathmanager.py --check              # Run all detections, summary
python pathmanager.py --check --verbose    # Detailed report
python pathmanager.py --check --json       # JSON output
python pathmanager.py --check duplicates   # Run specific detector
python pathmanager.py --check missing      # Check only missing dirs
python pathmanager.py --check shadowing    # Check only shadowing
python pathmanager.py --check windows      # Windows-specific only
```

### CLI Output Design

**Summary Mode (default with --check):**
```
============================================================
PathManager - System Information    [ v0.3.0 ]
============================================================
Machine Name: JAUs-Asus           Operating System: Windows 11
Hardware: AMD64                   Date: 2026-01-08 17:30:45
============================================================

Running PATH diagnostics...

####################
Problem Detection Summary
####################

✓ No duplicates found
✗ 3 directories not found
⚠ 2 executable shadowing issues detected
⚠ PATH length approaching limit (7,234 / 8,191 characters)

Status: ⚠ WARNINGS FOUND (3 errors, 2 warnings)

Path Summary:
  User PATH entries: 29      System PATH entries: 40      Combined PATH entries: 82

Run with --verbose for detailed report.
Legend: ✓ = OK, ⚠ = Warning, ✗ = Error
```

**Verbose Mode (--check --verbose):**
```
============================================================
PathManager - DETAILED PROBLEM REPORT    [ v0.3.0 ]
============================================================
Analysis Date: 2026-01-08 17:30:45 CST
Total PATH Entries: 82 (User: 29, System: 40)
============================================================

═══════════════════════════════════════════════════════════
[✗ ERROR] Missing Directories (3 found)
═══════════════════════════════════════════════════════════

  Entry #23 [User]: C:\Program Files\NonExistent
    ├─ Status: Directory does not exist on filesystem
    ├─ Suggestion: Remove from PATH or create directory
    └─ Auto-fixable: Yes

  Entry #45 [System]: D:\Tools\bin
    ├─ Status: Drive D:\ not accessible (removable drive?)
    ├─ Suggestion: Remove if drive no longer used
    └─ Auto-fixable: Yes

  Entry #67 [User]: C:\Dev\Projects\OldProject\bin
    ├─ Status: Directory does not exist
    ├─ Suggestion: Remove from PATH
    └─ Auto-fixable: Yes

═══════════════════════════════════════════════════════════
[⚠ WARNING] Executable Shadowing (2 found)
═══════════════════════════════════════════════════════════

  python.exe found in multiple locations:
    Entry #12 [System]: C:\Python39\python.exe ← THIS WILL RUN
    Entry #34 [User]:   C:\Python311\python.exe (SHADOWED)

    ├─ Impact: Python 3.9 will be used instead of 3.11
    ├─ Suggestion: Reorder PATH to use desired Python version
    └─ Auto-fixable: No (requires user decision)

  node.exe found in multiple locations:
    Entry #8 [System]:  C:\Program Files\nodejs\node.exe ← THIS WILL RUN
    Entry #28 [User]:   C:\Users\jimur\AppData\Local\nvm\node.exe (SHADOWED)

    ├─ Impact: System Node.js (v16.x) will be used
    ├─ Suggestion: Check if intended version is first in PATH
    └─ Auto-fixable: No (requires user decision)

═══════════════════════════════════════════════════════════
[ℹ INFO] PATH Statistics
═══════════════════════════════════════════════════════════

  Total entries: 82
  User PATH: 29 entries (1,234 chars - 60% of legacy limit)
  System PATH: 40 entries (6,000 chars - 73% of limit)
  Combined length: 7,234 chars (88% of limit)

  Status: ⚠ Approaching length limit

═══════════════════════════════════════════════════════════
SUMMARY
═══════════════════════════════════════════════════════════

  Total Problems: 5
    ✗ Errors: 3 (require attention)
    ⚠ Warnings: 2 (should review)
    ℹ Info: 0

  Recommended Actions:
    1. Remove 3 missing directories from PATH
    2. Review Python version shadowing (3.9 vs 3.11)
    3. Verify Node.js version is correct
    4. Consider cleaning up PATH to reduce length

Legend: ✓ = OK, ⚠ = Warning, ✗ = Error, ℹ = Info
```

**JSON Output (--check --json):**
```json
{
  "timestamp": "2026-01-08T17:30:45-06:00",
  "timezone": "CST",
  "version": "0.3.0",
  "total_entries": 82,
  "problems": [
    {
      "severity": "error",
      "category": "missing",
      "title": "Directory not found",
      "description": "Path does not exist on filesystem",
      "affected_indices": [23],
      "affected_paths": ["C:\\Program Files\\NonExistent"],
      "suggestion": "Remove from PATH or create directory",
      "auto_fixable": true
    }
  ],
  "summary": {
    "error_count": 3,
    "warning_count": 2,
    "info_count": 0
  }
}
```

---

## GUI Implementation

### Main Window Layout Changes

```
┌────────────────────────────────────────────────────────────────┐
│ File  Edit  View  Tools  Help                       [_][□][X] │
├────────────────────────────────────────────────────────────────┤
│ ⊕ Add  ⊖ Remove  ↑ Up  ↓ Down  🔍 Check  🧹 Clean  💾 Backup  │
│                                    ^^^^^                        │
│                                    NEW BUTTON                   │
├────────────────────────────────────────────────────────────────┤
│                    PATH Entries Table                          │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ #  │ Path                 │ Source │ Status │ Issues    │ │
│  │    │                      │        │        │   ^NEW    │ │
│  ├────┼──────────────────────┼────────┼────────┼───────────┤ │
│  │ 1  │ C:\Windows\system32  │ System │ ✓ OK   │           │ │
│  │ 12 │ C:\Python39          │ System │ ✓ OK   │ ⚠ Shadow │ │
│  │ 23 │ C:\NonExistent       │ User   │ ✗ Err  │ ✗ Missing │ │
│  │ 34 │ C:\Python311         │ User   │ ✓ OK   │ ⚠ Shadow │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│ ▼ Problems Detected (2 warnings, 3 errors)        [Expand ▼] │ ← NEW PANEL
├────────────────────────────────────────────────────────────────┤
│ Total: 82 | User: 29 | System: 40 | Issues: 5      v0.3.0    │
└────────────────────────────────────────────────────────────────┘
```

### New GUI Components

#### 1. "Check" Button (Toolbar)

**Behavior:**
- Click to run all detections
- Shows progress spinner while analyzing
- Updates table and problems panel when complete
- Keyboard shortcut: `Ctrl+K` or `F5`

**Implementation:**
```python
def on_check_button_clicked(self):
    # Show progress
    self.statusBar.showMessage("Analyzing PATH...")
    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

    # Run detection in background thread
    detector = PathDetector(self.analyzer)
    report = detector.detect_all_problems()

    # Update UI
    self.update_issues_column(report)
    self.update_problems_panel(report)
    self.statusBar.showMessage(f"Found {report.error_count} errors, {report.warning_count} warnings")
    QApplication.restoreOverrideCursor()
```

#### 2. "Issues" Column (Table)

**Design:**
- New column added to existing QTableWidget
- Shows icons for quick visual indication:
  - `✗` = Error (red)
  - `⚠` = Warning (yellow)
  - ` ` = No issues
- Tooltip shows issue summary on hover
- Click opens detail dialog

**Implementation:**
```python
def update_issues_column(self, report: DetectionReport):
    for row in range(self.table.rowCount()):
        entry_index = row  # Assuming row matches entry index

        # Find problems for this entry
        problems_for_entry = [
            p for p in report.problems
            if entry_index in p.affected_indices
        ]

        if problems_for_entry:
            # Create issue indicator
            most_severe = max(problems_for_entry, key=lambda p:
                {'error': 3, 'warning': 2, 'info': 1}[p.severity])

            icon_text = {'error': '✗', 'warning': '⚠', 'info': 'ℹ'}[most_severe.severity]
            color = {'error': QColor(255, 0, 0),
                    'warning': QColor(255, 165, 0),
                    'info': QColor(100, 100, 255)}[most_severe.severity]

            item = QTableWidgetItem(icon_text)
            item.setForeground(color)

            # Tooltip with issue summary
            tooltip = '\n'.join([p.title for p in problems_for_entry])
            item.setToolTip(tooltip)

            self.table.setItem(row, ISSUES_COLUMN, item)
```

#### 3. Problems Panel (Collapsible Bottom Panel)

**Collapsed State:**
```
┌────────────────────────────────────────────────────────────┐
│ ▼ Problems Detected (2 warnings, 3 errors)    [Expand ▼]  │
└────────────────────────────────────────────────────────────┘
```

**Expanded State:**
```
┌────────────────────────────────────────────────────────────┐
│ ▲ Problems Detected                           [Collapse ▲] │
├────────────────────────────────────────────────────────────┤
│ Filter: [All ▼] │ Errors: 3 │ Warnings: 2 │ Info: 0      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ ✗ ERROR: Missing Directory (Entry #23)                    │
│   C:\Program Files\NonExistent                             │
│   └─ Directory does not exist. Remove from PATH?          │
│      [Show in Table] [Details] [Fix]                       │
│                                                            │
│ ✗ ERROR: Missing Directory (Entry #45)                    │
│   D:\Tools\bin                                             │
│   └─ Drive not accessible (removable?)                    │
│      [Show in Table] [Details] [Fix]                       │
│                                                            │
│ ⚠ WARNING: Python shadowing (Entries #12, #34)            │
│   Multiple python.exe found. Using v3.9, v3.11 shadowed   │
│      [Show in Table] [Details]                             │
│                                                            │
│ ⚠ WARNING: Node.js shadowing (Entries #8, #28)            │
│   Multiple node.exe found. Using system version            │
│      [Show in Table] [Details]                             │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Implementation:**
- Use `QSplitter` to make panel resizable/collapsible
- `QListWidget` or custom widget for problem list
- Each problem is a list item with:
  - Icon indicating severity
  - Title and affected entries
  - Brief description
  - Action buttons (Show, Details, Fix)

**Interactions:**
- Click "Show in Table" → Highlights affected rows in main table
- Click "Details" → Opens problem detail dialog
- Click "Fix" → Opens fix preview dialog (Phase 4)
- Filter buttons → Show only errors, warnings, or specific categories
- Severity sorting → Errors first, then warnings, then info

#### 4. Problem Detail Dialog

**Opens when:** User clicks "Details" button or double-clicks problem

**Layout:**
```
┌────────────────────────────────────────────────┐
│ Problem Details                          [X]   │
├────────────────────────────────────────────────┤
│ ⚠ WARNING: Python Executable Shadowing         │
├────────────────────────────────────────────────┤
│                                                │
│ Multiple versions of python.exe found in PATH  │
│                                                │
│ Affected Entries:                              │
│   #12 [System]: C:\Python39\python.exe         │
│                 → This version WILL run        │
│   #34 [User]:   C:\Python311\python.exe        │
│                 → This version is SHADOWED     │
│                                                │
│ Impact:                                        │
│   When you type "python", version 3.9 will     │
│   be used instead of 3.11 due to PATH order.   │
│                                                │
│ Suggestion:                                    │
│   Reorder PATH to place desired Python version │
│   first, or remove the version you don't use.  │
│                                                │
│ Auto-fixable: No (requires your decision)      │
│                                                │
│ [Show in Table]  [Close]                       │
└────────────────────────────────────────────────┘
```

---

## Implementation Timeline

### Week 1: Core Detection Engine

**Days 1-2: Setup & Duplicates**
- [ ] Create `core/path_detector.py`
- [ ] Implement `Problem` and `DetectionReport` classes
- [ ] Implement `PathDetector.detect_duplicates()`
- [ ] Write unit tests for duplicate detection
- [ ] CLI: Add `--check` flag parsing

**Days 3-4: Missing Directories**
- [ ] Implement `PathDetector.detect_missing_directories()`
- [ ] Handle network paths and removable drives
- [ ] Write unit tests
- [ ] CLI: Implement summary output mode

**Day 5: CLI Polish**
- [ ] CLI: Implement verbose mode
- [ ] CLI: Add color coding (red/yellow/green)
- [ ] CLI: Test with various PATH configurations

### Week 2: Advanced Detection & GUI Basics

**Days 1-2: Shadowing Detection**
- [ ] Implement `PathDetector.detect_shadowed_executables()`
- [ ] Test with python, git, node, java
- [ ] Write unit tests
- [ ] CLI: Add specific detector flags

**Day 3: Windows-Specific Checks**
- [ ] Implement `PathDetector.detect_windows_issues()`
- [ ] Check PATH length limits
- [ ] Check for invalid characters
- [ ] Check for UNC paths, trailing backslashes
- [ ] Write unit tests

**Days 4-5: GUI Check Button & Issues Column**
- [ ] GUI: Add "Check" button to toolbar
- [ ] GUI: Add "Issues" column to table
- [ ] GUI: Implement threading for detection
- [ ] GUI: Update status bar with problem counts
- [ ] GUI: Add tooltips on Issues column

### Week 3: Problems Panel & Final Polish

**Days 1-2: Problems Panel**
- [ ] GUI: Create collapsible bottom panel using QSplitter
- [ ] GUI: Implement problem list widget
- [ ] GUI: Add filter buttons (All, Errors, Warnings)
- [ ] GUI: Implement expand/collapse

**Day 3: Problem Interactions**
- [ ] GUI: "Show in Table" highlights rows
- [ ] GUI: Create Problem Detail Dialog
- [ ] GUI: Double-click problem opens details
- [ ] GUI: Keyboard shortcuts (Ctrl+K for check)

**Days 4-5: Testing & Documentation**
- [ ] Test with edge cases (empty PATH, very long PATH, etc.)
- [ ] Test on Windows 11 Home and Pro
- [ ] Performance testing (should complete <1 second)
- [ ] Update CHANGELOG.md
- [ ] Update README.md with new --check flag
- [ ] Update QUICK_REFERENCE.md with detection features
- [ ] Create Phase 2 completion report

---

## Testing Strategy

### Test Cases

**Duplicate Detection:**
- [ ] Exact duplicates
- [ ] Case-insensitive duplicates
- [ ] Trailing slash variations
- [ ] Mixed separators (\ and /)
- [ ] Normalized path equivalents

**Missing Directories:**
- [ ] Regular missing directories
- [ ] Network paths (offline)
- [ ] Removable drives (disconnected)
- [ ] Paths on non-existent drives

**Shadowing:**
- [ ] Multiple Python versions
- [ ] Multiple Git installations
- [ ] Multiple Node.js versions
- [ ] Executables in subdirectories

**Windows Issues:**
- [ ] Very long PATH (>8000 chars)
- [ ] Invalid characters in paths
- [ ] UNC paths
- [ ] Trailing backslashes
- [ ] Mixed case consistency

**Performance:**
- [ ] Detection completes in <1 second for 50 entries
- [ ] Detection completes in <2 seconds for 100 entries
- [ ] No UI freezing during detection
- [ ] Memory usage stays reasonable

### Test PATH Configurations

Create test fixtures with known problems:

```python
# test_fixtures/problematic_path.txt
C:\Windows\system32      # OK
C:\Python39              # OK (but shadowed)
C:\Python39              # Duplicate!
C:\NonExistent           # Missing
C:\Python311             # OK (but shadowed)
D:\Tools\bin             # Missing (removable)
C:\Program Files\Git\cmd # OK
\\server\share           # Network path
C:\Path\With\Trailing\   # Trailing slash
```

---

## Success Criteria

✓ **Core Detection Works**
  - All 4 detection categories implemented
  - Accurate results with zero false positives on known-good PATH
  - Unit tests cover all detection logic

✓ **CLI Functional**
  - `--check` flag runs all detections
  - Summary mode shows clear problem count
  - Verbose mode shows detailed report
  - Color coding makes issues visible
  - JSON output available for scripting

✓ **GUI Enhanced**
  - "Check" button runs detection smoothly
  - Issues column shows visual indicators
  - Problems panel displays all issues clearly
  - Clicking problem highlights affected entries
  - Detail dialog shows comprehensive information

✓ **Performance**
  - Detection completes in <1 second for typical PATH
  - GUI remains responsive during detection
  - No memory leaks

✓ **Quality**
  - Unit tests pass
  - Works on Windows 11 Home and Pro
  - Documentation updated
  - Code reviewed and clean

---

## Next Phase Preview

**Phase 3: Backup System** (after Phase 2 complete)
- Automatic backup before any modification
- Backup browser and restore
- Backup comparison and diff view

**Phase 4: PATH Modification** (after Phase 3)
- Will add "Fix" button functionality
- Implement auto-fix for problems marked as `auto_fixable=True`
- Preview and confirmation dialogs

---

## Notes

- All timestamps use Central Time USA (CST/CDT) per Project_Rules.md
- Phase 2 is **detection only** - no PATH modifications
- Focus on accuracy over speed (but <1 second is target)
- Test extensively before moving to Phase 3
- Keep CLI and GUI feature parity

---

**Status:** Ready to start implementation
**Next Step:** Create `core/path_detector.py` with Problem and DetectionReport classes
