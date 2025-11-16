Belvedere
=========

Belvedere sets up rules for taking actions on files (move, copy, delete, etc) based on the name of a file, its extension, size, age, and more.

**Note:** Belvedere is now available in Python for cross-platform compatibility! The Python version works on Windows, macOS, and Linux.

## Quick Start

- **New User?** See the [Getting Started Guide](docs/getting-started.md)
- **Installing?** Check the [Installation Guide](#installation) below
- **Need Help?** Visit the [Troubleshooting Guide](docs/troubleshooting.md)
- **Full Documentation**: Browse the [docs folder](docs/)

## System Requirements

### Python Version (Recommended - Cross-Platform)
- Python 3.8 or later
- Works on Windows, macOS, and Linux
- PySide6, watchdog, and send2trash (installed automatically)

### AutoHotkey Version (Windows Only - Legacy)
- Windows 7, 8, 10, or 11
- AutoHotkey v1.1 or later

## Installation

### Python Version (Recommended)

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)
   - Or use your system's package manager

2. **Install Belvedere**
   ```bash
   # Clone or download the repository
   git clone https://github.com/mega-mattice/belvedere.git
   cd belvedere
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Or install as a package
   pip install -e .
   ```

3. **Run Belvedere**
   ```bash
   # Using the launcher script
   python belvedere.py
   
   # Or if installed as a package
   belvedere
   ```

### AutoHotkey Version (Windows Only)

Download the latest installer from the [releases page](https://github.com/mega-mattice/belvedere/releases) and run it. The installer will guide you through the setup process.

For detailed installation instructions, including Windows 11 specific information, see the [Installation Guide](docs/installation.md).

## Documentation

Comprehensive documentation is available in the [docs](docs/) folder:

- **[Getting Started Guide](docs/getting-started.md)** - Quick introduction for new users
- **[Installation Guide](docs/installation.md)** - Detailed installation instructions (AutoHotkey version)
- **[Usage Guide](docs/usage.md)** - Complete feature reference and best practices
- **[Troubleshooting Guide](docs/troubleshooting.md)** - Solutions to common issues

### Python Version Documentation

- **[Python Version Guide](PYTHON_VERSION.md)** - Running and using the Python version
- **[Version Comparison](VERSION_COMPARISON.md)** - Detailed comparison of AutoHotkey vs Python versions

## Features

- **File Monitoring**: Automatically watches specified folders for file changes
- **Rule-Based Actions**: Define conditions and actions for file management
- **Multiple Conditions**: Combine conditions with ALL or ANY matching
- **File Attributes**: Match on name, extension, size, creation date, modification date, access date
- **Actions**: Move, Copy, Rename, Delete, Send to Recycle Bin, Open
- **Recycle Bin Management**: Automatically manage recycle bin contents
- **System Tray**: Runs quietly in the background
- **Cross-Platform** (Python version): Works on Windows, macOS, and Linux

## Additional Information

### Python vs AutoHotkey Version

The Python version provides:
- **Cross-platform support**: Works on Windows, macOS, and Linux
- **Modern dependencies**: Uses PySide6 for GUI, watchdog for file monitoring, pathlib for file operations
- **JSON configuration**: Stores rules in JSON format instead of INI files (in `~/.config/belvedere/` or `~/.belvedere/`)
- **Same functionality**: All features from the AutoHotkey version are preserved

The AutoHotkey version remains available for users who prefer it, but the Python version is recommended for new users and anyone wanting cross-platform support.

For the original introduction, see [Lifehacker](http://lifehacker.com/341950/belvedere-automates-your-self+cleaning-pc)

For Windows 11 compatibility details (AutoHotkey version), see [WINDOWS11_COMPATIBILITY.md](WINDOWS11_COMPATIBILITY.md)
