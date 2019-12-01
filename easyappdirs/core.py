import json
import os
from os import mkdir, makedirs, walk, listdir
from os.path import join, exists, splitext, isfile
from typing import Iterable

import appdirs
import yaml
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
        self.file_types = {}
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

    def load(self, name: str, split=True, strip=True):
        """
        :param split: readlines() instead of read() if True
        :param strip: call strip() on each line
        """
        self.file_types[name] = 'normal'
        with open(self.get_path(name), "r") as f:
            if split:
                return [t.strip() if strip else t for t in f.readlines()]
            else:
                return f.read()

    def json_load(self, name: str, **kwargs) -> dict:
        self.file_types[name] = 'json'
        with open(self.get_path(name), "r") as f:
            return json.load(f, **kwargs)

    def yaml_load(self, name: str, loader=yaml.FullLoader) -> dict:
        self.file_types[name] = 'yaml'
        with open(self.get_path(name), "r") as f:
            return yaml.load(f, loader)

    def save(self, name: str, data):
        self.file_types[name] = 'normal'
        with open(self.get_path(name), "w+") as f:
            if not isinstance(data, Iterable):
                f.write(data)
            else:
                f.writelines(data)

    def json_save(self, name: str, data, default=None, **kwargs):
        self.file_types[name] = 'json'
        with open(self.get_path(name), "w+") as f:
            json.dump(data, f, indent=2, default=default, **kwargs)

    def yaml_save(self, name: str, data, **kwargs):
        self.file_types[name] = 'yaml'
        with open(self.get_path(name), "w+") as f:
            yaml.dump(data, f, indent=2, **kwargs)

    def exists(self, name: str) -> bool:
        return exists(self.get_path(name))

    def smart_save(self, name, data):
        """
        Automatically saves based on the file type.
        Supports JSON/YAML and will do a regular save for everything else
        """

        ext = os.path.splitext(self.file_paths[name])[1]
        if ext == 'yaml':
            self.yaml_save(name, data)
        elif ext == 'json':
            self.json_save(name, data)
        else:
            self.save(name, data)

    def smart_load(self, name, data):
        """
        Automatically loads based on the file type.
        Supports JSON/YAML and will do a regular load for everything else
        """

        ext = os.path.splitext(self.file_paths[name])[1]
        if ext == 'yaml':
            self.yaml_load(name)
        elif ext == 'json':
            self.json_load(name)
        else:
            self.load(name)

    @property
    def log_path(self):
        return join(self.user_log_dir, self.log_file_name)
