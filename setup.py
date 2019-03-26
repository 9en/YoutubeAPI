# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='YoutubeAPI',
    version='1.0.0',
    description='get youtube data',
    long_description=readme,
    author='9en',
    author_email='mty.0613@gmail.com',
    python_requires='>=3.4',
    install_requires=['configparser', 'requests', 'pandas'],
    url='https://github.com/9en/YoutubeAPI',
    license=license,
    packages=find_packages()
)

