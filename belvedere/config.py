"""
Configuration management for Belvedere.

Handles loading and saving of rules, preferences, and folder configurations.
Uses JSON format instead of INI for better cross-platform compatibility.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class Config:
    """Manages Belvedere configuration."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file. If None, uses default location.
        """
        if config_path is None:
            # Use platform-appropriate config directory
            if Path.home().joinpath('.config').exists():
                config_dir = Path.home() / '.config' / 'belvedere'
            else:
                config_dir = Path.home() / '.belvedere'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_path = config_dir / 'rules.json'
        
        self.config_path = Path(config_path)
        self.data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file.
        
        Returns:
            Configuration dictionary.
        """
        if not self.config_path.exists():
            return self._create_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration.
        
        Returns:
            Default configuration dictionary.
        """
        return {
            'folders': [],
            'rules': {},
            'preferences': {
                'sleep_time': 5000,  # milliseconds
                'recycle_bin': {
                    'enabled': False,
                    'manage_age': False,
                    'age_value': 0,
                    'age_unit': 'days',
                    'manage_size': False,
                    'size_value': 0,
                    'size_unit': 'MB',
                    'deletion_approach': 'Oldest First',
                    'auto_empty': False,
                    'empty_value': 0,
                    'empty_unit': 'days'
                }
            }
        }
    
    def save(self):
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)
    
    def get_folders(self) -> List[str]:
        """Get list of monitored folders.
        
        Returns:
            List of folder paths.
        """
        return self.data.get('folders', [])
    
    def add_folder(self, folder_path: str):
        """Add a folder to monitor.
        
        Args:
            folder_path: Path to the folder.
        """
        folders = self.data.get('folders', [])
        if folder_path not in folders:
            folders.append(folder_path)
            self.data['folders'] = folders
            self.save()
    
    def remove_folder(self, folder_path: str):
        """Remove a folder from monitoring.
        
        Args:
            folder_path: Path to the folder.
        """
        folders = self.data.get('folders', [])
        if folder_path in folders:
            folders.remove(folder_path)
            self.data['folders'] = folders
            # Remove associated rules
            self._remove_folder_rules(folder_path)
            self.save()
    
    def _remove_folder_rules(self, folder_path: str):
        """Remove all rules associated with a folder.
        
        Args:
            folder_path: Path to the folder.
        """
        rules_to_remove = []
        for rule_name, rule_data in self.data.get('rules', {}).items():
            if rule_data.get('folder') == folder_path:
                rules_to_remove.append(rule_name)
        
        for rule_name in rules_to_remove:
            del self.data['rules'][rule_name]
    
    def get_rules(self, folder_path: Optional[str] = None) -> Dict[str, Any]:
        """Get rules, optionally filtered by folder.
        
        Args:
            folder_path: If provided, only return rules for this folder.
            
        Returns:
            Dictionary of rules.
        """
        all_rules = self.data.get('rules', {})
        if folder_path is None:
            return all_rules
        
        return {
            name: rule for name, rule in all_rules.items()
            if rule.get('folder') == folder_path
        }
    
    def add_rule(self, rule_name: str, rule_data: Dict[str, Any]):
        """Add or update a rule.
        
        Args:
            rule_name: Name of the rule.
            rule_data: Rule configuration.
        """
        if 'rules' not in self.data:
            self.data['rules'] = {}
        self.data['rules'][rule_name] = rule_data
        self.save()
    
    def remove_rule(self, rule_name: str):
        """Remove a rule.
        
        Args:
            rule_name: Name of the rule to remove.
        """
        if rule_name in self.data.get('rules', {}):
            del self.data['rules'][rule_name]
            self.save()
    
    def get_preferences(self) -> Dict[str, Any]:
        """Get preferences.
        
        Returns:
            Preferences dictionary.
        """
        return self.data.get('preferences', {})
    
    def update_preferences(self, preferences: Dict[str, Any]):
        """Update preferences.
        
        Args:
            preferences: New preferences to merge.
        """
        current_prefs = self.data.get('preferences', {})
        current_prefs.update(preferences)
        self.data['preferences'] = current_prefs
        self.save()
