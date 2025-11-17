# Belvedere Usage Guide

This comprehensive guide covers all features and functionality of Belvedere.

## Table of Contents

- [Overview](#overview)
- [Managing Folders](#managing-folders)
- [Creating and Editing Rules](#creating-and-editing-rules)
- [Rule Subjects](#rule-subjects)
- [Rule Verbs](#rule-verbs)
- [Rule Actions](#rule-actions)
- [Advanced Rule Options](#advanced-rule-options)
- [Recycle Bin Management](#recycle-bin-management)
- [Preferences and Settings](#preferences-and-settings)
- [System Tray Menu](#system-tray-menu)
- [Rules File Format](#rules-file-format)
- [Best Practices](#best-practices)

## Overview

Belvedere is an automated file management tool that monitors specified folders and takes actions on files based on rules you define. It runs continuously in the background, periodically checking folders and applying rules.

### How Belvedere Works

1. **Monitoring**: Belvedere monitors folders you specify
2. **Checking**: Every few seconds (configurable), it scans these folders
3. **Matching**: Files are checked against your rules
4. **Acting**: When a file matches a rule's conditions, the specified action is performed
5. **Repeating**: The cycle continues indefinitely

## Managing Folders

Folders are the locations that Belvedere monitors for files to process.

### Adding a Folder

1. Open Belvedere (right-click system tray icon → "Manage Rules")
2. In the Folders tab, click the "+" button below the Folders list
3. Browse to the folder you want to monitor
4. Click "OK"

The folder will now appear in the Folders list.

### Removing a Folder

1. Select the folder in the Folders list
2. Click the "-" button below the Folders list
3. Confirm the deletion

**Note**: Removing a folder also removes all rules associated with that folder.

### Folder Best Practices

- **Don't monitor system folders**: Avoid monitoring Windows system folders
- **Be specific**: Monitor specific folders rather than entire drives
- **Test first**: Start with less critical folders to test your rules
- **Performance**: Monitoring many large folders can impact performance

## Creating and Editing Rules

Rules define what files to act on and what to do with them.

### Creating a New Rule

1. Select a folder from the Folders list
2. Click the "+" button below the Rules list
3. The Rule Editor window opens

### Rule Editor Components

#### Rule Name
Enter a descriptive name that explains what the rule does.
- Good: "Move old PDFs to Archive"
- Bad: "Rule 1"

#### Enable This Rule
Check this box to activate the rule. Uncheck to temporarily disable it.

#### Match Conditions
Choose how multiple conditions are evaluated:
- **All**: File must match ALL conditions (AND logic)
- **Any**: File must match ANY condition (OR logic)

#### Conditions
Define one or more conditions that files must meet:

1. Click "Add Condition" to add a new condition
2. Select:
   - **Subject**: What property of the file to check
   - **Verb**: How to compare it
   - **Object**: The value to compare against
3. Add more conditions as needed

#### Action Section
Define what to do with matching files:

- **Action**: Select the action to perform (Move, Copy, Delete, etc.)
- **Destination**: For Move/Copy actions, specify the target folder
- **Options**:
  - **Confirm before taking action**: Show confirmation dialog before acting
  - **Recursive**: Also check files in subfolders
  - **Overwrite existing files**: Replace files with same name in destination

### Editing an Existing Rule

1. Select the folder containing the rule
2. Select the rule in the Rules list
3. Click "Edit Rule"
4. Make your changes
5. Click "OK" to save

### Enabling/Disabling Rules

Quickly enable or disable a rule without editing:

1. Select the rule in the Rules list
2. Click the "Enable" or "Disable" button

The button text changes based on the rule's current state.

### Deleting a Rule

1. Select the rule in the Rules list
2. Click the "-" button below the Rules list
3. Confirm the deletion

## Rule Subjects

Subjects define what property of a file to examine.

### Name
The filename without the extension.

**Example**: For "document.pdf", the name is "document"

**Common Uses**:
- Match files with specific names
- Match files containing certain text
- Organize files by naming pattern

**Example Conditions**:
- Name is "Screenshot" - matches exactly "Screenshot"
- Name contains "backup" - matches "backup-2024", "file-backup", etc.

### Extension
The file type/extension.

**Example**: For "document.pdf", the extension is "pdf"

**Common Uses**:
- Organize files by type
- Process specific file formats
- Filter out unwanted file types

**Example Conditions**:
- Extension is "jpg" - matches .jpg files
- Extension is not "tmp" - matches all except .tmp files

**Note**: Don't include the dot. Use "pdf" not ".pdf"

### Size
The file size in bytes.

**Common Uses**:
- Archive or delete large files
- Filter by file size
- Free up disk space

**Size Conversions**:
- 1 KB = 1,024 bytes
- 1 MB = 1,048,576 bytes
- 10 MB = 10,485,760 bytes
- 100 MB = 104,857,600 bytes
- 1 GB = 1,073,741,824 bytes

**Example Conditions**:
- Size is greater than "1048576" - files larger than 1 MB
- Size is less than "1024" - files smaller than 1 KB

### Date Created
When the file was originally created.

**Common Uses**:
- Archive old files
- Delete temporary files
- Organize by creation date

**Format**: Enter number of days
- "30" means 30 days ago
- "365" means one year ago

**Example Conditions**:
- Date created is greater than "90" - files created more than 90 days ago
- Date created is less than "7" - files created in the last 7 days

### Date Last Modified
When the file was last changed.

**Common Uses**:
- Clean up stale files
- Archive inactive files
- Backup recently modified files

**Format**: Enter number of days (same as Date Created)

**Example Conditions**:
- Date last modified is greater than "30" - files not modified in 30+ days
- Date last modified is less than "1" - files modified today

### Date Last Opened
When the file was last accessed/opened.

**Common Uses**:
- Remove unused files
- Archive files that haven't been accessed
- Clean up forgotten downloads

**Format**: Enter number of days (same as Date Created)

**Example Conditions**:
- Date last opened is greater than "180" - files not opened in 6+ months
- Date last opened is less than "7" - files opened this week

**Note**: Not all file systems track access time accurately.

## Rule Verbs

Verbs define how to compare the subject with the object.

### Text Comparisons

#### is
Exact match (case-insensitive).

**Examples**:
- Name is "report" - matches "report" exactly
- Extension is "pdf" - matches .pdf files

#### is not
Does not match exactly (case-insensitive).

**Examples**:
- Extension is not "tmp" - matches everything except .tmp files
- Name is not "keepme" - matches all files except those named "keepme"

#### contains
Subject contains the object text (case-insensitive).

**Examples**:
- Name contains "backup" - matches "backup-file", "mybackup", "backup"
- Name contains "2024" - matches any filename with "2024" in it

#### does not contain
Subject does not contain the object text (case-insensitive).

**Examples**:
- Name does not contain "temp" - excludes files with "temp" in the name
- Extension does not contain "doc" - excludes .doc and .docx files

### Numeric and Date Comparisons

#### is greater than
For numbers: larger than the specified value.
For dates: older than the specified number of days.

**Examples**:
- Size is greater than "1048576" - files larger than 1 MB
- Date created is greater than "30" - files older than 30 days

#### is less than
For numbers: smaller than the specified value.
For dates: newer than the specified number of days.

**Examples**:
- Size is less than "1024" - files smaller than 1 KB
- Date modified is less than "7" - files modified in the last week

## Rule Actions

Actions define what to do with files that match the rule conditions.

### Move
Moves files to the specified destination folder.

**Settings**:
- **Destination**: Required - specify target folder
- **Overwrite**: Optional - replace existing files with same name

**Use Cases**:
- Organize files by type into folders
- Archive old files
- Sort downloads automatically

**Example**: Move image files from Downloads to Pictures folder

### Copy
Copies files to the destination folder, leaving original in place.

**Settings**:
- **Destination**: Required - specify target folder
- **Overwrite**: Optional - replace existing files with same name

**Use Cases**:
- Create backups
- Duplicate files to multiple locations
- Keep originals while organizing copies

**Example**: Copy important documents to a backup folder

### Delete
Permanently deletes files (bypasses Recycle Bin).

**Settings**: None

**Use Cases**:
- Remove temporary files
- Clean up old downloads
- Free disk space

**Warning**: Deleted files cannot be recovered. Consider using "Recycle" instead.

### Recycle
Moves files to the Windows Recycle Bin.

**Settings**: None

**Use Cases**:
- Safely remove files with ability to recover
- Clean up while maintaining safety net
- Temporary file removal

**Example**: Recycle files older than 90 days

### Rename
Renames files based on a pattern.

**Settings**:
- **Pattern**: Specify new filename pattern

**Use Cases**:
- Add prefixes or suffixes
- Standardize naming conventions
- Add dates to filenames

**Pattern Variables**:
- `{name}` - Original filename
- `{date}` - Current date
- `{time}` - Current time
- `{ext}` - File extension

**Example**: Rename to "backup-{name}-{date}.{ext}"

### Open
Opens files with their default application.

**Settings**: None

**Use Cases**:
- Auto-open new downloads
- Launch specific files automatically
- Trigger applications

**Example**: Open new PDF files as they're downloaded

## Advanced Rule Options

### Confirm Before Taking Action

When enabled, Belvedere will show a confirmation dialog before performing the action.

**Benefits**:
- Review what will happen before it happens
- Prevent accidental deletions
- Test new rules safely

**Use When**:
- Testing new rules
- Working with important files
- Using Delete action
- Learning how rules work

### Recursive

When enabled, the rule applies to files in subfolders as well as the main folder.

**Benefits**:
- Process entire folder structures
- Clean up nested directories
- Comprehensive file management

**Use When**:
- Folder has many subfolders
- Need to process all files regardless of location
- Organizing complex folder structures

**Warning**: Can process many files - use with caution and test first.

### Overwrite Existing Files

When enabled, Move/Copy actions will replace existing files in the destination.

**Benefits**:
- Keep only newest versions
- Update files automatically
- Simplify file synchronization

**Use When**:
- Intentionally updating files
- Replacing old versions
- Consolidating duplicates

**Warning**: Overwrites permanently replace files. Ensure you want this behavior.

## Recycle Bin Management

Belvedere can automatically manage your Windows Recycle Bin.

### Enabling Recycle Bin Management

1. Open Belvedere Rules window
2. Click the "Recycle Bin" tab
3. Check "Allow Belvedere to manage my Recycle Bin"
4. Configure desired options
5. Click "Save Preferences"

### Options

#### Remove Files by Age
Automatically delete files from Recycle Bin older than specified time.

**Settings**:
- **Time Value**: Number (e.g., 30)
- **Time Unit**: Days, Weeks, or Months

**Example**: Remove files older than 30 days

#### Manage Recycle Bin Size
Keep Recycle Bin under a specific size.

**Settings**:
- **Size Value**: Number (e.g., 5)
- **Size Unit**: MB or GB

**Example**: Keep Recycle Bin under 5 GB

#### Deletion Approach
Choose which files to delete first when size limit is reached:

- **Oldest First**: Delete oldest files first
- **Largest First**: Delete largest files first
- **Smallest First**: Delete smallest files first

#### Empty Recycle Bin Regularly
Automatically empty entire Recycle Bin on a schedule.

**Settings**:
- **Time Value**: Number (e.g., 7)
- **Time Unit**: Days, Weeks, or Months

**Example**: Empty Recycle Bin every 7 days

## Preferences and Settings

### Sleeptime

Controls how often Belvedere checks folders for files to process.

**Setting**: Time in milliseconds
- Default: 5000 (5 seconds)
- Minimum: 1000 (1 second)
- Maximum: No limit

**Considerations**:
- **Lower values** (1000-3000ms):
  - Faster response
  - More CPU usage
  - Better for frequently changing folders

- **Higher values** (10000-30000ms):
  - Less CPU usage
  - Slower response
  - Better for static folders
  - Better for battery life

**Recommended Settings**:
- Active downloads folder: 3000-5000ms
- Archive folders: 30000-60000ms
- General use: 5000-10000ms

### Saving Settings

After changing preferences:

1. Click "Save Preferences"
2. Changes take effect immediately

## System Tray Menu

Right-click the Belvedere icon in the system tray to access:

- **Manage Rules**: Open main configuration window
- **Pause/Resume**: Temporarily stop/start processing
- **Exit**: Close Belvedere

## Rules File Format

Belvedere stores all rules in a JSON file in your user configuration directory:
- **Linux/macOS**: `~/.config/belvedere/rules.json`
- **Windows**: `%USERPROFILE%\.belvedere\rules.json`

### Backup Your Rules

To backup your configuration:

1. Locate your configuration directory:
   - Linux/macOS: `~/.config/belvedere/`
   - Windows: `%USERPROFILE%\.belvedere\`
2. Copy `rules.json` to a safe location
3. Store the backup securely

### Restore Rules

To restore from backup:

1. Close Belvedere completely
2. Navigate to configuration directory
3. Replace `rules.json` with your backup
4. Restart Belvedere

### Sharing Rules

You can share your rules configuration:

1. Copy your `rules.json` file from configuration directory
2. Share it with others
3. They can place it in their configuration directory
4. Restart Belvedere to load new rules

**Note**: Ensure folder paths exist on the target system, or edit paths in the JSON file.

## Best Practices

### Rule Design

1. **Be Specific**: Make rules as specific as possible to avoid unintended matches
2. **Start Simple**: Begin with simple rules and add complexity as needed
3. **Use Descriptive Names**: Name rules clearly to remember their purpose
4. **Test First**: Always test rules with confirmation enabled first

### Safety

1. **Enable Confirmations**: Use "Confirm before taking action" for new or risky rules
2. **Use Recycle**: Prefer "Recycle" over "Delete" for file removal
3. **Backup Important Files**: Always maintain backups of critical files
4. **Test on Copies**: Test rules on copies of files before applying to originals

### Performance

1. **Optimize Sleeptime**: Adjust based on your needs
2. **Limit Recursive Scans**: Use recursive scanning sparingly
3. **Monitor Few Folders**: Don't monitor more folders than necessary
4. **Specific Conditions**: Use specific conditions to reduce processing

### Organization

1. **Group Related Rules**: Keep related rules together
2. **Disable vs Delete**: Disable rules temporarily instead of deleting
3. **Document Complex Rules**: Use clear names for complex rule logic
4. **Review Regularly**: Periodically review and update your rules

### Maintenance

1. **Check Results**: Regularly verify rules are working as expected
2. **Update Rules**: Modify rules as your needs change
3. **Clean Up**: Remove unused rules
4. **Backup Configuration**: Regularly backup your `rules.json` file

## Advanced Tips

### Multiple Conditions

Combine conditions for precise control:

**Example**: Move large, old PDFs
- Subject: Extension, Verb: is, Object: pdf
- Subject: Size, Verb: is greater than, Object: 10485760 (10MB)
- Subject: Date modified, Verb: is greater than, Object: 180
- Match: All

### Date-Based Organization

Create folders by date automatically:

1. Use Move action
2. Set destination to folder with date pattern
3. Use recursive to organize subdirectories

### File Type Organization

Organize downloads by category:

- **Documents**: pdf, doc, docx, txt → Documents folder
- **Images**: jpg, png, gif, bmp → Pictures folder
- **Videos**: mp4, avi, mkv → Videos folder
- **Archives**: zip, rar, 7z → Archives folder

Create separate rules for each category.

### Temporary File Cleanup

Remove temporary files automatically:

- Match extension: tmp, temp, cache
- Action: Delete
- Add confirmation for safety

### Project Organization

Keep project folders clean:

- Remove files older than 90 days
- Archive large files
- Organize by file type

## Need Help?

- **Getting Started**: See [Getting Started Guide](getting-started.md)
- **Installation**: See [Installation Guide](installation.md)
- **Troubleshooting**: See [Troubleshooting Guide](troubleshooting.md)
