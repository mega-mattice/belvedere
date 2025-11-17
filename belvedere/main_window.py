"""
Main GUI window for Belvedere.

Provides the tabbed interface for managing folders, rules, and preferences.
"""

from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLabel, QMessageBox, QFileDialog,
    QListWidgetItem, QCheckBox, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt, Signal

from .config import Config
from .rule_dialog import RuleDialog


class MainWindow(QMainWindow):
    """Main application window."""

    rules_changed = Signal()

    def __init__(self, config: Config):
        """Initialize the main window.

        Args:
            config: Configuration manager instance.
        """
        super().__init__()
        self.config = config
        self.current_folder = None
        self.init_ui()
        self.load_data()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Belvedere Rules")
        self.setGeometry(100, 100, 724, 443)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Create tabs
        self.create_folders_tab()
        self.create_recycle_bin_tab()
        self.create_preferences_tab()

    def create_folders_tab(self):
        """Create the folders and rules management tab."""
        tab = QWidget()
        layout = QHBoxLayout(tab)

        # Left side - Folders
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Folders"))

        self.folders_list = QListWidget()
        self.folders_list.currentItemChanged.connect(self.on_folder_selected)
        left_layout.addWidget(self.folders_list)

        # Folder buttons
        folder_buttons = QHBoxLayout()
        self.add_folder_btn = QPushButton("+")
        self.add_folder_btn.setFixedSize(30, 30)
        self.add_folder_btn.clicked.connect(self.add_folder)
        folder_buttons.addWidget(self.add_folder_btn)

        self.remove_folder_btn = QPushButton("-")
        self.remove_folder_btn.setFixedSize(30, 30)
        self.remove_folder_btn.clicked.connect(self.remove_folder)
        folder_buttons.addWidget(self.remove_folder_btn)

        folder_buttons.addStretch()
        left_layout.addLayout(folder_buttons)

        # Right side - Rules
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Rules"))

        self.rules_list = QListWidget()
        self.rules_list.currentItemChanged.connect(self.on_rule_selected)
        right_layout.addWidget(self.rules_list)

        # Rule buttons
        rule_buttons = QHBoxLayout()
        self.add_rule_btn = QPushButton("+")
        self.add_rule_btn.setFixedSize(30, 30)
        self.add_rule_btn.clicked.connect(self.add_rule)
        rule_buttons.addWidget(self.add_rule_btn)

        self.remove_rule_btn = QPushButton("-")
        self.remove_rule_btn.setFixedSize(30, 30)
        self.remove_rule_btn.clicked.connect(self.remove_rule)
        rule_buttons.addWidget(self.remove_rule_btn)

        self.edit_rule_btn = QPushButton("Edit Rule")
        self.edit_rule_btn.clicked.connect(self.edit_rule)
        rule_buttons.addWidget(self.edit_rule_btn)

        rule_buttons.addStretch()

        self.enable_btn = QPushButton("Enable")
        self.enable_btn.clicked.connect(self.toggle_rule)
        rule_buttons.addWidget(self.enable_btn)

        right_layout.addLayout(rule_buttons)

        # Add layouts to tab
        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 2)

        self.tabs.addTab(tab, "Folders")

    def create_recycle_bin_tab(self):
        """Create the recycle bin management tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Enable checkbox
        self.rb_enable = QCheckBox("Allow Belvedere to manage my Recycle Bin")
        self.rb_enable.stateChanged.connect(self.toggle_recycle_bin_options)
        layout.addWidget(self.rb_enable)

        # Manage age
        self.rb_manage_age = QCheckBox("Remove files in my Recycle Bin older than")
        layout.addWidget(self.rb_manage_age)

        age_layout = QHBoxLayout()
        age_layout.addSpacing(40)
        self.rb_age_value = QLineEdit()
        self.rb_age_value.setMaximumWidth(70)
        age_layout.addWidget(self.rb_age_value)

        self.rb_age_unit = QComboBox()
        self.rb_age_unit.addItems(['minutes', 'hours', 'days', 'weeks'])
        self.rb_age_unit.setCurrentText('days')
        age_layout.addWidget(self.rb_age_unit)
        age_layout.addStretch()
        layout.addLayout(age_layout)

        # Manage size
        self.rb_manage_size = QCheckBox("Keep my Recycle Bin under")
        layout.addWidget(self.rb_manage_size)

        size_layout = QHBoxLayout()
        size_layout.addSpacing(40)
        self.rb_size_value = QLineEdit()
        self.rb_size_value.setMaximumWidth(70)
        size_layout.addWidget(self.rb_size_value)

        self.rb_size_unit = QComboBox()
        self.rb_size_unit.addItems(['MB', 'KB'])
        size_layout.addWidget(self.rb_size_unit)
        size_layout.addStretch()
        layout.addLayout(size_layout)

        # Deletion approach
        approach_layout = QHBoxLayout()
        approach_layout.addSpacing(40)
        approach_layout.addWidget(QLabel("Deletion Approach:"))

        self.rb_deletion_approach = QComboBox()
        self.rb_deletion_approach.addItems([
            'Oldest First', 'Youngest First',
            'Largest First', 'Smallest First'
        ])
        approach_layout.addWidget(self.rb_deletion_approach)
        approach_layout.addStretch()
        layout.addLayout(approach_layout)

        # Auto empty
        self.rb_auto_empty = QCheckBox("Empty my Recycle Bin every")
        layout.addWidget(self.rb_auto_empty)

        empty_layout = QHBoxLayout()
        empty_layout.addSpacing(40)
        self.rb_empty_value = QLineEdit()
        self.rb_empty_value.setMaximumWidth(70)
        empty_layout.addWidget(self.rb_empty_value)

        self.rb_empty_unit = QComboBox()
        self.rb_empty_unit.addItems(['minutes', 'hours', 'days', 'weeks'])
        self.rb_empty_unit.setCurrentText('days')
        empty_layout.addWidget(self.rb_empty_unit)
        empty_layout.addStretch()
        layout.addLayout(empty_layout)

        layout.addStretch()

        # Save button
        save_btn = QPushButton("Save Preferences")
        save_btn.clicked.connect(self.save_recycle_bin_prefs)
        layout.addWidget(save_btn)

        self.tabs.addTab(tab, "Recycle Bin")

        # Store widgets for enable/disable
        self.rb_widgets = [
            self.rb_manage_age, self.rb_age_value, self.rb_age_unit,
            self.rb_manage_size, self.rb_size_value, self.rb_size_unit,
            self.rb_deletion_approach, self.rb_auto_empty,
            self.rb_empty_value, self.rb_empty_unit
        ]

    def create_preferences_tab(self):
        """Create the preferences tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Sleep time
        sleep_layout = QHBoxLayout()
        sleep_layout.addWidget(QLabel("Sleeptime:"))

        self.sleep_time_input = QLineEdit()
        self.sleep_time_input.setMaximumWidth(100)
        sleep_layout.addWidget(self.sleep_time_input)

        sleep_layout.addWidget(QLabel("(Time in milliseconds)"))
        sleep_layout.addStretch()
        layout.addLayout(sleep_layout)

        layout.addStretch()

        # Save button
        save_btn = QPushButton("Save Preferences")
        save_btn.clicked.connect(self.save_preferences)
        layout.addWidget(save_btn)

        self.tabs.addTab(tab, "Preferences")

    def load_data(self):
        """Load data from configuration."""
        # Load folders
        folders = self.config.get_folders()
        self.folders_list.clear()
        for folder in folders:
            item = QListWidgetItem(Path(folder).name)
            item.setData(Qt.UserRole, folder)
            self.folders_list.addItem(item)

        # Load preferences
        prefs = self.config.get_preferences()
        self.sleep_time_input.setText(str(prefs.get('sleep_time', 5000)))

        # Load recycle bin preferences
        rb_prefs = prefs.get('recycle_bin', {})
        self.rb_enable.setChecked(rb_prefs.get('enabled', False))
        self.rb_manage_age.setChecked(rb_prefs.get('manage_age', False))
        self.rb_age_value.setText(str(rb_prefs.get('age_value', '')))
        self.rb_age_unit.setCurrentText(rb_prefs.get('age_unit', 'days'))
        self.rb_manage_size.setChecked(rb_prefs.get('manage_size', False))
        self.rb_size_value.setText(str(rb_prefs.get('size_value', '')))
        self.rb_size_unit.setCurrentText(rb_prefs.get('size_unit', 'MB'))
        self.rb_deletion_approach.setCurrentText(rb_prefs.get('deletion_approach', 'Oldest First'))
        self.rb_auto_empty.setChecked(rb_prefs.get('auto_empty', False))
        self.rb_empty_value.setText(str(rb_prefs.get('empty_value', '')))
        self.rb_empty_unit.setCurrentText(rb_prefs.get('empty_unit', 'days'))

        self.toggle_recycle_bin_options()

    def on_folder_selected(self, current, previous):
        """Handle folder selection.

        Args:
            current: Currently selected item.
            previous: Previously selected item.
        """
        self.rules_list.clear()

        if current is None:
            self.current_folder = None
            return

        folder_path = current.data(Qt.UserRole)
        self.current_folder = folder_path

        # Load rules for this folder
        rules = self.config.get_rules(folder_path)
        for rule_name, rule_data in rules.items():
            enabled = rule_data.get('enabled', True)
            item = QListWidgetItem(f"{'Yes' if enabled else 'No'} - {rule_name}")
            item.setData(Qt.UserRole, rule_name)
            self.rules_list.addItem(item)

    def on_rule_selected(self, current, previous):
        """Handle rule selection.

        Args:
            current: Currently selected item.
            previous: Previously selected item.
        """
        if current is None:
            self.enable_btn.setText("Enable")
            return

        rule_name = current.data(Qt.UserRole)
        rules = self.config.get_rules(self.current_folder)
        rule = rules.get(rule_name, {})

        enabled = rule.get('enabled', True)
        self.enable_btn.setText("Disable" if enabled else "Enable")

    def add_folder(self):
        """Add a new folder to monitor."""
        folder = QFileDialog.getExistingDirectory(
            self, "Select Folder to Monitor"
        )

        if folder:
            self.config.add_folder(folder)
            item = QListWidgetItem(Path(folder).name)
            item.setData(Qt.UserRole, folder)
            self.folders_list.addItem(item)
            self.rules_changed.emit()

    def remove_folder(self):
        """Remove a folder from monitoring."""
        current = self.folders_list.currentItem()
        if current is None:
            QMessageBox.warning(
                self, "No Selection",
                "Please select a folder to remove."
            )
            return

        folder_path = current.data(Qt.UserRole)
        reply = QMessageBox.question(
            self, "Delete Folder",
            f"Are you sure you want to delete the folder '{Path(folder_path).name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.config.remove_folder(folder_path)
            row = self.folders_list.row(current)
            self.folders_list.takeItem(row)
            self.rules_list.clear()
            self.rules_changed.emit()

    def add_rule(self):
        """Add a new rule."""
        if self.current_folder is None:
            QMessageBox.warning(
                self, "No Folder Selected",
                "You must select a folder to create a rule."
            )
            return

        dialog = RuleDialog(self.current_folder, None, self)
        if dialog.exec():
            rule_name, rule_data = dialog.get_rule()
            self.config.add_rule(rule_name, rule_data)
            self.on_folder_selected(self.folders_list.currentItem(), None)
            self.rules_changed.emit()

    def edit_rule(self):
        """Edit an existing rule."""
        current = self.rules_list.currentItem()
        if current is None:
            QMessageBox.warning(
                self, "No Selection",
                "Please select a rule to edit."
            )
            return

        rule_name = current.data(Qt.UserRole)
        rules = self.config.get_rules(self.current_folder)
        rule_data = rules.get(rule_name)

        dialog = RuleDialog(self.current_folder, (rule_name, rule_data), self)
        if dialog.exec():
            new_rule_name, new_rule_data = dialog.get_rule()
            if new_rule_name != rule_name:
                self.config.remove_rule(rule_name)
            self.config.add_rule(new_rule_name, new_rule_data)
            self.on_folder_selected(self.folders_list.currentItem(), None)
            self.rules_changed.emit()

    def remove_rule(self):
        """Remove a rule."""
        current = self.rules_list.currentItem()
        if current is None:
            QMessageBox.warning(
                self, "No Selection",
                "Please select a rule to delete."
            )
            return

        rule_name = current.data(Qt.UserRole)
        reply = QMessageBox.question(
            self, "Delete Rule",
            f"Are you sure you want to delete the rule '{rule_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.config.remove_rule(rule_name)
            row = self.rules_list.row(current)
            self.rules_list.takeItem(row)
            self.rules_changed.emit()

    def toggle_rule(self):
        """Toggle rule enabled/disabled state."""
        current = self.rules_list.currentItem()
        if current is None:
            QMessageBox.warning(
                self, "No Selection",
                "Please select a rule to enable/disable."
            )
            return

        rule_name = current.data(Qt.UserRole)
        rules = self.config.get_rules(self.current_folder)
        rule = rules.get(rule_name, {})

        enabled = rule.get('enabled', True)
        rule['enabled'] = not enabled
        self.config.add_rule(rule_name, rule)

        self.on_folder_selected(self.folders_list.currentItem(), None)
        self.rules_changed.emit()

    def toggle_recycle_bin_options(self):
        """Enable/disable recycle bin options based on checkbox."""
        enabled = self.rb_enable.isChecked()
        for widget in self.rb_widgets:
            widget.setEnabled(enabled)

    def save_recycle_bin_prefs(self):
        """Save recycle bin preferences."""
        rb_prefs = {
            'enabled': self.rb_enable.isChecked(),
            'manage_age': self.rb_manage_age.isChecked(),
            'age_value': int(self.rb_age_value.text()) if self.rb_age_value.text() else 0,
            'age_unit': self.rb_age_unit.currentText(),
            'manage_size': self.rb_manage_size.isChecked(),
            'size_value': int(self.rb_size_value.text()) if self.rb_size_value.text() else 0,
            'size_unit': self.rb_size_unit.currentText(),
            'deletion_approach': self.rb_deletion_approach.currentText(),
            'auto_empty': self.rb_auto_empty.isChecked(),
            'empty_value': int(self.rb_empty_value.text()) if self.rb_empty_value.text() else 0,
            'empty_unit': self.rb_empty_unit.currentText()
        }

        self.config.update_preferences({'recycle_bin': rb_prefs})
        QMessageBox.information(
            self, "Saved Settings",
            "Your settings have been saved."
        )

    def save_preferences(self):
        """Save general preferences."""
        try:
            sleep_time = int(self.sleep_time_input.text())
            self.config.update_preferences({'sleep_time': sleep_time})
            QMessageBox.information(
                self, "Saved Settings",
                "Your settings have been saved."
            )
            self.rules_changed.emit()
        except ValueError:
            QMessageBox.warning(
                self, "Invalid Input",
                "Please enter a valid number for sleep time."
            )
