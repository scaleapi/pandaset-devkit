from distutils.core import setup

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='pandaset',
    version='0.1dev',
    packages=['pandaset'],
    python_requires='>=3.6',
    long_description='Pandaset Devkit for Python3',
    install_requires=requirements
)