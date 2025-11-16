"""
Unit tests for the Config module.

Tests configuration management including folder management,
rule management, preferences, and persistence.
"""

import json
import pytest
from pathlib import Path

from belvedere.config import Config


class TestConfigInitialization:
    """Tests for Config initialization."""
    
    def test_config_with_custom_path_creates_default(self, temp_config_path):
        """Test that Config creates default configuration with custom path."""
        # Arrange & Act
        config = Config(temp_config_path)
        
        # Assert
        assert config.config_path == temp_config_path
        assert config.data is not None
        assert 'folders' in config.data
        assert 'rules' in config.data
        assert 'preferences' in config.data
    
    def test_config_without_path_uses_default_location(self, monkeypatch, temp_dir):
        """Test that Config uses default location when no path provided."""
        # Arrange
        monkeypatch.setattr(Path, 'home', lambda: temp_dir)
        
        # Act
        config = Config()
        
        # Assert
        assert config.config_path is not None
        # Config path should be created in the home directory structure
        assert str(temp_dir) in str(config.config_path)
    
    def test_config_creates_default_structure(self, temp_config_path):
        """Test that default config has expected structure."""
        # Arrange & Act
        config = Config(temp_config_path)
        
        # Assert
        assert config.data['folders'] == []
        assert config.data['rules'] == {}
        assert 'sleep_time' in config.data['preferences']
        assert 'recycle_bin' in config.data['preferences']


class TestFolderManagement:
    """Tests for folder management operations."""
    
    def test_add_folder_succeeds(self, config):
        """Test adding a folder to monitoring."""
        # Arrange
        test_folder = "/tmp/test_folder"
        
        # Act
        config.add_folder(test_folder)
        
        # Assert
        assert test_folder in config.get_folders()
    
    def test_add_duplicate_folder_is_idempotent(self, config):
        """Test that adding same folder twice doesn't create duplicates."""
        # Arrange
        test_folder = "/tmp/test_folder"
        
        # Act
        config.add_folder(test_folder)
        config.add_folder(test_folder)
        
        # Assert
        folders = config.get_folders()
        assert folders.count(test_folder) == 1
    
    def test_remove_folder_succeeds(self, config):
        """Test removing a folder from monitoring."""
        # Arrange
        test_folder = "/tmp/test_folder"
        config.add_folder(test_folder)
        
        # Act
        config.remove_folder(test_folder)
        
        # Assert
        assert test_folder not in config.get_folders()
    
    def test_remove_nonexistent_folder_does_nothing(self, config):
        """Test that removing non-existent folder doesn't cause errors."""
        # Arrange
        test_folder = "/tmp/nonexistent_folder"
        
        # Act
        config.remove_folder(test_folder)
        
        # Assert - should not raise exception
        assert test_folder not in config.get_folders()
    
    def test_remove_folder_removes_associated_rules(self, config):
        """Test that removing folder also removes its rules."""
        # Arrange
        test_folder = "/tmp/test_folder"
        config.add_folder(test_folder)
        rule_data = {
            'folder': test_folder,
            'enabled': True,
            'conditions': []
        }
        config.add_rule('test_rule', rule_data)
        
        # Act
        config.remove_folder(test_folder)
        
        # Assert
        rules = config.get_rules(test_folder)
        assert len(rules) == 0
        assert 'test_rule' not in config.get_rules()
    
    def test_get_folders_returns_empty_list_initially(self, config):
        """Test that get_folders returns empty list for new config."""
        # Arrange & Act
        folders = config.get_folders()
        
        # Assert
        assert folders == []


class TestRuleManagement:
    """Tests for rule management operations."""
    
    def test_add_rule_succeeds(self, config):
        """Test adding a rule to configuration."""
        # Arrange
        rule_name = 'test_rule'
        rule_data = {
            'folder': '/tmp/test',
            'enabled': True,
            'conditions': [{'subject': 'Name', 'verb': 'is', 'object': 'test'}]
        }
        
        # Act
        config.add_rule(rule_name, rule_data)
        
        # Assert
        rules = config.get_rules()
        assert rule_name in rules
        assert rules[rule_name] == rule_data
    
    def test_add_rule_updates_existing_rule(self, config):
        """Test that adding rule with existing name updates it."""
        # Arrange
        rule_name = 'test_rule'
        rule_data_v1 = {'enabled': True, 'folder': '/tmp/test'}
        rule_data_v2 = {'enabled': False, 'folder': '/tmp/test2'}
        
        # Act
        config.add_rule(rule_name, rule_data_v1)
        config.add_rule(rule_name, rule_data_v2)
        
        # Assert
        rules = config.get_rules()
        assert rules[rule_name] == rule_data_v2
    
    def test_remove_rule_succeeds(self, config):
        """Test removing a rule from configuration."""
        # Arrange
        rule_name = 'test_rule'
        rule_data = {'folder': '/tmp/test', 'enabled': True}
        config.add_rule(rule_name, rule_data)
        
        # Act
        config.remove_rule(rule_name)
        
        # Assert
        rules = config.get_rules()
        assert rule_name not in rules
    
    def test_remove_nonexistent_rule_does_nothing(self, config):
        """Test that removing non-existent rule doesn't cause errors."""
        # Arrange
        rule_name = 'nonexistent_rule'
        
        # Act
        config.remove_rule(rule_name)
        
        # Assert - should not raise exception
        assert rule_name not in config.get_rules()
    
    def test_get_rules_without_folder_returns_all(self, config):
        """Test that get_rules without folder parameter returns all rules."""
        # Arrange
        config.add_rule('rule1', {'folder': '/tmp/test1'})
        config.add_rule('rule2', {'folder': '/tmp/test2'})
        
        # Act
        rules = config.get_rules()
        
        # Assert
        assert len(rules) == 2
        assert 'rule1' in rules
        assert 'rule2' in rules
    
    def test_get_rules_with_folder_filters_correctly(self, config):
        """Test that get_rules with folder parameter filters correctly."""
        # Arrange
        folder1 = '/tmp/test1'
        folder2 = '/tmp/test2'
        config.add_rule('rule1', {'folder': folder1})
        config.add_rule('rule2', {'folder': folder2})
        config.add_rule('rule3', {'folder': folder1})
        
        # Act
        rules = config.get_rules(folder1)
        
        # Assert
        assert len(rules) == 2
        assert 'rule1' in rules
        assert 'rule3' in rules
        assert 'rule2' not in rules


