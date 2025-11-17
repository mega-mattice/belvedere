"""
Tests for RecycleBinManager functionality.
"""

import platform
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from belvedere.config import Config
from belvedere.recycle_bin_manager import RecycleBinEntry, RecycleBinManager


class TestRecycleBinEntry:
    """Test RecycleBinEntry class."""

    def test_init_with_path_only(self, tmp_path):
        """Test initialization with just a path."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        entry = RecycleBinEntry(test_file)

        assert entry.path == test_file
        assert entry.original_path == str(test_file)
        assert entry.size == len("test content")

    def test_init_with_custom_original_path(self, tmp_path):
        """Test initialization with custom original path."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        entry = RecycleBinEntry(test_file, "/original/path.txt")

        assert entry.path == test_file
        assert entry.original_path == "/original/path.txt"


class TestRecycleBinManager:
    """Test RecycleBinManager class."""

    @pytest.fixture
    def config(self, tmp_path):
        """Create a temporary config for testing."""
        config_path = tmp_path / "test_config.json"
        return Config(config_path)

    @pytest.fixture
    def rb_manager(self, config):
        """Create RecycleBinManager instance."""
        return RecycleBinManager(config)

    def test_get_recycle_bin_paths_windows(self, rb_manager):
        """Test getting Windows recycle bin paths."""
        with patch('platform.system', return_value='Windows'):
            paths = rb_manager.get_recycle_bin_paths()
            # Should return paths for all possible drive letters
            assert len(paths) > 0
            assert all(str(p).endswith('$Recycle.Bin') for p in paths)

    def test_get_recycle_bin_paths_macos(self, rb_manager):
        """Test getting macOS recycle bin paths."""
        with patch('platform.system', return_value='Darwin'):
            paths = rb_manager.get_recycle_bin_paths()
            assert len(paths) == 1
            assert paths[0].name == '.Trash'

    def test_get_recycle_bin_paths_linux(self, rb_manager):
        """Test getting Linux recycle bin paths."""
        with patch('platform.system', return_value='Linux'):
            with patch.dict('os.environ', {'XDG_DATA_HOME': '/tmp/test_data'}):
                paths = rb_manager.get_recycle_bin_paths()
                assert any('Trash' in str(p) for p in paths)

    def test_manage_by_age_no_files(self, rb_manager):
        """Test age management when no files meet criteria."""
        with patch.object(rb_manager, 'get_recycle_bin_contents', return_value=[]):
            deleted = rb_manager.manage_by_age(30)
            assert deleted == 0

    def test_manage_by_age_with_old_files(self, rb_manager, tmp_path):
        """Test age management with files older than threshold."""
        # Create mock entries
        old_file = tmp_path / "old.txt"
        old_file.write_text("old")

        old_entry = RecycleBinEntry(
            old_file,
            deletion_date=datetime.now() - timedelta(days=40)
        )

        new_file = tmp_path / "new.txt"
        new_file.write_text("new")

        new_entry = RecycleBinEntry(
            new_file,
            deletion_date=datetime.now() - timedelta(days=10)
        )

        with patch.object(rb_manager, 'get_recycle_bin_contents', return_value=[old_entry, new_entry]):
            with patch('pathlib.Path.unlink') as mock_unlink:
                deleted = rb_manager.manage_by_age(30)

                # Should only delete the old file
                assert deleted == 1
                mock_unlink.assert_called_once_with()

    def test_manage_by_size_no_files(self, rb_manager):
        """Test size management when no files exist."""
        with patch.object(rb_manager, 'get_recycle_bin_contents', return_value=[]):
            deleted = rb_manager.manage_by_size(100)
            assert deleted == 0

    def test_manage_by_size_oldest_first(self, rb_manager, tmp_path):
        """Test size management with oldest first deletion approach."""
        # Create test files
        files = []
        entries = []

        for i in range(5):
            test_file = tmp_path / f"file_{i}.txt"
            test_file.write_text("x" * 100)  # 100 bytes each
            files.append(test_file)

            entry = RecycleBinEntry(
                test_file,
                deletion_date=datetime.now() - timedelta(days=i+1)
            )
            entry.size = 100
            entries.append(entry)

        # Total size = 500 bytes, limit = 200 bytes
        with patch.object(rb_manager, 'get_recycle_bin_contents', return_value=entries):
            with patch('pathlib.Path.unlink') as mock_unlink:
                deleted = rb_manager.manage_by_size(2)  # 2 MB limit

                # Should delete oldest files first (files 4, 3, 2)
                assert deleted == 3
                assert mock_unlink.call_count == 3

    def test_manage_by_size_largest_first(self, rb_manager, tmp_path):
        """Test size management with largest first deletion approach."""
        # Create test files with different sizes
        files = []
        entries = []

        sizes = [50, 200, 100, 300, 150]  # Total = 800 bytes

        for i, size in enumerate(sizes):
            test_file = tmp_path / f"file_{i}.txt"
            test_file.write_text("x" * size)
            files.append(test_file)

            entry = RecycleBinEntry(
                test_file,
                deletion_date=datetime.now() - timedelta(days=1)
            )
            entry.size = size
            entries.append(entry)

        # Sort by size for largest first
        entries.sort(key=lambda x: x.size, reverse=True)

        with patch.object(rb_manager, 'get_recycle_bin_contents', return_value=entries):
            with patch('pathlib.Path.unlink') as mock_unlink:
                deleted = rb_manager.manage_by_size(1)  # 1 MB limit

                # Should delete largest files first
                assert deleted == 3  # Files of 300, 200, 150 bytes
                assert mock_unlink.call_count == 3

    def test_auto_empty(self, rb_manager, tmp_path):
        """Test complete recycle bin emptying."""
        # Create test files
        files = []
        entries = []

        for i in range(3):
            test_file = tmp_path / f"file_{i}.txt"
            test_file.write_text(f"content {i}")
            files.append(test_file)

            entries.append(RecycleBinEntry(test_file))

        with patch.object(rb_manager, 'get_recycle_bin_contents', return_value=entries):
            with patch('pathlib.Path.unlink') as mock_unlink:
                deleted = rb_manager.auto_empty()

                assert deleted == 3
                assert mock_unlink.call_count == 3

    def test_apply_recycle_bin_rules_disabled(self, rb_manager, config):
        """Test applying rules when recycle bin management is disabled."""
        config.update_preferences({"recycle_bin": {"enabled": False}})
        results = rb_manager.apply_recycle_bin_rules()

        assert results == {"disabled": 0}

    def test_apply_recycle_bin_rules_age_management(self, rb_manager, config):
        """Test applying age-based recycle bin rules."""
        config.update_preferences({
            "recycle_bin": {
                "enabled": True,
                "manage_age": True,
                "age_value": 30,
                "age_unit": "days"
            }
        })

        with patch.object(rb_manager, 'manage_by_age', return_value=5) as mock_manage_age:
            results = rb_manager.apply_recycle_bin_rules()

            mock_manage_age.assert_called_once_with(30)
            assert results["age_based"] == 5

    def test_apply_recycle_bin_rules_size_management(self, rb_manager, config):
        """Test applying size-based recycle bin rules."""
        config.update_preferences({
            "recycle_bin": {
                "enabled": True,
                "manage_size": True,
                "size_value": 500,
                "size_unit": "MB",
                "deletion_approach": "Largest First"
            }
        })

        with patch.object(rb_manager, 'manage_by_size', return_value=2) as mock_manage_size:
            results = rb_manager.apply_recycle_bin_rules()

            mock_manage_size.assert_called_once_with(500, "Largest First")
            assert results["size_based"] == 2

    def test_apply_recycle_bin_rules_error_handling(self, rb_manager, config):
        """Test error handling in apply_recycle_bin_rules."""
        config.update_preferences({
            "recycle_bin": {
                "enabled": True,
                "manage_age": True,
                "age_value": 30,
                "age_unit": "days"
            }
        })

        with patch.object(rb_manager, 'manage_by_age', side_effect=Exception("Test error")):
            results = rb_manager.apply_recycle_bin_rules()

            # Should handle error gracefully and return partial results
            assert "age_based" in results

    def test_windows_recycle_bin_parsing(self, rb_manager, tmp_path):
        """Test Windows recycle bin content parsing."""
        rb_manager.system = "Windows"

        # Create mock Windows recycle bin structure
        recycle_bin = tmp_path / "$Recycle.Bin" / "S-1-5-21-1234567890-123456789-123456789-1000"
        recycle_bin.mkdir(parents=True)

        # Create $R and $I files
        r_file = recycle_bin / "$Rtest.txt"
        i_file = recycle_bin / "$Itest.txt"

        r_file.write_text("test content")
        i_file.write_text("mock metadata")

        with patch.object(rb_manager, 'get_recycle_bin_paths', return_value=[recycle_bin.parent]):
            entries = rb_manager.get_recycle_bin_contents()

            assert len(entries) == 1
            assert entries[0].path == r_file

    def test_linux_recycle_bin_parsing(self, rb_manager, tmp_path):
        """Test Linux trash content parsing."""
        rb_manager.system = "Linux"

        # Create mock Linux trash structure
        trash_dir = tmp_path / ".local" / "share" / "Trash"
        files_dir = trash_dir / "files"
        info_dir = trash_dir / "info"
        files_dir.mkdir(parents=True)
        info_dir.mkdir()

        # Create file and .trashinfo
        trash_file = files_dir / "test.txt"
        info_file = info_dir / "test.txt.trashinfo"

        trash_file.write_text("test content")
        info_file.write_text("""[Trash Info]
Path=/home/user/test.txt
DeletionDate=2023-11-17T10:30:45
""")

        with patch.object(rb_manager, 'get_recycle_bin_paths', return_value=[trash_dir]):
            entries = rb_manager.get_recycle_bin_contents()

            assert len(entries) == 1
            assert entries[0].path == trash_file
            assert entries[0].original_path == "/home/user/test.txt"
