#!/usr/bin/env python

from distutils.core import setup

setup(
    name='pypi2bb',
    version='0.1',
    description='Convert PyPi packages to Yocto recipes.',
    author='Karol Krizka',
    author_email='kkrizka@gmail.com',
    scripts=['pypi2bb.py'],
    install_requires=['jinja2','requests','parsesetup']
)

