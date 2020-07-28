#!/usr/bin/env python

import os

from setuptools import setup, find_packages

module_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    setup(
        name="mp_workshop",
        author="The Materials Project",
        author_email="feedback@materialsproject.org",
        license="modified BSD",
        description="Dependencies for the MP Workshop",
        version="2020.07.10",
        url="https://workshop.materialsproject.org",
        packages=find_packages("python_module"),
        package_dir={"": "python_module"},
        install_requires=[
            "pymatgen",
            "atomate",
            "graphviz",
            "mpcontribs-client",
            "crystal-toolkit",
        ],
        package_data={"mp_workshop.data.data_files": ["*.json"]},
        python_requires=">=3.7",
    )
