# PathManager Development Plan

## Project Vision

Transform PathManager from a simple PATH viewer into a comprehensive PATH management tool for Windows 11, with both CLI and GUI interfaces working in parallel. Focus on helping users view, identify problems, and safely fix PATH environment issues.

---

## Architecture Strategy

To support both CLI and GUI in parallel, use a **three-layer architecture**:

```
pathmanager/
├── core/
│   ├── __init__.py
│   ├── path_analyzer.py      # PATH reading, parsing, analysis
│   ├── path_detector.py      # Problem detection logic
│   ├── path_modifier.py      # PATH modification operations
│   └── backup_manager.py     # Backup/restore functionality
├── cli/
│   ├── __init__.py
│   └── cli_main.py           # CLI interface (refactored current script)
├── gui/
│   ├── __init__.py
│   ├── gui_main.py           # PyQt6 main window
│   ├── widgets/              # Custom widgets
│   └── dialogs/              # Dialog windows
└── pathmanager.py            # Entry point (CLI by default, --gui flag)
```

**Key Principle**: All business logic lives in `core/`, interfaces in `cli/` and `gui/` only handle presentation. This ensures both interfaces can share the same underlying functionality.

---

## Development Phases

### Phase 1: Foundation & Basic GUI

**Duration**: 2-3 weeks

**Objectives:**
- Refactor existing code into modular architecture
- Create basic PyQt6 GUI with current viewing functionality
- Establish Windows 11 PATH reading (User vs System paths)

**Deliverables:**
1. Restructure codebase into core/cli/gui layers
2. `PathAnalyzer` class: read PATH, detect OS, handle Windows registry access
3. Basic PyQt6 window showing PATH entries in a table
4. CLI maintained with new architecture
5. Handle both User PATH and System PATH on Windows (requires admin for system)

**Technical Details:**
- **Windows 11 Registry Access:**
  - User PATH: `HKEY_CURRENT_USER\Environment`
  - System PATH: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment`
- **Dependencies:** `pip install PyQt6`
- **GUI Components:** Use `QTableWidget` or `QTableView` for PATH display

**Tasks:**
- [ ] Create project structure (core/cli/gui folders)
- [ ] Install and verify PyQt6
- [ ] Create PathAnalyzer class with OS detection
- [ ] Implement Windows registry reading (User and System PATH)
- [ ] Build basic PyQt6 main window with table view
- [ ] Refactor existing pathmanager.py to use new architecture
- [ ] Add --gui command line flag to entry point
- [ ] Update README with new structure

---

### Phase 2: Problem Detection

**Duration**: 2-3 weeks

**Objectives:**
- Implement all four problem detection types
- Display problems in both CLI and GUI
- Provide detailed problem reports

**Features to Implement:**

#### 1. Duplicate Detection
**Location:** `core/path_detector.py`

Detect:
- Exact duplicates
- Case-insensitive duplicates (Windows is case-insensitive)
- Normalized path duplicates (`C:\Foo` vs `C:\Foo\`)
- Trailing slash variations

**Algorithm:**
```python
def find_duplicates(paths):
    # Track normalized versions
    seen = {}
    duplicates = []
    for idx, path in enumerate(paths):
        normalized = os.path.normpath(path).lower()
        if normalized in seen:
            duplicates.append((idx, path, seen[normalized]))
        else:
            seen[normalized] = (idx, path)
    return duplicates
```

#### 2. Non-existent Directories
Detect:
- Paths that don't exist on filesystem using `os.path.exists()`
- Distinguish between User and System PATH entries
- Handle special cases (network drives, removable media)

**Important:** Flag but don't auto-remove - directories might be temporarily unavailable (disconnected drives, network shares)

#### 3. Ordering Issues
Detect:
- Shadowed executables (same .exe in multiple PATH locations)
- Use `shutil.which()` to find which version would actually run
- Compare with expected locations

**Common Windows tools to check:**
- python.exe, python3.exe
- git.exe
- node.exe, npm.cmd
- java.exe
- code.cmd (VS Code)

**Example Output:**
```
⚠️  WARNING: Multiple versions of 'python.exe' found:
   1. C:\Python39\python.exe (will be used)
   2. C:\Python311\python.exe (shadowed)
```

#### 4. Windows-Specific Issues
Detect:
- **PATH length limits:**
  - System PATH: 8191 characters (relaxed in Windows 11)
  - User PATH: 2047 characters (legacy limit, relaxed in Windows 11)
- **Invalid characters:** `<>"|?*` in paths
- **UNC paths:** `\\server\share` format (valid but may cause issues)
- **Paths with spaces:** Check if properly handled
- **Trailing backslashes:** Can cause quoting issues
- **Special characters:** Check for problematic unicode

