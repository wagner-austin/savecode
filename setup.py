"""
setup.py - Packaging configuration for the savecode tool.
"""

from setuptools import setup, find_packages

setup(
    name='savecode',
    version='1.2.2',
    description='Save Python code from directories and files into one output file.',
    author='Austin Wagner',
    author_email='austinwagner@msn.com',
    url='https://github.com/wagner-austin',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'savecode=savecode.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
