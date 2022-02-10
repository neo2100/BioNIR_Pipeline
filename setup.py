# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='bionir_pipeline',
    version='0.1.0',
    description='Sample package for information retrieval pipeline (BioNIR_Pipeline)',
    long_description=readme,
    author='Mohammadhadi Shadmehr',
    author_email='mohammad_sh2100@yahoo.com',
    url='https://github.com/neo2100/BioNIR_Pipeline',
    license=license,
    packages=find_packages(exclude=('tests', 'examples', 'docs'))
)