"""
Unit tests for the RuleEngine module.

Tests rule evaluation, condition checking, and file action execution.
"""

from pathlib import Path

import pytest


class TestRuleEvaluation:
    """Tests for rule evaluation logic."""

    def test_evaluate_rule_with_nonexistent_file_returns_false(self, rule_engine):
        """Test that evaluating non-existent file returns False."""
        # Arrange
        file_path = Path("/nonexistent/file.txt")
        rule = {"conditions": [{"subject": "Name", "verb": "is", "object": "file"}]}

        # Act
        result = rule_engine.evaluate_rule(file_path, rule)

        # Assert
        assert result is False

    def test_evaluate_rule_with_empty_conditions_returns_false(self, rule_engine, sample_file):
        """Test that rule with no conditions returns False."""
        # Arrange
        rule = {"conditions": []}

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is False

    def test_evaluate_rule_all_match_type_requires_all_true(self, rule_engine, sample_file):
        """Test that ALL match type requires all conditions to be true."""
        # Arrange
        rule = {
            "conditions": [
                {"subject": "Name", "verb": "contains", "object": "test"},
                {"subject": "Extension", "verb": "is", "object": "txt"},
            ],
            "match_type": "ALL",
        }

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is True

    def test_evaluate_rule_all_match_type_fails_if_one_false(self, rule_engine, sample_file):
        """Test that ALL match type fails if any condition is false."""
        # Arrange
        rule = {
            "conditions": [
                {"subject": "Name", "verb": "is", "object": "test_document"},
                {"subject": "Extension", "verb": "is", "object": "pdf"},  # Wrong
            ],
            "match_type": "ALL",
        }

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is False

    def test_evaluate_rule_any_match_type_succeeds_if_one_true(self, rule_engine, sample_file):
        """Test that ANY match type succeeds if any condition is true."""
        # Arrange
        rule = {
            "conditions": [
                {"subject": "Name", "verb": "is", "object": "wrong_name"},
                {"subject": "Extension", "verb": "is", "object": "txt"},  # Correct
            ],
            "match_type": "ANY",
        }

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is True


class TestNameConditions:
    """Tests for name-based conditions."""

    def test_name_is_matches_exactly(self, rule_engine, sample_file):
        """Test that 'is' verb matches exact file name."""
        # Arrange
        rule = {"conditions": [{"subject": "Name", "verb": "is", "object": "test_document"}], "match_type": "ALL"}

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is True

    def test_name_is_case_insensitive(self, rule_engine, sample_file):
        """Test that name matching is case-insensitive."""
        # Arrange
        rule = {"conditions": [{"subject": "Name", "verb": "is", "object": "TEST_DOCUMENT"}], "match_type": "ALL"}

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is True

    def test_name_is_not_rejects_match(self, rule_engine, sample_file):
        """Test that 'is not' verb rejects matching name."""
        # Arrange
        rule = {"conditions": [{"subject": "Name", "verb": "is not", "object": "test_document"}], "match_type": "ALL"}

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is False

    def test_name_contains_matches_substring(self, rule_engine, sample_file):
        """Test that 'contains' verb matches substring."""
        # Arrange
        rule = {"conditions": [{"subject": "Name", "verb": "contains", "object": "document"}], "match_type": "ALL"}

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is True

    def test_name_does_not_contain_rejects_substring(self, rule_engine, sample_file):
        """Test that 'does not contain' verb rejects substring."""
        # Arrange
        rule = {"conditions": [{"subject": "Name", "verb": "does not contain", "object": "document"}], "match_type": "ALL"}

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is False


class TestExtensionConditions:
    """Tests for extension-based conditions."""

    def test_extension_is_matches_correctly(self, rule_engine, sample_file):
        """Test that extension matching works correctly."""
        # Arrange
        rule = {"conditions": [{"subject": "Extension", "verb": "is", "object": "txt"}], "match_type": "ALL"}

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is True

    def test_extension_is_case_insensitive(self, rule_engine, temp_dir):
        """Test that extension matching is case-insensitive."""
        # Arrange
        file_path = temp_dir / "test.TXT"
        file_path.write_text("content")
        rule = {"conditions": [{"subject": "Extension", "verb": "is", "object": "txt"}], "match_type": "ALL"}

        # Act
        result = rule_engine.evaluate_rule(file_path, rule)

        # Assert
        assert result is True

    def test_extension_matches_one_of_succeeds(self, rule_engine, sample_file):
        """Test that 'matches one of' works with comma-separated list."""
        # Arrange
        rule = {
            "conditions": [{"subject": "Extension", "verb": "matches one of", "object": "pdf, txt, doc"}],
            "match_type": "ALL",
        }

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is True


