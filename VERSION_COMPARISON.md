# Belvedere Version Comparison

## Feature Comparison

| Feature | AutoHotkey Version | Python Version |
|---------|-------------------|----------------|
| **Platform Support** | Windows only | Windows, macOS, Linux |
| **GUI Framework** | Native Windows API | PySide6 (Qt) |
| **File Monitoring** | Polling-based loop | watchdog (event-based) |
| **File Operations** | AHK built-in commands | pathlib (Python standard library) |
| **Configuration Storage** | INI file (rules.ini) | JSON file (rules.json) |
| **Config Location** | Application directory | User config directory (~/.config/belvedere/) |
| **System Tray** | ✅ Yes | ✅ Yes |
| **Rule Management** | ✅ Yes | ✅ Yes |
| **Multiple Conditions** | ✅ Yes (ALL/ANY) | ✅ Yes (ALL/ANY) |
| **File Actions** | Move, Copy, Delete, Recycle, Rename, Open | Move, Copy, Delete, Recycle, Rename, Open |
| **Recursive Monitoring** | ✅ Yes | ✅ Yes |
| **Recycle Bin Management** | ✅ Yes | ✅ Yes |
| **Confirmation Dialogs** | ✅ Yes | ✅ Yes |
| **Test Rule Feature** | ✅ Yes | ✅ Yes |
| **Dependencies** | AutoHotkey runtime | Python 3.8+, PySide6, watchdog, send2trash |
| **Installation** | Windows installer (.exe) | pip install |
| **Auto-start** | Startup folder shortcut | Startup folder/autostart (platform-dependent) |

## Technical Differences

### File Monitoring Approach

**AutoHotkey Version:**
- Uses a polling loop with configurable sleep time
- Scans folders at regular intervals
- Default: 5000ms (5 seconds)
- Resource usage: Consistent CPU usage based on sleep time

**Python Version:**
- Uses watchdog library for event-based monitoring
- Responds to file system events in real-time
- Also includes periodic scanning for compatibility
- Resource usage: More efficient, only activates on events

### Configuration Format

**AutoHotkey INI Example:**
```ini
[Folders]
Folders=C:\Downloads\|C:\Desktop\|

[Rules]
AllRuleNames=Rule1|Rule2|

[Rule1]
Folder=C:\Downloads\*
Enabled=1
Subject=Extension
Verb=is
Object=pdf
Action=Move file
Destination=C:\Documents\PDFs\
```

**Python JSON Example:**
```json
{
  "folders": [
    "C:\\Downloads",
    "C:\\Desktop"
  ],
  "rules": {
    "Rule1": {
      "folder": "C:\\Downloads",
      "enabled": true,
      "conditions": [
        {
          "subject": "Extension",
          "verb": "is",
          "object": "pdf"
        }
      ],
      "action": "Move file",
      "destination": "C:\\Documents\\PDFs"
    }
  }
}
```

## Migration Path

### From AutoHotkey to Python

1. **Export your rules**: Note down or screenshot your existing rules
2. **Install Python version**: Follow installation instructions in README.md
3. **Recreate rules**: Use the GUI to recreate your rules (interface is nearly identical)
4. **Test**: Use the "Test" button to verify rules work as expected
5. **Monitor**: Watch the application for a few days to ensure it behaves correctly

### Benefits of Migrating

- **Cross-platform**: Use the same configuration on multiple operating systems
- **Better performance**: Event-based monitoring is more efficient
- **Modern codebase**: Easier to maintain and extend
- **Active Python ecosystem**: More libraries and tools available

### Keeping Both Versions

You can run both versions simultaneously if needed:
- They use different configuration files
- No conflicts or interference
- Useful for gradual migration or testing

## Which Version Should I Use?

**Choose AutoHotkey Version if:**
- You're on Windows only
- You want the traditional installer experience
- You're already using AutoHotkey for other tasks
- You prefer INI file configuration

**Choose Python Version if:**
- You need cross-platform support
- You want to run on Linux or macOS
- You prefer modern Python tooling
- You want more efficient file monitoring
- You're comfortable with command-line installation

## Performance Notes

Both versions perform similarly for most use cases. The Python version may use slightly more memory due to the Qt framework, but offers better file monitoring efficiency through the watchdog library.

For typical usage (monitoring 1-5 folders with 5-10 rules), both versions use negligible system resources.
