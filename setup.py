from setuptools import setup, find_packages

setup(
    name="DMM6500",
    version="0.1",
    packages=find_packages(),
    install_requires = [
        'pyvisa'
    ]
)
