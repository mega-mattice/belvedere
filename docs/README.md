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
- Installation using pip (recommended)
- Running from source with Python
- Platform-specific instructions
- Upgrading
- Uninstallation

**Best for**: Users installing or upgrading Belvedere.

### [Running Guide](running.md)

Platform-specific instructions for running Belvedere after installation. Covers:
- Prerequisites and system requirements
- Running the application on different platforms
- Configuration file locations
- Platform-specific notes for Linux, macOS, and Windows
- Troubleshooting common runtime issues

**Best for**: Users who need help running Belvedere on their specific platform.

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

### [Building Guide](building.md)

Instructions for developers who want to build Belvedere from source. Covers:
- Automated releases with GitHub Actions
- Manual building with PyInstaller
- Platform-specific build considerations
- Build configuration and customization
- Distribution checklist and troubleshooting

**Best for**: Developers contributing to or distributing Belvedere.

### [Implementation Summary](implementation.md)

Technical overview of Belvedere's architecture and implementation. Covers:
- Project structure and core components
- Dependencies and technology stack
- Testing and performance characteristics
- Cross-platform compatibility details
- Future enhancement possibilities

**Best for**: Developers interested in understanding the codebase.

### [Changelog](changelog.md)

Development notes and release history. Contains:
- Feature additions and bug fixes by version
- Development roadmap items
- Historical implementation notes
- Release planning information

**Best for**: Users and developers tracking project progress.

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

2. **Install**: Follow the [Installation Guide](installation.md) to set up Belvedere
   - Install Belvedere properly
   - Configure to run at startup
   - Understand platform-specific considerations

3. **Run**: Use the [Running Guide](running.md) to get started
   - Launch the application
   - Understand the interface
   - Configure initial settings

4. **Master It**: Explore the [Usage Guide](usage.md)
   - Learn all rule types
   - Discover advanced features
   - Implement best practices

5. **Troubleshoot**: Keep the [Troubleshooting Guide](troubleshooting.md) handy
   - Quick reference for problems
   - Solutions to common issues

6. **Develop**: For contributors, see the [Building Guide](building.md)
   - Build from source
   - Understand the architecture
   - Contribute to development

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

- **Main Project README**: See [README.md](../README.md) in the repository root for project overview
- **Running Belvedere**: See [Running Guide](running.md) for platform-specific information
- **Implementation Details**: See [Implementation Summary](implementation.md) for technical details
- **Building Instructions**: See [Building Guide](building.md) for development setup

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
