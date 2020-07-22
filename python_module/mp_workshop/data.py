import os

import numpy as np

from monty.serialization import loadfn

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_files")
inflammation = np.loadtxt(os.path.join(data_dir, "inflammation-01.csv"), delimiter=",")
