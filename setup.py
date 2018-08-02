#!/usr/bin/env python

import os

from setuptools import setup

module_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    setup(
        name='mp_workshop',
        version='2018.07.27',
        install_requires=["pymatgen", "jupyter"],
        description='Repository for workshop code',
        package_data={"mp_workshop.data.data_files": ["*.json"]},
        python_requires='>=3.6',
    )
