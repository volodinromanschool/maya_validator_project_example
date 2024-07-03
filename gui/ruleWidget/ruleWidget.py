from PySide2 import QtWidgets, QtCore, QtGui
import os
import maya.cmds as cmds

from .ruleTopPanel import RuleTopPanel
from .ruleListPanel import RuleListPanel

class RuleWidget(QtWidgets.QWidget):

    signal_validator_run = QtCore.Signal(str)
    signal_validator_fix = QtCore.Signal(str)

    def __init__(self, rule_name="test", rule_desc="desc", rule_instance=None):
        super(RuleWidget, self).__init__()

        self.rule_name = rule_name
        self.rule_description = rule_desc
        self.rule_instance = rule_instance
        self.setup_ui()

    def setup_ui(self):
        # main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 5, 0)
        self.setLayout(self.main_layout)

        # Top Panel
        self.top_panel = RuleTopPanel(self.rule_name)
        self.top_panel.signal_ListVisibility.connect(self.toggle_list_panel_visibility)
        self.top_panel.signal_RuleRun.connect(self.on_rule_run)
        self.top_panel.signal_RuleFix.connect(self.on_rule_fix)
        self.main_layout.addWidget(self.top_panel)

        # list Panel
        self.list_panel = RuleListPanel()
        self.list_panel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.main_layout.addWidget(self.list_panel)

    def rule_run_fix(self):
        self.rule_instance.fix()

    def rule_run_check(self):
        result = self.rule_instance.check()
        return result

    def recreate_list(self, new_list=[]):
        self.list_panel.clear_list()
        if new_list:
            for i in new_list:
                self.add_invalid_object(i)


    def get_rule_name(self):
        return self.rule_name

    def set_rule_name(self, name):
        self.rule_name = name
        self.top_panel.set_label(name)

    def get_rule_description(self):
        return self.rule_description

    def set_rule_description(self, description):
        self.rule_description = description
        self.list_panel.set_description(description)

    def add_invalid_object(self, obj):
        self.list_panel.add_item(obj)

    def toggle_list_panel_visibility(self):
        self.list_panel.toggle_visibility()

    def on_rule_run(self):
        self.signal_validator_run.emit(self.rule_name)

    def on_rule_fix(self):
        self.signal_validator_fix.emit(self.rule_name)

