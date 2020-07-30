# flake8: noqa
import os
import yaml
import json
import gzip
from zipfile import ZipFile
from collections import defaultdict
from pandas import read_csv
from pymatgen import MPRester
from tqdm.notebook import tqdm
from urllib.parse import quote


mpr = MPRester()
dbdir = os.path.dirname(__file__)
dbpath = os.path.join(dbdir, "rii-database-2020-01-19.zip")
url = "https://refractiveindex.info/data_csv.php?datafile={}"
raw_data = defaultdict(list)

with ZipFile(dbpath) as zf:
    paths = zf.namelist()
    for path in tqdm(paths):
        if path.startswith("database/data/main") and path.endswith(".yml"):
            _, formula, fn = path.rsplit("/", 2)
            mat_ids = mpr.get_materials_ids(formula)
            if not mat_ids:
                continue

            tag = fn.split(".", 1)[0]
            contrib = {"identifier": mat_ids[0], "data": {"tag": tag}, "tables": []}
            try:
                dct = yaml.safe_load(zf.read(path))
            except Exception:
                continue

            for k, v in dct["DATA"][0].items():
                vals = v.split()
                if k == "type":
                    contrib["data"][k] = "f" + vals[-1]
                elif k == "wavelength_range":
                    contrib["data"]["Δλ"] = {
                        "min": f"{vals[0]} µm",
                        "max": f"{vals[1]} µm",
                    }
                elif k == "coefficients":
                    contrib["data"][k] = {f"c{idx}": c for idx, c in enumerate(vals)}

            datafile = quote(path.split("/", 1)[-1])
            df = read_csv(url.format(datafile))
            contrib["tables"].append(df.to_dict(orient="records"))
            raw_data[formula].append(contrib)

            if len(raw_data) == 200:
                break


outfile = os.path.join(dbdir, "raw_data.json.gz")
with gzip.open(outfile, "wb") as f:
    content = json.dumps(raw_data).encode("utf-8")
    f.write(content)
