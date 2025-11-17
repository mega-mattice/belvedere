"""
File monitoring system using watchdog.

Monitors folders for file changes and triggers rule evaluation.
"""

from pathlib import Path
from typing import Dict, Callable, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from .rule_engine import RuleEngine


class BelvedereEventHandler(FileSystemEventHandler):
    """Handles file system events for Belvedere."""

    def __init__(self, folder_path: str, rules: Dict[str, Any],
                 rule_engine: RuleEngine, confirm_callback: Callable = None):
        """Initialize event handler.

        Args:
            folder_path: Path to the monitored folder.
            rules: Dictionary of rules for this folder.
            rule_engine: RuleEngine instance for evaluating rules.
            confirm_callback: Optional callback for confirming actions.
        """
        super().__init__()
        self.folder_path = Path(folder_path)
        self.rules = rules
        self.rule_engine = rule_engine
        self.confirm_callback = confirm_callback

    def on_created(self, event: FileSystemEvent):
        """Handle file creation events.

        Args:
            event: The file system event.
        """
        if not event.is_directory:
            self._process_file(Path(event.src_path))

    def on_modified(self, event: FileSystemEvent):
        """Handle file modification events.

        Args:
            event: The file system event.
        """
        if not event.is_directory:
            self._process_file(Path(event.src_path))

    def _process_file(self, file_path: Path):
        """Process a file against all rules.

        Args:
            file_path: Path to the file to process.
        """
        if not file_path.exists() or not file_path.is_file():
            return

        for rule_name, rule in self.rules.items():
            if not rule.get('enabled', True):
                continue

            try:
                if self.rule_engine.evaluate_rule(file_path, rule):
                    # Check if confirmation is needed
                    if rule.get('confirm_action', False):
                        if self.confirm_callback:
                            if not self.confirm_callback(file_path, rule_name, rule):
                                continue

                    # Execute the action
                    self.rule_engine.execute_action(file_path, rule)
            except Exception as e:
                print(f"Error processing file {file_path} with rule {rule_name}: {e}")


class FileMonitor:
    """Manages file system monitoring for multiple folders."""

    def __init__(self, rule_engine: RuleEngine, confirm_callback: Callable = None):
        """Initialize the file monitor.

        Args:
            rule_engine: RuleEngine instance for evaluating rules.
            confirm_callback: Optional callback for confirming actions.
        """
        self.rule_engine = rule_engine
        self.confirm_callback = confirm_callback
        self.observer = Observer()
        self.handlers = {}
        self.watches = {}  # Store watch handles
        self.running = False

    def add_folder(self, folder_path: str, rules: Dict[str, Any], recursive: bool = False):
        """Add a folder to monitor.

        Args:
            folder_path: Path to the folder.
            rules: Dictionary of rules for this folder.
            recursive: Whether to monitor subdirectories.
        """
        if folder_path in self.handlers:
            self.remove_folder(folder_path)

        handler = BelvedereEventHandler(
            folder_path, rules, self.rule_engine, self.confirm_callback
        )

        watch = self.observer.schedule(handler, folder_path, recursive=recursive)
        self.handlers[folder_path] = handler
        self.watches[folder_path] = watch

    def remove_folder(self, folder_path: str):
        """Remove a folder from monitoring.

        Args:
            folder_path: Path to the folder.
        """
        if folder_path in self.handlers:
            # Unschedule the watch using the stored watch handle
            if folder_path in self.watches:
                self.observer.unschedule(self.watches[folder_path])
                del self.watches[folder_path]
            del self.handlers[folder_path]

    def update_rules(self, folder_path: str, rules: Dict[str, Any]):
        """Update rules for a folder.

        Args:
            folder_path: Path to the folder.
            rules: New rules dictionary.
        """
        if folder_path in self.handlers:
            self.handlers[folder_path].rules = rules

    def start(self):
        """Start monitoring."""
        if not self.running:
            self.observer.start()
            self.running = True

    def stop(self):
        """Stop monitoring."""
        if self.running:
            self.observer.stop()
            self.observer.join()
            self.running = False

    def scan_folder_once(self, folder_path: str, rules: Dict[str, Any], recursive: bool = False):
        """Scan a folder once and apply rules to existing files.

        This is useful for the periodic scan feature from the original app.

        Args:
            folder_path: Path to the folder.
            rules: Dictionary of rules to apply.
            recursive: Whether to scan subdirectories.
        """
        folder = Path(folder_path)
        if not folder.exists() or not folder.is_dir():
            return

        # Get files to process
        if recursive:
            files = list(folder.rglob('*'))
        else:
            files = list(folder.glob('*'))

        # Filter to only files
        files = [f for f in files if f.is_file()]

        # Process each file
        for file_path in files:
            for rule_name, rule in rules.items():
                if not rule.get('enabled', True):
                    continue

                try:
                    if self.rule_engine.evaluate_rule(file_path, rule):
                        # Check if confirmation is needed
                        if rule.get('confirm_action', False):
                            if self.confirm_callback:
                                if not self.confirm_callback(file_path, rule_name, rule):
                                    continue

                        # Execute the action
                        success = self.rule_engine.execute_action(file_path, rule)
                        if not success:
                            break  # Don't process more rules if action failed
                except Exception as e:
                    print(f"Error processing file {file_path} with rule {rule_name}: {e}")
