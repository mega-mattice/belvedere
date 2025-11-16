"""
Shared fixtures for Belvedere tests.

This module contains pytest fixtures that are available across all test files.
"""

import tempfile
import pytest
from pathlib import Path
from datetime import datetime

from belvedere.config import Config
from belvedere.rule_engine import RuleEngine
from belvedere.file_monitor import FileMonitor


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files.
    
    Returns:
        Path: Path to temporary directory.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_config_path(temp_dir):
    """Create a temporary config file path.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Returns:
        Path: Path to temporary config file.
    """
    return temp_dir / 'test_rules.json'


@pytest.fixture
def config(temp_config_path):
    """Create a Config instance with temporary storage.
    
    Args:
        temp_config_path: Temporary config file path fixture.
        
    Returns:
        Config: Config instance.
    """
    return Config(temp_config_path)


@pytest.fixture
def rule_engine():
    """Create a RuleEngine instance.
    
    Returns:
        RuleEngine: RuleEngine instance.
    """
    return RuleEngine()


@pytest.fixture
def file_monitor(rule_engine):
    """Create a FileMonitor instance.
    
    Args:
        rule_engine: RuleEngine fixture.
        
    Returns:
        FileMonitor: FileMonitor instance.
    """
    monitor = FileMonitor(rule_engine)
    yield monitor
    # Cleanup
    if monitor.running:
        monitor.stop()


@pytest.fixture
def sample_file(temp_dir):
    """Create a sample test file.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Returns:
        Path: Path to sample file.
    """
    file_path = temp_dir / 'test_document.txt'
    file_path.write_text('test content')
    return file_path


@pytest.fixture
def sample_rule():
    """Create a sample rule for testing.
    
    Returns:
        dict: Sample rule configuration.
    """
    return {
        'folder': '/tmp/test_folder',
        'enabled': True,
        'conditions': [
            {'subject': 'Name', 'verb': 'is', 'object': 'test_document'}
        ],
        'match_type': 'ALL',
        'action': 'Move file',
        'destination': '/tmp/dest',
        'overwrite': False
    }


@pytest.fixture
def dest_dir(temp_dir):
    """Create a destination directory for file operations.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Returns:
        Path: Path to destination directory.
    """
    dest = temp_dir / 'dest'
    dest.mkdir()
    return dest
