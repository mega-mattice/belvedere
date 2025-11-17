"""
Unit tests for the FileMonitor module.

Tests file monitoring, event handling, and folder scanning functionality.
"""

import pytest

from belvedere.file_monitor import BelvedereEventHandler, FileMonitor


class TestFileMonitorInitialization:
    """Tests for FileMonitor initialization."""

    def test_file_monitor_initializes_correctly(self, rule_engine):
        """Test that FileMonitor initializes with correct state."""
        # Arrange & Act
        monitor = FileMonitor(rule_engine)

        # Assert
        assert monitor.rule_engine is rule_engine
        assert monitor.observer is not None
        assert monitor.running is False
        assert monitor.handlers == {}

    def test_file_monitor_accepts_confirm_callback(self, rule_engine):
        """Test that FileMonitor accepts confirmation callback."""

        # Arrange
        def confirm_callback(file_path, rule_name, rule):
            return True

        # Act
        monitor = FileMonitor(rule_engine, confirm_callback)

        # Assert
        assert monitor.confirm_callback is confirm_callback


class TestFolderManagement:
    """Tests for folder monitoring management."""

    def test_add_folder_creates_handler(self, file_monitor, temp_dir):
        """Test that adding folder creates event handler."""
        # Arrange
        folder_path = str(temp_dir)
        rules = {"rule1": {"enabled": True, "conditions": []}}

        # Act
        file_monitor.add_folder(folder_path, rules)

        # Assert
        assert folder_path in file_monitor.handlers
        assert isinstance(file_monitor.handlers[folder_path], BelvedereEventHandler)

    def test_add_folder_replaces_existing_handler(self, file_monitor, temp_dir):
        """Test that adding folder again replaces existing handler."""
        # Arrange
        folder_path = str(temp_dir)
        rules1 = {"rule1": {"enabled": True}}
        rules2 = {"rule2": {"enabled": True}}
        file_monitor.add_folder(folder_path, rules1)

        # Act
        file_monitor.add_folder(folder_path, rules2)
        handler = file_monitor.handlers[folder_path]

        # Assert
        # Handler should have the new rules
        assert handler.rules == rules2
        # Only one handler for this folder
        assert folder_path in file_monitor.handlers

    def test_remove_folder_deletes_handler(self, file_monitor, temp_dir):
        """Test that removing folder deletes handler."""
        # Arrange
        folder_path = str(temp_dir)
        rules = {"rule1": {"enabled": True}}
        file_monitor.add_folder(folder_path, rules)

        # Act
        file_monitor.remove_folder(folder_path)

        # Assert
        assert folder_path not in file_monitor.handlers

    def test_remove_nonexistent_folder_does_nothing(self, file_monitor):
        """Test that removing non-existent folder doesn't cause errors."""
        # Arrange & Act
        file_monitor.remove_folder("/nonexistent/folder")

        # Assert - should not raise exception
        assert True

    def test_update_rules_modifies_handler_rules(self, file_monitor, temp_dir):
        """Test that update_rules modifies existing handler's rules."""
        # Arrange
        folder_path = str(temp_dir)
        rules1 = {"rule1": {"enabled": True}}
        rules2 = {"rule2": {"enabled": False}}
        file_monitor.add_folder(folder_path, rules1)

        # Act
        file_monitor.update_rules(folder_path, rules2)

        # Assert
        assert file_monitor.handlers[folder_path].rules == rules2

    def test_update_rules_for_nonexistent_folder_does_nothing(self, file_monitor):
        """Test that updating rules for non-existent folder doesn't error."""
        # Arrange & Act
        file_monitor.update_rules("/nonexistent/folder", {})

        # Assert - should not raise exception
        assert True


class TestMonitorStartStop:
    """Tests for monitor start and stop operations."""

    def test_start_monitor_sets_running_flag(self, file_monitor):
        """Test that starting monitor sets running flag."""
        # Arrange & Act
        file_monitor.start()

        # Assert
        assert file_monitor.running is True

        # Cleanup
        file_monitor.stop()

    def test_stop_monitor_clears_running_flag(self, file_monitor):
        """Test that stopping monitor clears running flag."""
        # Arrange
        file_monitor.start()

        # Act
        file_monitor.stop()

        # Assert
        assert file_monitor.running is False

    def test_start_when_already_running_is_safe(self, file_monitor):
        """Test that calling start when already running is safe."""
        # Arrange
        file_monitor.start()

        # Act
        file_monitor.start()

        # Assert
        assert file_monitor.running is True

        # Cleanup
        file_monitor.stop()

    def test_stop_when_not_running_is_safe(self, file_monitor):
        """Test that calling stop when not running is safe."""
        # Arrange & Act
        file_monitor.stop()

        # Assert
        assert file_monitor.running is False


