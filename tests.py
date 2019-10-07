import unittest

from easyappdirs.core import EasyAppDirs


class TestEasyAppDirs(unittest.TestCase):
    def setUp(self) -> None:
        self.dirs = EasyAppDirs(app_name="TestCase", app_author="Raphael")
        self.dirs.register_cache_file("dummy_cached_data.json")
        self.dirs.register_config_file("dummy_config.json")

    def test_path_creation(self):
        from os.path import exists
        self.assertTrue(exists(self.dirs.user_cache_dir))
        self.assertTrue(exists(self.dirs.user_data_dir))
        self.assertTrue(exists(self.dirs.user_cache_dir))
        self.assertTrue(exists(self.dirs.user_log_dir))
