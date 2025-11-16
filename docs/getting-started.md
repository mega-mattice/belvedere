# Getting Started with Belvedere

Welcome to Belvedere! This guide will help you get up and running quickly with automated file management.

## What is Belvedere?

Belvedere is an automated file management tool that allows you to set up rules for organizing your files. It can automatically move, copy, delete, or rename files based on:

- File name patterns
- File extensions
- File size
- File age (date created, modified, or last opened)

Once configured, Belvedere runs quietly in the background, keeping your folders organized automatically.

## First Launch

When you first launch Belvedere:

1. **System Tray Icon**: Belvedere runs in the system tray (notification area)
   - Look for the Belvedere icon in the bottom-right corner of your screen
   - Right-click the icon to access the menu

2. **Main Window**: Click the system tray icon or right-click and select "Manage Rules" to open the main window

## Quick Start: Creating Your First Rule

Let's create a simple rule to organize downloaded files.

### Example: Organize Downloads by File Type

This rule will automatically move image files from your Downloads folder to a Pictures subfolder.

1. **Open Belvedere Rules Window**
   - Right-click the Belvedere system tray icon
   - Select "Manage Rules"

2. **Add a Watched Folder**
   - In the "Folders" tab, click the "+" button under the Folders list
   - Browse to your Downloads folder (usually `C:\Users\YourName\Downloads`)
   - Click "OK"

3. **Create a New Rule**
   - Select your Downloads folder from the list
   - Click the "+" button under the Rules list
   - A new rule editor window will appear

4. **Configure the Rule**
   - **Rule Name**: Enter a descriptive name like "Move Images to Pictures"
   - **Conditions**: Set up when the rule should trigger
     - Subject: "Extension"
     - Verb: "is"
     - Object: "jpg" (you can add more extensions later)
   - **Action**: What to do with matching files
     - Action: "Move"
     - Destination: Browse to `Downloads\Pictures` (create the folder if needed)
   - **Options**:
     - Check "Enable this rule" to activate it
     - Optionally check "Confirm before taking action" to review before moving files

5. **Save the Rule**
   - Click "OK" to save your rule
   - The rule is now active!

### Adding More File Extensions

To make the rule work with multiple image types:

1. **Edit the Rule**
   - Select the rule and click "Edit Rule"

2. **Add More Conditions**
   - Click "Add Condition" button
   - Subject: "Extension", Verb: "is", Object: "png"
   - Click "Add Condition" again for more types (gif, bmp, etc.)

3. **Set Match Type**
   - At the top, set "Match" to "Any" (matches if ANY condition is true)
   - Or use "All" if you want files to match ALL conditions

## Understanding the Main Window

### Folders Tab

- **Folders List**: Shows all folders being monitored by Belvedere
- **Rules List**: Shows all rules for the selected folder
- **+ / - Buttons**: Add or remove folders and rules
- **Edit Rule**: Modify an existing rule
- **Enable/Disable**: Quickly enable or disable a rule

### Recycle Bin Tab

Belvedere can automatically manage your Recycle Bin:

- **Remove old files**: Automatically delete files older than X days
- **Manage size**: Keep Recycle Bin under a certain size
- **Empty regularly**: Empty the Recycle Bin on a schedule
- **Deletion approach**: Choose how to delete (oldest first, largest first, etc.)

### Preferences Tab

- **Sleeptime**: How often Belvedere checks for files (in milliseconds)
  - Default: 5000 (5 seconds)
  - Lower values = more responsive but uses more CPU
  - Higher values = less CPU usage but slower response

## Running Belvedere at Startup

To make Belvedere start automatically when Windows boots:

1. **Create Shortcut**
   - Press `Windows + R` to open Run dialog
   - Type: `shell:startup` and press Enter
   - This opens your Startup folder

2. **Add Belvedere**
   - Right-click in the Startup folder
   - Select "New" → "Shortcut"
   - Browse to Belvedere.exe (usually in `%LOCALAPPDATA%\Belvedere`)
   - Click "Finish"

Now Belvedere will start automatically when you log in to Windows.

## Understanding Rule Components

### Subjects (What to Check)

- **Name**: The file's name (without extension)
- **Extension**: The file type (.txt, .jpg, .pdf, etc.)
- **Size**: The file size in bytes
- **Date created**: When the file was created
- **Date last modified**: When the file was last changed
- **Date last opened**: When the file was last accessed

### Verbs (How to Compare)

- **is**: Exact match
- **is not**: Does not match exactly
- **contains**: Contains the text
- **does not contain**: Does not contain the text
- **is greater than**: For numbers/dates (newer/larger)
- **is less than**: For numbers/dates (older/smaller)

### Objects (What to Match)

- For **text subjects** (Name, Extension): Enter the text to match
- For **size**: Enter number in bytes (1 MB = 1,048,576 bytes)
- For **dates**: Enter days (e.g., "30" for 30 days ago)

### Actions (What to Do)

- **Move**: Move files to destination folder
- **Copy**: Copy files to destination folder
- **Delete**: Delete files permanently
- **Recycle**: Move files to Recycle Bin
- **Rename**: Rename files (using pattern)
- **Open**: Open files with default application

## Common Use Cases

### 1. Clean Up Old Files
- Subject: "Date last modified"
- Verb: "is greater than"
- Object: "90" (90 days)
- Action: "Recycle"

### 2. Organize by File Type
- Subject: "Extension"
- Verb: "is"
- Object: "pdf"
- Action: "Move"
- Destination: Specific folder

### 3. Archive Large Files
- Subject: "Size"
- Verb: "is greater than"
- Object: "104857600" (100 MB)
- Action: "Move"
- Destination: Archive folder

### 4. Process Screenshots
- Subject: "Name"
- Verb: "contains"
- Object: "Screenshot"
- Action: "Move"
- Destination: Screenshots folder

## Tips for Effective Use

1. **Start Simple**: Begin with one or two rules and expand gradually
2. **Test First**: Use "Confirm before taking action" when testing new rules
3. **Be Specific**: Make rules as specific as possible to avoid unintended actions
4. **Monitor**: Check the results of your rules regularly
5. **Backup**: Keep backups of important files before creating delete rules
6. **Combine Conditions**: Use multiple conditions for precise control

## Safety Features

- **Confirmation**: Enable "Confirm before taking action" to review each action
- **Disable Rules**: Quickly disable rules without deleting them
- **Recycle Instead of Delete**: Use "Recycle" action instead of "Delete" for safety
- **Test Folders**: Test rules on a copy of your files first

## Need More Help?

- **Detailed Usage**: See the [Usage Guide](usage.md) for complete feature documentation
- **Troubleshooting**: Check the [Troubleshooting Guide](troubleshooting.md) for common issues
- **Installation**: See the [Installation Guide](installation.md) for setup help

## Next Steps

Now that you understand the basics:

1. Create a few simple rules for your most cluttered folders
2. Enable confirmation on new rules until you're confident they work correctly
3. Monitor your rules for a few days
4. Expand and refine your rules as needed
5. Explore advanced features like recursive folder scanning and Recycle Bin management

Happy organizing!
