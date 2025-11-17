#!/usr/bin/env python3
"""
Test script for Belvedere functionality.

Tests the core components without requiring a GUI.
"""

import tempfile
from pathlib import Path

from belvedere.config import Config
from belvedere.rule_engine import RuleEngine


def test_config():
    """Test configuration management."""
    print("Testing configuration management...")

    # Create temporary config file
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_rules.json"
        config = Config(config_path)

        # Test folder management
        test_folder = "/tmp/test_folder"
        config.add_folder(test_folder)
        assert test_folder in config.get_folders(), "Failed to add folder"

        # Test rule management
        test_rule = {
            "folder": test_folder,
            "enabled": True,
            "conditions": [{"subject": "Name", "verb": "is", "object": "test"}],
            "action": "Move file",
            "destination": "/tmp/dest",
        }
        config.add_rule("test_rule", test_rule)
        rules = config.get_rules(test_folder)
        assert "test_rule" in rules, "Failed to add rule"

        # Test preferences
        config.update_preferences({"sleep_time": 10000})
        prefs = config.get_preferences()
        assert prefs["sleep_time"] == 10000, "Failed to update preferences"

        # Test persistence
        config.save()
        config2 = Config(config_path)
        assert test_folder in config2.get_folders(), "Config not persisted"

    print("✓ Configuration management tests passed")


def test_rule_engine():
    """Test rule engine."""
    print("\nTesting rule engine...")

    engine = RuleEngine()

    # Create test files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Test file with specific name
        test_file = tmpdir_path / "test_document.txt"
        test_file.write_text("test content")

        # Test name matching
        rule = {"conditions": [{"subject": "Name", "verb": "is", "object": "test_document"}], "match_type": "ALL"}
        result = engine.evaluate_rule(test_file, rule)
        assert result, "Failed to match file name"

        # Test extension matching
        rule = {"conditions": [{"subject": "Extension", "verb": "is", "object": "txt"}], "match_type": "ALL"}
        result = engine.evaluate_rule(test_file, rule)
        assert result, "Failed to match extension"

        # Test size matching
        rule = {
            "conditions": [{"subject": "Size", "verb": "is greater than", "object": "1", "units": "KB"}],
            "match_type": "ALL",
        }
        result = engine.evaluate_rule(test_file, rule)
        assert not result, "Size comparison failed"

        # Test contains
        rule = {"conditions": [{"subject": "Name", "verb": "contains", "object": "document"}], "match_type": "ALL"}
        result = engine.evaluate_rule(test_file, rule)
        assert result, "Failed to match contains"

        # Test multiple conditions (ALL)
        rule = {
            "conditions": [
                {"subject": "Name", "verb": "contains", "object": "test"},
                {"subject": "Extension", "verb": "is", "object": "txt"},
            ],
            "match_type": "ALL",
        }
        result = engine.evaluate_rule(test_file, rule)
        assert result, "Failed to match ALL conditions"

        # Test multiple conditions (ANY)
        rule = {
            "conditions": [
                {"subject": "Name", "verb": "is", "object": "wrong_name"},
                {"subject": "Extension", "verb": "is", "object": "txt"},
            ],
            "match_type": "ANY",
        }
        result = engine.evaluate_rule(test_file, rule)
        assert result, "Failed to match ANY conditions"

    print("✓ Rule engine tests passed")


def test_file_operations():
    """Test file operations."""
    print("\nTesting file operations...")

    engine = RuleEngine()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Test copy operation
        src_file = tmpdir_path / "source.txt"
        src_file.write_text("test content")
        dest_dir = tmpdir_path / "dest"
        dest_dir.mkdir()

        rule = {"action": "Copy file", "destination": str(dest_dir), "overwrite": False}
        result = engine.execute_action(src_file, rule)
        assert result, "Copy failed"
        assert (dest_dir / "source.txt").exists(), "File not copied"
        assert src_file.exists(), "Source file removed during copy"

        # Test move operation
        src_file2 = tmpdir_path / "source2.txt"
        src_file2.write_text("test content 2")

        rule = {"action": "Move file", "destination": str(dest_dir), "overwrite": False}
        result = engine.execute_action(src_file2, rule)
        assert result, "Move failed"
        assert (dest_dir / "source2.txt").exists(), "File not moved"
        assert not src_file2.exists(), "Source file not removed after move"

        # Test rename operation
        rename_file = tmpdir_path / "rename_test.txt"
        rename_file.write_text("rename test")

        rule = {"action": "Rename file", "destination": "renamed.txt", "overwrite": False}
        result = engine.execute_action(rename_file, rule)
        assert result, "Rename failed"
        assert (tmpdir_path / "renamed.txt").exists(), "File not renamed"
        assert not rename_file.exists(), "Original file still exists"

        # Test delete operation
        delete_file = tmpdir_path / "delete_test.txt"
        delete_file.write_text("delete test")

        rule = {"action": "Delete file"}
        result = engine.execute_action(delete_file, rule)
        assert result, "Delete failed"
        assert not delete_file.exists(), "File not deleted"

    print("✓ File operation tests passed")


def test_date_rules():
    """Test date-based rules."""
    print("\nTesting date-based rules...")

    engine = RuleEngine()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Create a file and modify it
        test_file = tmpdir_path / "date_test.txt"
        test_file.write_text("test")

        # Test "is in the last" for recent file
        rule = {
            "conditions": [{"subject": "Date last modified", "verb": "is in the last", "object": "1", "units": "days"}],
            "match_type": "ALL",
        }
        result = engine.evaluate_rule(test_file, rule)
        assert result, "Failed to match recent modification date"

        # Test "is not in the last" for recent file
        rule = {
            "conditions": [{"subject": "Date last modified", "verb": "is not in the last", "object": "1", "units": "minutes"}],
            "match_type": "ALL",
        }
        result = engine.evaluate_rule(test_file, rule)
        assert not result, "Incorrectly matched old date"

    print("✓ Date-based rule tests passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Belvedere Core Functionality Tests")
    print("=" * 60)

    try:
        test_config()
        test_rule_engine()
        test_file_operations()
        test_date_rules()

        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
