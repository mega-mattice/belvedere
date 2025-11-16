# Building Belvedere

This document describes how to build Belvedere for distribution.

## Automated Releases (Recommended)

Belvedere uses GitHub Actions to automatically build executables for all platforms when a new release is published:

1. Create a new release on GitHub (via the Releases page or `gh release create`)
2. The workflow automatically builds executables for:
   - Windows (`.exe`)
   - macOS (`.zip`)
   - Linux (`.tar.gz`)
3. Built executables are automatically uploaded to the release

See `.github/workflows/release.yml` for the workflow configuration.

## Manual Building

For local development and testing, you can build manually:

## Prerequisites

- Python 3.9 or later (up to 3.13)
- Poetry (for dependency management)

## Installing Poetry

If you don't have Poetry installed, install it using pip:

```bash
pip install poetry
```

Or follow the official installation instructions at [python-poetry.org](https://python-poetry.org/docs/#installation)

## Installing Dependencies

Install all dependencies (including development dependencies):

```bash
poetry install
```

To install only production dependencies:

```bash
poetry install --only main
```

## Running Belvedere

You can run Belvedere directly using Poetry:

```bash
poetry run belvedere
```

Or activate the virtual environment and run it:

```bash
poetry shell
belvedere
```

## Running Tests

Run the test suite:

```bash
poetry run python test_belvedere.py
```

## Building Executables with PyInstaller

Belvedere can be packaged as a standalone executable for Windows using PyInstaller.

### Building for Windows

1. Ensure you're on Windows or have a Windows build environment
2. Install dependencies (including dev dependencies):

```bash
poetry install
```

3. Build the executable:

```bash
poetry run pyinstaller belvedere.spec
```

The executable will be created in the `dist/` directory.

### Build Configuration

The build is configured via `belvedere.spec`. Key features:

- **Single file executable**: All dependencies bundled into one file
- **Windowed mode**: No console window appears
- **Icon**: Uses `resources/belvedere.ico`
- **Resources**: Includes all images from the resources directory

### Customizing the Build

To modify the build configuration, edit `belvedere.spec`. Common customizations:

- **Add data files**: Add entries to the `datas` list
- **Add hidden imports**: Add entries to the `hiddenimports` list
- **Change icon**: Modify the `icon` parameter in the `EXE` section

## Building for Other Platforms

While PyInstaller can build for multiple platforms, you must build on the target platform:

- **Windows**: Build on Windows to create `.exe`
- **macOS**: Build on macOS to create `.app`
- **Linux**: Build on Linux to create a Linux binary

To generate a spec file for your platform:

```bash
poetry run pyinstaller --name belvedere --onefile --windowed --icon resources/belvedere.ico belvedere.py
```

Then customize the generated `belvedere.spec` as needed.

## Distribution Checklist

Before distributing a build:

1. ✅ Test on a clean system without Python installed
2. ✅ Verify the icon displays correctly
3. ✅ Test all file operations (move, copy, delete, etc.)
4. ✅ Verify system tray functionality
5. ✅ Check that configuration is saved and loaded properly
6. ✅ Test with various file types and rules

## Troubleshooting Build Issues

### Missing Dependencies

If PyInstaller misses a dependency, add it to `hiddenimports` in `belvedere.spec`:

```python
hiddenimports=[
    'missing_module',
],
```

### Missing Data Files

If resource files are missing, add them to `datas` in `belvedere.spec`:

```python
datas=[
    ('path/to/file', 'destination/folder'),
],
```

### Build Size

To reduce build size:

- Use `--exclude-module` to exclude unnecessary modules
- Remove unused Qt modules from the build
- Disable UPX compression if it causes issues: set `upx=False` in spec file

## Poetry Commands Reference

Useful Poetry commands for development:

```bash
# Install dependencies
poetry install

# Add a new dependency
poetry add package-name

# Add a development dependency
poetry add --group dev package-name

# Update dependencies
poetry update

# Show installed packages
poetry show

# Activate virtual environment
poetry shell

# Run a command in the virtual environment
poetry run python script.py
```
