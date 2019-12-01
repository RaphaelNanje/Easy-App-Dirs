import unittest

from easyappdirs import EasyAppDirs

app_dirs = EasyAppDirs('easyappdirs_testing')


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        import os
        os.mkdir('testfiles')
        for i, folder in enumerate('testfolder' + str(i) for i in range(5)):
            if not os.path.exists(folder):
                os.mkdir(os.path.join('testfiles', folder))
            for file in [f'testfile{i}{j}.json' for j in range(2)]:
                with open(os.path.join('testfiles', folder, file), 'w') as f:
                    f.write('')

    def test_directory_load(self):
        app_dirs.directory_load('./testfiles/', True)
        for i in range(5):
            for file in [f'testfile{i}{j}.json' for j in range(2)]:
                self.assertIn(file, app_dirs.file_paths)

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
        self.assertIsNotNone(app_dirs.smart_load('testj'))
        app_dirs.smart_save('testy', data)
        self.assertIsNotNone(app_dirs.smart_load('testy'))
        app_dirs.smart_save('testt', data)
        self.assertIsNotNone(app_dirs.smart_load('testt'))

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        import shutil
        shutil.rmtree('./testfiles/')


if __name__ == '__main__':
    unittest.main()
