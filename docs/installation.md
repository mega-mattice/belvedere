# Belvedere Installation Guide

This guide will walk you through installing Belvedere on your system.

## System Requirements

Before installing Belvedere, ensure your system meets the following requirements:

- **Operating System**: Windows 7+, macOS 10.14+, or Linux (any modern distribution)
- **Python**: Python 3.8 or later
- **Display**: Graphical desktop environment with system tray support
- **Disk Space**: Approximately 300 MB (including dependencies)

## Installation Methods

### Method 1: Using pip (Recommended)

This is the easiest way to install Belvedere.

1. **Install Python** (if not already installed)
   - **Windows**: Download from [python.org](https://www.python.org/downloads/)
   - **macOS**: `brew install python` or download from [python.org](https://www.python.org/downloads/)
   - **Linux**: Use your package manager (e.g., `sudo apt install python3 python3-pip`)

2. **Install Belvedere**
   ```bash
   # Clone or download the repository
   git clone https://github.com/mega-mattice/belvedere.git
   cd belvedere

   # Install as a package
   pip install -e .
   ```

3. **Run Belvedere**
   ```bash
   belvedere
   ```

### Method 2: Running from Source

If you want to run Belvedere without installing:

1. **Install Python** (see Method 1)

2. **Download Belvedere**
   ```bash
   git clone https://github.com/mega-mattice/belvedere.git
   cd belvedere
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Belvedere**
   ```bash
   python belvedere.py
   # Or use the helper script
   python run_belvedere.py
   ```

## Platform-Specific Instructions

### Windows

1. **Install Python**
   - Download the installer from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation: `python --version`

2. **Install Belvedere** (see Method 1 or 2 above)

3. **Run at Startup** (optional)
   - Press `Windows + R`
   - Type `shell:startup` and press Enter
   - Create a shortcut to Belvedere in this folder
   - Or create a batch file with: `python -m belvedere.main`

### macOS

1. **Install Python**
   ```bash
   # Using Homebrew (recommended)
   brew install python

   # Or download from python.org
   ```

2. **Install Belvedere** (see Method 1 or 2 above)

3. **Run at Login** (optional)
   - System Preferences → Users & Groups → Login Items
   - Click "+" and add Belvedere
   - Or create a Launch Agent plist file

### Linux

1. **Install Python and Dependencies**
   ```bash
   # Debian/Ubuntu
   sudo apt update
   sudo apt install python3 python3-pip

   # Fedora
   sudo dnf install python3 python3-pip

   # Arch
   sudo pacman -S python python-pip
   ```

2. **Install System Libraries** (for PySide6)
   ```bash
   # Debian/Ubuntu
   sudo apt install libgl1-mesa-glx libegl1-mesa libxkbcommon-x11-0

   # Fedora
   sudo dnf install mesa-libGL mesa-libEGL libxkbcommon-x11
   ```

3. **Install Belvedere** (see Method 1 or 2 above)

4. **Run at Startup** (optional)
   - Create a desktop entry in `~/.config/autostart/`
   - Or add to your desktop environment's startup applications

## Verifying Installation

After installation, verify that Belvedere is working:

1. **Start Belvedere**
   ```bash
   belvedere
   # Or if running from source:
   python belvedere.py
   ```

2. **Check System Tray**
   - Look for the Belvedere icon in your system tray
   - Right-click the icon to see the menu

3. **Open the GUI**
   - Click the system tray icon or select "Manage" from the menu
   - The main window should appear

## Troubleshooting Installation Issues

### Python Not Found

- **Problem**: `python: command not found` or similar error
- **Solution**:
  - Ensure Python 3.8+ is installed
  - On some systems, use `python3` instead of `python`
  - Add Python to your PATH environment variable

### Import Errors

- **Problem**: `ModuleNotFoundError` for PySide6, watchdog, or send2trash
- **Solution**:
  - Install dependencies: `pip install -r requirements.txt`
  - Use the correct pip: `pip3` instead of `pip` on some systems
  - Try: `python -m pip install -r requirements.txt`

### Display Connection Error

- **Problem**: "Cannot connect to display" or similar
- **Solution**:
  - Belvedere requires a graphical desktop environment
  - Ensure you're not running in a headless environment
  - On Linux, ensure X11 or Wayland is running

### Permission Errors

- **Problem**: Permission denied when installing
- **Solution**:
  - Use `--user` flag: `pip install --user -e .`
  - Or use a virtual environment (recommended)
  - Don't use `sudo pip` - use virtual environments instead

### System Tray Not Showing (Linux)

- **Problem**: Icon doesn't appear in system tray
- **Solution**:
  - Ensure your desktop environment supports system tray icons
  - Install system tray extensions if needed (GNOME, etc.)
  - Some Wayland compositors have limited tray support - try X11

## Virtual Environment (Recommended)

Using a virtual environment prevents dependency conflicts:

```bash
# Create virtual environment
python -m venv belvedere-env

# Activate it
# Windows:
belvedere-env\Scripts\activate
# macOS/Linux:
source belvedere-env/bin/activate

# Install Belvedere
pip install -e .

# Run Belvedere
belvedere
```

## Uninstallation

To uninstall Belvedere:

### If Installed via pip

```bash
pip uninstall belvedere
```

### If Running from Source

Simply delete the Belvedere directory.

### Remove Configuration Files (Optional)

```bash
# Linux/macOS
rm -rf ~/.config/belvedere/
rm -rf ~/.belvedere/

# Windows
# Delete: %USERPROFILE%\.belvedere\
```

## Next Steps

After installation is complete:

1. **Configure Your First Rule**
   - Follow the [Getting Started Guide](getting-started.md)

2. **Explore Features**
   - Check out the [Usage Guide](usage.md)

3. **Set Up Automatic Startup** (optional)
   - Follow platform-specific instructions above

4. **Get Help**
   - Visit the [Troubleshooting Guide](troubleshooting.md) if you encounter issues

---

**Happy organizing!** 🗂️
