import json
import os
from os import mkdir, makedirs, walk, listdir
from os.path import join, exists, splitext, isfile

import appdirs
from logzero import logger

from easyappdirs.exceptions import NameAlreadyRegisteredError


class EasyAppDirs(appdirs.AppDirs):
    current_file_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, app_name, app_author, version=None, log_name="logs.log", override=False):
        """
        :param override: Set this to True to override paths of names that have already been registered
        """
        super().__init__(app_name, appauthor=app_author, version=version)
        self.file_paths = {}
        self.log_file_name = log_name
        self.override = False

        if not exists(self.user_data_dir):
            mkdir(self.user_data_dir)
        if not exists(self.user_cache_dir):
            mkdir(self.user_cache_dir)
        if not exists(self.user_config_dir):
            mkdir(self.user_config_dir)
        if not exists(self.user_log_dir):
            mkdir(self.user_log_dir)

    def register_file(self, file_name: str, path: str = current_file_dir, short_name: str = None):
        if file_name in self.file_paths:
            if join(path, file_name) == self.file_paths[file_name]:
                return self.file_paths[file_name]
            elif not self.override and self.file_paths[file_name] != join(path, file_name):
                raise NameAlreadyRegisteredError(
                    f"Override is set to {self.override} and '{file_name}' has already been registered.", file_name,
                    path)
            else:
                logger.info(
                    f"'{file_name}' already exists and is pointing to '{self.file_paths[file_name]}'... Overriding.")
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
        if not recursive:
            files = [f for f in listdir(path) if isfile(join(path, f))]
            for file in files:
                self.register_file(file, path, splitext(file)[0] if splitext(file)[0] != file else None)
            return files
        else:
            files_list = []
            for root, dirs, files in walk(path, topdown=True):
                for name in files:
                    file_name = name
                    short_name = splitext(name)[0] if splitext(name)[0] != file_name else None
                    self.register_file(file_name, root, short_name)
                    files_list.append(file_name)
            return files_list

    def load(self, name: str) -> object:
        with open(self.get_path(name), "r") as f:
            return f.readlines()

    def json_load(self, name: str) -> dict:
        with open(self.get_path(name), "r") as f:
            return json.load(f)

    def save(self, name: str, data):
        with open(self.get_path(name), "w+") as f:
            f.write(data)

    def json_save(self, name: str, data, default=None, **kwargs):
        with open(self.get_path(name), "w+") as f:
            json.dump(data, f, indent=2, default=default, **kwargs)

    def exists(self, name: str) -> bool:
        return exists(self.get_path(name))

    @property
    def log_path(self):
        return join(self.user_log_dir, self.log_file_name)
