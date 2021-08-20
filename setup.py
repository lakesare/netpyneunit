# -*- coding: utf-8 -*-

from setuptools import setup
import os
import sys

long_description = open("README.md").read()
with open('requirements.txt', 'r') as fp:
    install_requires = fp.read()

setup(
    name="netpyneunit",
    version='0.1.2',
    packages=['netpyneunit'],
    package_data={'netpyneunit':[
        os.path.join('tests','*.py'),
        os.path.join('models','*.py'),
        os.path.join('models/backends','*.py'),
        os.path.join('capabilities','*.py'),
        os.path.join('scores','*.py')],
    },
    install_requires=install_requires,
    extras_require={},
    author="Evgenia Karunus & Rick Gerkin",
    author_email="lakesare@gmail.com, rgerkin@asu.edu",
    description="A SciUnit library for testing of NetPyNE models.",
    long_description=long_description,
    license="MIT",
    url='https://github.com/rgerkin/netpyneunit',
    classifiers=[]
)
