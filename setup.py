# -*- coding: utf-8 -*-

import os
import sys
import addendum

from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()


with open('README.rst') as f:
    readme = f.read()


setup(
    name='django-addendum',
    version=addendum.__version__,
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
