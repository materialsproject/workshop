from pathlib import Path

import os

os.environ["PMG_VASP_PSP_DIR"] = str(Path(__file__).parent.resolve())
