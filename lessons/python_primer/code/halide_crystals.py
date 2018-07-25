from pymatgen import Element

halogens = []
for e in Element:
    if e.is_halogen:
        halogens.append(e)

halide_systems = []
for h in halogens:
    alkali_metals = []
    for e in Element:
        if e.is_alkali:
            alkali_metals.append(e)
    for m in alkali_metals:
        chemsys = "-".join(sorted([h.symbol, m.symbol]))
        halide_systems.append(chemsys)

halide_crystals = []
for c in crystals:
    if c['chemsys'] in halide_systems:
        halide_crystals.append(c)

formulae = []
for c in halide_crystals:
    formulae.append(c['pretty_formula'])

print(formulae)