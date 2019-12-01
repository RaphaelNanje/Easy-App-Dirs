import unittest
from easyappdirs import EasyAppDirs

app_dirs = EasyAppDirs('easyappdirs_testing')


class MyTestCase(unittest.TestCase):

    def test_register(self):
        app_dirs.register_file('test.json', './testfiles', 'testj')
        app_dirs.register_file('test.yaml', './testfiles', 'testy')
        app_dirs.register_file('test.txt', './testfiles', 'testt')

        self.assertTrue('testj' in app_dirs.file_paths)
        self.assertTrue('testy' in app_dirs.file_paths)
        self.assertTrue('testt' in app_dirs.file_paths)


    def test_save(self):
        data = dict(
            a=1,
            b=2,
            c=3
        )

        app_dirs.smart_save('testj', data)
        app_dirs.smart_load('testj')
        app_dirs.smart_save('testy', data)
        app_dirs.smart_load('testy')
        app_dirs.smart_save('testt', data)
        app_dirs.smart_load('testt')



if __name__ == '__main__':
    unittest.main()