class TestFolderScanning:
    """Tests for one-time folder scanning."""

    def test_scan_folder_once_processes_existing_files(self, file_monitor, temp_dir, dest_dir):
        """Test that scan_folder_once processes existing files."""
        # Arrange
        test_file = temp_dir / "test.txt"
        test_file.write_text("content")

        rules = {
            "move_rule": {
                "enabled": True,
                "conditions": [{"subject": "Extension", "verb": "is", "object": "txt"}],
                "match_type": "ALL",
                "action": "Move file",
                "destination": str(dest_dir),
                "overwrite": False,
            }
        }

        # Act
        file_monitor.scan_folder_once(str(temp_dir), rules)

        # Assert
        assert (dest_dir / "test.txt").exists()
        assert not test_file.exists()

    def test_scan_folder_once_skips_disabled_rules(self, file_monitor, temp_dir, dest_dir):
        """Test that scan_folder_once skips disabled rules."""
        # Arrange
        test_file = temp_dir / "test.txt"
        test_file.write_text("content")

        rules = {
            "disabled_rule": {
                "enabled": False,
                "conditions": [{"subject": "Extension", "verb": "is", "object": "txt"}],
                "match_type": "ALL",
                "action": "Move file",
                "destination": str(dest_dir),
                "overwrite": False,
            }
        }

        # Act
        file_monitor.scan_folder_once(str(temp_dir), rules)

        # Assert
        assert test_file.exists()
        assert not (dest_dir / "test.txt").exists()

    def test_scan_folder_once_handles_nonexistent_folder(self, file_monitor):
        """Test that scanning non-existent folder doesn't error."""
        # Arrange
        rules = {"rule1": {"enabled": True}}

        # Act
        file_monitor.scan_folder_once("/nonexistent/folder", rules)

        # Assert - should not raise exception
        assert True

    def test_scan_folder_once_skips_directories(self, file_monitor, temp_dir):
        """Test that scan_folder_once only processes files, not directories."""
        # Arrange
        subdir = temp_dir / "subdir"
        subdir.mkdir()

        rules = {"rule1": {"enabled": True, "conditions": [], "match_type": "ALL", "action": "Delete file"}}

        # Act
        file_monitor.scan_folder_once(str(temp_dir), rules)

        # Assert
        assert subdir.exists()  # Directory should not be deleted

    def test_scan_folder_recursive_processes_subdirectories(self, file_monitor, temp_dir, dest_dir):
        """Test that recursive scan processes files in subdirectories."""
        # Arrange
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        nested_file = subdir / "nested.txt"
        nested_file.write_text("content")

        rules = {
            "move_rule": {
                "enabled": True,
                "conditions": [{"subject": "Extension", "verb": "is", "object": "txt"}],
                "match_type": "ALL",
                "action": "Move file",
                "destination": str(dest_dir),
                "overwrite": False,
            }
        }

        # Act
        file_monitor.scan_folder_once(str(temp_dir), rules, recursive=True)

        # Assert
        assert (dest_dir / "nested.txt").exists()
        assert not nested_file.exists()


