from setuptools import setup

setup(
    name='easyappdirs',
    version='1.2.2',
    description='Wrapper for Appdirs that makes generating file paths easier',
    author='Raphael',
    author_email='rtnanje@gmail.com',
    packages=['easyappdirs'],  # same as name
    install_requires=['appdirs', 'logzero', 'pyyaml'],  # external packages as dependencies
)
