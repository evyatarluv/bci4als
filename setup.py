from setuptools import setup, find_packages


# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='BCI4ALS',
    version='0.1.0',
    description='Setting up a python package',
    author='Evyatar Luvaton, Noam Siegel',
    author_email='luvaton@post.bgu.ac.il',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(include=['MI, SSVEP']),
    install_requires=[
        'PyYAML',
        'opencv-python',
        'keras',
        'scipy',
        'pyxdf',
        'numpy>=1.14.5',
        'mne',
        'pandas',
        'sklearn',
        'pylsl'
    ],
    extras_require={'plotting': ['matplotlib>=2.2.0', 'jupyter']},
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['record=MI.record_experiment:main']},
    setup_requires=['flake8']

)