**Deliverables:**
- [ ] Create `PathDetector` class with detection methods
- [ ] Implement duplicate detection algorithm
- [ ] Implement non-existent directory checking
- [ ] Implement ordering/shadowing detection
- [ ] Implement Windows-specific issue detection
- [ ] CLI: Add colored output (red=error, yellow=warning, green=ok)
- [ ] CLI: Add `--check` or `--diagnose` command
- [ ] GUI: Create problem panel with severity indicators
- [ ] GUI: Add filter/sort capabilities for problems
- [ ] Add export to text/JSON report functionality
- [ ] Write unit tests for each detection type

---

### Phase 3: Backup System

**Duration**: 1 week

**Objectives:**
- Never lose working PATH configuration
- Easy rollback capability
- Backup history management

**Features:**

1. **Automatic Backup Before Modification**
   - Create backup before any PATH change
   - Store metadata (timestamp, OS, user who made change)

2. **Backup Storage Format**
   - Format: JSON with metadata
   - Location: `%APPDATA%\PathManager\backups\` (Windows) or `~/.pathmanager/backups/` (Unix)
   - Filename format: `backup_YYYYMMDD_HHMMSS.json`

3. **Backup File Structure:**
```json
{
  "timestamp": "2026-01-08T15:30:00-06:00",
  "timezone": "CST",
  "os": "Windows 11",
  "machine": "DESKTOP-ABC123",
  "user_path": ["C:\\Users\\...\\AppData\\Local\\Programs\\Python", ...],
  "system_path": ["C:\\Windows\\system32", ...],
  "hash": "sha256_hash_of_paths",
  "notes": "Backup before removing duplicates"
}
```

4. **Backup Management**
   - List all backups with dates
   - Preview backup contents
   - Restore from backup
   - Delete old backups (keep last N backups, configurable)
   - Compare current PATH with backup

**Deliverables:**
- [ ] Create `BackupManager` class in `core/backup_manager.py`
- [ ] Implement backup creation with JSON serialization
- [ ] Implement backup listing and sorting
- [ ] Implement restore functionality
- [ ] Add backup location configuration
- [ ] GUI: Backup browser dialog with preview
- [ ] GUI: Restore confirmation dialog with diff view
- [ ] CLI: `--backup-list` command
- [ ] CLI: `--backup-restore <timestamp>` command
- [ ] CLI: `--backup-create` manual backup command
- [ ] Add automatic backup cleanup (keep last 50 backups by default)
- [ ] Add backup verification (hash checking)

---

### Phase 4: PATH Modification

**Duration**: 2-3 weeks

**Objectives:**
- Safe PATH editing with preview and confirmation
- Support both User and System PATH (with admin elevation)
- All modifications go through backup system

**Safety Model:**
1. Create backup
2. Show preview of changes (before/after)
3. Require explicit confirmation
4. Apply changes
5. Verify changes applied correctly

**Features:**

#### Basic Operations
1. **Add New Entry**
   - Add to end or specific position
   - Choose User or System PATH
   - Validate path exists (warn if not)
   - Check for duplicates before adding

2. **Remove Entry**
   - Remove by index or exact path match
   - Confirm before removal
   - Support batch removal

3. **Reorder Entries**
   - Move entry up/down
   - Move to top/bottom
   - Drag-and-drop in GUI

4. **Enable/Disable Entry**
   - "Comment out" entries without deleting
   - Useful for testing PATH changes
   - Store disabled entries in config file

#### Smart Operations
1. **Remove All Duplicates**
   - Keep first occurrence
   - Show which entries will be removed
   - Preview before applying

2. **Remove Non-existent Paths**
   - Remove paths that don't exist
   - Option to keep network paths
   - Preview before applying

3. **Clean Up**
   - Combined operation:
     - Remove duplicates
     - Remove non-existent paths
     - Trim whitespace
     - Normalize path separators
   - Show comprehensive preview

4. **Import/Export**
   - Export PATH to file (.txt, .json, .reg)
   - Import PATH from file
   - Merge or replace existing PATH

#### Windows Registry Modification
**Critical Implementation Details:**

1. **Writing to Registry:**
```python
import winreg

def update_path(path_list, system=False):
    if system:
        key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        root = winreg.HKEY_LOCAL_MACHINE
    else:
        key_path = r"Environment"
        root = winreg.HKEY_CURRENT_USER

    with winreg.OpenKey(root, key_path, 0, winreg.KEY_SET_VALUE) as key:
        path_string = os.pathsep.join(path_list)
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, path_string)
```

2. **Broadcasting Changes:**
```python
import ctypes
from ctypes import wintypes

