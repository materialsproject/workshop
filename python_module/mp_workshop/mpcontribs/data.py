# flake8: noqa
import os
import gzip

userfile = os.path.join(dbdir, "usernames")
with open(userfile, "r") as f:
    users = f.readlines()

dbdir = os.path.dirname(__file__)
dbpath = os.path.join(dbdir, "raw_data.json.gz")

with gzip.GzipFile(dbpath, "r") as f:
    raw_data = json.loads(f.read().decode("utf-8"))

data = {}
formulas = list(raw_data.keys())
for user, formula in zip(users, formulas):
    data[user.strip()] = raw_data[formula]

outfile = os.path.join(dbdir, "data.json.gz")
with gzip.open(outfile, "wb") as f:
    content = json.dumps(data).encode("utf-8")
    f.write(content)
