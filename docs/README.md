# Belvedere Documentation

Welcome to the Belvedere documentation! This folder contains comprehensive guides for installing, using, and troubleshooting Belvedere.

## Quick Links

- **New to Belvedere?** Start with the [Getting Started Guide](getting-started.md)
- **Installing Belvedere?** See the [Installation Guide](installation.md)
- **Need detailed information?** Check the [Usage Guide](usage.md)
- **Having problems?** Visit the [Troubleshooting Guide](troubleshooting.md)

## Documentation Overview

### [Getting Started Guide](getting-started.md)

A quick introduction to Belvedere for new users. Learn:
- What Belvedere is and how it works
- How to create your first rule
- Basic configuration and setup
- Common use cases and examples
- Tips for effective use

**Best for**: First-time users who want to start using Belvedere quickly.

### [Installation Guide](installation.md)

Detailed instructions for installing Belvedere on all platforms. Covers:
- System requirements
- Installation using the installer (recommended)
- Running from source with AutoHotkey
- Windows 11 specific instructions
- Upgrading from previous versions
- Uninstallation

**Best for**: Users installing or upgrading Belvedere.

### [Usage Guide](usage.md)

Comprehensive reference for all Belvedere features. Includes:
- Managing folders and rules
- Complete reference for rule subjects, verbs, and actions
- Advanced rule options
- Recycle Bin management
- Preferences and settings
- Best practices and advanced tips

**Best for**: Users who want to master Belvedere's features or need detailed reference information.

### [Troubleshooting Guide](troubleshooting.md)

Solutions to common problems and issues. Addresses:
- Installation issues
- Startup problems
- Rules not working correctly
- Performance issues
- Windows 11 specific problems
- General troubleshooting steps

**Best for**: Users experiencing problems or unexpected behavior.

## What is Belvedere?

Belvedere is an automated file management tool that helps keep your folders organized. It monitors specified folders and automatically performs actions on files based on rules you define.

### Key Features

- **Automatic File Organization**: Set up rules to automatically move, copy, delete, or rename files
- **Flexible Rule System**: Create rules based on file name, extension, size, or age
- **Multiple Conditions**: Combine conditions for precise control
- **Recycle Bin Management**: Automatically clean up your Recycle Bin
- **Low Resource Usage**: Runs quietly in the background
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Common Use Cases

- **Download Organization**: Automatically sort downloads by file type
- **Temporary File Cleanup**: Remove old temporary files automatically
- **Photo Management**: Organize photos by date or event
- **Disk Space Management**: Archive or remove large old files
- **Document Sorting**: Keep documents organized by type or project

## Learning Path

We recommend the following path for learning Belvedere:

1. **Start Here**: Read the [Getting Started Guide](getting-started.md)
   - Understand what Belvedere does
   - Create a simple rule
   - Get comfortable with the interface

2. **Set Up**: Follow the [Installation Guide](installation.md) if not yet installed
   - Install Belvedere properly
   - Configure to run at startup
   - Understand Windows 11 considerations

3. **Master It**: Explore the [Usage Guide](usage.md)
   - Learn all rule types
   - Discover advanced features
   - Implement best practices

4. **Troubleshoot**: Keep the [Troubleshooting Guide](troubleshooting.md) handy
   - Quick reference for problems
   - Solutions to common issues

## Need Help?

### Documentation

All documentation is available in this folder:
- Browse the guides linked above
- Use Ctrl+F to search within documents
- Check the Table of Contents in each guide

### Community Support

- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions and share tips

### Contributing

Found an error in the documentation or want to improve it?
- Documentation source is in the `docs/` folder
- Submit pull requests with improvements
- Report documentation issues on GitHub

## Version Information

These documentation files are for:
- **Belvedere Version**: 0.5 and later
- **Windows**: 7, 8, 10, and 11
- **Last Updated**: November 2024

For older versions, some features or instructions may differ.

## Additional Resources

### External Links

- **Main Website**: [Lifehacker Article](http://lifehacker.com/341950/belvedere-automates-your-self+cleaning-pc)
- **Python**: [python.org](https://www.python.org/) (for installation)

### Related Documentation

- **Running Belvedere**: See [PYTHON_VERSION.md](../PYTHON_VERSION.md) in the repository root for platform-specific information
- **Implementation Details**: See [IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md) for technical details

## Quick Reference

### Essential Concepts

- **Folder**: A location that Belvedere monitors
- **Rule**: A set of conditions and an action to perform on matching files
- **Subject**: What property of a file to check (name, extension, size, date)
- **Verb**: How to compare the subject (is, contains, greater than, etc.)
- **Object**: The value to compare against
- **Action**: What to do with matching files (move, copy, delete, etc.)

### Common Subjects

- **Name**: Filename without extension
- **Extension**: File type (pdf, jpg, txt)
- **Size**: File size in bytes
- **Date created**: When file was created
- **Date last modified**: When file was last changed
- **Date last opened**: When file was last accessed

### Common Actions

- **Move**: Move files to destination
- **Copy**: Copy files to destination
- **Delete**: Permanently delete files
- **Recycle**: Move files to Recycle Bin
- **Rename**: Rename files
- **Open**: Open files with default application

### Important Locations

- **Configuration Folder**: 
  - Linux/macOS: `~/.config/belvedere/`
  - Windows: `%USERPROFILE%\.belvedere\`
- **Rules File**: `rules.json` in configuration folder

### Keyboard Shortcuts

- **Windows + R**: Open Run dialog
- **Ctrl+Shift+Esc**: Open Task Manager
- **Alt+Tab**: Switch between windows

---

**Happy organizing!** 🗂️