class TestPreferences:
    """Tests for preferences management."""
    
    def test_get_preferences_returns_defaults(self, config):
        """Test that get_preferences returns default preferences."""
        # Arrange & Act
        prefs = config.get_preferences()
        
        # Assert
        assert 'sleep_time' in prefs
        assert prefs['sleep_time'] == 5000
        assert 'recycle_bin' in prefs
    
    def test_update_preferences_merges_correctly(self, config):
        """Test that update_preferences merges new values."""
        # Arrange
        new_prefs = {'sleep_time': 10000}
        
        # Act
        config.update_preferences(new_prefs)
        
        # Assert
        prefs = config.get_preferences()
        assert prefs['sleep_time'] == 10000
        assert 'recycle_bin' in prefs  # Old keys preserved
    
    def test_update_preferences_preserves_existing_keys(self, config):
        """Test that updating preferences doesn't remove existing keys."""
        # Arrange
        original_prefs = config.get_preferences()
        new_prefs = {'new_key': 'new_value'}
        
        # Act
        config.update_preferences(new_prefs)
        
        # Assert
        updated_prefs = config.get_preferences()
        assert 'sleep_time' in updated_prefs
        assert 'recycle_bin' in updated_prefs
        assert updated_prefs['new_key'] == 'new_value'


class TestPersistence:
    """Tests for configuration persistence."""
    
    def test_save_creates_file(self, config, temp_config_path):
        """Test that save creates configuration file."""
        # Arrange
        config.add_folder('/tmp/test')
        
        # Act
        config.save()
        
        # Assert
        assert temp_config_path.exists()
    
    def test_save_creates_parent_directories(self, temp_dir):
        """Test that save creates parent directories if needed."""
        # Arrange
        nested_path = temp_dir / 'nested' / 'path' / 'config.json'
        config = Config(nested_path)
        
        # Act
        config.save()
        
        # Assert
        assert nested_path.exists()
        assert nested_path.parent.exists()
    
    def test_saved_config_can_be_loaded(self, temp_config_path):
        """Test that saved configuration can be loaded."""
        # Arrange
        config1 = Config(temp_config_path)
        test_folder = '/tmp/test_folder'
        config1.add_folder(test_folder)
        config1.save()
        
        # Act
        config2 = Config(temp_config_path)
        
        # Assert
        assert test_folder in config2.get_folders()
    
    def test_saved_config_preserves_all_data(self, temp_config_path):
        """Test that all configuration data is preserved on save/load."""
        # Arrange
        config1 = Config(temp_config_path)
        config1.add_folder('/tmp/test')
        config1.add_rule('rule1', {'folder': '/tmp/test', 'enabled': True})
        config1.update_preferences({'sleep_time': 15000})
        config1.save()
        
        # Act
        config2 = Config(temp_config_path)
        
        # Assert
        assert '/tmp/test' in config2.get_folders()
        assert 'rule1' in config2.get_rules()
        assert config2.get_preferences()['sleep_time'] == 15000
    
    def test_load_handles_corrupted_file_gracefully(self, temp_config_path):
        """Test that loading corrupted file creates default config."""
        # Arrange
        temp_config_path.write_text('corrupted json content {{{')
        
        # Act
        config = Config(temp_config_path)
        
        # Assert
        assert config.data is not None
        assert 'folders' in config.data
        assert config.data['folders'] == []
    
    def test_add_folder_auto_saves(self, config, temp_config_path):
        """Test that add_folder automatically saves configuration."""
        # Arrange & Act
        config.add_folder('/tmp/test')
        
        # Assert
        assert temp_config_path.exists()
        with open(temp_config_path) as f:
            data = json.load(f)
        assert '/tmp/test' in data['folders']
    
    def test_add_rule_auto_saves(self, config, temp_config_path):
        """Test that add_rule automatically saves configuration."""
        # Arrange & Act
        config.add_rule('test_rule', {'folder': '/tmp/test'})
        
        # Assert
        assert temp_config_path.exists()
        with open(temp_config_path) as f:
            data = json.load(f)
        assert 'test_rule' in data['rules']
