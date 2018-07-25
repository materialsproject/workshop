# Get elemental data from pymatgen
import json

from pymatgen import Element

atomic_numbers = {e.symbol: e.Z for e in Element}
atomic_weights = {e.symbol: e.atomic_mass for e in Element}

with open('../data/atomic_numbers.json', 'w') as f:
    json.dump(atomic_numbers, f)
with open('../data/atomic_weights.json', 'w') as f:
    json.dump(atomic_weights, f)