def broadcast_settings_change():
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x1A
    SMTO_ABORTIFHUNG = 0x0002

    result = ctypes.c_long()
    SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
    SendMessageTimeoutW(
        HWND_BROADCAST, WM_SETTINGCHANGE, 0,
        "Environment", SMTO_ABORTIFHUNG, 5000, ctypes.byref(result)
    )
```

3. **Admin Elevation for System PATH:**
   - Detect if admin rights needed
   - Use `ctypes.windll.shell32.IsUserAnAdmin()`
   - Prompt for elevation using UAC
   - Option: Restart app with admin rights using `runas`

**Deliverables:**
- [ ] Create `PathModifier` class in `core/path_modifier.py`
- [ ] Implement basic add/remove/reorder operations
- [ ] Implement smart cleanup operations
- [ ] Implement Windows registry writing
- [ ] Implement WM_SETTINGCHANGE broadcast
- [ ] Implement admin elevation detection and handling
- [ ] Create preview/diff functionality
- [ ] CLI: Interactive modification mode
- [ ] CLI: Batch commands (--add, --remove, --clean)
- [ ] GUI: Toolbar with modification buttons
- [ ] GUI: Drag-and-drop reordering
- [ ] GUI: Preview dialog showing before/after with highlighting
- [ ] GUI: Confirmation dialog for destructive operations
- [ ] Add comprehensive error handling
- [ ] Add verification that changes were applied
- [ ] Write extensive tests for registry operations

---

### Phase 5: Polish & Windows 11 Integration

**Duration**: 1-2 weeks

**Objectives:**
- Native Windows 11 look and feel
- Professional distribution
- Advanced features for power users

**Features:**

#### 1. Windows 11 UI Styling
- Modern, clean design matching Windows 11 aesthetic
- Fluent Design elements (acrylic, rounded corners)
- Dark mode support (follow system theme)
- High DPI awareness
- Proper icon set (SVG-based)

#### 2. System Tray Integration
- Minimize to system tray
- Quick actions from tray menu:
  - Open PathManager
  - Quick PATH check
  - View last backup
- Status indicator (green=healthy, yellow=warnings, red=problems)

#### 3. Distribution & Installation
- **Packaging Options:**
  - PyInstaller for standalone .exe
  - WiX or Inno Setup for proper installer
  - Optional: MSIX package for Windows Store

- **Installer Features:**
  - Add to Start Menu
  - Optional: Add to context menu
  - Create uninstaller
  - Check for admin rights if needed

#### 4. Advanced Features
- **Scheduled Health Checks:**
  - Weekly automatic PATH scan
  - Notifications for detected problems
  - Windows Task Scheduler integration

- **Context Menu Integration:**
  - Right-click folder → "Add to PATH"
  - Right-click in PathManager → "Open in Explorer"

- **Windows Terminal Integration:**
  - Profile for PathManager CLI
  - Custom color scheme

- **Auto-update System:**
  - Check GitHub releases for updates
  - Download and apply updates
  - Changelog display

- **Configuration:**
  - Settings dialog
  - Backup retention policy
  - Auto-check frequency
  - Theme preferences
  - Default to User or System PATH

#### 5. Documentation
- User guide (HTML/PDF)
- Keyboard shortcuts reference
- Troubleshooting guide
- Video tutorials (optional)

**Deliverables:**
- [ ] Apply Windows 11 styling to PyQt6 GUI
- [ ] Implement system tray functionality
- [ ] Create installer using PyInstaller + Inno Setup
- [ ] Add system tray with quick actions
- [ ] Implement settings dialog
- [ ] Add context menu integration
- [ ] Create Windows Terminal profile
- [ ] Implement auto-update checker
- [ ] Write comprehensive user documentation
- [ ] Create keyboard shortcuts
- [ ] Add tooltips and help text throughout GUI
- [ ] Performance optimization
- [ ] Final testing on clean Windows 11 install
- [ ] Prepare for optional Windows Store submission

---

## Key Technical Considerations

### Windows 11 Specifics
- **Registry Access:** Use `winreg` module for User and System PATH
- **Admin Rights:** System PATH requires elevation (UAC prompt)
- **Change Broadcasting:** Must send `WM_SETTINGCHANGE` message after registry changes
- **PATH Length:** Windows 11 has relaxed PATH length limits compared to older versions
- **Case Sensitivity:** Windows paths are case-insensitive
- **Path Separators:** Backslash `\` is standard, but forward slash `/` often works

### GUI Design Philosophy
- **Main Window Layout:**
  - Toolbar: Add, Remove, Move Up, Move Down, Clean, Backup, Restore
  - Table view with columns: [#, Path, Status, Type (User/System), Issues]
  - Problem panel (collapsible) showing detected issues
  - Status bar: Summary (e.g., "45 entries, 3 duplicates, 2 missing")

- **Color Coding:**
  - Green = OK
  - Yellow = Warning (non-critical issues)
  - Red = Error (critical issues)
  - Gray = Non-existent directory
  - Blue = System PATH entry

- **User Experience:**
  - Clear visual feedback for all operations
  - Progress indicators for long operations
  - Tooltips explaining all buttons and options
  - Undo/redo support where feasible

### Safety Principles
1. **Always backup before modification**
2. **Never auto-apply fixes without preview**
3. **Log all changes for audit trail**
4. **Test modifications on User PATH before System PATH**
5. **Provide easy rollback via restore**
6. **Validate all user input**
7. **Handle edge cases gracefully**

### Performance Considerations
- PATH reading should be fast (<100ms)
- Problem detection should complete in <1 second for typical PATH
- GUI should remain responsive during operations
- Use threading for long operations (registry writes, backups)
- Cache PATH analysis results when appropriate

---

## Immediate Next Steps (Phase 1 Start)

1. **Set up project structure**
   - Create core/cli/gui folder hierarchy
   - Create `__init__.py` files
   - Set up requirements.txt with PyQt6

2. **Install PyQt6 and verify**
   - `pip install PyQt6`
   - Create minimal test window to verify installation

3. **Create PathAnalyzer class**
   - Move existing PATH reading logic
   - Add Windows registry reading
   - Separate User and System PATH
   - Add OS detection

4. **Build basic PyQt6 GUI**
   - Main window with table view
   - Display PATH entries
   - Show User vs System distinction
   - Add basic menu bar

5. **Refactor pathmanager.py**
   - Use new PathAnalyzer class
   - Add --gui flag
   - Keep CLI as default

6. **Update documentation**
   - Update README.md with new usage
   - Update CLAUDE.md with new architecture
   - Document dependencies

---

## Success Metrics

**Phase 1:**
- CLI and GUI both display PATH correctly
- Can distinguish User and System PATH on Windows 11
- GUI is responsive and looks reasonable

**Phase 2:**
- Accurately detects all four problem types
- Zero false positives on known-good PATH
- Problem reports are clear and actionable

**Phase 3:**
- Backups created automatically
- Can restore from backup successfully
- No data loss in backup/restore cycle

**Phase 4:**
- Can safely modify PATH without corruption
- Changes persist across reboots
- Admin elevation works correctly for System PATH

**Phase 5:**
- Installer works on clean Windows 11
- GUI matches Windows 11 design language
- No crashes or hangs in normal usage

---

## Risk Mitigation

**Risk:** Corrupting PATH and breaking system
- **Mitigation:** Always backup, preview changes, extensive testing

**Risk:** Admin elevation issues
- **Mitigation:** Clear error messages, fallback to User PATH only

**Risk:** PyQt6 compatibility issues
- **Mitigation:** Test on multiple Windows 11 versions, have Qt fallbacks

**Risk:** Registry access denied
- **Mitigation:** Graceful error handling, clear instructions for user

**Risk:** Scope creep
- **Mitigation:** Stick to phase plan, defer nice-to-have features

---

## Future Enhancements (Beyond Phase 5)

- **PowerShell Module:** PathManager cmdlets for PowerShell users
- **PATH Templates:** Save/load PATH configurations for different development scenarios
- **Project-based PATH:** Temporary PATH modifications for specific projects
- **PATH Diff Tool:** Compare PATH between machines or users
- **Remote PATH Management:** Manage PATH on remote Windows machines
- **Integration with Package Managers:** Detect paths from Chocolatey, Scoop, winget
- **PATH Performance Analysis:** Measure impact of PATH on startup time
- **Smart Suggestions:** Recommend PATH optimizations based on installed software

---

## Timeline Summary

| Phase | Duration | Key Milestone |
|-------|----------|---------------|
| Phase 1 | 2-3 weeks | Basic GUI working alongside CLI |
| Phase 2 | 2-3 weeks | Problem detection complete |
| Phase 3 | 1 week | Backup/restore system working |
| Phase 4 | 2-3 weeks | Safe PATH modification working |
| Phase 5 | 1-2 weeks | Polished, distributable product |
| **Total** | **8-12 weeks** | **Production-ready PathManager** |

---

## Notes

- All timestamps and dates in this project must use **Central Time USA (CST/CDT)** per Project_Rules.md
- Follow semantic versioning for releases
- Keep CHANGELOG.md updated with each phase completion
- Regular commits with descriptive messages
- Test on Windows 11 Pro and Home editions
- Consider Windows 10 compatibility where feasible
