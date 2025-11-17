"""
Main application entry point for Belvedere.

Provides system tray icon and manages the application lifecycle.
"""

import sys
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QMessageBox, QSystemTrayIcon

from .config import Config
from .file_monitor import FileMonitor
from .main_window import MainWindow
from .recycle_bin_manager import RecycleBinManager
from .rule_engine import RuleEngine


class BelvedereApp:
    """Main Belvedere application."""

    def __init__(self):
        """Initialize the application."""
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.config = Config()
        self.rule_engine = RuleEngine()
        self.recycle_bin_manager = RecycleBinManager(self.config)
        self.file_monitor = FileMonitor(self.rule_engine, self.confirm_action)

        self.main_window = None
        self.setup_tray_icon()
        self.setup_timer()
        self.setup_auto_empty_timer()
        self.start_monitoring()

    def setup_tray_icon(self):
        """Setup system tray icon and menu."""
        # Try to load icon from resources, fallback to default
        icon_path = Path(__file__).parent.parent / "resources" / "belvedere.ico"
        if icon_path.exists():
            icon = QIcon(str(icon_path))
        else:
            icon = QIcon.fromTheme("application-x-executable")

        self.tray_icon = QSystemTrayIcon(icon, self.app)
        self.tray_icon.setToolTip("Belvedere 0.6")

        # Create menu
        menu = QMenu()

        manage_action = QAction("&Manage", menu)
        manage_action.triggered.connect(self.show_main_window)
        menu.addAction(manage_action)
        menu.setDefaultAction(manage_action)

        menu.addSeparator()

        about_action = QAction("&About...", menu)
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)

        exit_action = QAction("E&xit", menu)
        exit_action.triggered.connect(self.exit_app)
        menu.addAction(exit_action)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()

    def setup_timer(self):
        """Setup periodic scanning timer."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.periodic_scan)

        # Get sleep time from preferences
        prefs = self.config.get_preferences()
        sleep_time = prefs.get("sleep_time", 5000)
        self.timer.start(sleep_time)

    def setup_auto_empty_timer(self):
        """Setup timer for automatic recycle bin emptying."""
        self.auto_empty_timer = QTimer()
        self.auto_empty_timer.timeout.connect(self.auto_empty_recycle_bin)

        # Check if auto-empty is enabled and setup timer accordingly
        self.update_auto_empty_timer()

    def start_monitoring(self):
        """Start file system monitoring."""
        folders = self.config.get_folders()
        for folder in folders:
            rules = self.config.get_rules(folder)
            if rules:
                # Check if any rule uses recursive
                recursive = any(r.get("recursive", False) for r in rules.values())
                self.file_monitor.add_folder(folder, rules, recursive)

        self.file_monitor.start()

    def periodic_scan(self):
        """Perform periodic scan of monitored folders and recycle bin management."""
        # File monitoring
        folders = self.config.get_folders()
        for folder in folders:
            rules = self.config.get_rules(folder)
            if rules:
                recursive = any(r.get("recursive", False) for r in rules.values())
                self.file_monitor.scan_folder_once(folder, rules, recursive)

        # Recycle bin management
        try:
            results = self.recycle_bin_manager.apply_recycle_bin_rules()
            if any(count > 0 for count in results.values()):
                print(f"Recycle bin management: {results}")
        except Exception as e:
            print(f"Error during recycle bin management: {e}")

    def update_monitoring(self):
        """Update file monitoring based on current configuration."""
        # Restart monitoring with updated rules
        self.file_monitor.stop()

        # Clear existing handlers
        self.file_monitor.handlers.clear()

        # Re-add folders
        self.start_monitoring()

        # Update timer interval
        prefs = self.config.get_preferences()
        sleep_time = prefs.get("sleep_time", 5000)
        self.timer.setInterval(sleep_time)

        # Update auto-empty timer
        self.update_auto_empty_timer()

    def confirm_action(self, file_path: Path, rule_name: str, rule: dict) -> bool:
        """Confirm an action with the user.

        Args:
            file_path: Path to the file.
            rule_name: Name of the rule.
            rule: Rule dictionary.

        Returns:
            True if user confirms, False otherwise.
        """
        action = rule.get("action", "unknown action")
        reply = QMessageBox.question(
            None,
            "Action Confirmation",
            f"Are you sure you want to {action} {file_path.name} because of rule {rule_name}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        return reply == QMessageBox.Yes

    def tray_icon_activated(self, reason):
        """Handle tray icon activation.

        Args:
            reason: Activation reason.
        """
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_main_window()

    def show_main_window(self):
        """Show the main management window."""
        if self.main_window is None:
            self.main_window = MainWindow(self.config)
            self.main_window.rules_changed.connect(self.update_monitoring)

        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()

    def show_about(self):
        """Show about dialog."""
        about_text = """<h2>Belvedere 0.6</h2>
        <p>Belvedere is an automated file management application that performs
        actions on files based on user-defined criteria.</p>
        <p>For example, if a file in your downloads folder hasn't been opened
        in 4 weeks and it's larger than 10MB, you can tell Belvedere to
        automatically send it to the Recycle Bin.</p>
        <p>Belvedere is written by Adam Pash and distributed under the
        GNU Public License.</p>
        <p>Python version converted for cross-platform compatibility.</p>
        """

        QMessageBox.about(None, "About Belvedere", about_text)

    def update_auto_empty_timer(self):
        """Update the auto-empty timer based on current preferences."""
        prefs = self.config.get_preferences()
        rb_prefs = prefs.get("recycle_bin", {})

        # Stop existing timer
        self.auto_empty_timer.stop()

        # Check if auto-empty is enabled
        if rb_prefs.get("enabled", False) and rb_prefs.get("auto_empty", False):
            empty_value = rb_prefs.get("empty_value", 0)
            empty_unit = rb_prefs.get("empty_unit", "days")

            # Calculate interval in milliseconds
            if empty_unit == "minutes":
                interval_ms = empty_value * 60 * 1000
            elif empty_unit == "hours":
                interval_ms = empty_value * 60 * 60 * 1000
            elif empty_unit == "weeks":
                interval_ms = empty_value * 7 * 24 * 60 * 60 * 1000
            else:  # days
                interval_ms = empty_value * 24 * 60 * 60 * 1000

            if interval_ms > 0:
                self.auto_empty_timer.start(interval_ms)

    def auto_empty_recycle_bin(self):
        """Perform automatic recycle bin emptying."""
        try:
            deleted_count = self.recycle_bin_manager.auto_empty()
            if deleted_count > 0:
                print(f"Auto-emptied recycle bin: {deleted_count} files deleted")
        except Exception as e:
            print(f"Error during auto-empty: {e}")

    def exit_app(self):
        """Exit the application."""
        self.file_monitor.stop()
        self.auto_empty_timer.stop()
        self.tray_icon.hide()
        QApplication.quit()

    def run(self):
        """Run the application."""
        return self.app.exec()


def main():
    """Main entry point."""
    app = BelvedereApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
