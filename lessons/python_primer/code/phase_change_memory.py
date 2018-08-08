import random

from pymatgen import Element

from mp_workshop.data import crystals


def halogen(element):
    return element.is_halogen


def halide(crystal):
    elts = [Element(s) for s in crystal['elements']]
    anion = sorted(elts)[-1] # sorts by electronegativity
    return halogen(anion)


def chalcogen(element):
    return element.is_chalogen


def compound_class(crystal, predicate):
    # Fill this in.
    pass


my_crystal = random.sample(
    [c for c in crystals if halide(c)], 1)[0]

print(compound_class(my_crystal, halogen)
      == halide(my_crystal))