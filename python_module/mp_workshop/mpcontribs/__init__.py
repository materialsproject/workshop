import os
import gzip
import json
from pandas import DataFrame


def load_data():
    dbdir = os.path.dirname(__file__)
    dbpath = os.path.join(dbdir, "data.json.gz")

    with gzip.GzipFile(dbpath, "r") as f:
        data = json.loads(f.read().decode("utf-8"))

    for user, contributions in data.items():
        for contrib in contributions:
            for idx, dct in enumerate(contrib["tables"]):
                df = DataFrame(dct)
                df.index.name = contrib["data"].pop("tag")
                contrib["tables"][idx] = df

    return data


data = load_data()
