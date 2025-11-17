#!/usr/bin/env python3
"""
Quick start script for Belvedere.

This script checks for dependencies and launches Belvedere with helpful error messages.
"""

import sys


def check_python_version():
    """Check if Python version is sufficient."""
    if sys.version_info < (3, 8):
        print("Error: Belvedere requires Python 3.8 or later.")
        print(f"You are running Python {sys.version_info.major}.{sys.version_info.minor}")
        print("\nPlease upgrade Python:")
        print("  - Download from: https://www.python.org/downloads/")
        print("  - Or use your system's package manager")
        return False
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    missing = []

    try:
        import PySide6  # noqa: F401
    except ImportError:
        missing.append("PySide6")

    try:
        import watchdog  # noqa: F401
    except ImportError:
        missing.append("watchdog")

    try:
        import send2trash  # noqa: F401
    except ImportError:
        missing.append("send2trash")

    if missing:
        print("Error: Missing required dependencies:")
        for dep in missing:
            print(f"  - {dep}")
        print("\nTo install dependencies, run:")
        print("  pip install -r requirements.txt")
        print("\nOr install as a package:")
        print("  pip install -e .")
        return False

    return True


def check_display():
    """Check if display is available (Linux/Unix)."""
    import os
    import platform

    if platform.system() in ["Linux", "FreeBSD", "OpenBSD"]:
        if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
            print("Warning: No display detected.")
            print("Belvedere requires a graphical desktop environment.")
            print("\nIf you're using SSH, try:")
            print("  - SSH with X11 forwarding: ssh -X user@host")
            print("  - Or run Belvedere on the local machine")
            return False

    return True


def main():
    """Main entry point."""
    print("=" * 60)
    print("Belvedere - Automated File Management")
    print("=" * 60)
    print()

    # Check Python version
    if not check_python_version():
        return 1

    # Check dependencies
    if not check_dependencies():
        return 1

    # Check display (informational warning only)
    check_display()

    print("Starting Belvedere...")
    print("(The application will run in the system tray)")
    print()

    # Import and run the application
    try:
        from belvedere.main import main as belvedere_main

        return belvedere_main()
    except Exception as e:
        print(f"\nError starting Belvedere: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
