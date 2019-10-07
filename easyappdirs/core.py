import json
from os import mkdir, makedirs
from os.path import join, exists

import appdirs
from logzero import logger


class EasyAppDirs(appdirs.AppDirs):
    def __init__(self, app_name, app_author, version=None, log_name="logs.log"):
        super().__init__(app_name, appauthor=app_author, version=version)
        self.file_paths = {}
        self.log_file_name = log_name

        if not exists(self.user_data_dir):
            mkdir(self.user_data_dir)
        if not exists(self.user_cache_dir):
            mkdir(self.user_cache_dir)
        if not exists(self.user_config_dir):
            mkdir(self.user_config_dir)
        if not exists(self.user_log_dir):
            mkdir(self.user_log_dir)

    def register_file(self, file_name: str, path: str, short_name: str = None):
        makedirs(path)
        path = join(path, file_name)
        self.file_paths[file_name] = path
        if short_name:
            self.file_paths[short_name] = path
        return self.file_paths[file_name]

    def register_config_file(self, file_name: str, short_name: str = None, folder: str = None):
        return self.register_file(file_name, join(self.user_config_dir, folder if folder else ''), short_name)

    def register_cache_file(self, file_name: str, short_name: str = None, folder: str = None):
        return self.register_file(file_name, join(self.user_cache_dir, folder if folder else ''), short_name)

    def register_data_file(self, file_name: str, short_name: str = None, folder: str = None):
        return self.register_file(file_name, join(self.user_data_dir, folder if folder else ''), short_name)

    def get_path(self, name: str):
        return self.file_paths[name]

    def set_log_name(self, log_file_name: str):
        self.log_file_name = log_file_name

    def directory_load(self):
        """
        TODO
        This function will automatically load all files from each folder and add them to self.file_paths
        """
        pass

    def load(self, name: str) -> dict:
        with open(self.get_path(name), "r") as f:
            return json.load(f)

    def save(self, name: str, data):
        with open(self.get_path(name), "w+") as f:
            json.dump(data, f, indent=2)

    def exists(self, name: str) -> bool:
        return exists(self.get_path(name))

    @property
    def log_path(self):
        return join(self.user_log_dir, self.log_file_name)
