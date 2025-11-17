"""
Rule engine for evaluating file conditions and executing actions.

This module contains the logic for:
- Evaluating subjects (file attributes)
- Applying verbs (comparison operations)
- Executing actions on files
"""

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import send2trash


class RuleEngine:
    """Evaluates rules and executes actions on files."""

    def __init__(self):
        """Initialize the rule engine."""
        pass

    def evaluate_rule(self, file_path: Path, rule: Dict[str, Any]) -> bool:
        """Evaluate if a file matches a rule.

        Args:
            file_path: Path to the file to evaluate.
            rule: Rule configuration dictionary.

        Returns:
            True if file matches the rule, False otherwise.
        """
        if not file_path.exists() or not file_path.is_file():
            return False

        conditions = rule.get("conditions", [])
        if not conditions:
            return False

        match_type = rule.get("match_type", "ALL")

        results = []
        for condition in conditions:
            result = self._evaluate_condition(file_path, condition)
            results.append(result)

            # Short-circuit evaluation
            if match_type == "ANY" and result:
                return True
            elif match_type == "ALL" and not result:
                return False

        # Final evaluation
        if match_type == "ALL":
            return all(results)
        else:  # ANY
            return any(results)

    def _evaluate_condition(self, file_path: Path, condition: Dict[str, Any]) -> bool:
        """Evaluate a single condition.

        Args:
            file_path: Path to the file.
            condition: Condition dictionary with subject, verb, object, and units.

        Returns:
            True if condition matches, False otherwise.
        """
        subject_type = condition.get("subject")
        verb = condition.get("verb")
        obj = condition.get("object")
        units = condition.get("units")

        # Get the subject value from the file
        subject_value = self._get_subject_value(file_path, subject_type)

        # Apply the verb comparison
        return self._apply_verb(subject_value, verb, obj, units, subject_type)

    def _get_subject_value(self, file_path: Path, subject_type: str) -> Any:
        """Get the value of a file attribute.

        Args:
            file_path: Path to the file.
            subject_type: Type of attribute (Name, Extension, Size, etc.).

        Returns:
            The attribute value.
        """
        if subject_type == "Name":
            return file_path.stem
        elif subject_type == "Extension":
            return file_path.suffix.lstrip(".").lower()
        elif subject_type == "Size":
            return file_path.stat().st_size
        elif subject_type == "Date last modified":
            return datetime.fromtimestamp(file_path.stat().st_mtime)
        elif subject_type == "Date last opened":
            return datetime.fromtimestamp(file_path.stat().st_atime)
        elif subject_type == "Date created":
            return datetime.fromtimestamp(file_path.stat().st_ctime)
        else:
            return None

    def _apply_verb(self, subject_value: Any, verb: str, obj: str, units: Optional[str], subject_type: str) -> bool:
        """Apply a comparison verb.

        Args:
            subject_value: The file attribute value.
            verb: The comparison operation.
            obj: The comparison value.
            units: Units for the comparison (for sizes and dates).
            subject_type: Type of subject being compared.

        Returns:
            True if comparison matches, False otherwise.
        """
        if subject_value is None:
            return False

        # String comparisons
        if verb == "is":
            return str(subject_value).lower() == str(obj).lower()
        elif verb == "is not":
            return str(subject_value).lower() != str(obj).lower()
        elif verb == "contains":
            return str(obj).lower() in str(subject_value).lower()
        elif verb == "does not contain":
            return str(obj).lower() not in str(subject_value).lower()
        elif verb == "matches one of":
            options = [opt.strip().lower() for opt in str(obj).split(",")]
            return str(subject_value).lower() in options
        elif verb == "does not match one of":
            options = [opt.strip().lower() for opt in str(obj).split(",")]
            return str(subject_value).lower() not in options

        # Numeric comparisons (for size)
        elif verb in ["is greater than", "is less than"]:
            if subject_type == "Size":
                # Convert object to bytes based on units
                obj_value = float(obj)
                if units == "KB":
                    obj_value *= 1024
                elif units == "MB":
                    obj_value *= 1024 * 1024

                if verb == "is greater than":
                    return subject_value > obj_value
                else:  # is less than
                    return subject_value < obj_value

        # Date comparisons
        elif verb in ["is in the last", "is not in the last"]:
            if isinstance(subject_value, datetime):
                obj_value = float(obj)
                now = datetime.now()

                # Convert to timedelta based on units
                if units == "minutes":
                    threshold = now - timedelta(minutes=obj_value)
                elif units == "hours":
                    threshold = now - timedelta(hours=obj_value)
                elif units == "days":
                    threshold = now - timedelta(days=obj_value)
                elif units == "weeks":
                    threshold = now - timedelta(weeks=obj_value)
                else:
                    return False

                if verb == "is in the last":
                    return subject_value >= threshold
                else:  # is not in the last
                    return subject_value < threshold

        return False

    def execute_action(self, file_path: Path, rule: Dict[str, Any]) -> bool:
        """Execute the action specified in the rule.

        Args:
            file_path: Path to the file.
            rule: Rule configuration dictionary.

        Returns:
            True if action was successful, False otherwise.
        """
        action = rule.get("action")
        destination = rule.get("destination")
        overwrite = rule.get("overwrite", False)

        try:
            if action == "Move file":
                return self._move_file(file_path, destination, overwrite)
            elif action == "Copy file":
                return self._copy_file(file_path, destination, overwrite)
            elif action == "Rename file":
                return self._rename_file(file_path, destination, overwrite)
            elif action == "Delete file":
                return self._delete_file(file_path)
            elif action == "Send file to Recycle Bin":
                return self._recycle_file(file_path)
            elif action == "Open file":
                return self._open_file(file_path)
            else:
                return False
        except Exception as e:
            print(f"Error executing action {action} on {file_path}: {e}")
            return False

    def _move_file(self, file_path: Path, destination: str, overwrite: bool) -> bool:
        """Move a file to a destination.

        Args:
            file_path: Source file path.
            destination: Destination path.
            overwrite: Whether to overwrite existing files.

        Returns:
            True if successful, False otherwise.
        """
        dest_path = Path(destination)
        if not dest_path.exists():
            return False

        if dest_path.is_dir():
            dest_file = dest_path / file_path.name
        else:
            dest_file = dest_path

        if dest_file.exists() and not overwrite:
            return False

        shutil.move(str(file_path), str(dest_file))
        return True

    def _copy_file(self, file_path: Path, destination: str, overwrite: bool) -> bool:
        """Copy a file to a destination.

        Args:
            file_path: Source file path.
            destination: Destination path.
            overwrite: Whether to overwrite existing files.

        Returns:
            True if successful, False otherwise.
        """
        dest_path = Path(destination)
        if not dest_path.exists():
            return False

        if dest_path.is_dir():
            dest_file = dest_path / file_path.name
        else:
            dest_file = dest_path

        if dest_file.exists() and not overwrite:
            return False

        shutil.copy2(str(file_path), str(dest_file))
        return True

    def _rename_file(self, file_path: Path, new_name: str, overwrite: bool) -> bool:
        """Rename a file.

        Args:
            file_path: Source file path.
            new_name: New file name.
            overwrite: Whether to overwrite existing files.

        Returns:
            True if successful, False otherwise.
        """
        dest_file = file_path.parent / new_name

        if dest_file.exists() and not overwrite:
            return False

        file_path.rename(dest_file)
        return True

    def _delete_file(self, file_path: Path) -> bool:
        """Delete a file permanently.

        Args:
            file_path: File to delete.

        Returns:
            True if successful, False otherwise.
        """
        file_path.unlink()
        return True

    def _recycle_file(self, file_path: Path) -> bool:
        """Send a file to the recycle bin.

        Args:
            file_path: File to recycle.

        Returns:
            True if successful, False otherwise.
        """
        send2trash.send2trash(str(file_path))
        return True

    def _open_file(self, file_path: Path) -> bool:
        """Open a file with the default application.

        Args:
            file_path: File to open.

        Returns:
            True if successful, False otherwise.
        """
        import platform
        import subprocess

        system = platform.system()
        if system == "Windows":
            os.startfile(str(file_path))
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(file_path)])
        else:  # Linux and others
            subprocess.run(["xdg-open", str(file_path)])

        return True
