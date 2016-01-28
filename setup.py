# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'bookmarks',
]
requirements = []

setup(
    name='bookmarks',
    version='0.0.1',
    description='bookmarks',
    url='https://github.com/mozillazg/bookmarks',
    author='mozillazg',
    author_email='mozillazg101@gmail.com',
    license='MIT',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'bookmarks': 'bookmarks'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
)
