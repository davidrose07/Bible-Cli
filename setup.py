
from setuptools import setup, find_packages


setup(
    name='bible_cli',
    version='0.1',
    packages=find_packages(),
    requires=[
        'click',
        'colorama'
    ],
    entry_points='''
    [console_scripts]
    bible=bible_cli:main

'''
)