# Belvedere Installation Guide

This guide will walk you through installing Belvedere on your Windows system.

## System Requirements

Before installing Belvedere, ensure your system meets the following requirements:

- **Operating System**: Windows 7, 8, 10, or 11
- **Disk Space**: Approximately 5 MB of free disk space
- **AutoHotkey** (optional): AutoHotkey v1.1 or later is only required if you plan to run the .ahk script directly

## Installation Methods

### Method 1: Using the Installer (Recommended)

This is the easiest way to install Belvedere.

1. **Download the Installer**
   - Download the latest Belvedere installer from the [releases page](https://github.com/mega-mattice/belvedere/releases)
   - Look for the file named `Belvedere-Setup-0.5.exe` (or latest version)

2. **Run the Installer**
   - Double-click the downloaded installer file
   - Windows may show a security warning. Click "More info" and then "Run anyway" if prompted
   
3. **Follow Installation Wizard**
   - Click "Next" to begin the installation process
   - Choose the installation directory (default is recommended: `%LOCALAPPDATA%\Belvedere`)
   - Select Start Menu folder options
   - Choose whether to create desktop shortcuts
   - Click "Install" to begin the installation

4. **Complete Installation**
   - Optionally, check "Run Belvedere" to launch it immediately
   - Click "Finish" to exit the installer

### Method 2: Running from Source

If you want to run Belvedere from the source code:

1. **Install AutoHotkey**
   - Download AutoHotkey v1.1 from [autohotkey.com](https://www.autohotkey.com/)
   - Install AutoHotkey on your system

2. **Download Belvedere Source**
   - Clone or download the Belvedere repository from GitHub
   - Extract the files to a folder of your choice

3. **Run Belvedere Script**
   - Navigate to the Belvedere folder
   - Double-click `Belvedere.ahk` to run the application

## Windows 11 Specific Instructions

Windows 11 users should note the following:

### Installation Location
- Belvedere installs to `%LOCALAPPDATA%\Belvedere` by default (user-level installation)
- This location does not require administrator privileges
- Each user account can have its own Belvedere installation

### High-DPI Display Support
- Belvedere includes native support for high-DPI displays (4K monitors, etc.)
- The application will automatically scale correctly on high-resolution screens
- No additional configuration is needed

### Security and UAC
- The installer uses user-level installation (no admin rights required)
- Belvedere will not trigger UAC (User Account Control) prompts during normal operation
- Registry keys are stored in HKEY_CURRENT_USER (user-level) rather than HKEY_LOCAL_MACHINE

## Upgrading from Previous Versions

If you have an older version of Belvedere installed:

1. **Backup Your Rules**
   - Navigate to your old Belvedere installation folder
   - Copy the `rules.ini` file to a safe location
   - This file contains all your custom rules and settings

2. **Install New Version**
   - Run the new installer as described above
   - The installer will detect and remove the old version

3. **Restore Your Rules** (if needed)
   - If your rules don't automatically transfer:
   - Navigate to the new installation folder (usually `%LOCALAPPDATA%\Belvedere`)
   - Replace the new `rules.ini` with your backed-up version

## Uninstallation

To uninstall Belvedere:

1. **Using Windows Settings**
   - Open Windows Settings (Windows key + I)
   - Go to "Apps" or "Apps & features"
   - Find "Belvedere" in the list
   - Click "Uninstall" and follow the prompts

2. **Using Control Panel**
   - Open Control Panel
   - Go to "Programs and Features" or "Uninstall a program"
   - Select "Belvedere" from the list
   - Click "Uninstall" and follow the prompts

3. **Manual Cleanup** (optional)
   - If you want to remove all settings:
   - Delete the folder: `%LOCALAPPDATA%\Belvedere`
   - Delete registry keys under: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Uninstall\Belvedere`

## Troubleshooting Installation Issues

### Installer Won't Run
- **Problem**: Installer shows security warning or won't run
- **Solution**: Right-click the installer, select "Properties", check "Unblock", then click "OK" and try again

### Installation Fails
- **Problem**: Installer reports an error during installation
- **Solution**: 
  - Ensure you have write permissions to `%LOCALAPPDATA%`
  - Close any running instances of Belvedere
  - Temporarily disable antivirus software and try again

### AutoHotkey Script Won't Run
- **Problem**: Double-clicking Belvedere.ahk does nothing
- **Solution**: 
  - Ensure AutoHotkey v1.1 or later is installed
  - Right-click Belvedere.ahk and select "Run Script"
  - Check that .ahk files are associated with AutoHotkey

## Post-Installation

After installation is complete:

1. **Configure Startup** (optional)
   - To run Belvedere automatically when Windows starts
   - See the [Getting Started Guide](getting-started.md) for instructions

2. **Create Your First Rule**
   - Follow the [Usage Guide](usage.md) to create your first automation rule

3. **Explore Features**
   - Check out the [Getting Started Guide](getting-started.md) for a quick overview

## Next Steps

- [Getting Started Guide](getting-started.md) - Quick start for new users
- [Usage Guide](usage.md) - Detailed guide on using Belvedere
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
