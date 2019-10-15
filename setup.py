from setuptools import setup, find_packages
from flowcell_parser import __version__
import sys
import os
import glob
from io import open

try:
    with open("requirements.txt", "r") as f:
        install_requires = [x.strip() for x in f.readlines()]
except IOError:
    install_requires = []

setup(name = "flowcell_parser",
    version = __version__,
    author = "Denis Moreno",
    author_email = "denis.moreno@scilifelab.se",
    description = "Fetches data from demultiplexed flowcells and pushes it into statusdb",
    packages = find_packages(),
    scripts = glob.glob('scripts/*.py'),
    install_requires = install_requires
    )


