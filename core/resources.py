import os
import json
from MayaSceneValidator.core.config import Configurator
from MayaSceneValidator.core.common import read_json, log

root_ = os.path.dirname(__file__)
project_root_ = os.path.dirname(root_)

class Resources(object):
    __instance__ = None

    @staticmethod
    def get_instance():
        if not Resources.__instance__:
            Resources()
        return Resources.__instance__

    def __init__(self):
        if Resources.__instance__ is None:
            Resources.__instance__ = self
        else:
            raise Exception("Error Singleton")

        self.config_path = os.path.join(project_root_, "config.ini") # config.ini path
        self.preset_root = os.path.join(project_root_, "presets") # presets folder path
        self.preset_current = None  # current preset
        self.preset_current_path = None  # absolute path to the current preset
        self.preset_paths = []  # list of all presets absolute paths
        self.rules_root = os.path.join(project_root_, "rules")  # absolute path to rules folder
        self.rules_paths = []  # list of rules absolute paths
        self.config = None

        self.get_rules()
        self.get_presets()
        self.get_config()
        self.get_info()

    def get_config(self):
        """
        Creates configurator class instance
        :return: None
        """
        self.config = Configurator(config_path=self.config_path)
        self.config.init_config()
        self.get_current_preset_name()
        self.get_current_preset_path()

    def get_current_preset_name(self):
        self.preset_current = self.config.get_current_preset()

    def get_current_preset_path(self):
        self.preset_current_path = self.config.get_current_preset_path()

    def get_rules(self):
        self.rules_paths = []
        for path, folders, files in os.walk(self.rules_root):
            if path != self.rules_root:
                self.rules_paths.append(path)
        return self.rules_paths

    def get_presets(self):
        self.preset_paths = []
        for path, folders, files in os.walk(self.preset_root):
            for i in files:
                preset = os.path.join(path, i)
                self.preset_paths.append(preset)
        return self.preset_paths

    def get_current_preset_rules(self):
        json_data = read_json(self.preset_current_path)
        return json_data

    def get_preset_rules(self, preset_name=None):
        if not preset_name:
            return []
        for i in self.preset_paths:
            file_with_extension = os.path.split(i)[1]
            file_name = os.path.splitext(file_with_extension)[0]
            if preset_name == file_name:
                return read_json(i)

    def save_current_preset(self, preset=None):
        assert preset is not None, "preset is None"
        self.config.set_current_preset(preset=preset)

        for preset_path in self.preset_paths:
            if preset+".json" in preset_path:
                self.config.set_current_preset_path(preset_path=preset_path)
                break

        self.get_current_preset_name()
        self.get_current_preset_path()

    def get_info(self):

        #  print all rules found
        if self.rules_paths:
            for i in self.rules_paths:
                log(message=i, category="rule path")

        # print all presets found
        if self.preset_paths:
            for i in self.preset_paths:
                log(message=i, category="preset path")

        # print config.ini
        log(message="current preset = {}".format(self.preset_current), category="config.ini")
        log(message="current preset path = {}".format(self.preset_current_path), category="config.ini")