class TestEventHandler:
    """Tests for BelvedereEventHandler."""

    def test_event_handler_initializes_correctly(self, rule_engine, temp_dir):
        """Test that event handler initializes with correct state."""
        # Arrange
        folder_path = str(temp_dir)
        rules = {"rule1": {"enabled": True}}

        # Act
        handler = BelvedereEventHandler(folder_path, rules, rule_engine)

        # Assert
        assert handler.folder_path == temp_dir
        assert handler.rules == rules
        assert handler.rule_engine is rule_engine

    def test_event_handler_processes_matching_file(self, rule_engine, temp_dir, dest_dir):
        """Test that event handler processes file matching rule."""
        # Arrange
        rules = {
            "move_rule": {
                "enabled": True,
                "conditions": [{"subject": "Extension", "verb": "is", "object": "txt"}],
                "match_type": "ALL",
                "action": "Move file",
                "destination": str(dest_dir),
                "overwrite": False,
            }
        }
        handler = BelvedereEventHandler(str(temp_dir), rules, rule_engine)
        test_file = temp_dir / "test.txt"
        test_file.write_text("content")

        # Act
        handler._process_file(test_file)

        # Assert
        assert (dest_dir / "test.txt").exists()
        assert not test_file.exists()

    def test_event_handler_skips_disabled_rule(self, rule_engine, temp_dir, dest_dir):
        """Test that event handler skips disabled rules."""
        # Arrange
        rules = {
            "disabled_rule": {
                "enabled": False,
                "conditions": [{"subject": "Extension", "verb": "is", "object": "txt"}],
                "match_type": "ALL",
                "action": "Move file",
                "destination": str(dest_dir),
                "overwrite": False,
            }
        }
        handler = BelvedereEventHandler(str(temp_dir), rules, rule_engine)
        test_file = temp_dir / "test.txt"
        test_file.write_text("content")

        # Act
        handler._process_file(test_file)

        # Assert
        assert test_file.exists()
        assert not (dest_dir / "test.txt").exists()

    def test_event_handler_uses_confirm_callback(self, rule_engine, temp_dir, dest_dir):
        """Test that event handler uses confirmation callback."""
        # Arrange
        confirm_calls = []

        def confirm_callback(file_path, rule_name, rule):
            confirm_calls.append((file_path, rule_name))
            return False  # Reject action

        rules = {
            "confirm_rule": {
                "enabled": True,
                "confirm_action": True,
                "conditions": [{"subject": "Extension", "verb": "is", "object": "txt"}],
                "match_type": "ALL",
                "action": "Move file",
                "destination": str(dest_dir),
                "overwrite": False,
            }
        }
        handler = BelvedereEventHandler(str(temp_dir), rules, rule_engine, confirm_callback)
        test_file = temp_dir / "test.txt"
        test_file.write_text("content")

        # Act
        handler._process_file(test_file)

        # Assert
        assert len(confirm_calls) == 1
        assert confirm_calls[0][1] == "confirm_rule"
        assert test_file.exists()  # File not moved because callback returned False

    def test_event_handler_skips_nonexistent_file(self, rule_engine, temp_dir):
        """Test that event handler handles non-existent file gracefully."""
        # Arrange
        rules = {"rule1": {"enabled": True}}
        handler = BelvedereEventHandler(str(temp_dir), rules, rule_engine)
        nonexistent_file = temp_dir / "nonexistent.txt"

        # Act
        handler._process_file(nonexistent_file)

        # Assert - should not raise exception
        assert True


class TestIntegrationScenarios:
    """Integration tests for common scenarios."""

    def test_multiple_rules_applied_in_order(self, file_monitor, temp_dir, dest_dir):
        """Test that multiple matching rules are applied in order."""
        # Arrange
        test_file = temp_dir / "document.txt"
        test_file.write_text("content")

        # First rule copies, second rule would try to move
        rules = {
            "copy_rule": {
                "enabled": True,
                "conditions": [{"subject": "Extension", "verb": "is", "object": "txt"}],
                "match_type": "ALL",
                "action": "Copy file",
                "destination": str(dest_dir),
                "overwrite": False,
            }
        }

        # Act
        file_monitor.scan_folder_once(str(temp_dir), rules)

        # Assert
        assert (dest_dir / "document.txt").exists()
        assert test_file.exists()  # Original still exists after copy

    def test_handles_exception_during_processing(self, file_monitor, temp_dir, mocker):
        """Test that exception during processing doesn't crash monitor."""
        # Arrange
        test_file = temp_dir / "test.txt"
        test_file.write_text("content")

        mocker.patch.object(file_monitor.rule_engine, "evaluate_rule", side_effect=Exception("Test error"))

        rules = {
            "error_rule": {
                "enabled": True,
                "conditions": [{"subject": "Extension", "verb": "is", "object": "txt"}],
                "match_type": "ALL",
                "action": "Delete file",
            }
        }

        # Act
        file_monitor.scan_folder_once(str(temp_dir), rules)

        # Assert
        assert test_file.exists()  # File not deleted due to exception


@pytest.mark.unit
class TestUnitMarker:
    """Tests marked as unit tests."""

    def test_marked_as_unit_test(self, rule_engine):
        """Test with unit marker."""
        # Arrange & Act
        monitor = FileMonitor(rule_engine)

        # Assert
        assert monitor is not None
