"""
Rule editing dialog for Belvedere.

Provides interface for creating and editing file management rules.
"""

from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QCheckBox, QGroupBox, QFileDialog,
    QMessageBox, QWidget
)
from PySide6.QtCore import Qt
from typing import Optional, Tuple, Dict, Any, List


class RuleDialog(QDialog):
    """Dialog for creating and editing rules."""
    
    SUBJECTS = ['Name', 'Extension', 'Size', 'Date last modified', 
                'Date last opened', 'Date created']
    
    NAME_VERBS = ['is', 'is not', 'matches one of', 'does not match one of',
                  'contains', 'does not contain']
    
    NUM_VERBS = ['is', 'is not', 'is greater than', 'is less than']
    
    DATE_VERBS = ['is in the last', 'is not in the last']
    
    ACTIONS = ['Move file', 'Rename file', 'Send file to Recycle Bin',
               'Delete file', 'Copy file', 'Open file']
    
    SIZE_UNITS = ['MB', 'KB']
    DATE_UNITS = ['minutes', 'hours', 'days', 'weeks']
    
    def __init__(self, folder_path: str, existing_rule: Optional[Tuple[str, Dict[str, Any]]] = None, 
                 parent=None):
        """Initialize the rule dialog.
        
        Args:
            folder_path: Path to the folder this rule applies to.
            existing_rule: Tuple of (rule_name, rule_data) if editing existing rule.
            parent: Parent widget.
        """
        super().__init__(parent)
        self.folder_path = folder_path
        self.existing_rule = existing_rule
        self.condition_widgets = []
        
        self.init_ui()
        
        if existing_rule:
            self.load_rule(existing_rule)
    
    def init_ui(self):
        """Initialize the user interface."""
        if self.existing_rule:
            self.setWindowTitle("Edit Rule")
        else:
            self.setWindowTitle("Create a rule...")
        
        self.setGeometry(100, 100, 598, 348)
        
        layout = QVBoxLayout(self)
        
        # Folder label
        layout.addWidget(QLabel(f"Folder: {self.folder_path}"))
        
        # Description
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Description:"))
        self.description_input = QLineEdit()
        desc_layout.addWidget(self.description_input)
        layout.addLayout(desc_layout)
        
        # Rule options
        options_group = QGroupBox("Rule Options")
        options_layout = QVBoxLayout()
        
        self.enabled_check = QCheckBox("Enabled")
        self.enabled_check.setChecked(True)
        options_layout.addWidget(self.enabled_check)
        
        self.confirm_check = QCheckBox("Confirm Action")
        options_layout.addWidget(self.confirm_check)
        
        self.recursive_check = QCheckBox("Recursive")
        options_layout.addWidget(self.recursive_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Conditions header
        cond_header = QHBoxLayout()
        cond_header.addWidget(QLabel("If"))
        
        self.match_combo = QComboBox()
        self.match_combo.addItems(['ALL', 'ANY'])
        cond_header.addWidget(self.match_combo)
        
        cond_header.addWidget(QLabel("of the following conditions are met:"))
        cond_header.addStretch()
        layout.addLayout(cond_header)
        
        # Conditions container
        self.conditions_layout = QVBoxLayout()
        layout.addLayout(self.conditions_layout)
        
        # Add first condition
        self.add_condition()
        
        # Action section
        layout.addWidget(QLabel("Do the following:"))
        
        action_layout = QHBoxLayout()
        self.action_combo = QComboBox()
        self.action_combo.addItems(self.ACTIONS)
        self.action_combo.currentTextChanged.connect(self.update_destination_visibility)
        action_layout.addWidget(self.action_combo)
        
        self.dest_label = QLabel("to folder:")
        action_layout.addWidget(self.dest_label)
        
        self.destination_input = QLineEdit()
        action_layout.addWidget(self.destination_input)
        
        self.browse_btn = QPushButton("...")
        self.browse_btn.clicked.connect(self.browse_destination)
        action_layout.addWidget(self.browse_btn)
        
        self.overwrite_check = QCheckBox("Overwrite?")
        action_layout.addWidget(self.overwrite_check)
        
        layout.addLayout(action_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        test_btn = QPushButton("Test")
        test_btn.clicked.connect(self.test_rule)
        button_layout.addWidget(test_btn)
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.update_destination_visibility()
    
    def add_condition(self):
        """Add a new condition row."""
        condition_widget = QWidget()
        condition_layout = QHBoxLayout(condition_widget)
        condition_layout.setContentsMargins(0, 0, 0, 0)
        
        subject_combo = QComboBox()
        subject_combo.addItems(self.SUBJECTS)
        subject_combo.currentTextChanged.connect(
            lambda: self.update_verb_list(len(self.condition_widgets))
        )
        condition_layout.addWidget(subject_combo)
        
        verb_combo = QComboBox()
        verb_combo.addItems(self.NAME_VERBS)
        condition_layout.addWidget(verb_combo)
        
        object_input = QLineEdit()
        condition_layout.addWidget(object_input)
        
        units_combo = QComboBox()
        units_combo.setVisible(False)
        condition_layout.addWidget(units_combo)
        
        add_btn = QPushButton("+")
        add_btn.setFixedSize(20, 20)
        add_btn.clicked.connect(self.add_condition)
        condition_layout.addWidget(add_btn)
        
        if len(self.condition_widgets) > 0:
            remove_btn = QPushButton("-")
            remove_btn.setFixedSize(20, 20)
            remove_btn.clicked.connect(
                lambda: self.remove_condition(condition_widget)
            )
            condition_layout.addWidget(remove_btn)
        
        self.condition_widgets.append({
            'widget': condition_widget,
            'subject': subject_combo,
            'verb': verb_combo,
            'object': object_input,
            'units': units_combo
        })
        
        self.conditions_layout.addWidget(condition_widget)
    
    def remove_condition(self, widget: QWidget):
        """Remove a condition row.
        
        Args:
            widget: The condition widget to remove.
        """
        for i, cond in enumerate(self.condition_widgets):
            if cond['widget'] == widget:
                self.conditions_layout.removeWidget(widget)
                widget.deleteLater()
                self.condition_widgets.pop(i)
                break
    
    def update_verb_list(self, index: int):
        """Update verb list based on selected subject.
        
        Args:
            index: Index of the condition to update.
        """
        if index >= len(self.condition_widgets):
            return
        
        cond = self.condition_widgets[index]
        subject = cond['subject'].currentText()
        verb_combo = cond['verb']
        units_combo = cond['units']
        object_input = cond['object']
        
        # Clear and update verb list
        verb_combo.clear()
        
        if subject in ['Name', 'Extension']:
            verb_combo.addItems(self.NAME_VERBS)
            units_combo.setVisible(False)
            object_input.setMaximumWidth(140)
        elif subject == 'Size':
            verb_combo.addItems(self.NUM_VERBS)
            units_combo.clear()
            units_combo.addItems(self.SIZE_UNITS)
            units_combo.setVisible(True)
            object_input.setMaximumWidth(70)
        elif subject in ['Date last modified', 'Date last opened', 'Date created']:
            verb_combo.addItems(self.DATE_VERBS)
            units_combo.clear()
            units_combo.addItems(self.DATE_UNITS)
            units_combo.setVisible(True)
            object_input.setMaximumWidth(70)
    
    def update_destination_visibility(self):
        """Update visibility of destination controls based on action."""
        action = self.action_combo.currentText()
        
        if action in ['Move file', 'Copy file']:
            self.dest_label.setVisible(True)
            self.dest_label.setText("to folder:")
            self.destination_input.setVisible(True)
            self.browse_btn.setVisible(True)
            self.overwrite_check.setVisible(True)
        elif action == 'Rename file':
            self.dest_label.setVisible(True)
            self.dest_label.setText("to:")
            self.destination_input.setVisible(True)
            self.browse_btn.setVisible(False)
            self.overwrite_check.setVisible(False)
        else:  # Delete, Recycle, Open
            self.dest_label.setVisible(False)
            self.destination_input.setVisible(False)
            self.browse_btn.setVisible(False)
            self.overwrite_check.setVisible(False)
    
    def browse_destination(self):
        """Browse for destination folder."""
        folder = QFileDialog.getExistingDirectory(
            self, "Select Destination Folder"
        )
        if folder:
            self.destination_input.setText(folder)
    
    def load_rule(self, rule: Tuple[str, Dict[str, Any]]):
        """Load an existing rule into the dialog.
        
        Args:
            rule: Tuple of (rule_name, rule_data).
        """
        rule_name, rule_data = rule
        
        # Load basic info
        self.description_input.setText(rule_name)
        self.enabled_check.setChecked(rule_data.get('enabled', True))
        self.confirm_check.setChecked(rule_data.get('confirm_action', False))
        self.recursive_check.setChecked(rule_data.get('recursive', False))
        self.match_combo.setCurrentText(rule_data.get('match_type', 'ALL'))
        
        # Load conditions
        conditions = rule_data.get('conditions', [])
        # Remove default condition if we have existing ones
        if conditions:
            while self.condition_widgets:
                widget = self.condition_widgets[0]['widget']
                self.conditions_layout.removeWidget(widget)
                widget.deleteLater()
                self.condition_widgets.pop(0)
        
        for condition in conditions:
            self.add_condition()
            cond = self.condition_widgets[-1]
            cond['subject'].setCurrentText(condition.get('subject', 'Name'))
            self.update_verb_list(len(self.condition_widgets) - 1)
            cond['verb'].setCurrentText(condition.get('verb', 'is'))
            cond['object'].setText(condition.get('object', ''))
            if condition.get('units'):
                cond['units'].setCurrentText(condition['units'])
        
        # Load action
        self.action_combo.setCurrentText(rule_data.get('action', 'Move file'))
        self.destination_input.setText(rule_data.get('destination', ''))
        self.overwrite_check.setChecked(rule_data.get('overwrite', False))
    
    def get_rule(self) -> Tuple[str, Dict[str, Any]]:
        """Get the rule data from the dialog.
        
        Returns:
            Tuple of (rule_name, rule_data).
        """
        rule_name = self.description_input.text()
        
        conditions = []
        for cond in self.condition_widgets:
            condition = {
                'subject': cond['subject'].currentText(),
                'verb': cond['verb'].currentText(),
                'object': cond['object'].text(),
            }
            if cond['units'].isVisible():
                condition['units'] = cond['units'].currentText()
            conditions.append(condition)
        
        rule_data = {
            'folder': self.folder_path,
            'enabled': self.enabled_check.isChecked(),
            'confirm_action': self.confirm_check.isChecked(),
            'recursive': self.recursive_check.isChecked(),
            'match_type': self.match_combo.currentText(),
            'conditions': conditions,
            'action': self.action_combo.currentText(),
            'destination': self.destination_input.text(),
            'overwrite': self.overwrite_check.isChecked()
        }
        
        return rule_name, rule_data
    
    def test_rule(self):
        """Test the rule against files in the folder."""
        from .rule_engine import RuleEngine
        
        rule_name, rule_data = self.get_rule()
        
        # Validate rule
        if not rule_name:
            QMessageBox.warning(
                self, "Missing Description",
                "You need to write a description for your rule."
            )
            return
        
        # Test rule
        engine = RuleEngine()
        folder = Path(self.folder_path)
        matches = []
        
        if folder.exists():
            recursive = rule_data.get('recursive', False)
            if recursive:
                files = list(folder.rglob('*'))
            else:
                files = list(folder.glob('*'))
            
            files = [f for f in files if f.is_file()]
            
            for file_path in files:
                try:
                    if engine.evaluate_rule(file_path, rule_data):
                        matches.append(file_path.name)
                except Exception:
                    pass
        
        if matches:
            match_list = '\n'.join(matches[:20])  # Show first 20 matches
            if len(matches) > 20:
                match_list += f'\n... and {len(matches) - 20} more'
            QMessageBox.information(
                self, "Belvedere Test Matches",
                f"This rule matches the following file(s):\n\n{match_list}"
            )
        else:
            QMessageBox.information(
                self, "Belvedere Test Matches",
                "No matches were found"
            )
    
    def accept(self):
        """Validate and accept the dialog."""
        rule_name = self.description_input.text()
        
        if not rule_name:
            QMessageBox.warning(
                self, "Missing Description",
                "You need to write a description for your rule."
            )
            return
        
        if '|' in rule_name:
            QMessageBox.warning(
                self, "Invalid Character",
                "Your description cannot contain the | (pipe) character"
            )
            return
        
        # Validate conditions
        for cond in self.condition_widgets:
            if not cond['object'].text():
                QMessageBox.warning(
                    self, "Missing Data",
                    f"You're missing data in one of your {cond['subject'].currentText()} rules."
                )
                return
        
        # Validate destination for relevant actions
        action = self.action_combo.currentText()
        destination = self.destination_input.text()
        
        if action in ['Move file', 'Copy file', 'Rename file']:
            if not destination:
                QMessageBox.warning(
                    self, "Missing Destination",
                    f"You need to enter a destination folder for the {action} action."
                )
                return
            
            if action in ['Move file', 'Copy file']:
                dest_path = Path(destination)
                if not dest_path.exists():
                    QMessageBox.warning(
                        self, "Invalid Destination",
                        f"{destination} is not a real folder."
                    )
                    return
        
        super().accept()
