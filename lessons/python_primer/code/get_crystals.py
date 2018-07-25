import json

from pymatgen import MPRester

mpr = MPRester()

props = ['elements', 'chemsys', 'spacegroup', 'pretty_formula']
data = mpr.query({'e_above_hull': 0}, props)

for d in data:
    to_remove = [k for k in d['spacegroup']
                 if k not in ('number', 'crystal_system')]
    for k in to_remove:
        del d['spacegroup'][k]

with open('../data/crystals.json', 'w') as f:
    json.dump(data, f)