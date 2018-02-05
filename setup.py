# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='IJAL-interlinear',
    version='0.1.0',
    description='',
    long_description=readme,
    author='Paul Shannon',
    author_email='paul.thurmond.shannon@gmail.com',
    url='https://github.com/paul-shannon/IJAL-interlinear',
    license="MIT",
    packages=find_packages(exclude=('tests', 'docs'))
)

