# Belvedere Troubleshooting Guide

This guide helps you resolve common issues with Belvedere.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Startup Issues](#startup-issues)
- [Rule Issues](#rule-issues)
- [Performance Issues](#performance-issues)
- [File Operation Issues](#file-operation-issues)
- [Windows 11 Specific Issues](#windows-11-specific-issues)
- [General Issues](#general-issues)

## Installation Issues

### Installer Won't Run

**Symptoms**: Double-clicking installer does nothing or shows error.

**Solutions**:

1. **Unblock the file**:
   - Right-click the installer file
   - Select "Properties"
   - Check "Unblock" at the bottom
   - Click "Apply" then "OK"
   - Try running again

2. **Run as Administrator** (if needed):
   - Right-click the installer
   - Select "Run as administrator"

3. **Check Windows SmartScreen**:
   - If SmartScreen blocks it, click "More info"
   - Click "Run anyway"

4. **Disable Antivirus Temporarily**:
   - Some antivirus software may block installation
   - Temporarily disable and try again
   - Re-enable after installation

### Installation Fails with Error

**Symptoms**: Installer shows error message during installation.

**Solutions**:

1. **Close Belvedere if running**:
   - Right-click system tray icon
   - Select "Exit"
   - Try installation again

2. **Check Disk Space**:
   - Ensure you have at least 10 MB free space
   - Installation requires space in `%LOCALAPPDATA%`

3. **Check Permissions**:
   - Ensure you have write access to `%LOCALAPPDATA%`
   - Try running installer as administrator

4. **Clean Previous Installation**:
   - Uninstall previous version completely
   - Delete `%LOCALAPPDATA%\Belvedere` folder
   - Try installing again

### Can't Find Installation

**Symptoms**: Installation completed but can't find Belvedere.

**Solutions**:

1. **Check Installation Location**:
   - Default location: `%LOCALAPPDATA%\Belvedere`
   - Press Windows + R, type `%LOCALAPPDATA%\Belvedere`
   - Press Enter to open the folder

2. **Check Start Menu**:
   - Open Start Menu
   - Search for "Belvedere"
   - Should appear in the list

3. **Check Desktop**:
   - Look for Belvedere shortcut on desktop
   - Created if option was selected during installation

## Startup Issues

### Belvedere Won't Start

**Symptoms**: Running Belvedere does nothing or shows an error.

**Solutions**:

1. **Check if Already Running**:
   - Look for Belvedere icon in system tray
   - Check Task Manager/Activity Monitor for belvedere process
   - If running, right-click tray icon to show window

2. **Check Python Installation**:
   - Ensure Python 3.8+ is installed
   - Download from [python.org](https://www.python.org/)
   - Reinstall if necessary

3. **Run from Command Line**:
   - Open Command Prompt
   - Navigate to Belvedere folder
   - Run: `python belvedere.py`
   - Check for error messages

4. **Check Rules File**:
   - Corrupted `rules.json` may prevent startup
   - Rename `rules.json` to `rules.json.bak`
   - Try starting Belvedere
   - If it works, rules file was corrupted

5. **Reinstall Belvedere**:
   - Backup your `rules.json` file
   - Uninstall Belvedere
   - Reinstall
   - Restore `rules.json`

### No System Tray Icon

**Symptoms**: Belvedere starts but no icon in system tray.

**Solutions**:

1. **Check Hidden Icons**:
   - Click the up arrow (^) in system tray
   - Belvedere icon may be in hidden icons area

2. **Show Belvedere Icon**:
   - Right-click taskbar
   - Select "Taskbar settings"
   - Click "Select which icons appear on the taskbar"
   - Find Belvedere and turn it ON

3. **Restart Windows Explorer**:
   - Press Ctrl+Shift+Esc to open Task Manager
   - Find "Windows Explorer"
   - Right-click → "Restart"
   - Tray icon should reappear

### Belvedere Won't Run at Startup

**Symptoms**: Belvedere doesn't start automatically when Windows boots.

**Solutions**:

1. **Check Startup Folder**:
   - Press Windows + R
   - Type: `shell:startup`
   - Press Enter
   - Look for Belvedere shortcut
   - If missing, create one

2. **Create Startup Shortcut**:
   - Right-click in Startup folder
   - Select New → Shortcut
   - Browse to `python -m belvedere.main`
   - Click Finish

3. **Check Task Manager Startup**:
   - Press Ctrl+Shift+Esc
   - Click "Startup" tab
   - Find Belvedere
   - Ensure it's "Enabled"
   - If "Disabled", right-click and select "Enable"

4. **Check for Errors**:
   - Try starting Belvedere manually
   - If it won't start, see "Belvedere Won't Start" section

## Rule Issues

### Rules Not Running

**Symptoms**: Files matching rules aren't being processed.

**Solutions**:

1. **Check Rule is Enabled**:
   - Open Belvedere Rules window
   - Select the rule
   - Ensure checkbox "Enable this rule" is checked
   - Click Enable/Disable button to verify status

2. **Check Folder is Being Monitored**:
   - Verify folder appears in Folders list
   - Folder path must be correct and accessible

3. **Check Rule Conditions**:
   - Verify conditions match the files you expect
   - Test with simple condition first
   - Use "Confirm before taking action" to debug

4. **Check Match Type**:
   - "All" requires ALL conditions to match
   - "Any" requires just ONE condition to match
   - Verify you're using the correct option

5. **Check File Access**:
   - Ensure files aren't locked/in use
   - Close any programs using the files
   - Try again

6. **Restart Belvedere**:
   - Sometimes rules need a restart to activate
   - Right-click tray icon → Exit
   - Start Belvedere again

### Rules Running on Wrong Files

**Symptoms**: Rules act on files you didn't intend.

**Solutions**:

1. **Review Rule Conditions**:
   - Make conditions more specific
   - Add additional conditions to narrow matches
   - Use "All" match type for stricter matching

2. **Test with Confirmation**:
   - Enable "Confirm before taking action"
   - Review what files match
   - Adjust conditions as needed

3. **Check for Wildcards**:
   - "contains" is very broad
   - Consider using "is" for exact matches
   - Be specific with file names/extensions

4. **Check Case Sensitivity**:
   - Belvedere comparisons are case-insensitive
   - "PDF" matches "pdf", "Pdf", "pDF", etc.

### Rules Run Too Slowly

**Symptoms**: Files sit for a long time before being processed.

**Solutions**:

1. **Reduce Sleeptime**:
   - Open Preferences tab
   - Reduce Sleeptime value (in milliseconds)
   - Default is 5000 (5 seconds)
   - Try 2000-3000 for faster response
   - Click "Save Preferences"

2. **Reduce Recursive Scanning**:
   - If using recursive option, it scans all subfolders
   - This can be slow for large folder trees
   - Consider monitoring specific subfolders instead

3. **Limit Number of Rules**:
   - Each rule is evaluated for each file
   - Many rules = slower processing
   - Combine or simplify rules where possible

### Can't Delete/Move Files

**Symptoms**: Rule runs but files aren't deleted/moved.

**Solutions**:

1. **Check File Permissions**:
   - Ensure you have permission to modify files
   - Right-click file → Properties → Security
   - Verify you have necessary permissions

2. **Check File is Not Locked**:
   - Close any programs using the files
   - Some files may be locked by Windows or other programs
   - Try manually to verify

3. **Check Destination Exists**:
   - For Move/Copy actions, destination folder must exist
   - Create destination folder if needed
   - Verify path is correct

4. **Check Disk Space**:
   - Ensure destination has enough free space
   - Move/Copy won't work without space

5. **Check Overwrite Setting**:
   - If destination file exists and overwrite is off
   - File won't be moved/copied
   - Enable "Overwrite existing files" if desired

## Performance Issues

### High CPU Usage

**Symptoms**: Belvedere uses excessive CPU resources.

**Solutions**:

1. **Increase Sleeptime**:
   - Open Preferences tab
   - Increase Sleeptime value
   - Try 10000 (10 seconds) or higher
   - Click "Save Preferences"

2. **Reduce Monitored Folders**:
   - Remove folders that don't need monitoring
   - Monitor specific subfolders instead of parent folders

3. **Disable Recursive Scanning**:
   - Recursive scanning is CPU-intensive
   - Uncheck "Recursive" option on rules
   - Monitor specific folders instead

4. **Simplify Rules**:
   - Complex rules with many conditions take longer
   - Simplify where possible
   - Remove unnecessary conditions

5. **Reduce Number of Rules**:
   - Each rule is evaluated for every file
   - Combine similar rules if possible
   - Remove unused rules

### High Memory Usage

**Symptoms**: Belvedere uses excessive RAM.

**Solutions**:

1. **Restart Belvedere**:
   - Exit Belvedere completely
   - Restart it
   - Memory usage should normalize

2. **Reduce Monitored Folders**:
   - Large folders with many files use more memory
   - Monitor only necessary folders

3. **Update Belvedere**:
   - Ensure you have the latest version
   - Check for updates

### Slow Computer When Running

**Symptoms**: Computer is sluggish when Belvedere is running.

**Solutions**:

1. **All CPU/Memory solutions above**
2. **Limit Active Rules**:
   - Disable rules not currently needed
   - Enable only when necessary
3. **Schedule Heavy Processing**:
   - Use Windows Task Scheduler
   - Run Belvedere during low-usage times

## File Operation Issues

### Files Disappearing

**Symptoms**: Files vanish unexpectedly.

**Solutions**:

1. **Check Rules**:
   - Review all enabled rules
   - Look for Delete or Recycle actions
   - Verify rule conditions

2. **Check Recycle Bin**:
   - Files may have been recycled
   - Open Recycle Bin and look for files
   - Restore if needed

3. **Check Move Destinations**:
   - Files may have been moved
   - Check destination folders in rules
   - Search for files by name

4. **Enable Confirmations**:
   - Enable "Confirm before taking action"
   - Review actions before they happen
   - Prevents accidental deletions

5. **Disable Aggressive Rules**:
   - Temporarily disable Delete/Recycle rules
   - Re-enable one at a time to identify culprit

### Duplicate Files

**Symptoms**: Same files appear in multiple locations.

**Solutions**:

1. **Check Copy Rules**:
   - Copy action creates duplicates
   - If you want to move instead, change action to Move

2. **Check Overwrite Setting**:
   - Files may be copied multiple times
   - Enable "Overwrite existing files"

3. **Use Move Instead of Copy**:
   - Move removes from source
   - Copy leaves original

### Wrong File Renamed

**Symptoms**: Files renamed incorrectly.

**Solutions**:

1. **Review Rename Pattern**:
   - Check pattern in Rename action
   - Verify variables are correct
   - Test pattern with confirmation first

2. **Make Conditions More Specific**:
   - Add more conditions to narrow matches
   - Ensure only intended files match

## Windows 11 Specific Issues

### Blurry Text on High-DPI Display

**Symptoms**: Belvedere appears blurry on 4K or high-resolution display.

**Solutions**:

1. **Check Manifest File**:
   - Ensure `Belvedere.manifest` exists in installation folder
   - Should be included with v0.5+

2. **Override DPI Settings** (if needed):
   - Right-click python script
   - Select Properties
   - Click "Compatibility" tab
   - Click "Change high DPI settings"
   - Check "Override high DPI scaling behavior"
   - Select "Application" from dropdown
   - Click OK

3. **Update to Latest Version**:
   - Ensure you have v0.5 or later
   - Earlier versions don't support high-DPI displays

### UAC Prompts

**Symptoms**: User Account Control prompts when using Belvedere.

**Solutions**:

1. **Use User-Level Installation**:
   - Ensure installed to `%LOCALAPPDATA%\Belvedere`
   - Not to `Program Files`
   - v0.5+ installs to correct location by default

2. **Don't Run as Administrator**:
   - Don't run Belvedere as administrator unless necessary
   - User-level works for most scenarios

3. **Check Folder Permissions**:
   - Ensure monitored folders don't require admin access
   - Don't monitor system folders

### Windows Defender Blocks Belvedere

**Symptoms**: Windows Defender removes or blocks Belvedere.

**Solutions**:

1. **Add Exclusion**:
   - Open Windows Security
   - Go to Virus & threat protection
   - Click "Manage settings"
   - Scroll to Exclusions
   - Click "Add or remove exclusions"
   - Add the Belvedere folder

2. **Restore if Quarantined**:
   - Open Windows Security
   - Go to Protection history
   - Find Belvedere
   - Click Restore

3. **Submit False Positive**:
   - If repeatedly blocked, it may be a false positive
   - Submit to Microsoft for review

## General Issues

### Can't Open Rules Window

**Symptoms**: Clicking "Manage Rules" does nothing.

**Solutions**:

1. **Check if Window is Hidden**:
   - Press Alt+Tab to see all open windows
   - Rules window may be behind other windows
   - Click to bring to front

2. **Restart Belvedere**:
   - Exit completely
   - Start again
   - Try opening rules window

3. **Check Rules File**:
   - Corrupted rules.json may prevent window opening
   - Rename rules.json to rules.json.bak
   - Restart Belvedere
   - Try opening rules window

### Lost All Rules

**Symptoms**: All rules disappeared.

**Solutions**:

1. **Check Rules File**:
   - Navigate to `%LOCALAPPDATA%\Belvedere`
   - Look for `rules.json`
   - If missing, rules were deleted
   - Restore from backup if available

2. **Restore from Backup**:
   - If you have a backup of rules.json
   - Close Belvedere
   - Copy backup to installation folder
   - Restart Belvedere

3. **Check Correct Installation Folder**:
   - Belvedere may have installed to different location
   - Search for other Belvedere folders
   - Copy rules.json from old location

### Error Messages

#### "Cannot find folder"

**Cause**: Monitored folder was deleted or moved.

**Solution**:
- Remove the folder from Belvedere
- Re-add it if it should exist
- Or remove associated rules

#### "Cannot access file"

**Cause**: File is locked by another program or insufficient permissions.

**Solution**:
- Close programs using the file
- Check file permissions
- Ensure you have access rights

#### "Destination folder does not exist"

**Cause**: Move/Copy destination folder doesn't exist.

**Solution**:
- Create the destination folder
- Or update rule to use existing folder

## Getting More Help

If you're still experiencing issues:

1. **Check Documentation**:
   - [Installation Guide](installation.md)
   - [Getting Started Guide](getting-started.md)
   - [Usage Guide](usage.md)

2. **Backup Your Configuration**:
   - Always backup `rules.json` before troubleshooting
   - Located in `%LOCALAPPDATA%\Belvedere`

3. **Test with Fresh Install**:
   - Backup rules.json
   - Uninstall completely
   - Delete `%LOCALAPPDATA%\Belvedere`
   - Reinstall
   - Test without rules first
   - If works, restore rules one at a time

4. **Report Issues**:
   - Visit the GitHub repository
   - Check existing issues
   - Create new issue with:
     - Windows version
     - Belvedere version
     - Detailed description of problem
     - Steps to reproduce
     - Error messages if any

## Preventing Issues

### Best Practices

1. **Backup Rules Regularly**:
   - Copy rules.json to safe location
   - Before major changes
   - Before updates

2. **Test New Rules**:
   - Enable "Confirm before taking action"
   - Test on copies first
   - Verify behavior before going live

3. **Keep Belvedere Updated**:
   - Check for updates periodically
   - Backup before updating

4. **Monitor Results**:
   - Regularly check that rules work as expected
   - Review destination folders
   - Verify files are processed correctly

5. **Use Specific Rules**:
   - Make conditions as specific as possible
   - Reduces unexpected behavior
   - Easier to debug

6. **Start Simple**:
   - Begin with simple rules
   - Add complexity gradually
   - Easier to troubleshoot

### Maintenance

1. **Review Rules Quarterly**:
   - Remove unused rules
   - Update as needed
   - Simplify complex rules

2. **Clean Up Monitored Folders**:
   - Remove folders no longer needed
   - Update paths if folders moved

3. **Check Performance**:
   - Monitor CPU/memory usage
   - Adjust sleeptime as needed
   - Optimize rules

4. **Verify Backups**:
   - Test that backups work
   - Keep multiple backup versions
   - Store in safe location
