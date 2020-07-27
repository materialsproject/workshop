from pathlib import Path

import pymatgen

pymatgen.SETTINGS["PMG_VASP_PSP_DIR"] = Path(__file__).parent.resolve()
