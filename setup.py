# setup.py

from setuptools import setup, find_packages

setup(
    name='s_lang',
    version='0.1.0',
    description='The swarmly language based on yaml and pydantic',
    author='Adrian Plani',
    author_email='adrian@swarmly.io',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)