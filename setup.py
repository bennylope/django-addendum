# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()


with open('README.rst') as f:
    readme = f.read()

with open("addendum/__init__.py", "r") as module_file:
    for line in module_file:
        if line.startswith("__version__"):
            version_string = line.split("=")[1]
            version = version_string.strip().replace("'", "")

setup(
    name='django-addendum',
    version=version,
    description='Simple template-based content swapping for CMS-less sites',
    long_description=readme,
    author='Ben Lopatin',
    author_email='ben.lopatin@wellfireinteractive.com',
    url='https://github.com/wellfire/django-addendum',
    license='BSD License',
    packages=find_packages(exclude=('example', 'docs')),
    platforms=['OS Independent'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
)