class TestSizeConditions:
    """Tests for size-based conditions."""

    def test_size_is_greater_than_in_bytes(self, rule_engine, temp_dir):
        """Test size comparison in bytes."""
        # Arrange
        file_path = temp_dir / "large_file.txt"
        file_path.write_text("x" * 2000)  # 2000 bytes
        rule = {
            "conditions": [{"subject": "Size", "verb": "is greater than", "object": "1000", "units": "bytes"}],
            "match_type": "ALL",
        }

        # Act
        result = rule_engine.evaluate_rule(file_path, rule)

        # Assert
        assert result is True

    def test_size_is_greater_than_in_kb(self, rule_engine, temp_dir):
        """Test size comparison in kilobytes."""
        # Arrange
        file_path = temp_dir / "large_file.txt"
        file_path.write_text("x" * 2048)  # 2 KB
        rule = {
            "conditions": [{"subject": "Size", "verb": "is greater than", "object": "1", "units": "KB"}],
            "match_type": "ALL",
        }

        # Act
        result = rule_engine.evaluate_rule(file_path, rule)

        # Assert
        assert result is True

    def test_size_is_less_than_succeeds(self, rule_engine, sample_file):
        """Test 'is less than' size comparison."""
        # Arrange
        rule = {"conditions": [{"subject": "Size", "verb": "is less than", "object": "1", "units": "MB"}], "match_type": "ALL"}

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is True


class TestDateConditions:
    """Tests for date-based conditions."""

    def test_date_modified_is_in_the_last_days(self, rule_engine, sample_file):
        """Test 'is in the last' for recent file modification."""
        # Arrange
        rule = {
            "conditions": [{"subject": "Date last modified", "verb": "is in the last", "object": "1", "units": "days"}],
            "match_type": "ALL",
        }

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is True

    def test_date_modified_is_in_the_last_minutes(self, rule_engine, sample_file):
        """Test 'is in the last' with minutes unit."""
        # Arrange
        rule = {
            "conditions": [{"subject": "Date last modified", "verb": "is in the last", "object": "60", "units": "minutes"}],
            "match_type": "ALL",
        }

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is True

    def test_date_modified_is_not_in_the_last_fails(self, rule_engine, sample_file):
        """Test 'is not in the last' for recent file."""
        # Arrange
        rule = {
            "conditions": [{"subject": "Date last modified", "verb": "is not in the last", "object": "1", "units": "minutes"}],
            "match_type": "ALL",
        }

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result is False


