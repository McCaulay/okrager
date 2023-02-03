#!/usr/bin/env python
# okrager - Command line tool to inject a PS2 ELF into an Okage game save file.

import os
from setuptools import setup

PACKAGE_NAME = 'okrager'
VERSION = '0.1.0'

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename), 'r').read()

setup(
    name=PACKAGE_NAME,
    description='Command line tool to inject a PS2 ELF into an Okage Shadow King game save file',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    version=VERSION,
    author='McCaulay Hudson',
    maintainer='McCaulay Hudson',
    author_email='mccaulayhudson@protonmail.com',
    url='https://github.com/McCaulay/okrager',
    keywords='ps2 gamesave psu okage shadow king mast1c0re',
    platforms=['Unix', 'Windows'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=[
        'okrager',
    ],
    package_data={
        'okrager': [
            'stagers/bin/*.bin',
        ],
    },
    scripts=[
        'bin/okrager',
    ],
    install_requires=[
        'mymcplus==3.0.5',
        'pypsu==0.1.2',
    ],
    options={
        'bdist_wheel': {
            'universal': True,
        }
    }
)