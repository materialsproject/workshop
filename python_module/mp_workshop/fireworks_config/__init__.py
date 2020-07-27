"""
Module to setup fireworks config in any situation
"""
import os
from pathlib import Path

from monty.serialization import dumpfn


fw_config_dir = Path(__file__).parent.resolve()


fw_config = {
    "ADD_USER_PACKAGES": ["atomate.vasp.firetasks"],
    "CONFIG_FILE_DIR": str(fw_config_dir),
    "ECHO_TEST": "FW Echo Test: MP Workshop",
    "QUEUE_UPDATE_INTERVAL": 5,
}


fworker = {
    "name": "MP_Workshop",
    "query": "{}",
    "category": "",
    "env": {
        "db_file": str(fw_config_dir / "db.json"),
        "scratch_dir": None,
        "vasp_cmd": None,
    },
}


dumpfn(fw_config, fw_config_dir / "FW_config.yaml")
dumpfn(
    fworker, fw_config_dir / "my_fworker.yaml", indent=4, default_flow_style=False,
)


os.environ["FW_CONFIG_FILE"] = str(fw_config_dir / "FW_config.yaml")
