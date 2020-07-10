"""
Module to setup fireworks config in any situation
"""
import os
from monty.serialization import dumpfn

fw_config = {
    "ADD_USER_PACKAGES": ["atomate.vasp.firetasks"],
    "CONFIG_FILE_DIR": os.path.dirname(os.path.abspath(__file__)),
    "ECHO_TEST": "Echo Test: MP Workshop",
    "QUEUE_UPDATE_INTERVAL": 5,
}

qadapter = {
    "_fw_name": "CommonAdapter",
    "_fw_q_type": "SLURM",
    "rocket_launch": "rlaunch -c "
    + os.path.dirname(os.path.abspath(__file__))
    + " singleshot",
    "nodes": 1,
    "walltime": "24:00:00",
    "job_name": None,
    "logdir": None,
    "pre_rocket": "export PATH=/opt/conda/bin:$PATH",
}

fw_config_dir = os.path.dirname(os.path.abspath(__file__))

fworker = {
    "name": "MP_Workshop",
    "query": "{}",
    "category": "",
    "env": {
        "db_file": os.path.join(fw_config_dir, "db.json"),
        "scratch_dir": None,
        "vasp_cmd": None,
    },
}

dumpfn(fw_config, os.path.join(fw_config_dir, "FW_config.yaml"))
dumpfn(
    qadapter,
    os.path.join(fw_config_dir, "my_qadapter.yaml"),
    indent=4,
    default_flow_style=False,
)
dumpfn(
    fworker,
    os.path.join(fw_config_dir, "my_fworker.yaml"),
    indent=4,
    default_flow_style=False,
)
