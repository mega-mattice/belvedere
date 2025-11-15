# Windows 11 Compatibility Update

## Overview
This document describes the changes made to make Belvedere compatible with Windows 11.

## Changes Made

### 1. AutoHotkey Script (Belvedere.ahk)
- **DPI Awareness**: Added `DllCall("SetThreadDpiAwarenessContext", "ptr", -4, "ptr")` to enable per-monitor DPI awareness for high-DPI displays on Windows 10/11
- **Platform Documentation**: Updated platform comment to explicitly list Windows 7, 8, 10, and 11
- **Version Bump**: Incremented version from 0.4 to 0.5

### 2. NSIS Installer (installer/installer.nsi)
- **Installation Location**: Changed from `$PROGRAMFILES` to `$LOCALAPPDATA` for user-level installation
- **Registry Keys**: Changed from HKLM (system-wide) to HKCU (user-level) for better Windows 11 compatibility
- **Execution Level**: Added `RequestExecutionLevel user` to specify user-level privileges
- **Version Updates**: Updated all version references to 0.5

### 3. Application Manifest (Belvedere.manifest) - NEW FILE
Created a comprehensive Windows application manifest with:
- **OS Compatibility**: Explicit support declarations for Windows 7, 8, 8.1, 10, and 11
- **DPI Awareness**: PerMonitorV2 DPI awareness for optimal high-DPI display support
- **Execution Level**: asInvoker level for user-level execution
- **Version Information**: Set to 0.5.0.0

### 4. Documentation (README.md)
- Added **System Requirements** section listing Windows 7-11 support
- Added **Installation** section with notes for Windows 11 users
- Listed AutoHotkey v1.1+ requirement

## Technical Details

### Why User-Level Installation?
Windows 11 has stricter security requirements. Installing to `$LOCALAPPDATA` instead of `$PROGRAMFILES` provides several benefits:
- No administrator privileges required for installation
- Better compatibility with Windows 11 security model
- Reduced UAC prompts
- Each user can have their own Belvedere installation

### DPI Awareness
Modern Windows 11 systems often use high-DPI displays (4K, etc.). The DPI awareness settings ensure:
- Crisp text rendering on high-DPI displays
- Proper window scaling
- Correct mouse coordinates and hit testing
- Per-monitor DPI awareness for multi-monitor setups

### Application Manifest Benefits
The manifest file ensures:
- Windows 11 properly identifies the application as compatible
- Correct visual styles and theming
- Proper DPI scaling behavior
- Security context is properly defined

## Compatibility Notes

### Backward Compatibility
All changes maintain backward compatibility with:
- Windows 7, 8, 8.1, and 10
- Existing Belvedere rules and configurations
- AutoHotkey v1.x scripts

### Migration from Previous Versions
Users upgrading from previous versions should note:
- The new default installation location is `%LOCALAPPDATA%\Belvedere`
- Registry keys are now stored in HKCU instead of HKLM
- Existing rules.ini files can be copied to the new location

## Testing Recommendations

To verify Windows 11 compatibility:
1. Install on a Windows 11 system using the new installer
2. Verify the application runs without UAC prompts
3. Test on high-DPI displays (verify crisp rendering)
4. Verify all file operations work correctly
5. Test the application survives Windows 11 updates
6. Verify startup shortcuts work correctly

## Future Considerations

For full Windows 11 optimization, future updates could include:
- Windows 11 visual style updates
- Integration with Windows 11 notification system
- Support for Windows 11 dark mode
- WinUI 3 or modern UI framework migration (long-term)