class TestFileActions:
    """Tests for file action execution."""

    def test_move_file_succeeds(self, rule_engine, sample_file, dest_dir):
        """Test moving a file to destination directory."""
        # Arrange
        rule = {"action": "Move file", "destination": str(dest_dir), "overwrite": False}

        # Act
        result = rule_engine.execute_action(sample_file, rule)

        # Assert
        assert result is True
        assert (dest_dir / sample_file.name).exists()
        assert not sample_file.exists()

    def test_move_file_fails_if_destination_not_exists(self, rule_engine, sample_file):
        """Test that move fails if destination doesn't exist."""
        # Arrange
        rule = {"action": "Move file", "destination": "/nonexistent/directory", "overwrite": False}

        # Act
        result = rule_engine.execute_action(sample_file, rule)

        # Assert
        assert result is False
        assert sample_file.exists()

    def test_move_file_respects_overwrite_flag(self, rule_engine, temp_dir, dest_dir):
        """Test that move respects overwrite flag when file exists."""
        # Arrange
        src_file = temp_dir / "source.txt"
        src_file.write_text("source content")
        existing_file = dest_dir / "source.txt"
        existing_file.write_text("existing content")

        rule = {"action": "Move file", "destination": str(dest_dir), "overwrite": False}

        # Act
        result = rule_engine.execute_action(src_file, rule)

        # Assert
        assert result is False
        assert src_file.exists()
        assert existing_file.read_text() == "existing content"

    def test_copy_file_succeeds(self, rule_engine, sample_file, dest_dir):
        """Test copying a file to destination directory."""
        # Arrange
        rule = {"action": "Copy file", "destination": str(dest_dir), "overwrite": False}

        # Act
        result = rule_engine.execute_action(sample_file, rule)

        # Assert
        assert result is True
        assert (dest_dir / sample_file.name).exists()
        assert sample_file.exists()  # Original still exists

    def test_copy_file_preserves_content(self, rule_engine, temp_dir, dest_dir):
        """Test that copy preserves file content."""
        # Arrange
        src_file = temp_dir / "source.txt"
        content = "test content for copy"
        src_file.write_text(content)
        rule = {"action": "Copy file", "destination": str(dest_dir), "overwrite": False}

        # Act
        result = rule_engine.execute_action(src_file, rule)

        # Assert
        assert result is True
        copied_file = dest_dir / src_file.name
        assert copied_file.read_text() == content

    def test_rename_file_succeeds(self, rule_engine, sample_file):
        """Test renaming a file."""
        # Arrange
        new_name = "renamed_file.txt"
        rule = {"action": "Rename file", "destination": new_name, "overwrite": False}

        # Act
        result = rule_engine.execute_action(sample_file, rule)

        # Assert
        assert result is True
        assert (sample_file.parent / new_name).exists()
        assert not sample_file.exists()

    def test_rename_file_respects_overwrite_flag(self, rule_engine, temp_dir):
        """Test that rename respects overwrite flag."""
        # Arrange
        src_file = temp_dir / "source.txt"
        src_file.write_text("source")
        existing_file = temp_dir / "existing.txt"
        existing_file.write_text("existing")

        rule = {"action": "Rename file", "destination": "existing.txt", "overwrite": False}

        # Act
        result = rule_engine.execute_action(src_file, rule)

        # Assert
        assert result is False
        assert src_file.exists()

    def test_delete_file_succeeds(self, rule_engine, sample_file):
        """Test deleting a file permanently."""
        # Arrange
        rule = {"action": "Delete file"}

        # Act
        result = rule_engine.execute_action(sample_file, rule)

        # Assert
        assert result is True
        assert not sample_file.exists()

    def test_recycle_file_succeeds(self, rule_engine, sample_file, mocker):
        """Test sending a file to recycle bin."""
        # Arrange
        mock_send2trash = mocker.patch("belvedere.rule_engine.send2trash.send2trash")
        rule = {"action": "Send file to Recycle Bin"}

        # Act
        result = rule_engine.execute_action(sample_file, rule)

        # Assert
        assert result is True
        mock_send2trash.assert_called_once_with(str(sample_file))

    def test_unknown_action_returns_false(self, rule_engine, sample_file):
        """Test that unknown action returns False."""
        # Arrange
        rule = {"action": "Unknown Action"}

        # Act
        result = rule_engine.execute_action(sample_file, rule)

        # Assert
        assert result is False


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_evaluate_rule_with_directory_returns_false(self, rule_engine, temp_dir):
        """Test that evaluating a directory returns False."""
        # Arrange
        rule = {"conditions": [{"subject": "Name", "verb": "is", "object": "test"}], "match_type": "ALL"}

        # Act
        result = rule_engine.evaluate_rule(temp_dir, rule)

        # Assert
        assert result is False

    def test_action_handles_exception_gracefully(self, rule_engine, sample_file, mocker):
        """Test that action execution handles exceptions gracefully."""
        # Arrange
        mocker.patch("shutil.copy2", side_effect=Exception("Test error"))
        rule = {"action": "Copy file", "destination": "/tmp", "overwrite": False}

        # Act
        result = rule_engine.execute_action(sample_file, rule)

        # Assert
        assert result is False

    @pytest.mark.parametrize(
        "subject,verb,obj,expected",
        [
            ("Name", "is", "test_document", True),
            ("Name", "is", "wrong_name", False),
            ("Extension", "is", "txt", True),
            ("Extension", "is", "pdf", False),
        ],
        ids=["name_match", "name_mismatch", "ext_match", "ext_mismatch"],
    )
    def test_various_condition_combinations(self, rule_engine, sample_file, subject, verb, obj, expected):
        """Test various combinations of conditions using parametrize."""
        # Arrange
        rule = {"conditions": [{"subject": subject, "verb": verb, "object": obj}], "match_type": "ALL"}

        # Act
        result = rule_engine.evaluate_rule(sample_file, rule)

        # Assert
        assert result == expected
