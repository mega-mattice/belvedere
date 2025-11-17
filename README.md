Belvedere
=========

[![Lint](https://github.com/mega-mattice/belvedere/actions/workflows/lint.yml/badge.svg)](https://github.com/mega-mattice/belvedere/actions/workflows/lint.yml)
[![Test](https://github.com/mega-mattice/belvedere/actions/workflows/test.yml/badge.svg)](https://github.com/mega-mattice/belvedere/actions/workflows/test.yml)

Belvedere sets up rules for taking actions on files (move, copy, delete, etc) based on the name of a file, its extension, size, age, and more.

**Note:** Belvedere is built with Python for cross-platform compatibility and works on Windows, macOS, and Linux.

## Quick Start

- **New User?** See the [Getting Started Guide](docs/getting-started.md)
- **Installing?** Check the [Installation Guide](#installation) below
- **Need Help?** Visit the [Troubleshooting Guide](docs/troubleshooting.md)
- **Full Documentation**: Browse the [docs folder](docs/)

## System Requirements

- Python 3.8 or later
- Works on Windows, macOS, and Linux
- PySide6, watchdog, and send2trash (installed automatically)

## Installation

### For End Users (Windows)

Download the latest Windows executable from the [Releases](https://github.com/mega-mattice/belvedere/releases) page. No Python installation required!

### For Developers

1. **Install Python** (if not already installed)
   - Python 3.9 or later required
   - Download from [python.org](https://www.python.org/downloads/)
   - Or use your system's package manager

2. **Install Poetry** (recommended)
   ```bash
   pip install poetry
   ```

3. **Install Belvedere**
   ```bash
   # Clone or download the repository
   git clone https://github.com/mega-mattice/belvedere.git
   cd belvedere

   # Install dependencies with Poetry (recommended)
   poetry install

   # Or install with pip
   pip install -r requirements.txt

   # Or install as a package
   pip install -e .
   ```

4. **Run Belvedere**
   ```bash
   # Using Poetry
   poetry run belvedere

   # Using the launcher script
   python belvedere.py

   # Or if installed as a package
   belvedere
   ```

## Building from Source

For developers who want to build executables, see [Building Guide](docs/building.md) for detailed build instructions.

## Documentation

Comprehensive documentation is available in the [docs](docs/) folder:

- **[Getting Started Guide](docs/getting-started.md)** - Quick introduction for new users
- **[Installation Guide](docs/installation.md)** - Installation instructions for all platforms
- **[Usage Guide](docs/usage.md)** - Complete feature reference and best practices
- **[Troubleshooting Guide](docs/troubleshooting.md)** - Solutions to common issues
- **[Running Belvedere](docs/running.md)** - Running and using Belvedere
- **[Building Guide](docs/building.md)** - Build instructions for developers
- **[Implementation Summary](docs/implementation.md)** - Technical details about the implementation
- **[Changelog](docs/changelog.md)** - Development notes and release history

## Features

- **File Monitoring**: Automatically watches specified folders for file changes
- **Rule-Based Actions**: Define conditions and actions for file management
- **Multiple Conditions**: Combine conditions with ALL or ANY matching
- **File Attributes**: Match on name, extension, size, creation date, modification date, access date
- **Actions**: Move, Copy, Rename, Delete, Send to Recycle Bin, Open
- **Recycle Bin Management**: Automatically manage recycle bin contents
- **System Tray**: Runs quietly in the background
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Additional Information

### Technology Stack

Belvedere is built with modern Python technologies:
- **Cross-platform support**: Works on Windows, macOS, and Linux
- **Modern dependencies**: Uses PySide6 for GUI, watchdog for file monitoring, pathlib for file operations
- **JSON configuration**: Stores rules in JSON format (in `~/.config/belvedere/` or `~/.belvedere/`)
- **Event-based monitoring**: Efficient file system monitoring with real-time response

For the original introduction, see [Lifehacker](http://lifehacker.com/341950/belvedere-automates-your-self+cleaning-pc)
