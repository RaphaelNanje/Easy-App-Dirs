import json
from os import mkdir, makedirs, walk
from os.path import join, exists, splitext

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
        if not exists(path):
            makedirs(path, exist_ok=True)
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

    def directory_load(self, path: str, recursive=False):
        """
        Load and register all files within the specified directory
        """
        for root, dirs, files in walk(path, topdown=False):
            for name in files:
                file_name = name
                short_name = splitext(name)[0] if splitext(name)[0] != file_name else None
                self.register_file(file_name, root, short_name)

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
