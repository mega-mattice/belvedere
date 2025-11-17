"""
Recycle Bin Manager for Belvedere.

Handles automatic management of recycle bin contents based on configured rules:
- Age-based cleanup (remove files older than X time)
- Size-based cleanup (keep under size limit using various strategies)
- Scheduled auto-empty functionality
"""

import os
import platform
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .config import Config


class RecycleBinEntry:
    """Represents a file in the recycle bin with metadata."""

    def __init__(self, path: Path, original_path: Optional[str] = None,
                 deletion_date: Optional[datetime] = None):
        """Initialize recycle bin entry.

        Args:
            path: Current path in recycle bin
            original_path: Original file path before deletion
            deletion_date: When file was deleted
        """
        self.path = path
        self.original_path = original_path or str(path)
        self.deletion_date = deletion_date or datetime.fromtimestamp(path.stat().st_mtime)
        self.size = path.stat().st_size if path.exists() else 0


class RecycleBinManager:
    """Manages recycle bin contents according to configured rules."""

    def __init__(self, config: Config):
        """Initialize recycle bin manager.

        Args:
            config: Belvedere configuration instance
        """
        self.config = config
        self.system = platform.system()

    def get_recycle_bin_paths(self) -> List[Path]:
        """Get platform-appropriate recycle bin paths.

        Returns:
            List of paths to check for recycle bin contents
        """
        if self.system == "Windows":
            # Windows Recycle Bin - check all drive letters
            paths = []
            for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                recycle_path = Path(f"{drive}:\\$Recycle.Bin")
                if recycle_path.exists():
                    paths.append(recycle_path)
            return paths

        elif self.system == "Darwin":  # macOS
            # macOS Trash
            home = Path.home()
            return [home / ".Trash"]

        elif self.system == "Linux":
            # Linux trash directories (XDG spec)
            paths = []
            home = Path.home()
            data_home = os.environ.get("XDG_DATA_HOME", home / ".local" / "share")
            paths.append(Path(data_home) / "Trash")

            # Also check common mount points for external drives
            for mount_point in ["/media", "/mnt"]:
                if Path(mount_point).exists():
                    for item in Path(mount_point).iterdir():
                        if item.is_dir():
                            trash_path = item / ".Trash"
                            if trash_path.exists():
                                paths.append(trash_path)

            return paths
        else:
            return []

    def get_recycle_bin_contents(self) -> List[RecycleBinEntry]:
        """Get all files currently in the recycle bin.

        Returns:
            List of RecycleBinEntry objects
        """
        entries = []

        for recycle_path in self.get_recycle_bin_paths():
            try:
                if not recycle_path.exists():
                    continue

                # Different handling for different platforms
                if self.system == "Windows":
                    entries.extend(self._get_windows_recycle_bin_contents(recycle_path))
                elif self.system == "Darwin":  # macOS
                    entries.extend(self._get_unix_recycle_bin_contents(recycle_path))
                elif self.system == "Linux":
                    entries.extend(self._get_linux_recycle_bin_contents(recycle_path))

            except (OSError, PermissionError) as e:
                print(f"Error accessing recycle bin at {recycle_path}: {e}")
                continue

        return entries

    def _get_windows_recycle_bin_contents(self, recycle_path: Path) -> List[RecycleBinEntry]:
        """Get Windows recycle bin contents."""
        entries = []

        try:
            # Windows Recycle Bin structure: $Recycle.Bin/SID/filename
            for sid_dir in recycle_path.iterdir():
                if not sid_dir.is_dir():
                    continue

                # Each SID directory contains files and metadata
                for item in sid_dir.iterdir():
                    if item.is_file():
                        # Try to get metadata from $I file if it exists
                        metadata_file = sid_dir / f"$I{item.name[2:]}" if item.name.startswith("$R") else None
                        deletion_date = None

                        if metadata_file and metadata_file.exists():
                            try:
                                # Windows $I files contain metadata including deletion time
                                # This is complex to parse, so we'll use file modification time as approximation
                                deletion_date = datetime.fromtimestamp(metadata_file.stat().st_mtime)
                            except:
                                pass

                        entries.append(RecycleBinEntry(
                            path=item,
                            original_path=self._extract_windows_original_path(item, metadata_file),
                            deletion_date=deletion_date
                        ))

        except Exception as e:
            print(f"Error reading Windows recycle bin: {e}")

        return entries

    def _get_unix_recycle_bin_contents(self, recycle_path: Path) -> List[RecycleBinEntry]:
        """Get Unix-like (macOS/Linux) recycle bin contents."""
        entries = []

        try:
            for item in recycle_path.iterdir():
                if item.is_file():
                    entries.append(RecycleBinEntry(path=item))

        except Exception as e:
            print(f"Error reading Unix recycle bin: {e}")

        return entries

    def _get_linux_recycle_bin_contents(self, recycle_path: Path) -> List[RecycleBinEntry]:
        """Get Linux trash contents with metadata."""
        entries = []

        try:
            files_dir = recycle_path / "files"
            info_dir = recycle_path / "info"

            if files_dir.exists():
                for item in files_dir.iterdir():
                    if item.is_file():
                        # Check for .trashinfo file
                        info_file = info_dir / f"{item.name}.trashinfo"
                        original_path = None
                        deletion_date = None

                        if info_file.exists():
                            try:
                                # Parse .trashinfo file
                                with open(info_file, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    # Parse [Trash Info] format
                                    for line in content.split('\n'):
                                        if line.startswith('Path='):
                                            original_path = line[5:]
                                        elif line.startswith('DeletionDate='):
                                            # ISO format: 2023-11-17T10:30:45
                                            date_str = line[13:]
                                            try:
                                                deletion_date = datetime.fromisoformat(date_str.replace('T', ' '))
                                            except:
                                                pass
                            except Exception:
                                pass

                        entries.append(RecycleBinEntry(
                            path=item,
                            original_path=original_path,
                            deletion_date=deletion_date
                        ))

        except Exception as e:
            print(f"Error reading Linux trash: {e}")

        return entries

    def _extract_windows_original_path(self, file_path: Path, metadata_file: Optional[Path]) -> str:
        """Extract original path from Windows recycle bin metadata."""
        if metadata_file and metadata_file.exists():
            try:
                # This is a simplified version - full parsing would be more complex
                with open(metadata_file, 'rb') as f:
                    # Skip header and read original path (Unicode string)
                    f.seek(24)  # Skip header
                    data = f.read()
                    # Look for null-terminated Unicode string
                    path_end = data.find(b'\x00\x00')
                    if path_end > 0:
                        path_bytes = data[:path_end + 2]
                        return path_bytes.decode('utf-16-le', errors='ignore').rstrip('\x00')
            except:
                pass

        # Fallback: just return the filename
        return file_path.name

    def manage_by_age(self, max_age_days: int) -> int:
        """Remove files from recycle bin older than specified days.

        Args:
            max_age_days: Maximum age in days

        Returns:
            Number of files deleted
        """
        if max_age_days <= 0:
            return 0

        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        entries = self.get_recycle_bin_contents()
        deleted_count = 0

        for entry in entries:
            if entry.deletion_date < cutoff_date:
                try:
                    entry.path.unlink()
                    deleted_count += 1
                    # Also remove metadata files if they exist
                    self._cleanup_metadata_files(entry.path)
                except (OSError, PermissionError) as e:
                    print(f"Error deleting {entry.path}: {e}")

        return deleted_count

    def manage_by_size(self, max_size_mb: int, deletion_approach: str = "Oldest First") -> int:
        """Keep recycle bin under size limit using specified deletion approach.

        Args:
            max_size_mb: Maximum size in MB
            deletion_approach: "Oldest First", "Largest First", "Smallest First"

        Returns:
            Number of files deleted
        """
        if max_size_mb <= 0:
            return 0

        max_size_bytes = max_size_mb * 1024 * 1024
        entries = self.get_recycle_bin_contents()

        if not entries:
            return 0

        # Calculate current total size
        total_size = sum(entry.size for entry in entries)

        if total_size <= max_size_bytes:
            return 0  # Already under limit

        # Sort entries based on deletion approach
        if deletion_approach == "Oldest First":
            entries.sort(key=lambda x: x.deletion_date)
        elif deletion_approach == "Largest First":
            entries.sort(key=lambda x: x.size, reverse=True)
        elif deletion_approach == "Smallest First":
            entries.sort(key=lambda x: x.size)
        elif deletion_approach == "Youngest First":
            entries.sort(key=lambda x: x.deletion_date, reverse=True)
        else:
            entries.sort(key=lambda x: x.deletion_date)  # Default to oldest first

        deleted_count = 0
        for entry in entries:
            if total_size <= max_size_bytes:
                break

            try:
                entry.path.unlink()
                total_size -= entry.size
                deleted_count += 1
                # Also remove metadata files if they exist
                self._cleanup_metadata_files(entry.path)
            except (OSError, PermissionError) as e:
                print(f"Error deleting {entry.path}: {e}")

        return deleted_count

    def auto_empty(self) -> int:
        """Empty entire recycle bin.

        Returns:
            Number of files deleted
        """
        entries = self.get_recycle_bin_contents()
        deleted_count = 0

        for entry in entries:
            try:
                entry.path.unlink()
                deleted_count += 1
                # Also remove metadata files if they exist
                self._cleanup_metadata_files(entry.path)
            except (OSError, PermissionError) as e:
                print(f"Error deleting {entry.path}: {e}")

        return deleted_count

    def _cleanup_metadata_files(self, file_path: Path):
        """Clean up associated metadata files."""
        try:
            # Windows $I files
            if file_path.name.startswith("$R"):
                metadata_file = file_path.parent / f"$I{file_path.name[2:]}"
                if metadata_file.exists():
                    metadata_file.unlink()

            # Linux .trashinfo files
            elif self.system == "Linux":
                trash_info = Path(str(file_path).replace("/files/", "/info/") + ".trashinfo")
                if trash_info.exists():
                    trash_info.unlink()

        except Exception:
            pass  # Ignore cleanup errors

    def apply_recycle_bin_rules(self) -> Dict[str, int]:
        """Apply all configured recycle bin management rules.

        Returns:
            Dict with counts of deleted files by rule type
        """
        prefs = self.config.get_preferences()
        rb_prefs = prefs.get("recycle_bin", {})

        if not rb_prefs.get("enabled", False):
            return {"disabled": 0}

        results = {"age_based": 0, "size_based": 0, "auto_empty": 0}

        try:
            # Age-based management
            if rb_prefs.get("manage_age", False):
                age_value = rb_prefs.get("age_value", 0)
                age_unit = rb_prefs.get("age_unit", "days")

                # Convert to days
                if age_unit == "minutes":
                    age_days = age_value / (24 * 60)
                elif age_unit == "hours":
                    age_days = age_value / 24
                elif age_unit == "weeks":
                    age_days = age_value * 7
                else:  # days
                    age_days = age_value

                results["age_based"] = self.manage_by_age(int(age_days))

            # Size-based management
            if rb_prefs.get("manage_size", False):
                size_value = rb_prefs.get("size_value", 0)
                size_unit = rb_prefs.get("size_unit", "MB")
                deletion_approach = rb_prefs.get("deletion_approach", "Oldest First")

                # Convert to MB
                if size_unit == "KB":
                    size_mb = size_value / 1024
                else:  # MB
                    size_mb = size_value

                results["size_based"] = self.manage_by_size(int(size_mb), deletion_approach)

            # Auto-empty (this would be called on schedule, not here)
            # The auto_empty logic would be handled by the timer in main.py

        except Exception as e:
            print(f"Error applying recycle bin rules: {e}")

        return results
