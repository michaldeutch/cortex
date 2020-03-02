from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='cortex',
    version='0.1.0',
    packages=find_packages(),
    author='Michal Deutch',
    description='Advanced System Design Project',
    install_requires=required,
    test_require=['pytest']
)
