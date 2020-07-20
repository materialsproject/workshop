from pathlib import Path

import numpy as np
from monty.serialization import loadfn

data_dir = Path(__file__).parent.resolve()

atomic_weights = loadfn(data_dir / "atomic_weights.json")
atomic_numbers = loadfn(data_dir / "atomic_numbers.json")
with open(data_dir / "words") as f:
    words = [line for line in f]


crystals = loadfn(data_dir / "crystals.json")
inflammation = np.loadtxt(data_dir / "inflammation-01.csv", delimiter=",")
