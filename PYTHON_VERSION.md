# Running Belvedere (Python Version)

## Prerequisites

- Python 3.8 or later
- A graphical desktop environment (X11, Wayland, Windows Desktop, or macOS)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

Or install as a package:
```bash
pip install -e .
```

## Running the Application

### From the repository directory:
```bash
python belvedere.py
```

### If installed as a package:
```bash
belvedere
```

The application will start and show a system tray icon. Right-click the icon to:
- **Manage**: Open the rules management window
- **About**: View information about Belvedere
- **Exit**: Quit the application

## Configuration

Belvedere stores its configuration in:
- **Linux**: `~/.config/belvedere/rules.json`
- **macOS**: `~/.config/belvedere/rules.json` or `~/.belvedere/rules.json`
- **Windows**: `~/.belvedere/rules.json`

The configuration file is in JSON format and can be edited manually if needed.

## Running Tests

To run the core functionality tests:
```bash
python test_belvedere.py
```

## Platform-Specific Notes

### Linux
- Requires a desktop environment with system tray support
- Install dependencies: `sudo apt-get install python3-pyside6.qtwidgets` (Debian/Ubuntu)
- Or use pip: `pip install PySide6`

### macOS
- Should work out of the box with pip installation
- System tray icon appears in the menu bar

### Windows
- Works exactly like the original AutoHotkey version
- System tray icon appears in the notification area
- Can be set to run at startup by adding to the Startup folder

## Features

All features from the AutoHotkey version are preserved:

- **File Monitoring**: Automatically watches folders for changes
- **Rule-Based Actions**: Define conditions and actions for files
- **Subjects**: Name, Extension, Size, Date modified, Date created, Date last opened
- **Verbs**: is, is not, contains, does not contain, is greater than, is less than, etc.
- **Actions**: Move, Copy, Rename, Delete, Send to Recycle Bin, Open
- **Multiple Conditions**: Combine conditions with ALL or ANY matching
- **Recycle Bin Management**: Automatically manage recycle bin contents
- **Periodic Scanning**: Configurable scan interval

## Troubleshooting

### "No display" or "Cannot connect to display" error
This means you're running in a headless environment. Belvedere requires a graphical desktop.

### "ImportError: libEGL.so.1" or similar library errors (Linux)
Install the required system libraries:
```bash
sudo apt-get install libgl1-mesa-glx libegl1-mesa libxkbcommon-x11-0
```

### System tray icon not showing
- **Linux**: Ensure your desktop environment supports system tray icons (most modern DEs do)
- **Wayland**: Some Wayland compositors may have limited system tray support. Try running under X11.

### Performance
If the application uses too much CPU, increase the sleep time in Preferences (default is 5000 milliseconds = 5 seconds).

## Migrating from AutoHotkey Version

The Python version uses JSON configuration instead of INI files. To migrate:

1. Export your rules from the AutoHotkey version (or note them down)
2. Install and run the Python version
3. Recreate your rules using the GUI

The rule creation interface is nearly identical to the AutoHotkey version.
